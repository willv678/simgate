"""Loop 1. Python owns the `while`. Each state dispatches named scripts.

    READY    -> run_experiment.py
    RUNNING  -> monitor.py
    COMPLETE -> analyze.py, archive.py
    FAILED   -> diagnose.py, validate_diagnosis.py, recover.py (only if accepted)
    DONE     -> nothing

Claude runs only inside `diagnose.py --policy model`: one headless call per
FAILED run, then that process exits. One run is in flight at a time.
The loop ends when every entry is DONE, or, with --no-launch, when the only
entries left are READY. With --audit, a batch that was not stopped is then
audited (audit.py): flagged runs are quarantined. It stops early when an environment failure survives
CLEANUP_ENV or is halted, because the machine is shared and every later run
would fail. Each dispatched script is one trace line.

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

from read_state import ROOT, RunState, State, load_entry, queue_entries, read_state

HARNESS = Path(__file__).resolve().parent
DISPATCH = {
    State.READY: ("run_experiment.py",),
    State.RUNNING: ("monitor.py",),
    State.COMPLETE: ("analyze.py", "archive.py"),
    State.FAILED: ("diagnose.py", "validate_diagnosis.py", "recover.py"),
}


# Scripts that only read state, or append a result once: running one again
# after a crash does the same work. monitor.py aborted in native code once in
# about 300 calls and stopped the C2 tier 1 arm.
RERUNNABLE = ("monitor.py", "analyze.py")


class ScriptCrash(Exception):
    def __init__(self, script: str, entry_path: Path, returncode: int, stderr: str):
        super().__init__(
            f"{script} {entry_path.name} exited {returncode}:\n{stderr.strip()[-2000:]}"
        )
        self.returncode = returncode


def rerun_after(script: str, crash: ScriptCrash) -> bool:
    """Rerun once only a rerunnable script that a signal killed. Errors stop."""
    return script in RERUNNABLE and crash.returncode < 0


def run_script(script: str, entry_path: Path, extra: list[str]) -> dict:
    cmd = [sys.executable, str(HARNESS / script), str(entry_path), *extra]
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise ScriptCrash(script, entry_path, proc.returncode, proc.stderr)
    return json.loads(proc.stdout.strip().splitlines()[-1])


def next_entry(queue: Path, no_launch: bool) -> tuple[Path, RunState] | None:
    for path in queue_entries(queue):
        state = read_state(load_entry(path))
        if state.state is State.DONE:
            continue
        if state.state is State.READY and no_launch:
            continue
        return path, state
    return None


def summary(queue: Path, minutes: float, stopped: str | None) -> dict:
    entries = [load_entry(path) for path in queue_entries(queue)]
    resolutions = [entry["resolution"] for entry in entries]
    return {
        "entries": len(entries),
        "accepted": resolutions.count("ACCEPT"),
        "recovered": sum(
            r in ("CONFIGURE", "RE-RUN", "RESTART_CLEANUP", "CLEANUP_ENV")
            for r in resolutions
        ),
        "env_cleanups": sum(entry["env_cleanups"] for entry in entries),
        "halted": resolutions.count("HALT"),
        "halted_by_gate": sum(
            entry["resolution"] == "HALT"
            and entry["diagnosis"]["verdict"].startswith("rejected")
            for entry in entries
        ),
        "unresolved": resolutions.count(None),
        "model_calls": sum(
            entry["diagnosis"] is not None
            and entry["diagnosis"]["policy"] in ("model", "agent")
            for entry in entries
        ),
        "minutes": round(minutes, 1),
        "stopped": stopped,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("queue", type=Path)
    parser.add_argument("--policy", choices=("script", "model", "agent"), required=True)
    parser.add_argument("--model", default="claude-opus-5-5")
    parser.add_argument("--timeout-min", type=float, default=30.0)
    parser.add_argument("--no-launch", action="store_true")
    parser.add_argument("--trace", type=Path, required=True)
    parser.add_argument(
        "--audit", action="store_true", help="audit the batch when it ends (audit.py)"
    )
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

        stopped = None
        while stopped is None and (found := next_entry(args.queue, args.no_launch)):
            path, state = found
            for script in DISPATCH[state.state]:
                try:
                    result = run_script(script, path, extra.get(script, []))
                except ScriptCrash as crash:
                    if not rerun_after(script, crash):
                        raise SystemExit(str(crash)) from crash
                    record(
                        path,
                        state,
                        script,
                        {"crashed": crash.returncode, "rerun": True},
                    )
                    try:
                        result = run_script(script, path, extra.get(script, []))
                    except ScriptCrash as again:
                        raise SystemExit(str(again)) from again
                record(path, state, script, result)
                if script == "validate_diagnosis.py" and not result["accepted"]:
                    break
            # The machine is shared: every later run would fail the same way.
            halted = load_entry(path)["resolution"] == "HALT"
            if halted and state.k_status.startswith("environment"):
                stopped = "environment failure halted for a person"
            if read_state(load_entry(path)) == state:
                raise SystemExit(
                    f"{path.name} is still {state.state.value}; the loop would spin"
                )

        for path in queue_entries(args.queue):
            state = read_state(load_entry(path))
            if state.state is State.READY:
                record(path, state, None, {"skipped": stopped or "--no-launch"})
        minutes = (time.time() - start) / 60
        trace.write(
            json.dumps({"summary": summary(args.queue, minutes, stopped)}) + "\n"
        )
        if stopped:
            print(f"stopped: {stopped}", flush=True)
        elif args.audit:
            proc = subprocess.run(
                [sys.executable, str(HARNESS / "audit.py"), str(args.queue)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=True,
            )
            result = json.loads(proc.stdout.strip().splitlines()[-1])
            trace.write(json.dumps({"audit": result}) + "\n")
            print(f"audit: {json.dumps(result)}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
