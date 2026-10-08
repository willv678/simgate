"""Actor retiming in the harness: the wizard gets the rule, and a rule that
retimed no actor fails the run."""

from read_state import retime_not_applied, retime_request
from run_experiment import traffic_args

BASE = {"trafficsim_device": "cpu"}
PEDESTRIAN = {
    **BASE,
    "traffic": "replay",
    "retime_class": "person",
    "actor_time_shift_s": -1.0,
    "actor_speed_scale": 1.5,
}


def test_no_rule_without_a_class_or_with_unvaried_values():
    assert retime_request(BASE) is None
    assert (
        retime_request(
            {**PEDESTRIAN, "actor_time_shift_s": 0.0, "actor_speed_scale": 1.0}
        )
        is None
    )


def test_replay_drops_the_catk_device_and_adds_the_rule():
    args = traffic_args(PEDESTRIAN)
    assert not any(a.startswith("trafficsim.catk.device") for a in args)
    rule = "[{label_class:person,time_shift_s:-1.0,speed_scale:1.5}]"
    assert args == [f"+runtime.simulation_config.actor_retiming.rules={rule}"]
    assert traffic_args(BASE) == ["trafficsim.catk.device=cpu"]


def test_a_rule_that_retimed_no_actor_fails(tmp_path):
    run = tmp_path / "run"
    (run / "txt-logs").mkdir(parents=True)
    entry = {"run_dir": str(run), "config": PEDESTRIAN}
    log = run / "txt-logs" / "runtime_worker_0.log"
    log.write_text("nothing retimed\n")
    assert retime_not_applied(entry)
    log.write_text("Retimed actor 17 (person): time_shift_s=-1.0 speed_scale=1.5\n")
    assert retime_not_applied(entry) is None
    assert retime_not_applied({**entry, "config": BASE}) is None


def test_a_scene_key_actor_is_retimed_alone(tmp_path):
    from knobs import run_config

    fixed = {
        "traffic": "replay",
        "retime_class": "person",
        "retime_tracks": {"clipgt-a": "17"},
    }
    config = run_config("clipgt-a", {"actor_time_shift_s": -1.0}, fixed)
    assert retime_request(config) == {
        "track_id": "17",
        "time_shift_s": -1.0,
        "speed_scale": 1.0,
    }
    other = run_config("clipgt-b", {"actor_time_shift_s": -1.0}, fixed)
    assert retime_request(other)["label_class"] == "person"
    run = tmp_path / "run"
    (run / "txt-logs").mkdir(parents=True)
    log = run / "txt-logs" / "runtime_worker_0.log"
    log.write_text("Retimed actor 18 (person): time_shift_s=-1.0\n")
    assert retime_not_applied({"run_dir": str(run), "config": config})  # wrong actor
    log.write_text("Retimed actor 17 (person): time_shift_s=-1.0\n")
    assert retime_not_applied({"run_dir": str(run), "config": config}) is None


def test_a_track_id_is_passed_as_a_string():
    config = {**PEDESTRIAN, "retime_track": "123"}
    (arg,) = [a for a in traffic_args(config) if "actor_retiming" in a]
    assert 'track_id:"123"' in arg


def test_runs_start_their_port_search_apart():
    from run_experiment import PORT_BASE, base_port

    ports = {base_port(f"study_{i:03d}") for i in range(20)}
    assert len(ports) > 15
    assert all(PORT_BASE <= p < 40_000 for p in ports)
