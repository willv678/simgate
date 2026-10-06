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
