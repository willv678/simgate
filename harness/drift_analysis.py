"""Which way does the policy leave the recorded path once it drives?

For kept runs, the ego's signed lateral offset from the recorded human path
(left positive: the cross product of the path's heading with the ego's
displacement from the nearest recorded point), at fixed times after the
hand-off, up to the failure for failed runs. At the hand-off the ego replays
its recording, so the offset there is 0 by construction; a check on the
measurement. Per batch (any queue), and for the study runs together.

Open loop: during the warm-up the ego replays its recording while the driver
still plans every step. Each warm-up plan (in the ego's frame when it was
made) is compared with where the human actually went 1, 2 and 3 s later; a
lean there is the model's, before any closed-loop error (study runs at the
recorded ego speed). Writes research/DRIFT.md and research/drift.json.

    uv run python research/harness/drift_analysis.py [queue ...]
"""

import asyncio
import json
import sys
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))

from alpasim_utils.logs import async_read_pb_log
from outer import outcome
from physics import _read, completed_rollout
from plot_results import SURFACE, TEXT, TEXT_SECONDARY, _save, _style
from read_state import ROOT, load_entry, queue_entries

STUDIES = ROOT / "research" / "studies"
HARNESS = ROOT / "research" / "harness"
AFTER_S = (0.0, 1.0, 2.0, 3.0, 5.0, 7.0)
# The figure's time axis: every half second after the hand-off.
CURVE_S = tuple(x / 2 for x in range(0, 17))
SIDE_M = 0.5
BATCHES = ("b2_queue", "s1_queue", "v1_queue")


def signed_offset(raw: dict, t_us: float) -> float:
    """The ego's lateral offset from the recorded path at the logged step
    nearest t_us, left positive."""
    times = np.array(sorted(raw["ego"]))
    x, y, _ = raw["ego"][int(times[np.argmin(abs(times - t_us))])]
    rec = raw["recorded"]
    rx = np.array([r[1] for r in rec])
    ry = np.array([r[2] for r in rec])
    i = int(np.argmin(np.hypot(rx - x, ry - y)))
    ahead, behind = min(i + 1, len(rx) - 1), max(i - 1, 0)
    hx, hy = rx[ahead] - rx[behind], ry[ahead] - ry[behind]
    return float((hx * (y - ry[i]) - hy * (x - rx[i])) / (np.hypot(hx, hy) or 1.0))


def run_offsets(run_dir: Path) -> dict:
    result = outcome(run_dir)
    raw = asyncio.run(_read(completed_rollout(run_dir) / "rollout.asl"))
    start = min(raw["ego"])
    handoff = start + result["handoff_s"] * 1e6
    end = start + result["failed_at_s"] * 1e6 if result["failed"] else max(raw["ego"])
    return {
        "failed": result["failed"],
        "after": {
            s: signed_offset(raw, handoff + s * 1e6)
            for s in sorted(set(AFTER_S) | set(CURVE_S))
            if handoff + s * 1e6 <= end
        },
        "at_end": signed_offset(raw, end),
    }


PLAN_HORIZONS_S = (1.0, 2.0, 3.0)
# A plan this close to the hand-off may have been made with the policy's
# first steps already in its context; the first second of the log is skipped
# too, while the context fills.
WARMUP_MARGIN_US = 200_000


async def _plans(path: Path) -> list[list[tuple[int, float, float]]]:
    found = []
    async for message in async_read_pb_log(str(path)):
        if message.WhichOneof("log_entry") == "driver_return":
            poses = message.driver_return.trajectory.poses
            if poses:
                found.append(
                    [(p.timestamp_us, p.pose.vec.x, p.pose.vec.y) for p in poses]
                )
    return found


def warmup_plan_errors(run_dir: Path) -> dict[float, list[float]]:
    """Lateral error (left positive) of each warm-up plan against the
    recorded future, per horizon."""
    result = outcome(run_dir)
    path = completed_rollout(run_dir) / "rollout.asl"
    raw = asyncio.run(_read(path))
    rec = raw["recorded"]
    rt = np.array([r[0] for r in rec], dtype=float)
    rx = np.array([r[1] for r in rec])
    ry = np.array([r[2] for r in rec])
    start = min(raw["ego"])
    handoff = start + result["handoff_s"] * 1e6
    errors = {h: [] for h in PLAN_HORIZONS_S}
    for plan in asyncio.run(_plans(path)):
        made = plan[0][0]
        if not start + 1e6 <= made < handoff - WARMUP_MARGIN_US:
            continue
        x0, y0 = np.interp(made, rt, rx), np.interp(made, rt, ry)
        dx = np.interp(made + 2e5, rt, rx) - x0
        dy = np.interp(made + 2e5, rt, ry) - y0
        yaw = np.arctan2(dy, dx)
        for horizon in PLAN_HORIZONS_S:
            near = [p for p in plan if abs((p[0] - made) / 1e6 - horizon) < 0.26]
            if not near:
                continue
            fx = np.interp(made + horizon * 1e6, rt, rx) - x0
            fy = np.interp(made + horizon * 1e6, rt, ry) - y0
            human = -np.sin(yaw) * fx + np.cos(yaw) * fy
            errors[horizon].append(float(near[0][2] - human))
    return errors


