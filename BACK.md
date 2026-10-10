# While you were away (8-9 Oct)

Short version for Will. Every number has its source in `FACTS.md`; the day
by day is in `LOG.md`. Live results: `research/simgate serve` (Results tab),
`METHODS.md`, `GATE.md`, `DRIFT.md`.

## What we found

1. **The policy drifts left.** Once VaVAM takes over, the car moves left of
   where the human drove: about one lane within 5 s, in 88% of 853 runs (1%
   drift right). Its plans already lean left before it drives (open loop,
   median +0.2 m). It has been there since the first batches in September
   and with fresh frames. No integration bug found (command rule and
   encoding match VaVAM's training code; camera centred, right field of
   view). **The mirror test settles where it comes from:** with VaVAM's
   input and output mirrored, the same scenes and seeds drift *right* (18
   of 20 pairs, median -2.1 m against +6.4 m plain). The lean is in the
   model itself, not the simulator, the controller or the traffic side.
   `MIRROR.md`. **It is documented that VaVAM is weak in AlpaSim** (ECO,
   arXiv 2609.31383: scene score 11.0, 18% at-fault collisions, 28%
   off-road, in the 4 m corridor 57.6% of the time), but not why; our lean
   finding appears new. **Our 10 Hz loop doubles the drift:** at VaVAM's
   own 2 Hz rhythm the same runs drift +3.0 m instead of +6.4 m and crash 4
   times instead of 6. New studies should plan at 2 Hz
   (`control_timestep_us: 500000`); the running replicates stay at 10 Hz
   so they compare like for like. This is the dominant failure mode: most "hardest cases" are this
   drift meeting traffic or the road edge. `figures/drift.png`, `DRIFT.md`.
2. **We were over-counting failures by a quarter.** 49 of 200 counted
   crashes were replayed cars rear-ending our slowed ego, or contacts before
   the policy took over. A failure now counts only if it is the policy's,
   after hand-off (AlpaSim's own warm-up filter, nuPlan's rear rule). The
   pedestrian x ego speed result survives; cut-in and lead vehicle shrank.
3. **Ego speed is the stressor** (Shao's idea). Pedestrian timing alone:
   0-5 failures in 49 runs per method. With the ego's speed: every method
   confirms 5 hardest cases in 24-31 runs.
4. **The rule proposer had a real bug.** It kept confirming near misses that
   never fail until the budget ran out (lead vehicle: 0 failures in 49
   runs), while random + confirmation found 5 cases at knob extremes in 43.
   `rules_v2` stops confirming what surely passes, but still searched
   locally and also found 0 of 5. Reading: rule-guided local search is
   reliable in small spaces (pedestrian x ego speed: rules at 25 runs in
   both replicates) and needs global coverage first in larger ones. I did
   not keep tuning rule variants on lead vehicle (that would fit the method
   to its test); FACTS problem 26 and "Rule variants".
5. **Your feasible_best tuning breaks these scenes.** A/B over 4 settings and
   4 scenes: linear 0 of 10 failed, feasible_best 10 of 10 (p 0.002), none
   involving the pedestrian: it turns too sharply or veers off at RIGHT
   commands. Worth checking its gains, or the uncommitted configuration.py.
6. **Which search method is fastest depends on the space** (replicates so
   far, `METHODS.md`): pedestrian x ego speed (2 knobs, three replicates
   each, complete) hybrid 24/28/24, rules 25/25/25, random + confirmation
   31/32/32, llm 28/40/37 runs to the goal; lead
   vehicle (3 knobs, failures at the extremes) llm 5 of 5 by runs 23 and
   30 (two clean replicates), random + confirmation 5 by 43, then 4 and 3 of 5,
   hybrid 2, 3 and 3 of 5, rules 0, 0 and 0; cut-in (clean replicates only) hybrid 5 of 5 by
   runs 32 and 36, llm 4 and 4 of 5, random + confirmation 3, 3 and 2 of 5, rules 2 and 2 of 5 in 54. Plain random
   never confirms anything. Where the space is small every method does
   about as well; where it is large, the Claude methods find the hardest
   cases first. More replicates are running.
7. **Replays are exact** (same seed, 0.0 m over 122 steps) and **the ego
   speed knob works** (measured within 0.004 m/s of the request).

## What got built

- `research/simgate`: one command (`serve`, `worker`, `new`, `plan`,
  `queue`, `status`, `front`, `batch`, `export`, `doctor`) and a local web
  app: write a brief, see the plan and its checks, queue it, watch results
  (Studies, Results, Queue, Activity). A read-only snapshot in `site/`.
- Fair comparison: `random_confirm` baseline, replicates (`--replicate`),
  `rules_v2`, compare goals need coverage, analyses that count only
  finished arms (`analyze_methods.py`).
- Analyses: `gate_report.py`, `gallery.py` (hardest cases with frames),
  `drift_analysis.py`, `command_analysis.py`; figures `framework.png`,
  `drift.png`, `methods_*.png`, `gallery_*.png`.
- Open source: new README, CI on GitHub (all tests pass in a fresh
  environment), `simgate doctor`, problems 20-26 in FACTS for the paper's
  "issues met" table.

## Decisions I made (tell me if you disagree)

- New failure definition (above); old reading kept as `failed_any`.
- Kept `rules` and `hybrid` unchanged mid-experiment; fixes go in new arms.
- Left the warm-up seam fix (problem 24) unapplied until the replicates end,
  so they all see the same warm-up: `patches/pending-ego-retiming-seam.patch`.
- Mirror test in a second checkout (`~/alpasim-mirror`, your working copy
  untouched); run on 9 Oct after you said to cut the intersection
  replicates (~10 GPU hours saved).

## What needs you

- feasible_best's gains (finding 5).
- `patches/alpasim-src.diff` is from 29 Sep and lacks the retiming and seed
  hooks; refreshing it would also publish your uncommitted src edits,
  including the 7 files the formatter touched on 7 Oct (reconstructions in
  `~/alpasim_format_restore_7oct/`). Your call.
- A license for the repo before the OSS push.

## Still running

The GPU queue (two runs at a time, ~39 runs an hour): replicates 2-4 of
rules, hybrid, llm and random_confirm on the studies with failures, then
the mirror test. `research/simgate status` or the Queue tab.
