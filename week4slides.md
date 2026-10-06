# Week 4 slides: 6 Oct meeting with Dr. Shao

About 10 slides. Paths are relative to `research/`. Use the `.png` figures
(`.pdf` versions exist for the paper). Numbers are from `FACTS.md`.

---

## 1. From a gate to an AV testing system

**On slide**
- Last week: the inner loop (preflight K⁻, run, postflight K⁺, Claude on FAILED).
- This week: the **outer loop**. A researcher asks a question; the system designs
  the tests, runs them, checks every result is valid, and answers with evidence.
- One principle at every layer: **the model proposes, code decides.**

**Image:** a simple diagram you draw in the slide tool, left to right:
`brief.md → plan → outer loop (rounds) → inner loop (gate) → triage → report.md`.
Colour the Claude steps orange and the code steps blue, the same scheme as
`figures/architecture.png`.

**Say:** "Last week I showed the state machine. This week it runs a whole
study from a question to an answer."

---

## 2. The input: a brief, like a test plan

**On slide:** a screenshot of `briefs/latency_budget.md`, with its Question,
Scope, Budget and What counts sections.

**Say:** "AV teams write test plans before a campaign: a question, a scope, a
budget, what counts as failure. The brief has the same shape, and it can be
one sentence or a page." (Don't claim it was validated with industry engineers;
that's a next step.)

---

## 3. Brief → plan (Claude), checked by code

**On slide:** the plan, from `studies/latency_budget/plan.json`
- 6 scenes that drive cleanly at 0 delay, from **2.6 to 30.4 m/s** (city to highway).
- Strategy: probe at 200 ms, bisect toward the break, repeat at the edge.
- 5 rounds × 6 = 30 runs.
- Its own limits: "a rough bracket, not a failure rate"; "road type cannot be
  identified."
- Code checks every field: knobs from the catalog, scenes that exist, at most
  60 runs and 10 per round.

**Say:** "It took 26 seconds. The plan is checked like a recovery is: illegal
knobs or an over-budget plan never run."

---

## 4. The outer loop in action (pilot o1)

**Image:** `figures/pilot_grid.png`, the left panel (Claude) only. Present it
as what the loop did, not as Claude beating random. Random is only a floor; the
real baselines next week are a grid sweep (status quo), Optuna, and an
expert-written bisection script, compared on runs needed to answer.

**On slide**
- Round 1: probe 200 ms on the clean scenes, plus repeat one odd baseline.
- Round 2: two scenes broke at 200 → bisect to 100; re-run 0 ms ("was the clean
  baseline luck?").
- Round 3: repeats at the edge, 150 ms ×2 and 100 ms again.
- Result: **02eadd92 holds at 100 ms and fails from 150 ms.**
- Random, same budget: never ran a 0 ms baseline, spread its runs thin, one wide
  bracket.

**Say:** "15 runs each, so this is a demo, not a ranking. What matters is the
behaviour: baselines first, bisect, repeat at the boundary, because outcomes are
random." Avoid "Claude found 3× more failures": some of its 10 come from a
scene that fails even at 0 delay.

---

## 5. Why repeats: outcomes are random

**On slide**
- One scene, one identical config, **150 runs: 46 crashes.** CATK traffic is
  sampled.
- VaVAM fails about a third of S1's 100 scenes at 0 delay (27% crash, 36%
  off-road).
- So the question is a **failure rate vs. delay**, with a confidence range, not
  "find one crash".

**Say (if asked why VaVAM is so bad):** it's a research-grade open model, the
closed loop compounds errors, our failure definition is strict, and we run one
low-resolution camera on a 12 GB GPU. The system under test can be any policy;
see the GPU ask on slide 10.

---

## 6. The inner loop: what makes each run trustworthy

**On slide**, in two columns.

**Decides (plain code, can reject a run)**
- Preflight: the config and the machine (leftover containers, network pool,
  GPU, disk).
- During the run: stops a frozen run when its log stops growing (it used to
  hold the GPU 10 min).
- Postflight: exit code, metrics, every requested setting actually landed.
- Physics from the run's own log: acceleration, yaw rate, speed consistency, on
  the recording the whole run, contact with no collision scored.
- **Plan age** equals the requested delay at every step; **plan offset** equals
  the requested perception shift (new today).
- Rules the Auditor learned and a person approved (slide 8).

**Explains (Claude, never decides)**
- Triage of failures, the batch Auditor, the report.

