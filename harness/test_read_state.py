"""read_state.py: each state from the files a run leaves behind."""

import os

from read_state import State, read_state


def test_unlaunched_valid_config_is_ready(make_run):
    assert read_state(make_run("r", launched=False)).state is State.READY


def test_preflight_reject_is_failed_and_never_ready(make_run):
    result = read_state(make_run("r", context_length=1, launched=False))
    assert result.state is State.FAILED
    assert result.k_status == "preflight_rejected: context_length must be 8, got 1"


def test_live_process_without_exit_code_is_running(make_run):
    entry = make_run("r", exit_code=None, metrics=False)
    entry["pid"] = os.getpid()
    assert read_state(entry).state is State.RUNNING


def test_dead_process_without_exit_code_is_failed(make_run):
    result = read_state(make_run("r", exit_code=None, metrics=False))
    assert result.state is State.FAILED
    assert result.k_status.startswith("process_lost")


def test_nonzero_exit_and_no_metrics_reports_both(make_run):
    result = read_state(make_run("r", exit_code=1, metrics=False))
    assert result.state is State.FAILED
    assert result.k_status == (
        "wizard_exit_code: 1; "
        "postflight_failed: metrics file not found (no metrics.parquet)"
    )


def test_nonzero_exit_with_metrics_is_still_failed(make_run):
    result = read_state(make_run("r", exit_code=137))
    assert result.state is State.FAILED
    assert result.k_status == "wizard_exit_code: 137"


def test_delay_that_did_not_land_is_failed(make_run):
    result = read_state(make_run("r", planner_delay_us=150000, resolved_delay_us=0))
    assert result.state is State.FAILED
    assert result.k_status == (
        "config_not_landed: planner_delay_us requested 150000, resolved 0"
    )


def test_clean_run_is_complete_with_postflight_flags(make_run):
    result = read_state(make_run("r", at_fault=True))
    assert result.state is State.COMPLETE
    assert result.k_status == "postflight_success: at_fault=True, rear=False"


def test_resolved_entry_is_done(make_run):
    entry = make_run("r", exit_code=1, metrics=False)
    entry["resolution"] = "RE-RUN"
    assert read_state(entry).state is State.DONE


def test_environment_problem_before_launch_is_failed(make_run):
    entry = make_run("r", launched=False, environment=["GPU free 900 MiB < 10500 MiB"])
    result = read_state(entry)
    assert result.state is State.FAILED
    assert result.k_status == "environment: GPU free 900 MiB < 10500 MiB"


def test_scene_missing_from_catalog_is_preflight_rejected(make_run):
    entry = make_run("r", launched=False)
    entry["config"]["scene_id"] = "clipgt-not-in-catalog"
    assert read_state(entry).k_status.startswith("preflight_rejected: scene_id")


def test_traffic_device_that_did_not_land_is_failed(make_run):
    result = read_state(make_run("r", resolved_device="cuda"))
    assert result.k_status == (
        "config_not_landed: trafficsim_device requested cpu, resolved cuda"
    )


def test_a_controller_that_did_not_land_is_failed(make_run):
    assert read_state(make_run("ab", controller="nonlinear")).state is State.COMPLETE
    swapped = read_state(
        make_run("swapped", controller="nonlinear", resolved_controller="linear")
    )
    assert swapped.k_status == (
        "config_not_landed: controller requested nonlinear, resolved linear"
    )
    # Same MPC implementation, another config: told apart by the horizon.
    short = read_state(
        make_run("short", controller="nonlinear", resolved_controller="short_horizon")
    )
    assert short.k_status.endswith("requested nonlinear, resolved short_horizon")
    # An entry without a controller key asked for the linear MPC.
    legacy = read_state(make_run("legacy", resolved_controller="kinematic_ideal"))
    assert legacy.k_status == (
        "config_not_landed: controller requested linear, resolved kinematic_ideal"
    )


def test_each_controller_config_resolves_to_its_own_name():
    """knobs.CONTROLLERS' identifying values are what AlpaSim's controller
    configs compose to, and no other controller has them."""
    import yaml
    from knobs import CONTROLLERS
    from read_state import ROOT, resolved_controller

    configs = ROOT / "src" / "wizard" / "configs" / "controller"

    def composed(name: str) -> dict:
        raw = yaml.safe_load((configs / f"{name}.yaml").read_text(encoding="utf-8"))
        block = {}
        for parent in raw.pop("defaults", []):
            if parent != "_self_":
                block |= composed(parent)
        return block | raw

    assert {name: resolved_controller(composed(name)) for name in CONTROLLERS} == {
        name: name for name in CONTROLLERS
    }


def test_physics_bounds_fail_a_run_the_other_checks_keep(
    make_run, tmp_path, monkeypatch
):
    entry = make_run("r")
    assert read_state(entry).state is State.COMPLETE
    bounds = tmp_path / "physics_on.json"
    bounds.write_text('{"enabled": true, "max": {"max_abs_accel": {"max": 10.0}}}')
    monkeypatch.setenv("ALPASIM_PHYSICS", str(bounds))
    result = read_state(entry)
    # The fixture run has no completed rollout, so nothing shows the motion was possible.
    assert result.state is State.FAILED
    assert result.k_status.startswith("physics: no rollout log")


def test_a_launcher_from_another_boot_is_never_alive():
    import os

    from read_state import boot_id, launcher_alive

    me = {"pid": os.getpid(), "boot_id": boot_id()}
    assert launcher_alive(me)
    assert not launcher_alive({**me, "boot_id": "an-earlier-boot"})
    assert launcher_alive({"pid": os.getpid()})  # launched before boot ids were kept
