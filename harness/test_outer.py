"""The outer loop queues only legal runs, and the random proposer is legal."""

import random

import pytest
from knobs import SCENARIO, rejection, run_config
from outer import random_proposals

SCENES = {"clipgt-a", "clipgt-b"}
DELAY = ("planner_delay_us",)
BOTH = ("planner_delay_us", "lateral_bias_m")


def _run(**change):
    return {"scene_id": "clipgt-a", "planner_delay_us": 100_000, "why": "x", **change}


def test_a_legal_run_is_queued_with_the_inner_loops_settings():
    assert rejection(_run(), SCENES, DELAY) is None
    config = run_config("clipgt-a", {"planner_delay_us": 100_000}, {})
    assert config["planner_delay_us"] == 100_000
    assert config["lateral_bias_m"] == 0.0
    assert config["context_length"] == 8
    assert rejection(_run(lateral_bias_m=-0.3), SCENES, BOTH) is None


@pytest.mark.parametrize(
    "proposed,varied",
    [
        (_run(scene_id="clipgt-z"), DELAY),  # not a candidate
        (_run(planner_delay_us=75_000), DELAY),  # off the grid
        (_run(planner_delay_us=450_000), DELAY),  # beyond the range
        (_run(planner_delay_us=True), DELAY),  # a bool is not a delay
        (_run(planner_delay_us=100_000.0), DELAY),  # a delay is a whole number
        (_run(planner_delay_us="100000"), DELAY),
        ({**_run(), "context_length": 1}, DELAY),  # an execution setting
        ({"scene_id": "clipgt-a", "planner_delay_us": 0}, DELAY),  # no reason
        (_run(lateral_bias_m=0.3), DELAY),  # a knob the study does not vary
        (_run(), BOTH),  # a varied knob left out
        (_run(lateral_bias_m=0.25), BOTH),  # off the grid
    ],
)
def test_illegal_runs_are_dropped(proposed, varied):
    assert rejection(proposed, SCENES, varied)


@pytest.mark.parametrize("varied", [DELAY, BOTH])
def test_random_proposals_are_legal(varied):
    answer = random_proposals(sorted(SCENES), 50, varied, random.Random(0))
    assert len(answer["runs"]) == 50
    assert all(rejection(run, SCENES, varied) is None for run in answer["runs"])
    for knob in varied:
        assert {run[knob] for run in answer["runs"]} <= set(SCENARIO[knob])
