"""Case cards: one page per run that shows what happened, for a person to
judge whether a result makes sense.

A card has, from the run's own rollout log:
- a top-down view in the ego's frame at the moment judged (driving up the
  page): the ego's path and the key actor's path from the hand-off on,
  coloured by time; other road users' paths in grey; the human's recorded
  path dashed; footprints at the hand-off (faint) and at the moment judged;
- the ego's and the key actor's speed, the human's recorded speed;
- the gap between the ego's and the key actor's footprints;
- the ego's acceleration (how the controller reacted);
- the ego's sideways offset from the human's path (left positive);
- the front camera at the moment judged;
- the study, scene, setting, the gate's and the scorer's verdicts, and the
  triage's one-line explanation when the run has one.

The moment judged is the first at-fault contact as `outer.outcome` counts
it, else the first collision flag after the hand-off, else the closest
approach to another road user after the hand-off. The key actor is the road
user nearest the ego then.

    uv run python research/harness/case_card.py hardest   # confirmed hardest cases
    uv run python research/harness/case_card.py spot      # 20 random kept runs
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
from alpasim_utils.logs import async_read_pb_log
from compare_proposers import arms
from goals import challenging
from physics import EGO, _footprint, _read, actor_tracks, completed_rollout, nearest_actor
from read_state import ROOT, load_entry, queue_entries

STUDIES = ("pedestrian_ego_speed", "cut_in_merge", "lead_vehicle")
OUT = ROOT / "research" / "figures" / "cards"
SPOT_SEED, SPOT_N = 20261013, 20
VIEW_M = 40
CLASS = {"automobile": "car", "person": "pedestrian"}
# AlpaSim's video is 900 x 1000; the front camera is the bottom 488 rows.
CAMERA_CROP = "crop=900:488:0:512"


def _plan(study: str) -> dict:
    return json.loads((ROOT / "research" / "studies" / study / "plan.json").read_text())["plan"]


def kept(study: str) -> list[dict]:
    """Every kept run of every arm of the study: its folder, arm, setting and
    outcome."""
    varied = tuple(_plan(study)["vary"])
    runs = []
    for arm, folder in arms(ROOT / "research" / "studies" / study).items():
        for path in queue_entries(folder / "queue"):
            entry = load_entry(path)
            if entry["resolution"] != "ACCEPT" or "quarantine" in entry:
                continue
            run_dir = ROOT / entry["run_dir"]
            runs.append({"study": study, "arm": arm, "run": entry["name"], "run_dir": run_dir,
                         "scene_id": entry["config"]["scene_id"],
                         **{k: entry["config"][k] for k in varied},
                         "verdict": "kept", **outer.outcome(run_dir)})
    return runs


def triage_lines(study: str) -> dict:
    """run name -> the triage's record, from every arm."""
    found = {}
    for folder in arms(ROOT / "research" / "studies" / study).values():
        path = folder / "triage.json"
        if path.exists():
            for row in json.loads(path.read_text()):
                found[row["run"]] = row
    return found


def moment(run_dir: Path) -> tuple[str, float, float]:
    """(what, when, hand-off) for the moment a card is centred on."""
    metrics = pd.read_parquet(completed_rollout(run_dir) / "metrics.parquet")
    relevant = metrics[metrics["name"] == "eval_relevant"]
    driven = float(relevant.loc[relevant["values"] > 0, "timestamps_us"].min())
    found = outer.outcome(run_dir)
    if found["failed"]:
        clear = outer._contact_cleared(metrics, driven)
        contact = min(outer._first(metrics, "collision_front", clear),
                      outer._first(metrics, "collision_lateral", clear)
                      ) if found["collision_at_fault"] else float("inf")
        offroad = outer._first(metrics, "offroad", driven)
        if offroad < contact:
            return "left the road", offroad, driven
        return "at-fault contact", contact, driven
    flagged = min(outer._first(metrics, name, driven)
                  for name in ("collision_front", "collision_lateral", "collision_rear"))
    if np.isfinite(flagged):
        return "contact not counted (rear-ended or begun before the hand-off)", flagged, driven
    return "closest approach (no contact)", float("nan"), driven


async def _classes(path: Path) -> dict:
    async for message in async_read_pb_log(str(path)):
        if message.WhichOneof("log_entry") == "traffic_session_request":
            return {o.object_id: o.label_class
                    for o in message.traffic_session_request.logged_object_trajectories}
    return {}


def _speed(track: dict) -> tuple[np.ndarray, np.ndarray]:
    times = np.array(sorted(track), dtype=float)
    xy = np.array([track[t][:2] for t in times])
    if len(times) < 2:
        return times, np.zeros(len(times))
    v = np.hypot(*np.diff(xy, axis=0).T) / (np.diff(times) / 1e6)
    return (times[1:] + times[:-1]) / 2, v


