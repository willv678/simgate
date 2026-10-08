"""Did two runs with the same seed do the same thing? Compare their rollout logs.

A replay (replay.py) is exact only if, with the seed and traffic replayed,
nothing else in the run is random: the renderer, VaVAM on the GPU, the
controller and the physics. This compares the two scored rollouts step by step
and says where they first part, in the order the loop runs:

- the camera frames the driver got (the renderer; hashes of the image bytes);
- the plans the driver returned (VaVAM, given the same frames);
- the ego poses (controller and vehicle model, given the same plans), from
  physics.signals.

The first of these to differ is the source. Once the ego is somewhere else,
everything after it differs too. Exit code 0 when the seeds match and the
poses agree within --tol metres at every step.

    uv run python research/harness/check_replay.py <run_a> <run_b> [--tol 1e-6]
"""

import argparse
import asyncio
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
from alpasim_utils.logs import async_read_pb_log

sys.path.insert(0, str(Path(__file__).resolve().parent))

from read_state import ROOT

from physics import completed_rollout, session_seeds, signals


async def _frames_and_plans(path: Path) -> tuple[dict, dict]:
    """Image hash per (camera, frame end) and plan (x, y per waypoint) per
    plan start time, from one rollout log."""
    frames, plans = {}, {}
    async for message in async_read_pb_log(str(path)):
        kind = message.WhichOneof("log_entry")
        if kind == "driver_camera_image":
            image = message.driver_camera_image.camera_image
            key = (image.logical_id, image.frame_end_us)
            frames[key] = hashlib.sha256(image.image_bytes).hexdigest()
        elif kind == "driver_return":
            poses = message.driver_return.trajectory.poses
            if poses:
                plans[poses[0].timestamp_us] = np.array(
                    [(p.pose.vec.x, p.pose.vec.y) for p in poses]
                )
    return frames, plans


def compare(run_a: Path, run_b: Path, tol: float) -> dict:
    a, b = signals(run_a), signals(run_b)
    times = np.intersect1d(a["times_us"], b["times_us"])
    if not len(times):
        raise SystemExit(f"{run_a} and {run_b} share no step: not the same scene?")
    ia = np.searchsorted(a["times_us"], times)
    ib = np.searchsorted(b["times_us"], times)
    pose_diff = np.linalg.norm(a["xy"][ia] - b["xy"][ib], axis=1)
    yaw_diff = np.abs(a["yaw"][ia] - b["yaw"][ib])
    frames_a, plans_a = asyncio.run(
        _frames_and_plans(completed_rollout(run_a) / "rollout.asl")
    )
    frames_b, plans_b = asyncio.run(
        _frames_and_plans(completed_rollout(run_b) / "rollout.asl")
    )
    start = int(times[0])

    def since_start(t: int | None) -> float | None:
        return None if t is None else round((t - start) / 1e6, 3)

    frame_keys = set(frames_a) & set(frames_b)
    first_frame = min(
        (t for camera, t in frame_keys if frames_a[camera, t] != frames_b[camera, t]),
        default=None,
    )
    plan_times = set(plans_a) & set(plans_b)
    first_plan = min(
        (
            t
            for t in plan_times
            if plans_a[t].shape != plans_b[t].shape
            or float(np.abs(plans_a[t] - plans_b[t]).max()) > tol
        ),
        default=None,
    )
    first_pose = min(
        (int(t) for t, d in zip(times, pose_diff) if d > tol), default=None
    )
    seeds = {"a": session_seeds(run_a), "b": session_seeds(run_b)}
    found = {
        "seeds": seeds,
        "same_seeds": seeds["a"] == seeds["b"],
        "steps_compared": len(times),
        "same_steps": bool(np.array_equal(a["times_us"], b["times_us"])),
        "max_pose_diff_m": float(pose_diff.max()),
        "final_pose_diff_m": float(pose_diff[-1]),
        "max_yaw_diff_rad": float(yaw_diff.max()),
        "first_frame_divergence_s": since_start(first_frame),
        "first_plan_divergence_s": since_start(first_plan),
        "first_pose_divergence_s": since_start(first_pose),
        "frames_compared": len(frame_keys),
        "plans_compared": len(plan_times),
    }
    found["identical"] = bool(
        found["same_seeds"] and found["same_steps"] and found["max_pose_diff_m"] <= tol
    )
    return found


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_a", type=Path)
    parser.add_argument("run_b", type=Path)
    parser.add_argument(
        "--tol", type=float, default=1e-6, help="metres two poses may differ by"
    )
    args = parser.parse_args()
    found = compare(ROOT / args.run_a, ROOT / args.run_b, args.tol)
    print(json.dumps(found, indent=1))
    return 0 if found["identical"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
