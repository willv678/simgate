"""SimGate in the browser: write a brief, check its plan, queue it, watch it.

A small local web app over the same files and checks as the command line
(`simgate serve`; standard library only). It writes briefs to
research/briefs, plans with study.py --plan-only, saves a hand-edited plan
only if study.plan_problems passes it, and queues study jobs for the worker
(jobs.py); it never starts a simulation itself. Pages made by study_page.py
and the figures are served as they are.

It listens on 127.0.0.1 only: anyone who can reach it can queue GPU work.
From another machine, tunnel: ssh -L 8765:localhost:8765 <this machine>.
Requests that change anything must carry the X-SimGate header, which a page
from another site cannot send without a preflight this server never answers,
and a Host other than localhost is refused (DNS rebinding).
"""

import fcntl
import json
import re
import subprocess
import sys
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))

import jobs
from compare_proposers import proposer_report
from knobs import CONTROLLERS, DESCRIPTIONS, SCENARIO
from read_state import ROOT
from study import MAX_PER_ROUND, MAX_RUNS, plan_problems, plan_runs, tagged_scenes
from summarize_studies import arms

STUDIES = ROOT / "research" / "studies"
FIGURES = ROOT / "research" / "figures"
PAGE = Path(__file__).resolve().parent / "web" / "index.html"
NAME = re.compile(r"^[a-z0-9][a-z0-9_]{1,60}$")
STATIC = {".html": "text/html", ".png": "image/png", ".svg": "image/svg+xml",
          ".pdf": "application/pdf", ".json": "application/json",
          ".md": "text/plain", ".css": "text/css", ".js": "text/javascript",
          ".mp4": "video/mp4", ".jpg": "image/jpeg"}  # fmt: skip
TEMPLATE = """# {title}

## Question
{question}

## Scope
{scope}

## Budget
About {budget} runs.

## What counts
{counts}
"""


class Refused(Exception):
    """A request the app will not carry out, with the reason shown to the user."""


def briefs() -> list[dict]:
    """Every brief, with the study folder it would run in."""
    found = []
    for path in sorted(jobs.BRIEFS.rglob("*.md")):
        name = str(path.relative_to(jobs.BRIEFS).with_suffix(""))
        found.append(
            {
                "name": name,
                "study": path.stem,
                "planned": (STUDIES / path.stem / "plan.json").exists(),
            }
        )
    return found


def save_brief(name: str, text: str) -> dict:
    """Write research/briefs/<name>.md. A brief whose study has a plan is
    frozen (the study keeps its own copy), and a study folder is named by the
    brief's file name, so two briefs cannot share one."""
    if not NAME.match(name):
        raise Refused("a brief name is lower case letters, digits and _")
    if (STUDIES / name / "plan.json").exists():
        raise Refused(f"study {name} already has a plan; give the brief a new name")
    others = [b for b in briefs() if b["study"] == name and b["name"] != name]
    if others:
        raise Refused(f"research/briefs/{others[0]['name']}.md already uses that name")
    if not text.strip():
        raise Refused("the brief is empty")
    path = jobs.BRIEFS / f"{name}.md"
    path.write_text(text.rstrip() + "\n", encoding="utf-8")
    return {"name": name}


def plan_of(study: str) -> dict:
    path = STUDIES / study / "plan.json"
    if not NAME.match(study) or not path.exists():
        raise Refused(f"study {study!r} has no plan yet")
    plan = json.loads(path.read_text(encoding="utf-8"))["plan"]
    scenes = {f["scene_id"] for f in tagged_scenes()}
    return {
        "plan": plan,
        "runs": plan_runs(plan),
        "problems": plan_problems(plan, scenes),
        "locked": bool(arms(STUDIES / study)),
    }


