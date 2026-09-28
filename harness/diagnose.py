"""FAILED -> choose one recovery skill, by the hand-written policy or by Claude.

Both policies get the same structured status and answer on the same menu.
The answer is written to the entry for validate_diagnosis.py. Nothing runs here.

The model policy is one headless `claude -p` call:
- the system prompt is advisor/CLAUDE.md and nothing else is loaded: the call
  runs in an empty temporary directory with no setting sources, so no project
  CLAUDE.md, settings, hooks, or memory reach it;
- it has no tools, so it cannot read logs or files. Its whole context is the
  status below;
- --json-schema forces {skill, params}. There is no free-text answer;
- --no-session-persistence: the next failure is a new call with a fresh context.
A failed call is recorded as skill None, which validate_diagnosis.py rejects.
There is no fallback to the script.

    uv run python research/harness/diagnose.py <entry.json> --policy script|model
"""

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from policy import decide_recovery
from postflight import PostflightStatus
from read_state import (
    MAX_ATTEMPTS,
    State,
    console_log,
    load_entry,
    read_state,
    save_entry,
)
from skills import Skill

CONTRACT = Path(__file__).resolve().parent / "advisor" / "CLAUDE.md"
PROMPT = "Status of the failed run is on stdin. Return one skill and its params."
SCHEMA = {
    "type": "object",
    "properties": {
        "skill": {"type": "string", "enum": [skill.value for skill in Skill]},
        "params": {
            "type": "object",
            "properties": {
                "context_length": {"type": "integer"},
                "planner_delay_us": {"type": "integer"},
                "scene_file": {"type": "string"},
            },
        },
    },
    "required": ["skill", "params"],
    "additionalProperties": False,
}
ERROR_PATTERN = re.compile(
    r"Error|error=|Exception|out of memory|Killed|exited with code [1-9]|FAILED"
)
ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
MAX_ERROR_LINES = 15
MAX_LINE_CHARS = 240


def error_lines(log: Path) -> list[str]:
    """First distinct error lines of the console log, container prefix removed.

    Lines that differ only in numbers (timestamps, sizes, ids) count once.
    """
    if not log.is_file():
        return []
    lines: list[str] = []
    keys: set[str] = set()
    for raw in log.read_text(encoding="utf-8", errors="replace").splitlines():
        if not ERROR_PATTERN.search(raw):
            continue
        line = ANSI.sub("", raw).split(" | ", 1)[-1].strip()[:MAX_LINE_CHARS]
        key = re.sub(r"[0-9a-f]{6,}|\d+", "N", line)
        if key in keys:
            continue
        keys.add(key)
        lines.append(line)
        if len(lines) == MAX_ERROR_LINES:
            break
    return lines


def failure_status(entry: dict, k_status: str) -> dict:
    """The structured K⁺ status both policies see."""
    return {
        "state": State.FAILED.value,
        "run": entry["name"],
        "k_status": k_status,
        "config": entry["config"],
        "attempt": entry["attempt"],
        "max_attempts": MAX_ATTEMPTS,
        "error_lines": error_lines(console_log(entry)),
    }


def script_diagnosis(status: dict) -> dict:
    """decide_recovery on the same status. CONFIGURE sets the value preflight requires."""
    k_status = status["k_status"]
    if k_status.startswith("preflight_rejected"):
        decision = decide_recovery(k_status, None, status["attempt"])
        params = {"context_length": 8} if "context_length" in k_status else {}
    else:
        failed = PostflightStatus(success=False, error=k_status)
        decision = decide_recovery(None, failed, status["attempt"])
        params = {}
    return {"skill": decision.skill.value, "params": params}


def model_diagnosis(status: dict, model: str) -> dict:
    cmd = [
        "claude",
        "-p",
        PROMPT,
        "--model",
        model,
        "--tools",
        "",
        "--setting-sources",
        "",
        "--no-session-persistence",
        "--system-prompt-file",
        str(CONTRACT),
        "--output-format",
        "json",
        "--json-schema",
        json.dumps(SCHEMA),
    ]
    with tempfile.TemporaryDirectory() as empty:
        proc = subprocess.run(
            cmd,
            input=json.dumps(status, indent=2),
            cwd=empty,
            capture_output=True,
            text=True,
            timeout=300,
            check=False,
        )
    if proc.returncode != 0:
        return {"skill": None, "params": {}, "error": proc.stderr.strip()[-500:]}
    out = json.loads(proc.stdout)
    answer = out.get("structured_output")
    if out["is_error"] or answer is None:
        return {"skill": None, "params": {}, "error": str(out.get("result"))[:500]}
    return {
        "skill": answer["skill"],
        "params": answer["params"],
        "model": ",".join(out["modelUsage"]),
        "context_tokens": out["usage"]["input_tokens"]
        + out["usage"]["cache_creation_input_tokens"]
        + out["usage"]["cache_read_input_tokens"],
        "output_tokens": out["usage"]["output_tokens"],
        "duration_ms": out["duration_ms"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("entry", type=Path)
    parser.add_argument("--policy", choices=("script", "model"), required=True)
    parser.add_argument("--model", default="claude-opus-5-5")
    args = parser.parse_args()

    entry = load_entry(args.entry)
    state = read_state(entry)
    if state.state is not State.FAILED:
        raise SystemExit(f"{entry['name']} is {state.state.value}, not FAILED")

    status = failure_status(entry, state.k_status)
    if args.policy == "script":
        diagnosis = script_diagnosis(status)
    else:
        diagnosis = model_diagnosis(status, args.model)
    entry["diagnosis"] = {"policy": args.policy, "input": status, **diagnosis}
    save_entry(args.entry, entry)
    print(json.dumps({"policy": args.policy, **diagnosis}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
