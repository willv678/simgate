"""The plan-age check on three runs: research/figures/plan_age.pdf and .png.

The age of the plan the controller got, at every step after the warm-up
(physics.py). A clean run is at 0; a 200 ms delay run sits at 200 ms; a frozen
plan climbs step by step and resets.

    uv run python research/harness/plot_plan_age.py
"""

import sys
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))

from plot_results import SERIES, SURFACE, TEXT, TEXT_SECONDARY, _save, _style
from read_state import ROOT

from physics import signals

RUNS = {
    "clean, 0 ms delay (b2_091)": ("diag/b2_091", SERIES["script"]),
    "clean, 200 ms delay": ("diag/batch_7_delay_200ms", SERIES["tier1"]),
    "frozen plan, 0 ms delay (g2_002)": ("diag/g2_002", SERIES["tier0"]),
}


def main() -> int:
    fig, ax = plt.subplots(figsize=(3.4, 2.5), facecolor=SURFACE)
    _style(ax)
    for label, (run, color) in RUNS.items():
        ages = signals(ROOT / run)["plan_age_ms"]
        steps = np.arange(len(ages)) * 0.1
        ax.step(steps, ages, where="post", color=color, label=label, linewidth=1.2)
    ax.set_xlabel("time after the warm-up (s)", fontsize=7, color=TEXT_SECONDARY)
    ax.set_ylabel("age of the plan (ms)", fontsize=7, color=TEXT_SECONDARY)
    ax.tick_params(labelsize=6.5)
    ax.legend(
        fontsize=6,
        frameon=False,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.25),
        ncol=2,
    )
    ax.set_title(
        "The plan the controller got: as old as the delay",
        fontsize=7.5,
        color=TEXT,
        loc="left",
    )
    fig.tight_layout(pad=0.3)
    _save(fig, "plan_age")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
