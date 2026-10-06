#!/usr/bin/env bash
# Outer-loop pilot, 6 Oct: the same study twice on the same eight candidate
# scenes and budget (3 rounds of 5 runs), proposed by Claude (o1) and at random
# (o2). Waits for C3 to free the GPU. A rerun resumes each study.
#
#   setsid nohup research/harness/run_pilot.sh >> research/harness/outer.log 2>&1 &
set -euo pipefail
cd "$(dirname "$0")/../.."

H=research/harness
until grep -q "C3 done" $H/campaign.log; do sleep 30; done
uv run pytest -q $H
echo "$(date -Is) o1 starting"
uv run python $H/outer.py o1 --proposer llm --rounds 3 --per-round 5
echo "$(date -Is) o2 starting"
uv run python $H/outer.py o2 --proposer random --rounds 3 --per-round 5 --seed 1
echo "$(date -Is) pilot done"
