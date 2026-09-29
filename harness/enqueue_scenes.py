"""Queue one READY run per scene that is downloaded locally.

Local scene files are `data/nre-artifacts/all-usdzs/<uuid>.usdz`, named by the
`uuid` column of the scene catalog. Each queued run uses that row's
`scene_id`. Run names are `<prefix>_<nnn>`, in catalog order.

    uv run python research/harness/enqueue_scenes.py research/harness/s1_queue s1
"""

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from enqueue import RUN_ROOT, add, new_entry
from read_state import ROOT

SCENE_FILE = "data/scenes/sim_scenes.csv"
LOCAL_SCENES = ROOT / "data" / "nre-artifacts" / "all-usdzs"


def local_scene_ids() -> list[str]:
    local = {path.stem for path in LOCAL_SCENES.glob("*.usdz")}
    with (ROOT / SCENE_FILE).open(encoding="utf-8") as handle:
        return [
            row["scene_id"] for row in csv.DictReader(handle) if row["uuid"] in local
        ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("queue", type=Path)
    parser.add_argument("prefix")
    parser.add_argument("--context-length", type=int, default=8)
    parser.add_argument("--planner-delay-us", type=int, default=0)
    parser.add_argument("--trafficsim-device", default="cpu")
    args = parser.parse_args()

    scene_ids = local_scene_ids()
    for index, scene_id in enumerate(scene_ids, start=1):
        name = f"{args.prefix}_{index:03d}"
        config = {
            "context_length": args.context_length,
            "planner_delay_us": args.planner_delay_us,
            "scene_file": SCENE_FILE,
            "scene_id": scene_id,
            "trafficsim_device": args.trafficsim_device,
        }
        add(args.queue, new_entry(name, f"{RUN_ROOT}/{name}", config))
    print(f"queued {len(scene_ids)} scenes in {args.queue}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
