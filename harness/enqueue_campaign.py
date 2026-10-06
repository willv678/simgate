"""Queue a fault-injection campaign: faulted runs and clean runs, shuffled.

Every kind in faults.KINDS gets `--per-kind` runs, and with `--plan-faults`
every kind in faults.PLAN_FAULTS too. drop_delay requests a
100 ms planner delay so that the missing override changes the result; it is
persistent, like a launcher bug that repeats on every retry. All other runs
request no delay. Scenes rotate through `--scene-ids`. The seed fixes the
order and the kill and hang times, so a campaign can be queued again exactly.

    uv run python research/harness/enqueue_campaign.py research/harness/c1_queue c1 \
        --per-kind 1 --clean 2
"""

import argparse
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from enqueue import RUN_ROOT, add, new_entry
from faults import KINDS, PLAN_FAULTS, new_fault

SCENE_FILE = "data/scenes/sim_scenes.csv"
L8_SCENE = "clipgt-01d503d4-449b-46fc-8d78-9085e70d3554"
DROPPED_DELAY_US = 100_000


def fault_for(kind: str, rng: random.Random, silent_persistent: bool) -> dict:
    """With silent_persistent, rails, kinematic and the plan faults repeat on a
    retry, as the config or planner bug that causes them would. C1 and C2 ran
    without it."""
    if kind == "kill":
        return new_fault(kind, after_s=rng.randint(60, 150))
    if kind == "hang":
        return new_fault(kind, after_s=rng.randint(60, 150))
    persistent = kind == "drop_delay" or (
        silent_persistent and (kind in ("rails", "kinematic") or kind in PLAN_FAULTS)
    )
    return new_fault(kind, persistent=persistent)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("queue", type=Path)
    parser.add_argument("prefix")
    parser.add_argument("--per-kind", type=int, required=True)
    parser.add_argument("--clean", type=int, required=True)
    parser.add_argument("--scene-ids", default=L8_SCENE)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--silent-persistent", action="store_true")
    parser.add_argument("--plan-faults", action="store_true")
    args = parser.parse_args()

    rng = random.Random(args.seed)
    kinds = KINDS + (tuple(PLAN_FAULTS) if args.plan_faults else ())
    plan = [kind for kind in kinds for _ in range(args.per_kind)]
    plan += [None] * args.clean
    rng.shuffle(plan)
    scenes = args.scene_ids.split(",")
    for index, kind in enumerate(plan, start=1):
        name = f"{args.prefix}_{index:03d}"
        config = {
            "context_length": 8,
            "planner_delay_us": DROPPED_DELAY_US if kind == "drop_delay" else 0,
            "scene_file": SCENE_FILE,
            "scene_id": scenes[(index - 1) % len(scenes)],
            "trafficsim_device": "cpu",
        }
        fault = None if kind is None else fault_for(kind, rng, args.silent_persistent)
        add(args.queue, new_entry(name, f"{RUN_ROOT}/{name}", config, fault=fault))
    print(f"queued {len(plan)} runs in {args.queue}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
