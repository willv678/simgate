---
name: simgate
description: Run autonomous-driving stress-testing studies with SimGate on AlpaSim: check the machine, write and plan a brief, queue studies, watch them, compare search methods, make case cards, export OpenSCENARIO. Use when a person asks to stress-test the driving policy, to check on studies, or to show what SimGate found.
---

# Operate SimGate: run AV stress-testing studies on AlpaSim

SimGate stress-tests a driving policy (VaVAM) in AlpaSim. A person writes a
brief (a question in their own words); SimGate plans a study, runs it on the
GPU, keeps only runs that pass every validity check, and answers the brief.
Every command below runs from the AlpaSim repository root. You start
commands and read their output; the decisions inside a study (plan, next
runs, recovery, audit, triage, report) are made by the other SimGate skills,
each called by Python and checked by code.

## If this, run this

| Situation | Run | Then |
|---|---|---|
| Is the machine ready? | `research/simgate doctor` | fix what it names before queueing |
| A person wants to test something new | `research/simgate new <category>/<name>` | fill the brief: Question, Scope, Budget, What counts |
| A brief is written | `research/simgate plan <category>/<name>` | show the plan and the check's verdict to the person; never queue a plan the check rejects |
| The person approves a plan | `research/simgate queue <category>/<name> --proposer <methods> --replicate 1 2 3` | methods: `rules hybrid llm random_confirm optuna_confirm hybrid_optuna llm_v2 hybrid_v2` |
| Nothing is running | `research/simgate worker` | it runs queued studies as GPU slots free (2 at once) |
| A study should go next | `research/simgate front <job id>` | |
| How is it going? | `research/simgate status` | studies, arms (kept, failures, goal), the job queue |
| A study finished | `uv run python research/harness/study.py <brief> --report-only` | the report cites setting ids; Python writes the counts |
| Compare methods | `uv run python research/harness/analyze_methods.py`, then `uv run python research/harness/discovery_curve.py` | `research/METHODS.md`, `research/figures/discovery_*.png` |
| Show a person what failed | `uv run python research/harness/case_card.py hardest` (or `spot` for 20 random runs) | one card per case under `research/figures/cards/` |
| Explain the failures of a study | `uv run python research/harness/triage.py research/studies/<study>` | causes per failure (the simgate-triage skill) |
| Audit a finished batch | `uv run python research/harness/audit.py <queue dir>` | flagged runs and proposed rules (the simgate-audit skill); a person admits rules |
| Export a study as a standard scenario | `uv run --with scenariogeneration python research/harness/to_openscenario.py` | `research/scenarios/*.xosc`, OpenSCENARIO 1.4 |
| A person wants to show the results | `research/simgate serve`, or `research/simgate export` for a read-only snapshot | |

## What you never do

- Change a run's result, a study's counts, or a plan the check rejected.
- Launch AlpaSim directly, stop a run, or remove containers: the inner loop
  and its recovery skills do that.
- Edit `src/` (AlpaSim itself).
- Report a number you did not read from a file a script wrote.
