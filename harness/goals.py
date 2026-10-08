"""A study's goal, in a form code can check after every round.

The planner states the goal; plan_problems() in study.py checks it with
goal_problems(); after each round outer.run_study() calls goal_status() on the
kept runs and stops the study once the goal is met. The verdict comes from
here, from the 90% ranges of the failure rates (rate_range), never from the
model.

Four kinds:

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
- compare: in an A/B study, which of two controllers fails less. Every
  setting runs on both; pooled over the settings' paired runs, met when the
  90% ranges of the two failure rates separate and the pairs cover at least
  COMPARE_MIN_SETTINGS knob settings on COMPARE_MIN_SCENES scenes (a
  difference found at one setting says nothing about the question's range);
  "no difference shown" while the ranges overlap, and at the end of the
  budget if they still do. Also the exact two-sided sign test over the pairs
  where exactly one controller failed.

In a study that varies several knobs, a goal reads only the runs where every
other varied knob is at its unvaried value (knobs.UNVARIED).
"""

from itertools import pairwise
from math import comb

from knobs import SCENARIO, SIDES, UNVARIED

TYPES = ("separate", "bracket", "top_k", "compare")
# A compare goal is met only once its pairs cover this much of the question:
# distinct knob settings (scene apart) and distinct scenes.
COMPARE_MIN_SETTINGS = 3
COMPARE_MIN_SCENES = 2
KEYS = {
    "separate": {"type", "scene", "knob", "low", "high"},
    "top_k": {"type", "k", "high_min", "distinct_scenes"},
    "bracket": {"type", "scenes", "knob", "low_max", "high_min", "max_gap"},
    "compare": {"type"},
}


def rate_range(failed: int, runs: int, z: float = 1.645) -> tuple[float, float]:
    """The 90% Wilson interval for a failure rate from `failed` of `runs`; with
    no runs, every rate fits."""
    if runs == 0:
        return 0.0, 1.0
    p = failed / runs
    centre = (p + z * z / (2 * runs)) / (1 + z * z / runs)
    half = (
        z
        / (1 + z * z / runs)
        * ((p * (1 - p) / runs + z * z / (4 * runs * runs)) ** 0.5)
    )
    return round(max(0.0, centre - half), 2), round(min(1.0, centre + half), 2)


def sign_test(a: int, b: int) -> float:
    """Exact two-sided p of a split of a + b flips at least this uneven."""
    n, k = a + b, min(a, b)
    if n == 0:
        return 1.0
    return min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2**n)


def goal_problems(goal: dict, scenes: set[str], varied: tuple) -> list[str]:
    """Why a goal cannot be checked; empty when it can."""
    kind = goal.get("type")
    if kind not in TYPES:
        return [f"goal type must be one of {TYPES}"]
    if set(goal) != KEYS[kind]:
        return [f"a {kind} goal has exactly the keys {sorted(KEYS[kind])}"]
    if kind == "compare":
        return []
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


_NOT_KNOBS = {"id", "scene_id", *SIDES, "paired"}


def compare_status(table: list[dict]) -> dict:
    """Which controller fails less, from an A/B results table: each side's
    failures pooled over the paired runs of every setting, with the 90% range
    of its failure rate, and the sign test over the pairs where exactly one
    side failed."""
    pairs = sum(row["paired"]["pairs"] for row in table)
    pooled = {
        side: {
            "controller": table[0][side]["controller"] if table else None,
            "pairs": pairs,
            "failed": sum(row["paired"][f"{side}_failed"] for row in table),
        }
        for side in SIDES
    }
    for side in SIDES:
        pooled[side]["failure_rate_90"] = rate_range(pooled[side]["failed"], pairs)
    only = {
        side: sum(row["paired"][f"only_{side}_failed"] for row in table)
        for side in SIDES
    }
    sign = {
        "only_a_failed": only["a"],
        "only_b_failed": only["b"],
        "p": round(sign_test(only["a"], only["b"]), 3),
    }
    paired = [row for row in table if row["paired"]["pairs"]]
    coverage = {
        "knob_settings": len(
            {tuple(v for k, v in row.items() if k not in _NOT_KNOBS) for row in paired}
        ),
        "scenes": len({row["scene_id"] for row in paired}),
    }
    a, b = pooled["a"], pooled["b"]
    if a["failure_rate_90"][1] < b["failure_rate_90"][0]:
        safer, other = a, b
    elif b["failure_rate_90"][1] < a["failure_rate_90"][0]:
        safer, other = b, a
    else:
        return {
            "met": False,
            "verdict": "no difference shown: the pooled 90% ranges overlap",
            "pooled": pooled,
            "sign_test": sign,
            "coverage": coverage,
        }
    verdict = (
        f"{safer['controller']} fails less than {other['controller']}: "
        "the pooled 90% ranges separate"
    )
    if (
        coverage["knob_settings"] < COMPARE_MIN_SETTINGS
        or coverage["scenes"] < COMPARE_MIN_SCENES
    ):
        return {
            "met": False,
            "verdict": f"{verdict}, but only over {coverage['knob_settings']} knob "
            f"settings on {coverage['scenes']} scenes; the comparison needs "
            f"{COMPARE_MIN_SETTINGS} and {COMPARE_MIN_SCENES}",
            "pooled": pooled,
            "sign_test": sign,
            "coverage": coverage,
        }
    return {
        "met": True,
        "verdict": verdict,
        "pooled": pooled,
        "sign_test": sign,
        "coverage": coverage,
    }


def goal_status(goal: dict, table: list[dict], varied: tuple) -> dict:
    """{"met": bool, "verdict": str, ...} from outer.results(); a compare goal
    reads the A/B table, outer.results() with `compare`."""
    if goal["type"] == "compare":
        return compare_status(table)
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
