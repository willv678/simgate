"""Seeded runs: the seed reaches the wizard, is checked in the resolved config
and in the log, is derived per study run, and a kept run can be queued again."""

import asyncio
import json
from pathlib import Path

import pytest
import yaml
from alpasim_grpc.v0.logging_pb2 import LogEntry
from alpasim_utils.logs import LogWriter
from check_replay import compare
from conftest import SCENE_ID
from enqueue import add
from outer import Study, run_seed, run_study
from read_state import SEED_LIMIT, State, load_entry, queue_entries, read_state
from replay import replay_entry
from run_experiment import wizard_command

SEED_ARGS = (
    "+runtime.simulation_config.random_seed=123",
    "+driver.model.force_determinism=true",
)


def test_a_seeded_run_that_landed_and_was_logged_is_kept(make_run):
    assert read_state(make_run("r", seed=123)).state is State.COMPLETE


def test_a_seed_the_wizard_did_not_resolve_fails_the_run(make_run):
    result = read_state(make_run("r", seed=123, resolved_seed=7))
    assert result.k_status == "config_not_landed: seed requested 123, resolved 7"


def test_a_driver_without_determinism_fails_a_seeded_run(make_run):
    entry = make_run("r", seed=123)
    driver = Path(entry["run_dir"]) / "driver-config.yaml"
    config = yaml.safe_load(driver.read_text())
    config["model"] = {}
    driver.write_text(yaml.safe_dump(config))
    assert read_state(entry).k_status == (
        "config_not_landed: force_determinism requested True, resolved False"
    )


def test_a_seed_the_sessions_were_not_opened_with_fails_the_run(make_run):
    result = read_state(make_run("r", seed=123, logged_seed=999))
    assert result.state is State.FAILED
    assert result.k_status.startswith("seed_not_logged: requested 123")


@pytest.mark.parametrize("seed", [0, -1, SEED_LIMIT, True, 1.5, "123"])
def test_an_illegal_seed_never_launches(make_run, seed):
    result = read_state(make_run("r", launched=False, seed=seed))
    assert result.k_status.startswith("preflight_rejected: seed must be")


def test_the_wizard_gets_the_seed_only_when_the_run_has_one(make_run, tmp_path):
    config = make_run("r", launched=False, seed=123)["config"]
    command = wizard_command(config, tmp_path / "r")
    assert tuple(command[-2:]) == SEED_ARGS
    del config["seed"]
    unseeded = wizard_command(config, tmp_path / "r")
    assert not any(arg.startswith(tuple(SEED_ARGS)) for arg in unseeded)


def test_run_seeds_are_reproducible_distinct_and_legal():
    seeds = [run_seed("study", n) for n in range(1, 61)]
    assert seeds == [run_seed("study", n) for n in range(1, 61)]
    assert len(set(seeds)) == 60
    assert all(1 <= seed < SEED_LIMIT for seed in seeds)
    assert run_seed("other", 1) != seeds[0]


def _study(tmp_path: Path, seeded: bool) -> Study:
    return Study(
        name="t",
        queue=tmp_path / "queue",
        trace=tmp_path / "trace.jsonl",
        rounds_file=tmp_path / "rounds.jsonl",
        objective="x",
        candidates=[{"scene_id": "clipgt-a"}],
        varied=("planner_delay_us",),
        rounds=1,
        per_round=3,
        proposer="random",
        seeded=seeded,
    )


@pytest.mark.parametrize("seeded", [True, False])
def test_a_study_queues_each_run_with_its_seed_unless_unseeded(
    tmp_path, monkeypatch, seeded
):
    monkeypatch.setattr("outer.run_inner_loop", lambda study: None)
    run_study(_study(tmp_path, seeded))
    configs = [load_entry(p)["config"] for p in queue_entries(tmp_path / "queue")]
    assert len(configs) == 3
    if seeded:
        assert [c["seed"] for c in configs] == [run_seed("t", n) for n in (1, 2, 3)]
    else:
        assert not any("seed" in c for c in configs)


