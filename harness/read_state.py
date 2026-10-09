"""State of one queued run: READY, RUNNING, COMPLETE, FAILED, or DONE.

A queue entry is a JSON file that names a run directory and the config
requested for it. The state comes from that entry and from the files the run
left behind, using the checks that already exist:

- preflight (K⁻) on the requested config, before and after launch;
- the environment problems run_experiment.py found instead of launching;
- the wizard exit code, written next to the run by run_experiment.py;
- postflight (K⁺) on the run directory;
- whether the requested values are the ones the wizard resolved (the
  controller among them), and for a seeded run whether its sessions were
  opened with that seed (the log);
- for a run with a retimed ego, the runtime's line and the ego's speed at
  hand-off in the log (physics.handoff_speeds);
- the rules the tier 2 auditor proposed and promote.py admitted (rules.py);
- when enabled, whether the motion was physically possible (physics.py).

This module only reads. The scripts the loop dispatches write the entry.

    uv run python research/harness/read_state.py <entry.json>
"""

import csv
import json
import os
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

from analyze_cp2 import extract_resolved_config
from knobs import CONTROLLERS, DEFAULT_CONTROLLER
from postflight import validate_postflight
from preflight import PreflightError, validate_preflight
from rules import load_rules, violations

from physics import check as physics_problems
from physics import handoff_speed_matches, handoff_speeds, load_bounds, session_seeds

ROOT = Path(__file__).resolve().parents[2]

# Launches per lineage (the first launch plus recoveries) before a person decides.
MAX_ATTEMPTS = 3
# Every key of a queue config. Each is checked against the resolved config.
CONFIG_KEYS = (
    "context_length",
    "planner_delay_us",
    "scene_file",
    "scene_id",
    "trafficsim_device",
)
# Keys a CONFIGURE may change: how a run executes, never what it measures.
# The delay and the scene are the experiment; changing them in a recovery would
# keep a run that measures another condition (verify_supervisor.py, S3).
CONFIGURABLE_KEYS = ("context_length", "scene_file", "trafficsim_device")
# Optional perturbations of the plan between the driver and the controller,
# through AlpaSim's plan-corruption hook: what a study varies, like the delay.
PLAN_KEYS = ("lateral_bias_m", "waypoint_noise_std")
# VaVAM plans from 8 frames 500 ms apart and is asked for a plan every control
# step (100 ms). Frames every 500 ms mean four of every five plans reuse the
# last frames, re-anchored at the current pose; frames every 100 ms with every
# fifth frame in the context give each plan a fresh frame at the same 2 Hz
# spacing. Entries queued before 6 Oct 2026 have no frame_interval_us: 500 ms.
VAVAM_FRAME_SPACING_US = 500_000
LEGACY_FRAME_INTERVAL_US = 500_000
TRAFFICSIM_DEVICES = ("cpu", "cuda")
# A run's seed is AlpaSim's RolloutSpec.random_seed, where 0 means random; the
# driver adds its inference count to it, so seeds stay well below 2**32.
SEED_LIMIT = 2**31


class State(Enum):
    READY = "READY"
    RUNNING = "RUNNING"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"
    DONE = "DONE"


@dataclass(frozen=True)
class RunState:
    state: State
    k_status: str


