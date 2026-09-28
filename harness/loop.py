"""Loop 1. Python owns the `while`. Each state dispatches named scripts.

    READY    -> run_experiment.py
    RUNNING  -> monitor.py
    COMPLETE -> analyze.py, archive.py
    FAILED   -> diagnose.py, validate_diagnosis.py, recover.py (only if accepted)
    DONE     -> nothing

Claude runs only inside `diagnose.py --policy model`: one headless call per
FAILED run, then that process exits. One run is in flight at a time.
The loop ends when every entry is DONE, or, with --no-launch, when the only
entries left are READY. Each dispatched script is one trace line.

    uv run python research/harness/loop.py research/harness/queue --policy script
"""

import argparse
import json
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from read_state import ROOT, RunState, State, load_entry, read_state

HARNESS = Path(__file__).resolve().parent
DISPATCH = {
    State.READY: ("run_experiment.py",),
    State.RUNNING: ("monitor.py",),
    State.COMPLETE: ("analyze.py", "archive.py"),
    State.FAILED: ("diagnose.py", "validate_diagnosis.py", "recover.py"),
}


def run_script(script: str, entry_path: Path, extra: list[str]) -> dict:
    cmd = [sys.executable, str(HARNESS / script), str(entry_path), *extra]
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise SystemExit(
            f"{script} {entry_path.name} exited {proc.returncode}:\n{proc.stderr.strip()[-2000:]}"
        )
    return json.loads(proc.stdout.strip().splitlines()[-1])


def next_entry(queue: Path, no_launch: bool) -> tuple[Path, RunState] | None:
    for path in sorted(queue.glob("*.json")):
        state = read_state(load_entry(path))
        if state.state is State.DONE:
            continue
        if state.state is State.READY and no_launch:
            continue
        return path, state
    return None


def summary(queue: Path, minutes: float) -> dict:
    entries = [load_entry(path) for path in sorted(queue.glob("*.json"))]
    resolutions = [entry["resolution"] for entry in entries]
    return {
        "entries": len(entries),
        "accepted": resolutions.count("ACCEPT"),
        "recovered": sum(
            r in ("CONFIGURE", "RE-RUN", "RESTART_CLEANUP") for r in resolutions
        ),
        "halted": resolutions.count("HALT"),
        "unresolved": resolutions.count(None),
        "model_calls": sum(
            entry["diagnosis"] is not None and entry["diagnosis"]["policy"] == "model"
            for entry in entries
        ),
        "minutes": round(minutes, 1),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("queue", type=Path)
    parser.add_argument("--policy", choices=("script", "model"), required=True)
    parser.add_argument("--model", default="claude-opus-5-5")
    parser.add_argument("--timeout-min", type=float, default=30.0)
    parser.add_argument("--no-launch", action="store_true")
    parser.add_argument("--trace", type=Path, required=True)
    args = parser.parse_args()

    extra = {
        "monitor.py": ["--timeout-min", str(args.timeout_min)],
        "diagnose.py": ["--policy", args.policy, "--model", args.model],
    }
    start = time.time()
    with args.trace.open("a", encoding="utf-8") as trace:

        def record(
            path: Path, state: RunState, script: str | None, result: dict
        ) -> None:
            entry = load_entry(path)
            row = {
                "time": datetime.now(UTC).isoformat(timespec="seconds"),
                "entry": path.name,
                "run_dir": entry["run_dir"],
                "state": state.state.value,
                "k_status": state.k_status,
                "script": script,
                "result": result,
            }
            trace.write(json.dumps(row) + "\n")
            trace.flush()
            print(
                f"{path.name}: {state.state.value} -> {script} {json.dumps(result)}",
                flush=True,
            )

        while (found := next_entry(args.queue, args.no_launch)) is not None:
            path, state = found
            for script in DISPATCH[state.state]:
                result = run_script(script, path, extra.get(script, []))
                record(path, state, script, result)
                if script == "validate_diagnosis.py" and not result["accepted"]:
                    break
            if read_state(load_entry(path)) == state:
                raise SystemExit(
                    f"{path.name} is still {state.state.value}; the loop would spin"
                )

        for path in sorted(args.queue.glob("*.json")):
            state = read_state(load_entry(path))
            if state.state is State.READY:
                record(path, state, None, {"skipped": "--no-launch"})
        trace.write(
            json.dumps({"summary": summary(args.queue, (time.time() - start) / 60)})
            + "\n"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
