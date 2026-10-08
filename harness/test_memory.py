"""memory.py: a prior run counts only if this study would have run it itself."""

from knobs import run_config
from memory import effective

FIXED = {
    "traffic": "replay",
    "retime_class": "person",
    "retime_tracks": {"clipgt-a": "17"},
}


def test_a_repeat_with_another_seed_is_the_same_setting():
    ours = run_config("clipgt-a", {"actor_time_shift_s": -1.0}, FIXED, "linear")
    theirs = {**ours, "seed": 99}
    assert effective(theirs) == effective(ours)


def test_another_actor_target_or_traffic_mode_is_not():
    ours = run_config("clipgt-a", {"actor_time_shift_s": -1.0}, FIXED, "linear")
    assert effective({**ours, "retime_track": "18"}) != effective(ours)
    assert effective({**ours, "traffic": "catk"}) != effective(ours)
    assert effective({**ours, "controller": "feasible_best"}) != effective(ours)


def test_an_unretimed_run_matches_whatever_actor_it_named():
    ours = run_config("clipgt-a", {}, FIXED, "linear")
    other = run_config("clipgt-a", {}, {"traffic": "replay"}, "linear")
    assert effective(ours) == effective(other)


def test_older_entries_without_new_keys_match_their_defaults():
    old = {
        "context_length": 8,
        "planner_delay_us": 0,
        "scene_file": "data/scenes/sim_scenes.csv",
        "scene_id": "clipgt-a",
        "trafficsim_device": "cpu",
    }
    ours = run_config("clipgt-a", {}, {}, "linear")
    assert effective(old) == effective(ours)
