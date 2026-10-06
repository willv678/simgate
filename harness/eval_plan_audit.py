"""Can the auditor catch plan faults with the configs hidden?

The g2 batch: 4 lateral-bias and 4 plan-freeze runs and 2 clean runs on two
scenes. Plan faults leave the motion physically possible, so no physics bound
fires and the gate keeps them. Each condition hides the config files and shows
the motion; the conditions differ in the reference:

- one reference, b2_091, on one of the two scenes (as in every audit so far);
- one clean reference per scene (b2_091 and s1_smoke).

With `--queue`, the same two conditions on another plan-fault batch (g3, held
out): every run with a completed rollout, kept or not, and for the per-scene
condition the batch audit's own choice, scene_references(). Writes
plan_audit_eval.json and .txt, or `--out`.

    uv run python research/harness/eval_plan_audit.py
    uv run python research/harness/eval_plan_audit.py --queue g3_plan_queue \
        --out research/harness/plan_audit_eval_g3.json
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from audit import audit, ran_scene, scene_references
from eval_auditor import MODEL
from read_state import ROOT, load_entry, queue_entries

from physics import completed_rollout

HARNESS = Path(__file__).resolve().parent
OUTPUT = HARNESS / "plan_audit_eval.json"
TABLE = HARNESS / "plan_audit_eval.txt"
REFERENCES = {
    "b2_091": HARNESS / "b2_queue" / "091_b2_091.json",
    "s1_smoke": HARNESS / "s1_smoke_queue" / "001_s1_smoke.json",
}
G2 = "g2_plan_queue"
NUMBERS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six"}
CLAIM = (
    "Nominal closed-loop runs on {scenes} scenes: VaVAM drives after a 4.5 s warm-up "
    "on the recorded trajectory, the linear MPC tracks its plan, CATK traffic. "
    "Runs labelled reference are known-good runs of the same setup."
)


def _completed(run_dir: Path) -> bool:
    try:
        completed_rollout(run_dir)
    except FileNotFoundError:
        return False
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed-base", type=int, default=60)
    parser.add_argument("--only", choices=("one reference", "a reference per scene"))
    parser.add_argument("--out", type=Path, default=OUTPUT)
    parser.add_argument("--queue", default=G2)
    args = parser.parse_args()
    entries = [
        e
        for e in map(load_entry, queue_entries(HARNESS / args.queue))
        if _completed(ROOT / e["run_dir"])
    ]
    faulted = {e["name"] for e in entries if e["fault"]}
    base_runs = {e["name"]: ROOT / e["run_dir"] for e in entries}
    base_labels = {e["name"]: e["config"] for e in entries}
    results, lines = (
        {},
        ["condition\tplan faults caught\tclean flagged\treferences flagged"],
    )
    scenes = {ran_scene(e) for e in entries}
    if args.queue == G2:
        per_scene = {name: load_entry(path) for name, path in REFERENCES.items()}
    else:
        found = scene_references(scenes, HARNESS / args.queue).values()
        per_scene = {entry["name"]: entry for entry in found}
    conditions = {
        "one reference": {"b2_091": load_entry(REFERENCES["b2_091"])},
        "a reference per scene": per_scene,
    }
    kinds = sorted({e["fault"]["kind"] for e in entries if e["fault"]})
    clean = len(entries) - len(faulted)
    for seed, (condition, refs) in enumerate(conditions.items()):
        if args.only and condition != args.only:
            continue
        runs, labels = dict(base_runs), dict(base_labels)
        for name, ref in refs.items():
            runs[name] = ROOT / ref["run_dir"]
            labels[name] = {**ref["config"], "reference": True}
        report = audit(
            CLAIM.format(scenes=NUMBERS[len(scenes)]),
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
                for kind in kinds
            },
            "clean_flagged": sorted(flagged - faulted - set(refs)),
            "refs_flagged": sorted(flagged & set(refs)),
        }
        r = results[condition]
        lines.append(
            f"{condition}\t{len(caught)}/{len(faulted)} {r['by_kind']}\t"
            f"{len(r['clean_flagged'])}/{clean}\t{len(r['refs_flagged'])}"
        )
        print(lines[-1], flush=True)
    lines.append(f"model\t{MODEL}\tconfigs hidden, motion shown")
    args.out.write_text(json.dumps(results, indent=1) + "\n")
    args.out.with_suffix(".txt").write_text("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
