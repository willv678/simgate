"""The ego speed knob: the wizard gets the scale, and a run passes only when the
runtime says it retimed the ego and the ego's logged speed at hand-off is the
scale times the recorded speed there."""

import asyncio
from pathlib import Path

import numpy as np
import pytest
import yaml
from alpasim_grpc.v0.logging_pb2 import LogEntry
from alpasim_utils.logs import LogWriter
from conftest import SCENE_ID
from knobs import UNVARIED, rejection, run_config
from physics import handoff_speed_matches, handoff_speeds_from
from read_state import State, read_state
from run_experiment import ego_args, wizard_command

# Recorded ego: along a 50 m radius curve at 8 m/s + 0.5 m/s^2, rig poses
# every 100 ms over 10 s; the box centre is 1.5 m ahead of the rig. The
# policy takes over at 4.6 s (render start 0.1 s + force-GT 4.5 s).
RENDER_START_US = 100_000
FORCE_GT_US = 4_500_000
HANDOFF_US = RENDER_START_US + FORCE_GT_US
RADIUS_M = 50.0
BOX_OFFSET_M = 1.5


def _rig(t_s: float) -> tuple[float, float, float]:
    arc = 8.0 * t_s + 0.25 * t_s**2
    angle = arc / RADIUS_M
    return RADIUS_M * np.sin(angle), RADIUS_M * (1 - np.cos(angle)), angle


def _box(t_s: float) -> tuple[float, float, float]:
    x, y, yaw = _rig(t_s)
    return x + BOX_OFFSET_M * np.cos(yaw), y + BOX_OFFSET_M * np.sin(yaw), yaw


def _raw(scale: float, noise_m: float = 0.0) -> dict:
    """What physics._read gives for a run whose ego followed the recording
    retimed by `scale` (ego poses every control step, 100 ms)."""
    rng = np.random.default_rng(0)
    ego = {}
    for t_us in range(0, 10_000_001, 100_000):
        x, y, yaw = _box((HANDOFF_US + (t_us - HANDOFF_US) * scale) / 1e6)
        dx, dy = rng.normal(0.0, noise_m, 2) if noise_m else (0.0, 0.0)
        ego[t_us] = (x + dx, y + dy, yaw)
    ground_truth = [
        (t_us, *_box(t_us / 1e6)[:2]) for t_us in range(0, 10_000_001, 100_000)
    ]
    return {"ego": ego, "handoff_us": HANDOFF_US, "ground_truth": ground_truth}


@pytest.mark.parametrize("scale", [0.6, 0.8, 1.2, 1.4])
def test_a_retimed_ego_is_measured_at_scale_times_the_recorded_speed(scale):
    ego, recorded = handoff_speeds_from(_raw(scale), scale)
    assert ego == pytest.approx(scale * recorded, rel=1e-3)
    assert handoff_speed_matches(ego, recorded, scale)


def test_pose_noise_stays_inside_the_tolerance():
    # 2 cm of noise on each logged ego pose: about 0.1 m/s on the speed.
    ego, recorded = handoff_speeds_from(_raw(1.2, noise_m=0.02), 1.2)
    assert abs(ego - 1.2 * recorded) < 0.15
    assert handoff_speed_matches(ego, recorded, 1.2)


@pytest.mark.parametrize("requested", [0.8, 1.2])
def test_an_ego_at_its_recorded_speed_fails_a_scaled_request(requested):
    assert not handoff_speed_matches(*handoff_speeds_from(_raw(1.0), requested), requested)


def test_the_knob_is_a_scenario_knob_unvaried_at_one():
    assert UNVARIED["ego_speed_scale"] == 1.0
    assert run_config(SCENE_ID, {}, {}, "linear")["ego_speed_scale"] == 1.0
    proposed = {"scene_id": SCENE_ID, "why": "faster", "ego_speed_scale": 1.2}
    assert rejection(proposed, {SCENE_ID}, ("ego_speed_scale",)) is None
    assert rejection({**proposed, "ego_speed_scale": 1.3}, {SCENE_ID}, ("ego_speed_scale",))


