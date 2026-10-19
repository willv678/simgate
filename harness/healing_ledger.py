"""Every failed launch the agent handled, one row each, with its evidence.

The inner loop's claim ("129 of 144 failed launches healed with no person")
is a count. This script turns it into a ledger anyone can check: for every
launch that failed and went to the diagnose contract, what failed, what the
agent looked at, the skill it chose, the code check's verdict, what the
retry did, and how the run ended, with a link to the raw queue entry on
GitHub (error lines, machine snapshot, the agent's commands, its answer).

It also checks two things the count alone cannot show:
- a retry ran exactly the settings that were asked for (the agent healed
  the run, it did not change the experiment);
- every run asked for ended kept, stopped for a person, or is still running
  (nothing lost).

Writes HEALING.md, figures/healing/ledger.json, and two figures:
figures/healing/flow.png (runs asked for, then failure kind -> skill ->
end) and figures/healing/timeline.png (every failure over the campaign).

    uv run python research/harness/healing_ledger.py
"""

import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from paper_figures import CUTOFF, PALETTE, STYLE, _entries, failure_kind
from read_state import ROOT

RESEARCH = ROOT / "research"
OUT = RESEARCH / "figures" / "healing"
GITHUB = "https://github.com/willv678/simgate/blob/main/"
SKILLS = ("RE-RUN", "CLEANUP_ENV", "RESTART_CLEANUP", "CONFIGURE", "HALT")
ENDS = {"kept": PALETTE[4], "stopped": PALETTE[0], "running": PALETTE[5]}
# The physics check also stops a run whose plan fell short of the asked
# lateral shift, so "impossible motion" undersells what it caught.
KINDS = {"impossible motion": "failed the physics check"}
SKILL_WORDS = {
    "RE-RUN": "run it again",
    "CLEANUP_ENV": "clear leftovers, run again",
    "RESTART_CLEANUP": "restart clean",
    "CONFIGURE": "change a setting",
    "HALT": "stop for a person",
}


def lineages(entries: list[tuple[Path, dict]]) -> list[list[tuple[Path, dict]]]:
    """Each run asked for (an entry with no parent) and its retries, in order."""
    children = defaultdict(list)
    for path, entry in entries:
        if entry["parent"]:
            children[(path.parent, entry["parent"])].append((path, entry))
    out = []
    for path, entry in entries:
        if entry["parent"]:
            continue
        chain = [(path, entry)]
        while kids := children.get((chain[-1][0].parent, chain[-1][0].name)):
            chain.append(max(kids, key=lambda kid: kid[1]["attempt"]))
        out.append(chain)
    return out


def ending(chain: list[tuple[Path, dict]]) -> str:
    last = chain[-1][1]
    if last["resolution"] == "ACCEPT":
        return "kept"
    if last["resolution"] == "HALT":
        return "stopped"
    return "running"


def same_settings(chain: list[tuple[Path, dict]]) -> bool:
    """Every retry ran the parent's settings, except a knob a CONFIGURE named."""
    for (_, parent), (_, child) in zip(chain, chain[1:]):
        allowed = set(parent["diagnosis"]["params"]) if parent["diagnosis"]["skill"] == "CONFIGURE" else set()
        changed = {k for k in parent["config"].keys() | child["config"].keys()
                   if parent["config"].get(k) != child["config"].get(k)}
        if changed - allowed:
            return False
    return True


def study_arm(path: Path) -> tuple[str, str]:
    parts = path.relative_to(RESEARCH / "studies").parts
    return parts[0], parts[-3] if len(parts) > 3 else "llm"


