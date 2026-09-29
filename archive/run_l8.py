"""One wizard launch through the skill menu.

context_length 1 is rejected by preflight and is not launched.
A context_length 8 config is launched into diag/l8_ctx8. If that run writes
no metrics, the recovery skill is RE-RUN: one more launch, with CATK on CPU,
into diag/l8_rerun. The trace names the directory postflight read.
"""

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from policy import decide_recovery
from postflight import validate_postflight
from preflight import PreflightError, validate_preflight
from skills import Skill

ROOT = Path(__file__).resolve().parents[2]
TRACE = ROOT / "research" / "harness" / "l8_trace.jsonl"
FIRST = ROOT / "diag" / "l8_ctx8"
RERUN = ROOT / "diag" / "l8_rerun"


def _scene_file() -> str:
    path = ROOT / "data" / "scenes" / "sim_scenes.csv"
    if not path.is_file():
        raise SystemExit(f"scene file missing: {path}")
    return str(path.relative_to(ROOT))


def _rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def _prior_exit(run_dir_rel: str) -> int | None:
    if not TRACE.is_file():
        return None
    for line in TRACE.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        if row.get("input") == run_dir_rel and "wizard_exit_code" in row:
            return int(row["wizard_exit_code"])
    return None


def _launch(config: dict, log_dir: Path, trafficsim_device: str | None) -> int:
    cmd = [
        "uv",
        "run",
        "alpasim_wizard",
        "deploy=local",
        "topology=1gpu",
        "driver=vavam",
        "trafficsim=catk",
        "controller=linear",
        f"driver.inference.context_length={config['context_length']}",
        "runtime.simulation_config.force_gt_duration_us=4500000",
        "runtime.simulation_config.control_timestep_us=100000",
        "runtime.simulation_config.n_sim_steps=120",
        "runtime.simulation_config.route_start_offset_m=0.0",
        f"runtime.simulation_config.planner_delay_us={config['hydra_delay']}",
        f"wizard.log_dir={log_dir}",
    ]
    if trafficsim_device is not None:
        cmd.append(f"trafficsim.catk.device={trafficsim_device}")
    console = log_dir.parent / f"{log_dir.name}_console.log"
    console.parent.mkdir(parents=True, exist_ok=True)
    print("launching", _rel(log_dir), flush=True)
    with console.open("w", encoding="utf-8") as handle:
        handle.write(" ".join(cmd) + "\n")
        proc = subprocess.run(
            cmd,
            cwd=ROOT,
            stdout=handle,
            stderr=subprocess.STDOUT,
            check=False,
        )
    print(f"wizard exit {proc.returncode}", flush=True)
    return proc.returncode


def _outcome(log_dir: Path, exit_code: int, attempt: int) -> dict:
    rel = _rel(log_dir)
    status = validate_postflight(str(log_dir))
    decision = decide_recovery(None, status, attempt)
    metrics = sorted(log_dir.rglob("metrics.parquet")) if log_dir.is_dir() else []
    record = {
        "input": rel,
        "skill": decision.skill.value,
        "params": {"run_dir": rel},
        "wizard_exit_code": exit_code,
    }
    if status.success and metrics:
        record["k_status"] = (
            f"postflight_success: at_fault={status.at_fault_collision}, "
            f"rear={status.rear_contact}"
        )
        record["at_fault_collision"] = status.at_fault_collision
        record["rear_contact"] = status.rear_contact
        record["metrics"] = str(metrics[0].relative_to(ROOT))
    else:
        record["k_status"] = f"postflight_failed: {status.error}"
    return record


def _reject_context_length_1(scene: str) -> dict:
    rejected = {
        "context_length": 1,
        "hydra_delay": 0,
        "request_delay": 0,
        "scene_file": scene,
    }
    try:
        validate_preflight(rejected)
    except PreflightError as exc:
        decision = decide_recovery(str(exc), None)
        return {
            "input": rejected,
            "skill": decision.skill.value,
            "params": {"config": rejected},
            "k_status": f"preflight_rejected: {exc}",
            "launched": False,
        }
    raise SystemExit("context_length 1 was accepted")


def main() -> int:
    scene = _scene_file()
    accepted = {
        "context_length": 8,
        "hydra_delay": 0,
        "request_delay": 0,
        "scene_file": scene,
    }
    validate_preflight(accepted)

    records = [_reject_context_length_1(scene)]
    records.append(
        {
            "input": accepted,
            "skill": Skill.LAUNCH.value,
            "params": {"run_dir": _rel(FIRST), "config": accepted},
            "k_status": "preflight_ok",
            "launched": True,
        }
    )

    if FIRST.exists():
        exit_code = _prior_exit(_rel(FIRST))
        if exit_code is None:
            raise SystemExit(f"{FIRST} exists but has no recorded exit code")
    else:
        exit_code = _launch(accepted, FIRST, None)

    outcome = _outcome(FIRST, exit_code, 1)
    records.append(outcome)
    final = outcome

    if outcome["skill"] == Skill.RE_RUN.value:
        if RERUN.exists():
            raise SystemExit(f"{RERUN} already exists")
        records.append(
            {
                "input": accepted,
                "skill": Skill.LAUNCH.value,
                "params": {
                    "run_dir": _rel(RERUN),
                    "config": accepted,
                    "trafficsim_device": "cpu",
                },
                "k_status": "preflight_ok",
                "launched": True,
            }
        )
        rerun_exit = _launch(accepted, RERUN, "cpu")
        final = _outcome(RERUN, rerun_exit, 2)
        records.append(final)

    TRACE.write_text(
        "".join(json.dumps(row) + "\n" for row in records), encoding="utf-8"
    )
    print(final["k_status"], flush=True)
    metrics = final.get("metrics")
    return 0 if metrics and Path(ROOT / metrics).is_file() else 1


if __name__ == "__main__":
    raise SystemExit(main())
