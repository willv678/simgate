"""How often does each tier choose the right recovery? Replay real FAILED statuses.

Each case is the status diagnose.py recorded for a real failure. Tier 0 and
tier 1 answer it `--samples` times; the script answers once (it is
deterministic). An answer is right when its skill is in the case's RIGHT set
and validate_diagnosis.rejection accepts it against the config the run used.

Tier 1 sees the machine as diagnose.py recorded it at failure time. Failures
diagnosed before that record existed (29 Sep) replay against the live machine.

    uv run python research/harness/repeat_tiers.py --samples 5
"""

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from compare_policies import used_config
from diagnose import agent_diagnosis, model_diagnosis, script_diagnosis
from read_state import console_log, load_entry, run_dir
from validate_diagnosis import rejection

HARNESS = Path(__file__).resolve().parent
MODEL = "claude-opus-5-5"
RETRY = {"RE-RUN", "RESTART_CLEANUP"}
# (case, entry file, right skills, right params when CONFIGURE)
CASES = (
    ("drop_delay (persistent)", "c0_queue/001_c0_001.json", {"HALT"}, None),
    ("hang (transient)", "c0_queue/002_c0_002.json", RETRY, None),
    ("delete_metrics", "c0_queue/004_c0_004.json", RETRY, None),
    ("kill", "c0_queue/005_c0_005.json", RETRY, None),
    ("corrupt_metrics", "c0_queue/006_c0_006.json", RETRY, None),
    (
        "CUDA OOM (l8_ctx8)",
        "w1_model_queue/002_l8_ctx8.json",
        {"CONFIGURE"},
        {"trafficsim_device": "cpu"},
    ),
)
OUTPUT = HARNESS / "repeat_tiers.json"
TABLE = HARNESS / "repeat_tiers.txt"


def right(answer: dict, entry: dict, k_status: str, skills: set, params) -> bool:
    if answer["skill"] not in skills:
        return False
    if params is not None and answer["params"] != params:
        return False
    judged = {
        **entry,
        "config": used_config(entry),
        "env_cleanups": 0,
        "diagnosis": answer,
    }
    return rejection(judged, k_status) is None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, required=True)
    args = parser.parse_args()

    results = {}
    lines = ["case\tscript\ttier0 right\ttier0 choices\ttier1 right\ttier1 choices"]
    for case, file, skills, params in CASES:
        entry = load_entry(HARNESS / file)
        status = entry["diagnosis"]["input"]
        answers = {
            "script": [script_diagnosis(status)],
            "tier0": [model_diagnosis(status, MODEL) for _ in range(args.samples)],
            "tier1": [
                agent_diagnosis(
                    status,
                    MODEL,
                    run_dir(entry),
                    console_log(entry),
                    entry["diagnosis"].get("machine"),
                )
                for _ in range(args.samples)
            ],
        }
        scored = {
            tier: [right(a, entry, status["k_status"], skills, params) for a in batch]
            for tier, batch in answers.items()
        }
        choices = {
            tier: dict(Counter(str(a["skill"]) for a in batch))
            for tier, batch in answers.items()
        }
        results[case] = {"answers": answers, "right": scored, "choices": choices}
        lines.append(
            "\t".join(
                [
                    case,
                    f"{answers['script'][0]['skill']} ({'right' if scored['script'][0] else 'wrong'})",
                    f"{sum(scored['tier0'])}/{args.samples}",
                    json.dumps(choices["tier0"]),
                    f"{sum(scored['tier1'])}/{args.samples}",
                    json.dumps(choices["tier1"]),
                ]
            )
        )
        print(lines[-1], flush=True)
    lines.append(f"model\t{MODEL}")
    OUTPUT.write_text(json.dumps(results, indent=1) + "\n")
    TABLE.write_text("\n".join(lines) + "\n")
    print(TABLE.read_text())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
