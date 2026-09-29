"""State of one queued run: READY, RUNNING, COMPLETE, FAILED, or DONE.

A queue entry is a JSON file that names a run directory and the config
requested for it. The state comes from that entry and from the files the run
left behind, using the checks that already exist:

- preflight (K⁻) on the requested config, before and after launch;
- the environment problems run_experiment.py found instead of launching;
- the wizard exit code, written next to the run by run_experiment.py;
- postflight (K⁺) on the run directory;
- whether the requested values are the ones the wizard resolved.

This module only reads. The scripts the loop dispatches write the entry.

    uv run python research/harness/read_state.py <entry.json>
"""

import csv
import json
import os
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

from analyze_cp2 import extract_resolved_config
from postflight import validate_postflight
from preflight import PreflightError, validate_preflight

ROOT = Path(__file__).resolve().parents[2]

# Launches per lineage (the first launch plus recoveries) before a person decides.
MAX_ATTEMPTS = 3
# Every key of a queue config. Each is checked against the resolved config.
CONFIG_KEYS = (
    "context_length",
    "planner_delay_us",
    "scene_file",
    "scene_id",
    "trafficsim_device",
)
# Keys a CONFIGURE may change. The scene is the experiment, so it is not one.
CONFIGURABLE_KEYS = (
    "context_length",
    "planner_delay_us",
    "scene_file",
    "trafficsim_device",
)
TRAFFICSIM_DEVICES = ("cpu", "cuda")


class State(Enum):
    READY = "READY"
    RUNNING = "RUNNING"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"
    DONE = "DONE"


@dataclass(frozen=True)
class RunState:
    state: State
    k_status: str


def load_entry(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_entry(path: Path, entry: dict) -> None:
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(entry, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def run_dir(entry: dict) -> Path:
    return ROOT / entry["run_dir"]


def console_log(entry: dict) -> Path:
    """Wizard stdout and stderr, next to the run directory as in L8."""
    path = run_dir(entry)
    return path.parent / f"{path.name}_console.log"


def exit_file(entry: dict) -> Path:
    path = run_dir(entry)
    return path.parent / f"{path.name}_exit_code"


def preflight_config(config: dict) -> dict:
    """The dict preflight.py checks, built from a queue config.

    run_experiment.py writes the Hydra delay override from planner_delay_us,
    so the requested and Hydra delays are the same value here. Whether the
    delay landed is checked after exit, against the resolved config.
    """
    return {
        "context_length": config["context_length"],
        "hydra_delay": config["planner_delay_us"],
        "request_delay": config["planner_delay_us"],
        "scene_file": str(ROOT / config["scene_file"]),
    }


def config_problem(config: dict) -> str | None:
    """Why this config must not launch, or None. The one preflight every caller uses."""
    try:
        validate_preflight(preflight_config(config))
    except PreflightError as exc:
        return str(exc)
    if config["trafficsim_device"] not in TRAFFICSIM_DEVICES:
        return f"trafficsim_device must be one of {TRAFFICSIM_DEVICES}, got {config['trafficsim_device']!r}"
    with (ROOT / config["scene_file"]).open(encoding="utf-8") as handle:
        scene_ids = {row["scene_id"] for row in csv.DictReader(handle)}
    if config["scene_id"] not in scene_ids:
        return f"scene_id {config['scene_id']} is not in {config['scene_file']}"
    return None


def _exit_code(entry: dict) -> int | None:
    path = exit_file(entry)
    if not path.is_file():
        return None
    return int(path.read_text(encoding="utf-8").strip())


def _alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def config_not_landed(entry: dict) -> list[str]:
    """Requested values that differ from what the wizard resolved."""
    path = run_dir(entry)
    config = entry["config"]
    driver = yaml.safe_load((path / "driver-config.yaml").read_text(encoding="utf-8"))
    wizard = yaml.safe_load((path / "wizard-config.yaml").read_text(encoding="utf-8"))
    resolved = {
        "context_length": driver["inference"]["context_length"],
        "planner_delay_us": extract_resolved_config(path)["planner_delay_us"],
        "scene_file": wizard["scenes"]["scenes_csv"],
        "scene_id": wizard["scenes"]["scene_ids"],
        "trafficsim_device": wizard["trafficsim"]["catk"]["device"],
    }
    requested = {
        "context_length": config["context_length"],
        "planner_delay_us": config["planner_delay_us"],
        "scene_file": [str(ROOT / config["scene_file"])],
        "scene_id": [config["scene_id"]],
        "trafficsim_device": config["trafficsim_device"],
    }
    return [
        f"{key} requested {requested[key]}, resolved {resolved[key]}"
        for key in CONFIG_KEYS
        if requested[key] != resolved[key]
    ]


def read_state(entry: dict) -> RunState:
    if entry["resolution"] is not None:
        return RunState(State.DONE, f"resolved: {entry['resolution']}")

    problem = config_problem(entry["config"])
    if problem is not None:
        return RunState(State.FAILED, f"preflight_rejected: {problem}")

    if not entry["launched"]:
        if entry["environment"]:
            return RunState(
                State.FAILED, "environment: " + "; ".join(entry["environment"])
            )
        return RunState(State.READY, "preflight_ok")

    code = _exit_code(entry)
    if code is None:
        if entry["pid"] is not None and _alive(entry["pid"]):
            return RunState(State.RUNNING, f"pid {entry['pid']}")
        return RunState(State.FAILED, "process_lost: launcher gone, no exit code")

    status = validate_postflight(str(run_dir(entry)))
    failures = []
    if code != 0:
        failures.append(f"wizard_exit_code: {code}")
    if not status.success:
        failures.append(f"postflight_failed: {status.error}")
    if failures:
        return RunState(State.FAILED, "; ".join(failures))

    mismatches = config_not_landed(entry)
    if mismatches:
        return RunState(State.FAILED, "config_not_landed: " + "; ".join(mismatches))

    return RunState(
        State.COMPLETE,
        f"postflight_success: at_fault={status.at_fault_collision}, "
        f"rear={status.rear_contact}",
    )


def main() -> int:
    entry = load_entry(Path(sys.argv[1]))
    result = read_state(entry)
    print(json.dumps({"state": result.state.value, "k_status": result.k_status}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
