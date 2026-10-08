#!/usr/bin/env bash
# 7 Oct night, two runs in flight on the 24 GB GPU: the pedestrian study's
# hybrid arm starts now beside the rules arm (already running); the llm arm
# starts when the rules arm ends. Same plan, so the three stay comparable.
#
#   setsid nohup research/harness/run_parallel.sh >> research/harness/outer.log 2>&1 &
set -uo pipefail
cd "$(dirname "$0")/../.."

H=research/harness
BRIEF=research/briefs/categories/pedestrian_crossing.md
(
    echo "$(date -Is) pedestrian_crossing (hybrid) starting"
    uv run python $H/study.py $BRIEF --proposer hybrid --yes
    echo "$(date -Is) pedestrian_crossing (hybrid) done"
) &
while pgrep -f "study.py $BRIEF --proposer rules" > /dev/null; do sleep 60; done
echo "$(date -Is) pedestrian_crossing (llm) starting"
uv run python $H/study.py $BRIEF --proposer llm --yes
echo "$(date -Is) pedestrian_crossing (llm) done"
wait
