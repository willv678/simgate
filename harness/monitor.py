"""RUNNING -> wait for the wizard to exit, or stop it at the timeout.

Polls read_state.py. Reads nothing from the console log. On timeout it first
records the machine (environment.machine_snapshot), then terminates the
launcher's process group and writes exit code 124, so the next read_state.py
call reports FAILED with that code and the diagnosis can still see what a
stopped run no longer shows.

    uv run python research/harness/monitor.py <entry.json> [--timeout-min 30]
"""

import argparse
import json
import os
import signal
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from environment import machine_snapshot
from read_state import State, exit_file, load_entry, read_state, timeout_machine_file

TIMEOUT_EXIT_CODE = 124


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("entry", type=Path)
    parser.add_argument("--timeout-min", type=float, default=30.0)
    parser.add_argument("--poll-s", type=float, default=30.0)
    args = parser.parse_args()

    entry = load_entry(args.entry)
    deadline = entry["launched_at"] + args.timeout_min * 60.0
    timed_out = False
    while read_state(entry).state is State.RUNNING:
        if time.time() > deadline:
            timeout_machine_file(entry).write_text(machine_snapshot(), encoding="utf-8")
            os.killpg(entry["pid"], signal.SIGTERM)
            exit_file(entry).write_text(f"{TIMEOUT_EXIT_CODE}\n", encoding="utf-8")
            timed_out = True
            break
        time.sleep(args.poll_s)

    waited_min = (time.time() - entry["launched_at"]) / 60.0
    print(json.dumps({"timed_out": timed_out, "minutes": round(waited_min, 1)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
