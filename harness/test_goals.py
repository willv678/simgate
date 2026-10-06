"""goals.py: a goal is met only when the 90% ranges say so."""

import pytest
from goals import goal_problems, goal_status
from outer import results

DELAY = ("planner_delay_us",)
SCENES = {"clipgt-a", "clipgt-b"}


def _runs(scene, delay, failed, passed, start=0):
    rows = [{"failed": True}] * failed + [{"failed": False}] * passed
    return [
        {
            "run": f"r{start + i}",
            "scene_id": scene,
            "planner_delay_us": delay,
            "verdict": "kept",
            **row,
        }
        for i, row in enumerate(rows)
    ]


def _status(goal, *groups):
    rows = [row for group in groups for row in group]
    return goal_status(goal, results(rows, DELAY), DELAY)


SEPARATE = {
    "type": "separate",
    "scene": "clipgt-a",
    "knob": "planner_delay_us",
    "low": 100_000,
    "high": 150_000,
}
BRACKET = {
    "type": "bracket",
    "scenes": ["clipgt-a"],
    "knob": "planner_delay_us",
    "low_max": 0.4,
    "high_min": 0.6,
}


def test_separate_is_open_while_the_ranges_overlap():
    # The pilot: 0 of 2 at 100 ms, 2 of 2 at 150 ms; 0-58% and 42-100% overlap.
    status = _status(
        SEPARATE, _runs("clipgt-a", 100_000, 0, 2), _runs("clipgt-a", 150_000, 2, 0, 10)
    )
    assert not status["met"]


def test_separate_is_met_once_they_separate():
    status = _status(
        SEPARATE, _runs("clipgt-a", 100_000, 0, 5), _runs("clipgt-a", 150_000, 5, 0, 10)
    )
    assert status["met"] and status["verdict"].startswith("confirmed")


def test_bracket_needs_a_surely_low_and_a_larger_surely_high_value():
    low, high = _runs("clipgt-a", 100_000, 0, 5), _runs("clipgt-a", 150_000, 5, 0, 10)
    assert _status(BRACKET, low, high)["met"]
    assert not _status(BRACKET, low)["met"]
    # Surely low at a value below the largest legal one settles nothing.
    assert not _status(BRACKET, _runs("clipgt-a", 0, 0, 9))["met"]
    assert _status(BRACKET, _runs("clipgt-a", 400_000, 0, 9))[
        "met"
    ]  # never breaks in range


def test_bracket_reads_only_runs_with_other_knobs_unvaried():
    both = ("planner_delay_us", "lateral_bias_m")
    rows = [
        {**row, "lateral_bias_m": 0.3}
        for row in _runs("clipgt-a", 100_000, 0, 5)
        + _runs("clipgt-a", 150_000, 5, 0, 10)
    ]
    goal = {**BRACKET}
    assert not goal_status(goal, results(rows, both), both)["met"]


@pytest.mark.parametrize(
    "goal",
    [
        {"type": "maximise"},
        {**SEPARATE, "scene": "clipgt-z"},
        {**SEPARATE, "low": 150_000, "high": 100_000},
        {**SEPARATE, "high": 125_000},  # not a legal delay
        {**SEPARATE, "knob": "lateral_bias_m"},  # not varied
        {**SEPARATE, "extra": 1},
        {**BRACKET, "low_max": 0.6},
        {**BRACKET, "scenes": []},
    ],
)
def test_goals_that_cannot_be_checked_are_rejected(goal):
    assert goal_problems(goal, SCENES, DELAY)
