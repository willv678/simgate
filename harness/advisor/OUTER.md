# Outer loop: choose the next runs of a study

Python runs the study. Each round it calls you once, with `claude -p` and no
tools, to choose the next runs; then it checks every run you propose, queues
the legal ones, and runs them through the inner loop, which keeps a run only
if it passes every check (exit code, metrics, the requested settings landed,
physics, the batch audit). You never launch or keep anything.

## The study

The driving policy is VaVAM with a linear MPC controller and CATK traffic, on
real recorded scenes. The question (`objective`): **how does the policy's
failure rate on each candidate scene change with the study's knobs**, such as
planner delay (the time between a camera frame and the controller receiving
the plan made from it) or a sideways shift of the plan (as from a perception
error)? AV teams want to know which scenes are fragile and roughly where each
breaks.

Each run is one random sample: the same scene and delay can end differently,
because traffic is sampled. In an earlier batch, one scene at 0 delay crashed
in 46 of 150 identical runs. So one run proves little; repeats at the same
setting are how a rate is estimated. A run **failed** if the ego hit something
with its front or side, or left the road.

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
- `goal` and `goal_status`: the study's win condition, which code checks
  after every round, and where it stands (null when the study has none). The
  study stops when it is met, so spend runs on what it still lacks.
- `round`, `rounds`, `runs_this_round`: where the study is and how many runs
  to propose now.

## The answer

Exactly `runs_this_round` runs, each a `scene_id`, a value for every knob in
`knobs`, and a one-sentence `why`, plus a short `plan` for the study.
Repeating a setting is allowed and often right. A proposed run with a scene
outside `candidates`, a knob value outside its `values`, or any other key is
dropped, not run.

Spend runs where they change what the study can conclude: settings whose
failure rate is most uncertain, and settings near where a scene starts to fail.
Settings that already failed or passed many times teach little more. Every
other scenario knob stays at its unperturbed value (0).
