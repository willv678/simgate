"""Check the physics bounds on kept clean runs and on silent faults.

The bounds in rules/physics.json come from what a road car can do, not from
fitting. This script checks them: every kept B2 run (one scene), every kept S1
run (other scenes, a held-out check), and the clean pilot runs should pass; the
silent faults (rails, kinematic) should not. It reads no config file, so a
catch here is physics alone. Writes physics_calibration.json and .txt.

    uv run python research/harness/calibrate_physics.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from read_state import ROOT, load_entry, queue_entries

from physics import check, load_bounds, run_features

HARNESS = Path(__file__).resolve().parent
OUTPUT = HARNESS / "physics_calibration.json"
TABLE = HARNESS / "physics_calibration.txt"
SILENT = ("rails", "kinematic")
PLAN = ("lateral_bias", "lateral_bias_small", "plan_freeze", "waypoint_noise")


def kept(queue: str, faulted: bool | None, kinds: tuple = SILENT) -> dict[str, dict]:
    """Kept entries of a queue by name; faulted None means any, True only
    `kinds` faults, False none of them."""
    runs = {}
    for path in queue_entries(HARNESS / queue):
        entry = load_entry(path)
        if entry["resolution"] != "ACCEPT":
            continue
        fault = entry.get("fault")
        kind = fault["kind"] if fault else None
        if faulted is True and kind not in kinds:
            continue
        if faulted is False and kind in kinds:
            continue
        runs[entry["name"]] = entry
    return runs


def main() -> int:
    bounds = load_bounds()
    groups = {
        "B2 clean (one scene)": kept("b2_queue", None),
        "S1 clean (other scenes, held out)": kept("s1_queue", None),
        "pilot clean": kept("c0_queue", False),
        "silent faults": kept("c0_queue", True),
        "plan faults (g2)": kept("g2_plan_queue", True, PLAN),
        "g2 clean": kept("g2_plan_queue", False, PLAN),
    }
    results = {}
    lines = ["group\truns\tflagged\tfeature maxima"]
    for group, runs in groups.items():
        rows = {}
        for name, entry in runs.items():
            path = ROOT / entry["run_dir"]
            rows[name] = {
                "features": run_features(path),
                "problems": check(path, bounds, entry["config"]["planner_delay_us"]),
            }
        results[group] = rows
        flagged = sum(bool(r["problems"]) for r in rows.values())
        maxima = (
            {
                key: round(max(r["features"][key] for r in rows.values()), 3)
                for key in bounds["max"]
            }
            if rows
            else {}
        )
        lines.append(f"{group}\t{len(rows)}\t{flagged}\t{json.dumps(maxima)}")
        print(lines[-1], flush=True)
    OUTPUT.write_text(json.dumps(results, indent=1, default=float) + "\n")
    TABLE.write_text("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
