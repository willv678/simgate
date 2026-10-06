#!/usr/bin/env bash
# g3, the held-out plan-fault batch (0.3 m lateral bias, 0.3 m waypoint noise,
# clean; four scenes outside g2), under the bounds in rules/physics.json and
# tier 1. Waits for the outer-loop pilot to free the GPU. eval_plan_audit.py
# --queue g3_plan_queue is chained separately on "g3_plan done".
#
#   setsid nohup research/harness/run_g3.sh >> research/harness/campaign.log 2>&1 &
set -uo pipefail
cd "$(dirname "$0")/../.."

H=research/harness
until grep -q "pilot done" $H/outer.log 2> /dev/null; do sleep 60; done
echo "$(date -Is) g3_plan starting"
uv run python $H/loop.py $H/g3_plan_queue --policy agent --timeout-min 10 \
    --stall-s 120 --poll-s 5 --audit --trace $H/g3_plan_trace.jsonl
uv run python $H/score_campaign.py $H/g3_plan_queue > /dev/null
echo "$(date -Is) g3_plan done"
