"""The outer loop queues only legal runs, and the random proposer is legal."""

import random

import pytest
from knobs import DELAYS_US, rejection, run_config
from outer import random_proposals

SCENES = {"clipgt-a", "clipgt-b"}


def _run(**change):
    return {"scene_id": "clipgt-a", "planner_delay_us": 100_000, "why": "x", **change}


def test_a_legal_run_is_queued_with_the_inner_loops_settings():
    assert rejection(_run(), SCENES) is None
    config = run_config("clipgt-a", 100_000)
    assert config["planner_delay_us"] == 100_000
    assert config["context_length"] == 8


@pytest.mark.parametrize(
    "proposed",
    [
        _run(scene_id="clipgt-z"),  # not a candidate
        _run(planner_delay_us=75_000),  # off the grid
        _run(planner_delay_us=450_000),  # beyond the range
        _run(planner_delay_us=True),  # a bool is not a delay
        _run(planner_delay_us="100000"),
        {**_run(), "context_length": 1},  # an execution setting
        {"scene_id": "clipgt-a", "planner_delay_us": 0},  # no reason given
    ],
)
def test_illegal_runs_are_dropped(proposed):
    assert rejection(proposed, SCENES)


def test_random_proposals_are_legal():
    answer = random_proposals(sorted(SCENES), 50, random.Random(0))
    assert len(answer["runs"]) == 50
    assert all(rejection(run, SCENES) is None for run in answer["runs"])
    assert {run["planner_delay_us"] for run in answer["runs"]} <= set(DELAYS_US)
