"""loop.py end to end on a temporary queue, script policy, no launch."""

import json
import subprocess
import sys
from pathlib import Path

from enqueue import add
from read_state import load_entry

HARNESS = Path(__file__).resolve().parent


def _run_loop(queue: Path, trace: Path) -> list[dict]:
    subprocess.run(
        [
            sys.executable,
            str(HARNESS / "loop.py"),
            str(queue),
            "--policy",
            "script",
            "--no-launch",
            "--trace",
            str(trace),
        ],
        check=True,
        capture_output=True,
    )
    return [json.loads(line) for line in trace.read_text().splitlines()]


def _scripts(rows: list[dict], entry: str) -> list[tuple[str, str | None]]:
    return [(row["state"], row["script"]) for row in rows if row.get("entry") == entry]


def test_each_state_dispatches_its_scripts(tmp_path: Path, make_run):
    queue = tmp_path / "queue"
    add(queue, make_run("ctx1", context_length=1, launched=False))
    add(queue, make_run("no_metrics", exit_code=1, metrics=False))
    add(queue, make_run("clean"))
    add(queue, make_run("spent", exit_code=1, metrics=False, attempt=3))

    rows = _run_loop(queue, tmp_path / "trace.jsonl")

    recovery = [
        ("FAILED", "diagnose.py"),
        ("FAILED", "validate_diagnosis.py"),
        ("FAILED", "recover.py"),
    ]
    assert _scripts(rows, "001_ctx1.json") == recovery
    assert _scripts(rows, "002_no_metrics.json") == recovery
    assert _scripts(rows, "003_clean.json") == [
        ("COMPLETE", "analyze.py"),
        ("COMPLETE", "archive.py"),
    ]
    assert _scripts(rows, "004_spent.json") == recovery[:2]
    # Recovery queued two new runs. Neither is launched.
    assert _scripts(rows, "005_ctx1_a2.json") == [("READY", None)]
    assert _scripts(rows, "006_no_metrics_a2.json") == [("READY", None)]

    entries = {path.name: load_entry(path) for path in queue.glob("*.json")}
    assert entries["001_ctx1.json"]["resolution"] == "CONFIGURE"
    assert entries["005_ctx1_a2.json"]["config"]["context_length"] == 8
    assert entries["002_no_metrics.json"]["resolution"] == "RE-RUN"
    assert entries["003_clean.json"]["resolution"] == "ACCEPT"
    assert entries["004_spent.json"]["resolution"] == "HALT"

    results = (queue / "results.jsonl").read_text().splitlines()
    assert [json.loads(line)["name"] for line in results] == ["clean"]
    assert rows[-1]["summary"] | {"minutes": 0} == {
        "entries": 6,
        "accepted": 1,
        "recovered": 2,
        "halted": 1,
        "unresolved": 2,
        "model_calls": 0,
        "minutes": 0,
    }
