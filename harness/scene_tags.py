"""Scene tags: which stress-test scenarios each downloaded scene holds.

Five categories: lead_vehicle, unprotected_left, merge_cut_in, intersection,
pedestrian_crossing. A scene may have several. Two sources tag each scene of
S1 (its first kept run) independently:

- rules, from the recorded drive: the ego's turn, stops and lateral shift, the
  vehicle ahead in its lane, cars cutting in or crossing its path, oncoming
  cars at a left turn, and pedestrians near its path. Every rule tag carries
  its numbers. The recorded tracks come from the run's rollout.asl (the
  traffic session request carries every logged track with its class, the
  ego's included) or, for a scene without a run, from its scene file, cut to
  the window an S1 rollout covers (`file_tracks`). Both feed `scene_facts`.
- Claude, on three frames of the run's video (start, middle, near the end)
  under advisor/TAGS.md, reading only those frames.

A final tag is one Claude gives: confirmed (the rules found it too, "agree")
or added ("claude"). Tags only the rules found stay visible as "rules".
Writes scene_tags.json and scene_tags_check.md (20 scenes for a person to
verify) and prints the counts per category. Frames and Claude's answers are
kept in diag/scene_tags_frames/.

A scene with a file on disk but no run is tagged from the file alone with
`--files`: rule tags only, each with source "rules (file)", and they are its
final tags until a run lets Claude check them. `--files` adds such scenes to
scene_tags.json and leaves every entry already there unchanged; tagging the
S1 runs again keeps the file-tagged scenes that still have no run.
`--compare N` checks the two track sources against each other on N scenes
that have both.

    uv run python research/harness/scene_tags.py           # every kept S1 scene
    uv run python research/harness/scene_tags.py --reuse   # keep saved answers
    uv run python research/harness/scene_tags.py --files   # files without a run
    uv run python research/harness/scene_tags.py --compare 10
"""

import argparse
import asyncio
import csv
import json
import random
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
from alpasim_utils.artifact import Artifact
from alpasim_utils.geometry import Pose, Trajectory
from alpasim_utils.logs import async_read_pb_log
from alpasim_utils.scenario import Rig
from alpasim_utils.scene_data_source import SceneDataSource

sys.path.insert(0, str(Path(__file__).resolve().parent))

from headless import ask
from read_state import ROOT, load_entry, queue_entries

from physics import EGO, LANE_HALF_WIDTH_M, _yaw, completed_rollout

HARNESS = Path(__file__).resolve().parent
QUEUE = HARNESS / "s1_queue"
OUTPUT = HARNESS / "scene_tags.json"
CHECK = HARNESS / "scene_tags_check.md"
FRAMES = ROOT / "diag" / "scene_tags_frames"
CONTRACT = HARNESS / "advisor" / "TAGS.md"
SCENE_FILES = ROOT / "data" / "nre-artifacts" / "all-usdzs"
CATALOG = ROOT / "data" / "scenes" / "sim_scenes.csv"
# Smaller files are downloads still in progress (download_scenes.py, MIN_SIZE).
COMPLETE_BYTES = 100_000_000
FILE_SOURCE = "rules (file)"
MODEL = "claude-opus-5-5"
# The rollout S1 runs (simulation_config in every S1 run's
# generated-user-config-0.yaml): no start offset, 120 control steps of 0.1 s
# from the first front-camera frame (4.5 s force-GT warm-up, then 7.5 s closed
# loop), logged traffic kept when it lasts 3 s or more within the window.
S1_CAMERA = "camera_front_wide_120fov"
S1_STEPS = 120
S1_STEP_US = 100_000
S1_MIN_TRAFFIC_US = 3_000_000
CATEGORIES = (
    "lead_vehicle",
    "unprotected_left",
    "merge_cut_in",
    "intersection",
    "pedestrian_crossing",
)
KINDS = {
    "automobile": "vehicle",
    "heavy_truck": "vehicle",
    "trailer": "vehicle",
    "bus": "vehicle",
    "other_vehicle": "vehicle",
    "train_or_tram_car": "vehicle",
    "person": "pedestrian",
    "stroller": "pedestrian",
    "rider": "cyclist",
    "protruding_object": "other",
    "animal": "other",
}
# A track counts as near the ego when it comes this close to the recorded path.
NEAR_PATH_M = 30.0
PEDESTRIAN_NEAR_M = 5.0
# Lower than a full 90 degrees: a 12 s recording often holds only part of a turn.
TURN_DEG = 50.0
STOPPED_MPS = 0.5
MOVING_MPS = 1.0
# The path is extended straight ahead so that actors past where the recording
# ends (a car the ego stops behind) still project onto it.
EXTEND_M = 60.0
LEAD_RANGE_M = 30.0
LEAD_MIN_S = 2.0
LEAD_SLOWS_MPS = 2.0
ALIGNED_DEG = 30.0
# A cut-in: a car alongside or ahead moves from the next lane into the ego's.
CUT_IN_FROM_M = 2.5
CUT_IN_TO_M = 1.0
CUT_IN_AHEAD_M = (-5.0, 40.0)
# Crossing traffic crosses the path at this angle, up to this far past its end.
CROSSING_DEG = (45.0, 135.0)
CROSSING_AHEAD_M = 30.0
ONCOMING_DEG = 45.0
ONCOMING_NEAR_TURN_M = 40.0
# An ego lane change shows as cars around it shifting this far sideways
# relative to its path (below).
LANE_SHIFT_M = 2.5
LANE_SHIFT_SEARCH_M = 8.0
LANE_SHIFT_SPAN_M = 20.0
SCHEMA = {
    "type": "object",
    "properties": {
        "road_type": {
            "type": "string",
            "enum": ["urban", "suburban", "highway", "parking"],
        },
        "intersection_present": {"type": "boolean"},
        "crosswalk_visible": {"type": "boolean"},
        "pedestrians_visible": {"type": "boolean"},
        "traffic_lights_visible": {"type": "boolean"},
        "ego_maneuver": {
            "type": "string",
            "enum": ["straight", "left_turn", "right_turn", "lane_change", "merge"],
        },
        "categories": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "category": {"type": "string", "enum": list(CATEGORIES)},
                    "reason": {"type": "string"},
                },
                "required": ["category", "reason"],
                "additionalProperties": False,
            },
        },
    },
    "required": [
        "road_type",
        "intersection_present",
        "crosswalk_visible",
        "pedestrians_visible",
        "traffic_lights_visible",
        "ego_maneuver",
        "categories",
    ],
    "additionalProperties": False,
}


