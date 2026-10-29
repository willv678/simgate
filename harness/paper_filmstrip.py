"""Fig. 5: one cut-in scene through the policy's front camera at a setting
where it passes and at a confirmed hardest setting where it fails, with the
failing run from above at the same moments.

Camera frames come straight from AlpaSim's rollout video (the camera panel
of the composite it writes for every run). The neural reconstruction cannot
render a car pressed against the camera, and a car beside the ego is out of
its view, so the bottom row draws the failing run from its rollout log, as in
Fig. 4: every road user stays visible up to and including the contact.
Written to figures/paper/ as PDF and PNG.

    uv run python research/harness/paper_filmstrip.py
"""

import asyncio
import subprocess
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from case_card import kept, moment
from paper_figures import DOUBLE, OUT, STYLE, save
from physics import EGO, _footprint, _read, actor_tracks, completed_rollout, nearest_actor

# (study, run that passes, confirmed hardest run on the same scene, row labels)
PAIRS = {
    "fig_filmstrip": (
        "cut_in_merge",
        "cut_in_merge_random_confirm_r2_051",
        "cut_in_merge_hybrid_007",
        ("as recorded: passes", "cars 1.25$\\times$ faster: collides", "from above"),
    ),
}
FPS = 10
# The camera panel inside AlpaSim's 900 x 1000 composite frame, without
# the sky above the horizon.
CAMERA = (slice(629, 989), slice(32, 868))
# Camera frames from the hand-off to this long before the contact, then the contact.
BEFORE_CONTACT_S = 0.6
CAMERA_FRAMES = 4
# Top-down view in the ego's frame, driving to the right (metres).
AHEAD, BEHIND, SIDE = 24.0, 12.0, 7.5
EGO_C, KEY_C, OTHER_C, REC_C, FAIL = "#D55E00", "#E69F00", "0.62", "#0072B2", "#C62828"


def frame(video: Path, t: float) -> np.ndarray:
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", str(video), "-frames:v", "1",
         "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        check=True, capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(1000, 900, 3)[CAMERA]


def video(run: dict) -> Path:
    found = sorted((run["run_dir"] / "rollouts").glob("*/*/*.mp4"))
    if len(found) != 1:
        raise SystemExit(f"{run['run']}: expected one rollout video, found {len(found)}")
    return found[0]


def from_above(ax, raw: dict, actors: dict, key: str, handoff: float, at: float) -> None:
    """The failing run at `at` (absolute log time), centred on the ego."""
    ego = actors[EGO]
    now = min(ego, key=lambda s: abs(s - at))
    ex, ey, eyaw = ego[now]
    rot = np.array([[np.cos(-eyaw), -np.sin(-eyaw)], [np.sin(-eyaw), np.cos(-eyaw)]])
    view = lambda xy: (np.asarray(xy, dtype=float).reshape(-1, 2) - (ex, ey)) @ rot.T
    recorded = view([(r[1], r[2]) for r in raw["recorded"]])
    ax.plot(recorded[:, 0], recorded[:, 1], "--", color=REC_C, lw=0.7, zorder=1)
    for actor_id, track in actors.items():
        near = min(track, key=lambda s: abs(s - now))
        if abs(near - now) > 0.15e6:
            continue
        colour = EGO_C if actor_id == EGO else KEY_C if actor_id == key else OTHER_C
        mine = actor_id in (EGO, key)
        trail = [t for t in sorted(track) if handoff <= t <= now]
        if mine and len(trail) > 1:
            xy = view([track[t][:2] for t in trail])
            ax.plot(xy[:, 0], xy[:, 1], color=colour, lw=1.0, zorder=3)
        shape = view(np.array(_footprint(*track[near], raw["sizes"][actor_id]).exterior.coords))
        ax.fill(shape[:, 0], shape[:, 1], color=colour, alpha=0.95 if mine else 0.55, lw=0,
                zorder=5 if mine else 2)
    ax.set_xlim(-BEHIND, AHEAD)
    ax.set_ylim(-SIDE, SIDE)
    ax.set_aspect("equal")


def filmstrip(name: str, study: str, easy_name: str, hard_name: str, labels: tuple) -> None:
    runs = {r["run"]: r for r in kept(study)}
    easy, hard = runs[easy_name], runs[hard_name]
    if easy["failed"] or not hard["failed"] or easy["scene_id"] != hard["scene_id"]:
        raise SystemExit(f"{name}: need a passing and a failing run on one scene")
    raw = asyncio.run(_read(completed_rollout(hard["run_dir"]) / "rollout.asl"))
    actors = actor_tracks(raw)
    _, when, handoff = moment(hard["run_dir"])
    key, when = nearest_actor(raw, actors, when, handoff)
    t0 = min(actors[EGO])
    handoff_s, contact_s = (handoff - t0) / 1e6, (when - t0) / 1e6
    times = list(np.round(np.linspace(handoff_s, contact_s - BEFORE_CONTACT_S, CAMERA_FRAMES) * FPS) / FPS)
    times.append(round(contact_s * FPS) / FPS)
    columns = len(times)
    fig, axes = plt.subplots(3, columns, figsize=(DOUBLE, 2.15),
                             gridspec_kw={"height_ratios": [1, 1, 1.05]})
    fig.subplots_adjust(left=0.004, right=0.996, top=0.91, bottom=0.01, wspace=0.025, hspace=0.07)
    clips = (video(easy), video(hard))
    for col, t in enumerate(times):
        contact = col == columns - 1
        title = "hand-off" if col == 0 else "contact" if contact else f"+{t - handoff_s:.1f} s"
        if contact:
            title += f" (+{t - handoff_s:.1f} s)"
        axes[0, col].set_title(title, fontsize=7, pad=2, color=FAIL if contact else "black")
        for row in (0, 1):
            ax = axes[row, col]
            if row == 1 and contact:
                ax.set_facecolor("0.93")
                ax.text(0.5, 0.5, "the reconstruction cannot\nrender a car this close",
                        transform=ax.transAxes, ha="center", va="center", fontsize=6.2, color="0.35")
            else:
                ax.imshow(frame(clips[row], t))
        from_above(axes[2, col], raw, actors, key, handoff, t0 + t * 1e6)
        for row in range(3):
            ax = axes[row, col]
            ax.set_xticks([])
            ax.set_yticks([])
            for spine in ax.spines.values():
                spine.set_color(FAIL if contact and row > 0 else "0.75")
                spine.set_linewidth(1.4 if contact and row > 0 else 0.5)
    for row, label in enumerate(labels):
        axes[row, 0].text(0.03, 0.95, label, transform=axes[row, 0].transAxes, ha="left", va="top",
                          fontsize=6.4, color=FAIL if row == 1 else "0.15", zorder=10,
                          bbox={"fc": "white", "ec": "none", "alpha": 0.85, "pad": 1.2})
    save(fig, name)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update(STYLE)
    for name, (study, easy, hard, labels) in PAIRS.items():
        filmstrip(name, study, easy, hard, labels)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
