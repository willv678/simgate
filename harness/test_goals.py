"""goals.py: a goal is met only when the 90% ranges say so."""

import pytest
from goals import goal_problems, goal_status
from outer import results

DELAY = ("planner_delay_us",)
SCENES = {"clipgt-a", "clipgt-b"}


def _runs(scene, delay, failed, passed, start=0):
    rows = [{"failed": True, "criticality": 1.0}] * failed + [
        {"failed": False, "criticality": 0.0}
    ] * passed
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
    "max_gap": 50_000,
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
    # Too far apart to say where it breaks.
    far = _runs("clipgt-a", 0, 0, 5), _runs("clipgt-a", 400_000, 5, 0, 10)
    assert not _status(BRACKET, *far)["met"]
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
        {**BRACKET, "max_gap": 10_000},  # finer than the knob's steps
    ],
)
def test_goals_that_cannot_be_checked_are_rejected(goal):
    assert goal_problems(goal, SCENES, DELAY)


def test_bisection_probes_the_middle_then_repeats_until_classified():
    from baselines import next_probe
    from goals import goal_cells

    goal = {**BRACKET}
    cells = lambda *groups: goal_cells(
        results([r for g in groups for r in g], DELAY), "planner_delay_us", DELAY
    )
    assert next_probe("clipgt-a", cells(), goal) == 200_000  # middle of 0-400 ms
    # One failure at 200 ms is not yet surely high: probe it again.
    assert (
        next_probe("clipgt-a", cells(_runs("clipgt-a", 200_000, 1, 0)), goal) == 200_000
    )
    # Surely high at 200 ms: search below it.
    high = _runs("clipgt-a", 200_000, 5, 0)
    assert next_probe("clipgt-a", cells(high), goal) == 100_000
    # Surely low at 100 ms and surely high at 200 ms: probe 150 ms.
    low = _runs("clipgt-a", 100_000, 0, 5, 20)
    assert next_probe("clipgt-a", cells(high, low), goal) == 150_000
    # Settled once 150 ms is surely low or surely high.
    assert (
        next_probe(
            "clipgt-a", cells(high, low, _runs("clipgt-a", 150_000, 5, 0, 40)), goal
        )
        is None
    )


def test_grid_sweeps_every_scene_at_every_value_in_order():
    from baselines import grid_proposals
    from knobs import DELAYS_US

    first = grid_proposals(["clipgt-a", "clipgt-b"], 4, 0, BRACKET, DELAY)["runs"]
    assert [(r["scene_id"], r["planner_delay_us"]) for r in first] == [
        ("clipgt-a", 0),
        ("clipgt-b", 0),
        ("clipgt-a", 50_000),
        ("clipgt-b", 50_000),
    ]
    wrap = grid_proposals(["clipgt-a"], 1, len(DELAYS_US), BRACKET, DELAY)["runs"]
    assert wrap[0]["planner_delay_us"] == 0


def test_top_k_counts_settings_surely_failing_one_per_scene():
    top2 = {"type": "top_k", "k": 2, "high_min": 0.5, "distinct_scenes": True}
    same_scene = _status(
        top2, _runs("clipgt-a", 100_000, 5, 0), _runs("clipgt-a", 150_000, 5, 0, 10)
    )
    assert not same_scene["met"]  # two settings, but one scene
    two_scenes = _status(
        top2, _runs("clipgt-a", 100_000, 5, 0), _runs("clipgt-b", 150_000, 5, 0, 10)
    )
    assert two_scenes["met"] and len(two_scenes["settings"]) == 2
    unsure = _status(
        top2, _runs("clipgt-a", 100_000, 1, 0), _runs("clipgt-b", 150_000, 1, 0, 10)
    )
    assert not unsure["met"]  # single failures are not yet sure


