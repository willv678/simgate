#!/usr/bin/env bash
# Night of 6 Oct: after g3, the first study run end to end from a brief
# (briefs/latency_budget.md, plan already written and shown on 6 Oct).
#
#   setsid nohup research/harness/run_tonight.sh >> research/harness/outer.log 2>&1 &
set -uo pipefail
cd "$(dirname "$0")/../.."

H=research/harness
until grep -q "g3_plan done" $H/campaign.log; do sleep 60; done
echo "$(date -Is) latency_budget study starting"
uv run python $H/study.py research/briefs/latency_budget.md --yes
echo "$(date -Is) latency_budget study done"
