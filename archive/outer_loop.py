"""Outer loop. The next config is the latest ACCEPT row. Not a search.

Rows that preflight or postflight rejected are not read. The rule does not
score metrics or pick a new delay, scene, or gain.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TRACE = ROOT / "research" / "harness" / "l10_trace.jsonl"
SOURCES = (
    ROOT / "research" / "harness" / "l7_trace.jsonl",
    ROOT / "research" / "harness" / "l8_trace.jsonl",
)


def load_rows(paths: tuple[Path, ...]) -> list[dict]:
    rows: list[dict] = []
    for path in paths:
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
    return rows


def next_config(rows: list[dict]) -> dict | None:
    """Config from the latest ACCEPT row. Every other skill is ignored."""
    accepted = [row for row in rows if row.get("skill") == "ACCEPT"]
    if not accepted:
        return None
    params = accepted[-1].get("params") or {}
    config = params.get("config")
    if isinstance(config, dict):
        return dict(config)
    keys = ("context_length", "hydra_delay", "request_delay", "scene_file", "run_dir")
    return {key: params[key] for key in keys if key in params}


def _rejected(row: dict) -> bool:
    status = str(row.get("k_status") or "")
    if row.get("launched") is False:
        return True
    if row.get("skill") in {"RE-RUN", "RESTART_CLEANUP"}:
        return True
    return status.startswith("preflight_rejected") or status.startswith("postflight_failed")


def _identity(row: dict):
    params = row.get("params") or {}
    if isinstance(params.get("config"), dict):
        return params["config"]
    if "run_dir" in params:
        return params["run_dir"]
    return row.get("input")


def build_trace(rows: list[dict]) -> list[dict]:
    chosen = next_config(rows)
    trace = []
    for row in rows:
        if not _rejected(row):
            continue
        trace.append(
            {
                "skill": row.get("skill"),
                "identity": _identity(row),
                "becomes_next": False,
            }
        )
    trace.append(
        {
            "skill": "ACCEPT",
            "next_config": chosen,
            "becomes_next": True,
            "rule": "latest ACCEPT row",
        }
    )
    return trace


def main() -> int:
    rows = load_rows(SOURCES)
    trace = build_trace(rows)
    chosen = trace[-1]["next_config"]
    for row in trace[:-1]:
        if row["identity"] == chosen or row["identity"] == chosen.get("run_dir"):
            raise SystemExit(f"rejected run became next: {row['identity']}")
    TRACE.write_text(
        "".join(json.dumps(row) + "\n" for row in trace), encoding="utf-8"
    )
    print(json.dumps(chosen), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
