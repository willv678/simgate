"""Who closed the gap at a run's first at-fault contact: the ego or the actor?

outer.outcome counts a front or side collision before any rear contact as
the policy's. With traffic replayed, an actor cannot react to the ego: a car
that brakes on an open road can be run into by a replayed car coming up from
behind on the side, and the evaluator may score that contact at the ego's
front corner (triage cause actor_hit_ego). This reads the poses around the
first at-fault contact: over the WINDOW_US before it, the ego's and the
actor's speed toward each other along the line between their box centres
at the window's start; at contact, how far the ego was from the recorded
path toward the actor's side (drift_analysis.signed_offset).

The actor closed the gap when the ego was not moving toward it
(EGO_STILL_MPS), the actor was, and the ego was still inside its lane: its
offset toward the actor less than the room a car of its width has to the
lane line in a lane LANE_WIDTH_M wide (nuPlan's rule: an ego in two lanes is
at fault in a side contact). Comparing the two closing speeds instead would
blame the faster car in a head-on (the ego drifting into an oncoming lane at
10 m/s, met at 17 m/s); and an ego that drifted over seconds onto the lane
line (the policy's lean, DRIFT.md) and was passed by a faster car is in
that car's lane though it moved little in the last second. Lane widths are
not in the log, so the result is also given for SENSITIVITY_LANES_M.

For each named study, every kept failure that is a collision (not off-road
first) is classified and compared with its triage cause, and the method
table (analyze_methods) is recomputed with actor-closed contacts not counted.
Writes research/CLOSED.md and research/closed.json.

    uv run python research/harness/who_closed.py [study ...]
"""

import asyncio
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

import analyze_methods
import compare_proposers
import outer
from compare_proposers import arms
from drift_analysis import signed_offset
from physics import EGO, _footprint, _read, completed_rollout
from read_state import ROOT, load_entry, queue_entries

STUDIES = ROOT / "research" / "studies"
DEFAULT = ("cut_in_merge", "lead_vehicle", "pedestrian_ego_speed")
WINDOW_US = 1_000_000
# The ego is not moving toward the actor below this speed: pose noise at
# rest is centimetres per second.
EGO_STILL_MPS = 0.5
# US freeway lanes are 3.6-3.7 m (12 ft); the scenes are US highways.
LANE_WIDTH_M = 3.6
SENSITIVITY_LANES_M = (3.3, 3.6, 3.9)


def _logged(track: dict, t: float) -> float:
    """The latest logged timestamp not after t (the first if none is)."""
    times = [s for s in track if s <= t]
    return max(times) if times else min(track)


def _at(track: dict, t: float) -> tuple:
    """The pose at the latest timestamp not after t."""
    return track[_logged(track, t)]


def contact(run_dir: Path) -> dict | None:
    """The first at-fault contact's actor, closing speeds and the ego's
    offset toward the actor; None when the run has no at-fault collision or
    went off-road first."""
    metrics = pd.read_parquet(completed_rollout(run_dir) / "metrics.parquet")
    relevant = metrics[metrics["name"] == "eval_relevant"]
    driven = float(relevant.loc[relevant["values"] > 0, "timestamps_us"].min())
    hit = min(
        outer._first(metrics, "collision_front", driven),
        outer._first(metrics, "collision_lateral", driven),
    )
    rear = outer._first(metrics, "collision_rear", driven)
    offroad = outer._first(metrics, "offroad", driven)
    if not hit < rear or not hit <= offroad:
        return None
    raw = asyncio.run(_read(completed_rollout(run_dir) / "rollout.asl"))
    ego_track = raw["ego"]
    actors: dict[str, dict] = {}
    for t, rows in raw["others"].items():
        for x, y, yaw, actor_id in rows:
            actors.setdefault(actor_id, {})[t] = (x, y, yaw)
    ex, ey, eyaw = _at(ego_track, hit)
    ego_box = _footprint(ex, ey, eyaw, raw["sizes"][EGO])

    def overlap_or_distance(actor_id):
        x, y, yaw = _at(actors[actor_id], hit)
        other = _footprint(x, y, yaw, raw["sizes"][actor_id])
        return (-ego_box.intersection(other).area, ego_box.distance(other))

    near = [a for a in actors if min(actors[a]) <= hit <= max(actors[a])]
    actor_id = min(near, key=overlap_or_distance)
    # Poses are logged once per control step (100 ms, or 500 ms at 2 Hz).
    start, end = _logged(ego_track, hit - WINDOW_US), _logged(ego_track, hit)
    e0, e1 = np.array(ego_track[start][:2]), np.array([ex, ey])
    a0 = np.array(_at(actors[actor_id], start)[:2])
    a1 = np.array(_at(actors[actor_id], end)[:2])
    line = (a0 - e0) / np.linalg.norm(a0 - e0)
    seconds = (end - start) / 1e6
    left = np.array([-np.sin(eyaw), np.cos(eyaw)])
    side = float(np.sign((a1 - e1) @ left))
    return {
        "actor": actor_id,
        "contact_s": round((hit - driven) / 1e6, 1),
        "ego_closing_mps": round(float((e1 - e0) @ line) / seconds, 2),
        "actor_closing_mps": round(float(-(a1 - a0) @ line) / seconds, 2),
        "toward_actor_m": round(signed_offset(raw, hit) * side, 2),
        "ego_width_m": round(float(raw["sizes"][EGO][1]), 2),
    }


def actor_closed(c: dict, lane_m: float = LANE_WIDTH_M) -> bool:
    return (
        c["ego_closing_mps"] <= EGO_STILL_MPS
        and c["actor_closing_mps"] > EGO_STILL_MPS
        and c["toward_actor_m"] < (lane_m - c["ego_width_m"]) / 2
    )


