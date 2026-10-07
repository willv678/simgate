"""Download scene artifacts (.usdz) from the NuRec dataset on Hugging Face.

Takes the catalog's rows in order, skips scenes already on disk, and downloads
the next `--count` scenes of one release (`--revision`, 26.01 by default, the
release most of our scenes come from). Each file is checked against the UUID
in its own metadata before it is kept. Needs HF_TOKEN with access to the
gated dataset.

    uv run python research/harness/download_scenes.py --count 150
"""

import argparse
import csv
import os
import shutil
import tempfile
import zipfile
from pathlib import Path

import yaml
from huggingface_hub import hf_hub_download

ALPASIM_ROOT = Path(__file__).resolve().parents[2]
HUGGINGFACE_REPO = "nvidia/PhysicalAI-Autonomous-Vehicles-NuRec"
CATALOG = ALPASIM_ROOT / "data/scenes/sim_scenes.csv"
OUT_DIR = ALPASIM_ROOT / "data/nre-artifacts/all-usdzs"
MIN_SIZE = 100_000_000


def download(row: dict) -> None:
    target = OUT_DIR / f"{row['uuid']}.usdz"
    with tempfile.TemporaryDirectory(dir=OUT_DIR) as tmp:
        path = hf_hub_download(
            repo_id=HUGGINGFACE_REPO,
            repo_type="dataset",
            filename=row["path"],
            revision=row["hf_revision"],
            local_dir=tmp,
            token=os.environ["HF_TOKEN"],
        )
        with zipfile.ZipFile(path) as usdz, usdz.open("metadata.yaml") as meta:
            found = yaml.safe_load(meta)["uuid"]
        if found != row["uuid"]:
            raise ValueError(f"UUID mismatch: {found} != {row['uuid']}")
        shutil.move(path, target)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, required=True)
    parser.add_argument("--revision", default="26.01")
    args = parser.parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with CATALOG.open(newline="") as handle:
        rows = [r for r in csv.DictReader(handle) if r["hf_revision"] == args.revision]
    missing = [
        r
        for r in rows
        if not (OUT_DIR / f"{r['uuid']}.usdz").exists()
        or (OUT_DIR / f"{r['uuid']}.usdz").stat().st_size < MIN_SIZE
    ]
    done = 0
    for row in missing[: args.count]:
        print(f"[{done + 1}/{args.count}] {row['scene_id']}", flush=True)
        download(row)
        done += 1
    print(
        f"downloaded {done}; {len(rows) - len(missing) + done} of {len(rows)} on disk"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
