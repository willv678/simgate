"""The outer loop: a study that chooses its own runs, round by round.

Each round a proposer chooses the next runs; knobs.rejection drops any that are
not legal; the rest are queued and run through the inner loop (loop.py), which
keeps a run only if it passes every check and audits the batch. Only kept runs
are evidence. Proposers:

- llm: one headless Claude call per round with no tools (advisor/OUTER.md),
  given the candidates, the legal delays, and the study's history;
- random: uniform over candidates and delays.

The study: how a scene's failure rate changes with the scenario knobs it
varies (`--vary`, from knobs.SCENARIO; planner delay by default). A run failed if
the ego hit something with its front or side, or left the road (metrics).
Candidates are the first `--candidates` scenes S1 kept, in S1's order, each
with what S1's single run at 0 delay showed.

Files, all named after the study: `<study>_queue/` (the inner loop's queue),
`<study>_trace.jsonl` (its trace), `<study>_rounds.jsonl` (one row per round:
the proposals, what was dropped and why, the model call). A rerun finishes the
queue first, then continues from the next round.

    uv run python research/harness/outer.py o1 --proposer llm --rounds 4 --per-round 5
"""

import argparse
import json
import random
import subprocess
import sys
import tempfile
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

from enqueue import RUN_ROOT, add, new_entry
from knobs import DESCRIPTIONS, SCENARIO, rejection, run_config
from read_state import ROOT, load_entry, queue_entries

from physics import completed_rollout

HARNESS = Path(__file__).resolve().parent
CONTRACT = HARNESS / "advisor" / "OUTER.md"
FAILURE_METRICS = ("collision_front", "collision_lateral", "offroad")
TYPES = {"planner_delay_us": "integer", "lateral_bias_m": "number"}


def objective(varied: tuple[str, ...]) -> str:
    return (
        "How does the policy's failure rate on each candidate scene change with "
        + " and ".join(DESCRIPTIONS[knob] for knob in varied)
        + "? Find the fragile scenes and roughly where each breaks."
    )


def schema(varied: tuple[str, ...]) -> dict:
    run = {
        "scene_id": {"type": "string"},
        **{knob: {"type": TYPES[knob]} for knob in varied},
        "why": {"type": "string"},
    }
    return {
        "type": "object",
        "properties": {
            "plan": {"type": "string"},
            "runs": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": run,
                    "required": list(run),
                    "additionalProperties": False,
                },
            },
        },
        "required": ["plan", "runs"],
        "additionalProperties": False,
    }


def outcome(run_dir: Path) -> dict:
    """Failure and the metrics that explain it, from the scored rollout."""
    metrics = pd.read_parquet(completed_rollout(run_dir) / "metrics.parquet")
    peak = metrics.groupby("name")["values"].max()
    worst = metrics.groupby("name")["values"].min()
    return {
        "failed": bool(any(peak[name] > 0 for name in FAILURE_METRICS)),
        **{name: bool(peak[name] > 0) for name in FAILURE_METRICS},
        "min_distance_to_obstacle_m": round(
            float(worst["min_distance_to_obstacle_m"]), 2
        ),
        "progress": round(float(peak["progress"]), 2),
    }


def candidates(count: int) -> list[dict]:
    """The first `count` scenes S1 kept, with its 0-delay run's outcome."""
    found = []
    for path in queue_entries(HARNESS / "s1_queue"):
        entry = load_entry(path)
        if entry["resolution"] != "ACCEPT" or "quarantine" in entry:
            continue
        result = outcome(ROOT / entry["run_dir"])
        found.append(
            {
                "scene_id": entry["config"]["scene_id"],
                "s1_failed_at_0_delay": result["failed"],
                "s1_min_distance_to_obstacle_m": result["min_distance_to_obstacle_m"],
                "s1_progress": result["progress"],
            }
        )
        if len(found) == count:
            break
    return found


def history(queue: Path, varied: tuple[str, ...]) -> list[dict]:
    """Every run of the study: its setting and the gate's verdict; kept runs
    also carry their outcome."""
    rows = []
    for path in queue_entries(queue):
        entry = load_entry(path)
        row = {
            "run": entry["name"],
            "scene_id": entry["config"]["scene_id"],
            **{knob: entry["config"][knob] for knob in varied},
        }
        if "quarantine" in entry:
            row["verdict"] = f"quarantined: {entry['quarantine']}"
        elif entry["resolution"] == "ACCEPT":
            row["verdict"] = "kept"
            row.update(outcome(ROOT / entry["run_dir"]))
        else:
            row["verdict"] = f"not kept: {entry['resolution']}"
        rows.append(row)
    return rows


def planned(queue: Path) -> list[dict]:
    """The study's own runs, not the inner loop's retries of them."""
    if not queue.is_dir():
        return []
    entries = [load_entry(path) for path in queue_entries(queue)]
    return [entry for entry in entries if entry["parent"] is None]


