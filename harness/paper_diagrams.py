"""The paper's two diagrams, in the figures' style (paper_figures.STYLE).

- fig_framework: the two loops (Fig. 1). Top band, the outer loop: a brief
  becomes a checked plan, a proposer picks each round, the goal check decides
  when to stop, and each failure is explained before the report. Bottom band,
  the inner loop: every run is checked before and after it runs, kept with its
  outcome or healed, and each finished batch is audited.
- fig_investigator: the inner loop's investigator (Fig. 2). (a) its five
  steps, of which only the third is the agent; (b) one real failure traced
  through them (harness/c4smoke_queue, run c4k_006, 20 Oct 2026).

Agent orange, plain code blue, a person grey, the simulator white. Written
to figures/paper/ as PDF and PNG.

    uv run python research/harness/paper_diagrams.py
"""

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

sys.path.insert(0, str(Path(__file__).resolve().parent))

from paper_figures import DOUBLE, OUT, STYLE, save

KIND = {
    "agent": ("#FDE3D6", "#E8693A"),
    "code": ("#E3EEFB", "#2A78D6"),
    "person": ("#EEEEEE", "#7A7D82"),
    "sim": ("#FFFFFF", "#444444"),
}
INK, MUTED = "#1C1C1C", "#5F6368"


def box(ax, x, y, w, h, text, kind, size=6.6, mono=False, bold_first=False):
    fill, edge = KIND[kind]
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.05",
                                fc=fill, ec=edge, lw=0.8))
    lines = text.split("\n")
    family = "DejaVu Sans Mono" if mono else None
    if bold_first:
        ax.text(x + w / 2, y + h - 0.1, lines[0], ha="center", va="top", fontsize=size,
                weight="bold", color=INK)
        ax.text(x + w / 2, y + (h - 0.2) / 2, "\n".join(lines[1:]), ha="center", va="center",
                fontsize=size - 0.3, color=INK, linespacing=1.2, family=family)
    elif mono:
        ax.text(x + 0.09, y + h / 2, text, ha="left", va="center", fontsize=size, color=INK,
                linespacing=1.25, family=family)
    else:
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size, color=INK,
                linespacing=1.2)
    return (x, y, w, h)


def side(b, where):
    x, y, w, h = b
    return {"l": (x, y + h / 2), "r": (x + w, y + h / 2), "t": (x + w / 2, y + h),
            "b": (x + w / 2, y)}[where]


def arrow(ax, p, q, label=None, rad=0.0, label_at=0.5, dx=0.0, dy=0.06):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=6, lw=0.7, color="0.3",
                                 connectionstyle=f"arc3,rad={rad}", shrinkA=0, shrinkB=0))
    if label:
        x = p[0] + (q[0] - p[0]) * label_at + dx
        y = p[1] + (q[1] - p[1]) * label_at + dy
        ax.text(x, y, label, ha="center", va="bottom", fontsize=5.8, style="italic", color=MUTED)


def band(ax, y0, y1, title, title_x=0.12):
    ax.add_patch(FancyBboxPatch((0.04, y0), DOUBLE - 0.08, y1 - y0,
                                boxstyle="round,pad=0,rounding_size=0.06",
                                fc="none", ec="0.6", lw=0.6, ls=(0, (3, 2))))
    ax.text(title_x, y1 - 0.06, title, ha="left", va="top", fontsize=6.8, color=MUTED, style="italic")


def legend(ax, x, y):
    for i, (kind, label) in enumerate((("agent", "the agent proposes"), ("code", "plain code checks and acts"),
                                       ("person", "a person"), ("sim", "the simulator"))):
        fill, edge = KIND[kind]
        xi = x + i * 1.35
        ax.add_patch(FancyBboxPatch((xi, y), 0.22, 0.12, boxstyle="round,pad=0,rounding_size=0.02",
                                    fc=fill, ec=edge, lw=0.7))
        ax.text(xi + 0.28, y + 0.06, label, ha="left", va="center", fontsize=6.2, color=MUTED)


