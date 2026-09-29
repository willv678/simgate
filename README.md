# SimGate

**The model proposes, the gate decides.** Runtime assurance for LLM-operated
driving simulation.

SimGate runs batches of [AlpaSim](https://github.com/NVlabs/alpasim) driving
simulations unattended, with Claude helping to run them, and guarantees that
nothing the model says can put an invalid run into the dataset. Deterministic
checks (the Gate) decide which runs are kept. The model only proposes: a fix
from a five-item menu when a run fails (the Investigator), and flags and new
checks after a batch (the Auditor). Admitted checks join the Gate (the
Rulebook). An exhaustive search over every answer the model could give (the
Verifier) shows none of them breaks the Gate.

![Invalid runs kept](figures/invalid_kept.png)

*Pilot fault campaign: invalid runs kept in the dataset with no checks, with the
per-run Gate, and with the Gate plus the Auditor.*

| Start here | For |
|---|---|
| [`GUIDE.md`](GUIDE.md) | the whole project with diagrams and results |
| [`harness/README.md`](harness/README.md) | the code, safety model, and quickstart |
| [`FACTS.md`](FACTS.md) | every measurement and where it came from |
| [`OUTLINE.md`](OUTLINE.md) | the IEEE IV 2027 paper plan |

---

## Working in this repo

Start here. This folder is the only current description of Will's IEEE IV 2027 project.
The long notes at the repo root are background. If they disagree with this folder, this
folder wins.

People: Will (senior, writing the paper), Griffin (sophomore, ~10 h/week, runs batches
from the runbook), and whatever agent is in the repo. The advisor is Shao (controls,
University of Georgia). His slides from 2026-09-22 are in `source/diagrams.pdf`.

## Read order

| Who | Read | Update |
|---|---|---|
| A new LLM session | `PITCH.md`, then the board in `STATUS.md` | `STATUS.md` row and `LOG.md` when the task is done |
| Anyone about to change code or launch a run | `STATUS.md`, then `FACTS.md` | the board row it finished |
| Anyone asking "what is this project" | `GUIDE.md` (diagrams, results, slide plan); `MAP.md` is the older Loop 1 map | when a result or the claim changes |
| Will or Griffin, for the semester plan | `WEEKS.md` | when a week is replanned |
| Griffin, or an agent launching rollouts | `RUNBOOK.md` | when a command in it is wrong |
| Anyone tempted to re-diagnose the baseline | `FACTS.md` | when a new measurement replaces an old one |

Do not add another research markdown unless `STATUS.md` names the question it answers.

## What is current

The paper is SimGate: Loop 1 as Shao designed it on 22 Sep 2026 (preflight
K⁻, postflight K⁺, a finite skill menu), built and extended with an
investigating agent, a batch auditor, rule mining, and an exhaustive check of
the gate. Full picture: `GUIDE.md`. Claims and evidence: `OUTLINE.md`,
`FACTS.md`. Board: `STATUS.md`. Scripts from paused work are in `archive/`.

This folder is its own git repo (ignored by NVlabs AlpaSim), pushed to
https://github.com/willv678/switching-stability. New notes and harness scripts go
here so they publish without copying into `~/autolab-harness`. That older mirror is
frozen. Do not develop there. Griffin: clone or pull that repo for the week plan;
run wizard from the AlpaSim checkout.

Harness Python lives in `harness/`. Run it from the AlpaSim checkout:

```bash
cd /home/willvarner/alpasim
uv run python research/harness/analyze_cp2.py
uv run pytest research/harness/test_analyze_cp2.py
```

Edits inside AlpaSim packages stay in `../src/`. Refresh the published delta with
`./export_src_diff.sh` (writes `patches/alpasim-src.diff`).

## Background, not instructions

| File | What it still contains | What is stale |
|---|---|---|
| `paper-switching-stability.md` | The paper argument, risks, and phases | "Immediate next steps" at the bottom. Use `STATUS.md`. |
| `HANDOFF.md` | Code-level tasks and acceptance tests | The progress blurb at the bottom, and any task `STATUS.md` marks done. |
| `researchideas.md` | Why the red-team / search papers were rejected, and the rigor checklist | The eight-week plan and "next three days." |
| `paper-attribution-repair.md` | Interface interventions, kept as tools inside the stability paper | It is not the lead paper. |
| `SESSION_CHANGES.md` | What one September session changed in the controller | A session log, not a plan. |

## Rules for agents

- Python goes through `uv`. Never activate a venv. See `.cursor/rules/uv-python.mdc`.
- `src/` is upstream AlpaSim. Change it only when `STATUS.md` names the file.
- Harness scripts live in `harness/` (`analyze_cp2.py`, `download_scenes.py`, …). They can change. Do not add new experiment scripts at the AlpaSim repo root.
- The model is called only by `harness/diagnose.py` (on FAILED) and `harness/audit.py` (after a batch). Its system prompts are `harness/advisor/`. Any new model call needs a row in `STATUS.md`.
- Do not trust `cp2_failure_boundary.png` or `failure_boundary.png`. The latency axis on the historical 212 runs was parsed wrong. See `FACTS.md`.
- When you finish a task, edit `STATUS.md` in the same change: date, what was measured, where the artifact lives. A task with no artifact is not done.
