"""A blind sample of crashes for a person to judge: was it the policy's fault?

`make` draws a fixed random sample of kept runs from six studies, 10 per
study: about 7 that outer.outcome counts as an at-fault collision and 3 with
a collision flag it does not count (rear-ended, or a contact under way at the
hand-off), so the person can disagree in both directions. For each run it
writes a copy of the front-camera video with the time, the hand-off and the
contact to judge burned in, and a top-down plot of the 3 s around that
contact (the camera does not show a car hitting the ego's side or rear;
the video's own map view, kept, does, but at one moment at a time).
sheet.csv holds only what the person needs; which run, study and group
each id is goes to key.json, which the person does not open until `score`.

    uv run python research-griffin/harness/label_sheet.py make
"""

import asyncio
import csv
import json
import random
import subprocess
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

import outer
from compare_proposers import arms
from physics import EGO, _footprint, _read, completed_rollout
from read_state import ROOT, load_entry, queue_entries

STUDIES = (
    "cut_in_merge",
    "lead_vehicle",
    "pedestrian_ego_speed",
    "cut_in_merge_2hz",
    "lead_vehicle_2hz",
    "pedestrian_ego_speed_2hz",
)
PER_STUDY, NOT_COUNTED = 10, 3
SEED = 20261012
OUT = Path(__file__).resolve().parents[1] / "griffin" / "labels"
COLUMNS = (
    "id",
    "scene",
    "video",
    "topdown",
    "handoff_video_s",
    "contact_video_s",
    "fault",
    "what_happened",
    "minutes",
)
PANELS_S = (-2.0, -1.0, 0.0, 1.0)
# Each vehicle trails a line through where it was over the last second.
TRAIL_US = 1_000_000
VIEW_M = 30


def _flags(metrics: pd.DataFrame, since_us: float) -> float:
    return min(
        outer._first(metrics, name, since_us)
        for name in ("collision_front", "collision_lateral", "collision_rear")
    )


def contact_to_judge(run_dir: Path) -> tuple[str, float, float] | None:
    """(group, when, hand-off). ('counted', when) for an at-fault collision: its first at-fault
    contact, after any contact carried across the hand-off, as outcome
    counts it. ('not_counted', when) for a run with a collision flag after
    the hand-off that outcome does not count: the first such flag. None
    otherwise."""
    found = outer.outcome(run_dir)
    metrics = pd.read_parquet(completed_rollout(run_dir) / "metrics.parquet")
    relevant = metrics[metrics["name"] == "eval_relevant"]
    driven = float(relevant.loc[relevant["values"] > 0, "timestamps_us"].min())
    if found["collision_at_fault"]:
        clear = outer._contact_cleared(metrics, driven)
        when = min(
            outer._first(metrics, "collision_front", clear),
            outer._first(metrics, "collision_lateral", clear),
        )
        return "counted", when, driven
    if found["rear_ended"] or found["contact_at_handoff"]:
        return "not_counted", _flags(metrics, driven), driven
    return None


def kept_runs(study: str) -> list[Path]:
    runs = []
    for folder in arms(ROOT / "research" / "studies" / study).values():
        for path in queue_entries(folder / "queue"):
            entry = load_entry(path)
            if entry["resolution"] == "ACCEPT" and "quarantine" not in entry:
                runs.append(ROOT / entry["run_dir"])
    return sorted(runs)


def sample(rng: random.Random) -> list[dict]:
    """PER_STUDY runs per study, NOT_COUNTED of them from the not-counted
    group (fewer if the study has fewer), the rest counted."""
    chosen = []
    for study in STUDIES:
        groups = {"counted": [], "not_counted": []}
        for run_dir in kept_runs(study):
            judged = contact_to_judge(run_dir)
            if judged:
                groups[judged[0]].append((run_dir, *judged[1:]))
        quota = {"not_counted": min(NOT_COUNTED, len(groups["not_counted"]))}
        quota["counted"] = PER_STUDY - quota["not_counted"]
        for group, n in quota.items():
            for run_dir, when, driven in rng.sample(groups[group], n):
                chosen.append(
                    {"run": run_dir.name, "run_dir": str(run_dir), "study": study,
                     "group": group, "contact_us": when, "handoff_us": driven}
                )
    rng.shuffle(chosen)
    for i, c in enumerate(chosen, 1):
        c["id"] = f"L{i:02d}"
    return chosen


def _video_times(raw: dict, handoff_us: float, contact_us: float) -> tuple[int, int, float]:
    """Frame indices of the hand-off and the contact, and frames per second:
    the video has one frame per logged ego pose."""
    times = sorted(raw["ego"])
    fps = (len(times) - 1) / ((times[-1] - times[0]) / 1e6)
    index = lambda t: int(np.searchsorted(times, t))
    return index(handoff_us), index(contact_us), fps


# AlpaSim's video is 900 x 1000: a map view top left, the evaluator's
# metric table top right (it states collision_at_fault, so it would give the
# answer away), the front camera below. The table is blacked out and the
# labels go there.
METRIC_TABLE = "drawbox=x=545:y=0:w=355:h=512:color=black:t=fill"


