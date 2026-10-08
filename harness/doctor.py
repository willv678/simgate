"""Is this machine ready to run SimGate? Each check says what to do if not.

research/simgate doctor
"""

import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from environment import MIN_DISK_FREE_GB, _run
from knobs import SCENE_FILE
from read_state import ROOT

HOOKS = ("actor_retiming.py", "ego_retiming.py")
# Two runs at once need about 11 GB each (environment.MAX_RUNS_IN_FLIGHT).
GPU_TWO_RUNS_MIB = 22_000
GPU_ONE_RUN_MIB = 11_000


def checks() -> list[tuple[str, bool, str]]:
    """(what, ok, detail or what to do) for each requirement."""
    found = []
    runtime = ROOT / "src" / "runtime" / "alpasim_runtime"
    found.append(
        (
            "inside an AlpaSim checkout",
            runtime.is_dir(),
            str(ROOT)
            if runtime.is_dir()
            else "clone this repo as research/ inside "
            "an AlpaSim checkout (https://github.com/NVlabs/alpasim)",
        )
    )
    missing = [h for h in HOOKS if not (runtime / h).is_file()]
    found.append(
        (
            "AlpaSim retiming hooks",
            not missing,
            "present"
            if not missing
            else f"missing {', '.join(missing)}: from the "
            "AlpaSim checkout, git apply research/patches/alpasim-src.diff",
        )
    )
    for tool, fix in (
        ("uv", "install uv: https://docs.astral.sh/uv/"),
        ("docker", "install Docker and the NVIDIA container toolkit"),
        ("claude", "install the Claude Code CLI and log in (`claude`)"),
    ):
        path = shutil.which(tool)
        found.append((f"{tool} on PATH", path is not None, path or fix))
    if shutil.which("docker"):
        info = _run(["docker", "info", "--format", "{{.ServerVersion}}"])
        found.append(
            (
                "docker daemon reachable",
                info.returncode == 0,
                f"server {info.stdout.strip()}"
                if info.returncode == 0
                else "start Docker, and add your user to the docker group",
            )
        )
    gpu = _run(
        ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader,nounits"]
    )
    if gpu.returncode != 0:
        found.append(("NVIDIA GPU", False, "nvidia-smi found no GPU"))
    else:
        name, total = [x.strip() for x in gpu.stdout.splitlines()[0].split(",")]
        total = int(total)
        found.append(
            (
                "NVIDIA GPU",
                total >= GPU_ONE_RUN_MIB,
                f"{name}, {total} MiB: "
                + ("two runs at once" if total >= GPU_TWO_RUNS_MIB
                   else "one run at a time (set environment.MAX_RUNS_IN_FLIGHT=1)"
                   if total >= GPU_ONE_RUN_MIB else "too small for VaVAM"),
            )
        )  # fmt: skip
    scenes = ROOT / SCENE_FILE
    rows = (
        len(scenes.read_text(encoding="utf-8").splitlines()) - 1
        if scenes.is_file()
        else 0
    )
    found.append(
        (
            "AlpaSim scenes",
            rows > 0,
            f"{rows} in {SCENE_FILE}"
            if rows
            else f"no {SCENE_FILE}: download scenes "
            "with research/harness/download_scenes.py",
        )
    )
    tags = Path(__file__).resolve().parent / "scene_tags.json"
    found.append(
        (
            "scene tags",
            tags.is_file(),
            "present" if tags.is_file() else "run research/harness/scene_tags.py",
        )
    )
    diag = ROOT / "diag"
    free = shutil.disk_usage(diag if diag.exists() else ROOT).free // 2**30
    found.append(
        (
            "disk space",
            free >= MIN_DISK_FREE_GB,
            f"{free} GB free (runs need {MIN_DISK_FREE_GB} GB)",
        )
    )
    return found


def main() -> int:
    results = checks()
    for what, ok, detail in results:
        print(f"{'ok ' if ok else 'FIX'}  {what}: {detail}")
    bad = sum(not ok for _, ok, _ in results)
    print("\nready" if not bad else f"\n{bad} to fix before running studies")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
