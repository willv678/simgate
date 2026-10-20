"""A run may ask for another route-command rule; the driver must get it."""

import yaml

from knobs import run_config
from read_state import config_not_landed
from run_experiment import command_args, wizard_command

SCENE = "clipgt-0e002edd-c307-437c-9b97-6a1f6d28ac91"
TIGHT = {"threshold_m": 2.0, "lookahead_m": 20.0}


def test_alpasims_rule_adds_no_override_and_another_rule_does(tmp_path):
    plain = run_config(SCENE, {}, {}, "linear")
    assert command_args(plain) == []
    command = wizard_command(plain | {"command_rule": TIGHT}, tmp_path / "run")
    assert "driver.route.command_distance_threshold=2.0" in command
    assert "driver.route.min_lookahead_distance=20.0" in command


def test_a_rule_the_driver_did_not_get_is_not_landed(make_run):
    entry = make_run("cmd")
    entry["config"]["command_rule"] = TIGHT
    problems = config_not_landed(entry)
    assert any(p.startswith("command_rule requested") for p in problems)
    driver = yaml.safe_load(open(f"{entry['run_dir']}/driver-config.yaml"))
    driver["route"]["command_distance_threshold"] = 2.0
    open(f"{entry['run_dir']}/driver-config.yaml", "w").write(yaml.safe_dump(driver))
    assert not any(p.startswith("command_rule") for p in config_not_landed(entry))
