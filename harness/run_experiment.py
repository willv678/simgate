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
import zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from environment import environment_problems
from faults import before_launch, plan_hook_args, shell_around, wizard_args
from read_state import (
    PLAN_KEYS,
    ROOT,
    State,
    boot_id,
    console_log,
    ego_speed_request,
    exit_file,
    frame_interval_us,
    load_entry,
    plan_request,
    read_state,
    requested_controller,
    retime_request,
    run_dir,
    save_entry,
    seed_request,
    subsample_factor,
    traffic_mode,
)

PORT_BASE = 20_000
PORT_SLOTS = 400
PORT_STRIDE = 50


def plan_args(request: dict) -> list[str]:
    """The plan perturbations the run asks for, if any (read_state.PLAN_KEYS)."""
    asked = {key: request[key] for key in PLAN_KEYS if request[key]}
    return plan_hook_args(asked) if asked else []


def base_port(run_name: str) -> int:
    """Where the wizard starts looking for free ports for this run. It takes
    the next ports that are free when it writes the compose file, so two runs
    starting at once from one base port can pick the same ports; a base per
    run name keeps runs in flight apart."""
    return PORT_BASE + zlib.crc32(run_name.encode()) % PORT_SLOTS * PORT_STRIDE


def wizard_command(config: dict, log_dir: Path) -> list[str]:
    return [
        "uv",
        "run",
        "alpasim_wizard",
        "deploy=local",
        "topology=1gpu",
        "driver=vavam",
        f"trafficsim={'catk' if traffic_mode(config) == 'catk' else 'disabled'}",
        f"controller={requested_controller(config)}",
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
        f"wizard.baseport={base_port(log_dir.name)}",
        *plan_args(plan_request(config)),
        *traffic_args(config),
        *seed_args(config),
        *ego_args(config),
    ]


def traffic_args(config: dict) -> list[str]:
    """The CATK device when CATK runs, and the actor retiming rule if any (the
    base config has no actor_retiming block, so Hydra must add it, +)."""
    args = []
    if traffic_mode(config) == "catk":
        args.append(f"trafficsim.catk.device={config['trafficsim_device']}")
    rule = retime_request(config)
    if rule is not None:
        # Quoted, a track id stays a string: unquoted, Hydra reads "123" as 123.
        body = ",".join(
            f'{k}:"{v}"' if k == "track_id" else f"{k}:{v}" for k, v in rule.items()
        )
        args.append(f"+runtime.simulation_config.actor_retiming.rules=[{{{body}}}]")
    return args


def seed_args(config: dict) -> list[str]:
    """The wizard overrides of a seeded run. Neither key is in AlpaSim's base
    configs, so Hydra must add them (+)."""
    seed = seed_request(config)
    if seed is None:
        return []
    return [
        f"+runtime.simulation_config.random_seed={seed}",
        "+driver.model.force_determinism=true",
    ]


def ego_args(config: dict) -> list[str]:
    """The ego speed scale when it is not the recorded speed. The key is not
    in AlpaSim's base config, so Hydra must add it (+)."""
    scale = ego_speed_request(config)
    if scale == 1.0:
        return []
    return [f"+runtime.simulation_config.ego_speed_scale={scale}"]


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
    entry["boot_id"] = boot_id()
    save_entry(entry_path, entry)
    print(json.dumps({"pid": proc.pid, "run_dir": entry["run_dir"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
