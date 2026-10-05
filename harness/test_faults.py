"""faults.py: each fault changes only the launch it is attached to."""

from pathlib import Path

import pytest
from faults import new_fault, shell_around, wizard_args
from recover import _inherited

LOG_DIR = Path("/repo/diag/c1_004")
ARGS = [
    "uv",
    "run",
    "alpasim_wizard",
    "runtime.simulation_config.planner_delay_us=100000",
    f"wizard.log_dir={LOG_DIR}",
]


def test_no_fault_changes_nothing():
    assert wizard_args(None, ARGS) == ARGS
    assert shell_around(None, LOG_DIR) == ("", "", "")


def test_drop_delay_removes_only_the_delay_override():
    args = wizard_args(new_fault("drop_delay", persistent=True), ARGS)
    assert args == [ARGS[0], ARGS[1], ARGS[2], ARGS[4]]


@pytest.mark.parametrize(
    "fault,expected",
    [
        (
            new_fault("kill", after_s=90),
            ("", "timeout --preserve-status -s KILL 90 ", ""),
        ),
        (
            new_fault("hang", after_s=120),
            ("( sleep 120; docker pause c1_004-runtime-0-1 ) & ", "", ""),
        ),
        (
            new_fault("delete_metrics"),
            ("", "", "find /repo/diag/c1_004 -name metrics.parquet -delete; "),
        ),
    ],
)
def test_shell_around(fault, expected):
    assert shell_around(fault, LOG_DIR) == expected


def test_only_persistent_faults_repeat_on_the_retry():
    assert _inherited(new_fault("kill", after_s=90)) is None
    persistent = {**new_fault("drop_delay", persistent=True), "applied": True}
    assert _inherited(persistent) == {**persistent, "applied": False}


def test_unknown_fault_is_rejected():
    with pytest.raises(ValueError):
        new_fault("meteor")


def test_silent_faults_swap_one_argument():
    args = [
        "controller=linear",
        "runtime.simulation_config.force_gt_duration_us=4500000",
    ]
    assert wizard_args(new_fault("kinematic"), args) == [
        "controller=kinematic_ideal",
        args[1],
    ]
    assert wizard_args(new_fault("rails"), args) == [
        args[0],
        "runtime.simulation_config.force_gt_duration_us=60000000",
    ]


def test_plan_faults_turn_on_alpasims_own_hook():
    args = ["controller=linear"]
    assert wizard_args(new_fault("lateral_bias"), args) == [
        "controller=linear",
        "runtime.simulation_config.fault_injection.enabled=true",
        "runtime.simulation_config.fault_injection.lateral_bias_m=1.0",
    ]
