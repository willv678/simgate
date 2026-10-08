"""Compare the proposers that ran one study's plan: how fast each found what
the goal asked for.

A study's plan can be run by several proposers (study.py --proposer): llm in
the study folder, the others in <study>/<proposer>/. For each, replaying its
kept runs in launch order, the goal's progress after every run: for top_k the
number of challenging settings confirmed, for bracket the scenes settled. The
headline is runs to goal (None if the budget ran out first). Also: runs
launched, kept, failures, distinct scenes with a failure, proposals dropped by
the knob check or the rule fence, and the proposer's model cost. Writes
<study>/comparison.json and figures/compare_<study>.pdf/.png.

    uv run python research/harness/compare_proposers.py research/studies/pedestrian_crossing
"""

import argparse
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))

from goals import goal_status
from outer import history, results
from plot_results import SURFACE, TEXT, TEXT_SECONDARY, _save, _style
from read_state import load_entry, queue_entries

PROPOSERS = (
    "rules",
    "hybrid",
    "llm",
    "grid",
    "bisect",
    "random",
    "lhs",
    "optuna",
    "ga",
)
COLORS = {"rules": "#2a78d6", "hybrid": "#1baf7a", "llm": "#eb6834"}


def progress(
    goal: dict, kept: list[dict], varied: tuple, compare: dict | None
) -> list[int]:
    """The goal's count after each kept run, in launch order. `compare`: the
    controllers of an A/B study (its plan's fixed compare), or None."""
    counts = []
    for n in range(1, len(kept) + 1):
        status = goal_status(goal, results(kept[:n], varied, compare), varied)
        if goal["type"] == "top_k":
            counts.append(len(status["settings"]))
        elif goal["type"] == "bracket":
            counts.append(len(status["scenes"]))
        else:
            counts.append(int(status["met"]))
    return counts


def proposer_report(
    folder: Path, goal: dict | None, varied: tuple, compare: dict | None
) -> dict:
    queue = folder / "queue"
    entries = [load_entry(p) for p in queue_entries(queue)]
    rows = {r["run"]: r for r in history(queue, varied)}
    order = sorted(
        (e for e in entries if e["launched_at"] is not None),
        key=lambda e: e["launched_at"],
    )
    kept = [rows[e["name"]] for e in order if rows[e["name"]]["verdict"] == "kept"]
    rounds = [
        json.loads(line)
        for line in (folder / "rounds.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    calls = [r["call"] for r in rounds if r["call"]]
    counts = progress(goal, kept, varied, compare) if goal else []
    target = (
        goal["k"]
        if goal and goal["type"] == "top_k"
        else len(goal["scenes"])
        if goal and goal["type"] == "bracket"
        else 1
    )
    reached = next((i + 1 for i, c in enumerate(counts) if c >= target), None)
    return {
        "launched": len(order),
        "kept": len(kept),
        "failures": sum(r["failed"] for r in kept),
        "scenes_with_a_failure": len({r["scene_id"] for r in kept if r["failed"]}),
        "dropped": sum(len(r["dropped"]) for r in rounds),
        "runs_to_goal": reached,
        "goal_progress": counts,
        "model_seconds": round(sum(c["duration_ms"] for c in calls) / 1000, 1),
        "model_tokens": sum(c["context_tokens"] + c["output_tokens"] for c in calls),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("study", type=Path)
    args = parser.parse_args()
    plan = json.loads((args.study / "plan.json").read_text(encoding="utf-8"))["plan"]
    goal = None if plan["goal"]["type"] == "none" else plan["goal"]
    varied = tuple(plan["vary"])
    compare = plan["fixed"].get("compare")
    folders = {
        p: args.study if p == "llm" else args.study / p
        for p in PROPOSERS
        if ((args.study if p == "llm" else args.study / p) / "rounds.jsonl").exists()
    }
    report = {p: proposer_report(f, goal, varied, compare) for p, f in folders.items()}
    (args.study / "comparison.json").write_text(json.dumps(report, indent=1) + "\n")

    fig, ax = plt.subplots(figsize=(4.6, 2.8), facecolor=SURFACE)
    _style(ax)
    for proposer, r in report.items():
        ax.step(
            range(1, len(r["goal_progress"]) + 1),
            r["goal_progress"],
            where="post",
            color=COLORS.get(proposer, TEXT_SECONDARY),
            label=f"{proposer} (goal at {r['runs_to_goal'] or 'not reached'})",
            linewidth=1.6,
        )
    ax.set_xlabel("kept runs", fontsize=8, color=TEXT_SECONDARY)
    ax.set_ylabel(
        "challenging cases confirmed"
        if goal and goal["type"] == "top_k"
        else "goal progress",
        fontsize=8,
        color=TEXT_SECONDARY,
    )
    ax.set_title(
        f"{args.study.name}: who finds them faster", fontsize=9, color=TEXT, loc="left"
    )
    ax.legend(fontsize=7, frameon=False)
    fig.tight_layout()
    _save(fig, f"compare_{args.study.name}")
    for proposer, r in report.items():
        print(proposer, {k: v for k, v in r.items() if k != "goal_progress"})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
