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
- In an A/B study (`plan.fixed.compare` names controllers `a` and `b`), each
  `results` row instead has `a` and `b`, each with its `controller` and the
  counts above, and `paired`: the pairs (one run of each at the setting) and
  how many only `a` or only `b` failed. `goal_status` then has each
  controller's failures pooled over the pairs, with 90% ranges, and an exact
  sign test (`p`) over the pairs where only one failed. Say which controller
  is safer only if the goal says the ranges separate; otherwise say no
  difference was shown, and what the sign test and the settings suggest.
- `triage`: for each failed kept run, the cause read from its video and log
  (`no_brake_for_lead`, `turned_into_actor`, `left_road`, `actor_hit_ego`,
  `rendering`, `other`), whether the policy was at fault, and what happened.
  Use it to say why a scene fails, and say when failures were not the
  policy's.
- `goal_status`: whether the study's win condition was met, as code checked
  it from the ranges, with its verdict. The report prints it above your
  answer; your answer must agree with it.
- `not_kept`: runs the gate did not keep, and why. They are not evidence.

## The answer

Write no counts, totals, rates or ranges yourself: say "every run at 150 ms
and above failed", not "4 of 4", and cite the settings. The report prints the
counts next to each finding from its own table; a number you add by hand can
disagree with it. Values of the knobs (150 ms) are fine.

- `answer`: the direct answer to the question, in two to four sentences,
  with the uncertainty the ranges carry. One or two runs at a setting is a
  hint, not a rate. Say so when a conclusion rests on failures that may be
  the simulator's.
- `findings`: each a `claim` and the result ids it rests on (`settings`).
  Every claim must follow from the rows it cites.
- `open`: what the study could not settle, and the runs that would settle it.
