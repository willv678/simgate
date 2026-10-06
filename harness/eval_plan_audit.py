"""Can the auditor catch plan faults with the configs hidden?

The g2 batch: 4 lateral-bias and 4 plan-freeze runs and 2 clean runs on two
scenes. Plan faults leave the motion physically possible, so no physics bound
fires and the gate keeps them. Each condition hides the config files and shows
the motion; the conditions differ in the reference:

- one reference, b2_091, on one of the two scenes (as in every audit so far);
- one clean reference per scene (b2_091 and s1_smoke).

Writes plan_audit_eval.json and .txt.

    uv run python research/harness/eval_plan_audit.py
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from audit import audit
from eval_auditor import MODEL
from read_state import ROOT, load_entry, queue_entries

HARNESS = Path(__file__).resolve().parent
OUTPUT = HARNESS / "plan_audit_eval.json"
TABLE = HARNESS / "plan_audit_eval.txt"
REFERENCES = {
    "b2_091": HARNESS / "b2_queue" / "091_b2_091.json",
    "s1_smoke": HARNESS / "s1_smoke_queue" / "001_s1_smoke.json",
}
CLAIM = (
    "Nominal closed-loop runs on two scenes: VaVAM drives after a 4.5 s warm-up "
    "on the recorded trajectory, the linear MPC tracks its plan, CATK traffic. "
    "Runs labelled reference are known-good runs of the same setup."
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed-base", type=int, default=60)
    parser.add_argument("--only", choices=("one reference", "a reference per scene"))
    parser.add_argument("--out", type=Path, default=OUTPUT)
    args = parser.parse_args()
    entries = [load_entry(p) for p in queue_entries(HARNESS / "g2_plan_queue")]
    faulted = {e["name"] for e in entries if e["fault"]}
    base_runs = {e["name"]: ROOT / e["run_dir"] for e in entries}
    base_labels = {e["name"]: e["config"] for e in entries}
    results, lines = (
        {},
        ["condition\tplan faults caught\tclean flagged\treferences flagged"],
    )
    conditions = {
        "one reference": ["b2_091"],
        "a reference per scene": list(REFERENCES),
    }
    for seed, (condition, refs) in enumerate(conditions.items()):
        if args.only and condition != args.only:
            continue
        runs, labels = dict(base_runs), dict(base_labels)
        for name in refs:
            ref = load_entry(REFERENCES[name])
            runs[name] = ROOT / ref["run_dir"]
            labels[name] = {**ref["config"], "reference": True}
        report = audit(
            CLAIM,
            runs,
            labels,
            MODEL,
            seed=args.seed_base + seed,
            configs=False,
            motion=True,
        )
        flagged = set(report["flags"])
        caught = flagged & faulted
        results[condition] = {
            "flags": report["flags"],
            "caught": sorted(caught),
            "by_kind": {
                kind: sum(
                    e["name"] in caught
                    for e in entries
                    if e["fault"] and e["fault"]["kind"] == kind
                )
                for kind in ("lateral_bias", "plan_freeze")
            },
            "clean_flagged": sorted(flagged - faulted - set(refs)),
            "refs_flagged": sorted(flagged & set(refs)),
        }
        r = results[condition]
        lines.append(
            f"{condition}\t{len(caught)}/{len(faulted)} {r['by_kind']}\t"
            f"{len(r['clean_flagged'])}/2\t{len(r['refs_flagged'])}"
        )
        print(lines[-1], flush=True)
    lines.append(f"model\t{MODEL}\tconfigs hidden, motion shown")
    args.out.write_text(json.dumps(results, indent=1) + "\n")
    args.out.with_suffix(".txt").write_text("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