def write_video(source: Path, target: Path, handoff_frame: int, contact_frame: int) -> None:
    label = "fontsize=30:x=565:box=1:boxcolor=black@0.6"
    text = ",".join(
        (
            METRIC_TABLE,
            f"drawtext=text='t %{{pts\\:flt}} s':fontcolor=white:{label}:y=40",
            f"drawtext=text='POLICY DRIVING':fontcolor=yellow:{label}:y=100:enable='gte(n,{handoff_frame})'",
            f"drawtext=text='CONTACT TO JUDGE':fontcolor=red:{label}:y=160:enable='between(n,{contact_frame},{contact_frame + 2})'",
        )
    )
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-i", str(source), "-vf", text, "-c:v", "libx264",
         "-pix_fmt", "yuv420p", str(target)],
        check=True,
    )


def _pose(track: dict, t: float):
    times = sorted(track)
    i = int(np.searchsorted(times, t, side="right")) - 1
    return track[times[max(i, 0)]] if times[0] <= t <= times[-1] else None


def write_topdown(raw: dict, handoff_us: float, contact_us: float, title: str, target: Path) -> None:
    """Four panels around the contact, in the ego's frame at the contact
    (driving up the page): the ego red, other road users grey, each with a
    line through where it was over the last second, the human's recorded
    path dashed."""
    ex, ey, eyaw = _pose(raw["ego"], contact_us)
    turn = np.pi / 2 - eyaw
    rot = np.array([[np.cos(turn), -np.sin(turn)], [np.sin(turn), np.cos(turn)]])
    to_view = lambda xy: (np.asarray(xy) - (ex, ey)) @ rot.T
    actors: dict[str, dict] = {}
    for t, rows in raw["others"].items():
        for x, y, yaw, actor_id in rows:
            actors.setdefault(actor_id, {})[t] = (x, y, yaw)
    recorded = to_view([(r[1], r[2]) for r in raw["recorded"]])
    fig, axes = plt.subplots(1, len(PANELS_S), figsize=(16, 6))
    for ax, offset in zip(axes, PANELS_S):
        t = contact_us + offset * 1e6
        ax.plot(recorded[:, 0], recorded[:, 1], "--", color="tab:blue", lw=1)
        for actor_id, track in [(EGO, raw["ego"]), *actors.items()]:
            pose = _pose(track, t)
            if pose is None:
                continue
            shape = _footprint(*pose, raw["sizes"][actor_id])
            xy = to_view(np.array(shape.exterior.coords))
            if np.abs(xy).min() > VIEW_M * 1.5:
                continue
            ego = actor_id == EGO
            trail = [p for s, p in sorted(track.items()) if t - TRAIL_US <= s <= t]
            if len(trail) > 1:
                path = to_view([(p[0], p[1]) for p in trail])
                ax.plot(path[:, 0], path[:, 1], color="tab:red" if ego else "0.3", lw=1.5)
            ax.fill(xy[:, 0], xy[:, 1], color="tab:red" if ego else "0.6",
                    alpha=0.9 if ego else 0.7, zorder=3 if ego else 2)
        driving = "policy driving" if t >= handoff_us else "replaying the recording"
        ax.set_title(f"{offset:+.0f} s from contact\n{driving}")
        ax.set_xlim(-VIEW_M / 2, VIEW_M / 2)
        ax.set_ylim(-VIEW_M, VIEW_M)
        ax.set_aspect("equal")
        ax.grid(alpha=0.3)
    fig.suptitle(f"{title}: ego red, others grey, line = where it was over the last 1 s, "
                 "human's recorded path dashed; metres, ego driving up")
    fig.tight_layout()
    fig.savefig(target, dpi=80)
    plt.close(fig)


def make() -> int:
    if (OUT / "key.json").exists():
        print(f"{OUT / 'key.json'} exists: the sample is drawn once. Delete the labels folder to redraw.")
        return 1
    chosen = sample(random.Random(SEED))
    (OUT / "videos").mkdir(parents=True, exist_ok=True)
    (OUT / "topdown").mkdir(exist_ok=True)
    rows = []
    for c in chosen:
        rollout = completed_rollout(Path(c["run_dir"]))
        raw = asyncio.run(_read(rollout / "rollout.asl"))
        handoff_us = c["handoff_us"]
        handoff_frame, contact_frame, fps = _video_times(raw, handoff_us, c["contact_us"])
        video = OUT / "videos" / f"{c['id']}.mp4"
        write_video(next(rollout.glob("*_camera_front_wide_120fov_default.mp4")), video,
                    handoff_frame, contact_frame)
        topdown = OUT / "topdown" / f"{c['id']}.png"
        write_topdown(raw, handoff_us, c["contact_us"], c["id"], topdown)
        rows.append(
            {"id": c["id"], "scene": rollout.parent.name.removeprefix("clipgt-")[:8],
             "video": f"videos/{c['id']}.mp4", "topdown": f"topdown/{c['id']}.png",
             "handoff_video_s": round(handoff_frame / fps, 1),
             "contact_video_s": round(contact_frame / fps, 1),
             "fault": "", "what_happened": "", "minutes": ""}
        )
        print(c["id"], flush=True)
    with open(OUT / "sheet.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    (OUT / "key.json").write_text(json.dumps(chosen, indent=1) + "\n")
    print(f"wrote {len(rows)} rows to {OUT / 'sheet.csv'}")
    return 0


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else ""
    if command == "make":
        raise SystemExit(make())
    print(__doc__)
    raise SystemExit(2)
