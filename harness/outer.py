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
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

from enqueue import RUN_ROOT, add, new_entry
from goals import goal_status
from headless import ask
from knobs import DESCRIPTIONS, SCENARIO, rejection, run_config
from read_state import ROOT, load_entry, queue_entries

from physics import completed_rollout, signals

HARNESS = Path(__file__).resolve().parent
CONTRACT = HARNESS / "advisor" / "OUTER.md"
SCENE_FACTS = HARNESS / "scene_facts.json"
# About one lane width. Beyond it the reconstruction renders the ego's view
# from further off the recording car's path than it was built from.
FAR_FROM_RECORDING_M = 3.5
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
    """Failure and the metrics that explain it, from the scored rollout. For a
    failed run, also when it failed, how far the ego was from the recorded
    trajectory at that moment, and whether any camera frame was black: far
    from the recording the reconstructed scene renders less reliably, so such
    a failure may be the simulator's rather than the policy's."""
    metrics = pd.read_parquet(completed_rollout(run_dir) / "metrics.parquet")
    peak = metrics.groupby("name")["values"].max()
    worst = metrics.groupby("name")["values"].min()
    found = {
        "failed": bool(any(peak[name] > 0 for name in FAILURE_METRICS)),
        **{name: bool(peak[name] > 0) for name in FAILURE_METRICS},
        "min_distance_to_obstacle_m": round(
            float(worst["min_distance_to_obstacle_m"]), 2
        ),
        "progress": round(float(peak["progress"]), 2),
    }
    if found["failed"]:
        hits = metrics[metrics["name"].isin(FAILURE_METRICS) & (metrics["values"] > 0)]
        when = hits["timestamps_us"].min()
        track = metrics[metrics["name"] == "dist_to_gt_trajectory"]
        at = track.iloc[(track["timestamps_us"] - when).abs().argmin()]
        off = round(float(at["values"]), 1)
        black = bool(peak["img_is_black"] > 0)
        found |= {
            "failed_at_s": round((when - metrics["timestamps_us"].min()) / 1e6, 1),
            "off_recording_at_failure_m": off,
            "black_frames": black,
            "possible_artifact": off > FAR_FROM_RECORDING_M or black,
        }
    return found


def rate_range(failed: int, runs: int, z: float = 1.645) -> tuple[float, float]:
    """The 90% Wilson interval for a failure rate from `failed` of `runs`."""
    p = failed / runs
    centre = (p + z * z / (2 * runs)) / (1 + z * z / runs)
    half = (
        z
        / (1 + z * z / runs)
        * ((p * (1 - p) / runs + z * z / (4 * runs * runs)) ** 0.5)
    )
    return round(max(0.0, centre - half), 2), round(min(1.0, centre + half), 2)


def results(rows: list[dict], varied: tuple) -> list[dict]:
    """Kept runs per setting, numbered for citing: failures, the 90% range of
    the failure rate, and failures that may be the simulator's."""
    cells = defaultdict(list)
    for row in rows:
        if row["verdict"] == "kept":
            cells[(row["scene_id"], *(row[knob] for knob in varied))].append(row)
    table = []
    for index, (key, runs) in enumerate(sorted(cells.items()), start=1):
        failed = sum(run["failed"] for run in runs)
        table.append(
            {
                "id": f"S{index}",
                "scene_id": key[0],
                **dict(zip(varied, key[1:])),
                "runs": len(runs),
                "failed": failed,
                "failure_rate_90": rate_range(failed, len(runs)),
                "possible_artifacts": sum(
                    run.get("possible_artifact", False) for run in runs
                ),
                "run_names": [run["run"] for run in runs],
            }
        )
    return table


def scene_facts() -> list[dict]:
    """What S1 (one run per downloaded scene at 0 delay) showed about each
    scene it kept, in S1's order: whether that run failed, its closest
    approach, progress, top speed and distance driven. Cached in
    scene_facts.json; S1 does not change."""
    if SCENE_FACTS.exists():
        return json.loads(SCENE_FACTS.read_text(encoding="utf-8"))
    found = []
    for path in queue_entries(HARNESS / "s1_queue"):
        entry = load_entry(path)
        if entry["resolution"] != "ACCEPT" or "quarantine" in entry:
            continue
        run = ROOT / entry["run_dir"]
        result = outcome(run)
        metrics = pd.read_parquet(completed_rollout(run) / "metrics.parquet")
        found.append(
            {
                "scene_id": entry["config"]["scene_id"],
                "s1_failed_at_0_delay": result["failed"],
                "s1_min_distance_to_obstacle_m": result["min_distance_to_obstacle_m"],
                "s1_progress": result["progress"],
                "s1_top_speed_mps": round(float(signals(run)["speed"].max()), 1),
                "s1_distance_m": round(
                    float(
                        metrics.loc[
                            metrics["name"] == "dist_traveled_m", "values"
                        ].max()
                    ),
                    1,
                ),
            }
        )
    SCENE_FACTS.write_text(json.dumps(found, indent=1) + "\n", encoding="utf-8")
    return found


