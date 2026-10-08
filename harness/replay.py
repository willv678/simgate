"""Queue an exact re-run of a kept, seeded run: same config, seed included.

The re-run goes through the inner loop like any run, so the gate checks that
its seed landed and that its sessions were opened with it (read_state.py).
Whether it reproduces the original is for check_replay.py to say. A run without
a seed cannot be re-run exactly, so it is refused, as is a run the gate did not
keep.

    uv run python research/harness/replay.py <entry.json> <queue> [--name NAME]
"""

import argparse
import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from enqueue import RUN_ROOT, add, new_entry
from read_state import ROOT, load_entry, queue_entries, seed_request


def replay_entry(original: dict, queue: Path, name: str | None = None) -> dict:
    """A READY entry that re-runs `original` exactly, named `<name>_replay<k>`
    unless `name` is given. Raises SystemExit for a run that cannot be."""
    if seed_request(original["config"]) is None:
        raise SystemExit(f"{original['name']} has no seed: it cannot be re-run exactly")
    if original["resolution"] != "ACCEPT" or "quarantine" in original:
        raise SystemExit(f"{original['name']} was not kept by the gate")
    if name is None:
        replays = [
            path
            for path in queue_entries(queue)
            if load_entry(path).get("replay_of") == original["name"]
        ]
        name = f"{original['name']}_replay{len(replays) + 1}"
    entry = new_entry(name, f"{RUN_ROOT}/{name}", copy.deepcopy(original["config"]))
    entry["replay_of"] = original["name"]
    return entry


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("entry", type=Path, help="the kept run's queue entry")
    parser.add_argument("queue", type=Path, help="the queue to add the re-run to")
    parser.add_argument("--name", help="the re-run's name (default <run>_replay<k>)")
    args = parser.parse_args()
    entry = replay_entry(load_entry(args.entry), args.queue, args.name)
    path = add(args.queue, entry)
    print(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
