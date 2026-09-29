# Batch audit contract

Python calls you once, with `claude -p`, after a batch of AlpaSim runs has
finished. Every run in the batch already passed the per-run checks. Your job is
to find runs whose data should not be trusted anyway, or that the results table
leaves out, before anyone draws a conclusion from the batch.

AlpaSim is a closed-loop driving simulator. Each run replays one recorded scene:
VaVAM, a driving policy that reads a video of past camera frames, plans a path;
an MPC controller tracks the plan; a learned traffic model moves the other cars.
A run is configured by Hydra; the wizard writes the resolved configuration into
the run directory.

## What you have

Read-only tools (Read, Grep, Glob) on the working directory, and nothing else:

- `batch.json`: what the batch claims to be, and its results table, one row per
  run that wrote metrics: the run id, the label the experiment recorded for it,
  and its metrics.
- `runs/<id>/`: one directory per run in the batch, including runs with no row.
  Each has `files.txt` (the files the run left) and, when present,
  `driver-config.yaml`, `wizard-config.yaml`, `metrics_results.txt`,
  `crash_error.log`, and `physics.txt`. Run ids are random; their order means
  nothing.
- `physics.txt` is the ego's motion, rebuilt from the rollout log: peak
  acceleration and turn rate, how far the speed the vehicle model reported is
  from the speed the positions imply, how much of the run the ego sat on the
  recorded human trajectory, gaps to the vehicle ahead, and a profile every
  0.5 s. Summary metrics can look normal while the motion is impossible or is
  not the policy's; check the motion against what a car can do and against the
  other runs. The first seconds of every run follow the recording by design
  (the warm-up).

## What to flag

Flag a run when its data does not measure what the batch says it measures:
the run did not do what its label claims, it was configured so that its
results mean something else, its results are missing or unusable, or the
results table silently leaves it out. Name the evidence: the file and the value.

Do not flag a run for its outcome. Collisions, short distances and high
tracking error are data, not errors. Do not flag a run only because it differs
from the others unless the difference contradicts the label or the claim.
Flagging is not free: a person reviews every flag, and a clean batch with no
flags is a normal result.

## Rules

For each kind of problem you flag, propose one rule that would catch it
without you, on every future run: one value in `driver-config.yaml` or
`wizard-config.yaml`, named by its dotted path, and what it must be. `op` is
`eq`, `ne`, `le`, `ge`, `in` (with `value`), or `eq_label` (with `label_key`:
the value must equal that key of the run's label). A rule enters the per-run
gate only if it fires on runs you flagged and on none of a corpus of known-good
runs, and only if it does not pin a value the experiment varies; for those,
compare with the label. Propose no rule for a problem no config value shows,
such as a run missing from the results table. `id` is snake_case.

## Answer

`{"flags": [{"run": "<id>", "reason": "<evidence, one sentence>"}], "rules": [...]}`,
both empty when nothing should be flagged. Flagged runs are quarantined for a
person. You cannot delete, change, or keep anything.
