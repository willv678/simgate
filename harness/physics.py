"""What the car physically did in a run, from the run's rollout.asl.

Summary metrics can look normal while the motion is impossible or is not the
policy's. This module rebuilds the ego's motion at every control step and
reduces it to a few features that physics.json thresholds (K⁺) can bound:

- motion from poses, by finite differences: speed, acceleration, jerk, yaw rate;
- consistency: the speed the vehicle model reported against the speed the poses
  imply, and how much of the run the ego sits exactly on the recorded human
  trajectory;
- car following: the gap and time headway to the nearest actor ahead in the
  ego's lane, and whether the ego's box overlapped any actor's box (real sizes
  from the log; actor_poses already gives every actor, the ego included, at
  its box centre) without a collision being scored.

check() applies the bounds in rules/physics.json (or the file named by
ALPASIM_PHYSICS) to a finished run. K⁺ runs it
(read_state.py) when that file says enabled; the bounds and why each is set
where it is are in the file.

    uv run python research/harness/physics.py <run_dir> [<run_dir> ...]
"""

import asyncio
import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from alpasim_utils.logs import async_read_pb_log
from shapely.affinity import rotate, translate
from shapely.geometry import box

EGO = "EGO"
# The ego sits on the recorded trajectory when it is closer than this.
ON_RECORDING_M = 0.05
# An actor is ahead in the ego's lane when it is this far to either side.
LANE_HALF_WIDTH_M = 1.8
LEAD_RANGE_M = 60.0
# Contact means the boxes share this much area. A real collision overlaps by
# square metres (s1_010: 7 m²); clean runs show corner slivers up to 0.1 m²,
# which the evaluator's rounded bumpers do not count.
OVERLAP_M2 = 0.25
BOUNDS = Path(__file__).resolve().parent / "rules" / "physics.json"


def completed_rollout(run_dir: Path) -> Path:
    """The rollout the run was scored on. The runtime retries a failed rollout
    inside the same run, so a run can hold several; only one is `_complete`."""
    done = sorted(path.parent for path in run_dir.glob("rollouts/*/*/_complete"))
    if len(done) != 1:
        raise FileNotFoundError(
            f"{run_dir}: expected one completed rollout, found {len(done)}"
        )
    return done[0]


def _yaw(quat) -> float:
    return float(
        np.arctan2(
            2 * (quat.w * quat.z + quat.x * quat.y),
            1 - 2 * (quat.y * quat.y + quat.z * quat.z),
        )
    )


def _footprint(x: float, y: float, yaw: float, size: tuple[float, float]):
    length, width = size
    shape = box(-length / 2, -width / 2, length / 2, width / 2)
    return translate(rotate(shape, yaw, use_radians=True, origin=(0, 0)), x, y)


async def _read(path: Path) -> dict:
    ego, others, reported, recorded = {}, {}, {}, None
    sizes = {}
    async for message in async_read_pb_log(str(path)):
        kind = message.WhichOneof("log_entry")
        if kind == "rollout_metadata":
            meta = message.rollout_metadata
            for actor in meta.actor_definitions.actor_aabb:
                sizes[actor.actor_id] = (actor.aabb.size_x, actor.aabb.size_y)
        elif kind == "actor_poses":
            poses = message.actor_poses
            t = poses.timestamp_us
            for actor in poses.actor_poses:
                vec = actor.actor_pose.vec
                point = (vec.x, vec.y, _yaw(actor.actor_pose.quat))
                if actor.actor_id == EGO:
                    ego[t] = point
                else:
                    others.setdefault(t, []).append((*point, actor.actor_id))
        elif kind == "controller_request":
            state = message.controller_request.state
            velocity = state.state.linear_velocity
            reported[state.timestamp_us] = float(np.hypot(velocity.x, velocity.y))
        elif kind == "traffic_session_request" and recorded is None:
            for obj in message.traffic_session_request.logged_object_trajectories:
                if obj.object_id == EGO:
                    recorded = [
                        (p.timestamp_us, p.pose.vec.x, p.pose.vec.y)
                        for p in obj.trajectory.poses
                    ]
    return {
        "ego": ego,
        "others": others,
        "reported": reported,
        "recorded": recorded,
        "sizes": sizes,
    }


