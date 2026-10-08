"""Fixtures that build finished-run directories without a simulator."""

import asyncio
from pathlib import Path

import pandas as pd
import pytest
import yaml
from alpasim_grpc.v0.logging_pb2 import LogEntry
from alpasim_utils.logs import LogWriter

SCENE_ID = "clipgt-test-scene"

AGGREGATE = """\
│ collision_at_fault                  │     {at_fault:.2f}     │       max        │
│ collision_rear                      │     0.00     │       max        │
│ dist_traveled_m                     │    28.05     │       last       │
│ plan_deviation                      │     0.21     │       mean       │
│ tracking_error                      │     0.42     │       mean       │
"""


@pytest.fixture(autouse=True)
def no_promoted_rules(tmp_path: Path, monkeypatch):
    """Tests start from an empty rule set. Subprocesses inherit it."""
    rules = tmp_path / "promoted.json"
    rules.write_text("[]")
    monkeypatch.setenv("ALPASIM_RULES", str(rules))
    physics = tmp_path / "physics.json"
    physics.write_text('{"enabled": false, "max": {}}')
    monkeypatch.setenv("ALPASIM_PHYSICS", str(physics))
    return rules


def write_session_seeds(rollout: Path, seed: int) -> None:
    """A completed rollout whose log opens both sessions with `seed`."""

    async def write() -> None:
        async with LogWriter(str(rollout / "rollout.asl")) as log:
            entry = LogEntry()
            entry.driver_session_request.random_seed = seed
            await log.on_message(entry)
            entry = LogEntry()
            entry.traffic_session_request.random_seed = seed
            await log.on_message(entry)

    asyncio.run(write())
    (rollout / "_complete").touch()


@pytest.fixture
def scene_file(tmp_path: Path) -> Path:
    path = tmp_path / "sim_scenes.csv"
    path.write_text(f"uuid,scene_id\nu1,{SCENE_ID}\n", encoding="utf-8")
    return path


@pytest.fixture
def make_run(tmp_path: Path, scene_file: Path):
    """Queue entry plus the files a wizard run leaves behind."""

    def build(
        name: str,
        *,
        context_length: int = 8,
        planner_delay_us: int = 0,
        launched: bool = True,
        exit_code: int | None = 0,
        metrics: bool = True,
        resolved_delay_us: int | None = None,
        resolved_device: str | None = None,
        environment: list[str] | None = None,
        env_cleanups: int = 0,
        at_fault: bool = False,
        attempt: int = 1,
        seed: int | None = None,
        resolved_seed: int | None = None,
        logged_seed: int | None = None,
    ) -> dict:
        """A seeded run's seed lands and is logged unless `resolved_seed` or
        `logged_seed` says otherwise."""
        run_dir = tmp_path / "runs" / name
        entry = {
            "name": name,
            "run_dir": str(run_dir),
            "config": {
                "context_length": context_length,
                "planner_delay_us": planner_delay_us,
                "scene_file": str(scene_file),
                "scene_id": SCENE_ID,
                "trafficsim_device": "cpu",
            },
            "attempt": attempt,
            "parent": None,
            "launched": launched,
            "pid": None,
            "launched_at": None,
            "environment": environment,
            "env_cleanups": env_cleanups,
            "resolution": None,
            "diagnosis": None,
            "fault": None,
        }
        if seed is not None:
            entry["config"]["seed"] = seed
        if not launched:
            return entry
        run_dir.mkdir(parents=True)
        if exit_code is not None:
            (run_dir.parent / f"{name}_exit_code").write_text(f"{exit_code}\n")
        (run_dir / "driver-config.yaml").write_text(
            yaml.safe_dump(
                {
                    "inference": {
                        "context_length": context_length,
                        "subsample_factor": 1,
                    },
                    "model": {"force_determinism": True} if seed is not None else {},
                }
            )
        )
        delay = planner_delay_us if resolved_delay_us is None else resolved_delay_us
        simulation = {
            "planner_delay_us": delay,
            "cameras": [{"frame_interval_us": 500_000}],
        }
        if seed is not None:
            simulation["random_seed"] = seed if resolved_seed is None else resolved_seed
        (run_dir / "wizard-config.yaml").write_text(
            yaml.safe_dump(
                {
                    "runtime": {
                        "endpoints": {"trafficsim": {"skip": False}},
                        "simulation_config": simulation,
                    },
                    "scenes": {
                        "scenes_csv": [str(scene_file)],
                        "scene_ids": [SCENE_ID],
                    },
                    "trafficsim": {"catk": {"device": resolved_device or "cpu"}},
                }
            )
        )
        if seed is not None:
            rollout = run_dir / "rollouts" / SCENE_ID / "rollout-0"
            rollout.mkdir(parents=True)
            write_session_seeds(rollout, seed if logged_seed is None else logged_seed)
        if metrics:
            pd.DataFrame({"name": ["collision_rear"], "values": [[0.0]]}).to_parquet(
                run_dir / "metrics.parquet"
            )
            (run_dir / "aggregate").mkdir()
            (run_dir / "aggregate" / "metrics_results.txt").write_text(
                AGGREGATE.format(at_fault=float(at_fault))
            )
        return entry

    return build
