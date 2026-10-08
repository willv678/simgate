#!/usr/bin/env bash
# Replaces run_pool.sh (7 Oct, 21:3x): first the seeded-replay validation (rp1:
# one scene, seed 4242 twice and 4243 once, traffic replayed); if the two
# same-seed runs come out identical, the category studies not yet started are
# seeded ("seeded": true). Then the same job list, two studies at a time.
#
#   setsid nohup research/harness/run_pool2.sh >> research/harness/outer.log 2>&1 &
set -uo pipefail
cd "$(dirname "$0")/../.."

H=research/harness
SLOTS=2
running() { pgrep -fc "bin/python[0-9.]* research/harness/study.py"; }

until [ "$(running)" -lt "$SLOTS" ]; do sleep 30; done
echo "$(date -Is) rp1 (seeded replay validation) starting"
uv run python $H/loop.py $H/rp1_queue --policy agent --timeout-min 15 --stall-s 120 \
    --poll-s 5 --trace $H/rp1_trace.jsonl
if uv run python $H/check_replay.py diag/rp1_001 diag/rp1_002 > $H/rp1_same_seed.json; then
    echo "$(date -Is) rp1: same seed reproduced the run; seeding the category studies"
    for study in lead_vehicle intersection cut_in_merge; do
        uv run python - "$study" <<'PY'
import json, sys
from pathlib import Path
path = Path("research/studies") / sys.argv[1] / "plan.json"
data = json.loads(path.read_text())
data["plan"]["seeded"] = True
path.write_text(json.dumps(data, indent=1) + "\n")
PY
    done
else
    echo "$(date -Is) rp1: same seed did NOT reproduce the run; studies stay unseeded (see rp1_same_seed.json)"
fi
uv run python $H/check_replay.py diag/rp1_001 diag/rp1_003 > $H/rp1_other_seed.json
echo "$(date -Is) rp1 done"

JOBS=(
    "pedestrian_crossing llm"
    "pedestrian_crossing random"
    "pedestrian_crossing optuna"
    "lead_vehicle rules"
    "lead_vehicle hybrid"
    "lead_vehicle llm"
    "intersection rules"
    "intersection hybrid"
    "intersection llm"
    "cut_in_merge rules"
    "cut_in_merge hybrid"
    "cut_in_merge llm"
)
for job in "${JOBS[@]}"; do
    read -r brief proposer <<< "$job"
    until [ "$(running)" -lt "$SLOTS" ]; do sleep 30; done
    (
        echo "$(date -Is) $brief ($proposer) starting"
        uv run --with optuna python $H/study.py research/briefs/categories/$brief.md \
            --proposer "$proposer" --yes
        echo "$(date -Is) $brief ($proposer) done"
    ) &
    sleep 60
done
wait
echo "$(date -Is) pool done"
