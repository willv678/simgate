"""How many contacts the scorer does not count because the road user had
stopped dead (problem 31).

AlpaSim's actor retiming (src/runtime/alpasim_runtime/actor_retiming.py)
extends a retimed track over the whole rollout by holding its last pose after
its new end, so a car sped up or shifted earlier halts in one step where its
recording runs out. outer.outcome does not count a contact with such an actor
(`contact_with_held_actor`, physics.stopped_dead). This lists, per study that
retimes actors, the kept runs where that rule applied, with their settings.
Writes held_actors.json.

    uv run python research/harness/held_actors.py
"""

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from case_card import kept
from read_state import ROOT

STUDIES = ("cut_in_merge", "lead_vehicle", "cut_in_merge_2hz", "lead_vehicle_2hz")
KNOBS = ("actor_time_shift_s", "actor_speed_scale", "ego_speed_scale", "planner_delay_us")


def main() -> int:
    counts, rows = {}, []
    for study in STUDIES:
        tally = Counter()
        for run in kept(study):
            held = run["contact_with_held_actor"]
            tally["counted failure" if run["failed"] else "held actor" if held else "no failure"] += 1
            if held:
                rows.append({"study": study, "run": run["run"], "arm": run["arm"],
                             "scene": run["scene_id"],
                             "setting": {k: run[k] for k in KNOBS if k in run}})
        counts[study] = dict(tally)
        print(study, dict(tally), flush=True)
    (ROOT / "research" / "held_actors.json").write_text(
        json.dumps({"counts": counts, "runs": rows}, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
