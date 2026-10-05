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
- Invalid runs kept, every C1 arm: **25 with no gate → 10 with the per-run gate
  → 0 with the audit.** C2 (physics on): 25 → 0–1 → 0.
- C1, live: script 35 valid kept in 80 launches; **tier 1 35 in 72**; tier 0 25
  in 62. Tier 0 gave up on 10 recoverable runs (deleted or corrupt metrics,
  exit 0): tools matter when the log hides the cause, now shown live.
- Physics bounds on fresh runs: 25/30 silent faults caught, **0 of 95** false
  alarms in C1. The Auditor caught the other 5, so 30/30 together.
- Griffin's exploration (`griffin/ideas.md`): a 1.0 m lateral-bias fault passes
  every physics bound while `offroad` and `wrong_lane` stay 0.

**Problems found**
- The tier 1 arm of C2 stopped at run 32 of 50: `monitor.py` aborted in native
  code (exit -6, once in about 300 monitor calls). Resumed from where it
  stopped.
- One live physics false alarm in C2: the contact check used centre distances
  and a rough lane width, and fired on a near-miss the simulator measured at
  0.21 m apart. Being fixed with real vehicle boxes.
- With physics on, the script's blind retries keep more silent-fault runs than
  the models, because our injected faults do not repeat on a retry. A property
  of the fault design that the paper has to state.

**Next**
- Finish C2 tier 1, regenerate the report, and replace the replay-based
  diagnosis figure with live campaign figures.
- Box-based contact check; recalibrate.
- Griffin's lateral-bias fault: the first fault that beats every check.

**Slides**
1. Campaign design: one fault plan, three policies, physics off and on.
2. 25 → 10 → 0 in every arm (new figure).
3. Script vs tier 1 vs tier 0: valid kept, launches, halts.
4. Physics on fresh runs: 25/30 alone, 30/30 with the Auditor, 0 false alarms in C1.
5. What broke: the monitor abort, the contact false alarm, the retry caveat.

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
