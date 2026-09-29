"""Script, tier 0, and tier 1 on the same three real FAILED statuses.

Each case is the status diagnose.py recorded for a real failure. The script,
the model with no tools (tier 0), and the agent with read-only tools (tier 1)
answer it again, and validate_diagnosis.rejection judges each answer against
the config the run actually used. The Docker case is answered while
faults.fill_network_pool reproduces B2's full address pool, then the pool is
emptied. Nothing is recovered or launched.

    uv run python research/harness/compare_policies.py
"""

import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

from diagnose import agent_diagnosis, model_diagnosis, script_diagnosis
from faults import fill_network_pool, remove_networks
from read_state import console_log, load_entry, run_dir
from validate_diagnosis import rejection

HARNESS = Path(__file__).resolve().parent
MODEL = "claude-opus-5-5"
# The L8 command: this scene, CATK on CPU. l8_ctx1 never launched, so it has no resolved config.
L8_SCENE = "clipgt-01d503d4-449b-46fc-8d78-9085e70d3554"
CASES = (
    (
        "context_length 1, vetoed",
        HARNESS / "w1_model_queue" / "001_l8_ctx1.json",
        False,
    ),
    (
        "CUDA out of memory (diag/l8_ctx8)",
        HARNESS / "w1_model_queue" / "002_l8_ctx8.json",
        False,
    ),
    (
        "Docker network pool full (diag/b2_001)",
        HARNESS / "b2_queue" / "001_b2_001.json",
        True,
    ),
)
TABLE = HARNESS / "comparison_opus.txt"
DETAIL = HARNESS / "comparison_opus.jsonl"


def used_config(entry: dict) -> dict:
    """The config the run ran with, including keys older entries did not record."""
    wizard_config = run_dir(entry) / "wizard-config.yaml"
    if wizard_config.is_file():
        wizard = yaml.safe_load(wizard_config.read_text(encoding="utf-8"))
        scene_id = wizard["scenes"]["scene_ids"][0]
        device = wizard["trafficsim"]["catk"]["device"]
    else:
        scene_id, device = L8_SCENE, "cpu"
    return {**entry["config"], "scene_id": scene_id, "trafficsim_device": device}


def _verdict(entry: dict, answer: dict, k_status: str) -> str:
    judged = {
        **entry,
        "config": used_config(entry),
        "env_cleanups": 0,
        "diagnosis": answer,
    }
    reason = rejection(judged, k_status)
    return "accepted" if reason is None else f"rejected ({reason})"


def _cell(answer: dict) -> str:
    if answer["skill"] is None:
        return f"none ({answer['error'][:60]})"
    return (
        f"{answer['skill']} {answer['params']}" if answer["params"] else answer["skill"]
    )


def main() -> int:
    lines = ["case\tscript\ttier0\ttier1\tverdicts (script/tier0/tier1)"]
    details = []
    for case, path, fill_pool in CASES:
        entry = load_entry(path)
        status = entry["diagnosis"]["input"]
        fake = fill_network_pool() if fill_pool else []
        try:
            answers = {
                "script": script_diagnosis(status),
                "tier0": model_diagnosis(status, MODEL),
                "tier1": agent_diagnosis(
                    status, MODEL, run_dir(entry), console_log(entry)
                ),
            }
        finally:
            remove_networks(fake)
        verdicts = [
            _verdict(entry, answer, status["k_status"]) for answer in answers.values()
        ]
        lines.append(
            "\t".join(
                [
                    case,
                    *(_cell(answer) for answer in answers.values()),
                    " / ".join(verdicts),
                ]
            )
        )
        details.append({"case": case, "pool_filled": len(fake), **answers})
    lines.append(f"model\t{MODEL}")
    TABLE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    DETAIL.write_text(
        "".join(json.dumps(row) + "\n" for row in details), encoding="utf-8"
    )
    print(TABLE.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
