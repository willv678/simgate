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
        "plan_deviations": [np.zeros(5)] * n,
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
    driver = [
        (0, 10.0, 5.0, np.pi / 2),
        (500_000, 10.0, 7.0, np.pi / 2),
        (1_000_000, 10.0, 9.0, np.pi / 2),
    ]
    # The same plan in the ego's rig frame: straight ahead along x.
    same = [(0, 0.0, 0.0), (500_000, 2.0, 0.0), (1_000_000, 4.0, 0.0)]
    biased = [(t, x, y + 1.0) for t, x, y in same]
    # A timing slip moves points along the road, not across it.
    slipped = [(t, x + 0.1, y) for t, x, y in same]
    assert _handoff_gap(pose, driver, same) < 1e-9
    assert abs(_handoff_gap(pose, driver, biased) - 1.0) < 1e-9
    assert _handoff_gap(pose, driver, slipped) < 1e-9


def test_the_plan_must_be_the_drivers_plus_exactly_what_was_asked():
    from physics import plan_problems

    bounds = {
        "plan_age": {"slack_ms": 100},
        "plan_matches_request": {"offset_tolerance_m": 0.02, "noise_tolerance_m": 0.02},
    }

    def found(age=(0, 0), offset=0.0, noise=0.0):
        return {
            "median_plan_age_ms": age[0],
            "max_plan_age_ms": age[1],
            "median_plan_offset_m": offset,
            "plan_noise_m": noise,
        }

    def request(delay_us=0, bias=0.0, noise=0.0):
        return {
            "planner_delay_us": delay_us,
            "lateral_bias_m": bias,
            "waypoint_noise_std": noise,
        }

    assert plan_problems(found(), request(), bounds) == []
    # A delay rounds up to the next control step.
    assert plan_problems(found(age=(200, 200)), request(delay_us=150_000), bounds) == []
    assert plan_problems(found(age=(400, 900)), request(), bounds)  # a frozen plan
    assert plan_problems(
        found(), request(delay_us=100_000), bounds
    )  # delay not applied
    assert plan_problems(found(offset=-0.3), request(bias=-0.3), bounds) == []
    assert plan_problems(
        found(offset=1.0), request(), bounds
    )  # a bias nobody asked for
    assert plan_problems(
        found(offset=0.3), request(bias=-0.3), bounds
    )  # the wrong side
    assert plan_problems(found(noise=0.3), request(), bounds)  # noise nobody asked for


def test_the_offset_is_measured_along_each_waypoints_normal():
    from physics import _handoff_deviations

    # The ego at the origin heading +x; the driver's plan curves left.
    pose = (0.0, 0.0, 0.0)
    driver = [
        (0, 0.0, 0.0, 0.0),
        (500_000, 2.0, 0.5, np.pi / 4),
        (1_000_000, 3.0, 2.0, np.pi / 2),
    ]
    # The runtime's lateral bias: each waypoint moved left of its own heading.
    bias = 0.3
    given = [(t, x - np.sin(h) * bias, y + np.cos(h) * bias) for t, x, y, h in driver]
    assert np.allclose(_handoff_deviations(pose, driver, given), bias)
    same = [(t, x, y) for t, x, y, _ in driver]
    assert np.allclose(_handoff_deviations(pose, driver, same), 0.0)
