"""Proposers to compare Claude with, on the same knobs, gate and goal.

- grid: the status quo. Every scene at every value of the goal's knob, in
  order, then again: a sweep repeated until the budget runs out.
- bisect: what an engineer would script for a bracket goal. Per scene, binary
  search over the knob's values: probe the middle of the range still open,
  and repeat a probed value until its 90% range says surely low or surely
  high (goals.py), then move on. A settled scene gets no more runs.
- lhs: a Latin hypercube over the scene and every varied knob, one per round.
  Each dimension is cut into as many equal strata as the round has runs, each
  stratum is used once, and its midpoint is snapped to the scene or legal
  value it falls on, so every round covers each knob's range evenly.
- optuna: Bayesian optimisation (Optuna's TPE) of the criticality of a run,
  with the scene and each varied knob categorical over its legal values.
- ga: a genetic algorithm over the kept runs: tournament selection by
  criticality, uniform crossover of the scene and knob values, and mutation to
  a neighbouring legal value or another scene.

optuna and ga maximise the "criticality" of each kept run of the history
(outer.history), a score in [0, 1], higher being more critical. Both rebuild
their state from that history every round and are seeded from the study's
seed and the history's length, so a round's proposals depend only on what is
in the queue.

All read only what Claude's proposer reads: the kept runs so far. None reads
the brief; each is written for one kind of question, which is what the
comparison is about.
"""

import random
from itertools import product

from goals import goal_cells
from knobs import SCENARIO, UNVARIED

TOURNAMENT = 3


def _run(scene: str, knob: str, value, varied: tuple, why: str) -> dict:
    return {
        "scene_id": scene,
        **{k: UNVARIED[k] for k in varied},
        knob: value,
        "why": why,
    }


def grid_levels(knob: str, varied: tuple) -> tuple:
    """The values a grid sweeps for one knob: all of them when the study varies
    one knob; the lowest, middle and highest when it varies several, as test
    protocols such as Euro NCAP's do (a full factorial would not fit a budget)."""
    values = SCENARIO[knob]
    if len(varied) == 1:
        return values
    return (values[0], values[len(values) // 2], values[-1])


def grid_proposals(
    scenes: list[str], count: int, done: int, goal: dict | None, varied: tuple
) -> dict:
    """The next `count` cells of the sweep, after the `done` already proposed:
    every scene at every combination of the varied knobs' grid levels, in
    order, then again."""
    combos = list(product(*(grid_levels(k, varied) for k in varied)))
    sweep = [(scene, combo) for combo in combos for scene in scenes]
    picks = [sweep[(done + i) % len(sweep)] for i in range(count)]
    return {
        "plan": f"grid: {len(sweep)} cells, every scene at every level, in order",
        "runs": [
            {"scene_id": s, **dict(zip(varied, combo)), "why": "grid"}
            for s, combo in picks
        ],
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


def lhs_proposals(
    scenes: list[str], count: int, done: int, varied: tuple, seed: int
) -> dict:
    """`count` runs forming one Latin hypercube, after the `done` already
    proposed. Run i takes, in each dimension, the midpoint of stratum
    order[i] of `count`; the orders are shuffled from the seed and `done`."""
    rng = random.Random(seed * 1000 + done)
    dimensions = {"scene_id": scenes, **{knob: SCENARIO[knob] for knob in varied}}
    columns = {}
    for name, values in dimensions.items():
        order = rng.sample(range(count), count)
        columns[name] = [
            values[int((stratum + 0.5) / count * len(values))] for stratum in order
        ]
    return {
        "plan": f"lhs: one {count}-run Latin hypercube over the scene and "
        + ", ".join(varied),
        "runs": [
            {**{name: column[i] for name, column in columns.items()}, "why": "lhs"}
            for i in range(count)
        ],
    }


def _kept(history: list[dict]) -> list[dict]:
    return [row for row in history if row["verdict"] == "kept"]


def optuna_proposals(
    scenes: list[str], count: int, history: list[dict], varied: tuple, seed: int
) -> dict:
    """`count` runs asked of a TPE study told every kept run's criticality."""
    # optuna is not a workspace dependency: run with `uv run --with optuna`.
    import optuna

    optuna.logging.set_verbosity(optuna.logging.WARNING)
    space = {
        "scene_id": optuna.distributions.CategoricalDistribution(scenes),
        **{
            knob: optuna.distributions.CategoricalDistribution(SCENARIO[knob])
            for knob in varied
        },
    }
    sampler = optuna.samplers.TPESampler(seed=seed * 1000 + len(history))
    study = optuna.create_study(direction="maximize", sampler=sampler)
    kept = _kept(history)
    study.add_trials(
        [
            optuna.trial.create_trial(
                params={name: row[name] for name in space},
                distributions=space,
                value=row["criticality"],
            )
            for row in kept
        ]
    )
    trials = [study.ask(space) for _ in range(count)]
    return {
        "plan": f"optuna: TPE over the scene and {', '.join(varied)}, "
        f"told {len(kept)} kept runs",
        "runs": [{**trial.params, "why": "optuna"} for trial in trials],
    }


def _parent(kept: list[dict], rng: random.Random) -> dict:
    """The most critical of TOURNAMENT kept runs drawn at random."""
    entrants = rng.sample(kept, min(TOURNAMENT, len(kept)))
    return max(entrants, key=lambda row: row["criticality"])


def _mutate(name: str, value, scenes: list[str], rng: random.Random):
    """Another scene, or a legal value next to `value`."""
    if name == "scene_id":
        return rng.choice([scene for scene in scenes if scene != value])
    values = SCENARIO[name]
    index = values.index(value)
    neighbours = [values[i] for i in (index - 1, index + 1) if 0 <= i < len(values)]
    return rng.choice(neighbours)


def ga_proposals(
    scenes: list[str], count: int, history: list[dict], varied: tuple, seed: int
) -> dict:
    """`count` children of the kept runs. Until two runs are kept there is
    nothing to breed, and the round is a Latin hypercube instead."""
    kept = _kept(history)
    if len(kept) < 2:
        return lhs_proposals(scenes, count, len(history), varied, seed)
    rng = random.Random(seed * 1000 + len(history))
    genes = ("scene_id", *varied) if len(scenes) > 1 else varied
    runs = []
    for _ in range(count):
        mother, father = _parent(kept, rng), _parent(kept, rng)
        child = {
            name: rng.choice((mother, father))[name] for name in ("scene_id", *varied)
        }
        for name in genes:
            if rng.random() < 1 / len(genes):
                child[name] = _mutate(name, child[name], scenes, rng)
        runs.append({**child, "why": "ga"})
    return {
        "plan": f"ga: {count} children of {len(kept)} kept runs, by criticality",
        "runs": runs,
    }
