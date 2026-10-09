"""How fast each search method finds the hardest cases, over replicates.

For every study with a top_k goal and each proposer that ran it (every
replicate: compare_proposers.arms), from the kept runs in launch order:
runs to goal (the goal's k settings confirmed; the budget when not reached),
the cases confirmed at the end, the hardest-case score (compare_proposers.
hardest), failures found and the proposer's model time. Per study and
proposer the replicates are summarised by their median and range, and a
figure per study shows each proposer's mean discovery curve (confirmed cases
against kept runs, a replicate that stopped at its goal held at k after).
Writes research/METHODS.md, research/methods.json and
figures/methods_<study>.png/.pdf, figures/methods_overview.png/.pdf.

    uv run python research/harness/analyze_methods.py
"""

import json
import statistics
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))

from compare_proposers import COLORS, PROPOSERS, arms, proposer_of, proposer_report
from plot_results import SURFACE, TEXT, TEXT_SECONDARY, _save, _style
from read_state import ROOT
from study import plan_runs

STUDIES = ROOT / "research" / "studies"


def stopped_early(folder: Path, report: dict) -> bool:
    """An arm that stopped believing its goal met (its goal.json) where code
    now finds it unmet: it stopped under the broad failure definition used
    before 8 Oct 2026 (outer.FAILURE_METRICS) and did not spend its budget,
    so its runs to goal cannot be compared."""
    goal_file = folder / "goal.json"
    if not goal_file.exists():
        return False
    met = json.loads(goal_file.read_text(encoding="utf-8"))["met"]
    return met and report["runs_to_goal"] is None


def finished(folder: Path) -> bool:
    """A study arm is finished once its report was written after its last
    round (study.py writes the report when the outer loop ends)."""
    report = folder / "report.md"
    rounds = folder / "rounds.jsonl"
    return report.exists() and report.stat().st_mtime >= rounds.stat().st_mtime


def replicate_rows(study: Path, plan: dict) -> tuple[dict[str, list[dict]], list[str]]:
    """Each proposer's comparable replicates, each a proposer_report plus its
    arm name; and the arms left out because they stopped early."""
    goal = plan["goal"]
    found: dict[str, list[dict]] = {}
    left_out = []
    for arm, folder in arms(study).items():
        if not finished(folder):
            continue
        report = proposer_report(
            folder, goal, tuple(plan["vary"]), plan["fixed"].get("compare")
        )
        if stopped_early(folder, report):
            left_out.append(arm)
            continue
        found.setdefault(proposer_of(arm), []).append({"arm": arm, **report})
    return found, left_out


def curve(report: dict, k: int, budget: int) -> list[int]:
    """Confirmed cases after each kept run, up to the budget; a replicate that
    met its goal and stopped stays at k."""
    counts = report["goal_progress"]
    last = counts[-1] if counts else 0
    fill = k if report["runs_to_goal"] else last
    return (counts + [fill] * budget)[:budget]


def summary(reps: list[dict], k: int, budget: int) -> dict:
    to_goal = [r["runs_to_goal"] or budget for r in reps]
    return {
        "replicates": len(reps),
        "reached": sum(r["runs_to_goal"] is not None for r in reps),
        "runs_to_goal": to_goal,
        "median_runs_to_goal": statistics.median(to_goal),
        "confirmed": [
            min(r["goal_progress"][-1] if r["goal_progress"] else 0, k) for r in reps
        ],
        "hardest": [r["hardest"] for r in reps],
        "failures": [r["failures"] for r in reps],
        "kept": [r["kept"] for r in reps],
        "model_seconds": [r["model_seconds"] for r in reps],
    }


