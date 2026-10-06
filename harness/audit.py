"""Tier 2: audit a finished batch for runs no per-run rule caught.

The auditor is one headless `claude -p` call with advisor/AUDIT.md as its whole
system prompt and Read, Grep and Glob confined to a snapshot of the batch.
The snapshot holds the text a researcher would read for each run, under a
random id, with the run's real name and path replaced by that id so neither
gives the answer away. The answer is a list of flags; the schema only admits
run ids that are in the batch. A flag quarantines a run for a person. Nothing
is deleted or changed. The auditor also proposes rules (rules.py) that would
catch each kind of problem without it; promote.py decides which enter the gate.

    uv run python research/harness/audit.py <queue_dir> [--reference <entry.json>]

As a script it audits the runs a queue kept next to one known-good reference
run, marks flagged entries `quarantine`, and checks each proposed rule with
promote.admission. It never enacts a rule. Writes <queue_dir>/audit.json.
"""

import argparse
import json
import random
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

from promote import admission, clean_corpus
from read_state import ROOT, load_entry, queue_entries, save_entry
from rules import FILES, OPS

from physics import features, signals

HARNESS = Path(__file__).resolve().parent
CONTRACT = HARNESS / "advisor" / "AUDIT.md"
# A kept B2 run, not in the clean corpus; the evaluations use it as their one
# reference. Batch F showed one reference run lets the auditor see a batch that
# is wrong the same way throughout.
REFERENCE = HARNESS / "b2_queue" / "091_b2_091.json"
# Kept clean runs to draw references from: B2 on one scene, S1 on 99.
REFERENCE_QUEUES = ("b2_queue", "s1_queue")
PROMPT = (
    "Audit the batch in this directory: batch.json and runs/. "
    "Return the runs to quarantine, or none."
)
COPIED = ("driver-config.yaml", "wizard-config.yaml", "crash_error.log")
METRICS = (
    "collision_at_fault",
    "collision_rear",
    "dist_traveled_m",
    "tracking_error",
    "plan_deviation",
)
SKIPPED_DIRS = ("prometheus", "txt-logs")


def aggregate_metrics(run_path: Path) -> dict[str, float] | None:
    """The metrics a results row records, or None when the run wrote none."""
    if not any(run_path.rglob("metrics.parquet")):
        return None
    table = run_path / "aggregate" / "metrics_results.txt"
    if not table.is_file():
        return None
    text = table.read_text(errors="replace")
    found = {}
    for name in METRICS:
        match = re.search(rf"│\s*{name}\s+│\s+([0-9.]+|inf)", text)
        if match:
            found[name] = float(match.group(1))
    return found


def anonymize(names: list[str], seed: int) -> dict[str, str]:
    order = list(names)
    random.Random(seed).shuffle(order)
    return {name: f"r{index:02d}" for index, name in enumerate(order, start=1)}


def _scrub(text: str, run_path: Path, run_id: str) -> str:
    text = text.replace(str(run_path), f"/runs/{run_id}")
    return re.sub(rf"\b{re.escape(run_path.name)}\b", run_id, text)


def motion_text(run_path: Path) -> str:
    """The ego's motion for the auditor: physics features and a 0.5 s profile."""
    try:
        s = signals(run_path)
    except FileNotFoundError as exc:
        return f"no completed rollout: {exc}\n"
    found = features(s, collided=False)
    del found["contact_without_collision"]
    found["p99_abs_jerk"] = float(np.percentile(np.abs(s["jerk"]), 99))
    lines = ["# physics features (from the rollout log, not the configs)"]
    lines += [f"{key}: {value:.3f}" for key, value in found.items()]
    lines.append("")
    lines.append(
        "# profile every 0.5 s: t_s speed_mps accel_mps2 yaw_rate_rps "
        "reported_speed_mps off_recording_m lead_gap_m"
    )
    t0 = s["times_us"][0]
    for i in range(0, len(s["accel"]), 5):
        lines.append(
            f"{(s['times_us'][i + 1] - t0) / 1e6:.1f} {s['speed'][i]:.2f} "
            f"{s['accel'][i]:.2f} {s['yaw_rate'][i]:.3f} {s['reported_speed'][i]:.2f} "
            f"{s['off_recording_m'][i + 1]:.3f} {s['lead_gap_m'][i + 1]:.1f}"
        )
    return "\n".join(lines) + "\n"


