"""A study from a researcher's brief: plan, runs, and an answer.

A brief is a markdown file with a question in the researcher's own words, as
much or as little detail as they like. Three steps, each the model proposing
and code deciding:

1. plan: one headless Claude call (advisor/PLAN.md) turns the brief into a
   plan; plan_problems() checks every field against the knob catalog, the
   available scenes and the budget caps, and its goal with goals.py; a person
   confirms it unless --yes.
2. run: the outer loop (outer.run_study) runs the plan; every run goes through
   the inner loop and only kept runs count; after every round code checks the
   goal and stops the study once it is met (goal.json).
3. triage: Claude reads video frames around each failure and names its cause
   (triage.py);
4. report: code tabulates the kept runs per setting; one call
   (advisor/REPORT.md) writes the answer, citing setting ids; code renders
   report.md with its own counts next to every finding, so a number in the
   report comes from the table, not the model.

Every run is seeded, so replay.py can re-run it with the same seed, unless
plan.json says `"seeded": false` (a person adds it; the planner does not).

Everything lands in research/studies/<brief name>/: brief.md, plan.json,
queue/, trace.jsonl, rounds.jsonl, goal.json, triage.json, report.md. With
--proposer grid, bisect or random, the same plan runs again with that
proposer in <brief name>/<proposer>/, for comparison. A rerun continues where
the study stopped.

    uv run python research/harness/study.py research/briefs/latency_budget.md
    uv run python research/harness/study.py <brief> --plan-only
    uv run python research/harness/study.py <brief> --report-only
"""

import argparse
import json
import re
import shutil
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from goals import goal_problems
from headless import ask
from knobs import (
    DESCRIPTIONS,
    RETIME_CLASSES,
    SCENARIO,
    TRAFFIC_MODES,
    fixed_problems,
)
from outer import Study, history, results, run_study, scene_facts
from read_state import ROOT, load_entry, queue_entries
from triage import triage_study

HARNESS = Path(__file__).resolve().parent
STUDIES = ROOT / "research" / "studies"
PLANNER = HARNESS / "advisor" / "PLAN.md"
SCENE_TAGS = HARNESS / "scene_tags.json"
REPORTER = HARNESS / "advisor" / "REPORT.md"
MAX_RUNS = 60
MAX_PER_ROUND = 10
MODEL = "claude-opus-5-5"
# "4 of 4", "2/2": counts belong to the rendered table, not the prose.
HAND_COUNT = re.compile(r"\b\d+\s*(?:of|/|out of)\s*\d+\b")
PLAN_SCHEMA = {
    "type": "object",
    "properties": {
        "question": {"type": "string"},
        "objective": {"type": "string"},
        "vary": {"type": "array", "items": {"type": "string"}},
        "scenes": {"type": "array", "items": {"type": "string"}},
        "rounds": {"type": "integer"},
        "per_round": {"type": "integer"},
        "rationale": {"type": "string"},
        "fixed": {
            "type": "object",
            "properties": {
                "traffic": {"type": "string", "enum": list(TRAFFIC_MODES)},
                "retime_class": {"type": "string", "enum": list(RETIME_CLASSES)},
                "retime_tracks": {
                    "type": "object",
                    "additionalProperties": {"type": "string"},
                },
            },
            "required": ["traffic"],
            "additionalProperties": False,
        },
        "goal": {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "enum": ["separate", "bracket", "top_k", "none"],
                },
                "k": {"type": "integer"},
                "distinct_scenes": {"type": "boolean"},
                "max_gap": {"type": "number"},
                "scene": {"type": "string"},
                "scenes": {"type": "array", "items": {"type": "string"}},
                "knob": {"type": "string"},
                "low": {"type": "number"},
                "high": {"type": "number"},
                "low_max": {"type": "number"},
                "high_min": {"type": "number"},
            },
            "required": ["type"],
            "additionalProperties": False,
        },
    },
    "required": [
        "fixed",
        "goal",
        "question",
        "objective",
        "vary",
        "scenes",
        "rounds",
        "per_round",
        "rationale",
    ],
    "additionalProperties": False,
}
REPORT_SCHEMA = {
    "type": "object",
    "properties": {
        "answer": {"type": "string"},
        "findings": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "claim": {"type": "string"},
                    "settings": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["claim", "settings"],
                "additionalProperties": False,
            },
        },
        "open": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["answer", "findings", "open"],
    "additionalProperties": False,
}


