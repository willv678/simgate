# While you were away (8-10 Oct)

Short version for Will. Every number has its source in `FACTS.md`; the day
by day is in `LOG.md`. Live results: `research/simgate serve` (Results tab),
`METHODS.md`, `GATE.md`, `DRIFT.md`.

## What we found

1. **The policy drifts left.** Once VaVAM takes over, the car moves left of
   where the human drove: median 2.4 m within 5 s; 88% of all 2428 kept
   study runs are more than 0.5 m left by then, none right. Its plans already lean left before it drives (open loop,
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
6. **Which search method is fastest depends on the space.** All
   replicates are done (three clean ones per method and study,
   `METHODS.md`). Hardest 5 confirmed, runs to the goal or count found:

   | study | rules | hybrid | llm | random + confirmation |
   |---|---|---|---|---|
   | pedestrian x ego speed (2 knobs) | 25, 25, 25 | 24, 28, 24 | 28, 40, 37 | 31, 32, 32 |
   | lead vehicle (3 knobs) | 0, 0, 0 of 5 | 2, 3, 3 of 5 | 23, 30, 23 | 43, 4 of 5, 3 of 5 |
   | cut-in (2 knobs, 9 scenes) | 2, 2, 2 of 5 | 32, 36, 46 | 4 of 5, 4 of 5, 47 | 3, 3, 2 of 5 |

   Plain random never confirms anything. In the small space every method
   does about as well (rules most consistent). In the larger ones a Claude
   method wins every replicate, but not the same one: free llm on lead
   vehicle (failures at the knob extremes), hybrid on cut-in. **Why** (`WHERE.md`): a
   method wins where its starting guess matches where failures sit. The
   rules start at the middle of every knob's range, which is the recording
   on pedestrian (hard there), the 2 settings they confirm on cut-in, and on
   lead vehicle a *faster* lead car (easy): 100% of their runs there, 0 of 6
   hard scenes touched. llm read the brief ("slower lead = harder stop") and
   ran 100% at 0.5x. On cut-in the hard cases sit 1-2 steps from the
   recording; hybrid stays close (45% of runs on hard settings), llm finds
   all 6 hard scenes but spreads too thin to confirm 5. Rules alone never reach the goal there.
   **Caveat found 12 Oct (`CLOSED.md`, FACTS problem 29):** 49 of cut-in's
   208 counted crashes are a replayed car (which cannot react) running into
   an ego braking in its own lane, first touching its front corner, so the
   rear-end rule kept them. Without those, no method reaches 5 on cut-in
   (hybrid 3, 3, 3; llm 3, 4, 3). Pedestrian and lead vehicle do not change.
   So hybrid's cut-in win should be reported with this caveat or rerun.
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
- Held the warm-up seam fix (problem 24) until the replicates ended, so
  they all saw the same warm-up; applied to your checkout on 10 Oct
  (`src/runtime/alpasim_runtime/ego_retiming.py` and its test, 14 tests
  pass; originals in `~/alpasim_seam_backup_10oct/`, undo with
  `git apply -R research/patches/pending-ego-retiming-seam.patch`).
  Re-checked in a simulation on 12 Oct: the scene that halted at 1.2x now
  passes the gate at every speed (peak 3.7 m/s^2, was 10.7).
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

## Queue

Empty since 10 Oct 20:29 UTC; the GPU is free. Next studies should plan at
2 Hz (`control_timestep_us: 500000`, finding 1). `research/simgate status`
or the Queue tab.
