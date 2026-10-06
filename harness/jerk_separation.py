"""Can a jerk bound separate the kinematic fault from clean driving?

The kinematic fault swaps the linear MPC for kinematic_ideal. Some of its runs
stay under every physics bound (C3 kept three; the Auditor caught them by the
config and the per-scene reference). Jerk is the obvious candidate: this script
reads every run on disk with a completed rollout and compares jerk statistics
of kinematic runs with all other runs. Rails runs are left out of the other
group, since frac_on_recording already catches them. Writes jerk_separation.json
and .txt.

    uv run python research/harness/jerk_separation.py
"""

import json
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from read_state import ROOT, load_entry, queue_entries

from physics import signals

HARNESS = Path(__file__).resolve().parent
OUTPUT = HARNESS / "jerk_separation.json"
QUEUES = ("b2_queue", "s1_queue", "c0_queue", "g2_plan_queue") + tuple(
    f"{c}_{a}_queue" for c in ("c1", "c2", "c3") for a in ("script", "agent", "model")
)
STATS = {
    "p99_abs_jerk": lambda j: np.percentile(j, 99),
    "p90_abs_jerk": lambda j: np.percentile(j, 90),
    "median_abs_jerk": np.median,
    "frac_jerk_over_20": lambda j: np.mean(j > 20),
}


def jerk_stats(run_dir: Path) -> dict | None:
    try:
        jerk = np.abs(signals(run_dir)["jerk"])
    except (FileNotFoundError, OSError):
        return None
    return {name: float(f(jerk)) for name, f in STATS.items()}


def main() -> int:
    runs = []
    for queue in QUEUES:
        if not (HARNESS / queue).is_dir():
            continue
        for path in queue_entries(HARNESS / queue):
            entry = load_entry(path)
            kind = entry["fault"]["kind"] if entry.get("fault") else "clean"
            if kind != "rails":
                runs.append((queue, entry["name"], kind, ROOT / entry["run_dir"]))
    with ProcessPoolExecutor() as pool:
        found = list(pool.map(jerk_stats, [r[3] for r in runs]))
    rows = [
        {"queue": q, "name": n, "kinematic": k == "kinematic", **s}
        for (q, n, k, _), s in zip(runs, found)
        if s is not None
    ]
    lines = [
        "statistic\tkinematic min\tother max (run)\tother runs at or above kinematic min"
    ]
    result = {"runs": rows, "separation": {}}
    for name in STATS:
        kin = [r[name] for r in rows if r["kinematic"]]
        others = [r for r in rows if not r["kinematic"]]
        top = max(others, key=lambda r: r[name])
        overlap = sum(r[name] >= min(kin) for r in others)
        result["separation"][name] = {
            "kinematic_min": min(kin),
            "other_max": top[name],
            "other_max_run": top["name"],
            "others_at_or_above": overlap,
        }
        lines.append(
            f"{name}\t{min(kin):.3g}\t{top[name]:.3g} ({top['name']})\t{overlap}/{len(others)}"
        )
    lines.append(
        f"runs\t{sum(r['kinematic'] for r in rows)} kinematic, "
        f"{sum(not r['kinematic'] for r in rows)} other (rails left out)"
    )
    OUTPUT.write_text(json.dumps(result, indent=1) + "\n")
    OUTPUT.with_suffix(".txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
