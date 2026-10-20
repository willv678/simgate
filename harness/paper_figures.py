"""The IV 2027 paper's figures and Table I, regenerated from the research repo.

Every number in these figures is read from the study queues, the rollout
logs, or a JSON file a harness script wrote; none is typed by hand. Each
figure is written to figures/paper/ as a PDF (vector, for the paper) and a
200-dpi PNG (for reading), at IEEE two-column sizes (single column 3.5 in,
double column 7.16 in), 8 pt serif.

- fig_discovery: confirmed hardest cases against kept runs on the two
  unseen studies (hard, lane keeping), AI picks v2 against rules, random +
  repeat and Optuna + repeat, median and lowest-to-highest replicate
  (contacts with a car the retiming held still are not counted, problem 31,
  outer.outcome). Every other method and study is in Table I.
- fig_inner_loop: (a) every launch before CUTOFF, kept or not, and every
  failure the diagnose contract handled, healed or stopped; (b) per kind of
  failure, the skill the agent chose and how the run ended.
- fig_failure_types: Claude's triage cause of every failed run, per study
  (figures/cards/triage_causes.json).
- fig_outcome_mix: what every kept run of the method studies contains, in
  exclusive categories in OUTCOMES' order (outer.outcome); the counts are
  written to figures/cards/outcome_mix.json for VALIDITY.md.
- fig_cases: three confirmed hardest cases (CASES), each from above and as
  speed and gap over time, drawn from the rollout logs with case_card's
  helpers.
- table_methods.tex: Table I, from methods.json.

    uv run python research/harness/paper_figures.py
"""

import asyncio
import json
import statistics
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from case_card import _gap, _speed, kept, moment, triage_lines
from compare_proposers import COLORS
from discovery_curve import LABEL, study_curves
from physics import EGO, _footprint, _read, actor_tracks, completed_rollout, nearest_actor
from read_state import ROOT, load_entry, queue_entries

RESEARCH = ROOT / "research"
OUT = RESEARCH / "figures" / "paper"
SINGLE, DOUBLE = 3.5, 7.16
# Launches before this moment are counted: everything finished before the
# repeats queued on 20 Oct. Moved to the freeze (24 Oct) for the final numbers.
CUTOFF = datetime(2026, 10, 20, 13, 30, tzinfo=timezone.utc)
STUDY_NAMES = {
    "pedestrian_ego_speed": "Pedestrian",
    "cut_in_merge": "Car cutting in",
    "lead_vehicle": "Car ahead braking",
    "pedestrian_ego_speed_2hz": "Pedestrian, 2 Hz",
    "cut_in_merge_2hz": "Car cutting in, 2 Hz",
    "lead_vehicle_2hz": "Car ahead braking, 2 Hz",
}
# The discovery figure's panels.
PANEL_NAMES = {
    "car_conflicts_3knobs_2hz": "Hard: rare failures",
    "lane_keeping": "Lane keeping",
}
UNSEEN = ("car_conflicts_3knobs_2hz", "lane_keeping")
TEN_HZ = ("pedestrian_ego_speed", "cut_in_merge", "lead_vehicle")
# Baselines first, then the methods where the AI chooses.
# Fig. 4: the planned comparisons only.
FIG_METHODS = ("rules", "random_confirm", "optuna_confirm", "llm_v2")
TABLE_ORDER = ("rules", "random_confirm", "optuna_confirm", "hybrid", "hybrid_optuna", "llm",
               "llm_v2", "hybrid_v2")
