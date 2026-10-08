"""The whole framework as two nested loops. Writes research/figures/framework.pdf
and .png.

The outer loop turns a question into the hardest cases: a plan, then rounds of
proposed runs, each round ending in a goal check. Every run of a round goes
through the inner loop (Fig. architecture.png in detail), which keeps it only
if the gate passes it. Trusted parts (plain code) are blue; the model's
proposals are orange; the same palette as plot_architecture.py.

    uv run python research/harness/plot_framework.py
"""

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

sys.path.insert(0, str(Path(__file__).resolve().parent))

from plot_architecture import PERSON, TRUSTED, UNTRUSTED, arrow, node
from plot_results import SURFACE, TEXT, TEXT_SECONDARY, _save

W, H = 1.32, 0.46


def band(ax, x, y, w, h, title):
    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.02,rounding_size=0.08",
            facecolor="none",
            edgecolor=TEXT_SECONDARY,
            linewidth=0.6,
            linestyle=(0, (3, 2)),
        )
    )
    ax.text(x + 0.06, y + h - 0.1, title, fontsize=6.4, color=TEXT_SECONDARY, va="top")


def main() -> int:
    fig, ax = plt.subplots(figsize=(7.0, 3.3), facecolor=SURFACE)
    ax.set_xlim(0, 10.6)
    ax.set_ylim(0, 4.9)
    ax.set_axis_off()

    # Outer loop: from a question to the hardest cases.
    band(ax, 0.05, 2.55, 10.5, 2.3, "outer loop: search for the hardest cases")
    top, mid = 4.1, 3.15
    node(ax, 0.8, top, 1.2, H, "brief\n(a question)", PERSON)
    node(ax, 2.35, top, W, H, "Planner\nproposes a plan", UNTRUSTED)
    node(
        ax, 3.95, top, W + 0.12, H, "plan check: knobs,\nscenes, budget, goal", TRUSTED
    )
    node(ax, 5.6, top, W + 0.1, H, "Proposer: rules,\nClaude or baseline", UNTRUSTED)
    node(ax, 7.25, top, W, H, "knob check\n+ rule fence", TRUSTED)
    node(ax, 8.95, top, 1.5, H, "round of runs\n(scene, knob values)", TRUSTED)
    node(ax, 1.55, mid, 1.6, H, "goal check: k cases\nconfirmed by repeats", TRUSTED)
    node(ax, 3.6, mid, W, H, "Triage\nwhy each crash", UNTRUSTED)
    node(ax, 5.25, mid, W, H, "report\ncounts by code", TRUSTED)
    arrow(ax, (1.4, top), (1.69, top))
    arrow(ax, (3.01, top), (3.23, top))
    arrow(ax, (4.67, top), (4.89, top))
    arrow(ax, (6.31, top), (6.59, top))
    arrow(ax, (7.91, top), (8.2, top))
    arrow(
        ax,
        (2.35, mid + 0.23),
        (5.2, top - 0.23),
        rad=0.08,
    )
    arrow(ax, (2.35, mid), (2.94, mid), "met", (0.0, 0.09))
    arrow(ax, (4.26, mid), (4.59, mid))

    # Inner loop: one run, kept only if the gate passes it (right to left).
    band(
        ax,
        0.05,
        0.05,
        10.5,
        2.3,
        "inner loop: one run, kept only if the gate passes it",
    )
    low, high = 0.62, 1.62
    node(ax, 8.95, high, 1.5, H, "READY\nK\u207b preflight", TRUSTED)
    node(ax, 6.85, high, 1.6, H, "RUNNING\nAlpaSim closed loop", TRUSTED)
    node(
        ax,
        4.6,
        high,
        2.0,
        H + 0.1,
        "K\u207a postflight: config landed,\nknob verified from the log,\nphysics, Rulebook",
        TRUSTED,
        size=6.0,
    )
    node(
        ax,
        2.0,
        high,
        1.9,
        H,
        "kept, with its outcome\n(the policy's failures only)",
        TRUSTED,
    )
    node(ax, 4.6, low, 1.5, H, "FAILED\nstatus", TRUSTED)
    node(ax, 6.85, low, 1.6, H, "Investigator\npicks from a menu", UNTRUSTED)
    node(ax, 8.95, low, 1.5, H, "validator, then\nrecover or HALT", TRUSTED)
    arrow(ax, (8.2, high), (7.65, high))
    arrow(ax, (6.05, high), (5.6, high))
    arrow(ax, (3.6, high), (2.95, high), "pass", (0.0, 0.09))
    arrow(ax, (4.6, high - 0.28), (4.6, low + 0.23), "fail", (0.15, 0.0))
    arrow(ax, (5.35, low), (6.05, low))
    arrow(ax, (7.65, low), (8.2, low))
    arrow(ax, (8.95, low + 0.23), (8.95, high - 0.23), "retry", (0.25, 0.0))

    # The loops meet: every run goes down; kept outcomes come back up.
    arrow(ax, (8.95, top - 0.23), (8.95, high + 0.23), "every run", (0.42, 0.55))
    arrow(
        ax,
        (1.55, high + 0.23),
        (1.55, mid - 0.23),
    )

    for x, y, label in ((3.2, 3.66, "not met: next round"), (1.65, 2.45, "kept outcomes")):
        ax.text(
            x, y, label, fontsize=5.4, color=TEXT_SECONDARY, style="italic", va="center"
        )
    ax.text(10.5, 0.13, "blue: plain code    orange: the model proposes    grey: a person",
            fontsize=6, color=TEXT_SECONDARY, ha="right", va="bottom")  # fmt: skip
    fig.tight_layout(pad=0.2)
    _save(fig, "framework")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
