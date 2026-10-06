"""A study's goal, in a form code can check after every round.

The planner states the goal; plan_problems() in study.py checks it with
goal_problems(); after each round outer.run_study() calls goal_status() on the
kept runs and stops the study once the goal is met. The verdict comes from
here, from the 90% ranges of the failure rates (outer.rate_range), never from
the model.

Three kinds:

- separate: the failure rate at `high` is higher than at `low`, on one scene,
  for one knob: met when the range at `high` lies wholly above the range at
  `low`. "opposite" when they separate the other way.
- bracket: for each scene, where the failure rate goes from low to high as one
  knob increases: settled when some value is surely low (its range lies below
  `low_max`) and a value at most `max_gap` larger is surely high (its range
  lies above `high_min`), or when the knob's largest legal value is surely low (never
  breaks in range) or its smallest is surely high (fails already). Met when
  every scene is settled.

- top_k: the k most challenging settings: k settings (one per scene when
  `distinct_scenes`) whose failure rate is surely above `high_min`, confirmed
  by repeats, ranked by the lower end of that range and then by mean
  criticality (outer.criticality). The deliverable "after N runs, the k most
  challenging scenarios".

In a study that varies several knobs, a goal reads only the runs where every
other varied knob is at its unvaried value (knobs.UNVARIED).
"""

from itertools import pairwise

from knobs import SCENARIO, UNVARIED

TYPES = ("separate", "bracket", "top_k")
KEYS = {
    "separate": {"type", "scene", "knob", "low", "high"},
    "top_k": {"type", "k", "high_min", "distinct_scenes"},
    "bracket": {"type", "scenes", "knob", "low_max", "high_min", "max_gap"},
}


def goal_problems(goal: dict, scenes: set[str], varied: tuple) -> list[str]:
    """Why a goal cannot be checked; empty when it can."""
    kind = goal.get("type")
    if kind not in TYPES:
        return [f"goal type must be one of {TYPES}"]
    if set(goal) != KEYS[kind]:
        return [f"a {kind} goal has exactly the keys {sorted(KEYS[kind])}"]
    if kind == "top_k":
        problems = []
        if not 1 <= goal["k"] <= 10:
            problems.append("k must be 1 to 10")
        if goal["distinct_scenes"] and goal["k"] > len(scenes):
            problems.append("k distinct scenes needs at least k study scenes")
        if not 0.5 <= goal["high_min"] < 1:
            problems.append("need 0.5 <= high_min < 1")
        return problems
    if goal["knob"] not in varied:
        return [f"goal knob {goal['knob']!r} is not a knob the study varies"]
    values = SCENARIO[goal["knob"]]
    if kind == "separate":
        problems = []
        if goal["scene"] not in scenes:
            problems.append(f"goal scene {goal['scene']!r} is not a study scene")
        if goal["low"] not in values or goal["high"] not in values:
            problems.append(f"goal values must be among {list(values)}")
        elif goal["low"] >= goal["high"]:
            problems.append("goal low must be smaller than high")
        return problems
    problems = []
    if not goal["scenes"] or set(goal["scenes"]) - scenes:
        problems.append("goal scenes must be study scenes")
    if not 0 < goal["low_max"] <= 0.5 <= goal["high_min"] < 1:
        problems.append("need 0 < low_max <= 0.5 <= high_min < 1")
    step = min(b - a for a, b in pairwise(values))
    if not step <= goal["max_gap"] < values[-1] - values[0]:
        problems.append(f"max_gap must be from {step} to below the knob's whole range")
    return problems


def goal_cells(table: list[dict], knob: str, varied: tuple) -> dict:
    """(scene, value) -> the table row, for rows with every other knob unvaried."""
    others = [k for k in varied if k != knob]
    return {
        (row["scene_id"], row[knob]): row
        for row in table
        if all(row[k] == UNVARIED[k] for k in others)
    }


def challenging(table: list[dict], goal: dict) -> list[dict]:
    """The settings whose failure rate is surely above `high_min`, most
    critical first, at most one per scene when the goal asks for distinct
    scenes."""
    sure = [r for r in table if r["failure_rate_90"][0] > goal["high_min"]]
    sure.sort(key=lambda r: (-r["failure_rate_90"][0], -r["criticality"], r["id"]))
    if not goal["distinct_scenes"]:
        return sure
    seen, found = set(), []
    for row in sure:
        if row["scene_id"] not in seen:
            seen.add(row["scene_id"])
            found.append(row)
    return found


def goal_status(goal: dict, table: list[dict], varied: tuple) -> dict:
    """{"met": bool, "verdict": str, ...} from outer.results()."""
    if goal["type"] == "top_k":
        found = challenging(table, goal)
        return {
            "met": len(found) >= goal["k"],
            "verdict": f"{min(len(found), goal['k'])} of {goal['k']} challenging settings confirmed",
            "settings": [row["id"] for row in found[: goal["k"]]],
        }
    cells = goal_cells(table, goal["knob"], varied)
    if goal["type"] == "separate":
        low = cells.get((goal["scene"], goal["low"]))
        high = cells.get((goal["scene"], goal["high"]))
        if low is None or high is None:
            return {"met": False, "verdict": "open: a value has no kept runs yet"}
        if high["failure_rate_90"][0] > low["failure_rate_90"][1]:
            return {"met": True, "verdict": "confirmed: the ranges separate"}
        if low["failure_rate_90"][0] > high["failure_rate_90"][1]:
            return {"met": True, "verdict": "opposite: separate the other way"}
        return {"met": False, "verdict": "open: the ranges overlap"}

    values = SCENARIO[goal["knob"]]
    settled = {}
    for scene in goal["scenes"]:
        rows = sorted((value, row) for (s, value), row in cells.items() if s == scene)
        surely_low = [v for v, r in rows if r["failure_rate_90"][1] < goal["low_max"]]
        surely_high = [v for v, r in rows if r["failure_rate_90"][0] > goal["high_min"]]
        pairs = [
            (a, b)
            for a in surely_low
            for b in surely_high
            if 0 < b - a <= goal["max_gap"]
        ]
        if pairs:
            a, b = min(pairs, key=lambda pair: pair[1] - pair[0])
            settled[scene] = f"breaks above {a} and by {b}"
        elif values[-1] in surely_low:
            settled[scene] = f"surely low even at {values[-1]}, the largest value"
        elif values[0] in surely_high:
            settled[scene] = f"surely high already at {values[0]}, the smallest value"
    met = len(settled) == len(goal["scenes"])
    return {
        "met": met,
        "verdict": f"{len(settled)} of {len(goal['scenes'])} scenes settled",
        "scenes": settled,
    }
