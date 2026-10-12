"""Does planning at 2 Hz change what the studies find?

Each 2 Hz study (studies/<name>_2hz) repeats a 10 Hz study's plan with the
policy planning every 500 ms (fixed control_timestep_us; lead vehicle without
the planner delay, which 2 Hz cannot vary). Per pair of studies:

- paired settings: every (scene, knob values) both rates ran (10 Hz at zero
  delay). Under replay a setting's outcome barely depends on the seed, so
  each setting's majority outcome at each rate is compared, with the sign
  test over the settings where exactly one rate fails;
- the share of kept runs that failed, and the hard settings and scenes of
  each (where_found.study_map; not paired: each rate's methods chose where
  to look);
- the left drift: median signed offset from the recorded path 3 s and 5 s
  after the hand-off (drift_analysis.run_offsets);
- each method's result (analyze_methods: methods.json).

Writes research/HZ.md and research/hz.json.

    uv run python research/harness/hz_compare.py
"""

import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from compare_proposers import arms
from drift_analysis import run_offsets
from goals import sign_test
from outer import history
from read_state import ROOT, load_entry, queue_entries
from where_found import study_map

STUDIES = ROOT / "research" / "studies"
PAIRS = ("pedestrian_ego_speed", "cut_in_merge", "lead_vehicle")
SUFFIX = "_2hz"


def varied_of(study: Path) -> tuple:
    return tuple(
        json.loads((study / "plan.json").read_text(encoding="utf-8"))["plan"]["vary"]
    )


def setting_outcomes(study: Path, varied: tuple) -> dict:
    """(scene, values of `varied`) -> [runs, failures], zero delay only."""
    cells = defaultdict(lambda: [0, 0])
    own = varied_of(study)
    for folder in arms(study).values():
        for row in history(folder / "queue", own):
            if row["verdict"] != "kept" or row.get("planner_delay_us", 0) != 0:
                continue
            key = (row["scene_id"], *(row[k] for k in varied))
            cells[key][0] += 1
            cells[key][1] += row["failed"]
    return cells


def drift(study: Path) -> dict:
    offsets = {3.0: [], 5.0: []}
    for folder in arms(study).values():
        for path in queue_entries(folder / "queue"):
            entry = load_entry(path)
            if entry["resolution"] != "ACCEPT" or "quarantine" in entry:
                continue
            after = run_offsets(ROOT / entry["run_dir"])["after"]
            for s in offsets:
                if s in after:
                    offsets[s].append(after[s])
    return {
        f"+{s:g} s": {
            "n": len(v),
            "median_m": round(float(np.median(v)), 2) if v else None,
            "left": round(float(np.mean(np.array(v) > 0.5)), 2) if v else None,
        }
        for s, v in offsets.items()
    }


def compare(name: str, methods: dict) -> dict:
    slow, fast = STUDIES / f"{name}{SUFFIX}", STUDIES / name
    varied = varied_of(slow)
    at = {"10 Hz": setting_outcomes(fast, varied), "2 Hz": setting_outcomes(slow, varied)}
    shared = sorted(set(at["10 Hz"]) & set(at["2 Hz"]))
    majority = {
        rate: {k: at[rate][k][1] * 2 > at[rate][k][0] for k in shared} for rate in at
    }
    only_fast = sum(majority["10 Hz"][k] and not majority["2 Hz"][k] for k in shared)
    only_slow = sum(majority["2 Hz"][k] and not majority["10 Hz"][k] for k in shared)
    per_rate = {}
    for rate, study in (("10 Hz", fast), ("2 Hz", slow)):
        found = study_map(study)
        cells = setting_outcomes(study, tuple(found["varied"]))
        runs = sum(c[0] for c in cells.values())
        per_rate[rate] = {
            "kept_runs_at_zero_delay": runs,
            "failed_share": round(sum(c[1] for c in cells.values()) / max(runs, 1), 2),
            "hard_settings": found["hard_settings"],
            "hard_scenes": found["hard_scenes"],
            "drift": drift(study),
            "methods": methods.get(study.name, {}).get("proposers", {}),
        }
    return {
        "paired_settings": len(shared),
        "both_fail": sum(majority["10 Hz"][k] and majority["2 Hz"][k] for k in shared),
        "only_10hz_fails": only_fast,
        "only_2hz_fails": only_slow,
        "sign_test_p": round(sign_test(only_fast, only_slow), 4),
        **per_rate,
    }


def _method_cell(m: dict) -> str:
    if not m:
        return "-"
    if m["reached"] == m["replicates"]:
        return ", ".join(str(r) for r in m["runs_to_goal"]) + " runs"
    return ", ".join(f"{c} of 5" for c in m["confirmed"])


def main() -> int:
    methods = json.loads((ROOT / "research" / "methods.json").read_text())
    names = [n for n in PAIRS if (STUDIES / f"{n}{SUFFIX}" / "plan.json").exists()]
    report = {name: compare(name, methods) for name in names}
    (ROOT / "research" / "hz.json").write_text(json.dumps(report, indent=1) + "\n")
    lines = [
        "# Planning at 10 Hz against 2 Hz",
        "",
        "Generated by `harness/hz_compare.py`. Each 2 Hz study repeats a 10 Hz",
        "study's plan with the policy planning every 500 ms (VaVAM's own rhythm);",
        "lead vehicle without planner delay, and its 10 Hz runs at zero delay only.",
        "Paired: settings both rates ran, each rate's majority outcome.",
        "",
        "| study | paired settings | fail at both | only 10 Hz fails | only 2 Hz fails | sign test p |",
        "|---|---|---|---|---|---|",
    ]
    for name, r in report.items():
        lines.append(
            f"| {name} | {r['paired_settings']} | {r['both_fail']} | {r['only_10hz_fails']} "
            f"| {r['only_2hz_fails']} | {r['sign_test_p']} |"
        )
    lines += [
        "",
        "| study | rate | kept runs | failed | hard settings (scenes) | drift +3 s | drift +5 s |",
        "|---|---|---|---|---|---|---|",
    ]
    for name, r in report.items():
        for rate in ("10 Hz", "2 Hz"):
            x = r[rate]
            d3, d5 = x["drift"]["+3 s"], x["drift"]["+5 s"]
            lines.append(
                f"| {name} | {rate} | {x['kept_runs_at_zero_delay']} | {x['failed_share']:.0%} "
                f"| {x['hard_settings']} ({x['hard_scenes']}) "
                f"| {d3['median_m']:+.2f} m, {d3['left']:.0%} left "
                f"| {d5['median_m']:+.2f} m, {d5['left']:.0%} left |"
                if d3["n"] and d5["n"]
                else f"| {name} | {rate} | {x['kept_runs_at_zero_delay']} | {x['failed_share']:.0%} "
                f"| {x['hard_settings']} ({x['hard_scenes']}) | - | - |"
            )
    lines += [
        "",
        "Each method, 5 hardest confirmed (runs to the goal when every replicate",
        "reached it, else how many each confirmed):",
        "",
        "| study | rate | rules | rules_v3 | hybrid | llm | random_confirm |",
        "|---|---|---|---|---|---|---|",
    ]
    for name, r in report.items():
        for rate in ("10 Hz", "2 Hz"):
            m = r[rate]["methods"]
            lines.append(
                f"| {name} | {rate} | "
                + " | ".join(
                    _method_cell(m.get(p, {}))
                    for p in ("rules", "rules_v3", "hybrid", "llm", "random_confirm")
                )
                + " |"
            )
    (ROOT / "research" / "HZ.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
