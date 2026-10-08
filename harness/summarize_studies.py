"""Every study and every proposer that ran it, in one place.

For each study folder under research/studies with a plan, and each proposer
arm found in it (compare_proposers.PROPOSERS), the numbers the paper compares:
kept runs, failures, runs to goal, the challenging settings confirmed
(top_k goals) or scenes settled (bracket goals), and the model's cost. Writes
research/studies/SUMMARY.md, summary.json and index.html (links to each
study's page, if study_page.py made one), and figures/summary_runs_to_goal.

    uv run python research/harness/summarize_studies.py
"""

import html
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))

from compare_proposers import COLORS, PROPOSERS, proposer_report
from goals import goal_status
from outer import history, results
from plot_results import SURFACE, TEXT, TEXT_SECONDARY, _save, _style
from read_state import ROOT
from study import plan_runs

STUDIES = ROOT / "research" / "studies"


def arms(study: Path) -> dict[str, Path]:
    """Each proposer that ran this study's plan, and its folder."""
    found = {}
    for proposer in PROPOSERS:
        folder = study if proposer == "llm" else study / proposer
        if (folder / "rounds.jsonl").exists():
            found[proposer] = folder
    return found


def confirmed(folder: Path, plan: dict) -> list[str]:
    """What the goal found, in words: the challenging settings or the scenes
    settled, as code checks them now."""
    goal = plan["goal"]
    if goal["type"] == "none":
        return []
    varied = tuple(plan["vary"])
    compare = plan["fixed"].get("compare")
    table = results(history(folder / "queue", varied), varied, compare)
    status = goal_status(goal, table, varied)
    if goal["type"] == "top_k":
        by_id = {row["id"]: row for row in table}
        return [
            f"{by_id[i]['scene_id'][7:15]} at "
            + ", ".join(f"{k} {by_id[i][k]}" for k in varied)
            for i in status["settings"]
        ]
    if goal["type"] == "bracket":
        return [f"{scene[7:15]}: {where}" for scene, where in status["scenes"].items()]
    return [status["verdict"]]


def main() -> int:
    summary = {}
    for study in sorted(p for p in STUDIES.iterdir() if (p / "plan.json").exists()):
        plan = json.loads((study / "plan.json").read_text(encoding="utf-8"))["plan"]
        if "goal" not in plan:
            continue
        goal = None if plan["goal"]["type"] == "none" else plan["goal"]
        varied = tuple(plan["vary"])
        found = arms(study)
        if not found:
            continue
        summary[study.name] = {
            "question": plan["question"],
            "goal": plan["goal"],
            "budget": plan_runs(plan),
            "arms": {
                proposer: {
                    **{
                        k: v
                        for k, v in proposer_report(
                            folder, goal, varied, plan["fixed"].get("compare")
                        ).items()
                        if k != "goal_progress"
                    },
                    "found": confirmed(folder, plan),
                }
                for proposer, folder in found.items()
            },
        }
    (STUDIES / "summary.json").write_text(json.dumps(summary, indent=1) + "\n")

    lines = [
        "# Studies",
        "",
        "Every proposer that ran each study's plan, scored by code from the kept",
        "runs (`summarize_studies.py`). Runs to goal: kept runs until the goal",
        "was met, or not reached within the budget.",
        "",
        "| study | proposer | kept | failures | runs to goal | found | model s |",
        "|---|---|---|---|---|---|---|",
    ]
    for name, study in summary.items():
        for proposer, r in study["arms"].items():
            lines.append(
                f"| {name} | {proposer} | {r['kept']}/{study['budget']} | {r['failures']} "
                f"| {r['runs_to_goal'] or 'not reached'} | {len(r['found'])} "
                f"| {r['model_seconds']} |"
            )
    for name, study in summary.items():
        lines += ["", f"## {name}", "", study["question"], ""]
        for proposer, r in study["arms"].items():
            lines.append(
                f"- **{proposer}**: " + ("; ".join(r["found"]) or "nothing confirmed")
            )
    (STUDIES / "SUMMARY.md").write_text("\n".join(lines) + "\n")

    cards = []
    for name, study in summary.items():
        page = STUDIES / name / "index.html"
        link = (
            f'<a href="{name}/index.html">{html.escape(name)}</a>'
            if page.exists()
            else html.escape(name)
        )
        rows = "".join(
            f"<tr><td>{p}</td><td>{r['kept']}</td><td>{r['failures']}</td>"
            f"<td>{r['runs_to_goal'] or 'not reached'}</td><td>{len(r['found'])}</td></tr>"
            for p, r in study["arms"].items()
        )
        cards.append(
            f"<section><h2>{link}</h2><p>{html.escape(study['question'])}</p>"
            "<table><tr><th>proposer</th><th>kept runs</th><th>failures</th>"
            f"<th>runs to goal</th><th>found</th></tr>{rows}</table></section>"
        )
    (STUDIES / "index.html").write_text(
        "<!doctype html><html lang=en><meta charset=utf-8>"
        "<meta name=viewport content='width=device-width,initial-scale=1'>"
        "<title>SimGate studies</title><style>"
        ":root{--bg:#fbfaf7;--fg:#1f1e1c;--muted:#6b6a66;--line:#e4e3dd}"
        "@media (prefers-color-scheme:dark){:root{--bg:#1b1b1a;--fg:#eceae4;--muted:#a3a19b;--line:#3a3936}}"
        "body{background:var(--bg);color:var(--fg);font:16px/1.5 system-ui,sans-serif;"
        "max-width:960px;margin:0 auto;padding:16px}table{border-collapse:collapse;width:100%}"
        "td,th{border-bottom:1px solid var(--line);padding:4px 8px;text-align:left}"
        "p{color:var(--muted)}a{color:#2a78d6}</style>"
        "<h1>SimGate studies</h1><p>Each study answers a researcher's question; every proposer "
        "below ran the same plan, and every count is computed by code from runs that passed the "
        "gate.</p>" + "".join(cards) + "</html>\n"
    )

    fig, ax = plt.subplots(figsize=(6.4, 2.8), facecolor=SURFACE)
    _style(ax)
    names = list(summary)
    proposers = [p for p in PROPOSERS if any(p in s["arms"] for s in summary.values())]
    width = 0.8 / max(len(proposers), 1)
    for j, proposer in enumerate(proposers):
        for i, name in enumerate(names):
            r = summary[name]["arms"].get(proposer)
            if r is None:
                continue
            value = r["runs_to_goal"] or summary[name]["budget"]
            x = i + (j - (len(proposers) - 1) / 2) * width
            ax.bar(
                x,
                value,
                width=width,
                color=COLORS.get(proposer, TEXT_SECONDARY),
                hatch=None if r["runs_to_goal"] else "//",
                edgecolor=SURFACE,
                label=proposer if i == 0 else None,
            )
    ax.set_xticks(range(len(names)), names, fontsize=7, color=TEXT)
    ax.set_ylabel(
        "kept runs to goal (hatched: not reached)", fontsize=7, color=TEXT_SECONDARY
    )
    ax.legend(fontsize=7, frameon=False)
    fig.tight_layout()
    _save(fig, "summary_runs_to_goal")
    print((STUDIES / "SUMMARY.md").read_text())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
