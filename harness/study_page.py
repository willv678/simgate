"""A study as one web page, for someone seeing it for the first time.

Reads a study folder (brief.md, plan.json, report.json, triage.json and, when
the study had a goal, goal.json) and the study's queue, and writes
<study folder>/index.html with a frames/ folder beside it: one small PNG per
triaged failure, taken from the run's camera video at the failure moment.

The page has the question, the answer, a chart of the failure rate against
the varied knob for each scene (inline SVG, 90% ranges from report.json),
the findings with the settings they cite, why each failed run failed, every
run, and where the numbers came from. Counts and ranges are the ones code
computed (outer.results, outer.history); the page adds no numbers of its own.

    uv run python research/harness/study_page.py research/studies/confirm_break_02eadd92
    uv run python research/harness/study_page.py research/studies/pilot_o1 \
        --queue research/harness/o1_queue
"""

import argparse
import json
import subprocess
import sys
from collections import Counter
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from outer import FAR_FROM_RECORDING_M, history
from read_state import ROOT, load_entry, queue_entries

from physics import completed_rollout

THUMB_WIDTH_PX = 480
# Each knob in words: its name, what it means, and how to show a value.
KNOBS = {
    "planner_delay_us": {
        "name": "planner delay",
        "meaning": "time from a camera frame to the car's controller receiving "
        "the plan made from it",
        "scale": 1e-3,
        "unit": "ms",
    },
    "lateral_bias_m": {
        "name": "sideways shift of the plan",
        "meaning": "the plan moved sideways, left positive, as from a "
        "perception or localisation error",
        "scale": 1,
        "unit": "m",
    },
    "waypoint_noise_std": {
        "name": "plan jitter",
        "meaning": "random jitter added to each planned point (standard "
        "deviation), as from noisy perception",
        "scale": 1,
        "unit": "m",
    },
}
CAUSES = {
    "no_brake_for_lead": "Did not brake enough for the car ahead",
    "turned_into_actor": "Steered into another road user",
    "left_road": "Left the road",
    "actor_hit_ego": "Another road user hit the test car",
    "rendering": "Simulator picture problem",
    "other": "Other",
}
AT_FAULT = {
    "yes": "Driving policy at fault",
    "no": "Driving policy not at fault",
    "unclear": "Unclear who was at fault",
}
FAILURE_KINDS = {
    "collision_front": "front collision",
    "collision_lateral": "side collision",
    "offroad": "left the road",
}
# Chart geometry in SVG user units.
LEFT, RIGHT, TOP, PLOT_H, SLOT_W = 46, 12, 14, 150, 66
SQUARE, SQUARE_GAP, SQUARES_PER_ROW = 8, 3, 6


def knob_text(knob: str, value) -> str:
    spec = KNOBS[knob]
    return f"{value * spec['scale']:g} {spec['unit']}"


def setting_text(row: dict, varied: tuple) -> str:
    return ", ".join(f"{KNOBS[k]['name']} {knob_text(k, row[k])}" for k in varied)


def scene_short(scene_id: str) -> str:
    """The part of a scene id people quote: clipgt-02eadd92-... -> 02eadd92."""
    return scene_id[7:15]


def percent(rate: float) -> str:
    return f"{rate:.0%}"


def runs_text(row: dict) -> str:
    return f"{row['failed']} of {row['runs']} run" + ("s" * (row["runs"] != 1))


def evidence_line(row: dict, varied: tuple) -> str:
    """One setting of the results table in words, as HTML."""
    low, high = row["failure_rate_90"]
    flagged = (
        f"; {row['possible_artifacts']} possibly the simulator's"
        if row["possible_artifacts"]
        else ""
    )
    return (
        f"<b>{row['id']}</b> · scene {scene_short(row['scene_id'])}, "
        f"{escape(setting_text(row, varied))}: "
        f"{runs_text(row)} failed; failure rate "
        f"{percent(low)}–{percent(high)} (90% range){flagged} "
        f"<span class=muted>· {escape(', '.join(row['run_names']))}</span>"
    )