def _track(label: str, static: bool, times_us, start_us: int, xy, yaw) -> dict:
    """One recorded track as `scene_facts` reads it: times in seconds from
    `start_us`, positions in the plane, unwrapped yaw."""
    return {
        "label": label,
        "static": static,
        "t": (np.asarray(times_us, dtype=np.int64) - start_us) / 1e6,
        "xy": np.asarray(xy, dtype=float)[:, :2],
        "yaw": np.unwrap(np.asarray(yaw, dtype=float)),
    }


async def logged_tracks(path: Path) -> dict:
    """Every logged track, the ego's recorded drive included, in seconds from
    the start of the ego's recording."""
    async for message in async_read_pb_log(str(path)):
        if message.WhichOneof("log_entry") == "traffic_session_request":
            logged = message.traffic_session_request.logged_object_trajectories
            start = next(o for o in logged if o.object_id == EGO).trajectory.poses[0]
            return {
                obj.object_id: _track(
                    obj.label_class,
                    obj.is_static,
                    [p.timestamp_us for p in obj.trajectory.poses],
                    start.timestamp_us,
                    [(p.pose.vec.x, p.pose.vec.y) for p in obj.trajectory.poses],
                    [_yaw(p.pose.quat) for p in obj.trajectory.poses],
                )
                for obj in logged
            }
    raise ValueError(f"{path}: no traffic_session_request")