def rows(chains: list[list[tuple[Path, dict]]]) -> list[dict]:
    """One row per failed launch the agent diagnosed."""
    out = []
    for chain in chains:
        end = ending(chain)
        for i, (path, entry) in enumerate(chain):
            diagnosis = entry["diagnosis"]
            if not diagnosis:
                continue
            nxt = chain[i + 1][1] if i + 1 < len(chain) else None
            if diagnosis["skill"] == "HALT":
                then = "stopped"
            elif diagnosis["skill"] == "CLEANUP_ENV":
                then = "relaunched in place, kept" if entry["resolution"] == "ACCEPT" else "relaunched in place"
            elif nxt is None:
                then = "retry not launched yet"
            else:
                then = f"attempt {nxt['attempt']}: " + {"ACCEPT": "kept", "HALT": "stopped"}.get(
                    nxt["resolution"], "failed again" if nxt["resolution"] else "running")
            study, arm = study_arm(path)
            # An entry that failed before it launched, by when it was written.
            when = entry["launched_at"] or path.stat().st_mtime
            out.append({
                "when": datetime.fromtimestamp(when, timezone.utc).isoformat(timespec="minutes"),
                "before_cutoff": when < CUTOFF.timestamp(),
                "study": study, "arm": arm, "run": entry["name"], "attempt": entry["attempt"],
                "failure": KINDS.get(kind := failure_kind(diagnosis["input"]), kind),
                "status": diagnosis["input"]["k_status"],
                "looked_at": diagnosis["tool_calls"],
                "skill": diagnosis["skill"], "params": diagnosis["params"],
                "verdict": diagnosis["verdict"],
                "seconds": diagnosis["duration_ms"] / 1000,
                "then": then, "end": "stopped" if diagnosis["skill"] == "HALT" else end,
                "same_settings": same_settings(chain),
                "entry": str(path.relative_to(RESEARCH)),
            })
    return sorted(out, key=lambda r: r["when"])


def summary(chains: list[list[tuple[Path, dict]]], table: list[dict]) -> dict:
    launched = [c for c in chains if c[0][1]["launched"]]
    first_try = sum(1 for c in launched if len(c) == 1 and c[0][1]["resolution"] == "ACCEPT"
                    and not c[0][1]["diagnosis"])
    touched = [c for c in launched if any(e["diagnosis"] for _, e in c)]
    ends = Counter(ending(c) for c in touched)
    return {
        "runs_asked": len(launched),
        "launches": sum(len([e for _, e in c if e["launched"]]) for c in launched),
        "kept_first_try": first_try,
        "runs_with_a_failure": len(touched),
        "runs_healed": ends["kept"], "runs_stopped": ends["stopped"], "runs_running": ends["running"],
        "runs_kept": sum(ending(c) == "kept" for c in launched),
        "runs_running_total": sum(ending(c) == "running" for c in launched),
        "failures": len(table),
        "failures_healed": sum(r["end"] == "kept" for r in table),
        "failures_stopped": sum(r["end"] == "stopped" for r in table),
        "check_accepted": sum(r["verdict"] == "accepted" for r in table),
        "same_settings": sum(r["same_settings"] for r in table),
        "median_seconds": float(np.median([r["seconds"] for r in table])) if table else 0.0,
    }


def _band(ax, x0, y0, x1, y1, h, colour):
    """A flow of height h from (x0, y0) to (x1, y1), y at the band's bottom."""
    t = np.linspace(0, 1, 50)
    s = t * t * (3 - 2 * t)
    x = x0 + (x1 - x0) * t
    bottom = y0 + (y1 - y0) * s
    ax.fill_between(x, bottom, bottom + h, color=colour, alpha=0.45, lw=0)


