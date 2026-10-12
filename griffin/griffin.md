# Griffin: today (Mon 12 Oct)

Three pieces of work, each one something you can put on a resume and each
one something the IEEE IV paper needs. You can do most of it by prompting
Claude Code; what matters is that the result is checked and written down.
Will reads your hand-ins tomorrow.

| # | What | Where | Time | Resume line |
|---|---|---|---|---|
| 1 | Fresh install of the open-source repo | your MacBook | 1 h | Tested and fixed the install path of an open-source AV testing framework |
| 2 | Blind human check of who caused each crash | lab box (SSH) | 3-4 h | Designed and ran a blinded human evaluation of automated failure attribution for AV stress testing (n = 60, Cohen's kappa) |
| 3 | Statistics for the search-method comparison | lab box (SSH) | 2-3 h | Statistical analysis of LLM-guided vs rule-guided scenario search (bootstrap, permutation tests, power analysis) |

Stretch, if there is time: a Review tab in the web app (section 5).

## 0. Ground rules

- **The GPU is busy until about 04:00 UTC on 13 Oct** (2 Hz replicates). Do
  not run `simgate worker`, `simgate queue`, `simgate front`, or anything
  that launches a simulation. Everything below is CPU only and safe to run
  while the queue works.
- **Do not touch** `research/studies/`, `research/jobs/`,
  `research/harness/*_queue/`, the traces in `research/harness/*.jsonl`, or
  anything in `src/` (AlpaSim itself). Read them as much as you like.
- **Work on a branch:** `git -C ~/alpasim/research checkout -b griffin/oct12`.
  Push the branch; do not push to `main`. Will merges.
- **Python through `uv run`** from `~/alpasim` (e.g.
  `uv run python research/harness/who_closed.py`), never an activated venv.
- **Tests stay green:** `uv run pytest research/harness` (about 25 s).
- Every number you write down says where it came from (a file or a command).

Read first (30 min): `research/README.md`, then the top of
`research/BACK.md` (what we found this week), then FACTS problems 25, 29 and
30 (search `| 25 |` in `research/FACTS.md`). Those three problems are why
task 2 matters.

## 1. Fresh install on your Mac (1 h)

Pretend you found `github.com/willv678/simgate` on your own. The simulator
itself needs an NVIDIA GPU, so on a Mac the goal is the path a reader without
one takes: clone, install, run the tests, browse the results.

1. Clone it, follow **only** the README. Do not ask Will or read the code to
   get unstuck; if the README does not say it, that is a finding.
2. Run the tests the way the README says. Run `research/simgate doctor`; it
   should fail on the GPU check, cleanly and with a message that says why.
3. Open the read-only results snapshot (`site/`, README "Browse every study
   without a GPU") and click through every tab.

**Hand in** `research/griffin/INSTALL.md`: every place you got stuck or
confused, the exact command and error, how long each step took, and what you
would change. Then fix the easy ones (README wording, a clearer `doctor`
message) in one commit on your branch.

## 2. Blind human check of who caused each crash (3-4 h)

**Why.** The paper's failure counts rest on deciding, for each crash, whether
it was the policy's fault. Today three things decide that, and none of them
is a person:

- the failure rule, `outcome()` in `research/harness/outer.py` (counts a
  front or side contact after the hand-off, before any rear contact, and
  skips a contact already under way at the hand-off);
- the model's triage, `research/studies/<study>/**/triage.json` (fields
  `cause` and `policy_at_fault`);
- a geometric check, `research/harness/who_closed.py` (did a replayed car
  run into an ego braking in its own lane).

You will be the person. Label crashes without seeing any of the three, then
measure how well each one agrees with you.

**Build** `research/harness/label_sheet.py` with two commands:

- `make`: draw a fixed random sample (seed it) of 60 runs from the kept runs
  of six studies (`cut_in_merge`, `lead_vehicle`, `pedestrian_ego_speed`
  and their `_2hz` versions), stratified so each study gives 10. In each
  study take about 7 runs that `outcome()` counts as failed, and about 3
  that had a collision flag `outcome()` does *not* count (rear-ended, or a
  contact under way at the hand-off), so you can disagree in both
  directions. Shuffle, give each an id (L01-L60), and write
  `research/griffin/labels/sheet.csv` with: id, scene, video path, the
  hand-off time, and empty columns `fault` (policy / not_policy / unclear),
  `what_happened` (one line) and `minutes`. Nothing else: no study name, no
  setting, no triage, no rule result.
  - Kept runs and their run folders: `compare_proposers.arms(study)` and
    `read_state.queue_entries(folder / "queue")`; skip entries whose
    `resolution` is not `ACCEPT` or that have `quarantine`
    (`who_closed.classify` does exactly this).
  - Each run has a front-camera video:
    `diag/<run>/rollouts/<scene>/<id>/*_camera_front_wide_120fov_default.mp4`.
  - The front camera does not show a car hitting the ego's side or rear.
    So also draw a **top-down plot** for each run, 3 s before to 3 s after
    the first contact, ego and nearby cars as boxes:
    `asyncio.run(physics._read(rollout.asl))` gives poses (`raw["ego"]`,
    `raw["others"]`, `raw["sizes"]`) and `physics._footprint` gives a box;
    `who_closed.contact` shows how to use them. Save as
    `research/griffin/labels/topdown/L01.png` and so on.
- `score`: read your filled-in sheet, look up the three automated answers
  for each run, and write `research/griffin/LABELS.md`: one table per method
  (rule, triage, geometric check) against you, agreement in %, Cohen's
  kappa (write it out: a few lines of numpy; scikit-learn is not installed,
  and adding a dependency to the shared environment is Will's call), split by
  study and by rate, plus every disagreement with one line on why.

Label all 60 before you run `score`. Write down before you start what
"policy's fault" means to you (one paragraph at the top of the sheet); keep
it fixed. Note the minutes per run: how long a person takes is itself a
result (it is what an automated check saves).

**Hand in:** the two scripts' output, `LABELS.md`, the sheet, a test for
`label_sheet.py` (the sample is the same every time, nothing leaks into
the sheet).

## 3. Statistics for the method comparison (2-3 h)

**Why.** The paper compares how fast each search method finds the 5 hardest
cases: rules, hybrid, llm, random + confirmation (`research/METHODS.md`,
`research/methods.json`). With 3 replicates per method we currently say
things like "hybrid is about one case ahead on cut-in" and "on lead vehicle
no method is ahead". Are those claims supported?

**Build** `research/harness/method_stats.py`, writing
`research/griffin/STATS.md` and one figure in `research/figures/`:

1. For each study and method: confirmed hardest cases and runs to the goal,
   with bootstrap 90% intervals over replicates. `methods.json` has these
   per replicate (`confirmed`, `runs_to_goal`, `reached`).
2. Better than final counts: **confirmed cases as a function of runs**, one
   curve per replicate. `compare_proposers.proposer_report(folder, goal,
   vary, compare)` returns `goal_progress` (confirmed after each run); see
   how `analyze_methods.py` calls it. Plot median and range per method.
   Area under that curve is a fair single number for "found more, sooner".
3. Pairwise permutation tests between methods on that number, per study,
   with a correction for the number of comparisons. Which claims in the
   README's "Fair baselines" row and BACK finding 6 survive?
4. Power: from the spread you see, how many replicates would it take to
   tell hybrid from llm on cut-in? Replicates 2 and 3 of the 2 Hz studies
   are running tonight; is 3 enough?

Use only arms `analyze_methods.replicate_rows` includes (it leaves out arms
that stopped early). Do the 10 Hz studies first; the 2 Hz ones only have one
or two replicates finished today.

**Hand in:** the script with a test, `STATS.md`, the figure. Lead `STATS.md`
with the three sentences you would put in the paper.

## 4. When you hand in

- Push branch `griffin/oct12`, with `uv run pytest research/harness` passing.
- Add one line per task to the bottom of `research/LOG.md` (date, what,
  where the result is).
- Message Will the three headline numbers: install time and blockers,
  kappa of the failure rule against you, and which method claims survive.

## 5. Stretch: a Review tab in the web app

The web app (`research/harness/web.py`, `research/harness/web/`, tests in
`research/harness/test_web.py`; run with `research/simgate serve`) has
Studies, Results, Queue and Activity tabs. Add **Review**: shows one run's
video and top-down plot from task 2, three buttons (policy / not_policy /
unclear) and a notes box, and saves to the same `sheet.csv`. That turns
task 2 into a tool anyone can use to audit a study. Keep it read-only with
respect to studies and the queue.

## Starter prompts for Claude Code

Start every session with: *"Read research/griffin/griffin.md and follow its
ground rules. Do not launch simulations, do not edit research/studies,
research/jobs, the queue folders, or src/."* Then, for example:

- Task 2: *"Write research/harness/label_sheet.py as described in task 2.
  Start with `make`. Reuse who_closed.classify and physics._read; show me
  three top-down plots before generating all 60. Add a test that the sample
  is reproducible and that sheet.csv has no column that reveals the study,
  setting, triage or rule result."*
- Task 3: *"Write research/harness/method_stats.py as described in task 3.
  First print, for the three 10 Hz studies, each method's goal_progress
  curve per replicate, using analyze_methods.replicate_rows to pick the
  arms."*

Check what it writes: open the plots, recompute two numbers by hand, read
the diff before you commit.