def canvas(height):
    fig = plt.figure(figsize=(DOUBLE, height))
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_xlim(0, DOUBLE)
    ax.set_ylim(0, height)
    ax.axis("off")
    return fig, ax


def fig_framework() -> None:
    fig, ax = canvas(3.45)
    band(ax, 1.78, 3.38, "Outer loop: plan a study, choose each round of runs, stop at the goal")
    band(ax, 0.22, 1.7, "Inner loop: check every run before and after it runs; keep it or heal it", title_x=1.2)
    h = 0.42
    # Outer loop, top row.
    brief = box(ax, 0.15, 2.78, 0.85, h, "brief:\na question", "person")
    planner = box(ax, 1.2, 2.78, 0.95, h, "planner writes\na plan", "agent")
    plan_check = box(ax, 2.35, 2.78, 1.1, h, "plan check;\na person approves", "code")
    proposer = box(ax, 3.65, 2.78, 1.25, h, "proposer picks a round:\nthe agent, rules or a baseline", "agent", size=6.2)
    run_check = box(ax, 5.1, 2.78, 1.0, h, "run check:\nlegal scene, knobs", "code")
    arrow(ax, side(brief, "r"), side(planner, "l"))
    arrow(ax, side(planner, "r"), side(plan_check, "l"))
    arrow(ax, side(plan_check, "r"), side(proposer, "l"))
    arrow(ax, side(proposer, "r"), side(run_check, "l"))
    # Outer loop, bottom row.
    goal = box(ax, 0.15, 1.9, 1.15, h, "goal check:\n5 hardest confirmed?", "code")
    triage = box(ax, 1.75, 1.9, 1.1, h, "triage explains\neach failure", "agent")
    report = box(ax, 3.1, 1.9, 1.3, h, "report answers the brief;\ncode writes every number", "agent", size=6.2)
    arrow(ax, side(goal, "r"), side(triage, "l"), "met", label_at=0.5)
    arrow(ax, side(triage, "r"), side(report, "l"))
    arrow(ax, (1.1, 1.9 + h), (4.0, 2.78), "not met: next round", label_at=0.55, dx=-0.15, dy=0.03)
    # Inner loop, top row (right to left).
    preflight = box(ax, 5.55, 1.0, 1.4, h, "preflight + machine check:\nconfig legal, GPU, disk", "code", size=6.2)
    sim = box(ax, 3.95, 1.0, 1.35, h, "the policy drives\nin closed loop", "sim")
    postflight = box(ax, 2.05, 1.0, 1.65, h, "postflight: settings landed,\nknobs verified, physics, rules", "code", size=6.2)
    kept = box(ax, 0.15, 1.0, 1.5, h, "kept, with its outcome\n(the policy's failures only)", "code", size=6.2)
    arrow(ax, side(run_check, "b"), (6.0, 1.0 + h), "every run", label_at=0.45, dx=0.3, dy=-0.03)
    arrow(ax, side(preflight, "l"), side(sim, "r"))
    arrow(ax, side(sim, "l"), side(postflight, "r"))
    arrow(ax, side(postflight, "l"), side(kept, "r"), "pass", label_at=0.5)
    arrow(ax, side(kept, "t"), side(goal, "b"), "kept outcomes", label_at=0.22, dx=-0.42, dy=-0.02)
    # Inner loop, bottom row.
    auditor = box(ax, 0.15, 0.32, 1.1, h, "batch audit flags runs,\nproposes rules", "agent", size=6.2)
    admit = box(ax, 1.42, 0.32, 1.2, h, "rule admitted by code;\na person enacts it", "code", size=6.2)
    investigator = box(ax, 2.95, 0.32, 1.3, h, "investigator picks\none of five skills", "agent")
    validator = box(ax, 4.45, 0.32, 1.35, h, "validator, then the\nrecovery script", "code")
    person = box(ax, 6.0, 0.32, 0.95, h, "halted:\na person", "person")
    arrow(ax, side(kept, "b"), (0.7, 0.32 + h), "each batch", label_at=0.45, dx=0.3, dy=-0.03)
    arrow(ax, side(auditor, "r"), side(admit, "l"))
    arrow(ax, (2.3, 0.32 + h), (2.5, 1.0), "every later run", label_at=0.55, dx=-0.42, dy=-0.04)
    arrow(ax, (3.3, 1.0), (3.5, 0.32 + h), "fail", label_at=0.5, dx=0.14, dy=-0.04)
    arrow(ax, side(investigator, "r"), side(validator, "l"))
    arrow(ax, (5.6, 0.32 + h), (6.1, 1.0), "retry", label_at=0.5, dx=-0.17, dy=-0.04)
    arrow(ax, side(validator, "r"), side(person, "l"), "HALT", label_at=0.5)
    legend(ax, 1.25, 0.04)
    save(fig, "fig_framework")


