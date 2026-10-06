#!/usr/bin/env bash
# 6 Oct afternoon and night, after the pilot frees the GPU: the confirmation
# study (briefs/confirm_break_02eadd92.md, planned at 1:55 pm), then g3, then
# the latency_budget study. Each step resumes if rerun.
#
#   setsid nohup research/harness/run_today.sh >> research/harness/outer.log 2>&1 &
set -uo pipefail
cd "$(dirname "$0")/../.."

H=research/harness
until grep -q "pilot done" $H/outer.log; do sleep 15; done
echo "$(date -Is) confirm_break_02eadd92 study starting"
uv run python $H/study.py research/briefs/confirm_break_02eadd92.md --yes
echo "$(date -Is) confirm_break_02eadd92 study done"
research/harness/run_g3.sh >> $H/campaign.log 2>&1
echo "$(date -Is) latency_budget study starting"
uv run python $H/study.py research/briefs/latency_budget.md --yes
echo "$(date -Is) latency_budget study done"