def save_plan(study: str, plan: dict) -> dict:
    """A person's edit of a plan, kept only if the same checks a model's plan
    must pass find nothing, and only before any proposer has run it."""
    current = plan_of(study)
    if current["locked"]:
        raise Refused("a proposer has run this plan; it can no longer change")
    problems = plan_problems(plan, {f["scene_id"] for f in tagged_scenes()})
    if problems:
        raise Refused("; ".join(problems))
    path = STUDIES / study / "plan.json"
    saved = json.loads(path.read_text(encoding="utf-8"))
    path.write_text(
        json.dumps({**saved, "plan": plan, "edited_by_hand": True}, indent=1) + "\n",
        encoding="utf-8",
    )
    return plan_of(study)


_cache: dict[tuple, dict] = {}


def _signature(folder: Path) -> tuple:
    queue = folder / "queue"
    times = [p.stat().st_mtime for p in queue.glob("*.json")] if queue.is_dir() else []
    return (
        str(folder),
        (folder / "rounds.jsonl").stat().st_mtime,
        max(times, default=0),
    )


def arm_report(folder: Path, plan: dict) -> dict:
    """proposer_report, cached until the arm's rounds or queue change."""
    key = _signature(folder)
    if key not in _cache:
        goal = None if plan["goal"]["type"] == "none" else plan["goal"]
        try:
            report = proposer_report(
                folder, goal, tuple(plan["vary"]), plan["fixed"].get("compare")
            )
            report.pop("goal_progress")
        except Exception as exc:  # noqa: BLE001 (an arm mid-write; shown, retried next poll)
            report = {"error": f"{type(exc).__name__}: {exc}"}
        _cache[key] = report
    return _cache[key]


def running_arms(commands: list[str]) -> set[tuple[str, str]]:
    found = set()
    for c in commands:
        match = re.search(r"study\.py \S*?([\w-]+)\.md( .*)?$", c)
        if match and "--plan-only" not in c and "bin/python" in c:
            proposer = re.search(r"--proposer (\w+)", c)
            replicate = re.search(r"--replicate (\d+)", c)
            arm = proposer.group(1) if proposer else "llm"
            if replicate and replicate.group(1) != "1":
                arm += f"_r{replicate.group(1)}"
            found.add((match.group(1), arm))
    return found


def pool_pending(commands: list[str]) -> set[tuple[str, str]]:
    """The study arms a running run_pool script has yet to start: the jobs in
    its JOBS list without a "<brief> (<proposer>) starting" line in outer.log."""
    pending = set()
    log = tail(ROOT / "research" / "harness" / "outer.log", 100_000)
    for c in commands:
        match = jobs.POOL.search(c)
        if not match:
            continue
        script = ROOT / match.group(0).split(" ", 1)[1]
        if not script.is_file():
            continue
        listed = re.search(
            r"JOBS=\((.*?)\n\)", script.read_text(encoding="utf-8"), re.DOTALL
        )
        for brief, proposer in re.findall(
            r'"([\w/]+) (\w+)"', listed.group(1) if listed else ""
        ):
            if f"{brief} ({proposer}) starting" not in log:
                pending.add((Path(brief).name, proposer))
    return pending


def studies(commands: list[str]) -> list[dict]:
    running = running_arms(commands)
    pending = pool_pending(commands)
    found = []
    for folder in sorted(p for p in STUDIES.iterdir() if (p / "plan.json").exists()):
        plan = json.loads((folder / "plan.json").read_text(encoding="utf-8"))["plan"]
        if "goal" not in plan:
            continue
        found.append(
            {
                "name": folder.name,
                "question": plan["question"],
                "vary": plan["vary"],
                "scenes": len(plan["scenes"]),
                "budget": plan_runs(plan),
                "goal": plan["goal"],
                "page": (folder / "index.html").exists(),
                "report": (folder / "report.md").exists(),
                "arms": {
                    proposer: {
                        **arm_report(arm, plan),
                        "running": (folder.name, proposer) in running,
                        "page": str(arm.relative_to(STUDIES) / "index.html")
                        if (arm / "index.html").exists()
                        else None,
                    }
                    for proposer, arm in arms(folder).items()
                },
                "pool_pending": sorted(
                    proposer for study, proposer in pending if study == folder.name
                ),
            }
        )
    # Studies running now first, then those with results, then plans.
    return sorted(
        found,
        key=lambda s: (
            not any(a.get("running") for a in s["arms"].values()),
            not s["arms"],
            s["name"],
        ),
    )