def snapshot(
    runs: dict[str, Path],
    ids: dict[str, str],
    out: Path,
    configs: bool = True,
    motion: bool = True,
) -> None:
    for name, run_path in runs.items():
        run_id = ids[name]
        target = out / "runs" / run_id
        target.mkdir(parents=True)
        files = sorted(
            str(path.relative_to(run_path))
            for path in run_path.rglob("*")
            if path.is_file()
            and not path.relative_to(run_path).parts[0] in SKIPPED_DIRS
        )
        (target / "files.txt").write_text(
            _scrub("\n".join(files) + "\n", run_path, run_id)
        )
        if motion:
            (target / "physics.txt").write_text(motion_text(run_path))
        for filename in COPIED:
            source = run_path / filename
            if not configs and filename.endswith("-config.yaml"):
                continue
            if source.is_file():
                (target / filename).write_text(
                    _scrub(source.read_text(errors="replace"), run_path, run_id)
                )
        table = run_path / "aggregate" / "metrics_results.txt"
        if table.is_file():
            (target / "metrics_results.txt").write_text(
                table.read_text(errors="replace")
            )


def audit(
    claim: str,
    runs: dict[str, Path],
    labels: dict[str, dict],
    model: str,
    seed: int,
    configs: bool = True,
    motion: bool = True,
) -> dict:
    """Flags for `runs` (name -> directory), each labelled as the experiment recorded.

    configs=False leaves out the config files; motion=False leaves out physics.txt.
    """
    ids = anonymize(sorted(runs), seed)
    names = {run_id: name for name, run_id in ids.items()}
    rows = []
    for name in sorted(runs, key=ids.get):
        metrics = aggregate_metrics(runs[name])
        if metrics is not None:
            rows.append({"run": ids[name], "label": labels[name], "metrics": metrics})
    schema = {
        "type": "object",
        "properties": {
            "flags": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "run": {"type": "string", "enum": sorted(names)},
                        "reason": {"type": "string"},
                    },
                    "required": ["run", "reason"],
                    "additionalProperties": False,
                },
            },
            "rules": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "file": {"type": "string", "enum": list(FILES)},
                        "path": {"type": "string"},
                        "op": {"type": "string", "enum": list(OPS)},
                        "value": {
                            "type": ["number", "string", "boolean", "array"],
                            "items": {"type": ["number", "string", "boolean"]},
                        },
                        "label_key": {"type": "string"},
                        "reason": {"type": "string"},
                    },
                    "required": ["id", "file", "path", "op", "reason"],
                    "additionalProperties": False,
                },
            },
        },
        "required": ["flags", "rules"],
        "additionalProperties": False,
    }
    with tempfile.TemporaryDirectory() as workdir:
        out = Path(workdir)
        snapshot(runs, ids, out, configs=configs, motion=motion)
        (out / "batch.json").write_text(
            json.dumps({"claim": claim, "results": rows}, indent=1)
        )
        proc = subprocess.run(
            [
                "claude",
                "-p",
                PROMPT,
                "--model",
                model,
                "--tools",
                "Read,Grep,Glob",
                "--permission-mode",
                "dontAsk",
                "--permission-prompts",
                "none",
                "--setting-sources",
                "",
                "--no-session-persistence",
                "--system-prompt-file",
                str(CONTRACT),
                "--output-format",
                "json",
                "--json-schema",
                json.dumps(schema),
            ],
            cwd=out,
            capture_output=True,
            text=True,
            timeout=1800,
            check=False,
        )
    if proc.returncode != 0:
        raise RuntimeError(f"audit call failed: {proc.stderr.strip()[-500:]}")
    result = json.loads(proc.stdout)
    if result["is_error"] or result.get("structured_output") is None:
        raise RuntimeError(f"audit call returned no answer: {result.get('result')}")
    flags = {}
    for flag in result["structured_output"]["flags"]:
        flags.setdefault(names[flag["run"]], flag["reason"])
    return {
        "ids": ids,
        "flags": flags,
        "rules": result["structured_output"]["rules"],
        "model": ",".join(result["modelUsage"]),
        "context_tokens": result["usage"]["input_tokens"]
        + result["usage"]["cache_creation_input_tokens"]
        + result["usage"]["cache_read_input_tokens"],
        "turns": result["num_turns"],
        "duration_ms": result["duration_ms"],
    }


