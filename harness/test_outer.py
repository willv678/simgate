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
    config = run_config("clipgt-a", {"planner_delay_us": 100_000}, {}, "linear")
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


def _study(tmp_path, proposer, **fixed):
    from outer import Study

    return Study(
        name="ab",
        queue=tmp_path / "queue",
        trace=tmp_path / "trace.jsonl",
        rounds_file=tmp_path / "rounds.jsonl",
        objective="o",
        candidates=[{"scene_id": scene} for scene in sorted(SCENES)],
        varied=DELAY,
        rounds=2,
        per_round=3,
        proposer=proposer,
        goal={"type": "compare"} if "compare" in fixed else None,
        goal_file=tmp_path / "goal.json",
        fixed={"traffic": "catk", **fixed},
    )


@pytest.mark.parametrize("proposer", ["random", "grid", "rules", "lhs"])
def test_an_ab_study_queues_each_setting_once_per_controller(
    tmp_path, monkeypatch, proposer
):
    import outer
    from read_state import load_entry, queue_entries

    monkeypatch.setattr(outer, "run_inner_loop", lambda study: None)
    study = _study(tmp_path, proposer, compare={"a": "linear", "b": "nonlinear"})
    outer.run_study(study)
    entries = [load_entry(path) for path in queue_entries(study.queue)]
    assert len(entries) == 2 * study.rounds * study.per_round
    for a, b in zip(entries[::2], entries[1::2]):
        assert (a["config"]["controller"], b["config"]["controller"]) == (
            "linear",
            "nonlinear",
        )
        assert a["name"].removesuffix("_linear") == b["name"].removesuffix("_nonlinear")
        same = {k: v for k, v in a["config"].items() if k != "controller"}
        assert same == {k: v for k, v in b["config"].items() if k != "controller"}
    assert entries[-1]["name"] == "ab_006_nonlinear"


def test_a_study_without_compare_queues_one_linear_run_per_setting(
    tmp_path, monkeypatch
):
    import outer
    from read_state import load_entry, queue_entries

    monkeypatch.setattr(outer, "run_inner_loop", lambda study: None)
    study = _study(tmp_path, "random")
    outer.run_study(study)
    entries = [load_entry(path) for path in queue_entries(study.queue)]
    assert [e["name"] for e in entries] == [f"ab_{i:03d}" for i in range(1, 7)]
    assert {e["config"]["controller"] for e in entries} == {"linear"}


@pytest.mark.parametrize("varied", [DELAY, BOTH])
def test_random_proposals_are_legal(varied):
    answer = random_proposals(sorted(SCENES), 50, varied, random.Random(0))
    assert len(answer["runs"]) == 50
    assert all(rejection(run, SCENES, varied) is None for run in answer["runs"])
    for knob in varied:
        assert {run[knob] for run in answer["runs"]} <= set(SCENARIO[knob])
