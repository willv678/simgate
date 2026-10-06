# Outer loop: choose the next runs of a study

Python runs the study. Each round it calls you once, with `claude -p` and no
tools, to choose the next runs; then it checks every run you propose, queues
the legal ones, and runs them through the inner loop, which keeps a run only
if it passes every check (exit code, metrics, the requested settings landed,
physics, the batch audit). You never launch or keep anything.

## The study

The driving policy is VaVAM with a linear MPC controller and CATK traffic, on
real recorded scenes. The question: **how does the policy's failure rate on
each candidate scene grow with planner delay** (the time between a camera frame
and the controller receiving the plan made from it)? AV teams want to know
which scenes are fragile to latency and roughly where each breaks.

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
- `delays_us`: the delays you may choose.
- `history`: every run of this study so far: scene, delay, `failed`, and the
  gate's verdict (`kept`, or why not). Only kept runs are evidence.
- `round`, `rounds`, `runs_this_round`: where the study is and how many runs
  to propose now.

## The answer

Exactly `runs_this_round` runs, each a `scene_id`, a `planner_delay_us`, and a
one-sentence `why`, plus a short `plan` for the study. Repeating a setting is
allowed and often right. A proposed run with a scene outside `candidates`, a
delay outside `delays_us`, or any other key is dropped, not run.

Spend runs where they change what the study can conclude: settings whose
failure rate is most uncertain, and delays near where a scene starts to fail.
Settings that already failed or passed many times teach little more.
