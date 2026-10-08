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
        "fixed": {"traffic": "catk"},
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
        {"vary": ["actor_time_shift_s"]},  # actor knobs need replay and a class
        {"vary": ["actor_time_shift_s"], "fixed": {"traffic": "replay"}},
    ],
)
def test_a_plan_outside_them_is_rejected(change):
    assert plan_problems(_plan(**change), SCENES)


AB_FIXED = {"traffic": "catk", "compare": {"a": "linear", "b": "nonlinear"}}


def test_an_ab_plan_compares_two_existing_controllers():
    plan = _plan(fixed=AB_FIXED, goal={"type": "compare"})
    assert plan_problems(plan, SCENES) == []


@pytest.mark.parametrize(
    "change",
    [
        {"goal": {"type": "none"}},  # an A/B study needs the compare goal
        {"fixed": {"traffic": "catk"}},  # a compare goal needs two controllers
        {"fixed": {**AB_FIXED, "compare": {"a": "linear", "b": "mpc9000"}}},
        {"fixed": {**AB_FIXED, "compare": {"a": "linear", "b": "linear"}}},
        {"fixed": {**AB_FIXED, "compare": {"a": "linear"}}},
        {"fixed": AB_FIXED, "rounds": 4, "per_round": 10},  # 80 runs in pairs
    ],
)
def test_an_ab_plan_outside_the_catalog_or_budget_is_rejected(change):
    plan = _plan(**{"fixed": AB_FIXED, "goal": {"type": "compare"}, **change})
    assert plan_problems(plan, SCENES)


def test_ab_report_lines_show_both_controllers():
    from study import setting_text

    rows = [
        {
            "run": f"s_{i}_{controller}",
            "scene_id": "clipgt-aaaaaaaa-1",
            "planner_delay_us": 0,
            "controller": controller,
            "verdict": "kept",
            "failed": controller == "linear",
            "criticality": 1.0,
        }
        for i in range(2)
        for controller in ("linear", "nonlinear")
    ]
    (row,) = results(rows, ("planner_delay_us",), AB_FIXED["compare"])
    text = setting_text(row, ("planner_delay_us",))
    assert "linear 2/2 failed" in text and "nonlinear 0/2 failed" in text


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
    from goals import rate_range

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