def load_entry(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_entry(path: Path, entry: dict) -> None:
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(entry, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def queue_entries(queue: Path) -> list[Path]:
    """Entry files of a queue, in order. Reports such as audit.json sit beside them."""
    return sorted(queue.glob("[0-9][0-9][0-9]_*.json"))


def run_dir(entry: dict) -> Path:
    return ROOT / entry["run_dir"]


def console_log(entry: dict) -> Path:
    """Wizard stdout and stderr, next to the run directory as in L8."""
    path = run_dir(entry)
    return path.parent / f"{path.name}_console.log"


def exit_file(entry: dict) -> Path:
    path = run_dir(entry)
    return path.parent / f"{path.name}_exit_code"


def timeout_machine_file(entry: dict) -> Path:
    """The machine as monitor.py saw it when it timed the run out, before it
    stopped the run; stopping it removes the evidence (a paused container)."""
    path = run_dir(entry)
    return path.parent / f"{path.name}_timeout_machine.txt"


def preflight_config(config: dict) -> dict:
    """The dict preflight.py checks, built from a queue config.

    run_experiment.py writes the Hydra delay override from planner_delay_us,
    so the requested and Hydra delays are the same value here. Whether the
    delay landed is checked after exit, against the resolved config.
    """
    return {
        "context_length": config["context_length"],
        "hydra_delay": config["planner_delay_us"],
        "request_delay": config["planner_delay_us"],
        "scene_file": str(ROOT / config["scene_file"]),
    }


def config_problem(config: dict) -> str | None:
    """Why this config must not launch, or None. The one preflight every caller uses."""
    try:
        validate_preflight(preflight_config(config))
    except PreflightError as exc:
        return str(exc)
    seed = seed_request(config)
    if seed is not None and not (type(seed) is int and 1 <= seed < SEED_LIMIT):
        return f"seed must be an int from 1 to {SEED_LIMIT - 1}, got {seed!r}"
    if config["trafficsim_device"] not in TRAFFICSIM_DEVICES:
        return f"trafficsim_device must be one of {TRAFFICSIM_DEVICES}, got {config['trafficsim_device']!r}"
    if mirror_request(config) and not (MIRROR_CHECKOUT / "src").is_dir():
        return f"mirror runs need the mirror checkout at {MIRROR_CHECKOUT}"
    with (ROOT / config["scene_file"]).open(encoding="utf-8") as handle:
        scene_ids = {row["scene_id"] for row in csv.DictReader(handle)}
    if config["scene_id"] not in scene_ids:
        return f"scene_id {config['scene_id']} is not in {config['scene_file']}"
    return None


def _exit_code(entry: dict) -> int | None:
    path = exit_file(entry)
    if not path.is_file():
        return None
    return int(path.read_text(encoding="utf-8").strip())


BOOT_ID = Path("/proc/sys/kernel/random/boot_id")


def boot_id() -> str:
    return BOOT_ID.read_text(encoding="utf-8").strip()


def launcher_alive(entry: dict) -> bool:
    """Whether the run's launcher still runs. A pid from before a reboot can
    belong to an unrelated process now, so a run launched in another boot is
    never alive. Entries launched before 7 Oct 2026 have no boot_id."""
    if entry.get("boot_id", boot_id()) != boot_id():
        return False
    return _alive(entry["pid"])


def _alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def plan_request(config: dict) -> dict:
    """What the run asked of the plan handed to the controller: its delay and
    perturbations. Entries queued before 6 Oct 2026 have no perturbation keys."""
    return {
        "planner_delay_us": config["planner_delay_us"],
        **{key: config.get(key, 0.0) for key in PLAN_KEYS},
    }


def traffic_mode(config: dict) -> str:
    """ "catk": the CATK model drives other actors after the warm-up; "replay":
    they follow their recorded (possibly retimed) tracks for the whole run.
    Entries queued before 7 Oct 2026 have no traffic key: CATK."""
    return config.get("traffic", "catk")


def retime_request(config: dict) -> dict | None:
    """The actor retiming the run asks for (AlpaSim's actor_retiming hook), or
    None: one rule over one recorded actor (`retime_track`, the scene's key
    actor) or over every recorded actor of `retime_class`."""
    shift = config.get("actor_time_shift_s", 0.0)
    scale = config.get("actor_speed_scale", 1.0)
    if shift == 0.0 and scale == 1.0:
        return None
    if config.get("retime_track") is not None:
        selector = {"track_id": config["retime_track"]}
    elif config.get("retime_class") is not None:
        selector = {"label_class": config["retime_class"]}
    else:
        return None
    return {**selector, "time_shift_s": shift, "speed_scale": scale}


def retime_not_applied(entry: dict) -> str | None:
    """A retiming that matched no actor would leave the scene as recorded and
    the run labelled with a change it never had: the runtime logs one line per
    retimed actor, and one must name the requested actor or class."""
    request = retime_request(entry["config"])
    if request is None:
        return None
    log = run_dir(entry) / "txt-logs" / "runtime_worker_0.log"
    if "track_id" in request:
        marker = f"Retimed actor {request['track_id']} ("
        what = f"actor {request['track_id']}"
    else:
        marker = f"({request['label_class']}): time_shift_s="
        what = f"{request['label_class']} actor"
    if log.is_file() and marker in log.read_text(encoding="utf-8", errors="replace"):
        return None
    return f"retime_not_applied: no {what} was retimed"


def requested_controller(config: dict) -> str:
    """The controller config the run asks for (knobs.CONTROLLERS). Entries
    queued without a controller key ran the linear MPC, the only controller
    run_experiment.py launched before 7 Oct 2026."""
    return config.get("controller", DEFAULT_CONTROLLER)


def resolved_controller(block: dict) -> str:
    """The controller config whose identifying values the resolved controller
    block of wizard-config.yaml has, or "unknown"."""
    return next(
        (
            name
            for name, spec in CONTROLLERS.items()
            if all(block.get(k) == v for k, v in spec["resolved"].items())
        ),
        "unknown",
    )


def rule_label(config: dict) -> dict:
    """The label the promoted rules read: the run's config, with the
    controller it asked for."""
    return {**config, "controller": requested_controller(config)}


def seed_request(config: dict) -> int | None:
    """The run's seed, or None for a seed the runtime draws at random. A seeded
    run is replayable: the runtime opens its driver and traffic sessions with
    the seed, and VaVAM draws each plan's noise from it (force_determinism).
    Entries queued before seeded runs (7 Oct 2026), and runs of a study whose
    plan says `"seeded": false`, have no seed."""
    return config.get("seed")


def seed_not_logged(entry: dict) -> str | None:
    """A seed that reached the config but not the sessions would label the run
    replayable when it is not. The log records the seed each session was opened
    with; the scored rollout is the spec's first, so it gets the seed itself."""
    seed = seed_request(entry["config"])
    if seed is None:
        return None
    try:
        logged = session_seeds(run_dir(entry))
    except FileNotFoundError as exc:
        return f"seed_not_logged: no rollout log ({exc})"
    if logged != {"driver": seed, "traffic": seed}:
        return f"seed_not_logged: requested {seed}, sessions opened with {logged}"
    return None


def ego_speed_request(config: dict) -> float:
    """How many times its recorded speed the ego has when the policy takes
    over (AlpaSim's ego_speed_scale). Entries queued before 7 Oct 2026 have no
    ego_speed_scale: 1.0, the recorded speed."""
    return config.get("ego_speed_scale", 1.0)


# A second AlpaSim checkout beside this one whose VaVAM driver has the
# diagnostic `mirror` switch (the scene mirrored left to right); only runs
# that ask for it launch from there (run_experiment.launch_root).
MIRROR_CHECKOUT = ROOT.parent / "alpasim-mirror"
MIRROR_MARKER = "VAM mirror: on"


def mirror_request(config: dict) -> bool:
    """Whether VaVAM drives the mirrored scene. Entries without the key do
    not."""
    return config.get("mirror", False)


def mirror_not_applied(entry: dict) -> str | None:
    """A mirrored run's driver logs MIRROR_MARKER when it loads; any other
    run's must not, so a run cannot come from the wrong checkout unseen."""
    log = console_log(entry)
    logged = log.is_file() and MIRROR_MARKER in log.read_text(
        encoding="utf-8", errors="replace"
    )
    if logged != mirror_request(entry["config"]):
        return (
            f"mirror_not_applied: requested {mirror_request(entry['config'])}, "
            f"driver {'logged' if logged else 'did not log'} '{MIRROR_MARKER}'"
        )
    return None


def ego_speed_not_applied(entry: dict) -> str | None:
    """A retimed ego is checked by its own measurement: the runtime logs one
    "Retimed ego" line with the scale, and the ego's speed just before the
    hand-off must be the scale times the recorded ego's there."""
    scale = ego_speed_request(entry["config"])
    if scale == 1.0:
        return None
    log = run_dir(entry) / "txt-logs" / "runtime_worker_0.log"
    marker = f"Retimed ego: speed_scale={float(scale)},"
    if not (
        log.is_file() and marker in log.read_text(encoding="utf-8", errors="replace")
    ):
        return f"ego_speed_not_applied: no '{marker}' in the runtime log"
    try:
        ego, recorded = handoff_speeds(run_dir(entry), scale)
    except FileNotFoundError as exc:
        return f"ego_speed_not_applied: no rollout log ({exc})"
    if not handoff_speed_matches(ego, recorded, scale):
        return (
            f"ego_speed_not_applied: ego at {ego:.2f} m/s before the hand-off, "
            f"{scale} x the recorded {recorded:.2f} m/s is {scale * recorded:.2f}"
        )
    return None


# The control step every run used before 9 Oct 2026, and the rollout length
# it gave (120 steps). A run that sets another step keeps the rollout length.
LEGACY_CONTROL_TIMESTEP_US = 100_000
ROLLOUT_US = 12_000_000


def control_timestep_us(config: dict) -> int:
    """How often the driver plans and the controller acts. AlpaSim's own
    VaVAM setup uses 500 ms, with the camera in step."""
    return config.get("control_timestep_us", LEGACY_CONTROL_TIMESTEP_US)


def n_sim_steps(config: dict) -> int:
    return ROLLOUT_US // control_timestep_us(config)


def frame_interval_us(config: dict) -> int:
    return config.get("frame_interval_us", LEGACY_FRAME_INTERVAL_US)


def subsample_factor(config: dict) -> int:
    """Every how-many-th frame VaVAM's context takes, for 500 ms spacing."""
    return VAVAM_FRAME_SPACING_US // frame_interval_us(config)


def config_not_landed(entry: dict) -> list[str]:
    """Requested values that differ from what the wizard resolved."""
    path = run_dir(entry)
    config = entry["config"]
    driver = yaml.safe_load((path / "driver-config.yaml").read_text(encoding="utf-8"))
    wizard = yaml.safe_load((path / "wizard-config.yaml").read_text(encoding="utf-8"))
    resolved = {
        "context_length": driver["inference"]["context_length"],
        "planner_delay_us": extract_resolved_config(path)["planner_delay_us"],
        "scene_file": wizard["scenes"]["scenes_csv"],
        "scene_id": wizard["scenes"]["scene_ids"],
        "traffic": "replay"
        if wizard["runtime"]["endpoints"]["trafficsim"]["skip"]
        else "catk",
        "actor_retiming": [
            {k: str(v) if k == "track_id" else v for k, v in rule.items()}
            for rule in wizard["runtime"]["simulation_config"]
            .get("actor_retiming", {})
            .get("rules", [])
        ],
        "frame_interval_us": wizard["runtime"]["simulation_config"]["cameras"][0][
            "frame_interval_us"
        ],
        "subsample_factor": driver["inference"]["subsample_factor"],
        "controller": resolved_controller(wizard["controller"]),
        # AlpaSim writes these two only when a launch sets them
        # (run_experiment.seed_args).
        "seed": wizard["runtime"]["simulation_config"].get("random_seed"),
        "force_determinism": driver["model"].get("force_determinism", False),
        # Written only when a launch sets it (run_experiment.ego_args).
        "ego_speed_scale": wizard["runtime"]["simulation_config"].get(
            "ego_speed_scale", 1.0
        ),
        # Written only by a mirrored launch (run_experiment.mirror_args).
        "mirror": driver["model"].get("mirror", False),
        "control_timestep_us": wizard["runtime"]["simulation_config"][
            "control_timestep_us"
        ],
        "n_sim_steps": wizard["runtime"]["simulation_config"]["n_sim_steps"],
    }
    # AlpaSim writes the plan-corruption block only when a launch sets it.
    injected = wizard["runtime"]["simulation_config"].get("fault_injection", {})
    for key in PLAN_KEYS:
        resolved[key] = injected.get(key, 0.0) if injected.get("enabled") else 0.0
    requested = {
        "context_length": config["context_length"],
        "planner_delay_us": config["planner_delay_us"],
        "scene_file": [str(ROOT / config["scene_file"])],
        "scene_id": [config["scene_id"]],
        "traffic": traffic_mode(config),
        "actor_retiming": [r] if (r := retime_request(config)) else [],
        "frame_interval_us": frame_interval_us(config),
        "subsample_factor": subsample_factor(config),
        "controller": requested_controller(config),
        "seed": seed_request(config),
        "force_determinism": seed_request(config) is not None,
        "ego_speed_scale": ego_speed_request(config),
        "mirror": mirror_request(config),
        "control_timestep_us": control_timestep_us(config),
        "n_sim_steps": n_sim_steps(config),
        **{key: plan_request(config)[key] for key in PLAN_KEYS},
    }
    # The CATK device only exists when CATK runs.
    keys = [k for k in CONFIG_KEYS if k != "trafficsim_device"]
    if requested["traffic"] == "catk":
        keys.append("trafficsim_device")
        requested["trafficsim_device"] = config["trafficsim_device"]
        resolved["trafficsim_device"] = wizard["trafficsim"]["catk"]["device"]
    extra = (
        "traffic",
        "actor_retiming",
        "frame_interval_us",
        "subsample_factor",
        "controller",
        "seed",
        "force_determinism",
        "ego_speed_scale",
        "mirror",
        "control_timestep_us",
        "n_sim_steps",
    )
    return [
        f"{key} requested {requested[key]}, resolved {resolved[key]}"
        for key in (*keys, *extra, *PLAN_KEYS)
        if requested[key] != resolved[key]
    ]


def read_state(entry: dict) -> RunState:
    if entry["resolution"] is not None:
        return RunState(State.DONE, f"resolved: {entry['resolution']}")

    problem = config_problem(entry["config"])
    if problem is not None:
        return RunState(State.FAILED, f"preflight_rejected: {problem}")

    if not entry["launched"]:
        if entry["environment"]:
            return RunState(
                State.FAILED, "environment: " + "; ".join(entry["environment"])
            )
        return RunState(State.READY, "preflight_ok")

    code = _exit_code(entry)
    if code is None:
        if entry["pid"] is not None and launcher_alive(entry):
            return RunState(State.RUNNING, f"pid {entry['pid']}")
        return RunState(State.FAILED, "process_lost: launcher gone, no exit code")

    status = validate_postflight(str(run_dir(entry)))
    failures = []
    if code != 0:
        failures.append(f"wizard_exit_code: {code}")
    if not status.success:
        failures.append(f"postflight_failed: {status.error}")
    if failures:
        return RunState(State.FAILED, "; ".join(failures))

    mismatches = config_not_landed(entry)
    if mismatches:
        return RunState(State.FAILED, "config_not_landed: " + "; ".join(mismatches))

    unapplied = retime_not_applied(entry)
    if unapplied is not None:
        return RunState(State.FAILED, unapplied)

    ego_speed = ego_speed_not_applied(entry)
    if ego_speed is not None:
        return RunState(State.FAILED, ego_speed)

    unseeded = seed_not_logged(entry)
    if unseeded is not None:
        return RunState(State.FAILED, unseeded)

    unmirrored = mirror_not_applied(entry)
    if unmirrored is not None:
        return RunState(State.FAILED, unmirrored)

    broken = violations(load_rules(), run_dir(entry), rule_label(entry["config"]))
    if broken:
        return RunState(State.FAILED, "rule_violated: " + "; ".join(broken))

    bounds = load_bounds()
    if bounds["enabled"]:
        implausible = physics_problems(
            run_dir(entry), bounds, plan_request(entry["config"])
        )
        if implausible:
            return RunState(State.FAILED, "; ".join(implausible))

    return RunState(
        State.COMPLETE,
        f"postflight_success: at_fault={status.at_fault_collision}, "
        f"rear={status.rear_contact}",
    )


def main() -> int:
    entry = load_entry(Path(sys.argv[1]))
    result = read_state(entry)
    print(json.dumps({"state": result.state.value, "k_status": result.k_status}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
