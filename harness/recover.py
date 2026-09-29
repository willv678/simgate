"""FAILED -> run a diagnosis validate_diagnosis.py accepted.

A recovery of a launched run queues a new READY run in a new directory, one
attempt later, and resolves the failed run with the skill. The failed run
directory is not touched. RESTART_CLEANUP first takes down the failed run's
containers. CLEANUP_ENV first removes AlpaSim's leftovers from the machine
(environment.py); on a run that never launched it queues nothing, and the
same entry is READY again.

    uv run python research/harness/recover.py <entry.json>
"""

import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from enqueue import add, new_entry
from environment import cleanup_environment
from read_state import load_entry, run_dir, save_entry
from skills import Skill


def cleanup(entry: dict) -> str:
    compose = run_dir(entry) / "docker-compose.yaml"
    if not compose.is_file():
        return f"no {compose.name}; nothing to take down"
    subprocess.run(
        ["docker", "compose", "-f", str(compose), "down", "--remove-orphans"],
        check=True,
        capture_output=True,
    )
    return f"docker compose down on {entry['run_dir']}"


def main() -> int:
    entry_path = Path(sys.argv[1])
    entry = load_entry(entry_path)
    diagnosis = entry["diagnosis"]
    if diagnosis is None or diagnosis.get("verdict") != "accepted":
        raise SystemExit(f"{entry['name']} has no accepted diagnosis")
    skill = Skill(diagnosis["skill"])

    if skill is Skill.CLEANUP_ENV:
        note = "; ".join(cleanup_environment()) or "nothing to remove"
        if not entry["launched"]:
            entry["environment"] = None
            entry["env_cleanups"] += 1
            save_entry(entry_path, entry)
            print(json.dumps({"skill": skill.value, "queued": None, "cleanup": note}))
            return 0
    elif skill is Skill.RESTART_CLEANUP:
        note = cleanup(entry)
    else:
        note = None
    attempt = entry["attempt"] + 1
    name = f"{re.sub(r'_a[0-9]+$', '', entry['name'])}_a{attempt}"
    child_dir = Path(entry["run_dir"]).parent / name
    child = new_entry(
        name,
        str(child_dir),
        {**entry["config"], **diagnosis["params"]},
        attempt=attempt,
        parent=entry_path.name,
    )
    child_path = add(entry_path.parent, child)

    entry["resolution"] = skill.value
    save_entry(entry_path, entry)
    print(
        json.dumps({"skill": skill.value, "queued": child_path.name, "cleanup": note})
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
