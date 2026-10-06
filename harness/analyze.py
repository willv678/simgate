"""COMPLETE -> append the run's postflight flags and RUNBOOK metrics to results.

Results is one JSON line per kept run, in the queue directory. A run already
in the file is not appended twice.

    uv run python research/harness/analyze.py <entry.json>
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from postflight import validate_postflight
from read_state import State, load_entry, read_state, run_dir

RESULTS_NAME = "results.jsonl"
# The metric columns of the RUNBOOK batch CSV.
METRICS = ("collision_at_fault", "tracking_error", "plan_deviation", "dist_traveled_m")


def aggregate_metrics(path: Path) -> dict[str, float]:
    text = (path / "aggregate" / "metrics_results.txt").read_text(errors="replace")
    values = {}
    for name in METRICS:
        match = re.search(rf"│\s*{name}\s+│\s+([0-9.]+|inf)", text)
        if match is None:
            raise SystemExit(f"{path}: {name} missing from metrics_results.txt")
        values[name] = float(match.group(1))
    return values


def main() -> int:
    entry_path = Path(sys.argv[1])
    entry = load_entry(entry_path)
    state = read_state(entry)
    if state.state is not State.COMPLETE:
        raise SystemExit(f"{entry['name']} is {state.state.value}, not COMPLETE")

    results = entry_path.parent / RESULTS_NAME
    if results.is_file():
        for line in results.read_text(encoding="utf-8").splitlines():
            if json.loads(line)["run_dir"] == entry["run_dir"]:
                print(json.dumps({"appended": False}))
                return 0

    path = run_dir(entry)
    status = validate_postflight(str(path))
    row = {
        "name": entry["name"],
        "run_dir": entry["run_dir"],
        "config": entry["config"],
        "attempt": entry["attempt"],
        "at_fault_collision": status.at_fault_collision,
        "rear_contact": status.rear_contact,
        "solver_status": status.solver_status,
        # The runtime retries a crashed rollout inside one run and keeps the one
        # that completes; more than 1 means it did.
        "rollout_attempts": len(list(path.glob("rollouts/*/*/rollout.asl"))),
        **aggregate_metrics(path),
    }
    with results.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row) + "\n")
    print(json.dumps({"appended": True}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
