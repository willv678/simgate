"""validate_diagnosis.py: which diagnoses of a FAILED run may reach recover.py."""

import pytest
from validate_diagnosis import rejection

POSTFLIGHT = "wizard_exit_code: 1; postflight_failed: metrics file not found"
PREFLIGHT = "preflight_rejected: context_length must be 8, got 1"
ENVIRONMENT = "environment: docker network create failed"


def _entry(make_run, skill, params, *, context_length=8, attempt=1, env_cleanups=0):
    entry = make_run(
        "r",
        context_length=context_length,
        launched=False,
        attempt=attempt,
        env_cleanups=env_cleanups,
    )
    entry["diagnosis"] = {"policy": "model", "skill": skill, "params": params}
    return entry


@pytest.mark.parametrize(
    "skill,params,context_length,attempt,k_status,accepted",
    [
        ("RE-RUN", {}, 8, 1, POSTFLIGHT, True),
        ("RESTART_CLEANUP", {}, 8, 2, POSTFLIGHT, True),
        ("CONFIGURE", {"context_length": 8}, 1, 1, PREFLIGHT, True),
        # The delay is the experiment. A recovery may not change it.
        ("CONFIGURE", {"planner_delay_us": 100000}, 8, 1, POSTFLIGHT, False),
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
        ("CONFIGURE", {"trafficsim_device": "cuda"}, 8, 1, POSTFLIGHT, True),
        ("CONFIGURE", {"trafficsim_device": "tpu"}, 8, 1, POSTFLIGHT, False),
        # The scene is the experiment. A recovery may not swap it.
        ("CONFIGURE", {"scene_id": "clipgt-test-scene"}, 8, 1, POSTFLIGHT, False),
        # A launched run may blame the machine.
        ("CLEANUP_ENV", {}, 8, 1, POSTFLIGHT, True),
        ("CLEANUP_ENV", {}, 8, 3, POSTFLIGHT, False),
        ("CLEANUP_ENV", {}, 1, 1, PREFLIGHT, False),
        # A machine problem is fixed only by CLEANUP_ENV, whatever the attempt.
        ("CLEANUP_ENV", {}, 8, 3, ENVIRONMENT, True),
        ("CLEANUP_ENV", {"force": True}, 8, 1, ENVIRONMENT, False),
        ("RE-RUN", {}, 8, 1, ENVIRONMENT, False),
        ("RESTART_CLEANUP", {}, 8, 1, ENVIRONMENT, False),
        ("CONFIGURE", {"trafficsim_device": "cuda"}, 8, 1, ENVIRONMENT, False),
        # Handing a run to a person is always allowed, without params.
        ("HALT", {}, 8, 1, POSTFLIGHT, True),
        ("HALT", {}, 8, 3, POSTFLIGHT, True),
        ("HALT", {}, 1, 1, PREFLIGHT, True),
        ("HALT", {}, 8, 1, ENVIRONMENT, True),
        ("HALT", {"why": "x"}, 8, 1, POSTFLIGHT, False),
    ],
)
def test_gate(make_run, skill, params, context_length, attempt, k_status, accepted):
    entry = _entry(
        make_run, skill, params, context_length=context_length, attempt=attempt
    )
    reason = rejection(entry, k_status)
    assert (reason is None) is accepted, reason


def test_second_cleanup_of_the_same_machine_problem_is_rejected(make_run):
    entry = _entry(make_run, "CLEANUP_ENV", {}, env_cleanups=1)
    assert (
        rejection(entry, ENVIRONMENT) == "environment still failing after CLEANUP_ENV"
    )
