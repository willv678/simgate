"""One headless Claude call with no tools: a contract as the system prompt, JSON
on stdin, and an answer forced into a JSON schema. Used by the outer loop's
proposer, the study planner and the study reporter.

The Investigator's call (diagnose.py) differs in its tools and stream output
and keeps its own.
"""

import json
import subprocess
import tempfile
from pathlib import Path


def ask(
    prompt: str, data: dict, contract: Path, schema: dict, model: str
) -> tuple[dict, dict]:
    """The structured answer and the call's cost. Raises SystemExit if the
    call fails or gives no answer."""
    cmd = [
        "claude",
        "-p",
        prompt,
        "--model",
        model,
        "--tools",
        "",
        "--setting-sources",
        "",
        "--no-session-persistence",
        "--system-prompt-file",
        str(contract),
        "--output-format",
        "json",
        "--json-schema",
        json.dumps(schema),
    ]
    with tempfile.TemporaryDirectory() as empty:
        proc = subprocess.run(
            cmd,
            input=json.dumps(data, indent=1),
            cwd=empty,
            capture_output=True,
            text=True,
            timeout=600,
            check=False,
        )
    if proc.returncode != 0:
        raise SystemExit(f"model call failed: {proc.stderr.strip()[-500:]}")
    out = json.loads(proc.stdout)
    if out["is_error"] or out.get("structured_output") is None:
        raise SystemExit(f"model gave no answer: {str(out.get('result'))[:500]}")
    usage = out["usage"]
    call = {
        "model": ",".join(out["modelUsage"]),
        "context_tokens": usage["input_tokens"]
        + usage["cache_creation_input_tokens"]
        + usage["cache_read_input_tokens"],
        "output_tokens": usage["output_tokens"],
        "duration_ms": out["duration_ms"],
    }
    return out["structured_output"], call
