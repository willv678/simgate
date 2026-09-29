"""How repeatable is the tier 2 auditor? Re-audit each eval_auditor batch.

Each repeat uses a new seed, so the run ids and their order change too.
Together with the original audit in auditor_eval.json, every batch has
`--repeats + 1` samples. Writes auditor_repeats.json and .txt.

    uv run python research/harness/repeat_auditor.py --repeats 2
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from audit import audit
from eval_auditor import CASES, MODEL, score
from eval_auditor import OUTPUT as FIRST

HARNESS = Path(__file__).resolve().parent
OUTPUT = HARNESS / "auditor_repeats.json"
TABLE = HARNESS / "auditor_repeats.txt"
SEED_BASE = 100


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repeats", type=int, required=True)
    args = parser.parse_args()

    first = json.loads(FIRST.read_text())
    results = {}
    lines = ["case\tsamples\tcaught per sample\tfalse flags per sample"]
    for index, (name, build) in enumerate(CASES.items()):
        case = build()
        samples = [first[name]["scores"]]
        for repeat in range(args.repeats):
            seed = SEED_BASE + index * 10 + repeat
            report = audit(
                case["claim"], case["runs"], case["labels"], MODEL, seed=seed
            )
            samples.append(score(case, report))
            print(name, seed, samples[-1], flush=True)
        results[name] = samples
        caught = ",".join(f"{s['caught']}/{s['invalid']}" for s in samples)
        false = ",".join(str(s["false_flags"]) for s in samples)
        lines.append(f"{name}\t{len(samples)}\t{caught}\t{false}")
    lines.append(f"model\t{MODEL}")
    OUTPUT.write_text(json.dumps(results, indent=1) + "\n")
    TABLE.write_text("\n".join(lines) + "\n")
    print(TABLE.read_text())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
