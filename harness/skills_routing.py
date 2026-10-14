"""Do the packaged Agent Skills work when Claude must choose them itself?

The harness hands each contract to Claude as its whole system prompt, so
Claude never chooses. Here Claude Code gets the eight packaged skills
(package_skills.py) and nothing else: no system prompt from us, no tools
but Skill, and one real SimGate input on stdin with the same instruction for
every input. Per input it records which skill Claude loaded and whether its
answer passes the same code check the harness applies:

- diagnose: stored inputs of failed runs, a few per kind of failure and
  recorded recovery; checked by validate_diagnosis.rejection, compared with
  the recovery the harness's own call chose;
- plan: the planner's input for briefs; checked by study.plan_problems;
- propose: a round's input rebuilt from a finished llm arm after 20 runs;
  every proposed run checked by knobs.rejection.

Writes skills_routing.json.

    uv run python research/harness/skills_routing.py
"""

import json
import random
import shutil
import subprocess
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import outer
from goals import goal_status
from knobs import CONTROLLERS, DESCRIPTIONS, SCENARIO, rejection
from package_skills import OUT as SKILLS
from read_state import ROOT
from study import MAX_PER_ROUND, MAX_RUNS, plan_problems, study_of, tagged_scenes
from validate_diagnosis import rejection as diagnosis_rejection

RESEARCH = ROOT / "research"
MODEL = "claude-opus-5-5"
PROMPT = (
    "SimGate sent the input on stdin. Use the SimGate skill that fits it, and "
    "give that skill's answer as one JSON object and nothing else."
)
PER_KIND = 3
PLAN_BRIEFS = ("categories/lane_keeping", "hard/car_conflicts_3knobs_2hz", "categories/cut_in_merge")
PROPOSE_ARMS = (("cut_in_merge", 2), ("lead_vehicle", 2), ("pedestrian_ego_speed", 2))
PROPOSE_AFTER = 20


def diagnose_inputs() -> list[dict]:
    groups = defaultdict(list)
    for path in sorted((RESEARCH / "studies").glob("*/*/queue/*.json")):
        entry = json.loads(path.read_text(encoding="utf-8"))
        diagnosis = entry.get("diagnosis") if isinstance(entry, dict) else None
        if not diagnosis or "input" not in diagnosis or diagnosis.get("skill") is None:
            continue
        kind = diagnosis["input"]["k_status"].split(":")[0]
        groups[(kind, diagnosis["skill"])].append((entry, diagnosis))
    rng = random.Random(20261014)
    items = []
    for (kind, skill), found in sorted(groups.items()):
        for entry, diagnosis in rng.sample(found, min(PER_KIND, len(found))):
            items.append({"expect": "simgate-diagnose", "kind": f"{kind} / {skill}",
                          "input": diagnosis["input"], "recorded": skill, "entry": entry})
    return items


def plan_inputs() -> list[dict]:
    facts = tagged_scenes()
    knobs = {k: {"values": list(v), "meaning": DESCRIPTIONS[k]} for k, v in SCENARIO.items()}
    controllers = {name: spec["meaning"] for name, spec in CONTROLLERS.items()}
    return [
        {"expect": "simgate-plan", "kind": brief,
         "input": {"brief": (RESEARCH / "briefs" / f"{brief}.md").read_text(encoding="utf-8"),
                   "knobs": knobs, "scenes": facts, "controllers": controllers,
                   "max_runs": MAX_RUNS, "max_per_round": MAX_PER_ROUND},
         "scenes": {f["scene_id"] for f in facts}}
        for brief in PLAN_BRIEFS
    ]


def propose_inputs() -> list[dict]:
    items = []
    for name, replicate in PROPOSE_ARMS:
        folder = RESEARCH / "studies" / name
        plan = json.loads((folder / "plan.json").read_text(encoding="utf-8"))["plan"]
        study = study_of(folder / f"llm_r{replicate}", name, plan, "llm", MODEL, replicate)
        past = outer.history(study.queue, study.varied)[:PROPOSE_AFTER]
        table = outer.results(past, study.varied)
        state = {
            "objective": study.objective, "candidates": study.candidates,
            "knobs": {k: {"values": list(SCENARIO[k]), "meaning": DESCRIPTIONS[k]} for k in study.varied},
            "history": past, "summary": table, "goal": study.goal,
            "goal_status": goal_status(study.goal, table, study.varied),
            "round": PROPOSE_AFTER // study.per_round + 1, "rounds": study.rounds,
            "runs_this_round": study.per_round,
        }
        items.append({"expect": "simgate-propose", "kind": name, "input": state,
                      "scenes": {c["scene_id"] for c in study.candidates}, "varied": study.varied})
    return items


