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
   view). This is the dominant failure mode: most "hardest cases" are this
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
6. **Replays are exact** (same seed, 0.0 m over 122 steps) and **the ego
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
- Mirror test set up in a second checkout (`~/alpasim-mirror`), queued after
  the replicates (`research/simgate front m1_queue` to run it sooner).

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