def ran_scene(entry: dict) -> str:
    """The scene the run resolved to; B2's entries predate the scene_id key."""
    wizard = yaml.safe_load((ROOT / entry["run_dir"] / "wizard-config.yaml").read_text())
    return wizard["scenes"]["scene_ids"][0]


def scene_references(scenes: set[str], audited: Path) -> dict[str, dict]:
    """One kept clean run per scene, from the reference queues, never from the
    queue being audited. A frozen plan stood out only against its own scene
    (eval_plan_audit.py). Scenes with no such run get no reference."""
    found = {}
    for queue in REFERENCE_QUEUES:
        if (HARNESS / queue).resolve() == audited.resolve():
            continue
        for path in queue_entries(HARNESS / queue):
            entry = load_entry(path)
            if entry["resolution"] != "ACCEPT" or "quarantine" in entry:
                continue
            scene = ran_scene(entry)
            if scene in scenes and scene not in found:
                found[scene] = entry
    return found


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("queue", type=Path)
    parser.add_argument("--model", default="claude-opus-5-5")
    args = parser.parse_args()

    entry_paths = queue_entries(args.queue)
    # The loop already accounts for the runs it failed; the dataset is what it kept.
    kept = {
        path: entry
        for path in entry_paths
        if (entry := load_entry(path))["resolution"] == "ACCEPT"
    }
    batch = {
        entry["name"]: (ROOT / entry["run_dir"], entry["config"])
        for entry in kept.values()
    }
    scenes = {label["scene_id"] for _, label in batch.values()}
    references = scene_references(scenes, args.queue)
    runs = {name: path for name, (path, _) in batch.items()}
    labels = {name: label for name, (_, label) in batch.items()}
    for reference in references.values():
        runs[reference["name"]] = ROOT / reference["run_dir"]
        labels[reference["name"]] = {**reference["config"], "reference": True}
    claim = (
        f"All runs kept from queue {args.queue.name}, each with the config in its "
        "label. Runs labelled reference are known-good runs of the same setup on "
        "the same scenes, from earlier batches; they are there for comparison, "
        "not part of the batch."
    )
    report = audit(claim, runs, labels, args.model, seed=0)

    clean = clean_corpus()
    report["admissions"] = [
        {
            "rule": rule,
            **admission(rule, batch, set(report["flags"]) & set(batch), clean),
        }
        for rule in report["rules"]
    ]
    for path, entry in kept.items():
        if entry["name"] in report["flags"]:
            entry["quarantine"] = report["flags"][entry["name"]]
            save_entry(path, entry)
    (args.queue / "audit.json").write_text(json.dumps(report, indent=1) + "\n")
    summary = {
        "audited": len(batch),
        "quarantined": sorted(set(report["flags"]) & set(batch)),
        "references": sorted(r["name"] for r in references.values()),
        "scenes_without_reference": len(scenes) - len(references),
        "reference_flagged": sorted(
            r["name"] for r in references.values() if r["name"] in report["flags"]
        ),
        "rules_proposed": len(report["rules"]),
        "rules_admissible": [
            a["rule"]["id"] for a in report["admissions"] if a["admitted"]
        ],
    }
    print(json.dumps(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
