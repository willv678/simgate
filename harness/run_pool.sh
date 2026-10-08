#!/usr/bin/env bash
# Keeps two studies on the GPU at a time (MAX_RUNS_IN_FLIGHT), working through
# JOBS in order: "<brief name> <proposer>". Studies already running (started
# elsewhere) count toward the two. Each job resumes if rerun.
#
#   setsid nohup research/harness/run_pool.sh >> research/harness/outer.log 2>&1 &
set -uo pipefail
cd "$(dirname "$0")/../.."

H=research/harness
SLOTS=2
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
    until [ "$(pgrep -fc "bin/python[0-9.]* research/harness/study.py")" -lt "$SLOTS" ]; do sleep 30; done
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