def candidates(count: int) -> list[dict]:
    """The first `count` scenes S1 kept, with what S1 showed at 0 delay."""
    return scene_facts()[:count]


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
    prompt = "The study's state is on stdin. Choose this round's runs."
    return ask(prompt, state, CONTRACT, schema(varied), model)


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


@dataclass(frozen=True)
class Study:
    """One study: where its files live and how it chooses runs."""

    name: str
    queue: Path
    trace: Path
    rounds_file: Path
    objective: str
    candidates: list
    varied: tuple
    rounds: int
    per_round: int
    proposer: str
    model: str = "claude-opus-5-5"
    seed: int = 0
    goal: dict | None = None
    goal_file: Path | None = None


def pilot(name: str, candidate_count: int, varied: tuple, **settings) -> Study:
    """A study with its files in the harness folder, as the 6 Oct pilot ran."""
    return Study(
        name=name,
        queue=HARNESS / f"{name}_queue",
        trace=HARNESS / f"{name}_trace.jsonl",
        rounds_file=HARNESS / f"{name}_rounds.jsonl",
        objective=objective(varied),
        candidates=candidates(candidate_count),
        varied=varied,
        **settings,
    )


def run_inner_loop(study: Study) -> None:
    subprocess.run(
        [
            "uv",
            "run",
            "python",
            str(HARNESS / "loop.py"),
            str(study.queue),
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
            str(study.trace),
        ],
        cwd=ROOT,
        check=True,
    )


def run_study(study: Study) -> list[dict]:
    """Propose, check, queue and run every round not yet done; return the
    study's history. A rerun finishes the queue first, then continues."""
    scenes = [c["scene_id"] for c in study.candidates]
    done = (
        len(study.rounds_file.read_text(encoding="utf-8").splitlines())
        if study.rounds_file.exists()
        else 0
    )
    if done:
        run_inner_loop(study)

    for round_index in range(done, study.rounds):
        past = history(study.queue, study.varied) if study.queue.is_dir() else []
        status = check_goal(study, past, round_index)
        if status is not None and status["met"]:
            print(
                json.dumps({"goal met": status["verdict"], "after_rounds": round_index})
            )
            break
        state = {
            "objective": study.objective,
            "candidates": study.candidates,
            "knobs": {
                knob: {"values": list(SCENARIO[knob]), "meaning": DESCRIPTIONS[knob]}
                for knob in study.varied
            },
            "history": past,
            "summary": results(past, study.varied),
            "goal": study.goal,
            "goal_status": status,
            "round": round_index + 1,
            "rounds": study.rounds,
            "runs_this_round": study.per_round,
        }
        if study.proposer == "llm":
            answer, call = llm_proposals(state, study.varied, study.model)
        else:
            answer = random_proposals(
                scenes,
                study.per_round,
                study.varied,
                random.Random(study.seed * 1000 + round_index),
            )
            call = None

        queued, dropped = [], []
        for index, proposed in enumerate(answer["runs"]):
            why_not = (
                "over this round's budget"
                if index >= study.per_round
                else rejection(proposed, set(scenes), study.varied)
            )
            if why_not:
                dropped.append({**proposed, "dropped": why_not})
                continue
            name = f"{study.name}_{len(planned(study.queue)) + 1:03d}"
            settings = {knob: proposed[knob] for knob in study.varied}
            config = run_config(proposed["scene_id"], settings)
            add(study.queue, new_entry(name, f"{RUN_ROOT}/{name}", config))
            queued.append({**proposed, "run": name})

        row = {
            "round": round_index + 1,
            "proposer": study.proposer,
            "varied": study.varied,
            "plan": answer["plan"],
            "queued": queued,
            "dropped": dropped,
            "call": call,
        }
        with study.rounds_file.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(row) + "\n")
        print(
            json.dumps(
                {"round": row["round"], "queued": len(queued), "dropped": len(dropped)}
            )
        )
        run_inner_loop(study)
    else:
        check_goal(study, history(study.queue, study.varied), study.rounds)
    return history(study.queue, study.varied)


def check_goal(study: Study, past: list[dict], rounds_done: int) -> dict | None:
    """The goal's status from the kept runs so far, written to the goal file;
    None for a study without a goal."""
    if study.goal is None:
        return None
    status = goal_status(study.goal, results(past, study.varied), study.varied)
    study.goal_file.write_text(
        json.dumps({**status, "after_rounds": rounds_done}, indent=1) + "\n",
        encoding="utf-8",
    )
    return status


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
    study = pilot(
        args.study,
        args.candidates,
        varied,
        rounds=args.rounds,
        per_round=args.per_round,
        proposer=args.proposer,
        model=args.model,
        seed=args.seed,
    )
    kept = [row for row in run_study(study) if row["verdict"] == "kept"]
    print(
        json.dumps(
            {
                "study": study.name,
                "kept": len(kept),
                "failed": sum(r["failed"] for r in kept),
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
