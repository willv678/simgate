"""Counted failures against an actor the retiming holds still.

AlpaSim's actor retiming (src/runtime/alpasim_runtime/actor_retiming.py)
extends a retimed track over the whole rollout by holding its first pose
before its new start and its last pose after its new end. A car sped up or
shifted earlier therefore stops dead where its recording ends, and one
shifted later waits motionless where its recording begins. This finds, for
each counted failure of the actor-retiming studies, whether the road user
the ego met (the nearest at the failure) was held:

- held at its end: its pose does not change from before the failure to the
  end of the run, and it moved at more than STOP_FROM_MPS just before (an
  instant stop no car can make);
- held at its start: its pose does not change from the start of the run to
  after the failure.

Then rescores every replicated method arm with those contacts not counted:
how many of the goal's k hardest settings each arm confirmed, before and
after. Writes held_actors.json and held_rescore.json.

    uv run python research/harness/held_actors.py
"""

import asyncio
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import outer
from analyze_methods import replicate_rows
from case_card import _nearest, _tracks, kept, moment
from compare_proposers import arms
from goals import challenging
from physics import _read, completed_rollout
from read_state import ROOT

STUDIES = ("cut_in_merge", "lead_vehicle", "cut_in_merge_2hz", "lead_vehicle_2hz")
STOP_FROM_MPS = 2.0
SAME_M = 1e-3


def held(track: dict, when: float) -> str | None:
    times = sorted(track)
    xy = np.array([track[t][:2] for t in times])
    moved = np.hypot(*np.diff(xy, axis=0).T) > SAME_M
    if not moved.any():
        return None
    first_move, last_move = int(np.argmax(moved)), len(moved) - 1 - int(np.argmax(moved[::-1]))
    end_hold, start_hold = times[last_move + 1], times[first_move]
    if when >= end_hold and last_move + 1 < len(times) - 1:
        dt = (times[last_move + 1] - times[last_move]) / 1e6
        speed = np.hypot(*(xy[last_move + 1] - xy[last_move])) / dt
        if speed > STOP_FROM_MPS:
            return "held at its end"
    if when <= start_hold and first_move > 0:
        return "held at its start"
    return None


def confirmed(rows: list[dict], varied: tuple, goal: dict) -> int:
    return min(goal["k"], len(challenging(outer.results(rows, varied), goal)))


def rescore(held_runs: set[str]) -> dict:
    found = {}
    for study in STUDIES:
        folder = ROOT / "research" / "studies" / study
        plan = json.loads((folder / "plan.json").read_text(encoding="utf-8"))["plan"]
        varied = tuple(plan["vary"])
        replicates, _ = replicate_rows(folder, plan)
        folders = arms(folder)
        found[study] = {}
        for method, rows in replicates.items():
            before, after = [], []
            for row in rows:
                past = [r for r in outer.history(folders[row["arm"]] / "queue", varied)
                        if r["verdict"] == "kept"]
                before.append(confirmed(past, varied, plan["goal"]))
                past = [{**r, "failed": False} if r["run"] in held_runs else r for r in past]
                after.append(confirmed(past, varied, plan["goal"]))
            found[study][method] = {"before": before, "without held-actor failures": after}
    return found


def main() -> int:
    found, rows = {}, []
    for study in STUDIES:
        counts = Counter()
        for run in kept(study):
            if not run["failed"]:
                continue
            what, when, handoff = moment(run["run_dir"])
            if what != "at-fault contact":
                counts["left the road"] += 1
                continue
            raw = asyncio.run(_read(completed_rollout(run["run_dir"]) / "rollout.asl"))
            actors = _tracks(raw)
            key, when = _nearest(raw, actors, when, handoff)
            state = held(actors[key], when) if key else None
            counts[state or "moving or truly stopped"] += 1
            rows.append({"study": study, "run": run["run"], "arm": run["arm"],
                         "scene": run["scene_id"], "actor": key, "held": state,
                         "setting": {k: run[k] for k in ("actor_time_shift_s", "actor_speed_scale",
                                                         "ego_speed_scale", "planner_delay_us") if k in run}})
        found[study] = dict(counts)
        print(study, dict(counts), flush=True)
    (ROOT / "research" / "held_actors.json").write_text(
        json.dumps({"counts": found, "runs": rows}, indent=1) + "\n")
    rescored = rescore({row["run"] for row in rows if row["held"]})
    (ROOT / "research" / "held_rescore.json").write_text(json.dumps(rescored, indent=1) + "\n")
    for study, methods in rescored.items():
        for method, counts in methods.items():
            print(study, method, counts, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
