"""compare_proposers.py: the goal's progress replayed run by run."""

from compare_proposers import arms, hardest, progress, proposer_of

DELAY = ("planner_delay_us",)


def _run(scene, delay, failed, i, criticality=None):
    return {
        "run": f"r{i}",
        "scene_id": scene,
        "planner_delay_us": delay,
        "verdict": "kept",
        "failed": failed,
        "criticality": criticality if criticality is not None else float(failed),
    }


def test_top_k_progress_counts_settings_as_they_are_confirmed():
    goal = {"type": "top_k", "k": 2, "high_min": 0.5, "distinct_scenes": True}
    runs = [_run("clipgt-a", 0, True, i) for i in range(3)] + [
        _run("clipgt-b", 0, True, 10 + i) for i in range(3)
    ]
    counts = progress(goal, runs, DELAY, None)
    assert counts[0] == 0  # one failure is not yet sure
    assert counts[2] == 1  # three of three at 90%: surely above 0.5
    assert counts[-1] == 2


def test_hardest_ranks_near_misses_by_scene_when_nothing_fails():
    runs = [
        _run("clipgt-a", 0, False, 1, 0.2),
        _run("clipgt-a", 100, False, 2, 0.6),
        _run("clipgt-a", 100, False, 3, 0.4),  # that setting now averages 0.5
        _run("clipgt-b", 0, False, 4, 0.3),
    ]
    assert hardest(runs, DELAY, 2) == [0.1, 0.3, 0.25, 0.4]


def test_arms_finds_every_proposer_and_replicate(tmp_path):
    for folder in [
        "",
        "rules",
        "rules_r2",
        "llm_r3",
        "random_confirm",
        "random",
        "x_r2",
    ]:
        (tmp_path / folder).mkdir(exist_ok=True)
        (tmp_path / folder / "rounds.jsonl").write_text("")
    assert set(arms(tmp_path)) == {
        "llm", "llm_r3", "rules", "rules_r2", "random", "random_confirm"
    }  # fmt: skip
    assert proposer_of("rules_r2") == "rules"
    assert proposer_of("random_confirm") == "random_confirm"
