"""What the car physically did in a run, from the run's rollout.asl.

Summary metrics can look normal while the motion is impossible or is not the
policy's. This module rebuilds the ego's motion at every control step and
reduces it to a few features that physics.json thresholds (K⁺) can bound:

- motion from poses, by finite differences: speed, acceleration, jerk, yaw rate;
- consistency: the speed the vehicle model reported against the speed the poses
  imply, and how much of the run the ego sits exactly on the recorded human
  trajectory;
- plan handoff: after the force-GT warm-up (its length is in the log), the plan
  the controller was asked to track against the driver plan it came from,
  matched by the plans' timestamps, which the runtime keeps, and compared in the
  ego's frame from when the plan was made, the frame a delayed plan reaches the
  controller in. Two numbers: the sideways gap between them (a bias or waypoint noise moves it; in a clean run
  they are the same plan, up to interpolation on curves), and the plan's age
  when the controller got it, which equals the planner delay rounded up to the
  control step (a frozen plan ages step by step; a delay that never applied
  leaves it at 0);
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
from scipy.stats import chi2
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
    sizes, handoffs, plans, warm_up_end, poses_at = {}, [], {}, 0, {}
    async for message in async_read_pb_log(str(path)):
        kind = message.WhichOneof("log_entry")
        if kind == "rollout_metadata":
            meta = message.rollout_metadata
            for actor in meta.actor_definitions.actor_aabb:
                sizes[actor.actor_id] = (actor.aabb.size_x, actor.aabb.size_y)
            warm_up_end = (
                meta.session_metadata.start_timestamp_us + meta.force_gt_duration
            )
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
        elif kind == "driver_return":
            poses = message.driver_return.trajectory.poses
            if poses:
                plans[poses[0].timestamp_us] = [
                    (p.timestamp_us, p.pose.vec.x, p.pose.vec.y, _yaw(p.pose.quat))
                    for p in poses
                ]
        elif kind == "controller_request":
            request = message.controller_request
            state = request.state
            velocity = state.state.linear_velocity
            reported[state.timestamp_us] = float(np.hypot(velocity.x, velocity.y))
            pose = (state.pose.vec.x, state.pose.vec.y, _yaw(state.pose.quat))
            poses_at[state.timestamp_us] = pose
            given = [
                (p.timestamp_us, p.pose.vec.x, p.pose.vec.y)
                for p in request.planned_trajectory_in_rig.poses
            ]
            if plans and given and state.timestamp_us >= warm_up_end:
                # The driver plan this one came from; the newest if none matches.
                # The runtime puts a plan in the ego's frame when the plan is
                # made, and a delayed plan reaches the controller in that frame.
                source = plans.get(given[0][0], plans[max(plans)])
                made_at = poses_at.get(source[0][0], pose)
                age_us = state.timestamp_us - source[0][0]
                handoffs.append((made_at, source, given, age_us))
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
        "handoffs": handoffs,
    }


def _handoff_deviations(pose: tuple, driver_plan: list, given: list) -> np.ndarray:
    """Signed distance from the driver's plan, moved into the ego's rig frame,
    to the plan the controller was given, along each waypoint's left normal,
    at each of their shared times: a lateral bias of b moves every waypoint by
    exactly b along it. Across the path only: a few ms of timestamp jitter
    moves points along the road by up to 10 cm at highway speed, while a
    corrupted plan moves them across it."""
    ex, ey, yaw = pose
    t = np.array([p[0] for p in driver_plan], dtype=float)
    dx = np.array([p[1] for p in driver_plan]) - ex
    dy = np.array([p[2] for p in driver_plan]) - ey
    rx = np.cos(-yaw) * dx - np.sin(-yaw) * dy
    ry = np.sin(-yaw) * dx + np.cos(-yaw) * dy
    heading = np.unwrap([p[3] for p in driver_plan]) - yaw
    deviations = []
    for gt, gx, gy in given:
        if t[0] <= gt <= t[-1]:
            h = float(np.interp(gt, t, heading))
            ox, oy = gx - float(np.interp(gt, t, rx)), gy - float(np.interp(gt, t, ry))
            deviations.append(-np.sin(h) * ox + np.cos(h) * oy)
    return np.array(deviations)


def _handoff_gap(pose: tuple, driver_plan: list, given: list) -> float:
    """Largest sideways distance between the two plans over their shared times."""
    deviations = _handoff_deviations(pose, driver_plan, given)
    return float(np.max(np.abs(deviations))) if len(deviations) else 0.0


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
        for x, y, actor_yaw, actor_id in raw["others"].get(t, []):
            if actor_id in raw["sizes"]:
                other = _footprint(x, y, actor_yaw, raw["sizes"][actor_id])
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
        "xy": xy,
        "yaw": yaw,
        "speed": speed,
        "accel": accel,
        "jerk": jerk,
        "yaw_rate": yaw_rate,
        "reported_speed": reported,
        "off_recording_m": off_recording,
        "lead_gap_m": np.array(gaps),
        "overlap_m2": np.array(overlaps),
        "plan_handoff_m": np.array(
            [_handoff_gap(*h[:3]) for h in raw["handoffs"]] or [0.0]
        ),
        "plan_age_ms": np.array([h[3] / 1e3 for h in raw["handoffs"]] or [0.0]),
        "plan_deviations": [_handoff_deviations(*h[:3]) for h in raw["handoffs"]],
    }


async def _session_seeds(path: Path) -> dict:
    seeds = {}
    async for message in async_read_pb_log(str(path)):
        kind = message.WhichOneof("log_entry")
        if kind in ("driver_session_request", "traffic_session_request"):
            seeds[kind.removesuffix("_session_request")] = getattr(
                message, kind
            ).random_seed
            if len(seeds) == 2:
                break
    return seeds


def session_seeds(run_dir: Path) -> dict:
    """The seeds the scored rollout's driver and traffic sessions were opened
    with, as the runtime logged their session requests (near the log's start)."""
    return asyncio.run(_session_seeds(completed_rollout(run_dir) / "rollout.asl"))


def _collided(run_dir: Path) -> bool:
    metrics = pd.read_parquet(completed_rollout(run_dir) / "metrics.parquet")
    values = metrics.loc[metrics["name"] == "collision_any", "values"]
    return bool(len(values)) and float(values.max()) > 0


def _scatter(deviations: list) -> float:
    """The standard deviation of the plan's offsets about each handoff's own
    median: the median over handoffs of the sample variance, divided by the
    median of a chi-square with n-1 degrees of freedom over n-1, which makes
    it unbiased for Gaussian noise. The median ignores the few handoffs on
    curves where interpolation alone spreads the points."""
    variances = [np.var(d, ddof=1) for d in deviations if len(d) > 2]
    if not variances:
        return 0.0
    n = int(np.median([len(d) for d in deviations if len(d) > 2]))
    unbiased = chi2.median(n - 1) / (n - 1)
    return float(np.sqrt(np.median(variances) / unbiased))


def _median_over_steps(deviations: list, reduce) -> float:
    """The median over handoffs of one statistic of each handoff's deviations."""
    per_step = [reduce(d) for d in deviations if len(d)]
    return float(np.median(per_step)) if per_step else 0.0


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
        "median_plan_handoff_m": float(np.median(s["plan_handoff_m"])),
        "median_plan_age_ms": float(np.median(s["plan_age_ms"])),
        "max_plan_age_ms": float(np.max(s["plan_age_ms"])),
        "median_plan_offset_m": _median_over_steps(s["plan_deviations"], np.median),
        "plan_noise_m": _scatter(s["plan_deviations"]),
        "contact_without_collision": bool(
            np.max(s["overlap_m2"]) > OVERLAP_M2 and not collided
        ),
    }


