"""Campaigns C1, C2 and C3: one table per question, from the queues on disk.

Each campaign ran one fault plan (50 runs: 5 per fault kind, 10 clean) under
the script, tier 1 (agent) and tier 0 (model). C1 had the physics bounds off,
C2 and C3 on; in C3 the silent faults (rails, kinematic) persist on a retry.
Arms whose queue does not exist yet are skipped. Outcomes are scored, not skill labels: whether a lineage ended in a
valid kept run, how many launches it cost, and whether a person had to step in.

- yield: planned runs that ended as valid data in the dataset after the audit;
- invalid kept: runs carrying a data-corrupting fault that stayed in the
  dataset with no gate (exit code 0), after the per-run gate, after the audit;
- per fault kind: recovered, halted, launches;
- physics on fresh runs: the live K⁺ physics failures in C2 and C3, and every
  kept run checked after the fact with the current bounds.

    uv run python research/harness/campaign_report.py
"""

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from read_state import ROOT, load_entry, queue_entries
from score_campaign import CORRUPTS_DATA, lineages, score

from physics import check, load_bounds

HARNESS = Path(__file__).resolve().parent
CAMPAIGNS = ("c1", "c2", "c3")
LIVE_PHYSICS = ("c2", "c3")
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
    kind = lambda e: e["fault"]["kind"] if e["fault"] else "clean"

    valid_kept = invalid_after_gate = invalid_after_audit = 0
    for e in entries:
        if e["resolution"] != "ACCEPT":
            continue
        corrupt = e["fault"] is not None and e["fault"]["kind"] in CORRUPTS_DATA
        quarantined = "quarantine" in e
        invalid_after_gate += corrupt
        invalid_after_audit += corrupt and not quarantined
        valid_kept += not corrupt and not quarantined

    per_kind = defaultdict(
        lambda: {"lineages": 0, "recovered": 0, "halted": 0, "launches": 0}
    )
    for chain in chains:
        row = per_kind[kind(chain[0])]
        row["lineages"] += 1
        last = chain[-1]
        row["recovered"] += (
            last["resolution"] == "ACCEPT" and kind(last) not in CORRUPTS_DATA
        )
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


def skills_chosen(campaigns: tuple, arm: str) -> dict:
    """First diagnosis of each faulted lineage: the skill chosen, per fault kind."""
    chosen = defaultdict(Counter)
    durations = []
    for campaign in campaigns:
        for chain in lineages(HARNESS / f"{campaign}_{arm}_queue"):
            first = next((e for e in chain if e["diagnosis"] is not None), None)
            if first is None or chain[0]["fault"] is None:
                continue
            chosen[chain[0]["fault"]["kind"]][str(first["diagnosis"]["skill"])] += 1
            if "duration_ms" in first["diagnosis"]:
                durations.append(first["diagnosis"]["duration_ms"] / 1000)
    return {
        "skills": {kind: dict(c) for kind, c in chosen.items()},
        "median_call_s": round(sorted(durations)[len(durations) // 2], 1)
        if durations
        else None,
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
    for campaign in CAMPAIGNS:
        for arm in ARMS:
            if not (HARNESS / f"{campaign}_{arm}_queue").is_dir():
                continue
            r = arm_report(campaign, arm)
            r["physics_after_the_fact"] = physics_after_the_fact(campaign, arm, bounds)
            report[f"{campaign}_{arm}"] = r
            lines.append(
                f"{campaign} {NAMES[arm]}\t{r['planned']}\t{r['launches']}\t{r['valid_kept']}"
                f"\t{r['invalid_kept_no_gate']} / {r['invalid_kept_gate']} / {r['invalid_kept_audit']}"
                f"\t{r['halts']} ({r['halted_by_gate']})\t{r['model_calls']}\t{r['context_tokens']}"
                f"\t{r['minutes']}\t{r['complete']}"
            )
    lines.append("")
    lines.append(
        "per fault kind, recovered/lineages (launches, halts), per campaign arm:"
    )
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
    lines.append(
        "physics, current bounds on every kept run after the fact (none of these"
        " runs set the plan-handoff bound); C2 and C3 also live"
    )
    for key, r in report.items():
        p = r["physics_after_the_fact"]
        live = (
            f"\tlive failures {r['physics_failures']}"
            if key.startswith(LIVE_PHYSICS)
            else ""
        )
        lines.append(
            f"{key}\tsilent caught {p['silent_caught']}/{p['silent']}"
            f"\tother runs flagged {p['other_flagged']}/{p['other']}{live}"
        )
    lines.append("")
    lines.append(
        "first skill chosen per fault kind, all campaigns together (median seconds per model call):"
    )
    choices = {
        arm: skills_chosen(tuple(c for c in CAMPAIGNS if f"{c}_{arm}" in report), arm)
        for arm in ARMS
    }
    for arm in ARMS:
        lines.append(f"{NAMES[arm]} (median call {choices[arm]['median_call_s']} s)")
        for kind, counts in sorted(choices[arm]["skills"].items()):
            lines.append(f"  {kind}\t{json.dumps(counts)}")
    report["skills_chosen"] = choices
    OUTPUT.write_text(json.dumps(report, indent=1) + "\n")
    TABLE.write_text("\n".join(lines) + "\n")
    print(TABLE.read_text())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