def _gap(raw: dict, a: dict, b: dict, actor_id: str, times) -> np.ndarray:
    out = []
    for t in times:
        if t in a and t in b:
            out.append(_footprint(*a[t], raw["sizes"][EGO]).distance(
                _footprint(*b[t], raw["sizes"][actor_id])))
        else:
            out.append(np.nan)
    return np.array(out)


def _lateral(ego: dict, recorded: list) -> tuple[np.ndarray, np.ndarray]:
    """Signed distance of the ego from the human's recorded path, left positive."""
    path = np.array([(r[1], r[2]) for r in recorded])
    times = np.array(sorted(ego), dtype=float)
    out = []
    for t in times:
        x, y, _ = ego[t]
        i = int(np.argmin(np.hypot(path[:, 0] - x, path[:, 1] - y)))
        j = min(i + 1, len(path) - 1) if i + 1 < len(path) else i - 1
        dx, dy = path[j] - path[i] if j > i else path[i] - path[j]
        norm = np.hypot(dx, dy) or 1.0
        out.append(((x - path[i, 0]) * -dy + (y - path[i, 1]) * dx) / norm)
    return times, np.array(out)


def _camera(rollout: Path, raw: dict, when: float, target: Path) -> Path | None:
    videos = list(rollout.glob("*_camera_front_wide_120fov_default.mp4"))
    if not videos:
        return None
    frame = int(np.searchsorted(sorted(raw["ego"]), when))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(videos[0]), "-vf",
                    f"select=eq(n\\,{frame}),{CAMERA_CROP}", "-frames:v", "1", str(target)],
                   check=True)
    return target if target.exists() else None


def _setting(run: dict) -> str:
    parts = []
    for knob, label, unit in (("ego_speed_scale", "ego speed", "x"),
                              ("actor_speed_scale", "actor speed", "x"),
                              ("actor_time_shift_s", "actor timing", " s"),
                              ("planner_delay_us", "delay", " us")):
        if knob in run:
            value = run[knob]
            parts.append(f"{label} {value:+g}{unit}" if knob == "actor_time_shift_s"
                         else f"{label} {value:g}{unit}")
    return ", ".join(parts)