def summary(values: list[float]) -> dict:
    v = np.array(values)
    return {
        "n": len(v),
        "median_m": round(float(np.median(v)), 2) if len(v) else None,
        "left": round(float(np.mean(v > SIDE_M)), 2) if len(v) else None,
        "right": round(float(np.mean(v < -SIDE_M)), 2) if len(v) else None,
    }


def kept(queues: list[Path]) -> list[dict]:
    found = []
    for queue in queues:
        for path in queue_entries(queue):
            entry = load_entry(path)
            if entry["resolution"] == "ACCEPT" and "quarantine" not in entry:
                found.append(entry)
    return found


def main() -> int:
    study_queues = [
        q for q in sorted(STUDIES.rglob("queue")) if "aborted_" not in str(q)
    ]
    groups = {"studies": study_queues} | {
        name: [HARNESS / name] for name in (sys.argv[1:] or BATCHES)
    }
    report = {}
    fig, ax = plt.subplots(figsize=(4.6, 2.8), facecolor=SURFACE)
    _style(ax)
    colors = {
        "studies": "#eb6834",
        "s1_queue": "#2a78d6",
        "b2_queue": "#8c8c8c",
        "v1_queue": "#1baf7a",
    }
    for name, queues in groups.items():
        runs = [run_offsets(ROOT / e["run_dir"]) for e in kept(queues)]
        curve = [(s, [r["after"][s] for r in runs if s in r["after"]]) for s in CURVE_S]
        curve = [(s, v) for s, v in curve if len(v) >= 5]
        xs = [s for s, _ in curve]
        color = colors.get(name, TEXT_SECONDARY)
        ax.plot(xs, [np.median(v) for _, v in curve], color=color, linewidth=1.6,
                label=f"{name.removesuffix('_queue')} (n={len(runs)})")  # fmt: skip
        ax.fill_between(
            xs,
            [np.percentile(v, 25) for _, v in curve],
            [np.percentile(v, 75) for _, v in curve],
            color=color,
            alpha=0.15,
            linewidth=0,
        )
        report[name] = {
            "after_handoff": {
                s: summary([r["after"][s] for r in runs if s in r["after"]])
                for s in AFTER_S
            },
            "at_end": summary([r["at_end"] for r in runs]),
            "at_failure": summary([r["at_end"] for r in runs if r["failed"]]),
        }
    ax.axhline(0, color=TEXT_SECONDARY, linewidth=0.6)
    ax.set_xlabel(
        "seconds after the policy takes over", fontsize=8, color=TEXT_SECONDARY
    )
    ax.set_ylabel("offset from the human's path, m\n(left +; median, quartiles)",
                  fontsize=8, color=TEXT_SECONDARY)  # fmt: skip
    ax.set_title("The policy drifts left", fontsize=9, color=TEXT, loc="left")
    ax.legend(fontsize=7, frameon=False)
    fig.tight_layout()
    _save(fig, "drift")

    open_loop = {h: [] for h in PLAN_HORIZONS_S}
    for entry in kept(study_queues):
        if entry["config"].get("ego_speed_scale", 1.0) != 1.0:
            continue
        for horizon, values in warmup_plan_errors(ROOT / entry["run_dir"]).items():
            open_loop[horizon] += values
    report["open_loop_warmup_plans"] = {
        h: {**summary(v), "mean_m": round(float(np.mean(v)), 2) if v else None}
        for h, v in open_loop.items()
    }
    (ROOT / "research" / "drift.json").write_text(json.dumps(report, indent=1) + "\n")
    lines = [
        "# Which way the policy drifts",
        "",
        "Generated by `harness/drift_analysis.py`: the ego's signed lateral offset",
        "from the recorded human path (left positive) after the policy takes over;",
        f"left or right means more than {SIDE_M} m. 0 at the hand-off by construction.",
        "",
        "| runs | "
        + " | ".join(f"+{s:g} s" for s in AFTER_S)
        + " | at the end | at a failure |",
        "|---|" + "---|" * (len(AFTER_S) + 2),
    ]
    for name, r in report.items():
        if name == "open_loop_warmup_plans":
            continue
        cells = [r["after_handoff"][s] for s in AFTER_S] + [
            r["at_end"],
            r["at_failure"],
        ]
        lines.append(
            f"| {name} (n={r['at_end']['n']}) | "
            + " | ".join(
                f"{c['median_m']:+.2f} m, {c['left']:.0%} left, {c['right']:.0%} right"
                if c["n"]
                else "-"
                for c in cells
            )
            + " |"
        )
    lines += [
        "",
        "Open loop: warm-up plans (the ego on its recording) against where the",
        "human went, study runs at the recorded ego speed; left or right means",
        "more than the side threshold.",
        "",
        "| plan horizon | plans | median | mean | left | right |",
        "|---|---|---|---|---|---|",
    ]
    for h, c in report["open_loop_warmup_plans"].items():
        lines.append(
            f"| +{h:g} s | {c['n']} | {c['median_m']:+.2f} m | {c['mean_m']:+.2f} m "
            f"| {c['left']:.0%} | {c['right']:.0%} |"
        )
    (ROOT / "research" / "DRIFT.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
