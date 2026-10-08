"""The machine a run needs, checked before launch and cleaned by CLEANUP_ENV.

A run can fail for a reason outside its own config and directory: another
run's containers still hold the GPU, or leaked Docker networks have used up
the address pool (B2). These are shared by every run, so per-run recovery
cannot fix them.

Cleanup touches only AlpaSim's own leftovers: running containers whose
compose working directory is under this checkout, and networks named
`*_microservices_network` that no running container uses. It assumes no other
wizard run is in flight, as RUNBOOK.md requires. Stopped containers are kept.
"""

import json
import shutil
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NETWORK_SUFFIX = "_microservices_network"
PROBE_NETWORK = "alpasim_env_probe"
# VaVAM plus the renderer used 10,849 MiB on the 12 GB card (FACTS.md, invariant 10).
MIN_GPU_FREE_MIB = 10_500
# Runs of any queues that may share the machine (24 GB GPU, ~11 GB per run).
MAX_RUNS_IN_FLIGHT = 2
GPU_RELEASE_WAIT_S = 60
MIN_DISK_FREE_GB = 20


def _run(cmd: list[str]) -> subprocess.CompletedProcess:
    """A machine command's result; a tool the machine lacks (no docker, no
    nvidia-smi) answers like a shell would, exit code 127, which every check
    reads as a failure and every snapshot records."""
    try:
        return subprocess.run(cmd, capture_output=True, text=True, check=False)
    except FileNotFoundError:
        return subprocess.CompletedProcess(cmd, 127, "", f"{cmd[0]}: not found")


def _running_containers() -> list[dict]:
    out = _run(["docker", "ps", "--format", "{{json .}}"]).stdout
    return [json.loads(line) for line in out.splitlines() if line.strip()]


def alpasim_runs(containers: list[dict]) -> dict[Path, list[str]]:
    """Running containers of wizard runs in this checkout, by run directory
    (the compose project's working directory is the run's log directory)."""
    runs = {}
    for container in containers:
        labels = dict(
            item.split("=", 1) for item in container["Labels"].split(",") if "=" in item
        )
        working_dir = labels.get("com.docker.compose.project.working_dir", "")
        if working_dir.startswith(str(ROOT)):
            runs.setdefault(Path(working_dir), []).append(container["ID"])
    return runs


def _ended(run: Path) -> bool:
    """A run has ended once its exit code is written (read_state.exit_file)."""
    return run.parent.joinpath(f"{run.name}_exit_code").exists()


def stale_container_ids(containers: list[dict]) -> list[str]:
    """Containers of runs that have ended: leftovers, safe to remove."""
    return [
        cid
        for run, ids in alpasim_runs(containers).items()
        if _ended(run)
        for cid in ids
    ]


def in_flight_runs(containers: list[dict]) -> list[Path]:
    """Runs whose containers are up and that have not ended."""
    return [run for run in alpasim_runs(containers) if not _ended(run)]


def _alpasim_networks() -> list[str]:
    out = _run(["docker", "network", "ls", "--format", "{{.Name}}"]).stdout
    return [name for name in out.split() if name.endswith(NETWORK_SUFFIX)]


def _gpu_free_mib() -> int:
    out = _run(
        ["nvidia-smi", "--query-gpu=memory.free", "--format=csv,noheader,nounits"]
    ).stdout
    return int(out.splitlines()[0])


def environment_problems() -> list[str]:
    """Reasons the machine cannot take a run now. Empty when it can."""
    problems = []
    containers = _running_containers()
    stale = stale_container_ids(containers)
    if stale:
        problems.append(f"{len(stale)} AlpaSim containers of ended runs still running")
    in_flight = in_flight_runs(containers)
    if len(in_flight) >= MAX_RUNS_IN_FLIGHT:
        problems.append(
            f"{len(in_flight)} runs already in flight (at most {MAX_RUNS_IN_FLIGHT})"
        )

    probe = _run(["docker", "network", "create", PROBE_NETWORK])
    if probe.returncode == 0:
        _run(["docker", "network", "rm", PROBE_NETWORK])
    else:
        leaked = len(_alpasim_networks())
        problems.append(
            f"docker network create failed ({probe.stderr.strip()[-160:]}); "
            f"{leaked} AlpaSim networks exist"
        )

    gpu_free = _gpu_free_mib()
    # A run's GPU memory can take a few seconds to free after its teardown.
    waited = 0
    while gpu_free < MIN_GPU_FREE_MIB and waited < GPU_RELEASE_WAIT_S:
        time.sleep(5)
        waited += 5
        gpu_free = _gpu_free_mib()
    if gpu_free < MIN_GPU_FREE_MIB:
        problems.append(f"GPU free {gpu_free} MiB < {MIN_GPU_FREE_MIB} MiB")

    disk_free = shutil.disk_usage(ROOT / "diag").free // 2**30
    if disk_free < MIN_DISK_FREE_GB:
        problems.append(f"disk free {disk_free} GB < {MIN_DISK_FREE_GB} GB")
    return problems


def machine_snapshot() -> str:
    """What tier 1's shell tools would show now, recorded when a run fails."""
    sections = []
    for command in (
        ["docker", "ps", "--format", "{{.Names}}\t{{.Status}}"],
        ["docker", "network", "ls", "--format", "{{.Name}}"],
        ["nvidia-smi", "--query-gpu=memory.used,memory.free", "--format=csv"],
        ["df", "-h", str(ROOT / "diag")],
    ):
        out = _run(command).stdout.strip()
        sections.append(f"$ {' '.join(command)}\n{out}")
    return "\n\n".join(sections) + "\n"


def cleanup_environment() -> list[str]:
    """Remove AlpaSim's leftovers: containers of ended runs, and networks no
    container uses (a run in flight keeps its network, which docker refuses to
    remove). Returns what it did."""
    actions = []
    stale = stale_container_ids(_running_containers())
    if stale:
        _run(["docker", "rm", "-f", *stale])
        actions.append(f"removed {len(stale)} running AlpaSim containers")
    removed = [
        name
        for name in _alpasim_networks()
        if _run(["docker", "network", "rm", name]).returncode == 0
    ]
    if removed:
        actions.append(f"removed {len(removed)} AlpaSim networks")
    return actions
