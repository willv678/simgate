#!/usr/bin/env bash
# Rebuild every study's comparison, web pages and the cross-study summary from
# what is on disk; repeat every hour with --watch. Reads only; launches nothing.
#
#   research/harness/refresh_results.sh [--watch]
set -uo pipefail
cd "$(dirname "$0")/../.."

H=research/harness
refresh() {
    for study in research/studies/*/; do
        [ -f "$study/plan.json" ] || continue
        grep -q '"goal"' "$study/plan.json" || continue
        uv run python $H/compare_proposers.py "$study" > /dev/null 2>&1
        for arm in "$study" "$study"*/; do
            [ -f "$arm/report.json" ] && uv run python $H/study_page.py "$arm" > /dev/null 2>&1
        done
    done
    uv run python $H/summarize_studies.py > /dev/null 2>&1
    echo "$(date -Is) results refreshed"
}
refresh
while [ "${1:-}" = "--watch" ]; do
    sleep 3600
    refresh
done