# One confirmed hardest case per study: the policy at fault by both the
# scorer and Claude's triage, and (cut-in, lead) not against a held car.
CASES = (
    ("pedestrian_ego_speed", "pedestrian_ego_speed_llm_r2_013"),
    ("cut_in_merge", "cut_in_merge_hybrid_007"),
    ("lead_vehicle", "lead_vehicle_hybrid_025"),
)
CAUSES = {
    "turned_into_actor": "steered into a road user",
    "left_road": "left the road",
    "actor_hit_ego": "a road user drove into the ego",
    "no_brake_for_lead": "no braking for the car ahead",
    "other": "other",
    "rendering": "rendering fault",
}
OUTCOMES = {
    "counted failure": "policy failure",
    "counted failure, possible render artifact": "policy failure, ego > 3.5 m off the recording",
    "contact begun before the AI drove": "contact begun before the policy drove",
    "contact with a car that stopped dead": "contact with a car that stopped dead",
    "rear-ended by a replayed car": "rear-ended by a replayed car",
    "no contact": "no contact",
}
# Colour-blind-safe (Okabe-Ito) for categories that are not search methods.
PALETTE = ("#D55E00", "#E69F00", "#0072B2", "#56B4E9", "#009E73", "#999999")
STYLE = {
    "font.family": "serif",
    "font.serif": ["STIXGeneral"],
    "mathtext.fontset": "stix",
    "font.size": 8,
    "axes.titlesize": 8,
    "axes.labelsize": 8,
    "xtick.labelsize": 7,
    "ytick.labelsize": 7,
    "legend.fontsize": 7,
    "axes.linewidth": 0.5,
    "xtick.major.width": 0.5,
    "ytick.major.width": 0.5,
    "xtick.major.size": 2.5,
    "ytick.major.size": 2.5,
    "lines.linewidth": 1.0,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "pdf.fonttype": 42,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.02,
}


def save(fig, name: str) -> None:
    fig.savefig(OUT / f"{name}.pdf")
    fig.savefig(OUT / f"{name}.png", dpi=200)
    plt.close(fig)
    print(f"figures/paper/{name}.pdf", flush=True)


def fig_discovery() -> None:
    """The two unseen studies, single column: AI picks v2 (the method named
    before they ran) against the three baselines of the planned comparisons.
    Every other method, and the 10 Hz studies, are in Table I."""
    fig, axes = plt.subplots(1, 2, figsize=(SINGLE, 1.85), sharey=True)
    studies = {study: study_curves(study) for study in UNSEEN}
    for ax, (study, curves) in zip(axes, studies.items()):
        for method in FIG_METHODS:
            grid = np.array(curves[method], dtype=float)
            x = np.arange(1, grid.shape[1] + 1)
            ours = method == "llm_v2"
            ax.fill_between(x, grid.min(axis=0), grid.max(axis=0), color=COLORS[method],
                            alpha=0.15 if ours else 0.08, lw=0, step="post")
            ax.step(x, np.median(grid, axis=0), where="post", color=COLORS[method],
                    lw=1.6 if ours else 0.9, label=LABEL[method], zorder=3 if ours else 2)
        ax.set_title(f"{PANEL_NAMES[study]}", loc="left")
        ax.set_xlabel("kept runs")
        ax.set_ylim(-0.15, 5.3)
        ax.set_xlim(0, x[-1])
        ax.grid(alpha=0.25, lw=0.4)
    axes[0].set_ylabel("hardest cases confirmed")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=2, frameon=False,
               bbox_to_anchor=(0.5, -0.16), handlelength=1.5, columnspacing=1.2)
    reps = min(len(curves["llm_v2"]) for curves in studies.values())
    fig.text(0.5, -0.2, f"line: median of {reps} repeats; band: lowest to highest repeat",
             ha="center", va="bottom", fontsize=6.5, color="0.35")
    fig.tight_layout(w_pad=0.4, rect=(0, 0.06, 1, 1))
    save(fig, "fig_discovery")


def _entries() -> list[tuple[Path, dict]]:
    found = []
    for queue in sorted((RESEARCH / "studies").rglob("queue")):
        if "aborted_" in str(queue):
            continue
        found += [(path, load_entry(path)) for path in queue_entries(queue)]
    return found


def _before_cutoff(path: Path, entry: dict) -> bool:
    """Launched before CUTOFF; an entry never launched, by when it was written."""
    when = entry["launched_at"] or path.stat().st_mtime
    return when < CUTOFF.timestamp()


def failure_kind(status: dict) -> str:
    """The kind of failure a diagnosis saw, as the paper names it."""
    if "CUDA out of memory" in json.dumps(status.get("error_lines", [])):
        return "GPU out of memory"
    head = status["k_status"].split(":")[0]
    return {"wizard_exit_code": "simulator crash, other",
            "environment": "GPU still busy",
            "physics": "impossible motion",
            "process_lost": "launcher lost"}.get(head, head)


