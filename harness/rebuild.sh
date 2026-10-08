#!/usr/bin/env bash
# Rebuild every table and figure the paper reads from data on disk, with no
# model call: the tests (the exhaustive gate check included), the campaign
# report, the physics calibration and jerk analysis, and the figures, which are
# then copied into paper/figures. The model evaluations (eval_auditor.py,
# repeat_auditor.py, repeat_tiers.py, eval_physics_audit.py, eval_plan_audit.py)
# call the model and are not rerun here; their outputs stay as recorded.
#
#   research/harness/rebuild.sh
set -euo pipefail
cd "$(dirname "$0")/../.."

H=research/harness
uv run pytest -q $H
for script in campaign_report calibrate_physics jerk_separation \
    plot_results plot_campaign plot_architecture plot_framework; do
    echo "== $script"
    uv run python $H/$script.py > /dev/null
done
cp research/figures/{architecture,campaign_invalid,campaign_outcomes}.pdf research/paper/figures/
git -C research status --short -- harness/*.txt figures paper/figures