**Proof:** `figures/campaign_invalid.png`: C1–C3, nine arms, invalid runs kept
**225 → 40 → 0**, upper bound 1.3%.

---

## 7. The bug the outer loop found before it ran

**Image:** `figures/plan_age.png`

**On slide**
- The gate would have **rejected every delay experiment**: the plan-handoff
  check read 0.12–0.17 m against a 0.05 m bound.
- Cause: a delayed plan reaches the controller in the car's frame **from when
  the plan was made**. The check compared it with the newest plan, in the
  current frame.
- Fix: match each plan to its source by timestamp → 0.0001 m.
- New check, plan age: exactly the delay at every step (clean 0 ms over 589
  runs; frozen plan saw-tooth to 900 ms). It **proves from the log** that the
  delay was applied.
- Live in the pilot: 200 ms runs measured 200 ms at every step.

**Say:** "This is why the inner loop matters. An autonomous tester on a broken
gate would have reported nothing but failures."

---

## 8. The system learned a rule

**On slide**
- All three C3 audits **independently** proposed: "the controller must be the
  linear MPC."
- Admission: catches the flagged runs, fires on 0 of 51 clean runs.
- I approved it → it's in the gate (`harness/rules/promoted.json`). It now
  catches that fault on every run with no model.
- **AI proposes → data admits → person approves → code enforces.**

---

## 9. After the runs: why it failed, and the answer

**Image:** `figures/triage_example.png` (the frame Claude saw and its verdict)

**On slide**
- Triage: Claude reads frames around each crash and names the cause. o1's 10
  failures took 38 s: no brake for the car ahead 4, turned into another car 2,
  hit by another car 2, off-road 1, unclear 1.
- **All three 02eadd92 failures: late braking behind a car stopping at a red
  light**, which is what latency does.
- Failure validity: a crash far off the recorded path (>3.5 m) is flagged as
  possibly the simulator's.
- Report: the answer with **90% ranges**, and every number comes from code. When
  Claude miscounted once ("5 of 5" vs 4 of 4), code started rejecting counts in
  prose.

**Image (optional):** a screenshot of the Answer and Findings sections of
`studies/pilot_o1/report.md`.

---

## 10. Live right now: confirming the break

**On slide**
- Brief: `briefs/confirm_break_02eadd92.md`: "Does 02eadd92 break between
  100 and 150 ms? Win condition: the 90% ranges no longer overlap."
- The planner flagged the statistics itself: Wilson ranges separate at 4/4 vs
  0/4, while stricter Clopper–Pearson needs the pilot runs pooled in.
- **RESULT: not confirmed.** 150 ms: every run crashed (4 of 4, rate 60–100%).
  100 ms: 2 of 4 crashed (rate 18–82%), both over 3.5 m off the recorded path,
  so possibly the simulator's. The ranges overlap, so the win condition is not
  met. The crash type also changes: side contact at 100 ms, rear-ending at
  150 ms. (`studies/confirm_break_02eadd92/report.md`)

**Say:** "This morning's pilot suggested a clean break from 1–2 runs per
setting. I asked the system to confirm it with 90% confidence. It ran 8 more,
said *not confirmed*, flagged the doubtful failures, and listed what would
settle it. It won't let me fool myself."

---

## 11. Next and asks

**Next two weeks**
- Many rollouts per launch, for about 3× the evidence per GPU-hour.
- Stop when the question is answered, not when the budget runs out.
- Scene tags from logs and video, so a brief can say "intersections with
  pedestrians".
- A/B mode ("is checkpoint B safer than A?") and memory across studies, which
  gives regression testing.
- Exact replay of a failure: needs the traffic model to honour its seed, which
  would be an AlpaSim contribution.
- Design rule: **no knob without a measurement.**

**Ask: a bigger GPU.** We're on 12 GB: one weak research policy at ~15
runs/hour. NVIDIA's Alpamayo models, which AlpaSim targets, need ~40 GB. A
48–80 GB card would let us show the method on a second, stronger policy and
run repeats several times faster.

**Found today, testing tonight:** our harness runs VaVAM with 100 ms control
steps, while AlpaSim's VaVAM config uses 500 ms with camera and control in sync.
The ~30% baseline failure rate may be partly our setup. The gate checks that
settings *landed*; this is a new class of check: are they *right for the
policy*. The 30-run latency study waits for this check. g3 (held-out plan
faults) runs tonight.
