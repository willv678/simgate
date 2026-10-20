"""The skill contract figure: the diagnose contract's five parts, with the
counts of failed launches it handled read from the healing ledger
(healing_ledger.py, to the paper's cutoff). Writes
figures/meeting/skill_contract.png and paper/figures/fig_skill_contract.png.

    uv run python research/harness/skill_contract_figure.py
"""

import json
import shutil
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

RESEARCH = Path(__file__).resolve().parent.parent
CODE, AGENT, EDGE_C, EDGE_A = "#e3eefb", "#fde3d6", "#2a78d6", "#e8693a"


def main() -> None:
    s = json.loads((RESEARCH / "figures" / "healing" / "ledger.json").read_text())["to_cutoff"]
    f, a = plt.subplots(figsize=(14, 5.2))
    a.set_xlim(0, 14)
    a.set_ylim(0, 5.2)
    a.axis("off")

    def box(x, y, w, h, title, body, fill, edge):
        a.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04,rounding_size=0.12",
                                   fc=fill, ec=edge, lw=2))
        a.text(x + 0.15, y + h - 0.25, title, fontsize=12, weight="bold", va="top")
        a.text(x + 0.15, y + h - 0.7, body, fontsize=10, va="top", linespacing=1.4)

    box(0.2, 2.2, 2.4, 2.4, "1. When", "read_state.py says\nthe run FAILED\n(one fresh call\nper failure)", CODE, EDGE_C)
    box(3.0, 2.2, 2.6, 2.4, "2. What it sees", "why it failed\nthe run's config\nerror lines\nmachine snapshot\nread-only tools", CODE, EDGE_C)
    box(6.0, 2.2, 2.6, 2.4, "3. Agent answers", "exactly one skill:\nRE-RUN\nCONFIGURE (allowed keys)\nCLEANUP_ENV\nRESTART_CLEANUP · HALT", AGENT, EDGE_A)
    box(9.0, 2.2, 2.3, 2.4, "4. Code checks", "validate_diagnosis.py\nrejects e.g. changing\nwhat the run measures,\na 2nd CLEANUP_ENV", CODE, EDGE_C)
    box(11.7, 2.2, 2.1, 2.4, "5. Code acts", "recover.py\nqueues the retry;\nthe gate checks\nthe new run", CODE, EDGE_C)
    for x1, x2 in ((2.6, 3.0), (5.6, 6.0), (8.6, 9.0), (11.3, 11.7)):
        a.add_patch(FancyArrowPatch((x1, 3.4), (x2, 3.4), arrowstyle="-|>", mutation_scale=16, lw=1.6, color="0.3"))
    a.text(0.2, 5.0, "A skill contract: advisor/CLAUDE.md (diagnose a failed run)", fontsize=14, weight="bold")
    a.text(0.2, 1.65, f"Measured over {s['launches']:,} launches: {s['failures']} failed launches went through this "
           f"contract → {s['failures_healed']} healed and kept, {s['failures_stopped']} stopped for a person.", fontsize=11)
    a.text(0.2, 1.2, "Exhaustive check: every answer the agent could give, at every failure state: 3,822 "
           "transitions, 0 violations, ≤ 3 launches per run.", fontsize=11)
    a.text(0.2, 0.75, "The same five parts structure all seven contracts: diagnose, plan a study, choose the "
           "next runs, audit a batch, triage, tag scenes, report.", fontsize=11)
    a.add_patch(FancyBboxPatch((9.6, 0.2), 0.35, 0.25, boxstyle="round,pad=0.02", fc=CODE, ec=EDGE_C))
    a.text(10.05, 0.32, "plain code", fontsize=10, va="center")
    a.add_patch(FancyBboxPatch((11.4, 0.2), 0.35, 0.25, boxstyle="round,pad=0.02", fc=AGENT, ec=EDGE_A))
    a.text(11.85, 0.32, "the agent (Claude)", fontsize=10, va="center")
    out = RESEARCH / "figures" / "meeting" / "skill_contract.png"
    f.savefig(out, dpi=200, bbox_inches="tight")
    shutil.copy(out, RESEARCH / "paper" / "figures" / "fig_skill_contract.png")
    print(out)


if __name__ == "__main__":
    main()
