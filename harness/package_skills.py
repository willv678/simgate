"""Package SimGate's markdown contracts as Claude Agent Skills.

Each contract in advisor/ becomes a skill folder under research/.claude/skills/
(the place Claude Code loads project skills from): a SKILL.md with the
Agent Skills frontmatter (name, description), the contract unchanged, and the
scripts that check and act on its answer. advisor/ stays the source the
harness calls; this writes the package from it, and --check fails when the
package is out of date.

    uv run python research/harness/package_skills.py [--check]
"""

import argparse
import shutil
import sys
from pathlib import Path

HARNESS = Path(__file__).resolve().parent
ADVISOR = HARNESS / "advisor"
OUT = HARNESS.parent / ".claude" / "skills"

H = "uv run python research/harness"
SKILLS = {
    "simgate": {
        "contract": "OPERATE.md",
        "description": (
            "Run autonomous-driving stress-testing studies with SimGate on AlpaSim: "
            "check the machine, write and plan a brief, queue studies, watch them, "
            "compare search methods, make case cards, export OpenSCENARIO. Use when "
            "a person asks to stress-test the driving policy, to check on studies, "
            "or to show what SimGate found."
        ),
        "scripts": [],
    },
    "simgate-diagnose": {
        "contract": "CLAUDE.md",
        "description": (
            "Choose one recovery (CONFIGURE, RE-RUN, RESTART_CLEANUP, CLEANUP_ENV, "
            "HALT) for an AlpaSim run that SimGate marked FAILED. Use when given a "
            "failed run's status: state FAILED, k_status, config, attempt, "
            "error_lines."
        ),
        "scripts": [
            ("asks", f"{H}/diagnose.py <entry.json> --policy agent"),
            ("checks the answer", f"{H}/validate_diagnosis.py <entry.json>"),
            ("acts on it", f"{H}/recover.py <entry.json>"),
            ("proves the menu safe", f"{H}/verify_supervisor.py"),
        ],
    },
    "simgate-plan": {
        "contract": "PLAN.md",
        "description": (
            "Turn a researcher's SimGate brief (a question about the driving policy, "
            "scope, budget, what counts) into a study plan: scenes, knobs, rounds, "
            "goal. Use when given a brief with the knob catalogue and the scenes."
        ),
        "scripts": [
            ("asks and checks the plan", "research/simgate plan <category>/<name>"),
            ("runs it", "research/simgate queue <category>/<name> --proposer <methods>"),
        ],
    },
    "simgate-propose": {
        "contract": "OUTER.md",
        "description": (
            "Choose the next round of runs in a SimGate study from the runs so far, "
            "per-setting failure ranges and the goal's status. Use when given a "
            "study's objective, knobs, candidate scenes and run history."
        ),
        "scripts": [
            ("asks, checks every run (legal values, candidate scenes) and queues the legal ones",
             f"{H}/outer.py <study> --proposer llm"),
        ],
        "extra": {"OUTER_V2.md": "v2.md"},
    },
    "simgate-audit": {
        "contract": "AUDIT.md",
        "description": (
            "Audit a finished batch of AlpaSim runs for runs whose data should not "
            "be trusted although each passed its per-run checks, and propose rules "
            "that would catch them. Use when given batch.json and runs/<id>/ folders."
        ),
        "scripts": [
            ("asks; `promote.py` admits a proposed rule only if it catches the flagged "
             "runs and no clean run, and `rules.py` then checks it on every later run",
             f"{H}/audit.py <queue dir>"),
        ],
    },
    "simgate-triage": {
        "contract": "TRIAGE.md",
        "description": (
            "Say what happened in one failed AlpaSim run (a collision or leaving the "
            "road): cause from a fixed list, whether the policy was at fault, one "
            "paragraph. Use when given frames before the failure and its metrics."
        ),
        "scripts": [("asks for every failure of a study", f"{H}/triage.py research/studies/<study>")],
    },
    "simgate-tag-scene": {
        "contract": "TAGS.md",
        "description": (
            "Tag a recorded driving scene with its stress-test categories (road "
            "type, traffic, route, pedestrian, cut-in, lead vehicle). Use when given "
            "three frames of an AlpaSim scene."
        ),
        "scripts": [
            ("asks", f"{H}/scene_tags.py"),
            ("compares with tags computed from the recorded tracks", f"{H}/scene_tags.py --compare 10"),
        ],
    },
    "simgate-report": {
        "contract": "REPORT.md",
        "description": (
            "Answer a SimGate brief from its study's results, citing setting ids "
            "(Python writes the counts). Use when given a finished study's brief, "
            "plan, results table and triage."
        ),
        "scripts": [("asks and renders report.md", f"{H}/study.py <brief> --report-only")],
    },
}


def skill_md(name: str, spec: dict) -> str:
    contract = (ADVISOR / spec["contract"]).read_text(encoding="utf-8")
    text = f"---\nname: {name}\ndescription: {spec['description']}\n---\n\n{contract}"
    if spec["scripts"]:
        text += "\n## Scripts\n\nYou answer; code checks and acts. From the AlpaSim repository root:\n\n"
        text += "".join(f"- {what}: `{command}`\n" for what, command in spec["scripts"])
    for source, target in spec.get("extra", {}).items():
        text += f"\nA second version of this contract, used by the `*_v2` methods, is in `{target}`.\n"
    return text


def package() -> dict[Path, str]:
    files = {}
    for name, spec in SKILLS.items():
        files[OUT / name / "SKILL.md"] = skill_md(name, spec)
        for source, target in spec.get("extra", {}).items():
            files[OUT / name / target] = (ADVISOR / source).read_text(encoding="utf-8")
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="fail if the package is out of date")
    args = parser.parse_args()
    files = package()
    if args.check:
        stale = [p for p, text in files.items() if not p.is_file() or p.read_text(encoding="utf-8") != text]
        extra = {p for p in OUT.rglob("*") if p.is_file()} - set(files)
        for path in [*stale, *sorted(extra)]:
            print(f"out of date: {path.relative_to(HARNESS.parent)}")
        return 1 if stale or extra else 0
    shutil.rmtree(OUT, ignore_errors=True)
    for path, text in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        print(path.relative_to(HARNESS.parent))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
