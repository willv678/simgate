"""COMPLETE -> mark the run ACCEPT, which makes it DONE and keeps it in the dataset.

Runs after analyze.py. The run directory is not moved or deleted.

    uv run python research/harness/archive.py <entry.json>
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from analyze import RESULTS_NAME
from read_state import State, load_entry, read_state, save_entry
from skills import Skill


def main() -> int:
    entry_path = Path(sys.argv[1])
    entry = load_entry(entry_path)
    state = read_state(entry)
    if state.state is not State.COMPLETE:
        raise SystemExit(f"{entry['name']} is {state.state.value}, not COMPLETE")
    results = entry_path.parent / RESULTS_NAME
    rows = results.read_text(encoding="utf-8").splitlines() if results.is_file() else []
    if not any(json.loads(line)["run_dir"] == entry["run_dir"] for line in rows):
        raise SystemExit(
            f"{entry['run_dir']} is not in {results}; run analyze.py first"
        )

    entry["resolution"] = Skill.ACCEPT.value
    save_entry(entry_path, entry)
    print(json.dumps({"resolution": entry["resolution"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