def test_grid_over_several_knobs_uses_three_levels_each():
    from baselines import grid_proposals
    from knobs import rejection

    both = ("actor_time_shift_s", "actor_speed_scale")
    runs = grid_proposals(["clipgt-a"], 9, 0, None, both)["runs"]
    assert {(r["actor_time_shift_s"], r["actor_speed_scale"]) for r in runs} == {
        (shift, speed) for shift in (-2.0, 0.0, 2.0) for speed in (0.5, 1.25, 2.0)
    }
    assert all(rejection(r, {"clipgt-a"}, both) is None for r in runs)


AB = {"a": "linear", "b": "nonlinear"}


def _pairs(scene, delay, outcomes, start=0):
    """Kept runs of an A/B study: one linear and one nonlinear run per
    (linear failed, nonlinear failed) outcome."""
    return [
        {
            "run": f"r{start + i}_{controller}",
            "scene_id": scene,
            "planner_delay_us": delay,
            "controller": controller,
            "verdict": "kept",
            "failed": failed,
            "criticality": 1.0 if failed else 0.0,
        }
        for i, outcome in enumerate(outcomes)
        for controller, failed in zip(("linear", "nonlinear"), outcome)
    ]


def _compare(*groups):
    rows = [row for group in groups for row in group]
    return goal_status({"type": "compare"}, results(rows, DELAY, AB), DELAY)


def test_an_ab_table_shows_both_controllers_per_setting():
    rows = _pairs("clipgt-a", 0, [(True, False), (True, True)])
    rows.append({**rows[0], "run": "unpaired_linear"})  # its partner not kept
    (row,) = results(rows, DELAY, AB)
    assert (row["a"]["controller"], row["a"]["runs"], row["a"]["failed"]) == (
        "linear",
        3,
        3,
    )
    assert (row["b"]["controller"], row["b"]["runs"], row["b"]["failed"]) == (
        "nonlinear",
        2,
        1,
    )
    assert row["paired"] == {
        "pairs": 2,
        "a_failed": 2,
        "b_failed": 1,
        "only_a_failed": 1,
        "only_b_failed": 0,
    }


def test_compare_shows_no_difference_while_the_pooled_ranges_overlap():
    status = _compare(_pairs("clipgt-a", 0, [(True, False), (False, False)]))
    assert not status["met"]
    assert status["verdict"].startswith("no difference shown")
    assert status["sign_test"] == {"only_a_failed": 1, "only_b_failed": 0, "p": 1.0}


def test_compare_is_met_once_the_pooled_ranges_separate_over_enough_settings():
    status = _compare(
        _pairs("clipgt-a", 0, [(True, False)] * 4 + [(False, False)]),
        _pairs("clipgt-b", 100_000, [(True, False)] * 4 + [(True, True)], 10),
        _pairs("clipgt-b", 200_000, [(True, False)], 20),
    )
    assert status["met"]
    assert status["verdict"].startswith("nonlinear fails less than linear")
    assert (
        status["pooled"]["a"]["failed"] == 10 and status["pooled"]["b"]["failed"] == 1
    )
    assert status["sign_test"] == {"only_a_failed": 9, "only_b_failed": 0, "p": 0.004}
    assert status["coverage"] == {"knob_settings": 3, "scenes": 2}


def test_compare_is_not_met_by_a_difference_at_one_setting():
    # The 8 Oct A/B stopped after one round: every pair at one knob setting.
    status = _compare(
        *(
            _pairs(scene, 0, [(False, True)] * 2, 10 * i)
            for i, scene in enumerate(["clipgt-a", "clipgt-b", "clipgt-c"])
        )
    )
    assert not status["met"]
    assert "only over 1 knob settings on 3 scenes" in status["verdict"]


def test_the_sign_test_is_exact_and_two_sided():
    from goals import sign_test

    assert sign_test(0, 0) == 1.0
    assert sign_test(8, 0) == sign_test(0, 8) == 2 / 2**8
    assert sign_test(6, 1) == 2 * (1 + 7) / 2**7
    assert sign_test(5, 5) == 1.0


def test_a_compare_goal_has_only_its_type():
    assert goal_problems({"type": "compare"}, SCENES, DELAY) == []
    assert goal_problems({"type": "compare", "knob": "x"}, SCENES, DELAY)
