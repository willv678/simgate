# Week 4 slides: 6 Oct meeting with Dr. Shao

**Theme:** what we built and why, not results yet. About 9 slides. Image paths
are relative to `research/`.

---

## 1. From a gate to an automatic testing system

**On slide**
- Last week: the inner loop (preflight, run, postflight, Claude on failure).
- This week: the full system around it. **A researcher asks a question; the
  system designs the tests, runs them, checks every result, and answers.**
- One rule at every step: **Claude proposes, code decides.**

**Image:** draw this in the slide tool:

```
Brief → Plan → Outer loop ⇄ Inner loop → Triage → Report
```

Claude steps (Plan, Outer loop, Triage, Report) in orange; code steps (Inner
loop, plus the checks after each Claude step) in blue.

**Say:** "Last week I showed the state machine. This week it's wrapped in a
system you can hand a question to."

---

## 2. Feature: ask in plain English (`brief.md`)

**Image:** screenshot of `briefs/latency_budget.md`

**On slide**
- The researcher writes a short brief: question, scope, budget, what counts as
  failure.
- One sentence or a full page, whatever they want.
- Same shape as a test plan, so it's how test campaigns already start.
- Saved with the study, so you can always see what was asked.

---

## 3. Feature: brief → plan (Claude), checked by code

**Image:** screenshot of `studies/latency_budget/plan.json`

**On slide**
- Claude turns the brief into a concrete study: which knobs, which scenes, how
  many runs, what strategy.
- Example: it picked 6 scenes that drive cleanly with no delay, from city to
  highway speed, and wrote down its own limits ("a rough bracket, not a rate").
- **Code checks the plan before anything runs:** knobs must be in the catalog,
  scenes must exist, at most 60 runs.
- A person confirms it, or `--yes` lets it run overnight.

---

## 4. Feature: the outer loop picks the next runs

**Image:** `figures/delay_curve_02eadd92.png`

**On slide**
- Each round Claude sees every result so far and picks the next runs.
- What it did on its own: probed 200 ms, bisected toward the break, re-ran
  0 ms to check the baseline wasn't luck, and repeated near the edge.
- Every proposed run is checked against the knob catalog; illegal ones are
  dropped.
- The chart: crash rate climbs with delay on one scene. The bars show how
  sure we are; wide bars are where the next runs should go.

**Say:** "This is a deliberately simple question. One knob could be handled
with a hand-written binary search, so this is a demo of the loop, not proof it
beats one. Run longer, the bars shrink and it converges. The point is that
nobody wrote a search script: it read the brief. The real test is harder
questions, and comparing against a grid sweep, Optuna, and an expert-written
search, which is next."

---

## 5. Feature: the inner loop keeps every result honest

**Image:** `figures/campaign_invalid.png`

**On slide**, in two columns:

**Decides (plain code)**
- Preflight: the config and the machine.
- During the run: stops a run that freezes.
- Postflight: exit code, metrics, every requested setting actually applied.
- Physics from the run's own log.
- **Plan age** proves the requested delay really happened; **plan offset**
  proves a requested perception error really happened.
- Rules learned from past batches.

**Explains (Claude, never decides)**
- Fixes for broken runs (checked by a validator), the batch audit, triage.

**Proof:** three fault-injection campaigns, nine arms: invalid runs kept
**225 → 40 → 0**.

---

## 6. Why the inner loop matters: a bug it caught before it mattered

**Image:** `figures/plan_age.png`

**On slide**
- Before the first outer-loop run, I checked whether the gate could handle
  delay experiments. It couldn't: it would have **rejected every one**.
- A delayed plan reaches the controller in the car's position frame from
  when the plan was made, and the check didn't know that.
- Fixed, with a new check: the plan's age must equal the requested delay at
  every step. Clean runs read 0 ms, delay runs read exactly their delay,
  frozen plans form a saw-tooth.

**Say:** "An automatic tester is only as good as its checks. Without this
fix, the system would have confidently reported nonsense."

---

## 7. Feature: the system learns rules, a person approves them

**On slide**
- All three audits of one campaign independently proposed: "the controller
  must be the linear MPC."
- Admission: it catches the bad runs and fires on 0 of 51 good ones.
- I approved it, so now the gate enforces it on every run with no AI.
- **AI proposes → data admits → person approves → code enforces.**

---

## 8. Feature: why did it crash, and what's the answer

**Image:** `figures/triage_example.png`

**On slide**
- **Triage:** Claude watches frames around each crash and names the cause
  (e.g. "didn't brake for the car stopping at the red light").
- **Doubtful crashes flagged:** a crash far from where the real car drove may
  be a rendering problem, not the policy.
- **Report:** Claude answers the brief; every number in it comes from code.
  When Claude miscounted once, code started rejecting hand-written counts.
- **It won't over-claim:** I asked it to confirm a break the morning's pilot
  suggested. It said **"not confirmed"**, flagged two doubtful crashes, and
  listed the runs that would settle it.

---

## 9. Next, and what I need

**Next two weeks**
- **Real baselines:** a grid sweep (status quo), Optuna, and an expert-written
  search, compared on runs needed to answer, on harder multi-knob questions.
- **Check VaVAM's setup:** our harness runs it at 10 Hz control, while
  AlpaSim ships it at 2 Hz. Its high baseline crash rate may be partly ours.
  New class of check: are the settings *right for the policy*, not just
  applied?
- Several runs per launch (about 3× the evidence per GPU-hour); stop a study
  when its question is answered.
- Scene tags from logs and video, so a brief can say "intersections with
  pedestrians".
- A/B mode ("is model B safer than A?") and memory across studies.

**Ask: a bigger GPU.** 12 GB limits us to one research policy at ~15
runs/hour. NVIDIA's Alpamayo models (what AlpaSim targets) need ~40 GB. A
48–80 GB card would let us test a stronger, second policy and run repeats
faster.
