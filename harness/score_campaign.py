"""Score a fault-injection campaign queue, per fault kind.

A lineage is a queued run and the retries recovery queued after it. For each
lineage: whether the gate called any run in it FAILED, the skills chosen,
whether the lineage ended in a kept run, how many launches it spent, and
whether it was halted for a person.

Validity is ground truth from the injection: a launch that carried a fault in
CORRUPTS_DATA measured something other than its label. gate_invalid_kept counts
such launches the gate kept; the silent faults are the ones it cannot see.
The no-gate arm is computed from the same runs: keep every first launch whose
wizard exit code is 0, as a batch without preflight and postflight would.

    uv run python research/harness/score_campaign.py research/harness/c0_queue
"""

import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from read_state import exit_file, load_entry, queue_entries

# Faults whose run can exit 0 with data that does not measure its label.
CORRUPTS_DATA = {
    "delete_metrics",
    "corrupt_metrics",
    "drop_delay",
    "rails",
    "kinematic",
}


def lineages(queue: Path) -> list[list[dict]]:
    entries = {path.name: load_entry(path) for path in queue_entries(queue)}
    children = defaultdict(list)
    for name, entry in entries.items():
        if entry["parent"] is not None:
            children[entry["parent"]].append(name)
    chains = []
    for name, entry in entries.items():
        if entry["parent"] is not None:
            continue
        chain = [entry]
        while children[name]:
            name = children[name][0]
            chain.append(entries[name])
        chains.append(chain)
    return chains


def _exit_code(entry: dict) -> int | None:
    path = exit_file(entry)
    return int(path.read_text().strip()) if path.is_file() else None


def score(queue: Path) -> dict:
    rows = defaultdict(
        lambda: {
            "lineages": 0,
            "detected": 0,
            "recovered": 0,
            "halted": 0,
            "launches": 0,
            "skills": defaultdict(int),
            "gate_invalid_kept": 0,
            "no_gate_kept": 0,
            "no_gate_invalid_kept": 0,
        }
    )
    for chain in lineages(queue):
        first = chain[0]
        kind = first["fault"]["kind"] if first["fault"] else "clean"
        row = rows[kind]
        row["lineages"] += 1
        # A machine fault is recovered in place, so look for any diagnosis.
        row["detected"] += any(entry["diagnosis"] is not None for entry in chain)
        row["recovered"] += chain[-1]["resolution"] == "ACCEPT"
        row["halted"] += chain[-1]["resolution"] == "HALT"
        row["launches"] += sum(entry["launched"] for entry in chain)
        for entry in chain:
            if entry["diagnosis"] is not None:
                row["skills"][str(entry["diagnosis"]["skill"])] += 1
        corrupts = kind in CORRUPTS_DATA
        row["gate_invalid_kept"] += sum(
            entry["resolution"] == "ACCEPT"
            and entry["fault"] is not None
            and entry["fault"]["kind"] in CORRUPTS_DATA
            for entry in chain
        )
        if first["launched"] and _exit_code(first) == 0:
            row["no_gate_kept"] += 1
            row["no_gate_invalid_kept"] += corrupts
    return {kind: {**row, "skills": dict(row["skills"])} for kind, row in rows.items()}


def main() -> int:
    queue = Path(sys.argv[1])
    table = score(queue)
    (queue / "score.json").write_text(json.dumps(table, indent=1) + "\n")
    print(json.dumps(table, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
