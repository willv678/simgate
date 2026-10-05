#!/usr/bin/env bash
# Campaign C3: seed 3, physics bounds on, and rails and kinematic persistent
# (they come from config errors, which repeat on a retry). Waits for the g2
# plan-fault batch, then runs script, tier 1, tier 0, each audited and scored.
# A rerun skips finished arms and resumes the current one.
#
#   setsid nohup research/harness/run_c3.sh >> research/harness/campaign.log 2>&1 &
set -uo pipefail
cd "$(dirname "$0")/../.."

H=research/harness
SCENES=clipgt-01d503d4-449b-46fc-8d78-9085e70d3554,clipgt-023b7fcc-671c-40e3-9bd2-c66b0b073fbc,clipgt-0245ff75-aa3f-46b7-ba87-16a7afb841af,clipgt-026d6a39-bd8f-4175-bc61-fe50ed0403a3,clipgt-02e075b9-fd24-426b-971b-7cfcb2074cc9,clipgt-02eadd92-02f1-46d8-86fe-a9e338fed0b6
export ALPASIM_PHYSICS=$H/rules/physics_c2.json

until grep -q "g2_plan done" $H/campaign.log; do sleep 60; done
for arm in script agent model; do
    name=c3_${arm}
    queue=$H/${name}_queue
    trace=$H/${name}_trace.jsonl
    if grep -q '"audit"' "$trace" 2> /dev/null; then
        echo "$(date -Is) $name already done"
        continue
    fi
    if [ ! -d "$queue" ]; then
        uv run python $H/enqueue_campaign.py "$queue" "c3${arm:0:1}" \
            --per-kind 5 --clean 10 --scene-ids "$SCENES" --seed 3 --silent-persistent
    fi
    echo "$(date -Is) $name starting"
    uv run python $H/loop.py "$queue" --policy "$arm" --timeout-min 10 --audit --trace "$trace"
    uv run python $H/score_campaign.py "$queue" > /dev/null
    echo "$(date -Is) $name done: $(grep '"summary"' "$trace" | tail -1)"
done
echo "$(date -Is) C3 done"