def healing(entries: list[tuple[Path, dict]]) -> tuple[Counter, list[dict]]:
    """Launch resolutions and, per diagnosed entry, its failure, the agent's
    skill and how its lineage ended (a retry is a child entry naming its
    parent's file in the same queue)."""
    children = defaultdict(list)
    for path, entry in entries:
        if entry["parent"]:
            children[(path.parent, entry["parent"])].append((path, entry))

    def end(path: Path, entry: dict) -> str | None:
        kids = children.get((path.parent, path.name))
        if not kids:
            return entry["resolution"]
        return end(*max(kids, key=lambda kid: kid[1]["attempt"]))

    mine = [(p, e) for p, e in entries if _before_cutoff(p, e)]
    resolutions = Counter(e["resolution"] for p, e in mine if e["launched_at"] and e["resolution"])
    rows = []
    for path, entry in mine:
        diagnosis = entry["diagnosis"]
        if not diagnosis:
            continue
        final = "HALT" if diagnosis["skill"] == "HALT" else end(path, entry)
        rows.append({"failure": failure_kind(diagnosis["input"]), "skill": diagnosis["skill"],
                     "end": {"ACCEPT": "kept", "HALT": "stopped"}.get(final, "pending")})
    return resolutions, rows


def fig_inner_loop() -> dict:
    resolutions, rows = healing(_entries())
    launches, kept_n = sum(resolutions.values()), resolutions["ACCEPT"]
    ends = Counter(r["end"] for r in rows)
    fig = plt.figure(figsize=(DOUBLE, 2.0))
    grid = fig.add_gridspec(2, 2, width_ratios=[1, 1.35], hspace=1.6, wspace=0.42)
    top, bottom, right = fig.add_subplot(grid[0, 0]), fig.add_subplot(grid[1, 0]), fig.add_subplot(grid[:, 1])

    def bar(ax, parts, total, title):
        left = 0
        for label, n, colour in parts:
            ax.barh(0, n, left=left, color=colour, height=0.6, lw=0)
            left += n
        ax.set_xlim(0, total)
        ax.set_yticks([])
        ax.spines["left"].set_visible(False)
        ax.set_title(title, loc="left")
        ax.legend([plt.Rectangle((0, 0), 1, 1, color=c) for _, _, c in parts],
                  [f"{label} {n:,}" for label, n, _ in parts], loc="upper center",
                  bbox_to_anchor=(0.5, -0.45), ncol=len(parts), frameon=False,
                  handlelength=0.9, columnspacing=1.0)

    bar(top, [("kept", kept_n, PALETTE[4]), ("not kept", launches - kept_n, PALETTE[0])],
        launches, f"(a) {launches:,} finished launches: {100 * kept_n / launches:.1f}% kept")
    bar(bottom, [("healed, then kept", ends["kept"], PALETTE[4]),
                 ("stopped for a person", ends["stopped"], PALETTE[0])]
        + ([("pending", ends["pending"], PALETTE[5])] if ends["pending"] else []),
        len(rows), f"{len(rows)} failures handed to the agent")

    kinds = Counter(r["failure"] for r in rows)
    order = [k for k, _ in kinds.most_common()][::-1]
    for i, kind in enumerate(order):
        mine = [r for r in rows if r["failure"] == kind]
        healed = sum(r["end"] == "kept" for r in mine)
        right.barh(i, healed, color=PALETTE[4], height=0.6, lw=0)
        right.barh(i, len(mine) - healed, left=healed, color=PALETTE[0], height=0.6, lw=0)
        skills = Counter(r["skill"] for r in mine).most_common()
        right.text(len(mine) + 2, i, ", ".join(f"{s} {n}" for s, n in skills),
                   va="center", fontsize=6.5)
    right.set_yticks(range(len(order)), order)
    right.tick_params(axis="y", length=0)
    right.spines["left"].set_visible(False)
    right.set_xlim(0, max(kinds.values()) * 1.5)
    right.set_xlabel("failures (green: healed, then kept; red: stopped)")
    right.set_title("(b) the agent's skill per kind of failure", loc="left")
    save(fig, "fig_inner_loop")
    return {"launches": launches, "kept": kept_n, "diagnosed": len(rows),
            "healed": ends["kept"], "stopped": ends["stopped"], "pending": ends["pending"]}


