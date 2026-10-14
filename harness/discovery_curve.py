"""Confirmed hardest cases against runs spent, per search method.

For each arm the method table compares (analyze_methods), the number of
settings the study's goal counts as confirmed after each kept run; a
replicate that met its goal and stopped stays at k. Plotted per method as
the median over replicates with the range between the lowest and highest.
Writes figures/discovery_<study>.png and discovery.json. For the studies
that retime cars, also figures/discovery_<study>_no_frozen.png: the same
curves with contacts against a car the retiming held still not counted
(held_actors.json, problem 31); an arm then stays at its last count.

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

import outer
from analyze_methods import curve, replicate_rows
from compare_proposers import COLORS, arms
from held_actors import STUDIES as RETIMED
from held_actors import confirmed
from read_state import ROOT
from study import plan_runs

STUDIES = ("pedestrian_ego_speed", "cut_in_merge", "lead_vehicle",
           "pedestrian_ego_speed_2hz", "cut_in_merge_2hz", "lead_vehicle_2hz")
METHODS = ("rules", "hybrid", "llm", "random_confirm", "optuna_confirm", "hybrid_optuna")
LABEL = {"rules": "rules", "hybrid": "hybrid (rules + AI)", "llm": "AI picks",
         "random_confirm": "random + repeat", "optuna_confirm": "Optuna + repeat",
         "hybrid_optuna": "Optuna + AI"}
NAMES = {"pedestrian_ego_speed": "Pedestrian", "cut_in_merge": "Car cutting in",
         "lead_vehicle": "Car ahead braking"}
FIGURES = ROOT / "research" / "figures"


def study_curves(study: str) -> dict:
    """Each method's curves over the arms the method table compares
    (analyze_methods.replicate_rows), filled to the budget."""
    plan = json.loads((ROOT / "research" / "studies" / study / "plan.json").read_text())["plan"]
    reps, _ = replicate_rows(ROOT / "research" / "studies" / study, plan)
    k, budget = plan["goal"]["k"], plan_runs(plan)
    return {m: [curve(r, k, budget) for r in reps[m]] for m in METHODS if m in reps}


def unfrozen_curves(study: str, held_runs: set[str]) -> dict:
    """study_curves with contacts against held actors not counted."""
    folder = ROOT / "research" / "studies" / study
    plan = json.loads((folder / "plan.json").read_text())["plan"]
    varied, goal, budget = tuple(plan["vary"]), plan["goal"], plan_runs(plan)
    reps, _ = replicate_rows(folder, plan)
    folders = arms(folder)
    found = {}
    for method in METHODS:
        for row in reps.get(method, []):
            past = [{**r, "failed": False} if r["run"] in held_runs else r
                    for r in outer.history(folders[row["arm"]] / "queue", varied)
                    if r["verdict"] == "kept"]
            counts = [confirmed(past[:n], varied, goal) for n in range(1, len(past) + 1)]
            found.setdefault(method, []).append(
                (counts + [counts[-1] if counts else 0] * budget)[:budget])
    return found


def plot(study: str, curves: dict, target: Path, note: str = "") -> None:
    fig, ax = plt.subplots(figsize=(7, 4.5))
    for method in METHODS:
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
    ax.set_title(f"{NAMES[base]}{', 2 Hz' if study.endswith('_2hz') else ''}{note}", loc="left")
    ax.set_xlabel("kept runs so far")
    ax.set_ylabel("hardest cases confirmed")
    ax.set_ylim(-0.1, 5.3)
    ax.grid(alpha=0.3)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(fontsize=9, frameon=False, loc="upper left",
              title="median; band = lowest to highest repeat (n)", title_fontsize=8)
    fig.tight_layout()
    fig.savefig(target, dpi=200)
    plt.close(fig)


def main() -> int:
    held = json.loads((ROOT / "research" / "held_actors.json").read_text())["runs"]
    held_runs = {row["run"] for row in held if row["held"]}
    every = {}
    for study in STUDIES:
        curves = study_curves(study)
        every[study] = curves
        plot(study, curves, FIGURES / f"discovery_{study}.png")
        print(study, {m: [c[-1] if c else 0 for c in v] for m, v in curves.items()}, flush=True)
        if study in RETIMED:
            curves = unfrozen_curves(study, held_runs)
            every[f"{study} (frozen cars not counted)"] = curves
            plot(study, curves, FIGURES / f"discovery_{study}_no_frozen.png",
                 note=": contacts with frozen cars not counted")
            print(study, "no frozen", {m: [c[-1] for c in v] for m, v in curves.items()}, flush=True)
    (ROOT / "research" / "discovery.json").write_text(json.dumps(every) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
