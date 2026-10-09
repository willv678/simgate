"""Rule-guided search: the candidate runs a round may choose from.

Each round, rules turn the kept runs so far into a ranked list of candidate
runs. The `rules` proposer takes the best of them in order, no model; the
`hybrid` proposer shows them to Claude, which may choose only among them (any
other run is dropped before it is queued). Claude decides the order and the
mix; the rules decide what is legal to try, so the search cannot wander off.

The rules, per scene:
- bracket goal: the next bisection probe (baselines.next_probe);
- otherwise, from the scene's most critical setting so far (outer.criticality):
  repeat it until its failure rate is surely above the goal's `high_min`
  (confirm), and step each varied knob one notch either way from it
  (escalate, or back off to find the edge); a scene never tried gets its first
  probe at the middle of every knob's range;
- a scene already confirmed challenging is left alone when a top_k goal wants
  distinct scenes.
Scores: confirming a near-failure first, then steps from the most critical
settings, then first probes.

With `settle` (rules_v2), a setting whose failure rate is surely below the
goal's `high_min` (the top of its 90% range below it) is never confirmed:
without it a near miss that never fails is confirmed until the budget runs
out (lead vehicle, 9 Oct: every round after the first went to confirming the
middle probes, 0 failures in 38 runs), since a rate of 0 is never surely
above high_min. Such a scene also gets its corners.

With `corners`, a scene whose settings so far are all far from failing
(criticality below CORNER_BELOW) also offers its untried corners, every knob
at an end of its range (as Euro NCAP grids test the extremes), scored after
every untried scene's first probe and before small steps from a weak
setting: one-notch steps from the middle never reach a failure that needs an
extreme value within a study's budget (FACTS, random + confirmation).

`with_confirmation` gives any other proposer the same confirmation rule: up to
half of a round repeats the near-failures the rules would confirm, and the
proposer picks the rest. `random_confirm` is random search with it, the fair
baseline for a top_k goal, which counts only confirmed settings.
"""

from itertools import product

from baselines import next_probe
from goals import goal_cells
from knobs import SCENARIO, UNVARIED

DEFAULT_HIGH_MIN = 0.5
CONFIRM = "confirm "
CORNER_BELOW = 0.5
CORNER_SCORE = 0.25


def _key(run: dict, varied: tuple) -> tuple:
    return (run["scene_id"], *(run[knob] for knob in varied))


def _setting(
    scene: str, values: dict, varied: tuple, reason: str, score: float
) -> dict:
    return {
        "scene_id": scene,
        **{knob: values[knob] for knob in varied},
        "reason": reason,
        "score": round(score, 3),
    }


def _neighbours(values: dict, varied: tuple) -> list[dict]:
    found = []
    for knob in varied:
        grid = SCENARIO[knob]
        index = grid.index(values[knob])
        for step in (-1, 1):
            if 0 <= index + step < len(grid):
                found.append({**values, knob: grid[index + step]})
    return found


