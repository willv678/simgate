"""The gate holds against every answer any policy could give (verify_supervisor.py)."""

import verify_supervisor


def test_no_policy_can_break_the_gate(no_promoted_rules):
    report = verify_supervisor.explore()
    assert report["violations"] == []
    assert report["max_launches"] <= 3
    assert report["transitions"] > 1000