def test_the_wizard_gets_the_scale_only_when_it_is_varied(tmp_path):
    assert ego_args({}) == []
    assert ego_args({"ego_speed_scale": 1.0}) == []
    assert ego_args({"ego_speed_scale": 1.2}) == [
        "+runtime.simulation_config.ego_speed_scale=1.2"
    ]
    config = {
        **run_config(SCENE_ID, {"ego_speed_scale": 0.8}, {}, "linear"),
        "frame_interval_us": 100_000,
    }
    assert "+runtime.simulation_config.ego_speed_scale=0.8" in wizard_command(
        config, tmp_path / "run"
    )


def _write_rollout(run_dir: Path, raw: dict) -> None:
    rollout = run_dir / "rollouts" / SCENE_ID / "rollout-0"
    rollout.mkdir(parents=True)

    async def write() -> None:
        async with LogWriter(str(rollout / "rollout.asl")) as log:
            entry = LogEntry()
            meta = entry.rollout_metadata
            meta.session_metadata.render_start_timestamp_us = RENDER_START_US
            meta.force_gt_duration = FORCE_GT_US
            meta.transform_ego_coords_rig_to_aabb.vec.x = BOX_OFFSET_M
            meta.transform_ego_coords_rig_to_aabb.quat.w = 1.0
            for t_us, _, _ in raw["ground_truth"]:
                x, y, yaw = _rig(t_us / 1e6)
                pose = meta.ego_rig_recorded_ground_truth_trajectory.poses.add()
                pose.timestamp_us = t_us
                pose.pose.vec.x, pose.pose.vec.y = x, y
                pose.pose.quat.z, pose.pose.quat.w = np.sin(yaw / 2), np.cos(yaw / 2)
            await log.on_message(entry)
            for t_us, (x, y, yaw) in raw["ego"].items():
                entry = LogEntry()
                entry.actor_poses.timestamp_us = t_us
                actor = entry.actor_poses.actor_poses.add()
                actor.actor_id = "EGO"
                actor.actor_pose.vec.x, actor.actor_pose.vec.y = x, y
                actor.actor_pose.quat.z = np.sin(yaw / 2)
                actor.actor_pose.quat.w = np.cos(yaw / 2)
                await log.on_message(entry)

    asyncio.run(write())
    (rollout / "_complete").touch()


@pytest.fixture
def ego_run(make_run):
    """A finished run that asked for scale 1.2, with the scale resolved, the
    runtime's line logged and an ego `driven_at` the given scale."""

    def build(driven_at: float = 1.2, logged: bool = True, resolved: bool = True):
        entry = make_run("ego")
        entry["config"]["ego_speed_scale"] = 1.2
        run_dir = Path(entry["run_dir"])
        wizard_config = run_dir / "wizard-config.yaml"
        wizard = yaml.safe_load(wizard_config.read_text())
        if resolved:
            wizard["runtime"]["simulation_config"]["ego_speed_scale"] = 1.2
        wizard_config.write_text(yaml.safe_dump(wizard))
        (run_dir / "txt-logs").mkdir()
        (run_dir / "txt-logs" / "runtime_worker_0.log").write_text(
            "Retimed ego: speed_scale=1.2, hand-off speed 10.30 -> 12.36 m/s\n"
            if logged
            else "Session STARTING\n"
        )
        _write_rollout(run_dir, _raw(driven_at))
        return entry

    return build


def test_a_run_whose_ego_reached_the_scaled_speed_completes(ego_run):
    assert read_state(ego_run()).state is State.COMPLETE


def test_a_scale_that_did_not_land_fails(ego_run):
    result = read_state(ego_run(resolved=False))
    assert result.k_status == (
        "config_not_landed: ego_speed_scale requested 1.2, resolved 1.0"
    )


def test_a_run_without_the_runtime_line_fails(ego_run):
    result = read_state(ego_run(logged=False))
    assert result.state is State.FAILED
    assert result.k_status.startswith("ego_speed_not_applied: no 'Retimed ego")


def test_a_run_whose_ego_kept_its_recorded_speed_fails(ego_run):
    result = read_state(ego_run(driven_at=1.0))
    assert result.state is State.FAILED
    assert result.k_status.startswith("ego_speed_not_applied: ego at")
