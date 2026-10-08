"""The outer loop: a study that chooses its own runs, round by round.

Each round a proposer chooses the next runs; knobs.rejection drops any that are
not legal; the rest are queued and run through the inner loop (loop.py), which
keeps a run only if it passes every check and audits the batch. Only kept runs
are evidence. Proposers:

- llm: one headless Claude call per round with no tools (advisor/OUTER.md),
  given the candidates, the legal delays, and the study's history;
- random: uniform over candidates and delays;
- grid and bisect: the status-quo sweep and a scripted binary search
  (baselines.py), for comparison;
- lhs, optuna, ga: Latin-hypercube sampling, Bayesian optimisation (Optuna
  TPE; launch with `uv run --with optuna`) and a genetic algorithm, the last two
  maximising per-run criticality (baselines.py);
- rules: rule-guided search alone (guided.py): confirm near-failures, step
  from the most critical settings;
- hybrid: Claude chooses among the rules' candidates only; any other run is
  dropped.

The study: how a scene's failure rate changes with the scenario knobs it
varies (`--vary`, from knobs.SCENARIO; planner delay by default). A run failed if
the ego hit something with its front or side, or left the road (metrics).
Candidates are the first `--candidates` scenes S1 kept, in S1's order, each
with what S1's single run at 0 delay showed.

An A/B study (study.py, fixed setting `compare`) compares two controllers:
each proposed setting is queued once per controller, a pair with the same
scene and knob values. The proposers search the settings as in any study, on
the table that pools both controllers' runs per setting; the goal and the
report read the table that puts them side by side (results with `compare`).

Files, all named after the study: `<study>_queue/` (the inner loop's queue),
`<study>_trace.jsonl` (its trace), `<study>_rounds.jsonl` (one row per round:
the proposals, what was dropped and why, the model call). A rerun finishes the
queue first, then continues from the next round.

Every run of a seeded study carries a `seed` in its queue config,
from the study's name and the run's number, so replay.py can re-run it with
the same seed.

    uv run python research/harness/outer.py o1 --proposer llm --rounds 4 --per-round 5
"""

import argparse
import hashlib
import json
import random
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

from baselines import (
    bisect_proposals,
    ga_proposals,
    grid_proposals,
    lhs_proposals,
    optuna_proposals,
)
from enqueue import RUN_ROOT, add, new_entry
from goals import goal_status, rate_range
from guided import candidates, outside, rules_proposals, with_confirmation
from headless import ask
from knobs import (
    DEFAULT_CONTROLLER,
    DESCRIPTIONS,
    SCENARIO,
    SIDES,
    rejection,
    run_config,
)
from memory import prior_runs
from read_state import (
    ROOT,
    SEED_LIMIT,
    load_entry,
    queue_entries,
    requested_controller,
)

from physics import completed_rollout, signals

HARNESS = Path(__file__).resolve().parent
CONTRACT = HARNESS / "advisor" / "OUTER.md"
SCENE_FACTS = HARNESS / "scene_facts.json"
# About one lane width. Beyond it the reconstruction renders the ego's view
# from further off the recording car's path than it was built from.
FAR_FROM_RECORDING_M = 3.5
# Closest approach below which a run that did not fail counts as a near miss.
NEAR_MISS_M = 5.0
# A failure is the policy's: off the road, or a front or side collision that
# began before any rear contact, counted from the first step the policy
# drove (AlpaSim's eval_relevant; its evaluator drops the force-GT warm-up the
# same way, "warmup frames that produce spurious metric events"). A collision
# that starts at the ego's rear is the follower's (nuPlan counts it not at
# fault): replayed traffic follows its recording and cannot brake for an ego
# that drives slower than the human did. `failed_any` keeps the broad reading
# (any front, side or off-road flag at any time) used before 8 Oct 2026.
FAILURE_METRICS = ("collision_front", "collision_lateral", "offroad")
TYPES = {
    "planner_delay_us": "integer",
    "lateral_bias_m": "number",
    "waypoint_noise_std": "number",
    "actor_time_shift_s": "number",
    "actor_speed_scale": "number",
    "ego_speed_scale": "number",
}


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


