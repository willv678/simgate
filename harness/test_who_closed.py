"""who_closed.py: which first contacts the replayed actor closed."""

from who_closed import actor_closed


def _contact(ego, actor, toward, width=2.11):
    return {
        "ego_closing_mps": ego,
        "actor_closing_mps": actor,
        "toward_actor_m": toward,
        "ego_width_m": width,
    }


def test_a_car_running_into_a_braking_ego_in_its_lane_is_the_actors():
    # cut_in_merge_2hz_rules_v3_014: ego pulling away, replayed car at 16 m/s.
    assert actor_closed(_contact(-6.2, 16.5, 0.1))


def test_a_head_on_after_drifting_into_oncoming_traffic_is_the_egos():
    # pedestrian_ego_speed_rules_007: both closing, the oncoming car faster.
    assert not actor_closed(_contact(10.2, 17.6, 0.3))


def test_an_ego_over_the_lane_line_is_in_the_passing_cars_lane():
    # 2.11 m wide in a 3.6 m lane: 0.75 m to the line; 0.85 m is over it,
    # though not in a 3.9 m lane (0.9 m to the line).
    assert not actor_closed(_contact(-6.1, 11.7, 0.85))
    assert actor_closed(_contact(-6.1, 11.7, 0.85), lane_m=3.9)


def test_an_ego_stopped_in_the_next_lane_is_out_of_its_own():
    # pedestrian_ego_speed_2hz_015: the ego 7.9 m off its path, away from
    # the car that came into it.
    assert not actor_closed(_contact(-0.1, 6.9, -7.9))


def test_a_parked_or_slower_actor_never_closed_the_gap():
    assert not actor_closed(_contact(-0.5, 0.3, 0.0))