def _stacked(ax, data: dict, order: dict, studies: list[str], percent: bool) -> None:
    for i, study in enumerate(studies[::-1]):
        counts = data[study]
        total = sum(counts.values())
        left = 0.0
        for j, key in enumerate(order):
            share = counts.get(key, 0) / total * (100 if percent else 1)
            ax.barh(i, share, left=left, color=PALETTE[j], height=0.62, lw=0)
            if share >= 9:
                ax.text(left + share / 2, i, f"{share:.0f}", ha="center", va="center",
                        fontsize=6, color="white")
            left += share
        ax.text(101, i, f"{total:,}", va="center", fontsize=6.5, color="0.3")
    ax.set_yticks(range(len(studies)), [STUDY_NAMES[s] for s in studies[::-1]])
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    ax.set_xlim(0, 100)
    ax.legend([plt.Rectangle((0, 0), 1, 1, color=PALETTE[j]) for j in range(len(order))],
              list(order.values()), loc="upper right", bbox_to_anchor=(1.0, -0.25),
              ncol=2, frameon=False, handlelength=0.9, columnspacing=0.8, fontsize=6.5)


def fig_failure_types() -> None:
    data = json.loads((RESEARCH / "figures" / "cards" / "triage_causes.json").read_text())
    fig, ax = plt.subplots(figsize=(SINGLE - 0.55, 2.3))
    _stacked(ax, data, CAUSES, list(STUDY_NAMES), percent=True)
    ax.set_xlabel("share of failed runs, % (right: failed runs triaged)")
    save(fig, "fig_failure_types")


def outcome_category(run: dict) -> str:
    if run["failed"]:
        return "counted failure, possible render artifact" if run["possible_artifact"] else "counted failure"
    if run["contact_at_handoff"]:
        return "contact begun before the AI drove"
    if run["contact_with_held_actor"]:
        return "contact with a car that stopped dead"
    if run["rear_ended"]:
        return "rear-ended by a replayed car"
    return "no contact"


def fig_outcome_mix() -> None:
    data = {study: dict(Counter(outcome_category(run) for run in kept(study)))
            for study in STUDY_NAMES}
    (RESEARCH / "figures" / "cards" / "outcome_mix.json").write_text(json.dumps(data, indent=1) + "\n")
    fig, ax = plt.subplots(figsize=(SINGLE - 0.55, 2.3))
    _stacked(ax, data, OUTCOMES, list(STUDY_NAMES), percent=True)
    ax.legend_.remove()
    ax.legend([plt.Rectangle((0, 0), 1, 1, color=PALETTE[j]) for j in range(len(OUTCOMES))],
              list(OUTCOMES.values()), loc="upper right", bbox_to_anchor=(1.0, -0.25),
              ncol=1, frameon=False, handlelength=0.9)
    ax.set_xlabel("share of kept runs, % (right: kept runs)")
    save(fig, "fig_outcome_mix")