def _first(metrics: pd.DataFrame, name: str, since_us: float) -> float:
    """When metric `name` first flags at or after `since_us`; inf if never."""
    hits = metrics[
        (metrics["name"] == name)
        & (metrics["values"] > 0)
        & (metrics["timestamps_us"] >= since_us)
    ]
    return float(hits["timestamps_us"].min()) if len(hits) else float("inf")


def outcome(run_dir: Path) -> dict:
    """Failure and the metrics that explain it, from the scored rollout (the
    failure definition above FAILURE_METRICS). For a failed run, also when it
    failed, how far the ego was from the recorded trajectory at that moment,
    and whether any camera frame was black: far from the recording the
    reconstructed scene renders less reliably, so such a failure may be the
    simulator's rather than the policy's. The closest approach counts from the
    policy's first step until any rear contact."""
    metrics = pd.read_parquet(completed_rollout(run_dir) / "metrics.parquet")
    relevant = metrics[metrics["name"] == "eval_relevant"]
    driven = float(relevant.loc[relevant["values"] > 0, "timestamps_us"].min())
    start = float(metrics["timestamps_us"].min())
    peak = metrics.groupby("name")["values"].max()
    side_or_front = min(
        _first(metrics, "collision_front", driven),
        _first(metrics, "collision_lateral", driven),
    )
    rear = _first(metrics, "collision_rear", driven)
    offroad = _first(metrics, "offroad", driven)
    at_fault = side_or_front if side_or_front < rear else float("inf")
    when = min(at_fault, offroad)
    window = metrics[
        (metrics["name"] == "min_distance_to_obstacle_m")
        & (metrics["timestamps_us"] >= driven)
        & (metrics["timestamps_us"] < rear)
    ]
    found = {
        "failed": when < float("inf"),
        "collision_at_fault": at_fault < float("inf"),
        "offroad": offroad < float("inf"),
        "rear_ended": rear < float("inf"),
        "failed_any": bool(any(peak[name] > 0 for name in FAILURE_METRICS)),
        "handoff_s": round((driven - start) / 1e6, 1),
        "min_distance_to_obstacle_m": round(float(window["values"].min()), 2)
        if len(window)
        else None,
        "progress": round(float(peak["progress"]), 2),
    }
    found["criticality"] = criticality(
        found["failed"], found["min_distance_to_obstacle_m"]
    )
    if found["failed"]:
        track = metrics[metrics["name"] == "dist_to_gt_trajectory"]
        at = track.iloc[(track["timestamps_us"] - when).abs().argmin()]
        off = round(float(at["values"]), 1)
        black = bool(peak["img_is_black"] > 0)
        found |= {
            "failed_at_s": round((when - start) / 1e6, 1),
            "off_recording_at_failure_m": off,
            "black_frames": black,
            "possible_artifact": off > FAR_FROM_RECORDING_M or black,
        }
    return found


def criticality(failed: bool, min_distance_m: float | None) -> float:
    """How close a run came to failing, in [0, 1]: 1 for a failure; otherwise
    the closest approach to another actor, 0.9 at contact falling linearly to 0
    at NEAR_MISS_M (0 when the ego was rear-ended before it drove a step).
    Ranks settings by how challenging they are."""
    if failed:
        return 1.0
    if min_distance_m is None:
        return 0.0
    return round(0.9 * max(0.0, 1.0 - min_distance_m / NEAR_MISS_M), 3)


def tally(runs: list[dict]) -> dict:
    """Kept runs of one setting: failures, the 90% range of the failure rate,
    failures that may be the simulator's, and mean criticality (None without
    runs)."""
    failed = sum(run["failed"] for run in runs)
    return {
        "runs": len(runs),
        "failed": failed,
        "failure_rate_90": rate_range(failed, len(runs)),
        "possible_artifacts": sum(run.get("possible_artifact", False) for run in runs),
        "criticality": round(sum(run["criticality"] for run in runs) / len(runs), 3)
        if runs
        else None,
        "run_names": [run["run"] for run in runs],
    }


