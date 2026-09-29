"""Does what the auditor learns become checks that work without it?

For each lie, the auditor audits a learning batch and proposes rules;
promote.admission admits a rule only if it fires on a run the auditor flagged
and on none of the clean corpus (promote.clean_corpus). The admitted rules
alone, with no model call, are then applied to held-out batches:

| lie | learning batch | held-out batch |
|---|---|---|
| context_length 1 | A (eval_auditor) | E: the uniform batch the auditor missed |
| delay not applied | B (eval_auditor) | B2 runs 121-140 labelled 150 ms, 141-150 labelled 0 |
| silent faults | x1_001-004 (rails, kinematic) and 10 B2 runs | x1_005 (rails), x1_006 (kinematic) |

Every admitted rule is also applied to D, 30 clean runs, for false positives.
The admitted rules are written to mining_rules.json, not to the gate: a person
copies them into rules/promoted.json. Writes mining_eval.json and .txt.

    uv run python research/harness/eval_mining.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from audit import audit
from eval_auditor import (
    MODEL,
    case_control,
    case_latency,
    case_nominal,
    case_nominal_alone,
)
from promote import admission, clean_corpus
from read_state import ROOT, load_entry
from rules import violations

HARNESS = Path(__file__).resolve().parent
OUTPUT = HARNESS / "mining_eval.json"
TABLE = HARNESS / "mining_eval.txt"
RULES_OUT = HARNESS / "mining_rules.json"


def _queued(queue: str, names: list[str]) -> dict[str, tuple[Path, dict]]:
    entries = {
        entry["name"]: entry
        for entry in map(load_entry, (HARNESS / queue).glob("*.json"))
    }
    return {
        name: (ROOT / entries[name]["run_dir"], entries[name]["config"])
        for name in names
    }


def _batch(case: dict) -> dict[str, tuple[Path, dict]]:
    return {name: (path, case["labels"][name]) for name, path in case["runs"].items()}


def case_silent_learn() -> dict:
    faulted = _queued("c0_queue", ["x1_001", "x1_002", "x1_003", "x1_004"])
    contrast = _queued("b2_queue", [f"b2_{index:03d}" for index in range(11, 21)])
    runs = {**faulted, **contrast}
    return {
        "claim": "Nominal closed-loop runs: VaVAM plans, the linear MPC tracks the "
        "plan, CATK traffic, zero injected delay, one scene.",
        "runs": {name: path for name, (path, _) in runs.items()},
        "labels": {name: label for name, (_, label) in runs.items()},
        "truth": set(faulted),
    }


def held_out_latency() -> tuple[dict, set[str]]:
    runs = _queued("b2_queue", [f"b2_{index:03d}" for index in range(121, 151)])
    batch = {}
    for index, (name, (path, label)) in enumerate(sorted(runs.items())):
        delay = 150_000 if index < 20 else 0
        batch[name] = (path, {**label, "planner_delay_us": delay})
    return batch, {name for name in sorted(batch)[:20]}


def held_out_silent() -> tuple[dict, set[str]]:
    batch = _queued("c0_queue", ["x1_005", "x1_006"])
    return batch, set(batch)


def apply(rules: list[dict], batch: dict, truth: set[str]) -> dict:
    fired = {
        name for name, (path, label) in batch.items() if violations(rules, path, label)
    }
    return {
        "runs": len(batch),
        "invalid": len(truth),
        "caught": len(fired & truth),
        "false_flags": len(fired - truth),
    }


def main() -> int:
    clean = clean_corpus()
    control = _batch(case_control())
    nominal_alone = case_nominal_alone()
    stages = {
        "context_length_1": (
            case_nominal(),
            (_batch(nominal_alone), nominal_alone["truth"]),
        ),
        "delay_not_applied": (case_latency(), held_out_latency()),
        "silent_faults": (case_silent_learn(), held_out_silent()),
    }
    results = {}
    lines = [
        "lie\taudit caught/invalid\taudit false\tproposed\tadmitted"
        "\theld-out caught/invalid\theld-out false\tclean-control false"
    ]
    for seed, (name, (learn, (held_batch, held_truth))) in enumerate(stages.items()):
        report = audit(learn["claim"], learn["runs"], learn["labels"], MODEL, seed=seed)
        batch = _batch(learn)
        flagged = set(report["flags"])
        decisions = [
            {"rule": rule, **admission(rule, batch, flagged, clean)}
            for rule in report["rules"]
        ]
        admitted = [d["rule"] for d in decisions if d["admitted"]]
        held = apply(admitted, held_batch, held_truth)
        false_on_control = apply(admitted, control, set())["false_flags"]
        results[name] = {
            "audit": {
                "flagged": sorted(flagged),
                "truth": sorted(learn["truth"]),
                "context_tokens": report["context_tokens"],
            },
            "decisions": decisions,
            "held_out": held,
            "control_false_flags": false_on_control,
        }
        lines.append(
            "\t".join(
                str(value)
                for value in (
                    name,
                    f"{len(flagged & learn['truth'])}/{len(learn['truth'])}",
                    len(flagged - learn["truth"]),
                    len(report["rules"]),
                    len(admitted),
                    f"{held['caught']}/{held['invalid']}",
                    held["false_flags"],
                    false_on_control,
                )
            )
        )
        print(lines[-1], flush=True)
    lines.append(f"model\t{MODEL}\tclean corpus\t{len(clean)} runs")
    admitted_all = [
        {
            **d["rule"],
            "source": f"eval_mining:{name}",
            "evidence": {key: d[key] for key in ("caught", "flagged", "clean_checked")},
        }
        for name, result in results.items()
        for d in result["decisions"]
        if d["admitted"]
    ]
    RULES_OUT.write_text(json.dumps(admitted_all, indent=1) + "\n")
    OUTPUT.write_text(json.dumps(results, indent=1) + "\n")
    TABLE.write_text("\n".join(lines) + "\n")
    print(TABLE.read_text())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