def _case_panels(bev, speed, gap, study: str, run_name: str) -> dict:
    """One case from its rollout log: from above in the ego's frame at the
    failure (ego driving to the right), and the speeds and the gap over time."""
    run = next(r for r in kept(study) if r["run"] == run_name)
    raw = asyncio.run(_read(completed_rollout(run["run_dir"]) / "rollout.asl"))
    actors = actor_tracks(raw)
    what, when, handoff = moment(run["run_dir"])
    key, when = nearest_actor(raw, actors, when, handoff)
    ego = actors[EGO]
    t0 = min(ego)
    rel = lambda t: (np.asarray(t, dtype=float) - t0) / 1e6
    ex, ey, eyaw = ego[min(ego, key=lambda s: abs(s - when))]
    rot = np.array([[np.cos(-eyaw), -np.sin(-eyaw)], [np.sin(-eyaw), np.cos(-eyaw)]])
    view = lambda xy: (np.asarray(xy, dtype=float).reshape(-1, 2) - (ex, ey)) @ rot.T
    recorded = view([(r[1], r[2]) for r in raw["recorded"]])
    bev.plot(recorded[:, 0], recorded[:, 1], "--", color="#0072B2", lw=0.8)
    for actor_id, track in actors.items():
        times = [t for t in sorted(track) if handoff <= t <= when + 1e6]
        if len(times) < 2:
            continue
        xy = view([track[t][:2] for t in times])
        mine = actor_id in (EGO, key)
        colour = "#D55E00" if actor_id == EGO else "#E69F00" if actor_id == key else "0.7"
        bev.plot(xy[:, 0], xy[:, 1], color=colour, lw=1.4 if mine else 0.6, zorder=4 if mine else 1)
        near = min(track, key=lambda s: abs(s - when))
        if abs(near - when) <= 0.6e6:
            shape = view(np.array(_footprint(*track[near], raw["sizes"][actor_id]).exterior.coords))
            bev.fill(shape[:, 0], shape[:, 1], color=colour if mine else "0.6",
                     alpha=0.9 if mine else 0.5, lw=0, zorder=5 if mine else 2)
    bev.set_xlim(-32, 12)
    bev.set_ylim(-9, 9)
    bev.set_aspect("equal")
    bev.grid(alpha=0.25, lw=0.4)

    t, v = _speed(ego)
    speed.plot(rel(t), v, color="#D55E00", lw=1.0, label="ego")
    t_rec, v_rec = _speed({r[0]: (r[1], r[2], 0.0) for r in raw["recorded"]})
    speed.plot(rel(t_rec), v_rec, "--", color="#0072B2", lw=0.8, label="human, recorded")
    t_key, v_key = _speed(actors[key])
    speed.plot(rel(t_key), v_key, color="#E69F00", lw=1.0, label="the car it met")
    times = sorted(set(ego) & set(actors[key]))
    gaps = _gap(raw, ego, actors[key], key, times)
    gap.plot(rel(times), gaps, color="#E69F00", lw=1.0)
    gap.set_ylim(0, min(30, np.nanmax(gaps) * 1.05))
    for ax in (speed, gap):
        ax.axvline(rel(handoff), color="0.4", ls=":", lw=0.8)
        ax.axvline(rel(when), color="#D55E00", lw=0.8)
        ax.set_xlim(0, min(rel(max(ego)), rel(when) + 1.5))
        ax.grid(alpha=0.25, lw=0.4)
    speed.set_ylim(bottom=0)
    speed.set_ylabel("speed, m/s", labelpad=1)
    gap.set_ylabel("gap, m", labelpad=1)
    gap.set_xlabel("time, s", labelpad=1)
    speed.tick_params(labelbottom=False)
    return {"run": run_name, "setting": run, "what": what, "when_s": float(rel(when)),
            "handoff_s": float(rel(handoff)), "failed": run["failed"],
            "key_actor": key}


def fig_cases() -> list[dict]:
    fig = plt.figure(figsize=(DOUBLE, 2.9))
    grid = fig.add_gridspec(3, 3, height_ratios=[1.15, 0.75, 0.75], hspace=0.25, wspace=0.32)
    shown = []
    for i, (study, run_name) in enumerate(CASES):
        triage = triage_lines(study)[run_name]
        failed = next(r for r in kept(study) if r["run"] == run_name)["failed"]
        if triage["policy_at_fault"] != "yes" or not failed:
            raise SystemExit(f"{run_name}: triage {triage['policy_at_fault']}, counted {failed}")
        bev, speed = fig.add_subplot(grid[0, i]), fig.add_subplot(grid[1, i])
        gap = fig.add_subplot(grid[2, i], sharex=speed)
        found = _case_panels(bev, speed, gap, study, run_name)
        run = found.pop("setting")
        knobs = ", ".join(f"{label} {run[k]:g}x" for k, label in
                          (("ego_speed_scale", "ego speed"), ("actor_speed_scale", "car speed"))
                          if k in run and run[k] != 1.0)
        bev.set_title(f"({'abc'[i]}) {STUDY_NAMES[study]} study" + (f", {knobs}" if knobs else ""),
                      loc="left")
        shown.append({**found, "study": study, "cause": triage["cause"]})
    handles, labels = speed.get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=3, frameon=False,
               bbox_to_anchor=(0.5, -0.06), handlelength=1.5)
    fig.text(0.5, -0.14, "Top: from above at the failure, in metres, ego (red) driving to the right, "
             "the car it met orange, others grey, the human's recorded path dashed;\nlines from "
             "the hand-off on. Below, to 1.5 s after the failure: dotted, the policy takes over; "
             "solid, the failure.",
             ha="center", fontsize=6.5, color="0.3")
    save(fig, "fig_cases")
    return shown