def rollout_window_us(rig: Rig) -> tuple[int, int]:
    """Start and end of the recording an S1 rollout covers, as
    UnboundRollout.create derives them with S1's settings: from the start of
    the ego's recording to S1_STEPS control steps after the front camera's
    first frame closes, or as many whole steps as fit before the recording
    ends. The force-GT warm-up and the closed loop both lie inside it, so the
    facts describe the recorded scene over all the time a rollout simulates,
    the same tracks the run log carries."""
    start, stop = rig.trajectory.time_range_us.start, rig.trajectory.time_range_us.stop
    first_frame = rig.first_camera_frame_end_us([S1_CAMERA])
    steps = min(S1_STEPS, (stop - 1 - first_frame) // S1_STEP_US)
    if steps <= 0:
        raise ValueError(f"{rig.sequence_id}: no control step fits in the recording")
    return start, first_frame + steps * S1_STEP_US


def _box_centre(trajectory: Trajectory, rig: Rig) -> Trajectory:
    """The ego's recorded rig poses moved to the centre of its box, as the
    runtime logs the ego (get_ds_rig_to_aabb_center_transform)."""
    if rig.vehicle_config is None:
        raise ValueError(f"{rig.sequence_id}: no vehicle config in the scene file")
    vehicle = rig.vehicle_config
    offset = np.array(
        [
            vehicle.aabb_x_offset_m + vehicle.aabb_x_m / 2,
            vehicle.aabb_y_offset_m,
            vehicle.aabb_z_offset_m + vehicle.aabb_z_m / 2,
        ],
        dtype=np.float32,
    )
    return trajectory.transform(
        Pose(offset, np.array([0.0, 0.0, 0.0, 1.0], dtype=np.float32)),
        is_relative=True,
    )


def file_tracks(scene: SceneDataSource) -> dict:
    """Every recorded track of a scene file over the window an S1 rollout
    covers (`rollout_window_us`), shaped as `logged_tracks` returns them: the
    ego at its box centre, and the traffic AlpaSim keeps (cubic-spline
    smoothed by the loader, clipped to the window, at least S1_MIN_TRAFFIC_US
    long)."""
    rig = scene.rig
    start, end = rollout_window_us(rig)
    ego = _box_centre(rig.trajectory.clip(start, end + 1), rig)
    traffic = scene.traffic_objects.clip_trajectories(
        start, end + 1, exclude_empty=True
    ).filter_short_trajectories(S1_MIN_TRAFFIC_US)
    tracks = {EGO: _track("", False, ego.timestamps_us, start, ego.positions, ego.yaws)}
    for actor, obj in traffic.items():
        path = obj.trajectory
        tracks[actor] = _track(
            obj.label_class,
            obj.is_static,
            path.timestamps_us,
            start,
            path.positions,
            path.yaws,
        )
    return tracks


def speeds(t: np.ndarray, xy: np.ndarray) -> np.ndarray:
    if len(t) < 2:
        return np.zeros(len(t))
    return np.hypot(np.gradient(xy[:, 0], t), np.gradient(xy[:, 1], t))


def reference_path(xy: np.ndarray, yaw: np.ndarray, ahead_m: float) -> np.ndarray:
    """The recorded path without its standstill repeats, extended `ahead_m`
    straight along the final heading."""
    keep = [xy[0]]
    for point in xy[1:]:
        if np.hypot(*(point - keep[-1])) > 0.01:
            keep.append(point)
    end = keep[-1] + ahead_m * np.array([np.cos(yaw[-1]), np.sin(yaw[-1])])
    return np.array([*keep, end]) if ahead_m > 0 else np.array(keep)


def project(path: np.ndarray, points: np.ndarray) -> dict:
    """For each point: arc length along `path` to its nearest path point, the
    signed offset from the path (left positive), the distance, and the path's
    heading there."""
    if len(path) == 1:
        dist = np.hypot(*(points - path[0]).T)
        return {
            "s": np.zeros(len(points)),
            "d": dist,
            "dist": dist,
            "heading": np.zeros(len(points)),
        }
    a, seg = path[:-1], np.diff(path, axis=0)
    length = np.hypot(seg[:, 0], seg[:, 1])
    rel = points[:, None, :] - a[None, :, :]
    along = np.clip((rel * seg).sum(axis=2) / length**2, 0.0, 1.0)
    foot = a[None] + along[..., None] * seg[None]
    dist = np.hypot(*(points[:, None, :] - foot).transpose(2, 0, 1))
    nearest = dist.argmin(axis=1)
    rows = np.arange(len(points))
    cross = (
        seg[nearest, 0] * rel[rows, nearest, 1]
        - seg[nearest, 1] * rel[rows, nearest, 0]
    )
    starts = np.concatenate([[0.0], np.cumsum(length)])
    return {
        "s": starts[nearest] + along[rows, nearest] * length[nearest],
        "d": np.where(cross < 0, -1.0, 1.0) * dist[rows, nearest],
        "dist": dist[rows, nearest],
        "heading": np.arctan2(seg[nearest, 1], seg[nearest, 0]),
    }


def _angle_deg(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Unsigned angle between headings, 0 to 180 degrees."""
    return np.degrees(np.abs((a - b + np.pi) % (2 * np.pi) - np.pi))


def heading_change_deg(yaw: np.ndarray) -> float:
    """Net heading change over the drive; positive turns left (y points left)."""
    return float(np.degrees(yaw[-1] - yaw[0]))


def _at(track: dict, times: np.ndarray) -> dict:
    """A track interpolated to `times`, where it exists."""
    inside = (times >= track["t"][0]) & (times <= track["t"][-1])
    at = times[inside]
    speed = speeds(track["t"], track["xy"])
    return {
        "t": at,
        "index": np.flatnonzero(inside),
        "xy": np.column_stack(
            [np.interp(at, track["t"], track["xy"][:, k]) for k in (0, 1)]
        ),
        "yaw": np.interp(at, track["t"], track["yaw"]),
        "speed": np.interp(at, track["t"], speed),
    }


def ego_facts(ego: dict) -> dict:
    t, xy, yaw = ego["t"], ego["xy"], ego["yaw"]
    speed = speeds(t, xy)
    stopped = speed < STOPPED_MPS
    dt = np.gradient(t)
    change = heading_change_deg(yaw)
    turn = "none"
    if abs(change) > TURN_DEG:
        turn = "left" if change > 0 else "right"
    return {
        "duration_s": round(float(t[-1] - t[0]), 1),
        "distance_m": round(float(np.sum(np.hypot(*np.diff(xy, axis=0).T))), 1),
        "max_speed_mps": round(float(speed.max()), 1),
        "stopped_s": round(float(dt[stopped].sum()), 1),
        "stops": int(np.sum(np.diff(stopped.astype(int)) == 1) + stopped[0]),
        "heading_change_deg": round(change, 1),
        "turn": turn,
    }


def lead(ego: dict, s_ego: np.ndarray, path: np.ndarray, vehicles: dict) -> dict | None:
    """The vehicle nearest ahead in the ego's lane for longest (within
    LANE_HALF_WIDTH_M of its path, heading the same way, at most LEAD_RANGE_M
    ahead centre to centre), with how it moved while it led."""
    nearest = np.full(len(ego["t"]), np.inf)
    who = np.full(len(ego["t"]), "", dtype=object)
    seen = {}
    for actor, track in vehicles.items():
        at = _at(track, ego["t"])
        if not len(at["t"]):
            continue
        p = project(path, at["xy"])
        gap = p["s"] - s_ego[at["index"]]
        in_lane = (
            (np.abs(p["d"]) < LANE_HALF_WIDTH_M)
            & (_angle_deg(at["yaw"], p["heading"]) < ALIGNED_DEG)
            & (gap > 0)
            & (gap <= LEAD_RANGE_M)
        )
        for k, i in enumerate(at["index"]):
            if in_lane[k] and gap[k] < nearest[i]:
                nearest[i], who[i] = gap[k], actor
        seen[actor] = (at, gap)
    leaders = [actor for actor in who if actor]
    if not leaders:
        return None
    actor = max(sorted(set(leaders)), key=leaders.count)
    at, gap = seen[actor]
    led = np.isin(at["index"], np.flatnonzero(who == actor))
    speed = at["speed"][led]
    drop = max(float(speed[k] - speed[k:].min()) for k in range(len(speed)))
    dt = float(np.median(np.diff(ego["t"])))
    return {
        "actor": actor,
        "label": vehicles[actor]["label"],
        "lead_s": round(leaders.count(actor) * dt, 1),
        "min_gap_m": round(float(gap[led].min()), 1),
        "max_speed_mps": round(float(speed.max()), 1),
        "min_speed_mps": round(float(speed.min()), 1),
        "speed_drop_mps": round(drop, 1),
    }


def cut_ins(ego: dict, s_ego: np.ndarray, path: np.ndarray, vehicles: dict) -> list:
    """Moving vehicles alongside or ahead that move from the next lane
    (CUT_IN_FROM_M or more to the side of the ego's path) into its lane."""
    found = []
    for actor, track in vehicles.items():
        at = _at(track, ego["t"])
        if not len(at["t"]):
            continue
        p = project(path, at["xy"])
        gap = p["s"] - s_ego[at["index"]]
        near = (
            (gap > CUT_IN_AHEAD_M[0])
            & (gap < CUT_IN_AHEAD_M[1])
            & (_angle_deg(at["yaw"], p["heading"]) < ALIGNED_DEG)
            & (at["speed"] > MOVING_MPS)
        )
        side = np.abs(p["d"])
        for k in np.flatnonzero(near & (side >= CUT_IN_FROM_M)):
            inside = np.flatnonzero(near & (side <= CUT_IN_TO_M) & (gap > 0))
            later = inside[inside > k]
            if len(later):
                found.append(
                    {
                        "actor": actor,
                        "label": track["label"],
                        "from_m": round(float(p["d"][k]), 1),
                        "at_s": round(float(at["t"][later[0]]), 1),
                        "gap_m": round(float(gap[later[0]]), 1),
                    }
                )
                break
    return found


def lane_change(path: np.ndarray, path_length: float, vehicles: dict) -> dict:
    """The ego's lane change, read from the cars around it. A car that keeps
    its lane sits at a fixed offset from the ego's recorded path up to where
    the path changes lanes, and a lane width further over after it. Each
    moving car heading along the path within LANE_SHIFT_SEARCH_M of it, over
    at least LANE_SHIFT_SPAN_M of it, shifts by its last offset minus its
    first. The ego changed lanes when two or more cars shift LANE_SHIFT_M or
    more one way and at most half as many the other way; the ego's shift is
    the opposite of their median, positive to the left."""
    shifts = []
    for track in vehicles.values():
        p = project(path, track["xy"])
        along = np.flatnonzero(
            (np.abs(p["d"]) < LANE_SHIFT_SEARCH_M)
            & (p["s"] > 0)
            & (p["s"] < path_length)
            & (_angle_deg(track["yaw"], p["heading"]) < ALIGNED_DEG)
            & (speeds(track["t"], track["xy"]) > MOVING_MPS)
        )
        if (
            len(along) >= 10
            and p["s"][along[-1]] - p["s"][along[0]] >= LANE_SHIFT_SPAN_M
        ):
            shifts.append(
                float(np.median(p["d"][along[-5:]]) - np.median(p["d"][along[:5]]))
            )
    left = [s for s in shifts if s <= -LANE_SHIFT_M]
    right = [s for s in shifts if s >= LANE_SHIFT_M]
    same, other = max(left, right, key=len), min(left, right, key=len)
    changed = len(same) >= 2 and len(other) <= len(same) / 2
    return {
        "shift_m": round(-float(np.median(same)), 1) if changed else 0.0,
        "cars_shifted": len(same),
        "cars_shifted_other_way": len(other),
        "cars_compared": len(shifts),
    }


def crossings(path: np.ndarray, path_length: float, vehicles: dict) -> list:
    """Moving vehicles that cross the ego's path (or up to CROSSING_AHEAD_M
    past its end) at an angle in CROSSING_DEG."""
    found = []
    for actor, track in vehicles.items():
        p = project(path, track["xy"])
        speed = speeds(track["t"], track["xy"])
        angle = _angle_deg(track["yaw"], p["heading"])
        for k in range(len(p["d"]) - 1):
            if (
                np.sign(p["d"][k]) != np.sign(p["d"][k + 1])
                and max(p["dist"][k], p["dist"][k + 1]) < 2 * LANE_HALF_WIDTH_M
                and 0 < p["s"][k] < path_length + CROSSING_AHEAD_M
                and CROSSING_DEG[0] < angle[k] < CROSSING_DEG[1]
                and speed[k] > MOVING_MPS
            ):
                found.append(
                    {
                        "actor": actor,
                        "label": track["label"],
                        "angle_deg": round(float(angle[k]), 0),
                        "at_s": round(float(track["t"][k]), 1),
                    }
                )
                break
    return found


def oncoming(ego: dict, vehicles: dict) -> list:
    """For a left turn: moving vehicles heading against the ego's heading
    before the turn that come within ONCOMING_NEAR_TURN_M of the turn's middle."""
    yaw = ego["yaw"]
    turned = (yaw - yaw[0]) / (yaw[-1] - yaw[0])
    middle = ego["xy"][int(np.argmin(np.abs(turned - 0.5)))]
    found = []
    for actor, track in vehicles.items():
        speed = speeds(track["t"], track["xy"])
        against = _angle_deg(track["yaw"], np.full(len(track["yaw"]), yaw[0] + np.pi))
        near = np.hypot(*(track["xy"] - middle).T)
        hits = (
            (against < ONCOMING_DEG)
            & (speed > MOVING_MPS)
            & (near < ONCOMING_NEAR_TURN_M)
        )
        if hits.any():
            found.append(
                {
                    "actor": actor,
                    "label": track["label"],
                    "closest_to_turn_m": round(float(near[hits].min()), 1),
                }
            )
    return found


def pedestrians_near(ego: dict, path: np.ndarray, pedestrians: dict) -> list:
    """Pedestrians within PEDESTRIAN_NEAR_M of the recorded path: closest
    approach to the path, when, how far the ego was then, the closest they
    came to the ego itself, and whether they crossed the path."""
    found = []
    for actor, track in pedestrians.items():
        p = project(path, track["xy"])
        k = int(p["dist"].argmin())
        if p["dist"][k] > PEDESTRIAN_NEAR_M:
            continue
        close = p["dist"] < PEDESTRIAN_NEAR_M
        ego_xy = np.column_stack(
            [np.interp(track["t"], ego["t"], ego["xy"][:, c]) for c in (0, 1)]
        )
        to_ego = np.hypot(*(track["xy"] - ego_xy).T)
        found.append(
            {
                "actor": actor,
                "label": track["label"],
                "closest_m": round(float(p["dist"][k]), 1),
                "at_s": round(float(track["t"][k]), 1),
                "ego_distance_m": round(float(to_ego[k]), 1),
                "closest_to_ego_m": round(float(to_ego.min()), 1),
                "crosses": bool(np.any(np.diff(np.sign(p["d"][close])) != 0)),
            }
        )
    return sorted(found, key=lambda row: row["closest_m"])


def scene_facts(tracks: dict) -> dict:
    """The log facts of one scene from its logged tracks."""
    ego = tracks[EGO]
    others = {actor: track for actor, track in tracks.items() if actor != EGO}
    for actor, track in others.items():
        if track["label"] not in KINDS:
            raise ValueError(f"actor {actor}: unknown class {track['label']!r}")
    recorded = reference_path(ego["xy"], ego["yaw"], 0.0)
    extended = reference_path(ego["xy"], ego["yaw"], EXTEND_M)
    path_length = float(np.sum(np.hypot(*np.diff(recorded, axis=0).T)))
    s_ego = project(extended, ego["xy"])["s"]
    near = {
        actor: track
        for actor, track in others.items()
        if project(recorded, track["xy"])["dist"].min() < NEAR_PATH_M
    }
    vehicles = {
        actor: track
        for actor, track in near.items()
        if KINDS[track["label"]] == "vehicle" and not track["static"]
    }
    facts = ego_facts(ego)
    facts["near_path"] = {
        kind: sum(KINDS[track["label"]] == kind for track in near.values())
        for kind in ("vehicle", "pedestrian", "cyclist", "other")
    }
    facts["near_path"]["static"] = sum(track["static"] for track in near.values())
    facts["lead"] = lead(ego, s_ego, extended, vehicles)
    facts["cut_ins"] = cut_ins(ego, s_ego, extended, vehicles)
    facts["lane_change"] = lane_change(extended, path_length, vehicles)
    facts["crossing_vehicles"] = crossings(extended, path_length, vehicles)
    facts["oncoming"] = oncoming(ego, vehicles) if facts["turn"] == "left" else []
    facts["pedestrians_near"] = pedestrians_near(
        ego,
        recorded,
        {a: t for a, t in near.items() if KINDS[t["label"]] == "pedestrian"},
    )
    return facts


def rule_tags(facts: dict) -> dict[str, str]:
    """Candidate tags from the log facts, each with its evidence."""
    tags = {}
    found = facts["lead"]
    if (
        found is not None
        and found["lead_s"] >= LEAD_MIN_S
        and (
            found["speed_drop_mps"] >= LEAD_SLOWS_MPS
            or found["min_speed_mps"] < STOPPED_MPS
        )
    ):
        tags["lead_vehicle"] = (
            f"{found['label']} {found['actor']} ahead in lane for {found['lead_s']} s, "
            f"gap down to {found['min_gap_m']} m, speed {found['max_speed_mps']} -> "
            f"{found['min_speed_mps']} m/s (drop {found['speed_drop_mps']})"
        )
    if facts["turn"] == "left" and facts["oncoming"]:
        closest = min(row["closest_to_turn_m"] for row in facts["oncoming"])
        tags["unprotected_left"] = (
            f"left turn {facts['heading_change_deg']} deg, "
            f"{len(facts['oncoming'])} oncoming vehicle(s), closest {closest} m "
            "from the turn"
        )
    merge = []
    if facts["cut_ins"]:
        first = facts["cut_ins"][0]
        merge.append(
            f"{len(facts['cut_ins'])} cut-in(s), first {first['actor']} from "
            f"{first['from_m']} m to the side into the lane at {first['at_s']} s, "
            f"{first['gap_m']} m ahead"
        )
    change = facts["lane_change"]
    if change["shift_m"]:
        side = "left" if change["shift_m"] > 0 else "right"
        merge.append(
            f"ego changes lanes {abs(change['shift_m'])} m {side} "
            f"({change['cars_shifted']} of {change['cars_compared']} cars around "
            f"it shift the other way relative to its path)"
        )
    if merge:
        tags["merge_cut_in"] = "; ".join(merge)
    junction = []
    if facts["turn"] != "none":
        junction.append(f"{facts['turn']} turn {facts['heading_change_deg']} deg")
    if facts["crossing_vehicles"]:
        angles = sorted({row["angle_deg"] for row in facts["crossing_vehicles"]})
        junction.append(
            f"{len(facts['crossing_vehicles'])} vehicle(s) cross the path "
            f"(angles {', '.join(f'{a:.0f}' for a in angles)} deg)"
        )
    if junction:
        tags["intersection"] = "; ".join(junction)
    if facts["pedestrians_near"]:
        first = facts["pedestrians_near"][0]
        crossing = sum(row["crosses"] for row in facts["pedestrians_near"])
        tags["pedestrian_crossing"] = (
            f"{len(facts['pedestrians_near'])} pedestrian(s) within "
            f"{PEDESTRIAN_NEAR_M:.0f} m of the path ({crossing} cross it), closest "
            f"{first['closest_m']} m at {first['at_s']} s with the ego "
            f"{first['ego_distance_m']} m away; nearest to the ego "
            f"{min(row['closest_to_ego_m'] for row in facts['pedestrians_near'])} m"
        )
    return tags


def kept_runs(queue: Path) -> dict[str, dict]:
    """scene_id -> the first kept run of the queue on that scene."""
    found = {}
    for path in queue_entries(queue):
        entry = load_entry(path)
        if entry["resolution"] == "ACCEPT" and "quarantine" not in entry:
            found.setdefault(entry["config"]["scene_id"], entry)
    return found


def frames(run_dir: Path, folder: Path) -> list[str]:
    """Three frames of the run's video: at 0.5 s, the middle, 0.5 s before the end."""
    video = next(completed_rollout(run_dir).glob("*.mp4"))
    duration = float(
        subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "csv=p=0",
                str(video),
            ],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
    )
    folder.mkdir(parents=True, exist_ok=True)
    names = []
    for at in (0.5, round(duration / 2, 1), round(duration - 0.5, 1)):
        name = f"frame_{at:04.1f}s.png"
        subprocess.run(
            [
                "ffmpeg",
                "-v",
                "error",
                "-y",
                "-ss",
                f"{at}",
                "-i",
                str(video),
                "-frames:v",
                "1",
                str(folder / name),
            ],
            check=True,
        )
        names.append(name)
    return names


def claude_tags(scene_id: str, run_dir: Path, model: str, reuse: bool) -> dict:
    """Claude's answer for one scene, saved next to its frames folder."""
    folder = FRAMES / scene_id
    saved = FRAMES / f"{scene_id}.json"
    if reuse and saved.exists():
        return json.loads(saved.read_text(encoding="utf-8"))
    names = frames(run_dir, folder)
    prompt = (
        f"The frames are in {folder}: "
        + ", ".join(names)
        + ". Read every frame, then tag the scene."
    )
    answer, call = ask(
        prompt, {"frames": names}, CONTRACT, SCHEMA, model, read_dir=folder
    )
    found = {
        **answer,
        "frames": [str((folder / name).relative_to(ROOT)) for name in names],
        "call": call,
    }
    saved.write_text(json.dumps(found, indent=1) + "\n", encoding="utf-8")
    return found


def combine(rules: dict[str, str], claude: dict) -> dict:
    """Every tag either source gave, with its source and reasons. Final tags
    are Claude's: confirmed by the rules or added."""
    said = {row["category"]: row["reason"] for row in claude["categories"]}
    sources = {}
    for tag in CATEGORIES:
        if tag in rules and tag in said:
            sources[tag] = "agree"
        elif tag in said:
            sources[tag] = "claude"
        elif tag in rules:
            sources[tag] = "rules"
    return {
        "sources": sources,
        "final_tags": [tag for tag, source in sources.items() if source != "rules"],
        "reasons": {
            tag: {
                **({"rules": rules[tag]} if tag in rules else {}),
                **({"claude": said[tag]} if tag in said else {}),
            }
            for tag in sources
        },
    }


def scene_files(folder: Path, catalog: Path) -> dict[str, Path]:
    """scene_id -> its scene file in `folder`, for every complete file (at
    least COMPLETE_BYTES; smaller ones are still downloading). Files are named
    by their catalog uuid; of two files of one scene the one the wizard would
    run is kept, the latest by the catalog's last_modified."""
    rows = {}
    with catalog.open(newline="") as handle:
        for row in csv.DictReader(handle):
            rows[row["uuid"]] = row
    found = {}
    for path in sorted(folder.glob("*.usdz")):
        if path.stat().st_size < COMPLETE_BYTES:
            continue
        row = rows[path.stem]
        kept = found.get(row["scene_id"])
        if kept is None or row["last_modified"] > rows[kept.stem]["last_modified"]:
            found[row["scene_id"]] = path
    return found


def file_entry(path: Path) -> dict:
    """A scene's entry from its scene file alone: rule tags as final tags,
    each with source FILE_SOURCE."""
    facts = scene_facts(file_tracks(Artifact(str(path))))
    rules = rule_tags(facts)
    return {
        "scene_file": str(path.relative_to(ROOT)),
        "facts": facts,
        "rule_tags": rules,
        "sources": {tag: FILE_SOURCE for tag in rules},
        "final_tags": list(rules),
        "reasons": {tag: {"rules": text} for tag, text in rules.items()},
    }


def tag_files(scenes: dict, files: dict[str, Path]) -> dict:
    """`scenes` with an entry added from its file for every scene in `files`
    that has none; existing entries are kept as they are."""
    added = {s: file_entry(path) for s, path in files.items() if s not in scenes}
    return {**scenes, **added}


def _actors(facts: dict, key: str) -> list[str]:
    return sorted(row["actor"] for row in facts[key])


def compare_facts(from_file: dict, from_log: dict) -> list[str]:
    """Where a scene's facts from its file and from its run log disagree: the
    turn, near-path counts by class, the lead vehicle, the actors behind
    cut-ins, crossings, oncoming traffic and pedestrians near the path, and
    the rule tags. Measured numbers (distances, speeds, times) are left out:
    small differences there are expected."""
    found = []
    pairs = {
        "turn": (from_file["turn"], from_log["turn"]),
        "near_path": (from_file["near_path"], from_log["near_path"]),
        "lead": tuple(
            None if facts["lead"] is None else facts["lead"]["actor"]
            for facts in (from_file, from_log)
        ),
        **{
            key: (_actors(from_file, key), _actors(from_log, key))
            for key in ("cut_ins", "crossing_vehicles", "oncoming", "pedestrians_near")
        },
        "rule_tags": (sorted(rule_tags(from_file)), sorted(rule_tags(from_log))),
    }
    for key, (file_value, log_value) in pairs.items():
        if file_value != log_value:
            found.append(f"{key}: file {file_value} vs log {log_value}")
    return found


def compare(runs: dict[str, dict], files: dict[str, Path], count: int) -> str:
    """The first `count` scenes with both a kept run and a scene file: what
    their facts from each source disagree on, and how far the ego's distance
    and heading change differ."""
    lines = []
    shared = sorted(set(runs) & set(files))[:count]
    for scene_id in shared:
        rollout = completed_rollout(ROOT / runs[scene_id]["run_dir"]) / "rollout.asl"
        from_log = scene_facts(asyncio.run(logged_tracks(rollout)))
        from_file = scene_facts(file_tracks(Artifact(str(files[scene_id]))))
        differences = compare_facts(from_file, from_log)
        lines.append(
            f"{scene_id} ({runs[scene_id]['name']}): "
            f"{'agree' if not differences else 'DIFFER'}; distance "
            f"{from_file['distance_m']} vs {from_log['distance_m']} m, heading "
            f"{from_file['heading_change_deg']} vs {from_log['heading_change_deg']} "
            f"deg, duration {from_file['duration_s']} vs {from_log['duration_s']} s"
        )
        lines += [f"  {line}" for line in differences]
    return "\n".join(lines)


def table(scenes: dict) -> str:
    """Counts per category. Final tags of a file-tagged scene are its rule
    tags ("file" column), counted in "final" and "rules" too."""
    rows = [
        (
            f"{'category':<20} {'final':>5} {'rules':>5} {'claude':>6} {'both':>4} "
            f"{'rules only':>10} {'claude only':>11} {'file':>4}"
        )
    ]
    for tag in CATEGORIES:
        sources = [row["sources"].get(tag) for row in scenes.values()]
        both = sources.count("agree")
        rules_only, claude_only = sources.count("rules"), sources.count("claude")
        file = sources.count(FILE_SOURCE)
        rows.append(
            f"{tag:<20} {both + claude_only + file:>5} "
            f"{both + rules_only + file:>5} {both + claude_only:>6} {both:>4} "
            f"{rules_only:>10} {claude_only:>11} {file:>4}"
        )
    untagged = sum(not row["final_tags"] for row in scenes.values())
    from_files = sum("scene_file" in row for row in scenes.values())
    rows.append(
        f"{len(scenes)} scenes ({from_files} tagged from their file alone), "
        f"{untagged} with no final tag"
    )
    return "\n".join(rows)


def check_sheet(scenes: dict, per_category: int = 4, seed: int = 0) -> str:
    """Scenes sampled evenly across the final categories (a fixed seed), for
    a person to verify by hand."""
    rng = random.Random(seed)
    picked = {}
    for tag in CATEGORIES:
        pool = sorted(
            s
            for s, row in scenes.items()
            if tag in row["final_tags"] and s not in picked
        )
        for scene_id in rng.sample(pool, min(per_category, len(pool))):
            picked[scene_id] = tag
    rest = sorted(set(scenes) - set(picked))
    for scene_id in rng.sample(rest, per_category * len(CATEGORIES) - len(picked)):
        picked[scene_id] = "(fill)"
    lines = [
        "# Scene tags: hand check",
        "",
        (
            f"{len(picked)} scenes sampled evenly across the final categories "
            f"(seed {seed}; `(fill)` rows fill categories with too few scenes). "
            "Frames are relative to the AlpaSim checkout. Fill in the last column "
            "with the tags you see."
        ),
        "",
        "| # | scene | sampled for | rules | Claude | final | frames | person says |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for n, (scene_id, tag) in enumerate(picked.items(), 1):
        row = scenes[scene_id]
        lines.append(
            f"| {n} | `{scene_id}` ({row['run']}) | {tag} | "
            f"{', '.join(row['rule_tags']) or '-'} | "
            f"{', '.join(c['category'] for c in row['claude_tags']['categories']) or '-'} | "
            f"{', '.join(row['final_tags']) or '-'} | "
            f"{'<br>'.join(row['claude_tags']['frames'])} |  |"
        )
    lines += ["", "## Evidence", ""]
    for n, scene_id in enumerate(picked, 1):
        row = scenes[scene_id]
        lines.append(
            f"{n}. `{scene_id}`: ego {row['claude_tags']['ego_maneuver']}, "
            f"{row['claude_tags']['road_type']}"
        )
        for tag, why in row["reasons"].items():
            for source, text in why.items():
                lines.append(f"   - {tag} ({source}): {text}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", type=Path, default=QUEUE)
    parser.add_argument("--model", default=MODEL)
    parser.add_argument(
        "--reuse", action="store_true", help="keep Claude answers already saved"
    )
    parser.add_argument(
        "--files",
        action="store_true",
        help="add scenes not yet tagged, from their scene files alone",
    )
    parser.add_argument(
        "--compare",
        type=int,
        metavar="N",
        help="compare file and run-log facts on N scenes with a kept run",
    )
    args = parser.parse_args()
    runs = kept_runs(args.queue)
    if args.compare:
        print(compare(runs, scene_files(SCENE_FILES, CATALOG), args.compare))
        return 0
    saved = json.loads(OUTPUT.read_text(encoding="utf-8"))
    if args.files:
        scenes = tag_files(saved, scene_files(SCENE_FILES, CATALOG))
        OUTPUT.write_text(json.dumps(scenes, indent=1) + "\n", encoding="utf-8")
        print(f"{len(scenes) - len(saved)} scenes tagged from their files")
        print(table(scenes))
        return 0
    facts = {}
    for scene_id, entry in runs.items():
        rollout = completed_rollout(ROOT / entry["run_dir"]) / "rollout.asl"
        facts[scene_id] = scene_facts(asyncio.run(logged_tracks(rollout)))
    with ThreadPoolExecutor(4) as pool:
        answers = dict(
            zip(
                runs,
                pool.map(
                    lambda s: claude_tags(
                        s, ROOT / runs[s]["run_dir"], args.model, args.reuse
                    ),
                    runs,
                ),
            )
        )
    scenes = {}
    for scene_id, entry in runs.items():
        rules = rule_tags(facts[scene_id])
        scenes[scene_id] = {
            "run": entry["name"],
            "facts": facts[scene_id],
            "rule_tags": rules,
            "claude_tags": answers[scene_id],
            **combine(rules, answers[scene_id]),
        }
    from_files = {
        s: row for s, row in saved.items() if "scene_file" in row and s not in runs
    }
    CHECK.write_text(check_sheet(scenes), encoding="utf-8")
    scenes = {**scenes, **from_files}
    OUTPUT.write_text(json.dumps(scenes, indent=1) + "\n", encoding="utf-8")
    print(table(scenes))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