def plan_problems(plan: dict, scenes: set[str]) -> list[str]:
    """Why a plan may not run; empty when it may."""
    problems = []
    if not plan["vary"] or set(plan["vary"]) - set(SCENARIO):
        problems.append(f"vary must be a non-empty subset of {sorted(SCENARIO)}")
    if len(set(plan["vary"])) != len(plan["vary"]):
        problems.append("vary repeats a knob")
    if not plan["scenes"] or set(plan["scenes"]) - scenes:
        problems.append(f"unknown scenes {sorted(set(plan['scenes']) - scenes)}")
    if not 1 <= plan["per_round"] <= MAX_PER_ROUND:
        problems.append(f"per_round must be 1 to {MAX_PER_ROUND}")
    if plan["rounds"] < 1 or plan["rounds"] * plan["per_round"] > MAX_RUNS:
        problems.append(f"rounds x per_round must be 1 to {MAX_RUNS} runs")
    problems += fixed_problems(plan["fixed"], tuple(plan["vary"]))
    if set(plan["fixed"].get("retime_tracks", {})) - set(plan["scenes"]):
        problems.append("retime_tracks names scenes the plan does not have")
    if plan["goal"]["type"] != "none" and not problems:
        problems += goal_problems(
            plan["goal"], set(plan["scenes"]), tuple(plan["vary"])
        )
    return problems


def tagged_scenes() -> list[dict]:
    """Each scene's facts, with its categories from scene_tags.json and the
    actors a study could retime there. A category the log's rules found counts
    even when Claude's three frames missed it (a pedestrian on screen for a
    few seconds); Claude's other tags count as it gave them."""
    tags = json.loads(SCENE_TAGS.read_text(encoding="utf-8"))
    found = []
    for fact in scene_facts():
        entry = tags.get(fact["scene_id"])
        if entry is None:
            found.append({**fact, "tags": [], "key_actors": {}})
            continue
        facts = entry["facts"]
        pedestrians = sorted(facts["pedestrians_near"], key=lambda p: p["closest_m"])
        key_actors = {
            "lead_vehicle": facts["lead"]["actor"] if facts["lead"] else None,
            "pedestrian": pedestrians[0]["actor"] if pedestrians else None,
            "cut_in": facts["cut_ins"][0]["actor"] if facts["cut_ins"] else None,
            "crossing_vehicle": facts["crossing_vehicles"][0]["actor"]
            if facts["crossing_vehicles"]
            else None,
            "oncoming": facts["oncoming"][0]["actor"] if facts["oncoming"] else None,
        }
        found.append(
            {
                **fact,
                "tags": sorted(set(entry["final_tags"]) | set(entry["rule_tags"])),
                "turn": facts["turn"],
                "key_actors": {k: v for k, v in key_actors.items() if v is not None},
            }
        )
    return found


def make_plan(brief: str, model: str) -> tuple[dict, dict]:
    facts = tagged_scenes()
    data = {
        "brief": brief,
        "knobs": {
            knob: {"values": list(values), "meaning": DESCRIPTIONS[knob]}
            for knob, values in SCENARIO.items()
        },
        "scenes": facts,
        "max_runs": MAX_RUNS,
        "max_per_round": MAX_PER_ROUND,
    }
    prompt = "The brief, the knobs and the scenes are on stdin. Plan the study."
    plan, call = ask(prompt, data, PLANNER, PLAN_SCHEMA, model)
    problems = plan_problems(plan, {f["scene_id"] for f in facts})
    if problems:
        raise SystemExit("the plan was rejected: " + "; ".join(problems))
    return plan, call