def gpu() -> dict | None:
    try:
        out = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.used,memory.total,utilization.gpu",
             "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=5, check=True,
        ).stdout  # fmt: skip
    except (OSError, subprocess.SubprocessError):
        return None
    name, used, total, util = [x.strip() for x in out.splitlines()[0].split(",")]
    return {
        "name": name,
        "used_mib": int(used),
        "total_mib": int(total),
        "util": int(util),
    }


def tail(path: Path, lines: int = 40) -> str:
    if not path.is_file():
        return ""
    return "\n".join(
        path.read_text(encoding="utf-8", errors="replace").splitlines()[-lines:]
    )


def state() -> dict:
    commands = jobs._commands()
    return {
        "gpu": gpu(),
        "simulations": jobs.simulations_running(commands),
        "slots": jobs.SLOTS,
        "pool": jobs.pool_running(commands),
        "worker": _worker_alive(),
        "studies": studies(commands),
        "jobs": jobs.jobs()[-50:],
        "briefs": briefs(),
        "activity": tail(ROOT / "research" / "harness" / "outer.log", 25),
    }


def _worker_alive() -> bool:
    lock = jobs.JOBS / ".worker.lock"
    if not lock.exists():
        return False
    with open(lock) as handle:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return True
        fcntl.flock(handle, fcntl.LOCK_UN)
        return False


def results_summary() -> dict:
    """The cross-study numbers analyze_methods.py and gate_report.py wrote,
    or None for each not yet made."""
    found = {
        "gallery": sorted(
            p.stem.removeprefix("gallery_") for p in FIGURES.glob("gallery_*.png")
        )
    }
    for name in ("methods", "gate"):
        path = ROOT / "research" / f"{name}.json"
        found[name] = (
            json.loads(path.read_text(encoding="utf-8")) if path.exists() else None
        )
    return found


def catalog() -> dict:
    tags: dict[str, int] = {}
    for scene in tagged_scenes():
        for tag in scene["tags"]:
            tags[tag] = tags.get(tag, 0) + 1
    return {
        "knobs": {
            k: {"values": list(v), "meaning": DESCRIPTIONS[k]}
            for k, v in SCENARIO.items()
        },
        "categories": dict(sorted(tags.items(), key=lambda kv: -kv[1])),
        "controllers": {k: v["meaning"] for k, v in CONTROLLERS.items()},
        "proposers": list(jobs.PROPOSERS),
        "max_runs": MAX_RUNS,
        "max_per_round": MAX_PER_ROUND,
        "template": TEMPLATE,
    }