def main() -> int:
    results, excluded = {}, {}
    for study in sorted(p for p in STUDIES.iterdir() if (p / "plan.json").exists()):
        plan = json.loads((study / "plan.json").read_text(encoding="utf-8"))["plan"]
        if plan.get("goal", {}).get("type") != "top_k":
            continue
        reps, left_out = replicate_rows(study, plan)
        if left_out:
            excluded[study.name] = left_out
        if not reps:
            continue
        k, budget = plan["goal"]["k"], plan_runs(plan)
        results[study.name] = {
            "k": k,
            "budget": budget,
            "proposers": {p: summary(r, k, budget) for p, r in reps.items()},
        }

        fig, ax = plt.subplots(figsize=(4.6, 2.8), facecolor=SURFACE)
        _style(ax)
        for proposer in PROPOSERS:
            if proposer not in reps:
                continue
            curves = [curve(r, k, budget) for r in reps[proposer]]
            mean = [sum(c[i] for c in curves) / len(curves) for i in range(budget)]
            color = COLORS.get(proposer, TEXT_SECONDARY)
            for c in curves if len(curves) > 1 else []:
                ax.step(
                    range(1, budget + 1),
                    c,
                    where="post",
                    color=color,
                    alpha=0.2,
                    linewidth=0.8,
                )
            ax.step(
                range(1, budget + 1),
                mean,
                where="post",
                color=color,
                linewidth=1.8,
                label=f"{proposer} (n={len(curves)})",
            )
        ax.axhline(k, color=TEXT_SECONDARY, linewidth=0.6, linestyle=":")
        ax.set_xlabel("kept runs", fontsize=8, color=TEXT_SECONDARY)
        ax.set_ylabel("hardest cases confirmed", fontsize=8, color=TEXT_SECONDARY)
        ax.set_title(study.name, fontsize=9, color=TEXT, loc="left")
        ax.legend(fontsize=7, frameon=False)
        fig.tight_layout()
        _save(fig, f"methods_{study.name}")

    (ROOT / "research" / "methods.json").write_text(
        json.dumps(results, indent=1) + "\n"
    )

    names = list(results)
    proposers = [
        p for p in PROPOSERS if any(p in r["proposers"] for r in results.values())
    ]
    fig, ax = plt.subplots(figsize=(6.8, 3.0), facecolor=SURFACE)
    _style(ax)
    width = 0.8 / max(len(proposers), 1)
    for j, proposer in enumerate(proposers):
        for i, name in enumerate(names):
            s = results[name]["proposers"].get(proposer)
            if s is None:
                continue
            x = i + (j - (len(proposers) - 1) / 2) * width
            ax.bar(
                x,
                s["median_runs_to_goal"],
                width=width,
                color=COLORS.get(proposer, TEXT_SECONDARY),
                hatch=None if s["reached"] == s["replicates"] else "//",
                edgecolor=SURFACE,
                label=proposer
                if i
                == min(
                    n
                    for n, nm in enumerate(names)
                    if proposer in results[nm]["proposers"]
                )
                else None,
            )
            ax.scatter(
                [x] * len(s["runs_to_goal"]),
                s["runs_to_goal"],
                s=6,
                color=TEXT,
                zorder=3,
            )
    ax.set_xticks(range(len(names)), names, fontsize=7, color=TEXT, rotation=12)
    ax.set_ylabel(
        "kept runs to confirm k cases\n(median; dots: replicates; hatched: budget hit)",
        fontsize=7,
        color=TEXT_SECONDARY,
    )
    ax.legend(fontsize=7, frameon=False, ncol=2)
    fig.tight_layout()
    _save(fig, "methods_overview")

    lines = [
        "# How fast each search method finds the hardest cases",
        "",
        "Generated by `harness/analyze_methods.py` from the kept runs; every number",
        "is computed by code. Runs to goal: kept runs until the goal's k hardest",
        "settings were confirmed by repeats (the budget when it never was). Each",
        "replicate is an independent run of the same plan with its own seeds.",
        "Hardest: the mean criticality of the hardest setting found on each of the",
        "k most challenging scenes (1 = a crash), whether or not it was confirmed.",
        "",
        "| study | method | replicates | kept runs (each) | reached goal | runs to goal (each) | median | confirmed (each) | hardest (each) | failures (each) | model s (each) |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for name, r in results.items():
        for proposer, s in r["proposers"].items():
            lines.append(
                f"| {name} | {proposer} | {s['replicates']} "
                f"| {', '.join(map(str, s['kept']))} | {s['reached']} "
                f"| {', '.join(map(str, s['runs_to_goal']))} | {s['median_runs_to_goal']} "
                f"| {', '.join(map(str, s['confirmed']))} of {r['k']} "
                f"| {', '.join(map(str, s['hardest']))} "
                f"| {', '.join(map(str, s['failures']))} "
                f"| {', '.join(map(str, s['model_seconds']))} |"
            )
    out = [f"- {name}: {', '.join(arms)}" for name, arms in excluded.items()]
    if out:
        lines += [
            "",
            "Left out: arms that stopped believing their goal met under the broad",
            "failure definition used before 8 Oct 2026 (any front, side or off-road",
            "flag, warm-up and rear-ended collisions included), which code no longer",
            "finds met; they did not spend their budget, so their runs to goal",
            "cannot be compared.",
            "",
            *out,
        ]
    (ROOT / "research" / "METHODS.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
