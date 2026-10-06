"""Figure 1: SimGate's architecture. Writes research/figures/architecture.pdf and .png.

Trusted parts (plain code, checked) are blue; untrusted parts (the model) are
orange; a person is grey. Same palette as plot_results.py.

    uv run python research/harness/plot_architecture.py
"""

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

sys.path.insert(0, str(Path(__file__).resolve().parent))

from plot_results import SURFACE, TEXT, TEXT_SECONDARY, _save

TRUSTED = ("#e3eefb", "#2a78d6")
UNTRUSTED = ("#fde6dc", "#eb6834")
PERSON = ("#efeeea", "#7a7975")
ARROW = "#52514e"


def node(ax, x, y, w, h, text, style, size=6.6):
    face, edge = style
    ax.add_patch(
        FancyBboxPatch(
            (x - w / 2, y - h / 2),
            w,
            h,
            boxstyle="round,pad=0.01,rounding_size=0.06",
            facecolor=face,
            edgecolor=edge,
            linewidth=1.0,
        )
    )
    ax.text(
        x,
        y,
        text,
        ha="center",
        va="center",
        fontsize=size,
        color=TEXT,
        linespacing=1.15,
    )


def arrow(ax, start, end, label=None, offset=(0, 0.07), rad=0.0):
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=7,
            color=ARROW,
            linewidth=0.8,
            shrinkA=2,
            shrinkB=2,
            connectionstyle=f"arc3,rad={rad}",
        )
    )
    if label:
        mx = (start[0] + end[0]) / 2 + offset[0]
        my = (start[1] + end[1]) / 2 + offset[1]
        ax.text(
            mx,
            my,
            label,
            ha="center",
            va="center",
            fontsize=5.4,
            color=TEXT_SECONDARY,
            style="italic",
        )


def main() -> int:
    fig, ax = plt.subplots(figsize=(3.45, 3.0), facecolor=SURFACE)
    ax.set_facecolor(SURFACE)
    ax.set_xlim(0, 3.45)
    ax.set_ylim(0, 3.0)
    ax.axis("off")

    # Loop 1: one run.
    node(ax, 0.55, 2.62, 0.82, 0.32, "READY", TRUSTED)
    node(ax, 0.55, 2.02, 0.82, 0.38, "$K^-$ preflight\n+ machine check", TRUSTED)
    node(ax, 0.55, 1.42, 0.82, 0.32, "RUNNING\nsimulation", TRUSTED)
    node(
        ax,
        0.55,
        0.80,
        0.82,
        0.46,
        "$K^+$ postflight\nlanded · physics\n· Rulebook",
        TRUSTED,
    )
    node(ax, 0.55, 0.20, 0.82, 0.28, "kept (COMPLETE)", TRUSTED)
    arrow(ax, (0.55, 2.46), (0.55, 2.21))
    arrow(ax, (0.55, 1.83), (0.55, 1.58))
    arrow(ax, (0.55, 1.26), (0.55, 1.03))
    arrow(ax, (0.55, 0.57), (0.55, 0.34))

    # FAILED branch: the Investigator and the validator.
    node(ax, 1.72, 0.80, 0.70, 0.32, "FAILED\nstatus $c^+$", TRUSTED)
    node(
        ax,
        2.85,
        0.80,
        0.98,
        0.46,
        "Investigator\n(tier 1, read-only)\nproposes $\\hat u_k$",
        UNTRUSTED,
    )
    node(
        ax,
        2.85,
        1.55,
        0.98,
        0.46,
        "Validator\nmenu · budget\n· what is measured",
        TRUSTED,
        size=6.2,
    )
    node(ax, 1.72, 2.02, 0.70, 0.38, "recover $u_k$\nor HALT", TRUSTED)
    arrow(ax, (0.96, 0.80), (1.37, 0.80))
    arrow(ax, (2.07, 0.80), (2.36, 0.80))
    arrow(ax, (2.85, 1.03), (2.85, 1.34))
    arrow(ax, (2.36, 1.62), (2.07, 1.92))
    arrow(ax, (1.37, 2.20), (0.96, 2.55), label="new attempt", offset=(0.3, 0.12))

    # Loop 2: the Auditor and the Rulebook.
    node(ax, 1.72, 0.20, 0.70, 0.28, "Auditor\nflags · rules", UNTRUSTED, size=6.2)
    node(ax, 2.85, 0.20, 0.98, 0.28, "admission + person", PERSON, size=6.2)
    arrow(ax, (0.96, 0.20), (1.37, 0.20))
    arrow(ax, (2.07, 0.20), (2.36, 0.20))
    arrow(
        ax,
        (2.85, 0.34),
        (1.02, 0.66),
        label="Rulebook",
        offset=(-0.05, 0.06),
        rad=-0.15,
    )

    ax.text(
        0.02,
        2.93,
        "Trusted: plain code, checked by the Verifier",
        fontsize=5.6,
        color=TRUSTED[1],
        va="top",
    )
    ax.text(
        3.43,
        2.93,
        "Untrusted: the model proposes",
        fontsize=5.6,
        color=UNTRUSTED[1],
        va="top",
        ha="right",
    )
    fig.tight_layout(pad=0.1)
    _save(fig, "architecture")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