def fig_investigator() -> None:
    fig, ax = canvas(2.55)
    ax.text(0.06, 2.5, "(a) the five steps; only step 3 is the agent", ha="left", va="top",
            fontsize=7, color=INK)
    steps = (
        ("code", "1. When\na run has failed;\ncode calls a fresh agent,\nno memory of earlier calls"),
        ("code", "2. What it sees\nstatus, config, attempts left,\nerror lines, machine state;\nread-only tools"),
        ("agent", "3. What it answers\none skill and its params:\nRE-RUN, CONFIGURE,\nRESTART_CLEANUP,\nCLEANUP_ENV, HALT"),
        ("code", "4. Who checks it\nthe validator: a legal skill,\nlegal params, an attempt\nleft; else rejected"),
        ("code", "5. Who acts\nthe recovery script;\nthe agent never touches\nthe simulator"),
    )
    w, gap = 1.3, 0.115
    for i, (kind, text) in enumerate(steps):
        x = 0.08 + i * (w + gap)
        b = box(ax, x, 1.42, w, 0.9, text, kind, size=6.4, bold_first=True)
        if i < 4:
            arrow(ax, side(b, "r"), (x + w + gap, 1.42 + 0.45))
    ax.text(0.06, 1.25, "(b) one real failure, traced (20 Oct 2026)", ha="left", va="top",
            fontsize=7, color=INK)
    seen = box(ax, 0.08, 0.12, 2.05, 0.95,
               "status: FAILED\nreason: docker network create\n  failed: all address pools\n  used; 29 AlpaSim networks\nattempt: 1 of 3\nmachine: one other run in flight",
               "code", size=5.6, mono=True)
    tools = box(ax, 2.3, 0.12, 1.55, 0.95,
                "read-only tools:\n$ docker network ls\n$ docker ps -a\n  --format ...networks\n\n15 s, one call",
                "agent", size=5.6, mono=True)
    ax.add_patch(FancyBboxPatch((4.02, 0.42), 1.38, 0.38, boxstyle="round,pad=0,rounding_size=0.04",
                                fc=INK, ec=INK, lw=0.8))
    ax.text(4.71, 0.61, '{"skill": "CLEANUP_ENV",\n "params": {}}', ha="center", va="center",
            fontsize=5.8, color="white", family="DejaVu Sans Mono", linespacing=1.2)
    acted = box(ax, 5.57, 0.12, 1.5, 0.95,
                "validator: accepted\n\nrecovery script:\nremoved 28 leftover\nnetworks; the rerun\nwas kept",
                "code", size=6.2)
    arrow(ax, side(seen, "r"), side(tools, "l"))
    arrow(ax, side(tools, "r"), (4.02, 0.61))
    arrow(ax, (5.4, 0.61), side(acted, "l"))
    save(fig, "fig_investigator")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update(STYLE)
    fig_framework()
    fig_investigator()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
