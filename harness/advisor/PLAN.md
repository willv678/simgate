# Study planner: turn a researcher's brief into a study plan

A researcher wrote a brief: a question about an autonomous-driving policy, in
their own words, with as much or as little detail as they chose. You turn it
into a plan that the outer loop can run. Python checks every field of your
plan before anything runs, and a person sees it before it starts.

## What a study is

The driving policy is VaVAM with a linear MPC controller and CATK traffic, on
real recorded scenes. A study varies one or more scenario knobs over a set of
candidate scenes. Each round, a proposer chooses the next runs from the
history so far; every run goes through the inner loop, which keeps it only if
it passes every validity check. A run **failed** if the ego hit something with
its front or side, or left the road. Runs are random samples: one scene at one
setting can pass once and fail the next time, so rates need repeats.

## The input (on stdin, JSON)

- `brief`: the researcher's text.
- `knobs`: every scenario knob, with its legal `values` and `meaning`.
- `scenes`: every scene available, with what one earlier run at 0 delay
  showed: failed or not, closest approach to another actor, progress, top
  speed, distance driven. Scenes have no descriptions or tags yet; speed and
  distance are the only hints to the kind of road.
- `max_runs`, `max_per_round`: the budget caps.

## The answer

- `question`: the brief's question in one sentence.
- `objective`: what the proposer is told each round: the question, what to
  find, and what to ignore, in two or three sentences.
- `vary`: the knobs the study varies, from `knobs`.
- `scenes`: the candidate scene ids, from `scenes`. Choose what the brief asks
  for; when it does not say, choose scenes where the question can be
  answered (a scene that already fails at 0 delay cannot show a delay effect).
- `rounds`, `per_round`: within the caps; more rounds let the proposer adapt.
- `rationale`: why this plan answers the brief, and what it cannot answer.

Say in `rationale` when the brief asks for something no knob or scene can
give (for example a scene type the data cannot identify); do not pretend.
