"""physics.py: features from motion, and bounds applied to them."""

import numpy as np

from physics import features


def _signals(xs, reported=None, recorded_offset=1.0, gap=30.0, overlap=0.0):
    n = len(xs)
    speed = np.diff(xs) / 0.1
    return {
        "speed": speed,
        "accel": np.diff(speed) / 0.1,
        "jerk": np.diff(np.diff(speed) / 0.1) / 0.1,
        "yaw_rate": np.zeros(n - 1),
        "reported_speed": speed if reported is None else reported,
        "off_recording_m": np.full(n, recorded_offset),
        "lead_gap_m": np.full(n, gap),
        "overlap_m2": np.full(n, overlap),
        "plan_handoff_m": np.zeros(n),
        "plan_age_ms": np.zeros(n),
    }


def test_steady_driving_is_plausible():
    found = features(_signals(np.arange(0, 12, 1.0)), collided=False)
    assert found["max_abs_accel"] == 0
    assert found["max_speed_report_error"] == 0
    assert found["frac_on_recording"] == 0
    assert not found["contact_without_collision"]


def test_a_teleport_shows_in_acceleration_and_speed_report():
    xs = np.array([0, 1, 2, 3, 8, 9, 10], dtype=float)
    found = features(_signals(xs, reported=np.full(6, 10.0)), collided=False)
    assert found["max_abs_accel"] > 10
    assert found["max_speed_report_error"] > 1


def test_driving_on_the_recording_and_unscored_contact():
    found = features(
        _signals(np.arange(0, 12.0), recorded_offset=0.0, overlap=2.0), collided=False
    )
    assert found["frac_on_recording"] == 1.0
    assert found["contact_without_collision"]
    # Overlapping boxes are fine when the collision was scored.
    scored = features(_signals(np.arange(0, 12.0), overlap=2.0), collided=True)
    assert not scored["contact_without_collision"]
    # A close actor whose box does not overlap is not contact.
    near = features(_signals(np.arange(0, 12.0), gap=0.5), collided=False)
    assert not near["contact_without_collision"]


def test_plan_handoff_gap_is_zero_for_the_same_plan_and_sees_a_bias():
    from physics import _handoff_gap

    # Driver plan in world frame; the ego at (10, 5) heading +90 degrees.
    pose = (10.0, 5.0, np.pi / 2)
    driver = [(0, 10.0, 5.0), (500_000, 10.0, 7.0), (1_000_000, 10.0, 9.0)]
    # The same plan in the ego's rig frame: straight ahead along x.
    same = [(0, 0.0, 0.0), (500_000, 2.0, 0.0), (1_000_000, 4.0, 0.0)]
    biased = [(t, x, y + 1.0) for t, x, y in same]
    # A timing slip moves points along the road, not across it.
    slipped = [(t, x + 0.1, y) for t, x, y in same]
    assert _handoff_gap(pose, driver, same) < 1e-9
    assert abs(_handoff_gap(pose, driver, biased) - 1.0) < 1e-9
    assert _handoff_gap(pose, driver, slipped) < 1e-9


def test_plan_age_must_match_the_requested_delay():
    from physics import plan_age_problem

    def age(median, oldest):
        return {"median_plan_age_ms": median, "max_plan_age_ms": oldest}

    assert plan_age_problem(age(0, 0), 0, 100) is None
    assert plan_age_problem(age(200, 200), 150_000, 100) is None  # rounded up a step
    assert plan_age_problem(age(400, 900), 0, 100)  # a frozen plan
    assert plan_age_problem(age(0, 0), 100_000, 100)  # a delay that never applied
