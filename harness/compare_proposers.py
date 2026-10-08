"""Compare the proposers that ran one study's plan: how fast each found what
the goal asked for.

A study's plan can be run by several proposers (study.py --proposer): llm in
the study folder, the others in <study>/<proposer>/. For each, replaying its
kept runs in launch order, the goal's progress after every run: for top_k the
number of challenging settings confirmed, for bracket the scenes settled. The
headline is runs to goal (None if the budget ran out first). Also: runs
launched, kept, failures, distinct scenes with a failure, proposals dropped by
the knob check or the rule fence, and the proposer's model cost. When failures
are rare and no proposer reaches the goal, `hardest` still ranks them: after
every kept run, the mean criticality of the hardest setting found on each of
the k most challenging scenes (a scene not yet found counts 0; settings are
not confirmed, so this measures what a search turned up, not what it proved).
Writes
<study>/comparison.json and figures/compare_<study>.pdf/.png.

    uv run python research/harness/compare_proposers.py research/studies/pedestrian_crossing
"""

import argparse
import json
import re
import sys
from collections import defaultdict
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
    "random_confirm",
    "lhs",
    "optuna",
    "ga",
)
COLORS = {
    "rules": "#2a78d6",
    "hybrid": "#1baf7a",
    "llm": "#eb6834",
    "random_confirm": "#8a63d2",
    "random": "#8c8c8c",
    "optuna": "#c99a06",
    "grid": "#5f6b7a",
    "lhs": "#b0596b",
    "ga": "#3f8f8f",
}
REPLICATE = re.compile(r"_r(\d+)$")


def proposer_of(arm: str) -> str:
    """The proposer of an arm: "rules" for rules, rules_r2, rules_r3."""
    return REPLICATE.sub("", arm)


def arms(study: Path) -> dict[str, Path]:
    """Each arm that ran this study's plan, and its folder: one per proposer
    and replicate (the llm arm's first replicate is the study folder)."""
    found = {}
    for proposer in PROPOSERS:
        first = study if proposer == "llm" else study / proposer
        replicates = sorted(
            (int(REPLICATE.search(p.name).group(1)), p)
            for p in study.glob(f"{proposer}_r*")
            if REPLICATE.search(p.name) and proposer_of(p.name) == proposer
        )
        for name, folder in [(proposer, first)] + [
            (f"{proposer}_r{n}", p) for n, p in replicates
        ]:
            if (folder / "rounds.jsonl").exists():
                found[name] = folder
    return found


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


def hardest(kept: list[dict], varied: tuple, k: int) -> list[float]:
    """After each kept run, in launch order: the mean, over the k most
    challenging scenes, of the highest mean criticality of a setting found on
    that scene; scenes not yet found count 0."""
    curve = []
    cells = defaultdict(list)
    for row in kept:
        cells[(row["scene_id"], *(row[knob] for knob in varied))].append(
            row["criticality"]
        )
        best = defaultdict(float)
        for (scene, *_), values in cells.items():
            best[scene] = max(best[scene], sum(values) / len(values))
        top = sorted(best.values(), reverse=True)[:k]
        curve.append(round(sum(top) / k, 3))
    return curve


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
    curve = hardest(kept, varied, goal["k"] if goal and goal["type"] == "top_k" else 5)
    return {
        "launched": len(order),
        "kept": len(kept),
        "failures": sum(r["failed"] for r in kept),
        "scenes_with_a_failure": len({r["scene_id"] for r in kept if r["failed"]}),
        "dropped": sum(len(r["dropped"]) for r in rounds),
        "runs_to_goal": reached,
        "goal_progress": counts,
        "hardest": curve[-1] if curve else None,
        "hardest_progress": curve,
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
    folders = arms(args.study)
    report = {p: proposer_report(f, goal, varied, compare) for p, f in folders.items()}
    (args.study / "comparison.json").write_text(json.dumps(report, indent=1) + "\n")

    fig, (ax, hard) = plt.subplots(1, 2, figsize=(8.4, 2.8), facecolor=SURFACE)
    _style(ax)
    _style(hard)
    for proposer, r in report.items():
        hard.plot(
            range(1, len(r["hardest_progress"]) + 1),
            r["hardest_progress"],
            color=COLORS.get(proposer_of(proposer), TEXT_SECONDARY),
            label=f"{proposer} ({r['hardest']})",
            linewidth=1.6,
        )
    k = goal["k"] if goal and goal["type"] == "top_k" else 5
    hard.set_xlabel("kept runs", fontsize=8, color=TEXT_SECONDARY)
    hard.set_ylabel(
        f"criticality, {k} hardest scenes", fontsize=8, color=TEXT_SECONDARY
    )
    hard.set_ylim(0, 1)
    hard.set_title(
        "hardest cases found (1 = a crash)", fontsize=9, color=TEXT, loc="left"
    )
    hard.legend(fontsize=7, frameon=False)
    for proposer, r in report.items():
        ax.step(
            range(1, len(r["goal_progress"]) + 1),
            r["goal_progress"],
            where="post",
            color=COLORS.get(proposer_of(proposer), TEXT_SECONDARY),
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
        print(
            proposer,
            {
                key: v
                for key, v in r.items()
                if key not in ("goal_progress", "hardest_progress")
            },
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
