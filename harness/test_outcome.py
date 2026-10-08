"""outer.outcome: a failure is the policy's, counted after it takes over."""

import pandas as pd
import pytest

from outer import criticality, outcome

T0 = 1_000_000_000
STEP = 100_000
HANDOFF = 5  # the policy drives from the fifth step


def _run(tmp_path, events: dict[str, list[int]], distance=None):
    """A run whose metrics flag each named event at the given steps."""
    rollout = tmp_path / "rollouts" / "clipgt-x" / "r0"
    rollout.mkdir(parents=True)
    (rollout / "_complete").write_text("")
    steps = range(12)
    rows = []
    names = ("collision_front", "collision_lateral", "collision_rear", "offroad",
             "img_is_black", "progress", "dist_to_gt_trajectory")  # fmt: skip
    for name in names:
        for i in steps:
            rows.append((name, T0 + i * STEP, float(i in events.get(name, []))))
    for i in steps:
        rows.append(("eval_relevant", T0 + i * STEP, float(i >= HANDOFF)))
        d = distance[i] if distance else 10.0
        rows.append(("min_distance_to_obstacle_m", T0 + i * STEP, d))
    pd.DataFrame(rows, columns=["name", "timestamps_us", "values"]).to_parquet(
        rollout / "metrics.parquet"
    )
    return tmp_path


def test_a_collision_after_the_hand_off_is_a_failure(tmp_path):
    found = outcome(_run(tmp_path, {"collision_front": [7]}))
    assert found["failed"] and found["collision_at_fault"]
    assert found["failed_at_s"] == 0.7 and found["handoff_s"] == 0.5


def test_a_collision_in_the_warm_up_is_not_the_policys(tmp_path):
    found = outcome(_run(tmp_path, {"collision_front": [0, 1]}))
    assert not found["failed"] and found["failed_any"]


def test_being_rear_ended_first_is_not_the_policys(tmp_path):
    # Replayed traffic hits the ego from behind, then overlaps its front.
    found = outcome(_run(tmp_path, {"collision_rear": [6], "collision_front": [7, 8]}))
    assert not found["failed"] and found["rear_ended"] and found["failed_any"]


def test_a_front_collision_before_a_rear_one_is_the_policys(tmp_path):
    found = outcome(_run(tmp_path, {"collision_lateral": [6], "collision_rear": [8]}))
    assert found["failed"]


def test_leaving_the_road_is_a_failure_even_after_a_rear_contact(tmp_path):
    found = outcome(_run(tmp_path, {"collision_rear": [6], "offroad": [9]}))
    assert found["failed"] and found["offroad"]


def test_closest_approach_counts_from_the_hand_off_until_a_rear_contact(tmp_path):
    distance = [0.0] * 5 + [3.0, 2.0, 0.0, 0.0, 4.0, 4.0, 4.0]
    found = outcome(_run(tmp_path, {"collision_rear": [7]}, distance))
    assert found["min_distance_to_obstacle_m"] == 2.0
    assert found["criticality"] == pytest.approx(0.54)


def test_a_run_rear_ended_at_the_hand_off_has_no_near_miss():
    assert criticality(False, None) == 0.0
