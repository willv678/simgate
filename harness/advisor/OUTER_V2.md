# Outer loop, version 2: choose the next runs of a study

Python runs the study. Each round it calls you once, with `claude -p` and no
tools, to choose the next runs; then it checks every run you propose, queues
the legal ones, and runs them through the inner loop, which keeps a run only
if it passes every check (exit code, metrics, the requested settings landed,
physics, the batch audit). You never launch or keep anything.

## The study

The driving policy is VaVAM with a linear MPC controller, on real recorded
scenes. The other road users replay their recorded tracks (retimed by the
study's knobs); they do not react to the ego.
The question (`objective`): **which settings of the study's knobs make the
policy fail on which scenes**, such as the ego's speed when the policy takes
over (`ego_speed_scale`, a multiple of its recorded speed at the same place),
a recorded actor's timing and speed, a sideways shift of the plan (as from a
perception error), or planner delay.

With traffic replayed, a run at a given scene and setting is close to
repeatable: the seed moves only the policy's sampled plan. Earlier studies
found repeats of one setting ending the same way in nearly every run. So a
setting that failed once will usually fail again; repeats are still how the
goal confirms a setting, but expect them to agree, and do not spend runs
re-testing settings whose outcome is already clear.

A run **failed** if, after the policy took over, the ego left the road or hit
something with its front or side before anything hit it from behind
(replayed traffic cannot brake for a slower ego, so being rear-ended is not
the policy's failure), and the contact did not begin before the policy took
over.

What earlier studies of this policy found, to use as a prior: once it drives,
it drifts left of the human's path (a median 2.4 m within 5 s); most of its
failures are steering into another road user or off the road, not failing to
brake; a faster ego at the hand-off leaves it less room; a slower lead car
(0.5x) makes a harder stop.

## The input (on stdin, JSON)

- `objective`: the study question, as above.
- `candidates`: the scenes you may choose, each with what is known about it at
  0 delay from an earlier one-run-per-scene batch: whether that run failed,
  its top speed, and its closest distance to another actor.
- `knobs`: the knobs this study varies, each with its legal `values` and its
  `meaning`.
- `history`: every run of this study so far: scene, knob settings, `failed`,
  and the gate's verdict (`kept`, or why not). Only kept runs are evidence.
- `summary`: the kept runs per setting: `runs`, `failed`, and
  `failure_rate_90`, the range the true failure rate lies in with 90%
  confidence. A wide range means the setting needs more runs. A failed run
  also reports how far the ego was from the recorded trajectory when it
  failed; `possible_artifacts` counts failures so far off it (or with black
  frames) that the simulator's rendering, not the policy, may be to blame.
- `candidates` (hybrid studies only): the runs rules allow this round, each
  with a `reason` and a `score` (higher means the rules rank it more useful:
  confirm a near-failure, step from the most critical setting, first probe of
  a scene). Choose only among them, in any mix and with repeats; a run that is
  not a candidate is dropped. Each run's criticality (1 for a failure, up to
  0.9 for a near miss) and each setting's mean criticality are in `history`
  and `summary`.
- `failures` (version 2): every failed kept run so far, with what a
  reviewer who watched its video said: `cause` (no_brake_for_lead,
  turned_into_actor, left_road, actor_hit_ego, rendering, other),
  `what_happened`, and `policy_at_fault`. Use them to see why settings fail
  and where else the same mechanism would.
- `scene_facts` (version 2): for each candidate scene, what its recording
  holds: the ego's turn and top speed, the lead vehicle (gap, speed drop),
  cars cutting in, crossing or oncoming, pedestrians near the path.
- `notes` (version 2): what you wrote last round in `notes`, null in the
  first round.
- `goal` and `goal_status`: the study's win condition, which code checks
  after every round, and where it stands (null when the study has none). The
  study stops when it is met, so spend runs on what it still lacks.
- `round`, `rounds`, `runs_this_round`: where the study is and how many runs
  to propose now.
- `systems` and `comparison` (A/B studies only): the two controllers the
  study compares, `a` and `b`. Every run you propose is run once on each, a
  pair with the same scene and knob values; `history` names each run's
  `controller`, `summary` pools both controllers' runs per setting, and
  `comparison` shows them side by side, with `paired` counting the pairs
  where only one failed. The goal asks which fails less, pooled over all
  settings: spend runs where they could differ, not on settings both always
  pass or always fail.

## The answer

Exactly `runs_this_round` runs, each a `scene_id`, a value for every knob in
`knobs`, and a one-sentence `why`, plus a short `plan` for the study, and
`notes`: what you believe so far and what you will test next (at most about
100 words), which you get back next round.
Repeating a setting is allowed and often right. A proposed run with a scene
outside `candidates`, a knob value outside its `values`, or any other key is
dropped, not run.

Spend runs where they change what the study can conclude: settings whose
failure rate is most uncertain, and settings near where a scene starts to fail.
Settings that already failed or passed many times teach little more. Every
other scenario knob stays at its unperturbed value (0, or 1 for a speed
scale).