def study_of(folder: Path, name: str, plan: dict, proposer: str, model: str) -> Study:
    facts = {f["scene_id"]: f for f in scene_facts()}
    # Plans written before seeded runs have no "seeded"; their new runs are seeded.
    seeded = plan.get("seeded", True)
    if type(seeded) is not bool:
        raise SystemExit(f"plan.json: seeded must be true or false, got {seeded!r}")
    return Study(
        name=name,
        queue=folder / "queue",
        trace=folder / "trace.jsonl",
        rounds_file=folder / "rounds.jsonl",
        objective=plan["objective"],
        candidates=[facts[scene] for scene in plan["scenes"]],
        varied=tuple(plan["vary"]),
        rounds=plan["rounds"],
        per_round=plan["per_round"],
        proposer=proposer,
        model=model,
        goal=None if plan["goal"]["type"] == "none" else plan["goal"],
        fixed=plan["fixed"],
        goal_file=folder / "goal.json",
        seeded=seeded,
    )


def setting_text(row: dict, varied: tuple) -> str:
    knobs = ", ".join(f"{knob} {row[knob]}" for knob in varied)
    low, high = row["failure_rate_90"]
    return (
        f"{row['id']}: {row['scene_id'][7:15]} at {knobs}: "
        f"{row['failed']}/{row['runs']} failed, rate {low:.0%}-{high:.0%} (90%)"
        + (
            f", {row['possible_artifacts']} possibly the simulator's"
            if row["possible_artifacts"]
            else ""
        )
        + f" ({', '.join(row['run_names'])})"
    )


