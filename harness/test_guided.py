"""guided.py: the rules confirm near-failures, step from the most critical
setting, and keep a hybrid proposer to their candidates."""

from guided import candidates, outside, rules_proposals, with_confirmation
from knobs import rejection
from outer import results

DELAY = ("planner_delay_us",)
SCENES = ["clipgt-a", "clipgt-b"]
TOP3 = {"type": "top_k", "k": 3, "high_min": 0.5, "distinct_scenes": True}


def _runs(scene, delay, failed, passed, near=0.0, start=0):
    rows = [{"failed": True, "criticality": 1.0}] * failed + [
        {"failed": False, "criticality": near}
    ] * passed
    return [
        {
            "run": f"{scene}_{delay}_{start + i}",
            "scene_id": scene,
            "planner_delay_us": delay,
            "verdict": "kept",
            **row,
        }
        for i, row in enumerate(rows)
    ]


def test_an_untried_scene_gets_a_first_probe_in_the_middle():
    found = candidates(SCENES, [], TOP3, DELAY)
    assert {(c["scene_id"], c["planner_delay_us"]) for c in found} == {
        ("clipgt-a", 200_000),
        ("clipgt-b", 200_000),
    }


def test_a_single_failure_is_confirmed_before_anything_else():
    table = results(_runs("clipgt-a", 200_000, 1, 0), DELAY)
    found = candidates(["clipgt-a"], table, TOP3, DELAY)
    assert found[0]["planner_delay_us"] == 200_000
    assert found[0]["reason"].startswith("confirm")
    assert {c["planner_delay_us"] for c in found[1:]} == {150_000, 250_000}


def test_a_scene_confirmed_challenging_is_left_alone():
    table = results(_runs("clipgt-a", 200_000, 5, 0), DELAY)
    found = candidates(SCENES, table, TOP3, DELAY)
    assert {c["scene_id"] for c in found} == {"clipgt-b"}


def test_rules_spread_a_round_over_scenes_and_stay_legal():
    table = results(_runs("clipgt-a", 200_000, 1, 0), DELAY)
    answer = rules_proposals(SCENES, 6, table, TOP3, DELAY)
    assert len(answer["runs"]) == 6
    assert {r["scene_id"] for r in answer["runs"][:2]} == set(SCENES)
    assert all(rejection(r, set(SCENES), DELAY) is None for r in answer["runs"])


def test_a_hybrid_proposal_outside_the_candidates_is_dropped():
    ranked = candidates(SCENES, [], TOP3, DELAY)
    inside = {"scene_id": "clipgt-a", "planner_delay_us": 200_000, "why": "x"}
    assert outside(inside, ranked, DELAY) is None
    assert outside({**inside, "planner_delay_us": 400_000}, ranked, DELAY)


def _explore(n):
    return {
        "plan": "explore",
        "runs": [{"scene_id": "clipgt-b", "planner_delay_us": 0, "why": "random"}] * n,
    }


def test_confirmation_takes_at_most_half_a_round_and_exploration_the_rest():
    table = results(
        _runs("clipgt-a", 200_000, 1, 0) + _runs("clipgt-b", 100_000, 1, 0), DELAY
    )
    answer = with_confirmation(SCENES, 3, table, TOP3, DELAY, _explore)
    # Two near-failures to confirm, but a round of 3 gives them only 1 run.
    assert answer["runs"][0]["why"].startswith("confirm")
    assert [r["why"] for r in answer["runs"][1:]] == ["random", "random"]
    assert answer["plan"] == "1 confirmations; explore"


def test_without_near_failures_the_whole_round_explores():
    table = results(_runs("clipgt-a", 200_000, 0, 2), DELAY)
    answer = with_confirmation(SCENES, 4, table, TOP3, DELAY, _explore)
    assert [r["why"] for r in answer["runs"]] == ["random"] * 4