def _runs_to_goal(row: dict) -> str:
    if not row["reached"]:
        return "never"
    reached = sorted(r for r, c in zip(row["runs_to_goal"], row["confirmed"]) if c >= 5)
    span = f"{reached[0]}" if reached[0] == reached[-1] else f"{reached[0]}--{reached[-1]}"
    if row["reached"] < row["replicates"]:
        return f"{row['reached']} of {row['replicates']} reached, {span}"
    return f"{row['median_runs_to_goal']:g} ({span})"


def _confirmed(*rows: dict) -> str:
    return f"{sum(sum(r['confirmed']) for r in rows)}/{sum(5 * r['replicates'] for r in rows)}"


def table_methods() -> str:
    methods = json.loads((RESEARCH / "methods.json").read_text())
    hard, lane, ped, cut, lead = (methods[s]["proposers"] for s in UNSEEN + TEN_HZ)
    lines = [
        r"\begin{table}[t]",
        r"\caption{Search methods at an equal budget per study.}",
        r"\label{tab:methods}",
        r"\centering\footnotesize",
        r"\setlength{\tabcolsep}{2.5pt}",
        r"\begin{tabular}{@{}lccccc@{}}",
        r"\toprule",
        r" & \multicolumn{2}{c}{Unseen studies, 2\,Hz} & \multicolumn{2}{c}{Method studies, 10\,Hz} & \\",
        r"\cmidrule(lr){2-3}\cmidrule(lr){4-5}",
        r" & Hard & Lane keeping & Car scenes & Pedestrian & Model \\",
        r"Method & confirmed & runs to goal & confirmed & runs to goal & s/arm \\",
        r"\midrule",
    ]
    for m in TABLE_ORDER:
        rows = [s[m] for s in (hard, lane, ped, cut, lead) if m in s]
        seconds = statistics.median(x for r in rows for x in r["model_seconds"])
        ten_hz = m in cut and m in lead
        lines.append(
            f"{LABEL[m]} & {_confirmed(hard[m])} & {_runs_to_goal(lane[m])} & "
            f"{_confirmed(cut[m], lead[m]) if ten_hz else '--'} & "
            f"{_runs_to_goal(ped[m]) if m in ped else '--'} & "
            f"{f'{seconds:.0f}' if seconds else '--'} \\\\")
    reps = sorted({hard[m]["replicates"] for m in TABLE_ORDER} | {lane[m]["replicates"] for m in TABLE_ORDER})
    lines += [
        r"\bottomrule",
        r"\end{tabular}",
        r"\\[2pt]\parbox{\columnwidth}{\scriptsize Confirmed: hardest settings confirmed by "
        r"repeats, summed over repeats (5 per repeat). Runs to goal: kept runs until all 5 were "
        r"confirmed, median (range); `never' if no repeat got there. Hard: cut-in and car ahead, "
        r"three knobs, rare failures. Car scenes: car cutting in and car ahead braking. "
        f"Repeats per arm: unseen studies {'--'.join(map(str, (reps[0], reps[-1])))}, "
        r"10\,Hz studies 3. Contacts with a car the retiming held still are not counted. "
        r"Model: median seconds of model calls per arm.}",
        r"\end{table}",
    ]
    text = "\n".join(lines) + "\n"
    (OUT / "table_methods.tex").write_text(text)
    print("figures/paper/table_methods.tex", flush=True)
    return text


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update(STYLE)
    fig_discovery()
    loop = fig_inner_loop()
    fig_failure_types()
    fig_outcome_mix()
    cases = fig_cases()
    table_methods()
    (OUT / "numbers.json").write_text(json.dumps(
        {"cutoff": CUTOFF.isoformat(), "inner_loop": loop, "cases": cases}, indent=1, default=str) + "\n")
    print(json.dumps(loop))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
