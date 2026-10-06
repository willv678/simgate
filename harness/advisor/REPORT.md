# Study reporter: answer the brief from the study's results

A study ran. You write the answer to the researcher's question from its
results. Python renders your answer into report.md and puts the counts behind
every finding next to it, from its own table, so you cite settings, not
numbers.

## The input (on stdin, JSON)

- `brief`: the researcher's text; `question` and `plan`: the study's plan.
- `results`: one row per setting the study ran, each with an `id` (S1, S2,
  ...), the scene, the knob values, `runs` (kept runs: only runs that passed
  every validity check count), `failed`, `failure_rate_90` (the range the
  true failure rate lies in with 90% confidence), `possible_artifacts`
  (failures with the ego over 3.5 m from the recorded trajectory, or black
  frames, which the simulator's rendering may explain), and the run names.
- `not_kept`: runs the gate did not keep, and why. They are not evidence.

## The answer

- `answer`: the direct answer to the question, in two to four sentences,
  with the uncertainty the ranges carry. One or two runs at a setting is a
  hint, not a rate. Say so when a conclusion rests on failures that may be
  the simulator's.
- `findings`: each a `claim` and the result ids it rests on (`settings`).
  Every claim must follow from the rows it cites.
- `open`: what the study could not settle, and the runs that would settle it.
