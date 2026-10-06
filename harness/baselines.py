"""Proposers to compare Claude with, on the same knobs, gate and goal.

- grid: the status quo. Every scene at every value of the goal's knob, in
  order, then again: a sweep repeated until the budget runs out.
- bisect: what an engineer would script for a bracket goal. Per scene, binary
  search over the knob's values: probe the middle of the range still open,
  and repeat a probed value until its 90% range says surely low or surely
  high (goals.py), then move on. A settled scene gets no more runs.

Both read only what Claude's proposer reads: the kept runs so far. Neither
reads the brief; each is written for one kind of question, which is what the
comparison is about.
"""

from goals import goal_cells
from knobs import SCENARIO, UNVARIED


def _knob(goal: dict | None, varied: tuple) -> str:
    return goal["knob"] if goal else varied[0]


def _run(scene: str, knob: str, value, varied: tuple, why: str) -> dict:
    return {
        "scene_id": scene,
        **{k: UNVARIED[k] for k in varied},
        knob: value,
        "why": why,
    }


def grid_proposals(
    scenes: list[str], count: int, done: int, goal: dict | None, varied: tuple
) -> dict:
    """The next `count` cells of the sweep, after the `done` already proposed."""
    knob = _knob(goal, varied)
    sweep = [(scene, value) for value in SCENARIO[knob] for scene in scenes]
    picks = [sweep[(done + i) % len(sweep)] for i in range(count)]
    return {
        "plan": "grid: every scene at every value, in order, repeated",
        "runs": [_run(s, knob, v, varied, "grid") for s, v in picks],
    }


def next_probe(scene: str, cells: dict, goal: dict) -> object | None:
    """The value bisection probes next on one scene, or None once settled."""
    values = SCENARIO[goal["knob"]]
    rows = {v: cells[(scene, v)] for v in values if (scene, v) in cells}
    low = [v for v, r in rows.items() if r["failure_rate_90"][1] < goal["low_max"]]
    high = [v for v, r in rows.items() if r["failure_rate_90"][0] > goal["high_min"]]
    if any(0 < b - a <= goal["max_gap"] for a in low for b in high):
        return None
    if values[-1] in low or values[0] in high:
        return None
    floor = max(low, default=None)
    ceiling = min((b for b in high if floor is None or b > floor), default=None)
    open_values = [
        v
        for v in values
        if (floor is None or v > floor) and (ceiling is None or v < ceiling)
    ]
    if not open_values:
        return None
    middle = open_values[len(open_values) // 2]
    unsure = [v for v in open_values if v in rows]
    # Keep sampling the probed value nearest the middle until it is classified.
    if unsure:
        return min(
            unsure, key=lambda v: abs(open_values.index(v) - len(open_values) // 2)
        )
    return middle


def bisect_proposals(
    scenes: list[str], count: int, table: list[dict], goal: dict, varied: tuple
) -> dict:
    """`count` runs spread over the unsettled scenes, each at its next probe."""
    cells = goal_cells(table, goal["knob"], varied)
    probes = [(s, next_probe(s, cells, goal)) for s in scenes]
    probes = [(s, v) for s, v in probes if v is not None]
    if not probes:
        return {"plan": "bisect: every scene settled", "runs": []}
    picks = [probes[i % len(probes)] for i in range(count)]
    return {
        "plan": f"bisect: {len(probes)} scenes still open",
        "runs": [_run(s, goal["knob"], v, varied, "bisect") for s, v in picks],
    }
