"""FAILED -> choose one recovery skill: the hand-written script, or Claude.

Every policy gets the same structured status and answers on the same menu.
The answer is written to the entry for validate_diagnosis.py. Nothing runs here.

Two Claude policies, each one headless `claude -p` call:
- model (tier 0): no tools. Its whole context is the status.
- agent (tier 1): may investigate first with read-only tools. It can Read,
  Grep and Glob inside its working directories only: a temporary directory
  holding a copy of the console log, and the failed run directory. Bash is
  limited to AGENT_BASH. `dontAsk` with no permission prompter denies
  everything else. Tool calls and denials are recorded. The machine as the
  shell tools see it is saved with every diagnosis, so a replay can show the
  agent the machine at failure time (./machine.txt) instead of the live one.
Both tiers share the rest:
- the system prompt is advisor/CLAUDE.md and nothing else is loaded: the call
  runs in a temporary directory with no setting sources, so no project
  CLAUDE.md, settings, hooks, or memory reach it;
- --json-schema forces {skill, params}. There is no free-text answer;
- --no-session-persistence: the next failure is a new call with a fresh context.
A failed call is recorded as skill None, which validate_diagnosis.py rejects.
There is no fallback to the script.

    uv run python research/harness/diagnose.py <entry.json> --policy script|model|agent
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from environment import machine_snapshot
from policy import decide_recovery
from postflight import PostflightStatus
from read_state import (
    MAX_ATTEMPTS,
    TRAFFICSIM_DEVICES,
    State,
    console_log,
    load_entry,
    read_state,
    run_dir,
    save_entry,
)
from skills import Skill

CONTRACT = Path(__file__).resolve().parent / "advisor" / "CLAUDE.md"
MODEL_PROMPT = "Status of the failed run is on stdin. Return one skill and its params."
AGENT_BASH = ("docker ps", "docker network ls", "nvidia-smi", "df")
AGENT_PROMPT = (
    "Status of the failed run is on stdin. Before you answer you may investigate "
    "with read-only tools. Read, Grep and Glob work on ./console.log (the wizard "
    "console log, present only if the run launched) and on the run directory "
    "{run_dir}. Bash is limited to: {bash}. Anything else is denied. "
    "Then return one skill and its params."
)
REPLAY_PROMPT = (
    "Status of the failed run is on stdin. This failure is being replayed: the "
    "machine as it was when the run failed is in ./machine.txt. Before you answer "
    "you may investigate with read-only tools. Read, Grep and Glob work on "
    "./machine.txt, ./console.log (present only if the run launched) and the run "
    "directory {run_dir}. Anything else is denied. Then return one skill and its params."
)
SCHEMA = {
    "type": "object",
    "properties": {
        "skill": {"type": "string", "enum": [skill.value for skill in Skill]},
        "params": {
            "type": "object",
            "properties": {
                "context_length": {"type": "integer"},
                "scene_file": {"type": "string"},
                "trafficsim_device": {
                    "type": "string",
                    "enum": list(TRAFFICSIM_DEVICES),
                },
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
    if k_status.startswith("environment"):
        return {"skill": Skill.CLEANUP_ENV.value, "params": {}}
    if k_status.startswith("preflight_rejected"):
        decision = decide_recovery(k_status, None, status["attempt"])
        params = {"context_length": 8} if "context_length" in k_status else {}
    else:
        failed = PostflightStatus(success=False, error=k_status)
        decision = decide_recovery(None, failed, status["attempt"])
        params = {}
    return {"skill": decision.skill.value, "params": params}


def _tool_call(block: dict) -> str:
    tool_input = block["input"]
    detail = next(
        (
            tool_input[key]
            for key in ("command", "file_path", "pattern")
            if key in tool_input
        ),
        json.dumps(tool_input),
    )
    return f"{block['name']}: {str(detail)[:200]}"


def _claude(
    prompt: str, status: dict, workdir: Path, extra: list[str], model: str
) -> dict:
    cmd = [
        "claude",
        "-p",
        prompt,
        "--model",
        model,
        *extra,
        "--setting-sources",
        "",
        "--no-session-persistence",
        "--system-prompt-file",
        str(CONTRACT),
        "--output-format",
        "stream-json",
        "--verbose",
        "--json-schema",
        json.dumps(SCHEMA),
    ]
    proc = subprocess.run(
        cmd,
        input=json.dumps(status, indent=2),
        cwd=workdir,
        capture_output=True,
        text=True,
        timeout=600,
        check=False,
    )
    messages = [json.loads(line) for line in proc.stdout.splitlines() if line.strip()]
    results = [message for message in messages if message["type"] == "result"]
    if proc.returncode != 0 or not results:
        return {"skill": None, "params": {}, "error": proc.stderr.strip()[-500:]}
    out = results[-1]
    answer = out.get("structured_output")
    if out["is_error"] or answer is None:
        return {"skill": None, "params": {}, "error": str(out.get("result"))[:500]}
    tool_calls = [
        _tool_call(block)
        for message in messages
        if message["type"] == "assistant"
        for block in message["message"]["content"]
        if block["type"] == "tool_use" and block["name"] != "StructuredOutput"
    ]
    return {
        "skill": answer["skill"],
        "params": answer["params"],
        "model": ",".join(out["modelUsage"]),
        "context_tokens": out["usage"]["input_tokens"]
        + out["usage"]["cache_creation_input_tokens"]
        + out["usage"]["cache_read_input_tokens"],
        "output_tokens": out["usage"]["output_tokens"],
        "duration_ms": out["duration_ms"],
        "tool_calls": tool_calls,
        "denied": [
            f"{denial['tool_name']}: {json.dumps(denial['tool_input'])[:200]}"
            for denial in out["permission_denials"]
        ],
    }


def model_diagnosis(status: dict, model: str) -> dict:
    with tempfile.TemporaryDirectory() as empty:
        return _claude(MODEL_PROMPT, status, Path(empty), ["--tools", ""], model)


def agent_diagnosis(
    status: dict, model: str, run_path: Path, log: Path, machine: str | None = None
) -> dict:
    """Tier 1. With `machine`, a replay: the recorded machine replaces the shell."""
    if machine is None:
        prompt = AGENT_PROMPT.format(run_dir=run_path, bash=", ".join(AGENT_BASH))
        extra = [
            "--tools",
            "Read,Grep,Glob,Bash",
            "--allowedTools",
            *(f"Bash({command}:*)" for command in AGENT_BASH),
        ]
    else:
        prompt = REPLAY_PROMPT.format(run_dir=run_path)
        extra = ["--tools", "Read,Grep,Glob"]
    extra += ["--permission-mode", "dontAsk", "--permission-prompts", "none"]
    if run_path.is_dir():
        extra += ["--add-dir", str(run_path)]
    with tempfile.TemporaryDirectory() as workdir:
        if log.is_file():
            shutil.copy(log, Path(workdir) / "console.log")
        if machine is not None:
            (Path(workdir) / "machine.txt").write_text(machine, encoding="utf-8")
        return _claude(prompt, status, Path(workdir), extra, model)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("entry", type=Path)
    parser.add_argument("--policy", choices=("script", "model", "agent"), required=True)
    parser.add_argument("--model", default="claude-opus-5-5")
    args = parser.parse_args()

    entry = load_entry(args.entry)
    state = read_state(entry)
    if state.state is not State.FAILED:
        raise SystemExit(f"{entry['name']} is {state.state.value}, not FAILED")

    status = failure_status(entry, state.k_status)
    machine = machine_snapshot()
    if args.policy == "script":
        diagnosis = script_diagnosis(status)
    elif args.policy == "model":
        diagnosis = model_diagnosis(status, args.model)
    else:
        diagnosis = agent_diagnosis(
            status, args.model, run_dir(entry), console_log(entry)
        )
    entry["diagnosis"] = {
        "policy": args.policy,
        "input": status,
        "machine": machine,
        **diagnosis,
    }
    save_entry(args.entry, entry)
    print(json.dumps({"policy": args.policy, **diagnosis}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
