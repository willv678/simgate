"""READY -> check the machine, then launch one wizard run in the background.

If environment.py finds a problem, nothing launches: the problems are written
to the entry, and read_state.py reports the run FAILED with `environment: …`.
An injected fault on the entry (faults.py) is applied here. The console log's
first line is the wizard command as launched, without the fault's shell.

The command is the L8 re-run command, with the scene and CATK device from the
config. When the wizard returns, a
shell wrapper takes down the run's containers and network, then writes the
wizard exit code next to the run directory, so read_state.py can tell RUNNING
from finished without this process staying up. Without the teardown every run
leaves a Docker network behind, and after about 30 runs `docker compose up`
fails with "all predefined address pools have been fully subnetted".

    uv run python research/harness/run_experiment.py <entry.json>
"""

import json
import shlex
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from environment import environment_problems
from faults import before_launch, plan_hook_args, shell_around, wizard_args
from read_state import (
    PLAN_KEYS,
    ROOT,
    State,
    console_log,
    exit_file,
    frame_interval_us,
    load_entry,
    plan_request,
    read_state,
    retime_request,
    run_dir,
    save_entry,
    subsample_factor,
    traffic_mode,
)


def plan_args(request: dict) -> list[str]:
    """The plan perturbations the run asks for, if any (read_state.PLAN_KEYS)."""
    asked = {key: request[key] for key in PLAN_KEYS if request[key]}
    return plan_hook_args(asked) if asked else []


def wizard_command(config: dict, log_dir: Path) -> list[str]:
    return [
        "uv",
        "run",
        "alpasim_wizard",
        "deploy=local",
        "topology=1gpu",
        "driver=vavam",
        f"trafficsim={'catk' if traffic_mode(config) == 'catk' else 'disabled'}",
        "controller=linear",
        f"driver.inference.context_length={config['context_length']}",
        f"driver.inference.subsample_factor={subsample_factor(config)}",
        f"runtime.simulation_config.cameras.0.frame_interval_us={frame_interval_us(config)}",
        "runtime.simulation_config.force_gt_duration_us=4500000",
        "runtime.simulation_config.control_timestep_us=100000",
        "runtime.simulation_config.n_sim_steps=120",
        "runtime.simulation_config.route_start_offset_m=0.0",
        f"runtime.simulation_config.planner_delay_us={config['planner_delay_us']}",
        f"scenes.scenes_csv=[{ROOT / config['scene_file']}]",
        f"scenes.scene_ids=[{config['scene_id']}]",
        f"wizard.log_dir={log_dir}",
        *plan_args(plan_request(config)),
        *traffic_args(config),
    ]


def traffic_args(config: dict) -> list[str]:
    """The CATK device when CATK runs, and the actor retiming rule if any (the
    base config has no actor_retiming block, so Hydra must add it, +)."""
    args = []
    if traffic_mode(config) == "catk":
        args.append(f"trafficsim.catk.device={config['trafficsim_device']}")
    rule = retime_request(config)
    if rule is not None:
        body = ",".join(f"{k}:{v}" for k, v in rule.items())
        args.append(f"+runtime.simulation_config.actor_retiming.rules=[{{{body}}}]")
    return args


def main() -> int:
    entry_path = Path(sys.argv[1])
    entry = load_entry(entry_path)
    state = read_state(entry)
    if state.state is not State.READY:
        raise SystemExit(f"{entry['name']} is {state.state.value}, not READY")
    log_dir = run_dir(entry)
    if log_dir.exists():
        raise SystemExit(f"{log_dir} already exists")

    fault = entry["fault"]
    before_launch(fault)
    problems = environment_problems()
    if problems:
        entry["environment"] = problems
        save_entry(entry_path, entry)
        print(json.dumps({"launched": False, "environment": problems}))
        return 0

    cmd = shlex.join(wizard_args(fault, wizard_command(entry["config"], log_dir)))
    before, prefix, after = shell_around(fault, log_dir)
    console = shlex.quote(str(console_log(entry)))
    exit_path = exit_file(entry)
    exit_tmp = shlex.quote(f"{exit_path}.tmp")
    compose = shlex.quote(str(log_dir / "docker-compose.yaml"))
    script = (
        f"echo {shlex.quote(cmd)} > {console}; "
        f"{before}{prefix}{cmd} >> {console} 2>&1; "
        "code=$?; "
        f"{after}"
        f"docker compose -f {compose} down --remove-orphans >> {console} 2>&1; "
        f"echo $code > {exit_tmp} && mv {exit_tmp} {shlex.quote(str(exit_path))}"
    )
    log_dir.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.Popen(
        ["bash", "-c", script],
        cwd=ROOT,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    entry["launched"] = True
    entry["pid"] = proc.pid
    entry["launched_at"] = time.time()
    save_entry(entry_path, entry)
    print(json.dumps({"pid": proc.pid, "run_dir": entry["run_dir"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
