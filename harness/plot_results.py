"""Paper figures from results already on disk. Writes research/figures/*.pdf and .png.

1. invalid_kept: invalid runs left in the pilot's dataset with no gate, with
   the per-run gate, and after the tier 2 audit (c0_queue, score_campaign).
2. diagnosis: share of right recoveries per real failure for the script, tier 0
   and tier 1 (repeat_tiers.json).

Colors are the first three categorical slots of the reference palette,
validated for the light surface; every bar carries its value because the third
slot is below 3:1 contrast.

    uv run python research/harness/plot_results.py
"""

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))

from read_state import load_entry, queue_entries
from score_campaign import CORRUPTS_DATA, score

HARNESS = Path(__file__).resolve().parent
FIGURES = HARNESS.parent / "figures"
SURFACE = "#fcfcfb"
TEXT = "#0b0b0b"
TEXT_SECONDARY = "#52514e"
GRID = "#e4e3dd"
SERIES = {"script": "#2a78d6", "tier0": "#eb6834", "tier1": "#1baf7a"}
NAMES = {"script": "Script", "tier0": "Tier 0: no tools", "tier1": "Tier 1: tools"}


def _style(ax) -> None:
    ax.set_facecolor(SURFACE)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(TEXT_SECONDARY)
    ax.tick_params(colors=TEXT_SECONDARY, length=0, labelsize=8)
    ax.grid(axis="x", color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)


def _save(fig, name: str) -> None:
    FIGURES.mkdir(exist_ok=True)
    for suffix in ("pdf", "png"):
        fig.savefig(FIGURES / f"{name}.{suffix}", dpi=200, facecolor=SURFACE)
    plt.close(fig)


def invalid_kept() -> dict:
    queue = HARNESS / "c0_queue"
    table = score(queue)
    audited = [
        entry
        for entry in map(load_entry, queue_entries(queue))
        if entry["resolution"] == "ACCEPT"
        and entry["fault"] is not None
        and entry["fault"]["kind"] in CORRUPTS_DATA
        and "quarantine" not in entry
    ]
    counts = {
        "No gate\n(keep exit 0)": sum(
            row["no_gate_invalid_kept"] for row in table.values()
        ),
        "Per-run gate": sum(row["gate_invalid_kept"] for row in table.values()),
        "Gate + batch audit": len(audited),
    }
    fig, ax = plt.subplots(figsize=(3.4, 1.6), facecolor=SURFACE)
    _style(ax)
    labels = list(counts)[::-1]
    values = [counts[label] for label in labels]
    ax.barh(
        labels,
        values,
        height=0.55,
        color=SERIES["script"],
        edgecolor=SURFACE,
        linewidth=2,
    )
    for y, value in enumerate(values):
        ax.text(value + 0.15, y, str(value), va="center", fontsize=8, color=TEXT)
    ax.set_xlim(0, max(values) + 1.5)
    ax.set_xticks(range(0, max(values) + 1, 3))
    ax.set_xlabel(
        "Invalid runs kept (pilot, 17 launches)", fontsize=8, color=TEXT_SECONDARY
    )
    ax.tick_params(axis="y", labelcolor=TEXT)
    fig.tight_layout()
    _save(fig, "invalid_kept")
    return counts


def diagnosis() -> dict:
    results = json.loads((HARNESS / "repeat_tiers.json").read_text())
    cases = list(results)
    shares = {
        tier: [
            sum(results[c]["right"][tier]) / len(results[c]["right"][tier])
            for c in cases
        ]
        for tier in SERIES
    }
    fig, ax = plt.subplots(figsize=(3.4, 3.3), facecolor=SURFACE)
    _style(ax)
    height = 0.26
    for index, tier in enumerate(SERIES):
        # Inverted y axis: script on top of each group, in legend order.
        ys = [row + (index - 1) * height for row in range(len(cases))]
        ax.barh(
            ys,
            shares[tier],
            height=height,
            color=SERIES[tier],
            edgecolor=SURFACE,
            linewidth=1.5,
            label=NAMES[tier],
        )
        for y, share, case in zip(ys, shares[tier], cases):
            samples = len(results[case]["right"][tier])
            ax.text(
                share + 0.02,
                y,
                f"{round(share * samples)}/{samples}",
                va="center",
                fontsize=6,
                color=TEXT_SECONDARY,
            )
    labels = [
        c.replace("(l8_ctx8)", "").replace("(transient)", "†").strip() for c in cases
    ]
    ax.set_yticks(range(len(cases)), labels, fontsize=7, color=TEXT)
    ax.invert_yaxis()
    ax.set_xlim(0, 1.18)
    ax.set_xticks([0, 0.5, 1], ["0", "50%", "100%"])
    ax.set_xlabel(
        "Right recovery (replayed real failures)", fontsize=8, color=TEXT_SECONDARY
    )
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        fontsize=6.5,
        frameon=False,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.0),
        ncol=3,
        handlelength=1.2,
        columnspacing=1.0,
    )
    fig.text(
        0.02,
        0.01,
        "† replayed against the live machine. With the failure-time\n"
        "  snapshot, tier 1 chose RESTART_CLEANUP 3/3.",
        fontsize=5.5,
        color=TEXT_SECONDARY,
    )
    fig.tight_layout(rect=(0, 0.06, 1, 0.95))
    _save(fig, "diagnosis")
    return shares


def main() -> int:
    print(json.dumps({"invalid_kept": invalid_kept(), "diagnosis": diagnosis()}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
