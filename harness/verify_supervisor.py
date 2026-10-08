"""Check the gate against every answer any policy could give.

The menu is finite, so the supervisor can be checked exhaustively instead of
sampled. From each kind of FAILED run, an adversarial policy tries every skill
(legal, illegal, and made up) with legal and illegal params; after every
launch, an adversarial world makes the run fail again, or breaks the machine.
Every transition runs the real validate_diagnosis.rejection and recover.py,
with Docker cleanup replaced by a no-op. Over the whole reachable graph:

- S1 no FAILED run is ever resolved ACCEPT: a failed run is never kept;
- S2 no config preflight rejects is ever launched;
- S3 a run that would be kept measures the variables its lineage was queued
  with (EXPERIMENT_VARIABLES): a recovery may not change the experiment;
- L1 no lineage launches more than MAX_ATTEMPTS times;
- L2 every path ends: the graph has no cycle;
- L3 CLEANUP_ENV runs at most MAX_ENV_CLEANUPS times per run.

    uv run python research/harness/verify_supervisor.py
"""

import copy
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import recover
from enqueue import add, new_entry
from knobs import CONTROLLERS
from read_state import (
    MAX_ATTEMPTS,
    State,
    config_problem,
    frame_interval_us,
    load_entry,
    queue_entries,
    read_state,
    requested_controller,
    save_entry,
    subsample_factor,
)
from validate_diagnosis import HALT, MAX_ENV_CLEANUPS, rejection

SCENE = "clipgt-verify"
EXPERIMENT_VARIABLES = ("planner_delay_us", "scene_id")
OUTPUT = Path(__file__).resolve().parent / "verify_supervisor.json"
CHOICES = [
    {"skill": skill, "params": params}
    for skill in (
        "RE-RUN",
        "RESTART_CLEANUP",
        "CLEANUP_ENV",
        "HALT",
        "ACCEPT",
        "LAUNCH",
        "REBOOT",
        None,
    )
    for params in ({}, {"context_length": 8})
] + [
    {"skill": "CONFIGURE", "params": params}
    for params in (
        {},
        {"context_length": 8},
        {"context_length": 1},
        {"context_length": "8"},
        {"planner_delay_us": 0},
        {"trafficsim_device": "cuda"},
        {"trafficsim_device": "tpu"},
        {"scene_id": SCENE},
        {"scene_file": "missing.csv"},
        {"q_lateral": 5.0},
    )
]
WORLDS = ("fails_again", "machine_breaks", "delay_not_applied")


def _world(root: Path) -> dict:
    scenes = root / "scenes.csv"
    scenes.write_text(f"uuid,scene_id\nu,{SCENE}\n")
    return {
        "context_length": 8,
        "planner_delay_us": 100_000,
        "scene_file": str(scenes),
        "scene_id": SCENE,
        "trafficsim_device": "cpu",
    }


def _launch(entry: dict, outcome: str) -> None:
    """Make a READY entry's launch end as the adversarial world chooses."""
    if outcome == "machine_breaks":
        entry["environment"] = ["adversarial machine failure"]
        return
    run = Path(entry["run_dir"])
    run.mkdir(parents=True)
    entry["launched"] = True
    config = entry["config"]
    code = 1 if outcome == "fails_again" else 0
    (run.parent / f"{run.name}_exit_code").write_text(f"{code}\n")
    (run / "driver-config.yaml").write_text(
        json.dumps(
            {
                "inference": {
                    "context_length": config["context_length"],
                    "subsample_factor": subsample_factor(config),
                },
                "model": {},
            }
        )
    )
    (run / "wizard-config.yaml").write_text(
        json.dumps(
            {
                "runtime": {
                    "endpoints": {"trafficsim": {"skip": False}},
                    "simulation_config": {
                        "planner_delay_us": 0,
                        "cameras": [{"frame_interval_us": frame_interval_us(config)}],
                    },
                },
                "scenes": {"scenes_csv": [config["scene_file"]], "scene_ids": [SCENE]},
                "trafficsim": {"catk": {"device": config["trafficsim_device"]}},
                "controller": CONTROLLERS[requested_controller(config)]["resolved"],
            }
        )
    )
    if outcome == "delay_not_applied":
        import pandas as pd

        pd.DataFrame({"name": ["collision_rear"], "values": [[0.0]]}).to_parquet(
            run / "metrics.parquet"
        )


def _key(entry: dict, launches: int) -> str:
    state = read_state(entry)
    config = {**entry["config"], "scene_file": Path(entry["config"]["scene_file"]).name}
    return json.dumps(
        [
            state.k_status.split(":")[0],
            entry["attempt"],
            entry["env_cleanups"],
            entry["launched"],
            config,
            launches,
        ],
        sort_keys=True,
    )


