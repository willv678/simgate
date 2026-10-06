# Weekly

What got done each week, written so it can become the weekly slides. Newest
week first. Every number has its source in `FACTS.md`; daily detail is in
`LOG.md`. Update the current week as work lands; start a new section on Monday.

---

## Week of 5 Oct (in progress)

**Headline:** the full campaign is in. SimGate's guarantee held in every arm,
and tier 1 matched the script's yield with fewer wasted launches.

**Done**
- Campaign results analysed (`harness/campaign_report.txt`). Six arms: C1
  (physics off) and C2 (physics on) × script, tier 1, tier 0; 50 planned runs
  each.
- Invalid runs kept, all six arms: **0 after gate + audit.** Summed per
  campaign: C1 (physics off) 75 → 30 → 0; C2 (physics on) 75 → 4 → 0.
- C2 tier 1 finished after the resume: 36 valid kept in 72 launches.
- C1, live: script 35 valid kept in 80 launches; **tier 1 35 in 72**; tier 0 25
  in 62. Tier 0 gave up on 10 recoverable runs (deleted or corrupt metrics,
  exit 0): tools matter when the log hides the cause, now shown live.
- Physics bounds on fresh runs: 25/30 silent faults caught, **0 of 95** false
  alarms in C1. The Auditor caught the other 5, so 30/30 together.
- Griffin's exploration (`griffin/ideas.md`): a 1.0 m lateral-bias fault passes
  every physics bound while `offroad` and `wrong_lane` stay 0.
- Physics contact check rebuilt on real vehicle boxes: 0 false alarms on 256
  clean runs (was 1 live false alarm in C2).
- Live campaign figures: `figures/campaign_invalid.pdf`,
  `figures/campaign_outcomes.pdf` (replace the replay-based diagnosis chart).
- Griffin's plan faults added (lateral bias, plan freeze, waypoint noise, using
  AlpaSim's own hook). First batch failed at config (Hydra needs `+` for a
  block the base config lacks); tier 1 halted each at its first failure.
  Fixed and rerun as g2: the first lateral-bias run passed the full gate,
  physics included, and was kept. Griffin's finding holds live.
- C3 queued overnight after g2: seed 3, physics on, silent faults persistent.

- Night of 5–6 Oct:
  - **Plan faults are the hard case.** Lateral bias and plan freeze pass every
    physics bound and the gate keeps them; the Auditor with configs hidden
    caught 0/8 (it is told not to flag bad driving, and a corrupted plan looks
    like bad driving).
  - **New K⁺ check: did the controller track the driver's plan?** The log has
    both plans; after the warm-up they are identical in a clean run. Median
    sideways gap: 0–0.008 m on 258 clean runs, 0.14–1.0 m on all 8 plan
    faults. Given that number, the Auditor caught 8/8 with a reference per
    scene (0 false flags).
  - Batch audits now use one clean reference per scene automatically.
  - The Auditor's rule "fault injection must not be enabled" is now
    admissible (8/8 caught, 0/51 clean).
  - The monitor records the machine before stopping a timed-out run: on hangs
    both tiers had misdiagnosed (blamed slowness) because stopping the run
    erased the paused container.
  - Safety for overnight runs: a crashed read-only script is rerun once and
    logged, instead of stopping the arm.
  - **Paper draft v0** (`paper/main.tex`, Overleaf-ready), with Figure 1 drawn.
  - Hidden simulator retries measured: 1 of 496 kept runs.
  - **C3 script arm done** (persistent silent faults): 35 valid kept in 95
    launches; the gate kept 3 invalid runs (all kinematic) and the audit
    quarantined all 3, so 0 after the audit. Persistent rails cost the script
    15 launches and 5 budget halts. Tier 1 and tier 0 arms running.
  - **Why physics misses some kinematic runs:** on gentle scenes they peak
    under the acceleration bound, and no jerk statistic separates them from
    one jerky clean highway run (`jerk_separation.txt`, 687 runs). That fault
    needs the Auditor's config and per-scene reference, which is why there
    are two layers.
  - **Citations verified** against their sources: 17/18 exact, PlannerForge
    awaiting EMNLP pages. Seven entries had wrong or incomplete titles or
    authors.
  - Campaign report and figure pick up C3 as its arms finish.