def llm_proposals(
    state: dict, varied: tuple[str, ...], model: str
) -> tuple[dict, dict]:
    """The model's answer and the call's cost, from one headless call."""
    cmd = [
        "claude",
        "-p",
        "The study's state is on stdin. Choose this round's runs.",
        "--model",
        model,
        "--tools",
        "",
        "--setting-sources",
        "",
        "--no-session-persistence",
        "--system-prompt-file",
        str(CONTRACT),
        "--output-format",
        "json",
        "--json-schema",
        json.dumps(schema(varied)),
    ]
    with tempfile.TemporaryDirectory() as empty:
        proc = subprocess.run(
            cmd,
            input=json.dumps(state, indent=1),
            cwd=empty,
            capture_output=True,
            text=True,
            timeout=600,
            check=False,
        )
    if proc.returncode != 0:
        raise SystemExit(f"proposer call failed: {proc.stderr.strip()[-500:]}")
    out = json.loads(proc.stdout)
    if out["is_error"] or out.get("structured_output") is None:
        raise SystemExit(f"proposer gave no answer: {str(out.get('result'))[:500]}")
    usage = out["usage"]
    call = {
        "model": ",".join(out["modelUsage"]),
        "context_tokens": usage["input_tokens"]
        + usage["cache_creation_input_tokens"]
        + usage["cache_read_input_tokens"],
        "output_tokens": usage["output_tokens"],
        "duration_ms": out["duration_ms"],
    }
    return out["structured_output"], call


def random_proposals(
    scenes: list[str], count: int, varied: tuple[str, ...], rng: random.Random
) -> dict:
    return {
        "plan": "uniform over candidates and every varied knob",
        "runs": [
            {
                "scene_id": rng.choice(scenes),
                **{knob: rng.choice(SCENARIO[knob]) for knob in varied},
                "why": "random",
            }
            for _ in range(count)
        ],
    }


def run_inner_loop(study: str, queue: Path) -> None:
    subprocess.run(
        [
            "uv",
            "run",
            "python",
            str(HARNESS / "loop.py"),
            str(queue),
            "--policy",
            "agent",
            "--timeout-min",
            "10",
            "--stall-s",
            "120",
            "--poll-s",
            "5",
            "--audit",
            "--trace",
            str(HARNESS / f"{study}_trace.jsonl"),
        ],
        cwd=ROOT,
        check=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("study")
    parser.add_argument("--proposer", choices=("llm", "random"), required=True)
    parser.add_argument("--rounds", type=int, required=True)
    parser.add_argument("--per-round", type=int, required=True)
    parser.add_argument("--candidates", type=int, default=8)
    parser.add_argument("--model", default="claude-opus-5-5")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument(
        "--vary",
        default="planner_delay_us",
        help="comma-separated scenario knobs the study varies (knobs.SCENARIO)",
    )
    args = parser.parse_args()
    varied = tuple(args.vary.split(","))
    unknown = set(varied) - set(SCENARIO)
    if unknown:
        raise SystemExit(f"unknown knobs {sorted(unknown)}; known: {sorted(SCENARIO)}")

    queue = HARNESS / f"{args.study}_queue"
    rounds_file = HARNESS / f"{args.study}_rounds.jsonl"
    known = candidates(args.candidates)
    scenes = [c["scene_id"] for c in known]
    done = (
        len(rounds_file.read_text(encoding="utf-8").splitlines())
        if rounds_file.exists()
        else 0
    )
    if done:
        run_inner_loop(args.study, queue)

    for round_index in range(done, args.rounds):
        state = {
            "objective": objective(varied),
            "candidates": known,
            "knobs": {
                knob: {"values": list(SCENARIO[knob]), "meaning": DESCRIPTIONS[knob]}
                for knob in varied
            },
            "history": history(queue, varied) if queue.is_dir() else [],
            "round": round_index + 1,
            "rounds": args.rounds,
            "runs_this_round": args.per_round,
        }
        if args.proposer == "llm":
            answer, call = llm_proposals(state, varied, args.model)
        else:
            answer = random_proposals(
                scenes,
                args.per_round,
                varied,
                random.Random(args.seed * 1000 + round_index),
            )
            call = None

        queued, dropped = [], []
        for index, proposed in enumerate(answer["runs"]):
            why_not = (
                "over this round's budget"
                if index >= args.per_round
                else rejection(proposed, set(scenes), varied)
            )
            if why_not:
                dropped.append({**proposed, "dropped": why_not})
                continue
            name = f"{args.study}_{len(planned(queue)) + 1:03d}"
            settings = {knob: proposed[knob] for knob in varied}
            config = run_config(proposed["scene_id"], settings)
            add(queue, new_entry(name, f"{RUN_ROOT}/{name}", config))
            queued.append({**proposed, "run": name})

        row = {
            "round": round_index + 1,
            "proposer": args.proposer,
            "varied": varied,
            "plan": answer["plan"],
            "queued": queued,
            "dropped": dropped,
            "call": call,
        }
        with rounds_file.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(row) + "\n")
        print(
            json.dumps(
                {"round": row["round"], "queued": len(queued), "dropped": len(dropped)}
            )
        )
        run_inner_loop(args.study, queue)

    kept = [row for row in history(queue, varied) if row["verdict"] == "kept"]
    print(
        json.dumps(
            {
                "study": args.study,
                "kept": len(kept),
                "failed": sum(r["failed"] for r in kept),
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
