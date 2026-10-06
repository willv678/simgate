"""study.py: a plan runs only within the catalog and budget; the report's
counts come from the kept runs."""

import pytest
from outer import results
from study import MAX_RUNS, plan_problems

SCENES = {"clipgt-a", "clipgt-b"}


def _plan(**change):
    plan = {
        "question": "q",
        "objective": "o",
        "vary": ["planner_delay_us"],
        "scenes": ["clipgt-a"],
        "rounds": 3,
        "per_round": 5,
        "rationale": "r",
        "goal": {"type": "none"},
    }
    return {**plan, **change}


def test_a_plan_within_the_catalog_and_budget_runs():
    assert plan_problems(_plan(), SCENES) == []


@pytest.mark.parametrize(
    "change",
    [
        {"vary": []},
        {"vary": ["driver"]},  # not a scenario knob
        {"vary": ["planner_delay_us", "planner_delay_us"]},
        {"scenes": ["clipgt-z"]},
        {"scenes": []},
        {"per_round": 0},
        {"per_round": 11},
        {"rounds": 0},
        {"rounds": MAX_RUNS, "per_round": 2},  # over the run budget
        {"goal": {"type": "separate", "scene": "clipgt-b"}},  # malformed goal
    ],
)
def test_a_plan_outside_them_is_rejected(change):
    assert plan_problems(_plan(**change), SCENES)


def test_results_count_kept_runs_only_per_setting():
    rows = [
        {
            "run": "s_001",
            "scene_id": "clipgt-a",
            "planner_delay_us": 0,
            "verdict": "kept",
            "failed": False,
            "criticality": 0.0,
        },
        {
            "run": "s_002",
            "scene_id": "clipgt-a",
            "planner_delay_us": 0,
            "verdict": "kept",
            "failed": True,
            "criticality": 1.0,
        },
        {
            "run": "s_003",
            "scene_id": "clipgt-a",
            "planner_delay_us": 0,
            "verdict": "quarantined: x",
        },
        {
            "run": "s_004",
            "scene_id": "clipgt-b",
            "planner_delay_us": 100_000,
            "verdict": "kept",
            "failed": True,
            "criticality": 1.0,
        },
    ]
    table = results(rows, ("planner_delay_us",))
    assert [(r["id"], r["runs"], r["failed"]) for r in table] == [
        ("S1", 2, 1),
        ("S2", 1, 1),
    ]
    assert table[0]["run_names"] == ["s_001", "s_002"]


def test_the_failure_rate_range_shrinks_with_runs():
    from outer import rate_range

    low, high = rate_range(2, 2)
    assert 0.3 < low < 0.5 and high == 1.0  # two failures: likely, not certain
    assert rate_range(0, 10)[1] < 0.25
    assert rate_range(10, 20) == (
        round(1 - rate_range(10, 20)[1], 2),
        rate_range(10, 20)[1],
    )
    assert (
        rate_range(4, 8)[1] - rate_range(4, 8)[0]
        > rate_range(40, 80)[1] - rate_range(40, 80)[0]
    )


def test_counts_written_by_hand_are_caught():
    from study import HAND_COUNT

    assert HAND_COUNT.search("it failed 5 of 5 runs at 150 ms")
    assert HAND_COUNT.search("2/2 failed")
    assert not HAND_COUNT.search("every run at 150 ms and above failed (S10, S11)")