def results(rows: list[dict], varied: tuple, compare: dict | None = None) -> list[dict]:
    """Kept runs per setting, numbered for citing, tallied (tally) over every
    controller's runs. With `compare` ({"a": controller, "b": controller}, an
    A/B study), each setting instead has the two side by side, "a" and "b",
    each tallied with its controller's name, and "paired": its a and b runs
    matched in run order (the k-th kept a run with the k-th kept b run; a run
    whose partner was not kept is left out), with the failures of each side
    among the pairs and the pairs where only that side failed."""
    cells = defaultdict(list)
    for row in rows:
        if row["verdict"] == "kept":
            cells[(row["scene_id"], *(row[knob] for knob in varied))].append(row)
    table = []
    for index, (key, runs) in enumerate(sorted(cells.items()), start=1):
        setting = {"id": f"S{index}", "scene_id": key[0], **dict(zip(varied, key[1:]))}
        if compare is None:
            table.append({**setting, **tally(runs)})
            continue
        sides = {
            side: [run for run in runs if run["controller"] == compare[side]]
            for side in SIDES
        }
        pairs = list(zip(sides["a"], sides["b"]))
        table.append(
            {
                **setting,
                **{
                    side: {"controller": compare[side], **tally(sides[side])}
                    for side in SIDES
                },
                "paired": {
                    "pairs": len(pairs),
                    "a_failed": sum(a["failed"] for a, _ in pairs),
                    "b_failed": sum(b["failed"] for _, b in pairs),
                    "only_a_failed": sum(
                        a["failed"] and not b["failed"] for a, b in pairs
                    ),
                    "only_b_failed": sum(
                        b["failed"] and not a["failed"] for a, b in pairs
                    ),
                },
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


def first_scenes(count: int) -> list[dict]:
    """The first `count` scenes S1 kept, with what S1 showed at 0 delay."""
    return scene_facts()[:count]


def history_row(entry: dict, varied: tuple) -> dict:
    """One run: its setting, its controller and the gate's verdict; a kept run
    also carries its outcome, and a prior study's run (memory.py) its source."""
    row = {
        "run": entry["name"],
        "scene_id": entry["config"]["scene_id"],
        **{knob: entry["config"][knob] for knob in varied},
        "controller": requested_controller(entry["config"]),
    }
    if "prior" in entry:
        row["prior"] = entry["prior"]
    if "quarantine" in entry:
        row["verdict"] = f"quarantined: {entry['quarantine']}"
    elif entry["resolution"] == "ACCEPT":
        row["verdict"] = "kept"
        row.update(outcome(ROOT / entry["run_dir"]))
    else:
        row["verdict"] = f"not kept: {entry['resolution']}"
    return row


def history(queue: Path, varied: tuple[str, ...]) -> list[dict]:
    """Every run of the study, in queue order (history_row)."""
    return [history_row(load_entry(path), varied) for path in queue_entries(queue)]


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
    fixed: dict | None = None
    # Whether each run gets a seed (run_seed); `seed` above seeds the proposer.
    seeded: bool = False
    # Whether kept runs of other studies with this study's settings count as
    # evidence (memory.prior_runs).
    reuse: bool = False

    @property
    def compare(self) -> dict | None:
        """The two controllers of an A/B study, {"a": ..., "b": ...}, or None."""
        return (self.fixed or {}).get("compare")

    @property
    def systems(self) -> tuple[str, ...]:
        """The controllers each proposed setting runs on, once each."""
        if self.compare is None:
            return (DEFAULT_CONTROLLER,)
        return tuple(self.compare[side] for side in SIDES)


def run_seed(study: str, number: int) -> int:
    """The seed of a study's run `number`: a hash of both, so the same study
    queues the same seeds, and repeats of one setting get different ones."""
    digest = hashlib.sha256(f"{study}:{number}".encode()).digest()
    return int.from_bytes(digest[:8], "big") % (SEED_LIMIT - 1) + 1


def pilot(name: str, candidate_count: int, varied: tuple, **settings) -> Study:
    """A study with its files in the harness folder, as the 6 Oct pilot ran."""
    return Study(
        name=name,
        queue=HARNESS / f"{name}_queue",
        trace=HARNESS / f"{name}_trace.jsonl",
        rounds_file=HARNESS / f"{name}_rounds.jsonl",
        objective=objective(varied),
        candidates=first_scenes(candidate_count),
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

    prior = (
        [
            history_row(entry, study.varied)
            for entry in prior_runs(
                study.queue,
                scenes,
                study.fixed or {},
                list(study.compare.values()) if study.compare else ["linear"],
                study.varied,
            )
        ]
        if study.reuse
        else []
    )
    for round_index in range(done, study.rounds):
        past = history(study.queue, study.varied) if study.queue.is_dir() else []
        if study.reuse:
            past = prior + past
        status = check_goal(study, past, round_index)
        if status is not None and status["met"]:
            print(
                json.dumps({"goal met": status["verdict"], "after_rounds": round_index})
            )
            break
        proposed_before = len(planned(study.queue)) // len(study.systems)
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
        if study.compare is not None:
            state["systems"] = study.compare
            state["comparison"] = results(past, study.varied, study.compare)
        call = None
        if study.proposer == "llm":
            answer, call = llm_proposals(state, study.varied, study.model)
        elif study.proposer == "random":
            answer = random_proposals(
                scenes,
                study.per_round,
                study.varied,
                random.Random(study.seed * 1000 + round_index),
            )
        elif study.proposer == "random_confirm":
            rng = random.Random(study.seed * 1000 + round_index)
            answer = with_confirmation(
                scenes,
                study.per_round,
                state["summary"],
                study.goal,
                study.varied,
                lambda n: random_proposals(scenes, n, study.varied, rng),
            )
        elif study.proposer == "grid":
            answer = grid_proposals(
                scenes,
                study.per_round,
                proposed_before,
                study.goal,
                study.varied,
            )
        elif study.proposer == "bisect":
            answer = bisect_proposals(
                scenes, study.per_round, state["summary"], study.goal, study.varied
            )
        elif study.proposer == "lhs":
            answer = lhs_proposals(
                scenes,
                study.per_round,
                proposed_before,
                study.varied,
                study.seed,
            )
        elif study.proposer == "optuna":
            answer = optuna_proposals(
                scenes, study.per_round, past, study.varied, study.seed
            )
        elif study.proposer == "ga":
            answer = ga_proposals(
                scenes, study.per_round, past, study.varied, study.seed
            )
        elif study.proposer == "rules":
            answer = rules_proposals(
                scenes, study.per_round, state["summary"], study.goal, study.varied
            )
        elif study.proposer == "hybrid":
            ranked = candidates(scenes, state["summary"], study.goal, study.varied)
            answer, call = llm_proposals(
                {**state, "candidates": ranked}, study.varied, study.model
            )
        else:
            raise SystemExit(f"unknown proposer {study.proposer!r}")

        queued, dropped = [], []
        for index, proposed in enumerate(answer["runs"]):
            why_not = (
                "over this round's budget"
                if index >= study.per_round
                else rejection(proposed, set(scenes), study.varied)
            )
            if why_not is None and study.proposer == "hybrid":
                why_not = outside(proposed, ranked, study.varied)
            if why_not:
                dropped.append({**proposed, "dropped": why_not})
                continue
            number = len(planned(study.queue)) // len(study.systems) + 1
            settings = {knob: proposed[knob] for knob in study.varied}
            names = []
            for controller in study.systems:
                name = f"{study.name}_{number:03d}" + (
                    f"_{controller}" if study.compare else ""
                )
                config = run_config(
                    proposed["scene_id"], settings, study.fixed or {}, controller
                )
                # The runs of an A/B pair share the seed.
                if study.seeded:
                    config["seed"] = run_seed(study.name, number)
                add(study.queue, new_entry(name, f"{RUN_ROOT}/{name}", config))
                names.append(name)
            queued.append({**proposed, "runs": names})

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
    table = results(past, study.varied, study.compare)
    status = goal_status(study.goal, table, study.varied)
    study.goal_file.write_text(
        json.dumps({**status, "after_rounds": rounds_done}, indent=1) + "\n",
        encoding="utf-8",
    )
    return status


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("study")
    parser.add_argument("--proposer", choices=("llm", "random", "grid"), required=True)
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
