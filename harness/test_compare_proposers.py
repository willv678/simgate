"""compare_proposers.py: the goal's progress replayed run by run."""

from compare_proposers import progress

DELAY = ("planner_delay_us",)


def _run(scene, delay, failed, i):
    return {
        "run": f"r{i}",
        "scene_id": scene,
        "planner_delay_us": delay,
        "verdict": "kept",
        "failed": failed,
        "criticality": 1.0 if failed else 0.0,
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
