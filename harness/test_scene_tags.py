"""scene_tags.py: log facts from synthetic tracks, and rule tags from facts."""

import numpy as np
import pytest
from scene_tags import (
    ego_facts,
    lane_change,
    pedestrians_near,
    reference_path,
    rule_tags,
)

T = np.arange(0, 12.05, 0.1)


def _track(xy, label="automobile", t=T):
    xy = np.asarray(xy, dtype=float)
    step = np.gradient(xy, axis=0)
    return {
        "label": label,
        "static": False,
        "t": t,
        "xy": xy,
        "yaw": np.unwrap(np.arctan2(step[:, 1], step[:, 0])),
    }


def _turn(sign):
    """10 m straight, a quarter circle of radius 15 m, then straight."""
    s = 6.0 * T
    bend = 15 * np.pi / 2
    along = np.clip(s - 10, 0, bend) / 15
    x = np.where(s < 10, s, 10 + 15 * np.sin(along))
    y = np.where(s < 10, 0.0, 15 * (1 - np.cos(along)))
    after = s > 10 + bend
    x = np.where(after, 25.0, x)
    y = np.where(after, 15 + (s - 10 - bend), y)
    return _track(np.column_stack([x, sign * y]), label="")


@pytest.mark.parametrize("sign, side", [(1, "left"), (-1, "right")])
def test_a_quarter_turn_has_its_angle_and_side(sign, side):
    facts = ego_facts(_turn(sign))
    assert facts["heading_change_deg"] == pytest.approx(sign * 90, abs=2)
    assert facts["turn"] == side
    assert facts["stopped_s"] == 0


def test_a_straight_drive_with_a_stop_is_no_turn():
    x = np.minimum(8.0 * T, 50.0)
    facts = ego_facts(_track(np.column_stack([x, np.zeros_like(x)]), label=""))
    assert facts["turn"] == "none"
    assert facts["stops"] == 1
    assert facts["stopped_s"] == pytest.approx(12.0 - 50 / 8, abs=0.2)
    assert facts["max_speed_mps"] == pytest.approx(8.0, abs=0.1)


def test_a_pedestrian_crossing_ahead_has_its_closest_approach_and_time():
    ego = _track(np.column_stack([5.0 * T, np.zeros_like(T)]), label="")
    path = reference_path(ego["xy"], ego["yaw"], 0.0)
    crossing = _track(np.column_stack([np.full_like(T, 40.0), 6.0 - 1.2 * T]), "person")
    sidewalk = _track(np.column_stack([1.0 * T + 10, np.full_like(T, 7.0)]), "person")
    found = pedestrians_near(ego, path, {"p1": crossing, "p2": sidewalk})
    assert [row["actor"] for row in found] == ["p1"]
    assert found[0]["closest_m"] == pytest.approx(0.0, abs=0.1)
    assert found[0]["at_s"] == pytest.approx(5.0, abs=0.1)
    assert found[0]["ego_distance_m"] == pytest.approx(15.0, abs=0.6)
    assert found[0]["crosses"]


def test_cars_keeping_their_lanes_show_the_ego_changing_lanes():
    s = 10.0 * T
    lateral = np.clip((s - 40) / 30, 0, 1) * 3.5
    ego = _track(np.column_stack([s, lateral]), label="")
    path = reference_path(ego["xy"], ego["yaw"], 0.0)
    cars = {
        f"c{lane}": _track(np.column_stack([5 + 9.0 * T, np.full_like(T, lane)]))
        for lane in (0.0, 3.5)
    }
    found = lane_change(path, float(s[-1]), cars)
    assert found["shift_m"] == pytest.approx(3.5, abs=0.3)
    assert found["cars_shifted"] == 2

    straight = _track(np.column_stack([s, np.zeros_like(s)]), label="")
    path = reference_path(straight["xy"], straight["yaw"], 0.0)
    assert lane_change(path, float(s[-1]), cars)["shift_m"] == 0.0


def _facts(**change):
    return {
        "heading_change_deg": 0.0,
        "turn": "none",
        "lead": None,
        "cut_ins": [],
        "lane_change": {"shift_m": 0.0},
        "crossing_vehicles": [],
        "oncoming": [],
        "pedestrians_near": [],
        **change,
    }


LEAD = {
    "actor": "7",
    "label": "automobile",
    "lead_s": 5.0,
    "min_gap_m": 9.0,
    "max_speed_mps": 8.0,
    "min_speed_mps": 0.0,
    "speed_drop_mps": 8.0,
}


def test_rule_tags_follow_the_facts():
    assert rule_tags(_facts()) == {}
    assert set(rule_tags(_facts(lead=LEAD))) == {"lead_vehicle"}
    brief = {**LEAD, "lead_s": 1.0}
    assert rule_tags(_facts(lead=brief)) == {}
    steady = {**LEAD, "min_speed_mps": 8.0, "speed_drop_mps": 0.5}
    assert rule_tags(_facts(lead=steady)) == {}

    left = _facts(heading_change_deg=80.0, turn="left")
    assert set(rule_tags(left)) == {"intersection"}
    oncoming = [{"actor": "3", "label": "automobile", "closest_to_turn_m": 12.0}]
    assert set(rule_tags({**left, "oncoming": oncoming})) == {
        "intersection",
        "unprotected_left",
    }

    shifted = {"shift_m": -3.4, "cars_shifted": 2, "cars_compared": 5}
    assert "3.4 m right" in rule_tags(_facts(lane_change=shifted))["merge_cut_in"]
    walker = {
        "actor": "p",
        "label": "person",
        "closest_m": 0.4,
        "at_s": 3.0,
        "ego_distance_m": 12.0,
        "closest_to_ego_m": 6.0,
        "crosses": True,
    }
    tags = rule_tags(_facts(pedestrians_near=[walker]))
    assert set(tags) == {"pedestrian_crossing"}
    assert "1 cross it" in tags["pedestrian_crossing"]
