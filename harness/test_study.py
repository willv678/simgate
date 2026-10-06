"""study.py: a plan runs only within the catalog and budget; the report's
counts come from the kept runs."""

import pytest
from study import MAX_RUNS, plan_problems, results

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
        },
        {
            "run": "s_002",
            "scene_id": "clipgt-a",
            "planner_delay_us": 0,
            "verdict": "kept",
            "failed": True,
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
        },
    ]
    table = results(rows, ("planner_delay_us",))
    assert [(r["id"], r["runs"], r["failed"]) for r in table] == [
        ("S1", 2, 1),
        ("S2", 1, 1),
    ]
    assert table[0]["run_names"] == ["s_001", "s_002"]
