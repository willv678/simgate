#!/usr/bin/env bash
# Night of 6-7 Oct: after the actor-retiming smoke test (r1) passes, the
# pedestrian-crossing study three times on one plan: rules, hybrid, llm.
# Stops if any r1 run was not kept: the studies rely on retiming working.
#
#   setsid nohup research/harness/run_overnight.sh >> research/harness/outer.log 2>&1 &
set -uo pipefail
cd "$(dirname "$0")/../.."

H=research/harness
BRIEF=research/briefs/categories/pedestrian_crossing.md
until grep -q "r1 done" $H/outer.log; do sleep 30; done
if ! uv run python - <<'PY'
import json, glob, sys
entries = [json.load(open(p)) for p in sorted(glob.glob("research/harness/r1_queue/0*.json"))]
kept = [e["name"] for e in entries if e["resolution"] == "ACCEPT" and e["parent"] is None]
print("r1 kept:", kept)
sys.exit(0 if len(kept) == 3 else 1)
PY
then
    echo "$(date -Is) overnight studies NOT started: the retiming smoke test did not keep all three runs"
    exit 1
fi
for proposer in rules hybrid llm; do
    echo "$(date -Is) pedestrian_crossing ($proposer) starting"
    uv run python $H/study.py $BRIEF --proposer $proposer --yes
    echo "$(date -Is) pedestrian_crossing ($proposer) done"
done
