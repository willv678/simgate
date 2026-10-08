"""Failure triage: Claude looks at each failed run and says what happened.

For every kept run of a study that failed, three video frames (2 s and 1 s
before the failure, and at it) and the motion around it go to one headless
call (advisor/TRIAGE.md) that may read only those frames. It returns a cause
from a fixed list, a description, and whether the policy was at fault.
Writes <study folder>/triage.json and prints the causes counted.

    uv run python research/harness/triage.py research/studies/pilot_o1 \
        --queue research/harness/o1_queue
"""

import argparse
import json
import subprocess
import sys
import tempfile
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from headless import ask
from outer import history
from read_state import ROOT, load_entry, queue_entries

from physics import completed_rollout, signals

HARNESS = Path(__file__).resolve().parent
CONTRACT = HARNESS / "advisor" / "TRIAGE.md"
MODEL = "claude-opus-5-5"
CAUSES = (
    "no_brake_for_lead",
    "turned_into_actor",
    "left_road",
    "actor_hit_ego",
    "rendering",
    "other",
)
SCHEMA = {
    "type": "object",
    "properties": {
        "cause": {"type": "string", "enum": list(CAUSES)},
        "what_happened": {"type": "string"},
        "policy_at_fault": {"type": "string", "enum": ["yes", "no", "unclear"]},
    },
    "required": ["cause", "what_happened", "policy_at_fault"],
    "additionalProperties": False,
}
FRAMES_BEFORE_S = (2.0, 1.0, 0.0)


def frames(run_dir: Path, failed_at_s: float, folder: Path) -> list[str]:
    video = next(completed_rollout(run_dir).glob("*.mp4"))
    names = []
    for before in FRAMES_BEFORE_S:
        at = max(0.0, failed_at_s - before)
        name = f"frame_{at:04.1f}s.png"
        subprocess.run(
            [
                "ffmpeg",
                "-v",
                "error",
                "-y",
                "-ss",
                f"{at}",
                "-i",
                str(video),
                "-frames:v",
                "1",
                str(folder / name),
            ],
            check=True,
        )
        names.append(name)
    return names


def motion(run_dir: Path, failed_at_s: float) -> dict:
    """Speed and the gap to the actor ahead, every 0.5 s over the last 3 s."""
    s = signals(run_dir)
    t = (s["times_us"][1:] - s["times_us"][0]) / 1e6
    picks = [
        float(at)
        for at in np.arange(failed_at_s - 3.0, failed_at_s + 0.01, 0.5)
        if at >= 0
    ]
    index = [int(np.abs(t - at).argmin()) for at in picks]
    return {
        "time_s": [round(at, 1) for at in picks],
        "speed_mps": [round(float(s["speed"][i]), 1) for i in index],
        "gap_to_actor_ahead_m": [
            None if not np.isfinite(g) else round(float(g), 1)
            for g in (s["lead_gap_m"][i + 1] for i in index)
        ],
    }


def triage(row: dict, run_dir: Path, model: str) -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        names = frames(run_dir, row["failed_at_s"], folder)
        data = {
            "failure": {
                k: row[k]
                for k in ("collision_at_fault", "offroad", "rear_ended", "handoff_s")
            },
            "failed_at_s": row["failed_at_s"],
            "off_recording_at_failure_m": row["off_recording_at_failure_m"],
            "motion": motion(run_dir, row["failed_at_s"]),
            "frames": names,
        }
        prompt = (
            f"The failure is on stdin; the frames are in {folder}: "
            + ", ".join(names)
            + ". Read every frame, then say what happened."
        )
        answer, call = ask(prompt, data, CONTRACT, SCHEMA, model, read_dir=folder)
    return {"run": row["run"], "scene_id": row["scene_id"], **answer, "call": call}


def triage_study(queue: Path, model: str, known: list[dict] = ()) -> list[dict]:
    """Triage of every failed kept run of a study's queue, four calls at a
    time; runs already in `known` (an earlier triage of the same study, which
    a continued study extends) are kept as they are, not asked again."""
    dirs = {
        load_entry(p)["name"]: ROOT / load_entry(p)["run_dir"]
        for p in queue_entries(queue)
    }
    done = {row["run"] for row in known}
    failed = [r for r in history(queue, ()) if r.get("failed") and r["run"] not in done]
    with ThreadPoolExecutor(4) as pool:
        return list(known) + list(
            pool.map(lambda r: triage(r, dirs[r["run"]], model), failed)
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", type=Path, help="the study folder, for triage.json")
    parser.add_argument("--queue", type=Path, help="default: <folder>/queue")
    parser.add_argument("--model", default=MODEL)
    args = parser.parse_args()
    found = triage_study(args.queue or args.folder / "queue", args.model)
    (args.folder / "triage.json").write_text(json.dumps(found, indent=1) + "\n")
    for row in found:
        print(
            f"{row['run']} {row['cause']} (at fault: {row['policy_at_fault']}): "
            f"{row['what_happened']}"
        )
    print(json.dumps(Counter(row["cause"] for row in found)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
