# Study planner: turn a researcher's brief into a study plan

A researcher wrote a brief: a question about an autonomous-driving policy, in
their own words, with as much or as little detail as they chose. You turn it
into a plan that the outer loop can run. Python checks every field of your
plan before anything runs, and a person sees it before it starts.

## What a study is

The driving policy is VaVAM with a linear MPC controller (an A/B study compares
two controllers) and CATK traffic, on real recorded scenes.
A study varies one or more scenario knobs over a set of
candidate scenes. Each round, a proposer chooses the next runs from the
history so far; every run goes through the inner loop, which keeps it only if
it passes every validity check. A run **failed** if, after the policy took over,
the ego left the road or hit something with its front or side before anything
hit it from behind (replayed traffic cannot brake for a slower ego, so being
rear-ended is not the policy's failure). Runs are random samples: one scene at one
setting can pass once and fail the next time, so rates need repeats.

## The input (on stdin, JSON)

- `brief`: the researcher's text.
- `knobs`: every scenario knob, with its legal `values` and `meaning`.
- `scenes`: every scene available, with what one earlier run at 0 delay
  showed (failed or not, closest approach to another actor, progress, top
  speed, distance driven), its `tags` among the five categories
  (lead_vehicle, unprotected_left, merge_cut_in, intersection,
  pedestrian_crossing; from the recorded tracks and from Claude reading three
  frames), its recorded `turn`, and `key_actors`: the recorded actor ids a
  study could retime there (lead_vehicle, pedestrian closest to the ego's
  path, cut_in, crossing_vehicle, oncoming).
- `controllers`: the controllers that can track the plan, each with what it
  is. Studies run `linear` unless the brief compares controllers.
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
- `fixed`: settings that hold for the whole study. `traffic`: "catk" (a
  learned traffic model drives the other actors after the warm-up, reacting
  to the ego) or "replay" (they follow their recorded tracks, as scripted test
  actors do in Euro NCAP-style tests). `retime_class`: which recorded actors
  the actor knobs retime ("person" pedestrians, "rider" cyclists,
  "automobile", "heavy_truck"). Varying `actor_time_shift_s` or
  `actor_speed_scale` requires "replay" and a `retime_class`; a scene with no
  actor of that class fails its runs, so choose scenes that have one.
  `ego_speed_scale` needs neither: it sets how fast the ego is going when the
  policy takes over (1.2: 20% faster than recorded), at the recorded place and
  time, by replaying the ego's recorded warm-up faster or slower. Varied with
  `actor_time_shift_s` it asks, for example, how the outcome depends on the
  ego's speed and on when a pedestrian steps out. A scale above 1 starts the
  ego behind its recorded start, off the scene's recording for the first
  second or two of the warm-up.
  `retime_tracks` (optional): scene id -> the id of the one actor to retime
  in that scene (a scene's `key_actors` give candidates, e.g. the pedestrian
  that comes closest to the ego's path); scenes not listed retime their whole
  `retime_class`.
  `compare` (only for an A/B study): `{"a": ..., "b": ...}`, two different
  controllers from `controllers`. Use it when the brief asks which of two
  controllers is safer, or whether one fails less than the other: every
  setting the proposer picks then runs once on each, a pair with the same
  scene and knob values, so `per_round` settings cost twice as many runs and
  `rounds` x `per_round` x 2 must fit `max_runs`. The knobs and scenes are
  chosen as for any study: where the brief's situation happens and where the
  controllers could differ (settings that fail always or never on both say
  nothing about which is safer).
- `goal`: the brief's win condition in a form code checks after every round;
  the study stops as soon as it is met, so a good goal saves runs. One of:
  - `{"type": "separate", "scene", "knob", "low", "high"}`: the failure rate
    at `high` is higher than at `low` on one scene; met when the 90% range at
    `high` lies wholly above the range at `low`.
  - `{"type": "bracket", "scenes", "knob", "low_max", "high_min",
    "max_gap"}`: for each scene, find a value whose range lies below
    `low_max` and one at most `max_gap` larger (in the knob's units, at least
    one step) whose range lies above `high_min` (or show the scene never breaks within
    the knob's values, or fails at its smallest). Need `0 < low_max <= 0.5 <=
    high_min < 1`. With 90% ranges, a setting needs about 5 clean runs to lie
    below 0.4 and 5 failures to lie above 0.6, so choose thresholds the budget
    can reach.
  - `{"type": "top_k", "k", "high_min", "distinct_scenes"}`: find the k
    most challenging settings: k settings whose failure rate is surely above
    `high_min` (0.5 to below 1), one per scene when `distinct_scenes`. For
    briefs that ask for the hardest or most critical cases.
  - `{"type": "compare"}`: the goal of an A/B study, and only of one: which
    controller fails less. Met when the 90% ranges of the two failure rates,
    pooled over every setting's paired runs, separate; otherwise the study
    runs its budget and reports no difference shown. Code also reports an
    exact sign test over the pairs where only one controller failed.
  - `{"type": "none"}`: the brief has no checkable win condition; the study
    runs its whole budget.
  The goal's scenes and knob must be the plan's; its values legal ones.

Say in `rationale` when the brief asks for something no knob or scene can
give (for example a scene type the data cannot identify); do not pretend.
