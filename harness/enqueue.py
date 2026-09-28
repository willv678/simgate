"""Add a READY run to a queue directory.

Entries are `<seq>_<name>.json`. The loop takes them in file-name order.

    uv run python research/harness/enqueue.py research/harness/queue b2_01 \
        --context-length 8 --planner-delay-us 0 --scene-file data/scenes/sim_scenes.csv
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from read_state import ROOT, load_entry, save_entry

RUN_ROOT = "diag"


def new_entry(
    name: str, run_dir: str, config: dict, attempt: int = 1, parent: str | None = None
) -> dict:
    return {
        "name": name,
        "run_dir": run_dir,
        "config": config,
        "attempt": attempt,
        "parent": parent,
        "launched": False,
        "pid": None,
        "launched_at": None,
        "resolution": None,
        "diagnosis": None,
    }


def add(queue: Path, entry: dict) -> Path:
    queue.mkdir(parents=True, exist_ok=True)
    if any(load_entry(path)["name"] == entry["name"] for path in queue.glob("*.json")):
        raise SystemExit(f"{entry['name']} is already in {queue}")
    seq = len(list(queue.glob("*.json"))) + 1
    path = queue / f"{seq:03d}_{entry['name']}.json"
    save_entry(path, entry)
    return path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("queue", type=Path)
    parser.add_argument("name")
    parser.add_argument("--context-length", type=int, required=True)
    parser.add_argument("--planner-delay-us", type=int, required=True)
    parser.add_argument("--scene-file", required=True)
    args = parser.parse_args()

    config = {
        "context_length": args.context_length,
        "planner_delay_us": args.planner_delay_us,
        "scene_file": args.scene_file,
    }
    path = add(args.queue, new_entry(args.name, f"{RUN_ROOT}/{args.name}", config))
    print(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
