"""Campaign figures from campaign_report.json. Writes research/figures/*.pdf and .png.

1. campaign_invalid: invalid runs kept in the dataset, summed over the three
   arms of each campaign, with no gate, the per-run gate, and gate plus audit.
   C1 ran with the physics bounds off, C2 with them on, C3 with them on and the
   silent faults persistent. A campaign appears once all three arms finished.
2. campaign_outcomes: C1 per policy, three small panels with one axis each:
   valid runs kept, launches spent, runs handed to a person.

Same validated palette as plot_results.py; every bar carries its value.

    uv run python research/harness/plot_campaign.py
"""

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))

from plot_results import SERIES, SURFACE, TEXT, TEXT_SECONDARY, _save, _style

HARNESS = Path(__file__).resolve().parent
REPORT = HARNESS / "campaign_report.json"
POLICIES = {"script": "Script", "model": "Tier 0", "agent": "Tier 1"}
CAMPAIGN_COLOR = {
    "c1": SERIES["script"],
    "c2": SERIES["tier1"],
    "c3": SERIES["tier0"],
    "c4": "#7a7975",
}
CAMPAIGN_NAME = {
    "c1": "C1: physics off",
    "c2": "C2: physics on",
    "c3": "C3: faults persist",
    "c4": "C4: plus plan faults",
}


def invalid(report: dict) -> dict:
    stages = {
        "No gate\n(keep exit 0)": "invalid_kept_no_gate",
        "Per-run gate": "invalid_kept_gate",
        "Gate + audit": "invalid_kept_audit",
    }
    finished = [
        c
        for c in CAMPAIGN_NAME
        if all(report.get(f"{c}_{p}", {}).get("complete") for p in POLICIES)
    ]
    totals = {
        c: {s: sum(report[f"{c}_{p}"][k] for p in POLICIES) for s, k in stages.items()}
        for c in finished
    }
    fig, ax = plt.subplots(
        figsize=(3.4, 2.0 + 0.3 * (len(finished) - 2)), facecolor=SURFACE
    )
    _style(ax)
    labels = list(stages)[::-1]
    height = 0.72 / len(finished)
    for index, campaign in enumerate(finished):
        offset = (len(finished) - 1) / 2 - index
        ys = [row + offset * height for row in range(len(labels))]
        values = [totals[campaign][label] for label in labels]
        ax.barh(
            ys,
            values,
            height=height,
            color=CAMPAIGN_COLOR[campaign],
            edgecolor=SURFACE,
            linewidth=1.5,
            label=CAMPAIGN_NAME[campaign],
        )
        for y, value in zip(ys, values):
            ax.text(value + 1, y, str(value), va="center", fontsize=7, color=TEXT)
    ax.set_yticks(range(len(labels)), labels, fontsize=8, color=TEXT)
    ax.set_xlim(0, max(max(t.values()) for t in totals.values()) * 1.15)
    ax.set_xlabel(
        "Invalid runs kept, summed over the 3 arms", fontsize=7.5, color=TEXT_SECONDARY
    )
    handles, names = ax.get_legend_handles_labels()
    fig.legend(
        handles,
        names,
        fontsize=6.5,
        frameon=False,
        loc="upper center",
        bbox_to_anchor=(0.55, 1.0),
        ncol=len(finished),
        handlelength=1.2,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.9))
    _save(fig, "campaign_invalid")
    return totals


def outcomes(report: dict) -> dict:
    panels = {
        "Valid runs kept": "valid_kept",
        "Launches spent": "launches",
        "Handed to a person": "halts",
    }
    colors = {
        "script": SERIES["script"],
        "model": SERIES["tier0"],
        "agent": SERIES["tier1"],
    }
    fig, axes = plt.subplots(1, 3, figsize=(6.8, 1.7), facecolor=SURFACE)
    values = {}
    for ax, (title, key) in zip(axes, panels.items()):
        _style(ax)
        ax.grid(axis="x", visible=False)
        ax.grid(axis="y", color="#e4e3dd", linewidth=0.6)
        row = [report[f"c1_{p}"][key] for p in POLICIES]
        values[title] = dict(zip(POLICIES.values(), row))
        bars = ax.bar(
            list(POLICIES.values()),
            row,
            width=0.6,
            color=[colors[p] for p in POLICIES],
            edgecolor=SURFACE,
            linewidth=1.5,
        )
        for bar, value in zip(bars, row):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                value,
                str(value),
                ha="center",
                va="bottom",
                fontsize=7,
                color=TEXT,
            )
        ax.set_title(title, fontsize=8, color=TEXT, loc="left")
        ax.set_ylim(0, max(row) * 1.2)
        ax.tick_params(axis="x", labelsize=7, labelcolor=TEXT)
    fig.text(
        0.01,
        0.01,
        "Campaign C1: one plan of 50 runs (40 with injected faults) per policy.",
        fontsize=6,
        color=TEXT_SECONDARY,
    )
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    _save(fig, "campaign_outcomes")
    return values


def main() -> int:
    report = json.loads(REPORT.read_text())
    print(json.dumps({"invalid": invalid(report), "outcomes": outcomes(report)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
