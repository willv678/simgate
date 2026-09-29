#!/usr/bin/env bash
# Campaign C1: the same fault plan under the script, tier 0 and tier 1.
# Waits for the S1 scene batch to finish, audits it, then runs the three arms
# one after another (one GPU), each audited at the end, and scores them.
# Every arm uses seed 1, so faults, order, and kill/hang times are identical.
#
#   setsid nohup research/harness/run_campaign_c1.sh > research/harness/c1_chain.log 2>&1 &
set -uo pipefail
cd "$(dirname "$0")/../.."

H=research/harness
SCENES=clipgt-01d503d4-449b-46fc-8d78-9085e70d3554,clipgt-023b7fcc-671c-40e3-9bd2-c66b0b073fbc,clipgt-0245ff75-aa3f-46b7-ba87-16a7afb841af,clipgt-026d6a39-bd8f-4175-bc61-fe50ed0403a3,clipgt-02e075b9-fd24-426b-971b-7cfcb2074cc9,clipgt-02eadd92-02f1-46d8-86fe-a9e338fed0b6

echo "$(date -Is) waiting for S1"
while pgrep -f "loop.py $H/s1_queue" > /dev/null; do sleep 60; done
echo "$(date -Is) S1 done; auditing it"
uv run python $H/audit.py $H/s1_queue

for arm in script model agent; do
    queue=$H/c1_${arm}_queue
    if [ ! -d "$queue" ]; then
        uv run python $H/enqueue_campaign.py "$queue" "c1${arm:0:1}" \
            --per-kind 5 --clean 10 --scene-ids "$SCENES" --seed 1
    fi
    echo "$(date -Is) arm $arm starting"
    uv run python $H/loop.py "$queue" --policy "$arm" --timeout-min 10 --audit \
        --trace $H/c1_${arm}_trace.jsonl
    uv run python $H/score_campaign.py "$queue" > /dev/null
    echo "$(date -Is) arm $arm done: $(tail -1 $H/c1_${arm}_trace.jsonl)"
done
echo "$(date -Is) campaign done"
