"""Fig. 5: the same scene through the policy's front camera, at a setting
where it passes and at a confirmed hardest setting where it fails.

Frames come straight from AlpaSim's rollout video (the camera panel of the
composite it writes for every run), at the same times after the hand-off in
both runs, so a reader can see that the hardest case is a real, visible
failure and not a label. Written to figures/paper/ as PDF and PNG.

    uv run python research/harness/paper_filmstrip.py
"""

import subprocess
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from case_card import kept
from paper_figures import DOUBLE, OUT, STYLE, save

# (study, run that passes, confirmed hardest run on the same scene, row labels)
PAIRS = {
    "fig_filmstrip": (
        "cut_in_merge",
        "cut_in_merge_random_confirm_r2_051",
        "cut_in_merge_hybrid_007",
        ("as recorded: passes", "car cutting in 1.25$\\times$ faster: collides"),
    ),
}
FPS = 10
# The camera panel inside AlpaSim's 900 x 1000 composite frame, without
# the sky above the horizon.
CAMERA = (slice(629, 989), slice(32, 868))
COLUMNS = 5
# The neural reconstruction cannot render a car pressed against the camera,
# so the strip ends this long before the contact.
BEFORE_CONTACT_S = 0.6
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
    handoff, fail_at = hard["handoff_s"], hard["failed_at_s"]
    times = np.round(np.linspace(handoff, fail_at - BEFORE_CONTACT_S, COLUMNS) * FPS) / FPS
    fig, axes = plt.subplots(2, COLUMNS, figsize=(DOUBLE, 1.42))
    fig.subplots_adjust(left=0.004, right=0.996, top=0.88, bottom=0.01, wspace=0.025, hspace=0.06)
    for row, (run, label) in enumerate(zip((easy, hard), labels)):
        clip = video(run)
        for col, t in enumerate(times):
            ax = axes[row, col]
            ax.imshow(frame(clip, t))
            ax.set_xticks([])
            ax.set_yticks([])
            for spine in ax.spines.values():
                spine.set_color("0.75")
                spine.set_linewidth(0.5)
            if row == 0:
                title = "hand-off" if col == 0 else f"+{t - handoff:.1f} s"
                if col == COLUMNS - 1:
                    title += f" ({fail_at - t:.1f} s before contact)"
                ax.set_title(title, fontsize=7, pad=2)
            if col == 0:
                ax.text(0.03, 0.95, label, transform=ax.transAxes, ha="left", va="top", fontsize=6.4,
                        color=FAIL if row == 1 else "0.15",
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