def card(run: dict, triage: dict | None, target: Path) -> dict:
    """Write one card; returns what it shows, for the index."""
    target.parent.mkdir(parents=True, exist_ok=True)
    rollout = completed_rollout(run["run_dir"])
    raw = asyncio.run(_read(rollout / "rollout.asl"))
    classes = asyncio.run(_classes(rollout / "rollout.asl"))
    actors = actor_tracks(raw)
    what, when, handoff = moment(run["run_dir"])
    key, when = nearest_actor(raw, actors, when, handoff)
    ego = actors[EGO]
    t0 = min(ego)
    rel = lambda t: (np.asarray(t, dtype=float) - t0) / 1e6

    fig = plt.figure(figsize=(18, 9.5))
    grid = fig.add_gridspec(4, 3, width_ratios=[1.25, 1, 1.15], hspace=0.6, wspace=0.25)
    bev = fig.add_subplot(grid[:, 0])
    speed_ax, gap_ax = fig.add_subplot(grid[0, 1]), fig.add_subplot(grid[1, 1])
    accel_ax, lat_ax = fig.add_subplot(grid[2, 1]), fig.add_subplot(grid[3, 1])
    cam_ax = fig.add_subplot(grid[:2, 2])
    text_ax = fig.add_subplot(grid[2:, 2])

    # Top-down, in the ego's frame at the moment judged.
    ex, ey, eyaw = ego[min(ego, key=lambda s: abs(s - when))]
    turn = np.pi / 2 - eyaw
    rot = np.array([[np.cos(turn), -np.sin(turn)], [np.sin(turn), np.cos(turn)]])
    view = lambda xy: (np.asarray(xy, dtype=float).reshape(-1, 2) - (ex, ey)) @ rot.T
    start, end = handoff - 1e6, when + 1.5e6
    recorded = view([(r[1], r[2]) for r in raw["recorded"]])
    bev.plot(recorded[:, 0], recorded[:, 1], "--", color="tab:blue", lw=1.5,
             label="human's recorded path")
    for actor_id, track in actors.items():
        times = [t for t in sorted(track) if start <= t <= end]
        if len(times) < 2:
            continue
        xy = view([track[t][:2] for t in times])
        if np.abs(xy).min() > VIEW_M * 1.2:
            continue
        mine = actor_id in (EGO, key)
        colour = "tab:red" if actor_id == EGO else "tab:orange" if actor_id == key else "0.75"
        bev.plot(xy[:, 0], xy[:, 1], color=colour, lw=3 if mine else 1, zorder=4 if mine else 1)
        if mine:
            # A dot each whole second, labelled with the run's clock.
            for second in range(int(np.ceil(rel(start))), int(rel(end)) + 1):
                t = min(times, key=lambda s: abs(rel(s) - second))
                if abs(rel(t) - second) > 0.3:
                    continue
                x, y = view(track[t][:2])[0]
                bev.plot(x, y, "o", color=colour, ms=6, mec="white", zorder=6)
                bev.annotate(f"{second}s", (x, y), xytext=(6 if actor_id == EGO else -6, 0),
                             textcoords="offset points", fontsize=8, color=colour,
                             ha="left" if actor_id == EGO else "right", va="center", zorder=7)
        for t, alpha in ((handoff, 0.25), (when, 0.9)):
            near = min(track, key=lambda s: abs(s - t))
            if abs(near - t) > 0.6e6:
                continue
            shape = view(np.array(_footprint(*track[near], raw["sizes"][actor_id]).exterior.coords))
            bev.fill(shape[:, 0], shape[:, 1], color="0.55" if not mine else colour,
                     alpha=alpha, zorder=5 if mine else 2)
    bev.set_xlim(-VIEW_M / 2, VIEW_M / 2)
    bev.set_ylim(-VIEW_M * 0.75, VIEW_M * 0.75)
    bev.set_aspect("equal")
    bev.grid(alpha=0.3)
    bev.set_xlabel("metres (ego driving up the page)")
    key_name = CLASS.get(classes.get(key, ""), classes.get(key, "road user"))
    bev.set_title(f"From above: ego red, {key_name} {key} orange, others grey\n"
                  "faint box: at the hand-off; solid: at the moment judged", fontsize=11)
    bev.legend(loc="lower left", fontsize=9)

    # Time series.
    marks = lambda ax: [ax.axvline(rel(handoff), color="0.4", ls=":", lw=1.2),
                        ax.axvline(rel(when), color="tab:red", ls="-", lw=1.2)]
    t, v = _speed(ego)
    speed_ax.plot(rel(t), v, color="tab:red", lw=2, label="ego")
    rec = {r[0]: (r[1], r[2], 0.0) for r in raw["recorded"]}
    t_rec, v_rec = _speed(rec)
    speed_ax.plot(rel(t_rec), v_rec, "--", color="tab:blue", lw=1.2, label="human (recorded)")
    if key:
        t_k, v_k = _speed(actors[key])
        speed_ax.plot(rel(t_k), v_k, color="tab:orange", lw=2, label=key_name)
    speed_ax.set_ylabel("speed, m/s")
    speed_ax.legend(fontsize=8, loc="upper left", ncol=3)
    if key:
        times = sorted(set(ego) & set(actors[key]))
        gap_ax.plot(rel(times), _gap(raw, ego, actors[key], key, times), color="tab:orange", lw=2)
    gap_ax.axhline(0, color="0.5", lw=0.8)
    gap_ax.set_ylabel(f"gap to {key_name}, m")
    gap_ax.set_ylim(bottom=-0.5)
    accel = np.gradient(v, t / 1e6) if len(t) > 2 else np.zeros_like(v)
    accel_ax.plot(rel(t), accel, color="tab:red", lw=1.5)
    accel_ax.axhline(0, color="0.5", lw=0.8)
    accel_ax.set_ylabel("ego accel, m/s²")
    t_l, lat = _lateral(ego, raw["recorded"])
    lat_ax.plot(rel(t_l), lat, color="tab:red", lw=1.5)
    lat_ax.axhline(0, color="tab:blue", ls="--", lw=1)
    lat_ax.set_ylabel("left of human, m")
    lat_ax.set_xlabel("time, s  (dotted: AI takes over; red: moment judged)")
    for ax in (speed_ax, gap_ax, accel_ax, lat_ax):
        marks(ax)
        ax.set_xlim(rel(t0), rel(max(ego)))
        ax.grid(alpha=0.3)

    frame = _camera(rollout, raw, when, target.with_suffix(".camera.png"))
    if frame:
        cam_ax.imshow(plt.imread(frame))
        frame.unlink()
    cam_ax.set_title("front camera at the moment judged", fontsize=11)
    cam_ax.axis("off")

    lines = [
        f"study: {run['study']} ({run['arm']})",
        f"scene: {run['scene_id'].removeprefix('clipgt-')[:8]}    run: {run['run']}",
        f"setting: {_setting(run)}",
        "gate: kept (every check passed)",
        f"scored: {what} at {rel(when):.1f} s; AI took over at {rel(handoff):.1f} s",
        f"counted as the AI's failure: {'yes' if run['failed'] else 'no'}",
    ]
    if triage:
        lines.append(f"triage (Claude, from the video): {triage['cause']}, "
                     f"policy at fault: {triage['policy_at_fault']}")
        lines.append("")
        lines.extend(_wrap(triage["what_happened"], 58))
    text_ax.text(0, 1, "\n".join(_wrap_all(lines, 58)), va="top", family="monospace", fontsize=9.5)
    text_ax.axis("off")
    fig.suptitle(f"{run['study']}: {run['scene_id'].removeprefix('clipgt-')[:8]}, "
                 f"{_setting(run)}: {what}", fontsize=14, x=0.02, ha="left")
    fig.savefig(target, dpi=90, bbox_inches="tight")
    plt.close(fig)
    return {"card": str(target.relative_to(ROOT / "research")), "run": run["run"],
            "study": run["study"], "arm": run["arm"], "setting": _setting(run),
            "scene": run["scene_id"].removeprefix("clipgt-")[:8], "moment": what,
            "counted": bool(run["failed"]), "key_actor": f"{key_name} {key}",
            "triage": triage["what_happened"] if triage else None}


