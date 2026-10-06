"""Does feeding VaVAM a fresh frame every plan change how often it fails?

S1 ran every downloaded scene once with a frame every 500 ms (four of five plans
reuse the last frames); v1 ran the first 20 of the same scenes with a frame
every 100 ms and every fifth frame in the context (read_state.subsample_factor).
Both at 0 planner delay, same everything else, every run through the full
gate. Pairs each v1 scene with its S1 run: failure rates with 90% ranges, and
the scenes that flipped. The exact two-sided sign test on the flips says
whether the difference is more than chance (McNemar).

    uv run python research/harness/compare_frames.py
"""

import json
import sys
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from outer import outcome, rate_range
from read_state import ROOT, load_entry, queue_entries

HARNESS = Path(__file__).resolve().parent
OUTPUT = HARNESS / "compare_frames.json"


def kept(queue: str) -> dict[str, dict]:
    """scene_id -> outcome of each kept run of the queue (first kept run per scene)."""
    found = {}
    for path in queue_entries(HARNESS / queue):
        entry = load_entry(path)
        if entry["resolution"] == "ACCEPT" and "quarantine" not in entry:
            found.setdefault(
                entry["config"]["scene_id"],
                {"run": entry["name"], **outcome(ROOT / entry["run_dir"])},
            )
    return found


def sign_test(a: int, b: int) -> float:
    """Exact two-sided p of a split of a + b flips at least this uneven."""
    n, k = a + b, min(a, b)
    if n == 0:
        return 1.0
    return min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2**n)


def main() -> int:
    old, new = kept("s1_queue"), kept("v1_queue")
    scenes = sorted(set(old) & set(new))
    pairs = [(old[s], new[s]) for s in scenes]
    fixed = [s for s, (o, n) in zip(scenes, pairs) if o["failed"] and not n["failed"]]
    broke = [s for s, (o, n) in zip(scenes, pairs) if n["failed"] and not o["failed"]]
    report = {
        "scenes": len(scenes),
        "frames_every_500ms": {
            "failed": sum(o["failed"] for o, _ in pairs),
            "rate_90": rate_range(sum(o["failed"] for o, _ in pairs), len(pairs)),
        },
        "frames_every_100ms": {
            "failed": sum(n["failed"] for _, n in pairs),
            "rate_90": rate_range(sum(n["failed"] for _, n in pairs), len(pairs)),
        },
        "failed_only_with_stale_frames": fixed,
        "failed_only_with_fresh_frames": broke,
        "sign_test_p": round(sign_test(len(fixed), len(broke)), 3),
        "per_scene": {
            s[7:15]: {
                "500ms": o["failed"],
                "100ms": n["failed"],
                "runs": [o["run"], n["run"]],
            }
            for s, (o, n) in zip(scenes, pairs)
        },
    }
    OUTPUT.write_text(json.dumps(report, indent=1) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "per_scene"}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
