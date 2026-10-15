"""Confirmed hardest cases against runs spent, per search method.

For each arm the method table compares (analyze_methods), the number of
settings the study's goal counts as confirmed after each kept run; a
replicate that met its goal and stopped stays at k. Plotted per method as
the median over replicates with the range between the lowest and highest.
Writes figures/discovery_<study>.png and discovery.json.

    uv run python research/harness/discovery_curve.py
"""

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from analyze_methods import curve, replicate_rows
from compare_proposers import COLORS
from read_state import ROOT
from study import plan_runs

STUDIES = ("pedestrian_ego_speed", "cut_in_merge", "lead_vehicle",
           "pedestrian_ego_speed_2hz", "cut_in_merge_2hz", "lead_vehicle_2hz", "lane_keeping")
METHODS = ("rules", "hybrid", "llm", "random_confirm", "optuna_confirm", "hybrid_optuna")
V2 = ("llm_v2", "hybrid_v2")
LABEL = {"rules": "rules", "hybrid": "hybrid (rules + AI)", "llm": "AI picks",
         "random_confirm": "random + repeat", "optuna_confirm": "Optuna + repeat",
         "hybrid_optuna": "Optuna + AI", "llm_v2": "AI picks v2", "hybrid_v2": "hybrid v2"}
NAMES = {"pedestrian_ego_speed": "Pedestrian", "cut_in_merge": "Car cutting in",
         "lead_vehicle": "Car ahead braking", "lane_keeping": "Lane keeping"}
FIGURES = ROOT / "research" / "figures"


def study_curves(study: str) -> dict:
    """Each method's curves over the arms the method table compares
    (analyze_methods.replicate_rows), filled to the budget."""
    plan = json.loads((ROOT / "research" / "studies" / study / "plan.json").read_text())["plan"]
    reps, _ = replicate_rows(ROOT / "research" / "studies" / study, plan)
    k, budget = plan["goal"]["k"], plan_runs(plan)
    return {m: [curve(r, k, budget) for r in reps[m]] for m in METHODS + V2 if m in reps}


def plot(study: str, curves: dict, target: Path) -> None:
    fig, ax = plt.subplots(figsize=(9, 4.5))
    for method in METHODS + V2:
        runs = [c for c in curves.get(method, []) if c]
        if not runs:
            continue
        n = max(len(c) for c in runs)
        grid = np.array(runs, dtype=float)
        x = np.arange(1, n + 1)
        colour = COLORS.get(method, "0.4")
        ax.fill_between(x, grid.min(axis=0), grid.max(axis=0), color=colour, alpha=0.15, lw=0)
        ax.plot(x, np.median(grid, axis=0), color=colour, lw=2.2,
                label=f"{LABEL[method]} ({len(runs)})")
    base = study.removesuffix("_2hz")
    ax.set_title(f"{NAMES[base]}{', 2 Hz' if study.endswith('_2hz') else ''}", loc="left")
    ax.set_xlabel("kept runs so far")
    ax.set_ylabel("hardest cases confirmed")
    ax.set_ylim(-0.1, 5.3)
    ax.grid(alpha=0.3)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(fontsize=9, frameon=False, loc="upper left", bbox_to_anchor=(1.01, 1),
              title="median; band = lowest to\nhighest repeat (n)", title_fontsize=8)
    fig.tight_layout()
    fig.savefig(target, dpi=200)
    plt.close(fig)


def main() -> int:
    every = {}
    for study in STUDIES:
        curves = study_curves(study)
        every[study] = curves
        plot(study, curves, FIGURES / f"discovery_{study}.png")
        print(study, {m: [c[-1] if c else 0 for c in v] for m, v in curves.items()}, flush=True)
    (ROOT / "research" / "discovery.json").write_text(json.dumps(every) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