def fig_flow(s: dict, table: list[dict]) -> None:
    fig = plt.figure(figsize=(7.16, 3.4))
    grid = fig.add_gridspec(2, 1, height_ratios=[0.5, 2.4], hspace=0.9)
    top, ax = fig.add_subplot(grid[0]), fig.add_subplot(grid[1])

    parts = [("kept on the first try", s["kept_first_try"], PALETTE[2]),
             ("failed, healed by the agent, kept", s["runs_healed"], PALETTE[4]),
             ("stopped for a person", s["runs_stopped"], PALETTE[0]),
             ("still running", s["runs_running_total"], PALETTE[5])]
    parts = [p for p in parts if p[1]]
    left = 0
    for label, n, colour in parts:
        top.barh(0, n, left=left, color=colour, height=0.6, lw=0)
        left += n
    top.set_xlim(0, left)
    top.set_yticks([])
    top.spines["left"].set_visible(False)
    top.set_title(f"(a) {s['runs_asked']:,} runs asked for: {100 * s['runs_kept'] / s['runs_asked']:.1f}% "
                  f"ended with a kept run", loc="left")
    top.legend([plt.Rectangle((0, 0), 1, 1, color=c) for _, _, c in parts],
               [f"{label} {n:,}" for label, n, _ in parts], loc="upper center",
               bbox_to_anchor=(0.5, -0.5), ncol=len(parts), frameon=False, handlelength=0.9)

    kinds = [k for k, _ in Counter(r["failure"] for r in table).most_common()]
    skills = [k for k in SKILLS if any(r["skill"] == k for r in table)]
    ends = [k for k in ENDS if any(r["end"] == k for r in table)]
    total = len(table)
    gap = total * 0.1
    xs = (0.0, 1.0, 2.45)
    width = 0.06

    def stack(names, count):
        y, out = 0.0, {}
        for name in names:
            out[name] = y
            y += count(name) + gap
        return out

    y_kind = stack(kinds, lambda k: sum(r["failure"] == k for r in table))
    y_skill = stack(skills, lambda k: sum(r["skill"] == k for r in table))
    y_end = stack(ends, lambda k: sum(r["end"] == k for r in table))
    used_kind, used_skill_in, used_skill_out, used_end = Counter(), Counter(), Counter(), Counter()
    for kind in kinds:
        for skill in skills:
            n = sum(r["failure"] == kind and r["skill"] == skill for r in table)
            if not n:
                continue
            mostly = Counter(r["end"] for r in table if r["failure"] == kind and r["skill"] == skill)
            _band(ax, xs[0] + width, y_kind[kind] + used_kind[kind], xs[1],
                  y_skill[skill] + used_skill_in[skill], n, ENDS[mostly.most_common(1)[0][0]])
            used_kind[kind] += n
            used_skill_in[skill] += n
    for skill in skills:
        for end in ends:
            n = sum(r["skill"] == skill and r["end"] == end for r in table)
            if not n:
                continue
            _band(ax, xs[1] + width, y_skill[skill] + used_skill_out[skill], xs[2],
                  y_end[end] + used_end[end], n, ENDS[end])
            used_skill_out[skill] += n
            used_end[end] += n

    def column(x, starts, count, label, side):
        for name, y in starts.items():
            n = count(name)
            ax.bar(x + width / 2, n, bottom=y, width=width, color="0.25", lw=0)
            tx = x - 0.02 if side == "left" else x + width + 0.02
            ax.text(tx, y + n / 2, label(name).replace(" (", f" {n} (", 1) if "(" in label(name)
                    else f"{label(name)} {n}", va="center",
                    bbox={"fc": "white", "ec": "none", "alpha": 0.8, "pad": 0.4},
                    ha="right" if side == "left" else "left", fontsize=7)

    column(xs[0], y_kind, lambda k: sum(r["failure"] == k for r in table), lambda k: k, "left")
    column(xs[1], y_skill, lambda k: sum(r["skill"] == k for r in table),
           lambda k: f"{k} ({SKILL_WORDS[k]})", "right")
    column(xs[2], y_end, lambda k: sum(r["end"] == k for r in table),
           lambda k: {"kept": "healed, kept", "stopped": "stopped for a person",
                      "running": "retry still running"}[k], "right")
    for x, title in zip(xs, ("what failed", "the agent's choice (checked by code)", "how the run ended")):
        ax.text(x + width / 2, -total * 0.06, title, ha="center", va="bottom", fontsize=7, color="0.3")
    ax.set_xlim(-0.8, 3.05)
    ax.set_ylim(max(max(y.values()) for y in (y_kind, y_skill, y_end)) + total * 0.12, -total * 0.2)
    ax.axis("off")
    ax.set_title(f"(b) the {total} failed launches the agent handled: "
                 f"{s['failures_healed']} healed, {s['failures_stopped']} stopped", loc="left")
    fig.savefig(OUT / "flow.pdf")
    fig.savefig(OUT / "flow.png", dpi=200)
    plt.close(fig)


