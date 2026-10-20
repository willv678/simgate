"""The paper's planned comparisons, recomputed from methods.json.

On each unseen study, AI picks v2 (named before either study ran) against
each of random + repeat, Optuna + repeat and rules: an exact two-sided
permutation test on the per-repeat values (difference of means), then Holm
over those three. The hard study is scored by hardest cases confirmed per
repeat (higher is better), lane keeping by kept runs to goal (lower is
better; a repeat that never got there counts as the whole budget). Writes
figures/paper/planned_tests.json.

    uv run python research/harness/planned_tests.py
"""

import json
from itertools import combinations
from math import comb
from pathlib import Path

RESEARCH = Path(__file__).resolve().parent.parent
PLANNED = ("random_confirm", "optuna_confirm", "rules")
STUDIES = {"car_conflicts_3knobs_2hz": "confirmed", "lane_keeping": "runs_to_goal"}


def permutation_p(a: list[float], b: list[float]) -> float:
    """Exact two-sided p: the share of relabellings of a + b whose difference
    of means is at least as far from zero as the one observed."""
    pooled, n = a + b, len(a)
    observed = abs(sum(a) / n - sum(b) / len(b))
    total = sum(pooled)
    extreme = 0
    for picked in combinations(range(len(pooled)), n):
        first = sum(pooled[i] for i in picked)
        if abs(first / n - (total - first) / len(b)) >= observed - 1e-12:
            extreme += 1
    return extreme / comb(len(pooled), n)


def holm(ps: list[float]) -> list[float]:
    order = sorted(range(len(ps)), key=lambda i: ps[i])
    adjusted, running = [0.0] * len(ps), 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (len(ps) - rank) * ps[i]))
        adjusted[i] = running
    return adjusted


def study_tests(proposers: dict, metric: str) -> list[dict]:
    v2 = proposers["llm_v2"][metric]
    raw = [permutation_p(v2, proposers[m][metric]) for m in PLANNED]
    return [
        {"against": m, "v2": v2, "other": proposers[m][metric], "p": p, "holm": h,
         "smallest_possible": 2 / comb(len(v2) + len(proposers[m][metric]), len(v2))}
        for m, p, h in zip(PLANNED, raw, holm(raw))
    ]


def main() -> None:
    methods = json.loads((RESEARCH / "methods.json").read_text())
    out = {s: study_tests(methods[s]["proposers"], metric) for s, metric in STUDIES.items()}
    (RESEARCH / "figures" / "paper" / "planned_tests.json").write_text(json.dumps(out, indent=1) + "\n")
    for study, tests in out.items():
        for t in tests:
            print(f"{study:26} v2 vs {t['against']:15} p {t['p']:.4f}  Holm {t['holm']:.4f}  "
                  f"(n {len(t['v2'])} v {len(t['other'])})")


if __name__ == "__main__":
    main()
