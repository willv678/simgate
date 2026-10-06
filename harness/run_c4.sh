#!/usr/bin/env bash
# Campaign C4: seed 4 on six scenes no other campaign used (the first six kept
# S1 scenes not in B2, C1-C3, g2 or g3), every physics bound on including the
# plan handoff, and the plan faults added to the plan. Silent and plan faults
# persist on a retry. Waits for the g3 batch, then runs script, tier 1, tier 0,
# each audited and scored. A rerun skips finished arms and resumes the current
# one.
#
#   setsid nohup research/harness/run_c4.sh >> research/harness/campaign.log 2>&1 &
set -uo pipefail
cd "$(dirname "$0")/../.."

H=research/harness
SCENES=clipgt-032b6f21-6799-4ad8-8712-0405f087ac4a,clipgt-04394343-92f3-409c-9695-e7cd5397fa02,clipgt-04749bb9-9b37-495b-bed0-77f0e33ac7da,clipgt-048b974e-1546-488a-b8f9-d32bff77f5aa,clipgt-0499fb41-122d-4180-83af-f954a9974d3b,clipgt-04db1bb2-90fe-47a7-9d09-27d020c618d4
export ALPASIM_PHYSICS=$H/rules/physics_c4.json

until grep -q "g3_plan done" $H/campaign.log; do sleep 60; done
if [ ! -f "$ALPASIM_PHYSICS" ]; then
    uv run python -c "import json; b = json.load(open('$H/rules/physics.json')); b['enabled'] = True; json.dump(b, open('$ALPASIM_PHYSICS', 'w'), indent=1)"
fi
for arm in script agent model; do
    name=c4_${arm}
    queue=$H/${name}_queue
    trace=$H/${name}_trace.jsonl
    if grep -q '"audit"' "$trace" 2> /dev/null; then
        echo "$(date -Is) $name already done"
        continue
    fi
    if [ ! -d "$queue" ]; then
        uv run python $H/enqueue_campaign.py "$queue" "c4${arm:0:1}" \
            --per-kind 5 --clean 10 --scene-ids "$SCENES" --seed 4 \
            --silent-persistent --plan-faults
    fi
    echo "$(date -Is) $name starting"
    uv run python $H/loop.py "$queue" --policy "$arm" --timeout-min 10 --audit --trace "$trace"
    uv run python $H/score_campaign.py "$queue" > /dev/null
    echo "$(date -Is) $name done: $(grep '"summary"' "$trace" | tail -1)"
done
echo "$(date -Is) C4 done"