def queue(body: dict) -> dict:
    kind = body.get("kind", "study")
    brief = body["brief"]
    study = jobs.brief_path(brief).stem
    if kind == "study":
        if not (STUDIES / study / "plan.json").exists():
            raise Refused("make and check the plan first")
        problems = plan_of(study)["problems"]
        if problems:
            raise Refused("the plan has problems: " + "; ".join(problems))
    job = jobs.add(
        brief, body.get("proposer", "llm"), kind, int(body.get("replicate", 1))
    )
    if kind == "plan":
        job = jobs.start(job)
    return job


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):  # quiet: the page polls every few seconds
        pass

    def _send(self, status: int, body: bytes, kind: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", kind)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, value, status: int = 200) -> None:
        self._send(status, json.dumps(value).encode(), "application/json")

    def _host_ok(self) -> bool:
        host = (self.headers.get("Host") or "").rsplit(":", 1)[0]
        return host in ("localhost", "127.0.0.1", "[::1]")

    def _file(self, base: Path, rest: str) -> None:
        path = (base / rest).resolve()
        if base.resolve() not in path.parents or not path.is_file():
            return self._send(404, b"not found", "text/plain")
        if path.suffix not in STATIC:
            return self._send(404, b"not served", "text/plain")
        self._send(200, path.read_bytes(), STATIC[path.suffix])

    def do_GET(self):
        if not self._host_ok():
            return self._send(403, b"use localhost", "text/plain")
        url = urlparse(self.path)
        query = {k: v[0] for k, v in parse_qs(url.query).items()}
        try:
            if url.path == "/":
                return self._send(200, PAGE.read_bytes(), "text/html; charset=utf-8")
            if url.path == "/api/state":
                return self._json(state())
            if url.path == "/api/catalog":
                return self._json(catalog())
            if url.path == "/api/results":
                return self._json(results_summary())
            if url.path == "/api/brief":
                return self._json(
                    {"text": jobs.brief_path(query["name"]).read_text(encoding="utf-8")}
                )
            if url.path == "/api/plan":
                return self._json(plan_of(query["study"]))
            if url.path == "/api/job_log":
                job_id = query["id"]
                if not re.match(r"^[\w.-]+$", job_id):
                    raise Refused("bad job id")
                return self._json({"log": tail(jobs.JOBS / f"{job_id}.log", 200)})
            if url.path.startswith("/studies/"):
                return self._file(STUDIES, url.path[len("/studies/") :])
            if url.path.startswith("/figures/"):
                return self._file(FIGURES, url.path[len("/figures/") :])
        except (Refused, ValueError, KeyError) as exc:
            return self._json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)
        self._send(404, b"not found", "text/plain")

    def do_POST(self):
        if not self._host_ok() or self.headers.get("X-SimGate") != "1":
            return self._send(403, b"refused", "text/plain")
        url = urlparse(self.path)
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length) or b"{}")
            if url.path == "/api/brief":
                return self._json(save_brief(body["name"], body["text"]))
            if url.path == "/api/plan":
                return self._json(save_plan(body["study"], body["plan"]))
            if url.path == "/api/jobs":
                return self._json(queue(body))
            if url.path == "/api/jobs/cancel":
                return self._json(jobs.cancel(body["id"]))
        except (Refused, ValueError, KeyError, json.JSONDecodeError) as exc:
            return self._json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)
        self._send(404, b"not found", "text/plain")


def export(out: Path) -> None:
    """A read-only snapshot of the app: the page, and the answers of every
    GET it makes as JSON files beside it. Study pages and figures are linked
    where they are in the repository (out must sit one folder below
    research/, as research/site/ does), so GitHub Pages can serve the
    repository as it is."""
    if out.resolve().parent != (ROOT / "research").resolve():
        raise Refused("export to a folder directly under research/, e.g. research/site")
    (out / "api" / "plan").mkdir(parents=True, exist_ok=True)
    snapshot = {**state(), "jobs": [], "worker": False, "pool": False, "gpu": None}
    for study in snapshot["studies"]:
        for arm in study["arms"].values():
            arm["running"] = False
    (out / "api" / "state.json").write_text(json.dumps(snapshot), encoding="utf-8")
    (out / "api" / "catalog.json").write_text(json.dumps(catalog()), encoding="utf-8")
    (out / "api" / "results.json").write_text(
        json.dumps(results_summary()), encoding="utf-8"
    )
    for study in snapshot["studies"]:
        (out / "api" / "plan" / f"{study['name']}.json").write_text(
            json.dumps(plan_of(study["name"])), encoding="utf-8"
        )
    from datetime import date

    page = PAGE.read_text(encoding="utf-8").replace(
        "<script>",
        f"<script>window.SIMGATE_STATIC = {json.dumps(str(date.today()))};</script>"
        "\n<script>",
        1,
    )
    (out / "index.html").write_text(page, encoding="utf-8")


def serve(port: int = 8765) -> None:
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"SimGate at http://localhost:{port}  (Ctrl-C to stop)", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
