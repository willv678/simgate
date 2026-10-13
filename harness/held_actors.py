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

Writes held_actors.json.

    uv run python research/harness/held_actors.py
"""

import asyncio
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from case_card import _nearest, _tracks, kept, moment
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
