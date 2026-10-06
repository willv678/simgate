"""RUNNING -> wait for the wizard to exit, or stop it at the timeout or a stall.

Polls read_state.py. Reads nothing from the console log. The runtime writes the
rollout log (rollout.asl) as the simulation runs, so with --stall-s a run whose
log stops growing mid-simulation is stopped early instead of at the timeout: a
frozen run used to hold the GPU for the whole timeout. Mid-simulation means the
newest rollout has no metrics.parquet yet; after that the log is finished and
the runtime is scoring and encoding video.

On a timeout or a stall it first records the machine
(environment.machine_snapshot; a stall heads it with the reason), then terminates the
launcher's process group and writes exit code 124, so the next read_state.py
call reports FAILED with that code and the diagnosis can still see what a
stopped run no longer shows.

    uv run python research/harness/monitor.py <entry.json> [--timeout-min 30] [--stall-s 120]
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
from read_state import (
    State,
    exit_file,
    load_entry,
    read_state,
    run_dir,
    timeout_machine_file,
)

TIMEOUT_EXIT_CODE = 124


def stalled_for(path: Path, now: float) -> float:
    """Seconds since the newest rollout log grew, while its simulation is still
    running; 0 before the first log exists and once the rollout is scored."""
    logs = sorted(
        path.glob("rollouts/*/*/rollout.asl"), key=lambda p: p.stat().st_mtime
    )
    if not logs or (logs[-1].parent / "metrics.parquet").exists():
        return 0.0
    return now - logs[-1].stat().st_mtime


def stop(entry: dict, reason: str | None) -> None:
    """A timeout records the machine alone; a stall heads it with the reason."""
    header = f"stopped: {reason}\n" if reason else ""
    timeout_machine_file(entry).write_text(
        header + machine_snapshot(), encoding="utf-8"
    )
    os.killpg(entry["pid"], signal.SIGTERM)
    exit_file(entry).write_text(f"{TIMEOUT_EXIT_CODE}\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("entry", type=Path)
    parser.add_argument("--timeout-min", type=float, default=30.0)
    parser.add_argument("--poll-s", type=float, default=30.0)
    parser.add_argument(
        "--stall-s",
        type=float,
        default=0.0,
        help="stop a run whose simulation log stops growing this long; 0 is off",
    )
    args = parser.parse_args()

    entry = load_entry(args.entry)
    deadline = entry["launched_at"] + args.timeout_min * 60.0
    timed_out = stalled = False
    while read_state(entry).state is State.RUNNING:
        now = time.time()
        if now > deadline:
            stop(entry, None)
            timed_out = True
            break
        idle = stalled_for(run_dir(entry), now)
        if args.stall_s and idle > args.stall_s:
            stop(entry, f"the simulation log stopped growing {idle:.0f} s ago")
            stalled = True
            break
        time.sleep(args.poll_s)

    waited_min = (time.time() - entry["launched_at"]) / 60.0
    print(
        json.dumps(
            {
                "timed_out": timed_out,
                "stalled": stalled,
                "minutes": round(waited_min, 1),
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