**Problems found**
- The tier 1 arm of C2 stopped at run 32 of 50: `monitor.py` aborted in native
  code (exit -6, once in about 300 monitor calls). Resumed from where it
  stopped.
- One live physics false alarm in C2: the contact check used centre distances
  and a rough lane width, and fired on a near-miss the simulator measured at
  0.21 m apart. Fixed with real vehicle boxes; a first version double-counted
  the ego's rear-axle offset and made 37 false contacts before the frame was
  checked against the log.
- With physics on, the script's blind retries keep more silent-fault runs than
  the models, because our injected faults do not repeat on a retry. A property
  of the fault design that the paper has to state.

**Next**
- C3 overnight: seed 3, physics on, silent faults persistent (as a config
  error would be).
- Griffin's lateral-bias fault: the first fault that beats every check.

**Slides**
0. Draft v0 exists; what is pending (C3, g3, citations).
1. Campaign design: one fault plan, three policies, physics off and on.
2. 25 → 10 → 0 in every arm (new figure).
3. Script vs tier 1 vs tier 0: valid kept, launches, halts.
4. Physics on fresh runs: 25/30 alone, 30/30 with the Auditor, 0 false alarms in C1.
5. The hard case: plan faults, and the plan-handoff check (0 → 8/8).
6. What broke: the monitor abort, the contact false alarm, the retry caveat,
   evidence erased by our own timeout.

---

## Week of 28 Sep

**Headline:** SimGate went from a design to a measured system: the model
proposes, the gate decides, and what the model learns becomes code.

**Done**
- Mon: Shao's state machine built (`loop.py`): Python owns the loop, Claude is
  called only on FAILED. B2: 150 runs unattended in 9 h, 150 kept; the only
  failures were a Docker network leak.
- Tue: machine check and CLEANUP_ENV; tier 1 Investigator with read-only tools
  (fence: 5/5 forbidden actions denied); tier 2 Auditor (46/46 planted lies,
  0 false flags, same result three times); rule mining (a learned rule caught
  the batch the Auditor missed, 10/10, no model); the Verifier (found a real
  hole, now 0 violations over 3,822 transitions); eight fault injectors and the
  pilot campaign; physics checks after Shao's meeting.
- Tue: named the system **SimGate** (Gate, Investigator, Auditor, Rulebook,
  Verifier); `GUIDE.md` and `SLIDES.md`; repo renamed to `simgate`.
- Wed: campaigns C1 and C2 ran unattended (about 30 h of GPU).
- Fri: Griffin's exploration day.

**Results** (`FACTS.md`)
- Pilot: invalid runs kept 9 → 6 → 0 (`figures/invalid_kept.pdf`).
- Diagnosis replay: script 4/6, tier 0 19/30, tier 1 24/30 (`figures/diagnosis.pdf`).
- Auditor blind spot: a batch wrong the same way throughout (0/10); one
  reference run fixes it (10/10).
- Physics bounds: 0 false alarms on 233 clean runs, 6/6 silent faults, no config
  read. Auditor with configs hidden: 6/6 with the motion, 3/6 without.

**Problems found**
- The Docker network leak (29 networks) broke B2's first 8 runs and the same
  leak was in the old autolab batch.
- The Verifier's hole: CONFIGURE of the delay let a recovery keep a run
  measuring the wrong condition. The delay is no longer configurable.
- A jerk bound fired on clean highway runs and was dropped.
- The simulator retries crashed rollouts inside one run, unseen by the gate.

**Slides**
1. Unattended runs lie: our four lies.
2. SimGate: Simplex for AI agents; the five parts.
3. The Verifier found a hole.
4. 9 → 6 → 0; the Auditor's 46/46 and its blind spot.
5. Physics: when the numbers look fine.
