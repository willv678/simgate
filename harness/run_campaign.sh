#!/usr/bin/env bash
# Campaigns C1 and C2: the same fault plan under the script, tier 1 and tier 0.
# Waits for the S1 scene batch to finish, audits it, then runs every arm one
# after another (one GPU), each audited at the end, and scores it. Within a
# campaign every arm uses the same seed, so faults, order, and kill/hang times
# are identical. C2 repeats C1 with seed 2, which doubles every cell.
# Tier 1 runs before tier 0 so that stopping early keeps script vs tier 1.
# A rerun skips finished arms and resumes the current one.
#
#   setsid nohup research/harness/run_campaign.sh > research/harness/campaign.log 2>&1 &
set -uo pipefail
cd "$(dirname "$0")/../.."

H=research/harness
SCENES=clipgt-01d503d4-449b-46fc-8d78-9085e70d3554,clipgt-023b7fcc-671c-40e3-9bd2-c66b0b073fbc,clipgt-0245ff75-aa3f-46b7-ba87-16a7afb841af,clipgt-026d6a39-bd8f-4175-bc61-fe50ed0403a3,clipgt-02e075b9-fd24-426b-971b-7cfcb2074cc9,clipgt-02eadd92-02f1-46d8-86fe-a9e338fed0b6

echo "$(date -Is) waiting for S1"
while pgrep -f "loop.py $H/s1_queue" > /dev/null; do sleep 60; done
echo "$(date -Is) S1 done; auditing it"
[ -f $H/s1_queue/audit.json ] || uv run python $H/audit.py $H/s1_queue

for seed in 1 2; do
    for arm in script agent model; do
        name=c${seed}_${arm}
        queue=$H/${name}_queue
        trace=$H/${name}_trace.jsonl
        if grep -q '"audit"' "$trace" 2> /dev/null; then
            echo "$(date -Is) $name already done"
            continue
        fi
        if [ ! -d "$queue" ]; then
            uv run python $H/enqueue_campaign.py "$queue" "c${seed}${arm:0:1}" \
                --per-kind 5 --clean 10 --scene-ids "$SCENES" --seed "$seed"
        fi
        echo "$(date -Is) $name starting"
        uv run python $H/loop.py "$queue" --policy "$arm" --timeout-min 10 --audit \
            --trace "$trace"
        uv run python $H/score_campaign.py "$queue" > /dev/null
        echo "$(date -Is) $name done: $(grep '"summary"' "$trace" | tail -1)"
    done
done
echo "$(date -Is) campaign done"