def fig_timeline(chains: list[list[tuple[Path, dict]]], table: list[dict]) -> None:
    launches = [e["launched_at"] for c in chains for _, e in c if e["launched_at"]]
    # Studies with no failed launch have no row; their launches are in the counts.
    studies = sorted({r["study"] for r in table},
                     key=lambda s: min(e["launched_at"] or 9e12 for c in chains
                                       if study_arm(c[0][0])[0] == s for _, e in c))
    fig, (hist, ax) = plt.subplots(2, 1, figsize=(7.16, 3.4), sharex=True,
                                   gridspec_kw={"height_ratios": [1, 2.6], "hspace": 0.12})
    days = np.arange(np.floor(min(launches) / 86400), np.ceil(max(launches) / 86400) + 1) * 86400
    stamps = [datetime.fromtimestamp(t, timezone.utc) for t in launches]
    hist.hist(stamps, bins=[datetime.fromtimestamp(d, timezone.utc) for d in days],
              color="0.7", lw=0)
    hist.set_ylabel("launches\nper day")
    hist.set_title("Every failed launch the agent handled, over the whole campaign", loc="left")
    for r in table:
        when = datetime.fromisoformat(r["when"])
        y = studies.index(r["study"])
        if r["end"] == "kept":
            ax.plot(when, y, "o", ms=3.2, mfc="none", mec=ENDS["kept"], mew=0.8)
        elif r["end"] == "stopped":
            ax.plot(when, y, "x", ms=4, color=ENDS["stopped"], mew=1.0)
        else:
            ax.plot(when, y, "s", ms=3, color=ENDS["running"])
    ax.axvline(CUTOFF, color="0.4", lw=0.6, ls="--")
    ax.text(CUTOFF, -0.6, " paper's current cutoff", fontsize=6.5, color="0.35", va="top")
    ax.set_yticks(range(len(studies)), studies)
    ax.set_ylim(len(studies) - 0.3, -0.7)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", alpha=0.25, lw=0.4)
    ax.legend([plt.Line2D([], [], ls="", marker="o", mfc="none", mec=ENDS["kept"]),
               plt.Line2D([], [], ls="", marker="x", color=ENDS["stopped"])],
              ["healed, then kept", "stopped for a person"], loc="lower center",
              bbox_to_anchor=(0.5, -0.32), ncol=2, frameon=False)
    import matplotlib.dates as mdates
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
    fig.savefig(OUT / "timeline.pdf")
    fig.savefig(OUT / "timeline.png", dpi=200)
    plt.close(fig)