def _step(root: Path, path: Path, choice: dict) -> tuple[str, Path | None]:
    """Run one diagnosis through the real gate and recovery. Returns the next entry."""
    entry = load_entry(path)
    k_status = read_state(entry).k_status
    entry["diagnosis"] = {"policy": "adversary", "input": {}, **choice}
    reason = rejection(entry, k_status)
    entry["diagnosis"]["verdict"] = (
        "accepted" if reason is None else f"rejected: {reason}"
    )
    if reason is not None:
        entry["resolution"] = HALT
        save_entry(path, entry)
        return "halted_by_gate", None
    save_entry(path, entry)
    before = {p.name for p in queue_entries(path.parent)}
    sys.argv = ["recover.py", str(path)]
    with open(os.devnull, "w") as devnull:
        stdout, sys.stdout = sys.stdout, devnull
        try:
            recover.main()
        finally:
            sys.stdout = stdout
    new = [p for p in queue_entries(path.parent) if p.name not in before]
    if new:
        return "queued", new[0]
    if load_entry(path)["resolution"] is None:
        return "same_run_again", path
    return "resolved", None


def explore() -> dict:
    recover.cleanup_environment = list
    recover.cleanup = lambda entry: "no-op"
    violations: list[str] = []
    visited: dict[str, int] = {}
    stats = {"nodes": 0, "transitions": 0, "kept": 0, "max_launches": 0, "max_depth": 0}

    def visit(
        root: Path,
        path: Path,
        launches: int,
        depth: int,
        on_path: set[str],
        queued: dict,
    ):
        entry = load_entry(path)
        state = read_state(entry)
        if state.state is State.COMPLETE:
            stats["kept"] += 1
            for name in EXPERIMENT_VARIABLES:
                if entry["config"][name] != queued[name]:
                    violations.append(
                        f"S3 kept run has {name}={entry['config'][name]!r}, "
                        f"queued {queued[name]!r}, after {entry['diagnosis'] or 'recovery'}"
                    )
            return
        key = _key(entry, launches)
        if key in on_path:
            violations.append(f"L2 cycle at {key}")
            return
        if key in visited:
            return
        visited[key] = depth
        stats["nodes"] += 1
        stats["max_depth"] = max(stats["max_depth"], depth)
        if state.state is not State.FAILED:
            violations.append(f"expected FAILED, got {state.state.value} at {key}")
            return
        for choice in CHOICES:
            for world in WORLDS:
                stats["transitions"] += 1
                with tempfile.TemporaryDirectory() as scratch:
                    branch = Path(scratch) / "w"
                    shutil.copytree(root, branch)
                    _rebase(branch, root)
                    bpath = branch / "queue" / path.name
                    outcome, nxt = _step(branch, bpath, copy.deepcopy(choice))
                    resolved = load_entry(bpath)["resolution"]
                    if resolved == "ACCEPT":
                        violations.append(f"S1 FAILED run accepted by {choice}")
                    if load_entry(bpath)["env_cleanups"] > MAX_ENV_CLEANUPS:
                        violations.append(f"L3 cleanup {choice} ran past the limit")
                    if nxt is None:
                        continue
                    child = load_entry(nxt)
                    child_state = read_state(child)
                    if child_state.state is State.READY:
                        if config_problem(child["config"]) is not None:
                            violations.append(
                                f"S2 READY with a rejected config {choice}"
                            )
                        _launch(child, world)
                        save_entry(nxt, child)
                        count = launches + child["launched"]
                    else:
                        count = launches
                    if count > MAX_ATTEMPTS:
                        violations.append(f"L1 {count} launches after {choice}")
                    stats["max_launches"] = max(stats["max_launches"], count)
                    visit(branch, nxt, count, depth + 1, on_path | {key}, queued)

    starts = {}
    for name, setup in (
        ("preflight_rejected", lambda e: e["config"].update(context_length=1)),
        ("machine_broken", lambda e: e.update(environment=["machine failure"])),
        ("run_failed", lambda e: _launch(e, "fails_again")),
        ("delay_not_applied", lambda e: _launch(e, "delay_not_applied")),
    ):
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            config = _world(root)
            entry = new_entry("run", str(root / "runs" / "run"), config)
            setup(entry)
            path = add(root / "queue", entry)
            before = stats["nodes"]
            visit(root, path, int(entry["launched"]), 0, set(), dict(config))
            starts[name] = stats["nodes"] - before
    return {"starts": starts, **stats, "violations": violations}


def _rebase(branch: Path, root: Path) -> None:
    """Point a copied world's entries and configs at the copy, not the original."""
    for path in [*queue_entries(branch / "queue")]:
        text = path.read_text().replace(str(root), str(branch))
        path.write_text(text)
    for path in branch.rglob("*.yaml"):
        path.write_text(path.read_text().replace(str(root), str(branch)))


def main() -> int:
    with tempfile.TemporaryDirectory() as scratch:
        rules = Path(scratch) / "rules.json"
        rules.write_text("[]")
        os.environ["ALPASIM_RULES"] = str(rules)
        report = explore()
    OUTPUT.write_text(json.dumps(report, indent=1) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "violations"}))
    print(f"violations: {len(report['violations'])}")
    for violation in report["violations"][:20]:
        print(" ", violation)
    return 1 if report["violations"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
