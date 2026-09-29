"""Script and model on the same real FAILED statuses. Replaces the Haiku L6 table.

Each case is the status diagnose.py recorded for a real failure. Both policies
answer it again here, and validate_diagnosis.rejection judges both answers.
Nothing is recovered or launched.

    uv run python research/harness/compare_policies.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from diagnose import model_diagnosis, script_diagnosis
from read_state import load_entry
from validate_diagnosis import rejection

HARNESS = Path(__file__).resolve().parent
MODEL = "claude-opus-5-5"
CASES = {
    "context_length 1, vetoed": HARNESS / "w1_model_queue" / "001_l8_ctx1.json",
    "CUDA out of memory (diag/l8_ctx8)": HARNESS / "w1_model_queue" / "002_l8_ctx8.json",
    "Docker network pool full (diag/b2_001)": HARNESS / "b2_queue" / "001_b2_001.json",
}
OUTPUT = HARNESS / "comparison_opus.txt"


def _verdict(entry: dict, answer: dict, k_status: str) -> str:
    reason = rejection({**entry, "diagnosis": answer}, k_status)
    return "accepted" if reason is None else f"rejected ({reason})"


def _cell(answer: dict) -> str:
    return f"{answer['skill']} {answer['params']}" if answer["params"] else answer["skill"]


def main() -> int:
    lines = ["case\tscript\tmodel\tscript_verdict\tmodel_verdict"]
    agree = 0
    for case, path in CASES.items():
        entry = load_entry(path)
        status = entry["diagnosis"]["input"]
        script = script_diagnosis(status)
        model = model_diagnosis(status, MODEL)
        agree += (script["skill"], script["params"]) == (model["skill"], model["params"])
        lines.append(
            "\t".join(
                [
                    case,
                    _cell(script),
                    _cell(model),
                    _verdict(entry, script, status["k_status"]),
                    _verdict(entry, model, status["k_status"]),
                ]
            )
        )
    lines.append(f"agreement\t{agree}/{len(CASES)}")
    lines.append(f"model\t{MODEL}")
    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(OUTPUT.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
