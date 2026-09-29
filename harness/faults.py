"""Faults injected on purpose, for the campaign and for replaying B2.

A queue entry may carry `fault`: {"kind": ..., "persistent": bool, ...}.
run_experiment.py applies it; nothing a diagnosing policy reads names it, so a
policy sees only the fault's effects. A persistent fault is copied to the
retry that recover.py queues, like a bug that repeats on every launch.

| kind | injected | effect |
|---|---|---|
| kill | SIGKILL to the wizard after `after_s` | process death, exit 137 |
| hang | `docker pause` of the runtime container after `after_s` | monitor timeout, paused containers left behind |
| delete_metrics | metrics.parquet deleted after the wizard exits | exit 0, no metrics |
| corrupt_metrics | metrics.parquet truncated after the wizard exits | exit 0, unreadable metrics |
| drop_delay | the planner delay override left off the command | exit 0, delay 0 instead of the request |
| fill_network_pool | Docker's address pool filled before the machine check | no network for the run |
"""

import shlex
import subprocess
from pathlib import Path

from environment import NETWORK_SUFFIX

KINDS = (
    "kill",
    "hang",
    "delete_metrics",
    "corrupt_metrics",
    "drop_delay",
    "fill_network_pool",
)
MAX_FAKE_NETWORKS = 256
DELAY_OVERRIDE = "runtime.simulation_config.planner_delay_us="


def fill_network_pool() -> list[str]:
    created = []
    for index in range(MAX_FAKE_NETWORKS):
        name = f"fault_{index}{NETWORK_SUFFIX}"
        proc = subprocess.run(
            ["docker", "network", "create", name], capture_output=True, check=False
        )
        if proc.returncode != 0:
            return created
        created.append(name)
    raise RuntimeError(f"pool still not full after {MAX_FAKE_NETWORKS} networks")


def remove_networks(names: list[str]) -> None:
    for name in names:
        subprocess.run(
            ["docker", "network", "rm", name], capture_output=True, check=False
        )


def before_launch(fault: dict | None) -> None:
    """Faults on the machine, applied once, before the machine check."""
    if (
        fault is not None
        and fault["kind"] == "fill_network_pool"
        and not fault["applied"]
    ):
        fill_network_pool()
        fault["applied"] = True


def wizard_args(fault: dict | None, args: list[str]) -> list[str]:
    if fault is not None and fault["kind"] == "drop_delay":
        return [arg for arg in args if not arg.startswith(DELAY_OVERRIDE)]
    return args


def shell_around(fault: dict | None, log_dir: Path) -> tuple[str, str, str]:
    """Shell text before the wizard command, as its prefix, and after it exits."""
    if fault is None:
        return "", "", ""
    kind = fault["kind"]
    if kind == "kill":
        return "", f"timeout --preserve-status -s KILL {fault['after_s']} ", ""
    if kind == "hang":
        container = shlex.quote(f"{log_dir.name}-runtime-0-1")
        return f"( sleep {fault['after_s']}; docker pause {container} ) & ", "", ""
    target = shlex.quote(str(log_dir))
    if kind == "delete_metrics":
        return "", "", f"find {target} -name metrics.parquet -delete; "
    if kind == "corrupt_metrics":
        return (
            "",
            "",
            f"find {target} -name metrics.parquet -exec truncate -s 16 {{}} +; ",
        )
    return "", "", ""


def new_fault(kind: str, persistent: bool = False, after_s: int | None = None) -> dict:
    if kind not in KINDS:
        raise ValueError(f"unknown fault {kind!r}")
    return {
        "kind": kind,
        "persistent": persistent,
        "after_s": after_s,
        "applied": False,
    }