def chart_svg(rows: list[dict], varied: tuple, outcomes: dict[str, bool]) -> str:
    """One SVG panel per scene: for each setting, the 90% range of the failure
    rate as a bar, the observed rate as a dot, and one square per kept run
    below the axis (orange failed, blue passed). `outcomes` maps a run name
    to whether it failed. Settings share one x axis across panels."""
    slots = sorted({tuple(row[k] for k in varied) for row in rows})
    most_runs = max(row["runs"] for row in rows)
    square_rows = -(-most_runs // SQUARES_PER_ROW)
    width = LEFT + len(slots) * SLOT_W + RIGHT
    axis_y = TOP + PLOT_H
    height = axis_y + 26 + square_rows * (SQUARE + SQUARE_GAP) + 20

    def y(rate: float) -> float:
        return TOP + (1 - rate) * PLOT_H

    panels = []
    for scene in dict.fromkeys(row["scene_id"] for row in rows):
        parts = []
        for rate in (0, 0.5, 1):
            parts.append(
                f"<line class=grid x1={LEFT} x2={width - RIGHT} "
                f"y1={y(rate):.1f} y2={y(rate):.1f} />"
                f"<text class=tick x={LEFT - 8} y={y(rate) + 4:.1f} "
                f"text-anchor=end>{percent(rate)}</text>"
            )
        for index, slot in enumerate(slots):
            cx = LEFT + (index + 0.5) * SLOT_W
            label = ", ".join(knob_text(k, v) for k, v in zip(varied, slot))
            parts.append(
                f"<text class=tick x={cx:.1f} y={axis_y + 18} "
                f"text-anchor=middle>{escape(label)}</text>"
            )
        parts.append(
            f"<line class=axis x1={LEFT} x2={width - RIGHT} y1={axis_y} y2={axis_y} />"
        )
        for row in rows:
            if row["scene_id"] != scene:
                continue
            cx = LEFT + (slots.index(tuple(row[k] for k in varied)) + 0.5) * SLOT_W
            low, high = row["failure_rate_90"]
            rate = row["failed"] / row["runs"]
            tip = (
                f"{row['id']}: {setting_text(row, varied)}. {runs_text(row)} "
                f"failed; failure rate {percent(low)} to "
                f"{percent(high)} (90% range)"
                + (
                    f"; {row['possible_artifacts']} possibly the simulator's"
                    if row["possible_artifacts"]
                    else ""
                )
            )
            squares = []
            for i, run in enumerate(row["run_names"]):
                sx = (
                    cx
                    - (
                        min(row["runs"], SQUARES_PER_ROW) * (SQUARE + SQUARE_GAP)
                        - SQUARE_GAP
                    )
                    / 2
                    + (i % SQUARES_PER_ROW) * (SQUARE + SQUARE_GAP)
                )
                sy = axis_y + 28 + (i // SQUARES_PER_ROW) * (SQUARE + SQUARE_GAP)
                kind = "fail" if outcomes[run] else "pass"
                squares.append(
                    f'<rect class="run {kind}" x={sx:.1f} y={sy:.1f} '
                    f"width={SQUARE} height={SQUARE} rx=2 />"
                )
            parts.append(
                f"<g class=setting><title>{escape(tip)}</title>"
                f"<rect class=hit x={cx - SLOT_W / 2:.1f} y={TOP - 6} "
                f"width={SLOT_W} height={height - TOP} />"
                f"<rect class=range x={cx - 6:.1f} y={y(high):.1f} width=12 "
                f"height={max(y(low) - y(high), 4):.1f} rx=4 />"
                f"<circle class=rate cx={cx:.1f} cy={y(rate):.1f} r=6 />"
                f"<text class=id x={cx + 12:.1f} y={y(rate) + 4:.1f}>"
                f"{row['id']}</text>" + "".join(squares) + "</g>"
            )
        panels.append(
            f"<figure class=panel><figcaption>Scene {scene_short(scene)}"
            f"</figcaption>"
            f'<svg viewBox="0 0 {width} {height}" style="max-width:{width}px" '
            f'role=img aria-label="Failure rate by setting on scene '
            f'{scene_short(scene)}">' + "".join(parts) + "</svg></figure>"
        )
    return "".join(panels)


def thumbnail(run_dir: Path, at_s: float, path: Path) -> None:
    """The camera frame at `at_s` seconds into the run's video, scaled down."""
    video = next(completed_rollout(run_dir).glob("*.mp4"))
    subprocess.run(
        [
            "ffmpeg",
            "-v",
            "error",
            "-y",
            "-ss",
            f"{at_s}",
            "-i",
            str(video),
            "-frames:v",
            "1",
            "-vf",
            f"scale={THUMB_WIDTH_PX}:-2",
            str(path),
        ],
        check=True,
    )


def failure_kind(row: dict) -> str:
    return ", ".join(text for key, text in FAILURE_KINDS.items() if row[key])


def goal_html(goal: dict | None) -> str:
    if goal is None:
        return (
            "<p class=goal>No goal that code can check was set, so the study "
            "ran its whole budget.</p>"
        )
    scenes = "".join(
        f"<li>Scene {scene_short(scene)}: {escape(text)}</li>"
        for scene, text in goal.get("scenes", {}).items()
    )
    return (
        f"<p class=goal><b>Goal, checked by code (not by the model):</b> "
        f"{escape(goal['verdict'])}, after {goal['after_rounds']} rounds.</p>"
        + (f"<ul>{scenes}</ul>" if scenes else "")
    )


def triage_html(causes: list[dict], by_run: dict, varied: tuple) -> str:
    if not causes:
        return "<p>No kept run failed, so there was nothing to explain.</p>"
    counts = Counter(c["cause"] for c in causes)
    summary = "; ".join(
        f"{CAUSES[cause].lower()}: {n}" for cause, n in counts.most_common()
    )
    cards = []
    for cause in causes:
        row = by_run[cause["run"]]
        where = (
            f"Failed at {row['failed_at_s']} s ({failure_kind(row)}), "
            f"{row['off_recording_at_failure_m']} m from the recorded drive"
            + (
                " — far enough that the picture may be unreliable"
                if row["possible_artifact"]
                else ""
            )
            + "."
        )
        fault = "fail" if cause["policy_at_fault"] == "yes" else "neutral"
        cards.append(
            f"<article class=case>"
            f'<a href="frames/{escape(cause["run"])}.png">'
            f'<img src="frames/{escape(cause["run"])}.png" loading=lazy '
            f'width={THUMB_WIDTH_PX} alt="Front camera of run '
            f"{escape(cause['run'])} at {row['failed_at_s']} s, the moment it "
            f'failed"></a>'
            f"<div><h3>{escape(cause['run'])}</h3>"
            f"<p class=muted>Scene {scene_short(row['scene_id'])}, "
            f"{escape(setting_text(row, varied))}</p>"
            f"<p><span class=tag>{escape(CAUSES[cause['cause']])}</span> "
            f'<span class="tag {fault}">'
            f"{escape(AT_FAULT[cause['policy_at_fault']])}</span></p>"
            f"<p>{escape(cause['what_happened'])}</p>"
            f"<p class=muted>{escape(where)}</p></div></article>"
        )
    return (
        "<p>For each failed run, Claude looked at the camera frames just "
        "before and at the failure, and at the speed and the gap to the car "
        "ahead, and named a cause from a fixed list. The picture is the "
        f"front camera at the failure moment.</p><p><b>Causes:</b> "
        f"{escape(summary)}.</p>" + "".join(cards)
    )


def runs_html(rows: list[dict], varied: tuple) -> str:
    head = "".join(f"<th>{escape(KNOBS[k]['name'])}</th>" for k in varied)
    body = []
    for row in rows:
        knobs = "".join(f"<td>{knob_text(k, row[k])}</td>" for k in varied)
        if row["verdict"] != "kept":
            kept = f"No: {escape(row['verdict'].split(': ', 1)[-1])}"
            result = when = off = "<td></td>"
        else:
            kept = "Yes"
            if row["failed"]:
                result = (
                    f'<td><span class="tag fail">Failed</span> '
                    f"{escape(failure_kind(row))}</td>"
                )
                when = f"<td>{row['failed_at_s']} s</td>"
                flag = (
                    " <span class=muted>(possibly the simulator's)</span>"
                    if row["possible_artifact"]
                    else ""
                )
                off = f"<td>{row['off_recording_at_failure_m']} m{flag}</td>"
            else:
                result = '<td><span class="tag pass">Passed</span></td>'
                when = off = "<td></td>"
        body.append(
            f"<tr><td class=run>{escape(row['run'])}</td>"
            f"<td>{scene_short(row['scene_id'])}</td>{knobs}"
            f"<td>{kept}</td>{result}{when}{off}</tr>"
        )
    return (
        "<div class=scroll><table><thead><tr><th>Run</th><th>Scene</th>"
        f"{head}<th>Kept</th><th>Result</th><th>Failed at</th>"
        "<th>Off the recorded drive at failure</th></tr></thead>"
        f"<tbody>{''.join(body)}</tbody></table></div>"
    )


def settings_table(table: list[dict], varied: tuple) -> str:
    head = "".join(f"<th>{escape(KNOBS[k]['name'])}</th>" for k in varied)
    body = "".join(
        f"<tr><td>{r['id']}</td><td>{scene_short(r['scene_id'])}</td>"
        + "".join(f"<td>{knob_text(k, r[k])}</td>" for k in varied)
        + f"<td>{r['failed']} of {r['runs']}</td>"
        f"<td>{percent(r['failure_rate_90'][0])}–"
        f"{percent(r['failure_rate_90'][1])}</td>"
        f"<td>{r['possible_artifacts'] or ''}</td></tr>"
        for r in table
    )
    return (
        "<details><summary>The chart as a table</summary><div class=scroll>"
        f"<table><thead><tr><th>Setting</th><th>Scene</th>{head}"
        "<th>Failed</th><th>Failure rate (90% range)</th>"
        "<th>Possibly the simulator's</th></tr></thead>"
        f"<tbody>{body}</tbody></table></div></details>"
    )


def provenance_html(
    plan_file: dict,
    report: dict,
    causes: list[dict],
    rounds: list[dict],
    rows: list[dict],
) -> str:
    plan = plan_file["plan"]
    kept = [row for row in rows if row["verdict"] == "kept"]
    who = [
        (
            f"The plan was written by {plan_file['call']['model']} from the brief "
            "and checked by code against the knob catalog and the run budget."
            if plan_file["call"]
            else "The plan was fixed by a script, not written by a model."
        )
    ]
    if rounds:
        proposers = sorted({r["proposer"] for r in rounds})
        models = sorted({r["call"]["model"] for r in rounds if r["call"]})
        who.append(
            f"The runs were chosen in {len(rounds)} rounds by "
            f"{', '.join(proposers)}"
            + (f" ({', '.join(models)})" if models else "")
            + "; code rejected any choice outside the plan before it ran."
        )
    if causes:
        who.append(f"Failures were explained by {causes[0]['call']['model']}.")
    who.append(f"The answer and findings were written by {report['call']['model']}.")
    return (
        f"<p>{' '.join(escape(line) for line in who)}</p>"
        f"<p><b>Runs:</b> {len(rows)} in the study, {len(kept)} kept, "
        f"{len(rows) - len(kept)} not kept; {sum(r['failed'] for r in kept)} "
        f"of the kept runs failed.</p>"
        "<p><b>How the numbers were computed:</b> a run counts only if it "
        "passed every automatic check of the simulator (it is <i>kept</i>). A "
        "run failed if the test car hit something with its front or side, or "
        "left the road. For each setting, code counts the kept runs that failed "
        "and gives the 90% Wilson range of the failure rate. A failure is "
        "flagged as possibly the simulator's when the test car was more than "
        f"{FAR_FROM_RECORDING_M:g} m (about a lane) from the recorded drive, or "
        "a camera frame was black, because there the rebuilt scene is drawn "
        "less reliably. The model wrote the words; every count and range on "
        "this page is computed from the run records, not written by the model.</p>"
        "<details><summary>Why the plan looks the way it does</summary>"
        f"<p class=pre>{escape(plan['rationale'])}</p></details>"
    )


def page(folder: Path, queue: Path) -> tuple[str, list[tuple[str, Path, float]]]:
    """The page's HTML, and the thumbnails it refers to as (run, run dir,
    failure time)."""
    plan_file = json.loads((folder / "plan.json").read_text(encoding="utf-8"))
    plan = plan_file["plan"]
    varied = tuple(plan["vary"])
    report = json.loads((folder / "report.json").read_text(encoding="utf-8"))
    triage_file = folder / "triage.json"
    causes = (
        json.loads(triage_file.read_text(encoding="utf-8"))
        if triage_file.exists()
        else []
    )
    goal_file = folder / "goal.json"
    goal = (
        json.loads(goal_file.read_text(encoding="utf-8"))
        if goal_file.exists()
        else None
    )
    rounds_file = (
        queue.parent / f"{queue.name.removesuffix('_queue')}_rounds.jsonl"
        if queue.name.endswith("_queue")
        else queue.parent / "rounds.jsonl"
    )
    rounds = (
        [json.loads(line) for line in rounds_file.read_text().splitlines()]
        if rounds_file.exists()
        else []
    )
    brief = (folder / "brief.md").read_text(encoding="utf-8")

    rows = history(queue, varied)
    by_run = {row["run"]: row for row in rows}
    dirs = {
        load_entry(p)["name"]: ROOT / load_entry(p)["run_dir"]
        for p in queue_entries(queue)
    }
    thumbs = [
        (c["run"], dirs[c["run"]], by_run[c["run"]]["failed_at_s"]) for c in causes
    ]
    table = report["results"]
    answer = report["answer"]
    by_id = {row["id"]: row for row in table}
    outcomes = {row["run"]: row["failed"] for row in rows if row["verdict"] == "kept"}

    findings = "".join(
        f"<li><p>{escape(f['claim'])}</p><ul class=evidence>"
        + "".join(f"<li>{evidence_line(by_id[s], varied)}</li>" for s in f["settings"])
        + "</ul></li>"
        for f in answer["findings"]
    )
    still_open = "".join(f"<li>{escape(item)}</li>" for item in answer["open"])
    knobs_read = "; ".join(
        f"<b>{escape(KNOBS[k]['name'])}</b>: {escape(KNOBS[k]['meaning'])}"
        for k in varied
    )
    scenes = sorted({row["scene_id"] for row in table})
    title = f"Study {folder.name}"
    body = f"""
<header>
<p class=eyebrow>SimGate study · {escape(folder.name)}</p>
<h1>{escape(plan["question"])}</h1>
<p class=muted>{len(rows)} simulated drives on {len(scenes)} scene(s) rebuilt from
real recordings, varying {escape(", ".join(KNOBS[k]["name"] for k in varied))}.</p>
<details class=terms><summary>What the words on this page mean</summary><ul>
<li><b>Run</b>: one simulated drive of a scene by the driving policy under test.</li>
<li><b>Scene</b>: a few seconds of a real recorded drive, rebuilt so the policy can
drive it again; named by the first characters of its id.</li>
<li><b>Test car</b> (the "ego"): the car the policy drives. The other road users
replay what they did in the recording.</li>
<li><b>Recorded drive</b>: the path the human driver took in the recording.</li>
<li><b>Kept</b>: the run passed every automatic check that the simulator ran it
as asked. Only kept runs count as evidence.</li>
<li><b>Failed</b>: the test car hit something with its front or side, or left the
road.</li>
<li><b>Setting</b>: one scene at one knob value, numbered S1, S2, … so the
findings can cite it.</li>
<li><b>90% range</b>: the failure rates that fit what was seen, at 90% confidence.
Few runs give a wide range.</li>
</ul></details>
</header>

<section id=question><h2>1. The question</h2>
<p>{escape(plan["question"])}</p>
<p><b>What was varied:</b> {knobs_read}.</p>
<details><summary>The researcher's brief, as written</summary>
<p class=pre>{escape(brief)}</p></details>
</section>

<section id=answer><h2>2. The answer</h2>
<p class=answer>{escape(answer["answer"])}</p>
{goal_html(goal)}
</section>

<section id=chart><h2>3. Failure rate by setting</h2>
<p class=how>How to read it: each dot is the share of runs that failed at that
setting, the <span class=swatch-range></span> bar is its 90% range, and each
square below the axis is one run (<span class="key fail">orange</span> failed,
<span class="key pass">blue</span> passed). Hover a setting for its numbers.</p>
{chart_svg(table, varied, outcomes)}
{settings_table(table, varied)}
</section>

<section id=findings><h2>4. Findings</h2>
<p class=muted>Each finding is the model's reading; the lines under it are the
counts code computed for the settings it cites.</p>
<ol class=findings>{findings}</ol>
<h3>Still open</h3><ul>{still_open}</ul>
</section>

<section id=why><h2>5. Why the runs failed</h2>
{triage_html(causes, by_run, varied)}
</section>

<section id=runs><h2>6. Every run</h2>
{runs_html(rows, varied)}
</section>

<section id=provenance><h2>7. Where this came from</h2>
{provenance_html(plan_file, report, causes, rounds, rows)}
</section>
"""
    html = (
        "<!doctype html><html lang=en><head><meta charset=utf-8>"
        '<meta name=viewport content="width=device-width, initial-scale=1">'
        f"<title>{escape(title)}</title><style>{STYLE}</style></head>"
        f"<body><main>{body}</main></body></html>\n"
    )
    return html, thumbs


STYLE = """
:root {
  color-scheme: light;
  --surface: #fcfcfb; --raised: #f3f2ef; --ink: #0b0b0b; --ink-2: #52514e;
  --line: #dcdad4; --pass: #2a78d6; --fail: #eb6834; --fail-ink: #b0400f;
  --pass-ink: #1d5aa6;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    color-scheme: dark;
    --surface: #1a1a19; --raised: #252523; --ink: #ffffff; --ink-2: #c3c2b7;
    --line: #3a3936; --pass: #3987e5; --fail: #d95926; --fail-ink: #f2986f;
    --pass-ink: #8db8f0;
  }
}
:root[data-theme="dark"] {
  color-scheme: dark;
  --surface: #1a1a19; --raised: #252523; --ink: #ffffff; --ink-2: #c3c2b7;
  --line: #3a3936; --pass: #3987e5; --fail: #d95926; --fail-ink: #f2986f;
  --pass-ink: #8db8f0;
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--surface); color: var(--ink);
  font: 16px/1.55 system-ui, -apple-system, "Segoe UI", Roboto, Helvetica,
  Arial, sans-serif; }
main { max-width: 960px; margin: 0 auto; padding: 24px 16px 64px; }
h1 { font-size: 1.6rem; line-height: 1.25; margin: 0.2em 0 0.4em; }
h2 { font-size: 1.25rem; margin: 2.2em 0 0.6em; padding-top: 0.6em;
  border-top: 1px solid var(--line); }
h3 { font-size: 1rem; margin: 1.2em 0 0.3em; }
p, li { overflow-wrap: anywhere; }
.eyebrow, .muted, .how { color: var(--ink-2); }
.eyebrow { font-size: 0.85rem; margin: 0; }
.pre { white-space: pre-wrap; }
details { margin: 0.8em 0; }
summary { cursor: pointer; color: var(--pass-ink); }
.terms ul { padding-left: 1.2em; }
.answer { font-size: 1.1rem; }
.goal { background: var(--raised); padding: 10px 14px; border-radius: 6px; }
.panel { margin: 1em 0 0.5em; }
.panel figcaption { font-weight: 600; }
.panel svg { width: 100%; height: auto; display: block; }
svg text { font: 13px system-ui, -apple-system, "Segoe UI", sans-serif; }
svg .tick { fill: var(--ink-2); }
svg .id { fill: var(--ink-2); font-size: 12px; }
svg .grid { stroke: var(--line); stroke-width: 1; }
svg .axis { stroke: var(--ink-2); stroke-width: 1; }
svg .range { fill: var(--fail); fill-opacity: 0.3; }
svg .rate { fill: var(--fail); stroke: var(--surface); stroke-width: 2; }
svg .run.fail { fill: var(--fail); }
svg .run.pass { fill: var(--pass); }
svg .hit { fill: transparent; }
svg .setting:hover .hit { fill: var(--raised); }
.swatch-range { display: inline-block; width: 8px; height: 1em;
  vertical-align: -0.15em; border-radius: 3px; background: var(--fail);
  opacity: 0.35; }
.key { font-weight: 600; }
.key.fail { color: var(--fail-ink); }
.key.pass { color: var(--pass-ink); }
.findings > li { margin-bottom: 1em; }
.findings p { margin: 0 0 0.3em; }
.evidence { font-size: 0.9rem; padding-left: 1.1em; }
.case { display: grid; grid-template-columns: 240px 1fr; gap: 16px;
  padding: 14px 0; border-bottom: 1px solid var(--line); }
.case img { width: 100%; height: auto; border-radius: 4px; }
.case h3 { margin-top: 0; }
.case p { margin: 0.3em 0; }
@media (max-width: 600px) { .case { grid-template-columns: 1fr; } }
.tag { display: inline-block; font-size: 0.85rem; padding: 1px 8px;
  border-radius: 10px; border: 1px solid var(--line); background: var(--raised); }
.tag.fail { border-color: var(--fail); color: var(--fail-ink); }
.tag.pass { border-color: var(--pass); color: var(--pass-ink); }
.scroll { overflow-x: auto; }
table { border-collapse: collapse; width: 100%; font-size: 0.88rem; }
th, td { text-align: left; padding: 6px 8px; border-bottom: 1px solid var(--line);
  vertical-align: top; }
th { color: var(--ink-2); font-weight: 600; }
td.run { overflow-wrap: anywhere; min-width: 7em; }
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", type=Path, help="the study folder")
    parser.add_argument("--queue", type=Path, help="default: <folder>/queue")
    args = parser.parse_args()
    html, thumbs = page(args.folder, args.queue or args.folder / "queue")
    frames = args.folder / "frames"
    frames.mkdir(exist_ok=True)
    for run, run_dir, at_s in thumbs:
        thumbnail(run_dir, at_s, frames / f"{run}.png")
    path = args.folder / "index.html"
    path.write_text(html, encoding="utf-8")
    print(f"{path} ({len(html) // 1024} KB, {len(thumbs)} frames)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