def ask(data: dict) -> dict:
    with tempfile.TemporaryDirectory() as work:
        shutil.copytree(SKILLS, Path(work) / ".claude" / "skills")
        proc = subprocess.run(
            ["claude", "-p", PROMPT, "--model", MODEL, "--tools", "Skill",
             "--allowedTools", "Skill", "--setting-sources", "project",
             "--no-session-persistence", "--output-format", "stream-json", "--verbose"],
            input=json.dumps(data, indent=1), cwd=work, capture_output=True,
            text=True, timeout=900, check=False)
    messages = [json.loads(line) for line in proc.stdout.splitlines() if line.strip()]
    loaded = [block["input"].get("skill") for m in messages if m["type"] == "assistant"
              for block in m["message"]["content"]
              if block["type"] == "tool_use" and block["name"] == "Skill"]
    result = next((m for m in reversed(messages) if m["type"] == "result"), None)
    text = (result or {}).get("result") or ""
    start, end = text.find("{"), text.rfind("}")
    try:
        answer = json.loads(text[start:end + 1]) if start >= 0 else None
    except json.JSONDecodeError:
        answer = None
    return {"loaded": loaded, "answer": answer,
            "cost_usd": (result or {}).get("total_cost_usd"),
            "error": None if result else proc.stderr.strip()[-300:]}


def diagnosis_problem(item: dict, skill: str | None, params: dict) -> str | None:
    """validate_diagnosis on the entry as it was when the status was taken:
    an accepted CLEANUP_ENV has since been counted in env_cleanups."""
    stored = item["entry"]
    cleaned = stored["diagnosis"]["skill"] == "CLEANUP_ENV" and stored["diagnosis"].get("verdict") == "accepted"
    entry = {**stored, "attempt": item["input"]["attempt"],
             "env_cleanups": stored["env_cleanups"] - cleaned,
             "diagnosis": {"skill": skill, "params": params}}
    return diagnosis_rejection(entry, item["input"]["k_status"])


def check(item: dict, answer: dict | None) -> str | None:
    """Why the answer would not pass the harness's code check, or None."""
    if not isinstance(answer, dict):
        return "no JSON answer"
    if item["expect"] == "simgate-diagnose":
        return diagnosis_problem(item, answer.get("skill"), answer.get("params", {}))
    if item["expect"] == "simgate-plan":
        plan = answer.get("plan", answer)
        try:
            problems = plan_problems(plan, item["scenes"])
        except (KeyError, TypeError) as missing:
            return f"plan incomplete: {missing}"
        return "; ".join(problems) or None
    runs = answer.get("runs")
    if not isinstance(runs, list) or not runs:
        return "no runs"
    reasons = [r for run in runs if (r := rejection(run, item["scenes"], item["varied"]))]
    return "; ".join(reasons) or None


def main() -> int:
    items = diagnose_inputs() + plan_inputs() + propose_inputs()
    rows = []
    for item in items:
        got = ask(item["input"])
        problem = check(item, got["answer"])
        row = {"expect": item["expect"], "kind": item["kind"], "loaded": got["loaded"], "answer": got["answer"],
               "chose_right": got["loaded"][:1] == [item["expect"]],
               "passes_check": problem is None, "problem": problem,
               "cost_usd": got["cost_usd"], "error": got["error"]}
        if item["expect"] == "simgate-diagnose":
            row["recorded"] = item["recorded"]
            row["same_as_recorded"] = (got["answer"] or {}).get("skill") == item["recorded"]
            row["recorded_passes_check"] = diagnosis_problem(item, item["recorded"], {}) is None
        rows.append(row)
        print(json.dumps({k: row[k] for k in ("expect", "kind", "loaded", "passes_check", "problem")}), flush=True)
    summary = {}
    for expect in sorted({r["expect"] for r in rows}):
        mine = [r for r in rows if r["expect"] == expect]
        summary[expect] = {
            "inputs": len(mine),
            "chose this skill first": sum(r["chose_right"] for r in mine),
            "answer passes the code check": sum(r["passes_check"] for r in mine),
            **({"same recovery as the harness's call": sum(r["same_as_recorded"] for r in mine)}
               if expect == "simgate-diagnose" else {}),
        }
    summary["cost_usd"] = round(sum(r["cost_usd"] or 0 for r in rows), 2)
    (RESEARCH / "skills_routing.json").write_text(
        json.dumps({"summary": summary, "rows": rows}, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
