# While you were away (8-13 Oct)

**13 Oct evening, after the meeting:** everything from Dr. Shao's feedback is
in `CHECKLIST.md`, item by item. The finding that needs you: problem 31
(retimed cars freeze in their lane; the AI search learned to hit them).

Short version for Will. Every number has its source in `FACTS.md`; the day
by day is in `LOG.md`. Live results: `research/simgate serve` (Results tab),
`METHODS.md`, `GATE.md`, `DRIFT.md`, `HZ.md`, `WHERE.md`, `CLOSED.md`.

## 11-13 Oct: the studies again at 2 Hz, and two scoring fixes

1. **At 2 Hz the policy fails less, and no method finds 5 hardest cases.**
   You said to use the free GPU; I re-ran all three studies with VaVAM
   planning every 500 ms, its training rhythm (finding 1 below), with the
   same methods plus `rules_v3` (rules starting at the recording). First
   replicate, hardest cases confirmed of 5:

   | study | rules | rules_v3 | hybrid | llm | random + confirmation |
   |---|---|---|---|---|---|
   | pedestrian x ego speed | 4 | 4 | 4 | 4 | 4 |
   | cut-in | 2 | 0 | 3 | 3 | 4 |
   | lead vehicle | 0 | 0 | 1 | 5 (in 46 runs) | 1 |

   llm on lead vehicle is the only arm at 2 Hz that reaches 5: it is the
   only one that slowed the lead car to half speed and shifted its timing.
   One of its five is not a fair failure, though: the warm-up left the ego
   0.5 m behind a lead car closing at 4 m/s, which no braking could stop.
   Without that case it is 4.

   Run on the same settings at both rates, pedestrian x ego speed fails
   far less at 2 Hz: of 63 settings, 17 fail at both rates, 17 only at
   10 Hz, 2 only at 2 Hz (p 0.0007), and the drift at 5 s halves (+1.9 m
   against +3.9 m). Two scenes that crash every time as recorded at 10 Hz
   pass at 2 Hz. At 2 Hz there are 6 hard pedestrian scenes; every method
   found 4 of them, and which 4 depends on the method: the rule methods
   and hybrid find the ones that fail as recorded; llm only finds the ones
   that need a faster ego. So at 2 Hz ego speed matters more. `HZ.md`,
   `WHERE.md`.
2. **The 10 Hz method table changed** (finding 6, now final): a crash that
   had already started before the policy took over no longer counts
   (problem 30). Lead vehicle llm's earlier win (23-30 runs) came from those:
   a lead car slowed to 0.5x met the ego while the ego was still replaying
   the human's drive. With the fix, no method reaches 5 on lead vehicle or
   cut-in. On pedestrian x ego speed every method still does. At 2 Hz the
   same thing happens one step later (poses every 500 ms), so the hand-off
   step itself now counts as warm-up. The arms that had stopped early were
   re-run to their full budget.
3. **Replayed cars running into the ego are mostly covered by fix 2**
   (problem 29, `CLOSED.md`). A replayed car cannot react, so it can
   drive into an ego braking in its own lane. I wrote a check for this
   from the car positions. It first flagged 49 cut-in crashes, but almost
   all were crashes already under way at the hand-off, which fix 2 now
   ignores. On what is left, at 10 Hz none are of this kind, and the
   method table is unchanged. At 2 Hz there are 6 on cut-in, and they lower
   random + confirmation from 4 to 3. The failure definition is
   unchanged; `CLOSED.md` has the tables both ways.
4. **The warm-up seam fix works in a real run** (problem 24): the scene
   that halted at 1.2x now passes the gate at all five speeds (peak
   3.7 m/s^2, was 10.7).
5. **One new robustness issue** (problem 28): the archive step crashed once
   at exit after saving its run. Re-running it now recognizes the saved
   run, and the study continued.

**Queue (13 Oct 20:00 UTC):** every 2 Hz replicate finished overnight
(table in FACTS "2 Hz complete"). Pooled over cut-in and lead vehicle at
both rates: rules 10 of 60 confirmed, hybrid 33, llm 32, random +
confirmation 19. Now running: `optuna_confirm` (Optuna with the same
confirmation as random) at 10 Hz on the three studies, 3 replicates, about
4 hours. Plan to the 24 Oct freeze: `OUTLINE.md`.

**Report files:** the `report.md` of an arm that finished before 12 Oct
15:37 UTC gives its goal under the old count; `METHODS.md` and FACTS use
the fix.

## What needs you

- **Which rate the paper uses.** 2 Hz is VaVAM's own rhythm and drifts
  half as much, so its failures are more fairly the policy's; 10 Hz has
  three full replicates. My suggestion: 10 Hz for the method comparison,
  with 2 Hz as the check that the ranking holds (replicates 2 and 3 are
  queued).
- **Whether a replayed car running into the ego counts** (problem 29).
  It is left counted for now; `CLOSED.md` has both tables.
- **A slowed lead car meets the ego in the warm-up** (problem 30). The
  scoring now ignores that crash. Keeping the lead car clear until the
  hand-off would need a change to the retiming in alpasim `src/`, so I
  left it to you.
- feasible_best's gains (finding 5 below).
- `patches/alpasim-src.diff` is from 29 Sep and lacks the retiming and seed
  hooks; refreshing it would also publish your uncommitted src edits,
  including the 7 files the formatter touched on 7 Oct (reconstructions in
  `~/alpasim_format_restore_7oct/`). Your call.
- A license for the repo before the OSS push.

## 8-10 Oct

### What we found

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
6. **Which search method is fastest depends on the space, and on lead
   vehicle and cut-in none reaches the goal.** Three replicates per method,
   every arm run to its full budget, scored with the 12 Oct fix (a contact
   already under way when the policy takes over is not the policy's, FACTS
   problem 30). Hardest 5 confirmed: runs to the goal, or how many found.

   | study | rules | hybrid | llm | random + confirmation |
   |---|---|---|---|---|
   | pedestrian x ego speed (2 knobs) | 25, 25, 25 | 24, 28, 24 | 28, 40, 37 | 31, 32, 32 |
   | lead vehicle (3 knobs) | 0, 0, 0 of 5 | 2, 3, 3 of 5 | 3, 1, 3 of 5 | 4, 1, 2 of 5 |
   | cut-in (2 knobs, 9 scenes) | 2, 2, 2 of 5 | 4, goal at 48, 4 of 5 | 3, 4, 3 of 5 | 3, 0, 1 of 5 |

   Plain random never confirms anything. In the small space every method
   reaches the goal (rules most consistent). In the larger ones none does;
   rules alone are the weakest, hybrid is about one case ahead on cut-in,
   and on lead vehicle no method is ahead across replicates. **This
   replaces the 10 Oct table**, where llm "won" lead vehicle in 23-30 runs:
   70 of its 74 failures were a lead car slowed to 0.5x that the ego met
   during the warm-up, while it still replayed the human's path, and was
   still touching when the policy took over. **Why a method does well**
   (`WHERE.md`): where its starting guess matches where failures sit. Rules
   start at the middle of every knob's range: the recording on pedestrian
   (hard there), two settings they confirm on cut-in, and a faster lead car
   on lead vehicle (easy). On cut-in hybrid stays near the recording, where
   the hard cases are. Replayed cars running into the ego (`CLOSED.md`,
   problem 29) do not change this table (point 3 above).
7. **Replays are exact** (same seed, 0.0 m over 122 steps) and **the ego
   speed knob works** (measured within 0.004 m/s of the request).

### What got built

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

### Decisions I made (tell me if you disagree)

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