def triage_causes(study: Path) -> dict:
    found = {}
    for path in [*study.glob("*/triage.json"), *study.glob("triage.json")]:
        for t in json.loads(path.read_text(encoding="utf-8")):
            found[t["run"]] = t["cause"]
    return found


def classify(study: Path) -> dict:
    """run directory name -> contact() for every kept collision failure."""
    found = {}
    for folder in arms(study).values():
        for path in queue_entries(folder / "queue"):
            entry = load_entry(path)
            if entry["resolution"] != "ACCEPT" or "quarantine" in entry:
                continue
            run_dir = ROOT / entry["run_dir"]
            if outer.outcome(run_dir)["collision_at_fault"]:
                found[run_dir.name] = contact(run_dir)
    return found


def methods_without(names: list, closed: set) -> dict:
    """analyze_methods' table with the runs in `closed` not counted as
    failures (outer.outcome patched for the duration), over the arms
    analyze_methods compares. An arm that stopped at its goal and no longer
    meets it shows how many it confirmed in the runs it took."""
    plans, compared = {}, {}
    for name in names:
        study = STUDIES / name
        plans[name] = json.loads((study / "plan.json").read_text(encoding="utf-8"))["plan"]
        reps, _ = analyze_methods.replicate_rows(study, plans[name])
        compared[name] = [r["arm"] for rows in reps.values() for r in rows]
    original = outer.outcome

    def stricter(run_dir: Path) -> dict:
        found = original(run_dir)
        if Path(run_dir).name in closed and not found["offroad"]:
            found = {**found, "failed": False, "collision_at_fault": False}
        return found

    outer.outcome = stricter
    try:
        table = {}
        for name, plan in plans.items():
            folders = arms(STUDIES / name)
            reps = {}
            for arm in compared[name]:
                report = compare_proposers.proposer_report(
                    folders[arm], plan["goal"], tuple(plan["vary"]), plan["fixed"].get("compare")
                )
                reps.setdefault(compare_proposers.proposer_of(arm), []).append(report)
            k, budget = plan["goal"]["k"], analyze_methods.plan_runs(plan)
            table[name] = {p: analyze_methods.summary(r, k, budget) for p, r in reps.items()}
        return table
    finally:
        outer.outcome = original


def _cell(m: dict | None) -> str:
    if not m:
        return "-"
    if m["reached"] == m["replicates"]:
        return ", ".join(str(r) for r in m["runs_to_goal"])
    return ", ".join(f"{c} of 5" for c in m["confirmed"])


def main() -> int:
    names = sys.argv[1:] or list(DEFAULT)
    contacts = {name: classify(STUDIES / name) for name in names}
    report = {}
    for name in names:
        causes = triage_causes(STUDIES / name)
        agree = Counter()
        for run, c in contacts[name].items():
            if c is not None:
                agree[(actor_closed(c), causes.get(run) == "actor_hit_ego")] += 1
        report[name] = {
            "collisions": sum(c is not None for c in contacts[name].values()),
            "actor_closed": {
                str(lane): sum(bool(c and actor_closed(c, lane)) for c in contacts[name].values())
                for lane in SENSITIVITY_LANES_M
            },
            "rule_and_triage": {
                "both_actor": agree[(True, True)],
                "rule_only": agree[(True, False)],
                "triage_only": agree[(False, True)],
                "neither": agree[(False, False)],
            },
            "contacts": contacts[name],
        }
    proposers = [
        p
        for p in compare_proposers.PROPOSERS
        if p in ("rules", "rules_v3", "hybrid", "llm", "random_confirm")
    ]
    counted = methods_without(names, set())
    tables = {
        str(lane): methods_without(
            names,
            {
                run
                for name in names
                for run, c in contacts[name].items()
                if c and actor_closed(c, lane)
            },
        )
        for lane in SENSITIVITY_LANES_M
    }
    (ROOT / "research" / "closed.json").write_text(
        json.dumps(
            {"studies": report, "methods_as_counted": counted, "methods_without_actor_closed": tables},
            indent=1,
        )
        + "\n"
    )
    lines = [
        "# Who closed the gap at the first contact",
        "",
        "Generated by `harness/who_closed.py`. Every kept run counted as a",
        "collision failure (outer.outcome): at its first at-fault contact, did",
        "the replayed actor close the gap on an ego that was not moving toward",
        "it and still in its own lane? Compared with each run's triage cause",
        f"(actor_hit_ego or not), lane {LANE_WIDTH_M} m.",
        "",
        "| study | collisions | actor closed (lane 3.3 / 3.6 / 3.9 m) | rule and triage: actor | rule only | triage only | neither |",
        "|---|---|---|---|---|---|---|",
    ]
    for name, r in report.items():
        a, n = r["rule_and_triage"], r["actor_closed"]
        lines.append(
            f"| {name} | {r['collisions']} | {' / '.join(str(n[str(l)]) for l in SENSITIVITY_LANES_M)} "
            f"| {a['both_actor']} | {a['rule_only']} | {a['triage_only']} | {a['neither']} |"
        )
    lines += [
        "",
        "Runs to the goal (or confirmed of 5), as counted and with actor-closed",
        "contacts not counted:",
        "",
        "| study | count | " + " | ".join(proposers) + " |",
        "|---|---|" + "---|" * len(proposers),
    ]
    for name in names:
        rows = [("as counted", counted[name])] + [
            (f"without, lane {lane} m", tables[str(lane)][name]) for lane in SENSITIVITY_LANES_M
        ]
        for label, methods in rows:
            lines.append(
                f"| {name} | {label} | " + " | ".join(_cell(methods.get(p)) for p in proposers) + " |"
            )
    (ROOT / "research" / "CLOSED.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
