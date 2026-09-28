"""Batch timeline figure for L11.

Reads the L7 trace, the L8 trace, and the L6 comparison table.
Writes research/batch_timeline.png.
"""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[2]
L7 = ROOT / "research" / "harness" / "l7_trace.jsonl"
L8 = ROOT / "research" / "harness" / "l8_trace.jsonl"
COMPARISON = ROOT / "research" / "harness" / "comparison_table.txt"
OUTPUT = ROOT / "research" / "batch_timeline.png"

FACE = {
    "veto": "#F6D7C8",
    "recover": "#F8E8C2",
    "launch": "#D7E5F4",
    "keep": "#D5EDDF",
}
EDGE = {
    "veto": "#B85C38",
    "recover": "#A67C2D",
    "launch": "#3D6F99",
    "keep": "#2F7D57",
}


def _rows(path: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _comparison(path: Path) -> tuple[list[tuple[str, str]], dict[str, str]]:
    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    pairs = []
    meta: dict[str, str] = {}
    for line in lines[1:]:
        parts = line.split("\t")
        if parts[0] in {"agreement", "model_wins"}:
            meta[parts[0]] = parts[1]
        else:
            pairs.append((parts[0], parts[1]))
    return pairs, meta


def _flag(value: bool) -> str:
    return "true" if value else "false"


def l7_steps(rows: list[dict]) -> list[dict]:
    steps = []
    for row in rows:
        skill = row["skill"]
        if skill == "CONFIGURE":
            steps.append(
                {
                    "skill": skill,
                    "role": "veto",
                    "detail": f"context_length {row['input']['context_length']}",
                    "stay": "out",
                }
            )
        elif skill == "RE-RUN":
            steps.append(
                {
                    "skill": skill,
                    "role": "recover",
                    "detail": "metrics missing",
                    "stay": "out",
                }
            )
        elif skill == "ACCEPT":
            steps.append(
                {
                    "skill": skill,
                    "role": "keep",
                    "detail": (
                        f"at-fault {_flag(row['at_fault_collision'])}, "
                        f"rear {_flag(row['rear_contact'])}"
                    ),
                    "stay": "kept",
                }
            )
        else:
            raise ValueError(skill)
    return steps


def l8_steps(rows: list[dict]) -> list[dict]:
    steps = []
    for row in rows:
        skill = row["skill"]
        if skill == "CONFIGURE":
            steps.append(
                {
                    "skill": skill,
                    "role": "veto",
                    "detail": f"context_length {row['input']['context_length']}",
                    "stay": "not launched",
                }
            )
        elif skill == "LAUNCH":
            steps.append(
                {
                    "skill": skill,
                    "role": "launch",
                    "detail": Path(row["params"]["run_dir"]).name,
                    "stay": "",
                }
            )
        elif skill == "RE-RUN":
            steps.append(
                {
                    "skill": skill,
                    "role": "recover",
                    "detail": Path(row["params"]["run_dir"]).name,
                    "stay": "out",
                }
            )
        elif skill == "ACCEPT":
            steps.append(
                {
                    "skill": skill,
                    "role": "keep",
                    "detail": (
                        f"at-fault {_flag(row['at_fault_collision'])}, "
                        f"rear {_flag(row['rear_contact'])}"
                    ),
                    "stay": "kept",
                }
            )
        else:
            raise ValueError(skill)
    return steps


def _draw_lane(ax, steps: list[dict], y: float, label: str) -> None:
    width, height, gap = 1.62, 1.05, 0.22
    ax.text(
        -0.08,
        y + height / 2,
        label,
        ha="right",
        va="center",
        fontsize=9,
        fontweight="bold",
        color="#222",
    )
    for index, step in enumerate(steps):
        x = index * (width + gap)
        patch = FancyBboxPatch(
            (x, y),
            width,
            height,
            boxstyle="round,pad=0.02,rounding_size=0.08",
            facecolor=FACE[step["role"]],
            edgecolor=EDGE[step["role"]],
            linewidth=1.2,
        )
        ax.add_patch(patch)
        stay = step["stay"]
        body = f"{step['skill']}\n{step['detail']}"
        if stay:
            body = f"{body}\n{stay}"
        ax.text(
            x + width / 2,
            y + height / 2,
            body,
            ha="center",
            va="center",
            fontsize=7.5,
            color="#1c1c1c",
            linespacing=1.25,
        )
        if index + 1 < len(steps):
            ax.annotate(
                "",
                xy=(x + width + gap - 0.02, y + height / 2),
                xytext=(x + width + 0.02, y + height / 2),
                arrowprops={"arrowstyle": "-|>", "color": "#555", "lw": 0.9},
            )


def _agreement_line(pairs: list[tuple[str, str]], meta: dict[str, str]) -> str:
    cells = ", ".join(f"{script}/{model}" for script, model in pairs)
    return (
        f"L6 agreement {meta['agreement']}. "
        f"Script/model: {cells}. "
        f"model_wins {meta['model_wins']}."
    )


def main() -> None:
    l7 = l7_steps(_rows(L7))
    l8 = l8_steps(_rows(L8))
    pairs, meta = _comparison(COMPARISON)
    if len(l7) != 3 or len(l8) != 5:
        raise SystemExit(f"unexpected step counts: L7={len(l7)} L8={len(l8)}")

    fig, ax = plt.subplots(figsize=(10.6, 4.6), dpi=200)
    _draw_lane(ax, l7, 2.15, "L7")
    _draw_lane(ax, l8, 0.55, "L8")
    ax.set_xlim(-0.85, 9.15)
    ax.set_ylim(0.15, 3.55)
    ax.axis("off")
    ax.set_title(
        "Batch timeline: skill, veto, recovery, and what stays in the dataset",
        loc="left",
        fontsize=11,
        pad=8,
        color="#222",
    )
    ax.text(
        4.15,
        0.28,
        _agreement_line(pairs, meta),
        ha="center",
        va="top",
        fontsize=8,
        color="#222",
    )
    fig.tight_layout()
    fig.savefig(OUTPUT, bbox_inches="tight", facecolor="white")
    print(OUTPUT)


if __name__ == "__main__":
    main()
