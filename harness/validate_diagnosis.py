"""FAILED -> accept or reject the diagnosis before recover.py may run.

The same gate applies to the script and the model. A rejected diagnosis sets
the run's resolution to HALT: the run is DONE, dropped, and needs a person.

    uv run python research/harness/validate_diagnosis.py <entry.json>
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from read_state import (
    CONFIGURABLE_KEYS,
    MAX_ATTEMPTS,
    State,
    config_problem,
    load_entry,
    read_state,
    save_entry,
)
from skills import Skill

HALT = "HALT"
RECOVERIES = {
    Skill.CONFIGURE,
    Skill.RE_RUN,
    Skill.RESTART_CLEANUP,
    Skill.CLEANUP_ENV,
    Skill.HALT,
}
# A cleanup that did not fix the machine will not fix it the second time.
MAX_ENV_CLEANUPS = 1


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
    params = diagnosis["params"]
    if skill is not Skill.CONFIGURE and params:
        return f"{skill.value} takes no params, got {sorted(params)}"
    # Handing a run to a person is always allowed. It spends no launch.
    if skill is Skill.HALT:
        return None

    # The run never launched, so it has spent no attempt.
    if k_status.startswith("environment"):
        if skill is not Skill.CLEANUP_ENV:
            return f"{skill.value} cannot fix the environment"
        if entry["env_cleanups"] >= MAX_ENV_CLEANUPS:
            return "environment still failing after CLEANUP_ENV"
        return None

    if entry["attempt"] >= MAX_ATTEMPTS:
        return f"attempt {entry['attempt']} of {MAX_ATTEMPTS}: budget spent"
    if skill is not Skill.CONFIGURE:
        if k_status.startswith("preflight_rejected"):
            return f"{skill.value} would relaunch a config preflight rejected"
        return None

    if not params:
        return "CONFIGURE with no params"
    unknown = sorted(set(params) - set(CONFIGURABLE_KEYS))
    if unknown:
        return f"CONFIGURE of unknown params {unknown}"
    patched = {**entry["config"], **params}
    if patched == entry["config"]:
        return "CONFIGURE changes nothing"
    problem = config_problem(patched)
    if problem is not None:
        return f"CONFIGURE rejected by preflight: {problem}"
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
