"""Admit an auditor-proposed rule into the gate only if the data backs it.

A proposal is admitted when all of these hold:
- it is a well-formed rule (rules.rule_problem);
- it does not pin an experiment variable to a constant. A variable is a label
  key that takes more than one value across the audited batch and the clean
  corpus (a delay sweep
  varies planner_delay_us). A rule on one must compare with the label
  (eq_label), or it would outlaw the sweep;
- it fires on at least one run the auditor flagged, so it catches what it was
  proposed for;
- it fires on no run of the clean corpus: runs that passed every check and
  were kept, each with the label its queue recorded.
Admitted rules are appended to the promoted set with their evidence.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from read_state import ROOT, load_entry
from rules import rule_problem, rules_file, violation

HARNESS = Path(__file__).resolve().parent
# Runs = (directory, label). The corpus is kept runs that no evaluation batch uses.
CLEAN_QUEUES = {
    "b2_queue": [f"b2_{index:03d}" for index in (9, 10, *range(92, 121))]
    + [f"b2_{index:03d}_a2" for index in range(1, 9)],
    "s1_smoke_queue": ["s1_smoke"],
    "demo_queue": ["demo_ctx1_a2"],
}
# B1 predates the queue. Its command requested context_length 8, delay 0, the L8 scene, CATK on CPU.
B1_LABEL = {
    "context_length": 8,
    "planner_delay_us": 0,
    "scene_file": "data/scenes/sim_scenes.csv",
    "scene_id": "clipgt-01d503d4-449b-46fc-8d78-9085e70d3554",
    "trafficsim_device": "cpu",
}


def clean_corpus() -> dict[str, tuple[Path, dict]]:
    corpus = {}
    for queue, names in CLEAN_QUEUES.items():
        entries = {
            entry["name"]: entry
            for entry in map(load_entry, (HARNESS / queue).glob("*.json"))
        }
        for name in names:
            entry = entries[name]
            if entry["resolution"] != "ACCEPT":
                raise SystemExit(f"{name} in the clean corpus was not kept")
            corpus[name] = (ROOT / entry["run_dir"], entry["config"])
    for index in range(1, 11):
        corpus[f"b1_{index:02d}"] = (ROOT / "diag" / f"b1_{index:02d}", B1_LABEL)
    return corpus


def admission(
    rule: dict,
    batch: dict[str, tuple[Path, dict]],
    flagged: set[str],
    clean: dict[str, tuple[Path, dict]],
) -> dict:
    """Whether to admit a rule proposed from `batch`, where the auditor flagged `flagged`."""
    problem = rule_problem(rule)
    if problem is not None:
        return {"admitted": False, "reason": problem}
    seen: dict[str, set[str]] = {}
    for _, label in [*batch.values(), *clean.values()]:
        for key, value in label.items():
            seen.setdefault(key, set()).add(json.dumps(value))
    pinned = rule["path"].split(".")[-1]
    if rule["op"] != "eq_label" and len(seen.get(pinned, ())) > 1:
        return {"admitted": False, "reason": f"pins experiment variable {pinned}"}
    caught = sorted(name for name in flagged if violation(rule, *batch[name]))
    if not caught:
        return {"admitted": False, "reason": "fires on none of the flagged runs"}
    false = sorted(
        name for name, (path, label) in clean.items() if violation(rule, path, label)
    )
    if false:
        return {
            "admitted": False,
            "reason": f"fires on {len(false)} clean runs",
            "clean_fired": false[:5],
        }
    return {
        "admitted": True,
        "caught": caught,
        "flagged": len(flagged),
        "clean_checked": len(clean),
    }


def promote(rule: dict, evidence: dict, source: str) -> None:
    path = rules_file()
    rules = json.loads(path.read_text(encoding="utf-8"))
    if any(existing["id"] == rule["id"] for existing in rules):
        return
    rules.append({**rule, "source": source, "evidence": evidence})
    path.write_text(json.dumps(rules, indent=1) + "\n", encoding="utf-8")