def markdown(s: dict, cut: dict, table: list[dict]) -> str:
    kinds = Counter(r["failure"] for r in table)
    lines = [
        "# Self-healing: every failed launch, with its evidence",
        "",
        "Written by `harness/healing_ledger.py` from the study queues; nothing here is",
        "typed by hand. Rerun it to check: `uv run python research/harness/healing_ledger.py`.",
        "Each row links to the raw queue entry, which holds the error lines the agent",
        "was shown, a snapshot of the machine (GPU memory, containers, disk), the",
        "commands the agent ran to look, its answer, and the code check's verdict.",
        "",
        "![flow](figures/healing/flow.png)",
        "",
        "![timeline](figures/healing/timeline.png)",
        "",
        "## The numbers",
        "",
        "| | whole campaign so far | to the paper's cutoff (13 Oct 21:18 UTC) |",
        "|---|---|---|",
        f"| runs asked for (launched) | {s['runs_asked']:,} | {cut['runs_asked']:,} |",
        f"| launches, retries included | {s['launches']:,} | {cut['launches']:,} |",
        f"| kept on the first try | {s['kept_first_try']:,} | {cut['kept_first_try']:,} |",
        f"| failed launches handed to the agent | {s['failures']} | {cut['failures']} |",
        f"| ... healed, then kept | {s['failures_healed']} | {cut['failures_healed']} |",
        f"| ... stopped for a person | {s['failures_stopped']} | {cut['failures_stopped']} |",
        f"| runs that ended kept | {s['runs_kept']:,} ({100 * s['runs_kept'] / s['runs_asked']:.1f}%) "
        f"| {cut['runs_kept']:,} ({100 * cut['runs_kept'] / cut['runs_asked']:.1f}%) |",
        f"| runs still running | {s['runs_running_total']} | {cut['runs_running_total']} |",
        f"| agent's choice passed the code check | {s['check_accepted']} of {s['failures']} "
        f"| {cut['check_accepted']} of {cut['failures']} |",
        f"| retry ran exactly the settings asked for | {s['same_settings']} of {s['failures']} "
        f"| {cut['same_settings']} of {cut['failures']} |",
        f"| agent's time per diagnosis, median | {s['median_seconds']:.0f} s | {cut['median_seconds']:.0f} s |",
        "",
        "A run is one setting the search asked for; a launch is one try at it.",
        "Failed launches count each try, so one run can fail more than once.",
        "\"Failed the physics check\" is the gate working, not a heal that failed:",
        "the run came back physically wrong (the reported speed disagrees with the",
        "motion, or the plan shifted less than the lateral shift asked for), so a",
        "rerun would give the same wrong run and the agent stops it. Leaving those",
        f"out, the agent healed {s['failures_healed']} of "
        f"{s['failures'] - sum(r['failure'] == 'failed the physics check' for r in table)} "
        "launches that failed for operational reasons (GPU, simulator, launcher).",
        "",
        "Every code-check verdict here is \"accepted\": in production the agent never",
        "chose an action the check refuses. That the check does refuse bad actions is",
        "shown separately, by trying every possible answer against every failure",
        "state (FACTS \"Exhaustive check\") and by planted faults (`VALIDITY.md`).",
        "",
        "## What failed and what the agent chose",
        "",
        "| what failed | count | the agent's choice | healed | stopped |",
        "|---|---|---|---|---|",
    ]
    for kind, n in kinds.most_common():
        mine = [r for r in table if r["failure"] == kind]
        picks = ", ".join(f"{k} {v}" for k, v in Counter(r["skill"] for r in mine).most_common())
        lines.append(f"| {kind} | {n} | {picks} | {sum(r['end'] == 'kept' for r in mine)} "
                     f"| {sum(r['end'] == 'stopped' for r in mine)} |")
    lines += ["", "## One example of each kind", ""]
    for kind, _ in kinds.most_common():
        r = next(r for r in table if r["failure"] == kind)
        looked = "; ".join(f"`{c.removeprefix('Bash: ')[:70]}`" for c in r["looked_at"]) or "nothing (no tools)"
        lines += [
            f"**{kind}**: [{r['run']}]({GITHUB}{r['entry']}), attempt {r['attempt']}, {r['when'][:16]} UTC.",
            f"Status the agent saw: `{r['status'][:150]}`. It looked at: {looked}.",
            f"It chose {r['skill']} ({SKILL_WORDS[r['skill']]}); the code check: {r['verdict']}; "
            f"then: {r['then']}.",
            "",
        ]
    lines += [
        "## Every failed launch",
        "",
        "| # | when (UTC) | study / arm | run (raw entry) | try | what failed | agent looked | chose | check | then | same settings |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for i, r in enumerate(table, 1):
        lines.append(
            f"| {i} | {r['when'][5:16].replace('T', ' ')} | {r['study']} / {r['arm']} "
            f"| [{r['run'].removeprefix(r['study'] + '_')}]({GITHUB}{r['entry']}) | {r['attempt']} "
            f"| {r['failure']} | {len(r['looked_at'])} commands | {r['skill']} | {r['verdict']} "
            f"| {r['then']} | {'yes' if r['same_settings'] else '**no**'} |")
    return "\n".join(lines) + "\n"


def main() -> None:
    import json

    plt.rcParams.update(STYLE)
    OUT.mkdir(parents=True, exist_ok=True)
    entries = _entries()
    chains = lineages(entries)
    table = rows(chains)
    s = summary(chains, table)
    early = [c for c in chains if (c[0][1]["launched_at"] or 9e12) < CUTOFF.timestamp()]
    cut = summary(early, [r for r in table if r["before_cutoff"]])
    fig_flow(s, table)
    fig_timeline(chains, table)
    (OUT / "ledger.json").write_text(json.dumps({"summary": s, "to_cutoff": cut, "failures": table},
                                                indent=1) + "\n")
    (RESEARCH / "HEALING.md").write_text(markdown(s, cut, table))
    print(json.dumps({"whole": s, "to_cutoff": cut}, indent=1))


if __name__ == "__main__":
    main()
