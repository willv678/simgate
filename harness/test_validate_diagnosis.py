"""validate_diagnosis.py: which diagnoses of a FAILED run may reach recover.py."""

import pytest
from validate_diagnosis import rejection

POSTFLIGHT = "wizard_exit_code: 1; postflight_failed: metrics file not found"
PREFLIGHT = "preflight_rejected: context_length must be 8, got 1"


def _entry(make_run, skill, params, *, context_length=8, attempt=1):
    entry = make_run(
        "r", context_length=context_length, launched=False, attempt=attempt
    )
    entry["diagnosis"] = {"policy": "model", "skill": skill, "params": params}
    return entry


@pytest.mark.parametrize(
    "skill,params,context_length,attempt,k_status,accepted",
    [
        ("RE-RUN", {}, 8, 1, POSTFLIGHT, True),
        ("RESTART_CLEANUP", {}, 8, 2, POSTFLIGHT, True),
        ("CONFIGURE", {"context_length": 8}, 1, 1, PREFLIGHT, True),
        ("CONFIGURE", {"planner_delay_us": 100000}, 8, 1, POSTFLIGHT, True),
        # A FAILED run is never kept, and launching is READY's step.
        ("ACCEPT", {}, 8, 1, POSTFLIGHT, False),
        ("LAUNCH", {}, 8, 1, POSTFLIGHT, False),
        ("REBOOT", {}, 8, 1, POSTFLIGHT, False),
        (None, {}, 8, 1, POSTFLIGHT, False),
        # Budget.
        ("RE-RUN", {}, 8, 3, POSTFLIGHT, False),
        ("CONFIGURE", {"context_length": 8}, 1, 3, PREFLIGHT, False),
        # A config preflight rejected is never relaunched as is.
        ("RE-RUN", {}, 1, 1, PREFLIGHT, False),
        ("RESTART_CLEANUP", {}, 1, 1, PREFLIGHT, False),
        ("RE-RUN", {"context_length": 8}, 8, 1, POSTFLIGHT, False),
        # CONFIGURE is limited to known keys and to configs preflight accepts.
        ("CONFIGURE", {}, 8, 1, POSTFLIGHT, False),
        ("CONFIGURE", {"q_lateral": 5.0}, 8, 1, POSTFLIGHT, False),
        ("CONFIGURE", {"context_length": 8}, 8, 1, POSTFLIGHT, False),
        ("CONFIGURE", {"context_length": 4}, 1, 1, PREFLIGHT, False),
        ("CONFIGURE", {"context_length": "8"}, 1, 1, PREFLIGHT, False),
        ("CONFIGURE", {"scene_file": "no/such/scenes.csv"}, 8, 1, POSTFLIGHT, False),
    ],
)
def test_gate(make_run, skill, params, context_length, attempt, k_status, accepted):
    entry = _entry(
        make_run, skill, params, context_length=context_length, attempt=attempt
    )
    reason = rejection(entry, k_status)
    assert (reason is None) is accepted, reason
