"""A queue of studies to run, and the worker that runs them two at a time.

A job is one file in research/jobs/: a brief and a proposer to run it with
(kind "study"), or a brief to plan (kind "plan", no GPU, started at once).
The worker (`simgate worker`, one per machine: it takes an exclusive lock)
starts queued study jobs, oldest first, while fewer than SLOTS simulations
run. It counts every study and every loop outside a study, so a run started
by hand, or by a run_pool script, takes a slot too; while a run_pool script
is alive the worker starts nothing, so two dispatchers never race for a slot.

Each job runs detached (`setsid`), writes its output to <id>.log and its exit
code to <id>.exit, so a job's state is read from files, as the inner loop's
is: queued, running (its launcher alive in this boot), done (exit 0), failed
(another exit code, or the launcher gone without one), cancelled.
"""

import fcntl
import json
import re
import shlex
import subprocess
import time
from datetime import UTC, datetime
from pathlib import Path

from read_state import ROOT, _alive, boot_id

JOBS = ROOT / "research" / "jobs"
BRIEFS = ROOT / "research" / "briefs"
SLOTS = 2
PROPOSERS = (
    "llm",
    "hybrid",
    "rules",
    "grid",
    "bisect",
    "random",
    "lhs",
    "optuna",
    "ga",
)
STUDY = re.compile(r"bin/python[0-9.]* \S*research/harness/study\.py ")
NO_GPU = ("--plan-only", "--report-only")
LOOP_OUTSIDE = re.compile(
    r"bin/python[0-9.]* \S*research/harness/loop\.py \S*research/harness/"
)
POOL = re.compile(r"bash \S*research/harness/run_pool\w*\.sh")


def _now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def _commands() -> list[str]:
    found = []
    for proc in Path("/proc").iterdir():
        if not proc.name.isdigit():
            continue
        try:
            raw = (proc / "cmdline").read_bytes()
        except OSError:
            continue
        found.append(raw.replace(b"\0", b" ").decode(errors="replace").strip())
    return found


def simulations_running(commands: list[str] | None = None) -> int:
    """Studies running (a study with --plan-only does not count: it uses no
    GPU) plus loops outside any study."""
    commands = _commands() if commands is None else commands
    return sum(
        bool(STUDY.search(c) and not any(flag in c for flag in NO_GPU))
        or bool(LOOP_OUTSIDE.search(c))
        for c in commands
    )


def pool_running(commands: list[str] | None = None) -> bool:
    commands = _commands() if commands is None else commands
    return any(POOL.search(c) for c in commands)


def brief_path(brief: str) -> Path:
    """A brief named relative to research/briefs (with or without .md); it
    must exist and stay inside that folder."""
    path = (BRIEFS / brief).with_suffix(".md").resolve()
    if BRIEFS.resolve() not in path.parents or not path.is_file():
        raise ValueError(f"no brief {brief!r} in research/briefs")
    return path


def _write(job: dict) -> None:
    path = JOBS / f"{job['id']}.json"
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(job, indent=1) + "\n", encoding="utf-8")
    tmp.replace(path)


def add(brief: str, proposer: str, kind: str = "study") -> dict:
    """Queue a study job (or a plan job, which `start` runs at once)."""
    if kind not in ("study", "plan"):
        raise ValueError(f"unknown job kind {kind!r}")
    if proposer not in PROPOSERS:
        raise ValueError(f"unknown proposer {proposer!r}")
    path = brief_path(brief)
    JOBS.mkdir(parents=True, exist_ok=True)
    name = str(path.relative_to(BRIEFS).with_suffix(""))
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S%f")
    job = {
        "id": f"{stamp}_{kind}_{path.stem}_{proposer}",
        "kind": kind,
        "brief": name,
        "study": path.stem,
        "proposer": proposer,
        "queued_at": _now(),
        "cancelled": False,
    }
    _write(job)
    return job


def jobs() -> list[dict]:
    """Every job, oldest first, each with its state."""
    if not JOBS.is_dir():
        return []
    found = [json.loads(p.read_text(encoding="utf-8")) for p in JOBS.glob("*.json")]
    return [
        {**job, "state": state(job)} for job in sorted(found, key=lambda j: j["id"])
    ]


def state(job: dict) -> str:
    exit_file = JOBS / f"{job['id']}.exit"
    if exit_file.exists():
        code = exit_file.read_text(encoding="utf-8").strip()
        return "done" if code == "0" else "failed"
    if job["cancelled"]:
        return "cancelled"
    if "pid" not in job:
        return "queued"
    if job["boot_id"] == boot_id() and _alive(job["pid"]):
        return "running"
    return "failed"


def command(job: dict) -> list[str]:
    brief = f"research/briefs/{job['brief']}.md"
    if job["kind"] == "plan":
        return [
            "uv",
            "run",
            "python",
            "research/harness/study.py",
            brief,
            "--plan-only",
        ]
    return [
        "uv", "run", "--with", "optuna", "python", "research/harness/study.py",
        brief, "--proposer", job["proposer"], "--yes",
    ]  # fmt: skip


def start(job: dict) -> dict:
    """Launch a job detached from this process; its exit code lands in
    <id>.exit whatever happens to the worker or the web server."""
    log = JOBS / f"{job['id']}.log"
    exit_file = JOBS / f"{job['id']}.exit"
    script = (
        f"{shlex.join(command(job))} > {shlex.quote(str(log))} 2>&1; "
        f"echo $? > {shlex.quote(str(exit_file))}"
    )
    process = subprocess.Popen(
        ["bash", "-c", script],
        cwd=ROOT,
        start_new_session=True,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    job = {**job, "pid": process.pid, "boot_id": boot_id(), "started_at": _now()}
    _write(job)
    return job


def cancel(job_id: str) -> dict:
    """Cancel a job that has not started; a running study is stopped by a
    person, since stopping it mid-run leaves a run for the loop to diagnose."""
    path = JOBS / f"{job_id}.json"
    if path.parent != JOBS or not path.is_file():
        raise ValueError(f"no job {job_id!r}")
    job = json.loads(path.read_text(encoding="utf-8"))
    if state(job) != "queued":
        raise ValueError(f"job {job_id} is {state(job)}, not queued")
    job["cancelled"] = True
    _write(job)
    return job


def next_job(found: list[dict], running: int, pool: bool) -> dict | None:
    """The job the worker starts now: the oldest queued study job, if a slot
    is free, no run_pool script is dispatching, and no job of the same study
    arm is running (two loops on one arm's queue would refuse each other)."""
    if pool or running >= SLOTS:
        return None
    busy = {(j["study"], j["proposer"]) for j in found if j["state"] == "running"}
    for job in found:
        if (
            job["kind"] == "study"
            and job["state"] == "queued"
            and (job["study"], job["proposer"]) not in busy
        ):
            return job
    return None


def work(poll_s: float = 30, settle_s: float = 60) -> None:
    """Start queued studies as slots free up, until stopped. One worker per
    machine."""
    JOBS.mkdir(parents=True, exist_ok=True)
    lock = open(JOBS / ".worker.lock", "w")  # noqa: SIM115 (held while the worker lives)
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        raise SystemExit("a worker is already running")
    print(f"{_now()} worker started, {SLOTS} slots", flush=True)
    while True:
        commands = _commands()
        job = next_job(jobs(), simulations_running(commands), pool_running(commands))
        if job is None:
            time.sleep(poll_s)
            continue
        start(job)
        print(f"{_now()} started {job['id']}", flush=True)
        # A study takes a while to start its first loop; let it show up in
        # the process table before counting slots again.
        time.sleep(settle_s)
