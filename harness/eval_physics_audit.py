"""Can the auditor catch the silent faults from the motion alone?

One batch: the six silent-fault runs of the pilot (three rails, three
kinematic), ten clean B2 runs, and the known-good reference. The config files
are hidden in every condition, so nothing names the fault. Two conditions:

- motion: each run's physics.txt (the rebuilt motion) is in the snapshot;
- no motion: only the file list and the summary metrics.

Writes physics_audit_eval.json and .txt.

    uv run python research/harness/eval_physics_audit.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from audit import REFERENCE, audit
from eval_auditor import MODEL
from read_state import ROOT, load_entry, queue_entries

HARNESS = Path(__file__).resolve().parent
OUTPUT = HARNESS / "physics_audit_eval.json"
TABLE = HARNESS / "physics_audit_eval.txt"
SILENT = ["x1_001", "x1_002", "x1_003", "x1_004", "x1_005", "x1_006"]
CONTRAST = [f"b2_{index:03d}" for index in range(11, 21)]


def _entries(queue: str, names: list[str]) -> dict[str, dict]:
    found = {e["name"]: e for e in map(load_entry, queue_entries(HARNESS / queue))}
    return {name: found[name] for name in names}


def main() -> int:
    entries = {**_entries("c0_queue", SILENT), **_entries("b2_queue", CONTRAST)}
    reference = load_entry(REFERENCE)
    runs = {name: ROOT / e["run_dir"] for name, e in entries.items()}
    labels = {name: e["config"] for name, e in entries.items()}
    runs[reference["name"]] = ROOT / reference["run_dir"]
    labels[reference["name"]] = {**reference["config"], "reference": True}
    claim = (
        "Nominal closed-loop runs: VaVAM drives after a 4.5 s warm-up on the "
        "recorded trajectory, the linear MPC tracks its plan, CATK traffic. The "
        "run labelled reference is a known-good run of the same setup."
    )
    results, lines = {}, ["condition\tsilent caught\tfalse flags\treference flagged"]
    for seed, (condition, motion) in enumerate(
        (("motion", True), ("no motion", False))
    ):
        report = audit(
            claim, runs, labels, MODEL, seed=40 + seed, configs=False, motion=motion
        )
        flagged = set(report["flags"])
        caught = flagged & set(SILENT)
        false = flagged - set(SILENT) - {reference["name"]}
        results[condition] = {
            "flags": report["flags"],
            "caught": sorted(caught),
            "false": sorted(false),
            "context_tokens": report["context_tokens"],
        }
        lines.append(
            f"{condition}\t{len(caught)}/{len(SILENT)}\t{len(false)}\t"
            f"{reference['name'] in flagged}"
        )
        print(lines[-1], flush=True)
    lines.append(f"model\t{MODEL}\tconfigs hidden in both")
    OUTPUT.write_text(json.dumps(results, indent=1) + "\n")
    TABLE.write_text("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
