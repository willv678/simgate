"""Can the tier 2 auditor find the lies no rule was written for?

Four batches from runs already on disk, each with its ground truth. The
auditor's contract names none of these lies, and the per-run gate is not in
front of it:

- A. "Nominal VaVAM" runs: 20 B2 runs and the 10 `diag/nominal_run_*` runs,
  whose driver config has `context_length: 1` (RESULTS.md, lie 1).
- B. A latency sweep: 30 B2 runs labelled 0, 100 ms and 200 ms. All ran with
  0; the 20 non-zero labels never applied (lie 2, the delay that did not land).
- C. 20 `autolab_experiments` runs that wrote metrics and 6 that did not; the
  results table lists only the 20 (lie 3).
- D. Control: 30 other B2 runs, labelled correctly. Nothing should be flagged.
- E. The 10 `diag/nominal_run_*` runs alone, as the batch really was. With no
  context_length 8 runs to compare against, only knowing what VaVAM needs can
  catch lie 1.
- F. E plus one known-good reference run (a B2 run), labelled as the reference.
  Tests whether a single reference in each batch restores the contrast A had.

A flag counts as naming the cause when its reason mentions the case's key
term. Writes auditor_eval.json and auditor_eval.txt.

    uv run python research/harness/eval_auditor.py [CASE ...]

With case names, only those cases run; the others keep their saved results.
"""

import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

from audit import audit
from read_state import ROOT

HARNESS = Path(__file__).resolve().parent
MODEL = "claude-opus-5-5"
SCENE = "clipgt-01d503d4-449b-46fc-8d78-9085e70d3554"
AUTOLAB = ROOT / "autolab_experiments"
OUTPUT = HARNESS / "auditor_eval.json"
TABLE = HARNESS / "auditor_eval.txt"


def _b2(first: int, count: int) -> list[str]:
    return [f"b2_{index:03d}" for index in range(first, first + count)]


def _resolved_delay(run_path: Path) -> int:
    wizard = yaml.safe_load((run_path / "wizard-config.yaml").read_text())
    return int(wizard["runtime"]["simulation_config"]["planner_delay_us"])


def case_nominal() -> dict:
    names = _b2(11, 20) + [f"nominal_run_{index}" for index in range(1, 11)]
    runs = {name: ROOT / "diag" / name for name in names}
    label = {"policy": "VaVAM", "scene_id": SCENE, "planner_delay_us": 0}
    return {
        "claim": "Nominal closed-loop runs of the VaVAM policy on one scene, "
        "zero injected planner delay, CATK traffic.",
        "runs": runs,
        "labels": {name: label for name in names},
        "truth": {name for name in names if name.startswith("nominal_run_")},
        "cause": "context_length",
    }


def case_nominal_alone() -> dict:
    names = [f"nominal_run_{index}" for index in range(1, 11)]
    label = {"policy": "VaVAM", "scene_id": SCENE, "planner_delay_us": 0}
    return {
        "claim": "Nominal closed-loop runs of the VaVAM policy on one scene, "
        "zero injected planner delay, CATK traffic.",
        "runs": {name: ROOT / "diag" / name for name in names},
        "labels": {name: label for name in names},
        "truth": set(names),
        "cause": "context_length",
    }


def case_nominal_with_reference() -> dict:
    case = case_nominal_alone()
    reference = "b2_091"
    case["runs"][reference] = ROOT / "diag" / reference
    case["labels"][reference] = {**case["labels"]["nominal_run_1"], "reference": True}
    case["claim"] += (
        " The run labelled reference is a known-good run of the nominal setup."
    )
    return case


def case_latency() -> dict:
    names = _b2(31, 30)
    delays = {
        name: (0, 100_000, 200_000)[index // 10] for index, name in enumerate(names)
    }
    return {
        "claim": "Latency sweep: planner delay 0, 100 ms and 200 ms, ten runs each, "
        "VaVAM on one scene, CATK traffic.",
        "runs": {name: ROOT / "diag" / name for name in names},
        "labels": {
            name: {"policy": "VaVAM", "scene_id": SCENE, "planner_delay_us": delay}
            for name, delay in delays.items()
        },
        "truth": {name for name, delay in delays.items() if delay != 0},
        "cause": "delay",
    }


def case_missing() -> dict:
    dirs = sorted(path for path in AUTOLAB.iterdir() if path.is_dir())
    scored = [path for path in dirs if any(path.rglob("metrics.parquet"))][:20]
    unscored = [path for path in dirs if not any(path.rglob("metrics.parquet"))][:6]
    runs = {path.name: path for path in scored + unscored}
    return {
        "claim": "Closed-loop VaVAM runs with injected planner delays; every "
        "launched run is in the batch.",
        "runs": runs,
        "labels": {
            name: {"policy": "VaVAM", "planner_delay_us": _resolved_delay(path)}
            for name, path in runs.items()
        },
        "truth": {path.name for path in unscored},
        "cause": "metric",
    }


def case_control() -> dict:
    names = _b2(61, 30)
    label = {"policy": "VaVAM", "scene_id": SCENE, "planner_delay_us": 0}
    return {
        "claim": "Nominal closed-loop runs of the VaVAM policy on one scene, "
        "zero injected planner delay, CATK traffic.",
        "runs": {name: ROOT / "diag" / name for name in names},
        "labels": {name: label for name in names},
        "truth": set(),
        "cause": None,
    }


CASES = {
    "A_context_length_1": case_nominal,
    "B_delay_not_applied": case_latency,
    "C_missing_metrics": case_missing,
    "D_clean_control": case_control,
    "E_context_length_1_alone": case_nominal_alone,
    "F_context_length_1_with_reference": case_nominal_with_reference,
}


def score(case: dict, report: dict) -> dict:
    flagged = set(report["flags"])
    truth = case["truth"]
    caught = flagged & truth
    named = {
        name
        for name in caught
        if case["cause"] and case["cause"] in report["flags"][name].lower()
    }
    return {
        "runs": len(case["runs"]),
        "invalid": len(truth),
        "flagged": len(flagged),
        "caught": len(caught),
        "false_flags": len(flagged - truth),
        "missed": len(truth - flagged),
        "cause_named": len(named),
    }


def main() -> int:
    only = set(sys.argv[1:]) or set(CASES)
    results = json.loads(OUTPUT.read_text()) if OUTPUT.is_file() else {}
    for seed, (name, build) in enumerate(CASES.items()):
        if name not in only:
            continue
        case = build()
        report = audit(case["claim"], case["runs"], case["labels"], MODEL, seed=seed)
        scores = score(case, report)
        results[name] = {"scores": scores, "truth": sorted(case["truth"]), **report}
        print(name, scores, flush=True)
    lines = ["case\truns\tinvalid\tflagged\tcaught\tfalse_flags\tmissed\tcause_named"]
    for name, result in results.items():
        lines.append(
            "\t".join([name, *(str(value) for value in result["scores"].values())])
        )
    lines.append(f"model\t{MODEL}")
    OUTPUT.write_text(json.dumps(results, indent=1) + "\n")
    TABLE.write_text("\n".join(lines) + "\n")
    print(TABLE.read_text())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
