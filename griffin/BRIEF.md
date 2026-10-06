# Griffin: explore what SimGate could do next (Fri 2 Oct)

One day, open-ended, with Claude (Opus 5.5) as your pair. The goal is a list of
good ideas, a few of them prototyped, without breaking anything that is already
measured. Will reads your list on Monday.

## 1. Learn the system first (about 1 hour)

Read in this order:

1. `research/GUIDE.md`: what SimGate is, with diagrams. Read all of it.
2. `research/harness/README.md`: the code and the safety model.
3. `research/harness/advisor/CLAUDE.md`: the only thing the Investigator is
   told. Its five skills are the menu you will be extending.
4. `research/harness/test_validate_diagnosis.py`: the gate's rules as one table.

The one idea everything rests on: **the model proposes, the gate decides.** The
model can only pick from a finite menu; deterministic code checks every
answer; `verify_supervisor.py` tries every possible answer to prove nothing
breaks the gate. Any new capability has to keep that true.

## 2. Ground rules

- **Work on a branch:** `git -C research checkout -b griffin/explore`. Do not push
  to `main`. Will merges what he wants.
- **Do not edit `src/`** (AlpaSim itself) and do not touch existing queue folders
  or traces in `research/harness/` (`b2_*`, `s1_*`, `c0_*`, `c1_*` to `c4_*`,
  `g2_*`, `g3_*`). They are the paper's data.
- **Tests stay green:** `uv run pytest research/harness` from `~/alpasim`. It
  includes the exhaustive gate check. A new skill or parameter without a
  validator rule, a test, and a passing verifier is not done.
- **GPU:** from 6 Oct the GPU runs C3, then g3, then C4, until about 8 Oct
  (`tail research/harness/campaign.log`). Before launching, check nothing
  else is running: `ps aux | grep "[l]oop.py"` must print nothing.
  Small batches only (10 runs or fewer), in your own queue folder named
  `research/harness/g_<something>_queue`. One batch at a time.
- **Python through `uv run`**, never an activated venv.

## 3. The task: find new capabilities (about 6 hours)

Pick any of the four tracks. For each idea, write it down even if you do not
build it. Build the one or two you like most.

### Track A: more things the Investigator can change

CONFIGURE may only change **how a run executes, never what it measures**
(context length, traffic model on CPU/GPU, scene catalog). What else is an
execution knob? Look through `src/wizard/configs/` and a run's
`diag/<run>/wizard-config.yaml` for settings like batch sizes, timeouts,
devices, or rendering options. For each candidate, write: what failure it would
fix, and why it does **not** change what the experiment measures. If it does
change the measurement, it does not belong on the menu (the verifier found
exactly this bug with the delay).

To add one: `read_state.py` (`CONFIG_KEYS`, `CONFIGURABLE_KEYS`, the landed
check), `run_experiment.py` (`wizard_command`), `diagnose.py` (`SCHEMA`),
`advisor/CLAUDE.md`, a row in `test_validate_diagnosis.py`, and a CONFIGURE
variant in `verify_supervisor.py`'s `CHOICES`.

### Track B: new faults, especially ones that hide in the numbers

Dr. Shao's diagrams list execution uncertainty: sensor noise, actuator lag,
dropout, disturbance. AlpaSim already has a plan-corruption hook you can turn
on with settings alone, no `src/` edits:

```
runtime.simulation_config.fault_injection.enabled=true
runtime.simulation_config.fault_injection.lateral_bias_m=0.5
runtime.simulation_config.fault_injection.waypoint_noise_std=0.3
runtime.simulation_config.fault_injection.freeze_plan_steps=10
runtime.simulation_config.fault_injection.truncate_horizon_s=0.5
```

Add new kinds to `faults.py` (see how `rails` and `kinematic` swap one wizard
argument) and run a few. The interesting question: **does the run still look
normal in its summary metrics?** Then check whether the physics checks
(`physics.py`) or the Auditor catch it. A fault nothing catches is a great
finding; write down what check would catch it.

### Track C: new physics or K⁺ checks

`physics.py` rebuilds the car's motion from each run's log. Ideas:

- **Hidden retries.** The simulator sometimes retries a crashed rollout inside
  one run (`diag/s1_059` holds three rollouts, one complete). Nothing records
  this. A check that counts them would be a real addition.
- **Car following.** Time headway to the car ahead, closing speed, braking
  before contact.
- **Lane keeping.** Does the motion agree with the `offroad` and
  `min_distance_to_lane_boundary_m` metrics?

New bounds must fire on **no** clean run: check with
`uv run python research/harness/calibrate_physics.py`.

### Track D: new jobs for the agents

What else could the Investigator or the Auditor be asked, with the same rule
that they only propose? For example: the Auditor explaining why a scene keeps
failing, comparing two batches for drift, or proposing physics bounds the way
it proposes config rules. Write each as: the question, what the agent would see,
what it would answer, and what deterministic check decides whether to act.

## 4. What to hand in

1. `research/griffin/ideas.md`, a table with one row per idea:

   | Idea | Track | What it catches or fixes | Changes what a run measures? | Built? | Evidence |
   |---|---|---|---|---|---|

2. Your branch, with any prototypes and their tests passing.
3. Three lines to Will at the end of the day: the best idea, what you built, and
   anything that surprised you.

## 5. Starting your Claude session

From `~/alpasim`, run `claude` and paste:

```
Read research/griffin/BRIEF.md, then research/GUIDE.md and research/harness/README.md.
I am Griffin, helping on SimGate for one day. Follow the brief's ground rules exactly:
branch griffin/explore, no edits to src/ or to existing queue folders and traces,
tests must stay green, at most 10 GPU runs per batch in my own g_*_queue folder.
Help me work through the tracks in section 3. Start by explaining the five
skills and the validator to me, then help me pick an idea from Track B.
```

If something seems wrong or a test fails and you cannot tell why, stop and write
it down for Will instead of working around it.