def signals(run_dir: Path) -> dict:
    """Per-step motion of the ego and its lead, as arrays."""
    raw = asyncio.run(_read(completed_rollout(run_dir) / "rollout.asl"))
    times = np.array(sorted(raw["ego"]))
    xy = np.array([raw["ego"][t][:2] for t in times])
    yaw = np.unwrap([raw["ego"][t][2] for t in times])
    dt = np.diff(times) / 1e6
    speed = np.linalg.norm(np.diff(xy, axis=0), axis=1) / dt
    accel = np.diff(speed) / dt[1:]
    jerk = np.diff(accel) / dt[2:]
    yaw_rate = np.diff(yaw) / dt
    step_times = times[1:]
    reported = np.array([raw["reported"].get(int(t), np.nan) for t in step_times])

    recorded = raw["recorded"] or []
    if recorded:
        rt = np.array([r[0] for r in recorded], dtype=float)
        rx = np.interp(times, rt, [r[1] for r in recorded])
        ry = np.interp(times, rt, [r[2] for r in recorded])
        off_recording = np.hypot(xy[:, 0] - rx, xy[:, 1] - ry)
    else:
        off_recording = np.full(len(times), np.nan)

    gaps, overlaps = [], []
    for t in times:
        x0, y0, heading = raw["ego"][t]
        ego_box = _footprint(x0, y0, heading, raw["sizes"][EGO])
        overlap = 0.0
        best = np.inf
        for x, y, yaw, actor_id in raw["others"].get(t, []):
            if actor_id in raw["sizes"]:
                other = _footprint(x, y, yaw, raw["sizes"][actor_id])
                overlap = max(overlap, ego_box.intersection(other).area)
            dx, dy = x - x0, y - y0
            ahead = dx * np.cos(heading) + dy * np.sin(heading)
            side = -dx * np.sin(heading) + dy * np.cos(heading)
            if 0 < ahead < LEAD_RANGE_M and abs(side) < LANE_HALF_WIDTH_M:
                best = min(best, ahead)
        gaps.append(best)
        overlaps.append(overlap)
    return {
        "times_us": times,
        "speed": speed,
        "accel": accel,
        "jerk": jerk,
        "yaw_rate": yaw_rate,
        "reported_speed": reported,
        "off_recording_m": off_recording,
        "lead_gap_m": np.array(gaps),
        "overlap_m2": np.array(overlaps),
    }


def _collided(run_dir: Path) -> bool:
    metrics = pd.read_parquet(completed_rollout(run_dir) / "metrics.parquet")
    values = metrics.loc[metrics["name"] == "collision_any", "values"]
    return bool(len(values)) and float(values.max()) > 0


def features(s: dict, collided: bool) -> dict:
    """The numbers physics checks bound. Gaps are centre to centre."""
    mismatch = np.abs(s["speed"] - s["reported_speed"])
    headway = s["lead_gap_m"][1:] / np.maximum(s["speed"], 0.5)
    return {
        "max_speed": float(np.max(s["speed"])),
        "max_abs_accel": float(np.max(np.abs(s["accel"]))),
        "p99_abs_jerk": float(np.percentile(np.abs(s["jerk"]), 99)),
        "max_abs_yaw_rate": float(np.max(np.abs(s["yaw_rate"]))),
        "max_speed_report_error": float(np.nanmax(mismatch))
        if np.isfinite(mismatch).any()
        else None,
        "frac_on_recording": float(np.mean(s["off_recording_m"] < ON_RECORDING_M)),
        "min_lead_gap_m": float(np.min(s["lead_gap_m"])),
        "min_time_headway_s": float(np.min(headway)),
        "max_overlap_m2": float(np.max(s["overlap_m2"])),
        "contact_without_collision": bool(
            np.max(s["overlap_m2"]) > OVERLAP_M2 and not collided
        ),
    }


def run_features(run_dir: Path) -> dict:
    return features(signals(run_dir), _collided(run_dir))


def load_bounds() -> dict:
    path = Path(os.environ.get("ALPASIM_PHYSICS", BOUNDS))
    return json.loads(path.read_text(encoding="utf-8"))


def check(run_dir: Path, bounds: dict) -> list[str]:
    """Physics problems of a finished run under `bounds`. Empty when it passes."""
    try:
        found = run_features(run_dir)
    except FileNotFoundError as exc:
        return [f"physics: no rollout log or metrics ({exc})"]
    problems = [
        f"physics: {name} {found[name]:.3g} > {limit['max']}"
        for name, limit in bounds["max"].items()
        if found[name] is not None and found[name] > limit["max"]
    ]
    if found["contact_without_collision"]:
        problems.append(
            "physics: the ego's box overlapped another actor's and no collision was scored"
        )
    return problems


def main() -> int:
    for arg in sys.argv[1:]:
        found = run_features(Path(arg))
        print(
            Path(arg).name,
            json.dumps(
                {
                    k: round(v, 3) if isinstance(v, float) else v
                    for k, v in found.items()
                }
            ),
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
