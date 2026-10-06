"""What the outer loop may propose: each knob typed, with its legal values.

A knob is either a scenario variable (what a study varies and measures) or an
execution setting (how a run executes, fixed here and changed only by a
recovery in the inner loop). The outer loop proposes scenario knobs only;
every proposed run is checked here before it is queued, as the inner loop's
validator checks a recovery.

Only knobs the inner loop can apply and verify are listed: the scene, and the
planner delay, which postflight checks twice (the resolved config, and the age
of the plan the controller got, physics.py).
"""

SCENE_FILE = "data/scenes/sim_scenes.csv"
DELAYS_US = tuple(range(0, 400_001, 50_000))
EXECUTION = {"context_length": 8, "scene_file": SCENE_FILE, "trafficsim_device": "cpu"}
PROPOSED_KEYS = {"scene_id", "planner_delay_us", "why"}


def run_config(scene_id: str, planner_delay_us: int) -> dict:
    return {**EXECUTION, "scene_id": scene_id, "planner_delay_us": planner_delay_us}


def rejection(proposed: dict, scenes: set[str]) -> str | None:
    """Why a proposed run may not be queued, or None. `scenes` is the study's
    candidate set: scenes of the catalog that are downloaded locally."""
    if set(proposed) != PROPOSED_KEYS:
        return f"keys must be {sorted(PROPOSED_KEYS)}, got {sorted(proposed)}"
    if proposed["scene_id"] not in scenes:
        return f"scene {proposed['scene_id']!r} is not a candidate of this study"
    delay = proposed["planner_delay_us"]
    if type(delay) is not int or delay not in DELAYS_US:
        return f"planner_delay_us {delay!r} is not one of {list(DELAYS_US)}"
    return None