def candidates(
    scenes: list[str],
    table: list[dict],
    goal: dict | None,
    varied: tuple,
    corners: bool = False,
    settle: bool = False,
) -> list[dict]:
    """Ranked candidate runs, best first, each with its reason and score."""
    if goal is not None and goal["type"] == "bracket":
        cells = goal_cells(table, goal["knob"], varied)
        found = []
        for scene in scenes:
            value = next_probe(scene, cells, goal)
            if value is not None:
                values = {**{k: UNVARIED[k] for k in varied}, goal["knob"]: value}
                found.append(
                    _setting(scene, values, varied, "next bisection probe", 1.0)
                )
        return found

    high_min = goal["high_min"] if goal and "high_min" in goal else DEFAULT_HIGH_MIN
    distinct = bool(goal and goal["type"] == "top_k" and goal["distinct_scenes"])
    tried = {}
    for row in table:
        tried.setdefault(row["scene_id"], []).append(row)
    found = []
    for scene in scenes:
        rows = tried.get(scene, [])
        if not rows:
            middle = {k: SCENARIO[k][len(SCENARIO[k]) // 2] for k in varied}
            found.append(
                _setting(
                    scene, middle, varied, "first probe, middle of every knob", 0.3
                )
            )
            continue
        if distinct and any(r["failure_rate_90"][0] > high_min for r in rows):
            continue
        best = max(rows, key=lambda r: (r["criticality"], r["failure_rate_90"][0]))
        values = {k: best[k] for k in varied}
        settled_low = settle and best["failure_rate_90"][1] < high_min
        if (
            best["criticality"] >= 0.5
            and best["failure_rate_90"][0] <= high_min
            and not settled_low
        ):
            found.append(
                _setting(
                    scene,
                    values,
                    varied,
                    f"{CONFIRM}{best['id']}: near failure, not yet sure",
                    0.6 + 0.4 * best["criticality"],
                )
            )
        seen = {_key(r, varied) for r in rows}
        if corners and (best["criticality"] < CORNER_BELOW or settled_low):
            for ends in product(*((SCENARIO[k][0], SCENARIO[k][-1]) for k in varied)):
                corner = dict(zip(varied, ends))
                if (scene, *ends) not in seen:
                    found.append(
                        _setting(
                            scene,
                            corner,
                            varied,
                            "a corner: the scene is far from failing so far"
                            if not settled_low
                            else "a corner: its nearest miss surely fails rarely",
                            CORNER_SCORE,
                        )
                    )
        for step in _neighbours(values, varied):
            if (scene, *(step[k] for k in varied)) not in seen:
                found.append(
                    _setting(
                        scene,
                        step,
                        varied,
                        f"one notch from {best['id']}, the scene's most critical",
                        0.1 + 0.5 * best["criticality"],
                    )
                )
    found.sort(key=lambda c: -c["score"])
    return found


def rules_proposals(
    scenes: list[str],
    count: int,
    table: list[dict],
    goal: dict | None,
    varied: tuple,
    corners: bool = False,
    settle: bool = False,
) -> dict:
    """The best `count` candidates, one scene at a time in turn so no scene
    takes the whole round; candidates repeat when there are too few."""
    ranked = candidates(scenes, table, goal, varied, corners, settle)
    if not ranked:
        return {"plan": "rules: nothing left to try", "runs": []}
    by_scene = {}
    for c in ranked:
        by_scene.setdefault(c["scene_id"], []).append(c)
    order = []
    while len(order) < len(ranked):
        for queue in by_scene.values():
            if queue:
                order.append(queue.pop(0))
    picks = [order[i % len(order)] for i in range(count)]
    return {
        "plan": f"rules: {len(ranked)} candidates",
        "runs": [
            {**{k: c[k] for k in ("scene_id", *varied)}, "why": c["reason"]}
            for c in picks
        ],
    }


def with_confirmation(
    scenes: list[str],
    count: int,
    table: list[dict],
    goal: dict | None,
    varied: tuple,
    explore,
) -> dict:
    """At most half the round confirms the rules' near-failures, best first;
    `explore(n)` (a proposer's answer for n runs) fills the rest."""
    confirm = [
        c
        for c in candidates(scenes, table, goal, varied)
        if c["reason"].startswith(CONFIRM)
    ][: count // 2]
    rest = explore(count - len(confirm))
    return {
        "plan": f"{len(confirm)} confirmations; {rest['plan']}",
        "runs": [
            {**{k: c[k] for k in ("scene_id", *varied)}, "why": c["reason"]}
            for c in confirm
        ]
        + rest["runs"],
    }


def outside(run: dict, ranked: list[dict], varied: tuple) -> str | None:
    """Why a hybrid proposal is not among the round's candidates, or None."""
    if _key(run, varied) in {_key(c, varied) for c in ranked}:
        return None
    return "not one of this round's rule candidates"