def test_a_kept_seeded_run_is_queued_again_with_its_config(make_run, tmp_path):
    original = make_run("r", seed=123)
    original["resolution"] = "ACCEPT"
    queue = tmp_path / "replays"
    first = replay_entry(original, queue)
    assert first["name"] == "r_replay1"
    assert first["config"] == original["config"]
    assert first["replay_of"] == "r"
    assert read_state(first).state is State.READY
    add(queue, first)
    assert replay_entry(original, queue)["name"] == "r_replay2"


@pytest.mark.parametrize(
    "change,why",
    [
        ({"seed": None}, "has no seed"),
        ({"resolution": "RE-RUN"}, "not kept"),
        ({"quarantine": "flagged"}, "not kept"),
    ],
)
def test_a_run_that_cannot_be_replayed_exactly_is_refused(
    make_run, tmp_path, change, why
):
    original = {**make_run("r", seed=123, launched=False), "resolution": "ACCEPT"}
    if "seed" in change:
        del original["config"]["seed"]
    else:
        original.update(change)
    with pytest.raises(SystemExit, match=why):
        replay_entry(original, tmp_path / "replays")


def _write_rollout(run: Path, xs: list[float], plan_y: float, image: bytes) -> None:
    """A completed rollout with the ego at (x, 0) every 100 ms, one camera
    frame and one plan per step, and both sessions opened with seed 5."""
    rollout = run / "rollouts" / SCENE_ID / "rollout-0"
    rollout.mkdir(parents=True)

    async def write() -> None:
        async with LogWriter(str(rollout / "rollout.asl")) as log:
            entry = LogEntry()
            aabb = entry.rollout_metadata.actor_definitions.actor_aabb.add()
            aabb.actor_id = "EGO"
            aabb.aabb.size_x, aabb.aabb.size_y = 4.5, 2.0
            await log.on_message(entry)
            for kind in ("driver_session_request", "traffic_session_request"):
                entry = LogEntry()
                getattr(entry, kind).random_seed = 5
                await log.on_message(entry)
            for step, x in enumerate(xs):
                t = 1_000_000 + step * 100_000
                entry = LogEntry()
                entry.actor_poses.timestamp_us = t
                pose = entry.actor_poses.actor_poses.add()
                pose.actor_id = "EGO"
                pose.actor_pose.vec.x = x
                pose.actor_pose.quat.w = 1.0
                await log.on_message(entry)
                entry = LogEntry()
                frame = entry.driver_camera_image.camera_image
                frame.logical_id, frame.frame_end_us = "front", t
                frame.image_bytes = image if step >= 2 else b"same"
                await log.on_message(entry)
                entry = LogEntry()
                waypoint = entry.driver_return.trajectory.poses.add()
                waypoint.timestamp_us = t
                waypoint.pose.vec.y = plan_y if step >= 1 else 0.0
                await log.on_message(entry)

    asyncio.run(write())
    (rollout / "_complete").touch()


def test_check_replay_finds_identical_runs_and_where_others_part(tmp_path):
    xs = [0.0, 1.0, 2.0, 3.0, 4.0]
    _write_rollout(tmp_path / "a", xs, plan_y=0.0, image=b"frame")
    _write_rollout(tmp_path / "b", xs, plan_y=0.0, image=b"frame")
    _write_rollout(tmp_path / "c", [*xs[:3], 3.5, 4.5], plan_y=0.2, image=b"other")
    same = compare(tmp_path / "a", tmp_path / "b", tol=1e-6)
    assert same["identical"] and same["max_pose_diff_m"] == 0.0
    assert same["first_plan_divergence_s"] is None
    parted = compare(tmp_path / "a", tmp_path / "c", tol=1e-6)
    assert not parted["identical"]
    assert parted["max_pose_diff_m"] == pytest.approx(0.5)
    # The plan parts first (step 1), then the frames (step 2), then the pose (step 3).
    assert parted["first_plan_divergence_s"] == 0.1
    assert parted["first_frame_divergence_s"] == 0.2
    assert parted["first_pose_divergence_s"] == 0.3
    assert json.dumps(parted)
