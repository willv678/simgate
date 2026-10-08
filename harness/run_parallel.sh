#!/usr/bin/env bash
# The pedestrian study's three arms on one plan, two at a time on the 24 GB
# GPU: rules and hybrid together, llm as soon as either ends.
#
#   setsid nohup research/harness/run_parallel.sh >> research/harness/outer.log 2>&1 &
set -uo pipefail
cd "$(dirname "$0")/../.."

H=research/harness
BRIEF=research/briefs/categories/pedestrian_crossing.md
arm() {
    echo "$(date -Is) pedestrian_crossing ($1) starting"
    uv run python $H/study.py $BRIEF --proposer "$1" --yes
    echo "$(date -Is) pedestrian_crossing ($1) done"
}
arm rules &
sleep 30
arm hybrid &
wait -n
arm llm &
wait
