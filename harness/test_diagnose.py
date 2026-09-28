"""diagnose.py: the status both policies see, and the script policy's answer."""

from pathlib import Path

import pytest
from diagnose import error_lines, script_diagnosis


def test_error_lines_drop_prefixes_colour_and_number_only_repeats(tmp_path: Path):
    log = tmp_path / "console.log"
    log.write_text(
        "renderer-0-1  | starting\n"
        "trafficsim-0-1  | torch.OutOfMemoryError: CUDA out of memory. Tried 24.00 MiB\n"
        "trafficsim-0-1  | torch.OutOfMemoryError: CUDA out of memory. Tried 38.00 MiB\n"
        "\x1b[Kruntime-0-1 exited with code 1\n"
    )
    assert error_lines(log) == [
        "torch.OutOfMemoryError: CUDA out of memory. Tried 24.00 MiB",
        "runtime-0-1 exited with code 1",
    ]


def test_error_lines_empty_when_never_launched(tmp_path: Path):
    assert error_lines(tmp_path / "missing.log") == []


@pytest.mark.parametrize(
    "k_status,attempt,skill,params",
    [
        (
            "preflight_rejected: context_length must be 8, got 1",
            1,
            "CONFIGURE",
            {"context_length": 8},
        ),
        ("preflight_rejected: scene_file does not exist: x.csv", 1, "CONFIGURE", {}),
        ("wizard_exit_code: 1; postflight_failed: no metrics", 1, "RE-RUN", {}),
        (
            "wizard_exit_code: 1; postflight_failed: no metrics",
            2,
            "RESTART_CLEANUP",
            {},
        ),
        (
            "config_not_landed: planner_delay_us requested 150000, resolved 0",
            1,
            "RE-RUN",
            {},
        ),
    ],
)
def test_script_policy(k_status, attempt, skill, params):
    status = {"k_status": k_status, "attempt": attempt}
    assert script_diagnosis(status) == {"skill": skill, "params": params}