def write_report(
    folder: Path,
    brief: str,
    plan: dict,
    rows: list[dict],
    causes: list[dict],
    model: str,
) -> Path:
    varied = tuple(plan["vary"])
    table = results(rows, varied)
    not_kept = [row for row in rows if row["verdict"] != "kept"]
    triaged = [
        {k: c[k] for k in ("run", "cause", "policy_at_fault", "what_happened")}
        for c in causes
    ]
    goal_file = folder / "goal.json"
    goal = (
        json.loads(goal_file.read_text(encoding="utf-8"))
        if goal_file.exists()
        else None
    )
    data = {
        "brief": brief,
        "question": plan["question"],
        "plan": plan,
        "goal_status": goal,
        "results": table,
        "triage": triaged,
        "not_kept": not_kept,
    }
    prompt = "The brief, the plan and the results are on stdin. Answer the question."
    answer, call = ask(prompt, data, REPORTER, REPORT_SCHEMA, model)
    prose = " ".join([answer["answer"], *(f["claim"] for f in answer["findings"])])
    if HAND_COUNT.search(prose):
        raise SystemExit(
            f"the report writes counts by hand: {HAND_COUNT.findall(prose)}"
        )
    by_id = {row["id"]: row for row in table}
    unknown = {s for f in answer["findings"] for s in f["settings"]} - set(by_id)
    if unknown:
        raise SystemExit(
            f"the report cites settings that do not exist: {sorted(unknown)}"
        )

    lines = [
        f"# {plan['question']}",
        "",
        (
            f"Study `{folder.name}`: {sum(r['runs'] for r in table)} kept runs on "
            f"{len({r['scene_id'] for r in table})} scenes, varying "
            f"{', '.join(varied)}; {len(not_kept)} runs not kept by the gate. "
            "Counts are kept runs only."
        ),
        "",
        (
            f"**Goal (checked by code, not the model):** {goal['verdict']}"
            + (f"; {goal['scenes']}" if goal.get("scenes") else "")
            + f", after {goal['after_rounds']} rounds."
            if goal
            else "**Goal:** none that code can check; the study ran its budget."
        ),
        "",
        "## Answer",
        "",
        answer["answer"],
        "",
        "## Findings",
        "",
    ]
    for finding in answer["findings"]:
        lines.append(f"- {finding['claim']}")
        lines += [f"  - {setting_text(by_id[s], varied)}" for s in finding["settings"]]
    lines += ["", "## Open", ""] + [f"- {item}" for item in answer["open"]]
    if triaged:
        counts = Counter(c["cause"] for c in triaged)
        lines += ["", "## Why the runs failed (triage from the video and log)", ""]
        lines.append(", ".join(f"{cause} {n}" for cause, n in counts.most_common()))
        lines.append("")
        lines += [
            f"- {c['run']}: {c['cause']}, policy at fault: {c['policy_at_fault']}. "
            f"{c['what_happened']}"
            for c in triaged
        ]
    lines += ["", "## Every setting", ""] + [
        f"- {setting_text(r, varied)}" for r in table
    ]
    if not_kept:
        lines += ["", "## Not kept by the gate", ""]
        lines += [f"- {r['run']}: {r['verdict']}" for r in not_kept]
    lines += [
        "",
        "## Provenance",
        "",
        (
            f"Plan: `plan.json` (rationale: {plan['rationale']}). Report written by "
            f"{call['model']} from `results` in {call['duration_ms'] / 1000:.0f} s; "
            "every count above is computed from the queue, not written by the model."
        ),
    ]
    configs = [load_entry(p)["config"] for p in queue_entries(folder / "queue")]
    seeded = sum("seed" in config for config in configs)
    lines += [
        "",
        (
            f"{seeded} of {len(configs)} queued runs are seeded (`seed` in the "
            "run's queue config); `replay.py` queues a kept one again with it."
        ),
    ]
    path = folder / "report.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    (folder / "report.json").write_text(
        json.dumps({"answer": answer, "results": table, "call": call}, indent=1) + "\n",
        encoding="utf-8",
    )
    return path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("brief", type=Path)
    parser.add_argument(
        "--yes", action="store_true", help="run the plan without asking"
    )
    parser.add_argument("--plan-only", action="store_true")
    parser.add_argument("--report-only", action="store_true")
    parser.add_argument("--model", default=MODEL)
    parser.add_argument(
        "--proposer",
        choices=(
            "llm",
            "hybrid",
            "rules",
            "grid",
            "bisect",
            "random",
            "lhs",
            "optuna",
            "ga",
        ),
        default="llm",
        help="who picks the runs; baselines run the same plan in <study>/<proposer>/",
    )
    args = parser.parse_args()

    folder = STUDIES / args.brief.stem
    folder.mkdir(parents=True, exist_ok=True)
    if not (folder / "brief.md").exists():
        shutil.copy(args.brief, folder / "brief.md")
    brief = (folder / "brief.md").read_text(encoding="utf-8")

    plan_file = folder / "plan.json"
    if plan_file.exists():
        plan = json.loads(plan_file.read_text(encoding="utf-8"))["plan"]
    else:
        plan, call = make_plan(brief, args.model)
        plan_file.write_text(json.dumps({"plan": plan, "call": call}, indent=1) + "\n")
    print(json.dumps(plan, indent=1))
    if args.plan_only:
        return 0

    if args.proposer == "bisect" and plan["goal"]["type"] != "bracket":
        raise SystemExit("bisect needs a bracket goal")
    runs = folder if args.proposer == "llm" else folder / args.proposer
    runs.mkdir(exist_ok=True)
    name = folder.name if args.proposer == "llm" else f"{folder.name}_{args.proposer}"
    study = study_of(runs, name, plan, args.proposer, args.model)
    if not args.report_only:
        if not args.yes and input("Run this plan? [y/N] ").strip().lower() != "y":
            return 1
        run_study(study)
    rows = history(study.queue, study.varied)
    triage_file = runs / "triage.json"
    if not triage_file.exists():
        triage_file.write_text(
            json.dumps(triage_study(study.queue, args.model), indent=1) + "\n"
        )
    causes = json.loads(triage_file.read_text(encoding="utf-8"))
    print(f"report: {write_report(runs, brief, plan, rows, causes, args.model)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