def run_features(run_dir: Path) -> dict:
    return features(signals(run_dir), _collided(run_dir))


def load_bounds() -> dict:
    path = Path(os.environ.get("ALPASIM_PHYSICS", BOUNDS))
    return json.loads(path.read_text(encoding="utf-8"))


def plan_problems(found: dict, request: dict, bounds: dict) -> list[str]:
    """The plan the controller got must be the driver's plan with exactly what
    the run asked for: its age the requested delay (up to one control step),
    its offset the requested lateral bias, its scatter the requested noise."""
    problems = []
    delay_ms = request["planner_delay_us"] / 1e3
    slack_ms = bounds["plan_age"]["slack_ms"]
    median, oldest = found["median_plan_age_ms"], found["max_plan_age_ms"]
    if not (delay_ms <= median < delay_ms + slack_ms and oldest < delay_ms + slack_ms):
        problems.append(
            f"physics: plan age median {median:.0f} ms, max {oldest:.0f} ms; "
            f"the requested planner delay is {delay_ms:.0f} ms"
        )
    match = bounds["plan_matches_request"]
    offset = found["median_plan_offset_m"]
    if abs(offset - request["lateral_bias_m"]) > match["offset_tolerance_m"]:
        problems.append(
            f"physics: plan offset {offset:+.3f} m; the requested lateral bias is "
            f"{request['lateral_bias_m']:+.3f} m"
        )
    noise = found["plan_noise_m"]
    asked = request["waypoint_noise_std"]
    if (
        abs(noise - asked)
        > match["noise_tolerance_m"] + match["noise_relative"] * asked
    ):
        problems.append(
            f"physics: plan scatter {noise:.3f} m; the requested waypoint noise is "
            f"{request['waypoint_noise_std']:.3f} m"
        )
    return problems


def check(run_dir: Path, bounds: dict, request: dict) -> list[str]:
    """Physics problems of a finished run under `bounds`, given what it asked of
    the plan (read_state.plan_request). Empty when it passes."""
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
    return problems + plan_problems(found, request, bounds)


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
