# Week 4 slides: 6 Oct

Plain language, for someone seeing this for the first time. At most four
bullets per slide. Image paths are relative to `research/`.

---

## 1. Automatic testing for self-driving software

- Testing a self-driving model in simulation means thousands of runs, and a
  person has to decide what to test, babysit the runs, and read the results.
- I'm building a system that does all of that from one written question.
- An AI (Claude) suggests each step. Plain code checks every suggestion
  before anything happens.

**Image:** draw a simple left-to-right flow:
`Question → Test plan → Run tests → Check each run → Explain crashes → Answer`

---

## 2. You start by writing a question

**Image:** screenshot of `briefs/latency_budget.md`

- A short text file: the question, which scenes, how many runs, what counts as
  a crash.
- Example: "How much delay can the driving model handle before it crashes?"
- It's like the test plan an engineer writes before a test campaign.

---

## 3. The AI turns it into a test plan

**Image:** screenshot of `studies/latency_budget/plan.json`

- Claude picks the scenes, the settings to try, and how many runs.
- It also writes down what the plan can't tell you.
- Code checks the plan first (real settings, real scenes, within budget), and
  a person can approve it.

---

## 4. The AI picks which tests to run next

**Image:** `figures/delay_curve_02eadd92.png`

- After each batch it looks at the results and picks the next tests.
- Here it narrowed in on where one scene starts crashing as delay goes up.
- The bars show how sure we are; it spends more runs where they're wide.

**Say:** "This is a simple example that a basic search could also do. Next I'll
compare it against the standard methods on harder questions."

---

## 5. Every run is checked before we trust it

**Image:** `figures/campaign_invalid.png`

- Simulations break quietly: a crash halfway, missing results, a wrong
  setting. They still look like normal data.
- After every run, plain code checks it: did it finish, did the settings
  actually apply, is the car's motion physically possible?
- Test: I broke runs on purpose, 225 times. Without checks, all 225 bad runs
  would have been counted. With them: **0.**

**How to read the chart:** each bar is the number of broken runs that got
counted as real data. Top: no checks. Middle: checks on each run. Bottom:
checks plus a review of the whole batch.

---

## 6. The checks caught a problem before it mattered

**Image:** `figures/plan_age.png`

- Before the first real test, the checks would have thrown out every delay
  experiment. A bug in how they handled delay.
- Fixed. Now each run proves from its own log that the delay really happened.

**How to read the chart:** how old the car's driving plan is at each moment.
No delay: 0. A 200 ms delay: always 200. A broken, frozen plan: a sawtooth.

---

## 7. It learns new checks, and a person approves them

- The AI reviewed a batch and noticed a pattern in the bad runs: the wrong
  controller was being used.
- It proposed a new check. Code tested it on 51 known-good runs: no false
  alarms.
- I approved it, and now it runs on every test automatically, with no AI.

---

## 8. It explains crashes and won't over-claim

**Image:** `figures/triage_example.png`

- For each crash, the AI watches the video and says why: "didn't brake for the
  car stopping at the red light."
- Every number in the final answer comes from code, not the AI.
- When I asked it to confirm an early result, it said **"not confirmed, needs
  more runs."**

---

## 9. Next steps

- Compare against standard search methods on harder questions.
- Check the simulator setup for the driving model (it may be running at the
  wrong speed).
- Get more tests per hour, and add scene descriptions ("intersection,
  pedestrians").
- **Ask:** a bigger GPU (48–80 GB) to test a stronger driving model, NVIDIA's
  Alpamayo, which needs ~40 GB.
