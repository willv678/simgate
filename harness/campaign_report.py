"""Campaigns C1 and C2: one table per question, from the queues on disk.

Each campaign ran one fault plan (50 runs: 5 per fault kind, 10 clean) under
the script, tier 1 (agent) and tier 0 (model). C1 had the physics bounds off,
C2 on. Outcomes are scored, not skill labels: whether a lineage ended in a
valid kept run, how many launches it cost, and whether a person had to step in.

- yield: planned runs that ended as valid data in the dataset after the audit;
- invalid kept: runs carrying a data-corrupting fault that stayed in the
  dataset with no gate (exit code 0), after the per-run gate, after the audit;
- per fault kind: recovered, halted, launches;
- physics on fresh runs: C2's live K⁺ physics failures on runs with no silent
  fault (false alarms), and C1's kept runs checked after the fact.

    uv run python research/harness/campaign_report.py
"""

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from physics import check, load_bounds
from read_state import ROOT, load_entry, queue_entries
from score_campaign import CORRUPTS_DATA, lineages, score

HARNESS = Path(__file__).resolve().parent
ARMS = ("script", "agent", "model")
NAMES = {"script": "script", "agent": "tier 1", "model": "tier 0"}
SILENT = {"rails", "kinematic"}
OUTPUT = HARNESS / "campaign_report.json"
TABLE = HARNESS / "campaign_report.txt"


def _summary(campaign: str, arm: str) -> dict:
    trace = HARNESS / f"{campaign}_{arm}_trace.jsonl"
    rows = [json.loads(line) for line in trace.read_text().splitlines() if line.strip()]
    summaries = [row["summary"] for row in rows if "summary" in row]
    minutes = sum(s["minutes"] for s in summaries)
    return {"complete": bool(summaries), "minutes": round(minutes, 1)}


def _tokens(entries: list[dict]) -> int:
    return sum(
        e["diagnosis"].get("context_tokens", 0)
        for e in entries
        if e["diagnosis"] is not None and e["diagnosis"]["policy"] != "script"
    )


def arm_report(campaign: str, arm: str) -> dict:
    queue = HARNESS / f"{campaign}_{arm}_queue"
    entries = [load_entry(path) for path in queue_entries(queue)]
    chains = lineages(queue)
    kind = lambda e: e["fault"]["kind"] if e["fault"] else "clean"  # noqa: E731

    valid_kept = invalid_after_gate = invalid_after_audit = 0
    for e in entries:
        if e["resolution"] != "ACCEPT":
            continue
        corrupt = e["fault"] is not None and e["fault"]["kind"] in CORRUPTS_DATA
        quarantined = "quarantine" in e
        invalid_after_gate += corrupt
        invalid_after_audit += corrupt and not quarantined
        valid_kept += not corrupt and not quarantined

    per_kind = defaultdict(lambda: {"lineages": 0, "recovered": 0, "halted": 0, "launches": 0})
    for chain in chains:
        row = per_kind[kind(chain[0])]
        row["lineages"] += 1
        last = chain[-1]
        row["recovered"] += last["resolution"] == "ACCEPT" and kind(last) not in CORRUPTS_DATA
        row["halted"] += last["resolution"] == "HALT"
        row["launches"] += sum(e["launched"] for e in chain)

    physics_failures = Counter()
    for e in entries:
        status = (e["diagnosis"] or {}).get("input", {}).get("k_status", "")
        if "physics:" in status:
            physics_failures["silent" if kind(e) in SILENT else "other"] += 1

    table = score(queue)
    return {
        "planned": len(chains),
        "launches": sum(e["launched"] for e in entries),
        "valid_kept": valid_kept,
        "invalid_kept_no_gate": sum(r["no_gate_invalid_kept"] for r in table.values()),
        "invalid_kept_gate": invalid_after_gate,
        "invalid_kept_audit": invalid_after_audit,
        "halts": sum(e["resolution"] == "HALT" for e in entries),
        "halted_by_gate": sum(
            e["resolution"] == "HALT"
            and e["diagnosis"] is not None
            and e["diagnosis"]["verdict"].startswith("rejected")
            for e in entries
        ),
        "model_calls": sum(
            e["diagnosis"] is not None and e["diagnosis"]["policy"] != "script"
            for e in entries
        ),
        "context_tokens": _tokens(entries),
        "physics_failures": dict(physics_failures),
        "per_kind": dict(per_kind),
        **_summary(campaign, arm),
    }


def physics_after_the_fact(campaign: str, arm: str, bounds: dict) -> dict:
    """The physics bounds on every run C1 kept: silent faults and clean runs."""
    caught = Counter()
    for path in queue_entries(HARNESS / f"{campaign}_{arm}_queue"):
        e = load_entry(path)
        if e["resolution"] != "ACCEPT":
            continue
        group = "silent" if e["fault"] and e["fault"]["kind"] in SILENT else "other"
        caught[(group, bool(check(ROOT / e["run_dir"], bounds)))] += 1
    return {
        "silent_caught": caught[("silent", True)],
        "silent": caught[("silent", True)] + caught[("silent", False)],
        "other_flagged": caught[("other", True)],
        "other": caught[("other", True)] + caught[("other", False)],
    }


def main() -> int:
    bounds = {**load_bounds(), "enabled": True}
    report = {}
    lines = [
        "arm\tplanned\tlaunches\tvalid kept\tinvalid kept: no gate / gate / gate+audit"
        "\thalts (by gate)\tmodel calls\tcontext tokens\tminutes\tcomplete"
    ]
    for campaign in ("c1", "c2"):
        for arm in ARMS:
            r = arm_report(campaign, arm)
            if campaign == "c1":
                r["physics_after_the_fact"] = physics_after_the_fact(campaign, arm, bounds)
            report[f"{campaign}_{arm}"] = r
            lines.append(
                f"{campaign} {NAMES[arm]}\t{r['planned']}\t{r['launches']}\t{r['valid_kept']}"
                f"\t{r['invalid_kept_no_gate']} / {r['invalid_kept_gate']} / {r['invalid_kept_audit']}"
                f"\t{r['halts']} ({r['halted_by_gate']})\t{r['model_calls']}\t{r['context_tokens']}"
                f"\t{r['minutes']}\t{r['complete']}"
            )
    lines.append("")
    lines.append("per fault kind, recovered/lineages (launches, halts), C1 then C2:")
    kinds = sorted({k for r in report.values() for k in r["per_kind"]})
    for k in kinds:
        cells = []
        for key, r in report.items():
            row = r["per_kind"].get(k)
            if row:
                cells.append(
                    f"{key}: {row['recovered']}/{row['lineages']} ({row['launches']}, {row['halted']})"
                )
        lines.append(f"{k}\t" + "\t".join(cells))
    lines.append("")
    lines.append("physics, fresh runs: C1 kept runs checked after the fact; C2 live failures")
    for key, r in report.items():
        if "physics_after_the_fact" in r:
            p = r["physics_after_the_fact"]
            lines.append(
                f"{key}\tsilent caught {p['silent_caught']}/{p['silent']}"
                f"\tother runs flagged {p['other_flagged']}/{p['other']}"
            )
        else:
            lines.append(f"{key}\tlive physics failures {r['physics_failures']}")
    OUTPUT.write_text(json.dumps(report, indent=1) + "\n")
    TABLE.write_text("\n".join(lines) + "\n")
    print(TABLE.read_text())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
