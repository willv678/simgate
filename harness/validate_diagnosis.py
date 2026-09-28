"""FAILED -> accept or reject the diagnosis before recover.py may run.

The same gate applies to the script and the model. A rejected diagnosis sets
the run's resolution to HALT: the run is DONE, dropped, and needs a person.

    uv run python research/harness/validate_diagnosis.py <entry.json>
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from preflight import PreflightError, validate_preflight
from read_state import (
    CONFIG_KEYS,
    MAX_ATTEMPTS,
    State,
    load_entry,
    preflight_config,
    read_state,
    save_entry,
)
from skills import Skill

HALT = "HALT"
RECOVERIES = {Skill.CONFIGURE, Skill.RE_RUN, Skill.RESTART_CLEANUP}


def rejection(entry: dict, k_status: str) -> str | None:
    """Why the entry's diagnosis must not run, or None when it may."""
    diagnosis = entry["diagnosis"]
    if diagnosis["skill"] is None:
        return f"no skill: {diagnosis.get('error')}"
    try:
        skill = Skill(diagnosis["skill"])
    except ValueError:
        return f"unknown skill {diagnosis['skill']!r}"
    if skill not in RECOVERIES:
        return f"{skill.value} is not a recovery for FAILED"
    if entry["attempt"] >= MAX_ATTEMPTS:
        return f"attempt {entry['attempt']} of {MAX_ATTEMPTS}: budget spent"

    params = diagnosis["params"]
    if skill is not Skill.CONFIGURE:
        if params:
            return f"{skill.value} takes no params, got {sorted(params)}"
        if k_status.startswith("preflight_rejected"):
            return f"{skill.value} would relaunch a config preflight rejected"
        return None

    if not params:
        return "CONFIGURE with no params"
    unknown = sorted(set(params) - set(CONFIG_KEYS))
    if unknown:
        return f"CONFIGURE of unknown params {unknown}"
    patched = {**entry["config"], **params}
    if patched == entry["config"]:
        return "CONFIGURE changes nothing"
    try:
        validate_preflight(preflight_config(patched))
    except PreflightError as exc:
        return f"CONFIGURE rejected by preflight: {exc}"
    return None


def main() -> int:
    entry_path = Path(sys.argv[1])
    entry = load_entry(entry_path)
    state = read_state(entry)
    if state.state is not State.FAILED:
        raise SystemExit(f"{entry['name']} is {state.state.value}, not FAILED")

    reason = rejection(entry, state.k_status)
    entry["diagnosis"]["verdict"] = (
        "accepted" if reason is None else f"rejected: {reason}"
    )
    if reason is not None:
        entry["resolution"] = HALT
    save_entry(entry_path, entry)
    print(
        json.dumps(
            {"accepted": reason is None, "verdict": entry["diagnosis"]["verdict"]}
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
