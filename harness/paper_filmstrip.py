"""Fig. 5: one scene of the main study through the policy's front camera, at
the recorded setting, where it passes, and at a confirmed hardest setting,
where it fails.

Frames come straight from AlpaSim's rollout video (the camera panel of the
composite it writes for every run), at the same times in both runs, counted
back from the failing run's contact. The case is a rear-end collision close
to the recorded path, so the road user it hits stays in the camera's view and
the reconstruction renders it sharply. Written to figures/paper/ as PDF and PNG.

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
from physics import EGO, _read, actor_tracks, completed_rollout

# (study, run that passes, confirmed hardest run on the same scene, row labels)
PAIRS = {
    "fig_filmstrip": (
        "car_conflicts_3knobs_2hz",
        "car_conflicts_3knobs_2hz_hybrid_v2_016",
        "car_conflicts_3knobs_2hz_llm_v2_r5_031",
        ("as recorded: passes", "ego 1.4$\\times$, other cars 0.5$\\times$: crashes"),
    ),
}
FPS = 10
# The camera panel inside AlpaSim's 900 x 1000 composite frame, without
# the sky above the horizon.
CAMERA = (slice(629, 989), slice(32, 868))
# Frame times, in seconds before the failing run's contact.
BEFORE_CONTACT_S = (2.0, 1.5, 1.0, 0.5, 0.0)
FAIL = "#C62828"


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


def filmstrip(name: str, study: str, easy_name: str, hard_name: str, labels: tuple) -> None:
    runs = {r["run"]: r for r in kept(study)}
    easy, hard = runs[easy_name], runs[hard_name]
    if easy["failed"] or not hard["failed"] or easy["scene_id"] != hard["scene_id"]:
        raise SystemExit(f"{name}: need a passing and a failing run on one scene")
    _, when, handoff = moment(hard["run_dir"])
    raw = asyncio.run(_read(completed_rollout(hard["run_dir"]) / "rollout.asl"))
    t0 = min(actor_tracks(raw)[EGO])
    handoff_s, contact_s = (handoff - t0) / 1e6, (when - t0) / 1e6
    times = [round((contact_s - before) * FPS) / FPS for before in BEFORE_CONTACT_S]
    fig, axes = plt.subplots(2, len(times), figsize=(DOUBLE, 1.42))
    fig.subplots_adjust(left=0.004, right=0.996, top=0.88, bottom=0.01, wspace=0.025, hspace=0.06)
    for row, run in enumerate((easy, hard)):
        clip = video(run)
        for col, t in enumerate(times):
            ax = axes[row, col]
            ax.imshow(frame(clip, t))
            ax.set_xticks([])
            ax.set_yticks([])
            contact = row == 1 and col == len(times) - 1
            for spine in ax.spines.values():
                spine.set_color(FAIL if contact else "0.75")
                spine.set_linewidth(1.4 if contact else 0.5)
    for col, t in enumerate(times):
        after = t - handoff_s
        title = "hand-off" if abs(after) < 0.05 else f"{after:+.1f} s"
        if col == len(times) - 1:
            title = f"contact ({title})"
        axes[0, col].set_title(title, fontsize=7, pad=2, color=FAIL if col == len(times) - 1 else "black")
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
