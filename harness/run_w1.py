"""W1: the state loop on runs that already exist. No simulator launch.

Adopts three cases from l8_trace.jsonl into a fresh queue:
- the context_length 1 config L8 did not launch;
- diag/l8_ctx8, wizard exit 1 and no metrics;
- diag/l8_rerun, wizard exit 0 and metrics.
The two launched runs get the exit code the L8 trace recorded, written where
run_experiment.py would have written it. Then loop.py runs with --no-launch,
once per policy, each on its own queue, so the READY runs that recovery
queues are traced but not launched.

    uv run python research/harness/run_w1.py
"""

import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from enqueue import add, new_entry
from outer_loop import load_rows
from read_state import ROOT, exit_file

HARNESS = Path(__file__).resolve().parent
L8 = HARNESS / "l8_trace.jsonl"
RUNS = {
    "w1_trace.jsonl": ("w1_queue", "script"),
    "w1_model_trace.jsonl": ("w1_model_queue", "model"),
}


def queue_config(l8_config: dict) -> dict:
    return {
        "context_length": l8_config["context_length"],
        "planner_delay_us": l8_config["request_delay"],
        "scene_file": l8_config["scene_file"],
    }


def adopt(queue: Path, rows: list[dict]) -> None:
    rejected = next(row for row in rows if row.get("launched") is False)
    add(
        queue,
        new_entry(
            "l8_ctx1", "diag/l8_ctx1", queue_config(rejected["params"]["config"])
        ),
    )

    launches = {
        row["params"]["run_dir"]: row["params"]["config"]
        for row in rows
        if row["skill"] == "LAUNCH"
    }
    for row in rows:
        if "wizard_exit_code" not in row:
            continue
        run_dir = row["params"]["run_dir"]
        entry = new_entry(Path(run_dir).name, run_dir, queue_config(launches[run_dir]))
        entry["launched"] = True
        exit_file(entry).write_text(f"{row['wizard_exit_code']}\n", encoding="utf-8")
        add(queue, entry)


def main() -> int:
    rows = load_rows((L8,))
    for trace_name, (queue_name, policy) in RUNS.items():
        queue = HARNESS / queue_name
        trace = HARNESS / trace_name
        if queue.exists():
            shutil.rmtree(queue)
        trace.unlink(missing_ok=True)
        adopt(queue, rows)
        subprocess.run(
            [
                sys.executable,
                str(HARNESS / "loop.py"),
                str(queue),
                "--policy",
                policy,
                "--no-launch",
                "--trace",
                str(trace),
            ],
            cwd=ROOT,
            check=True,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
