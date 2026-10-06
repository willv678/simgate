"""The outer loop's next config comes from ACCEPT rows only."""

import json
from pathlib import Path

from outer_loop import build_trace, next_config

REJECTED = {
    "skill": "CONFIGURE",
    "params": {
        "config": {
            "context_length": 1,
            "hydra_delay": 0,
            "request_delay": 0,
            "scene_file": "data/scenes/sim_scenes.csv",
        }
    },
    "k_status": "preflight_rejected: context_length must be 8, got 1",
    "launched": False,
}
FAILED = {
    "skill": "RE-RUN",
    "params": {"run_dir": "diag/l8_ctx8"},
    "k_status": "postflight_failed: metrics file not found (no metrics.parquet)",
}
KEPT = {
    "skill": "ACCEPT",
    "params": {"run_dir": "diag/l8_rerun"},
    "k_status": "postflight_success: at_fault=False, rear=False",
}


def test_rejected_run_is_not_the_next_config():
    chosen = next_config([REJECTED, FAILED, KEPT])
    assert chosen == {"run_dir": "diag/l8_rerun"}
    assert chosen != REJECTED["params"]["config"]
    assert chosen["run_dir"] != FAILED["params"]["run_dir"]


def test_trace_marks_rejected_rows_as_not_next():
    trace = build_trace([REJECTED, FAILED, KEPT])
    assert trace[-1]["becomes_next"] is True
    assert trace[-1]["next_config"]["run_dir"] == "diag/l8_rerun"
    rejected = trace[:-1]
    assert rejected
    assert all(row["becomes_next"] is False for row in rejected)
    assert "diag/l8_ctx8" in [row["identity"] for row in rejected]


def test_l10_trace_file_keeps_rejected_runs_out():
    path = Path(__file__).resolve().parent / "l10_trace.jsonl"
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    chosen = rows[-1]["next_config"]
    assert rows[-1]["becomes_next"] is True
    for row in rows[:-1]:
        assert row["becomes_next"] is False
        assert row["identity"] != chosen
        assert row["identity"] != chosen.get("run_dir")