def _wrap_all(lines: list[str], width: int) -> list[str]:
    return [part for line in lines for part in (_wrap(line, width) or [""])]


def _wrap(text: str, width: int) -> list[str]:
    words, lines, line = text.split(), [], ""
    for word in words:
        if len(line) + len(word) + 1 > width:
            lines.append(line)
            line = word
        else:
            line = f"{line} {word}".strip()
    return [*lines, line] if line else lines


def hardest(study: str) -> list[dict]:
    """One failed run of each confirmed hardest setting, all arms pooled."""
    runs = kept(study)
    plan = _plan(study)
    varied = tuple(plan["vary"])
    table = outer.results(runs, varied)
    chosen = []
    for row in challenging(table, plan["goal"]):
        failed = [r for r in runs if r["failed"] and r["scene_id"] == row["scene_id"]
                  and all(r[k] == row[k] for k in varied)]
        if failed:
            chosen.append(sorted(failed, key=lambda r: r["run"])[0])
    return chosen


def write_index(title: str, cards: list[dict], target: Path, intro: str) -> None:
    lines = [f"# {title}", "", intro, ""]
    for c in cards:
        lines += [f"## {c['study']}, {c['scene']}: {c['setting']}", "",
                  f"![]({Path(c['card']).relative_to(target.parent.relative_to(ROOT / 'research'))})",
                  "", f"- {c['moment']}; counted as the AI's failure: "
                  f"{'yes' if c['counted'] else 'no'}; key actor: {c['key_actor']}",
                  f"- run `{c['run']}` ({c['arm']})"]
        if c["triage"]:
            lines.append(f"- triage: {c['triage']}")
        lines.append("")
    target.write_text("\n".join(lines))


def verdict_sheet(cards: list[dict], path: Path) -> None:
    """A sheet for a person to mark each card: does the run make sense
    (yes / no / unsure), and why. Never overwrites a sheet already started."""
    if path.exists():
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["card", "run", "makes_sense", "note"])
        for c in cards:
            writer.writerow([Path(c["card"]).name, c["run"], "", ""])


def main(command: str) -> int:
    if command == "hardest":
        cards = []
        for study in STUDIES:
            triage = triage_lines(study)
            for run in hardest(study):
                cards.append(card(run, triage.get(run["run"]),
                                  OUT / "hardest" / f"{study}_{run['run']}.png"))
                print(cards[-1]["card"], flush=True)
        write_index("The hardest confirmed cases", cards, OUT / "hardest" / "README.md",
                    "One card per confirmed hardest setting (failure rate surely above "
                    "one half), all search methods pooled, at 10 Hz. Generated by "
                    "`harness/case_card.py hardest`.")
        (OUT / "hardest" / "cards.json").write_text(json.dumps(cards, indent=1) + "\n")
        verdict_sheet(cards, OUT / "hardest" / "verdicts.csv")
        return 0
    if command == "spot":
        pool = [r for study in STUDIES for r in kept(study)]
        chosen = random.Random(SPOT_SEED).sample(pool, SPOT_N)
        triage = {name: row for study in STUDIES for name, row in triage_lines(study).items()}
        cards = []
        for i, run in enumerate(chosen, 1):
            cards.append(card(run, triage.get(run["run"]), OUT / "spot" / f"S{i:02d}.png"))
            print(cards[-1]["card"], flush=True)
        write_index("Spot check: 20 random kept runs", cards, OUT / "spot" / "README.md",
                    f"{SPOT_N} kept runs drawn at random (seed {SPOT_SEED}) from the "
                    f"{len(pool)} kept runs of the three 10 Hz method studies, whatever "
                    "their outcome. Each card is for a person to say whether the run "
                    "makes sense. Generated by `harness/case_card.py spot`.")
        (OUT / "spot" / "cards.json").write_text(json.dumps(cards, indent=1) + "\n")
        verdict_sheet(cards, OUT / "spot" / "verdicts.csv")
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1 else ""))
