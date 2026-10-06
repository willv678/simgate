"""Outer-loop pilot: what each proposer's study ran, kept, and found.

For each study (o1 Claude, o2 random): runs proposed, dropped by the knob
check, launched, kept, not kept by the gate, and failures among kept runs; the
proposer's model cost; and a grid of kept runs and failures per scene and
delay, drawn as research/figures/pilot_grid.pdf and .png.

    uv run python research/harness/pilot_report.py
"""

import json
import sys
from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))

from knobs import DELAYS_US
from outer import history
from plot_results import SURFACE, TEXT, TEXT_SECONDARY, _save
from read_state import load_entry, queue_entries

HARNESS = Path(__file__).resolve().parent
STUDIES = {"o1": "Claude proposes", "o2": "random"}
VARIED = ("planner_delay_us",)
OUTPUT = HARNESS / "pilot_report.json"


def brackets(kept: list[dict]) -> dict:
    """Per scene that passed at some delay and failed at a larger one, where it
    breaks: the largest delay below which every kept run passed, and the
    smallest delay above it with a failure, in ms."""
    found = {}
    for scene in {r["scene_id"] for r in kept}:
        runs = sorted(
            (r["planner_delay_us"], r["failed"]) for r in kept if r["scene_id"] == scene
        )
        passed_up_to = None
        for delay, failed in runs:
            if failed:
                break
            passed_up_to = delay
        later = [
            d for d, f in runs if f and passed_up_to is not None and d > passed_up_to
        ]
        if passed_up_to is not None and later:
            found[scene[7:15]] = [passed_up_to // 1000, min(later) // 1000]
    return found


def study_report(study: str) -> dict:
    queue = HARNESS / f"{study}_queue"
    rounds = [
        json.loads(line)
        for line in (HARNESS / f"{study}_rounds.jsonl").read_text().splitlines()
    ]
    entries = [load_entry(path) for path in queue_entries(queue)]
    rows = history(queue, VARIED)
    kept = [row for row in rows if row["verdict"] == "kept"]
    grid = Counter()
    for row in kept:
        cell = (row["scene_id"], row["planner_delay_us"])
        grid[(*cell, "runs")] += 1
        grid[(*cell, "failed")] += row["failed"]
    calls = [r["call"] for r in rounds if r["call"]]
    return {
        "rounds": len(rounds),
        "proposed": sum(len(r["queued"]) + len(r["dropped"]) for r in rounds),
        "dropped": sum(len(r["dropped"]) for r in rounds),
        "launches": sum(e["launched"] for e in entries),
        "kept": len(kept),
        "not_kept": [row for row in rows if row["verdict"] != "kept"],
        "failed": sum(row["failed"] for row in kept),
        "settings": len({(r["scene_id"], r["planner_delay_us"]) for r in kept}),
        "scenes": len({r["scene_id"] for r in kept}),
        "brackets": brackets(kept),
        "proposer_tokens": sum(c["context_tokens"] + c["output_tokens"] for c in calls),
        "proposer_seconds": round(sum(c["duration_ms"] for c in calls) / 1000, 1),
        "plans": [r["plan"] for r in rounds],
        "grid": {f"{s[7:15]}@{d // 1000}ms:{k}": v for (s, d, k), v in grid.items()},
        "_cells": grid,
    }


def draw(reports: dict) -> None:
    scenes = sorted({key[0] for r in reports.values() for key in r["_cells"]})
    fig, axes = plt.subplots(
        1,
        len(reports),
        figsize=(6.8, 0.35 * len(scenes) + 1.0),
        facecolor=SURFACE,
        sharey=True,
        squeeze=False,
    )
    for ax, (study, report) in zip(axes[0], reports.items()):
        ax.set_facecolor(SURFACE)
        for y, scene in enumerate(scenes):
            for x, delay in enumerate(DELAYS_US):
                runs = report["_cells"][(scene, delay, "runs")]
                if not runs:
                    continue
                failed = report["_cells"][(scene, delay, "failed")]
                ax.scatter(
                    x,
                    y,
                    s=60 + 40 * runs,
                    color="#eb6834" if failed else "#2a78d6",
                    alpha=0.35 + 0.65 * failed / runs,
                    edgecolor=SURFACE,
                )
                ax.text(
                    x,
                    y,
                    f"{failed}/{runs}",
                    ha="center",
                    va="center",
                    fontsize=5.5,
                    color=TEXT,
                )
        ax.set_xticks(
            range(len(DELAYS_US)), [d // 1000 for d in DELAYS_US], fontsize=6.5
        )
        ax.set_yticks(range(len(scenes)), [s[7:15] for s in scenes], fontsize=6.5)
        ax.set_xlim(-0.6, len(DELAYS_US) - 0.4)
        ax.set_ylim(-0.6, len(scenes) - 0.4)
        ax.set_xlabel("planner delay (ms)", fontsize=7, color=TEXT_SECONDARY)
        ax.set_title(
            f"{STUDIES[study]}: {report['failed']} failures in {report['kept']} kept runs",
            fontsize=7.5,
            color=TEXT,
            loc="left",
        )
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
    fig.text(
        0.01,
        0.01,
        "Each cell: failed / kept runs at that scene and delay.",
        fontsize=6,
        color=TEXT_SECONDARY,
    )
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    _save(fig, "pilot_grid")


def main() -> int:
    reports = {
        study: study_report(study)
        for study in STUDIES
        if (HARNESS / f"{study}_rounds.jsonl").exists()
    }
    draw(reports)
    for report in reports.values():
        del report["_cells"]
    OUTPUT.write_text(json.dumps(reports, indent=1) + "\n")
    for study, r in reports.items():
        print(
            f"{study} ({STUDIES[study]}): {r['rounds']} rounds, {r['proposed']} proposed, "
            f"{r['dropped']} dropped, {r['launches']} launches, {r['kept']} kept, "
            f"{len(r['not_kept'])} not kept, {r['failed']} failed, {r['settings']} settings "
            f"on {r['scenes']} scenes, proposer {r['proposer_tokens']} tokens "
            f"{r['proposer_seconds']} s; breaks bracketed (ms): {r['brackets']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
