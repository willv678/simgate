"""Evidence from earlier studies: kept runs elsewhere with this study's settings.

A study whose plan says `"reuse_prior": true` (a person adds it) starts with
the kept runs of other studies that it would have run itself: rebuilding the
run this study would queue for the prior run's scene, controller and knob
values gives the same effective settings, the seed apart (a different seed is
a repeat). The proposer, the goal check and the report then see those runs as
evidence, marked with the study they came from.

A study's own proposer arms never share runs: every arm folder under the same
study is excluded, so the comparison of proposers stays independent.
"""

from pathlib import Path

from knobs import SCENARIO, UNVARIED, run_config
from read_state import (
    ROOT,
    frame_interval_us,
    load_entry,
    queue_entries,
    requested_controller,
    retime_request,
    traffic_mode,
)

STUDIES = ROOT / "research" / "studies"


def effective(config: dict) -> dict:
    """What a run actually asks the simulator for, with every default made
    explicit and the actor target only when a retiming applies; the seed left
    out."""
    found = {
        k: v
        for k, v in config.items()
        if k not in ("seed", "retime_class", "retime_track")
    }
    for knob, value in UNVARIED.items():
        found.setdefault(knob, value)
    found["frame_interval_us"] = frame_interval_us(config)
    found["traffic"] = traffic_mode(config)
    found["controller"] = requested_controller(config)
    rule = retime_request(config)
    found["retime"] = None if rule is None else rule
    return found


def study_root(queue: Path) -> Path:
    """The study folder a queue belongs to: <study>/queue for the llm arm,
    <study>/<proposer>/queue for the others."""
    folder = queue.parent
    return folder if folder.parent == STUDIES else folder.parent


def prior_runs(
    queue: Path, scenes: list[str], fixed: dict, controllers: list[str], varied: tuple
) -> list[dict]:
    """Kept, unquarantined entries of other studies that this study would have
    run itself, each marked with `prior`: the study it came from."""
    own = study_root(queue)
    found = []
    for other in sorted(STUDIES.rglob("queue")):
        if not other.is_dir() or study_root(other) == own:
            continue
        for path in queue_entries(other):
            entry = load_entry(path)
            config = entry["config"]
            if entry["resolution"] != "ACCEPT" or "quarantine" in entry:
                continue
            controller = requested_controller(config)
            values = {k: config.get(k, UNVARIED[k]) for k in varied}
            if (
                config["scene_id"] not in scenes
                or controller not in controllers
                or any(values[k] not in SCENARIO[k] for k in varied)
            ):
                continue
            ours = run_config(config["scene_id"], values, fixed, controller)
            if effective(ours) == effective(config):
                found.append({**entry, "prior": study_root(other).name})
    return found
