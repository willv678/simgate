# Status

Living tracker. As of 2026-09-22. If you finish something, replace the row. Do not
append a second status for the same task.

Deadline: conference paper **15 Nov 2026**, 6 pages including figures and references.
Notification 15 Jan 2027. Workshop papers, if needed as a fallback, are due 1 Feb 2027.
Source: https://ieee-iv.org/2027/contributions/call-for-papers/

## Now

PI decision, 28 Sep 2026. The controller is a Claude session on a Max subscription,
not an OpenRouter wrapper. The session may only dispatch named scripts. The model
is allowed in one branch: `FAILED` calls a diagnose step, then `validate_diagnosis.py`
accepts or rejects that diagnosis, then `recover.py` runs the accepted recovery.
`READY`, `RUNNING`, and `COMPLETE` are Python. Do not shop models. Do not wrap the
chat-completions API.

The state loop he wrote:

```
READY    -> run_experiment.py
RUNNING  -> monitor.py
COMPLETE -> analyze.py, plot.py, archive.py
FAILED   -> diagnose, validate_diagnosis.py, recover.py
```

`read_state.py` is the thing the loop polls. Map it onto the checks that already
exist. Do not start over. Loop 2 stays motivation.

The `while` is Python. Claude is not a session that stays open. On `FAILED` only,
Python runs `claude -p` once, with `research/harness/advisor/CLAUDE.md` as the
whole system prompt, no tools, and an empty working directory. Python passes the
failure status and at most 15 distinct error lines. Then the process exits.
`validate_diagnosis.py` accepts a skill from the menu, or a CONFIGURE of
`context_length`, `planner_delay_us`, or the scene file. Anything else is
rejected and `recover.py` does not run.

The paper model is pinned to `claude-opus-5-5`. Haiku was a pilot. Do not sweep
models. A win is not agreement with the script. A win is the next run writing a
metrics file with no person in the loop. On the GPU out-of-memory case, `RE-RUN`
and `RESTART_CLEANUP` are both legal. Neither is the fix that worked: CATK on
CPU is not on the menu. `--no-launch` must not run `docker compose down`. Do not
start the draft. Do not launch `--policy model` until Will says the GPU is free.

The agent emits a skill \(s_k\) such as CONFIGURE, LAUNCH, RE-RUN, RESTART_CLEANUP,
plus parameters. It does not emit free text. \(K^-\) rejects an illegal skill or a
config that must not launch. \(K^+\) turns a crash, a core dump, or a garbage metrics
file into a structured status the agent can use on the next step. Research question
Shao stated: how long can this run without a person, and how does it detect and
recover.

The comparison that makes the model earn its place: the same skill menu with a
hand-written policy, versus the model. Failures \(w_k\) must include bad science,
not only process death: `context_length` underflow, missing metrics, config that
did not land, solver status that is not the solver's. A 24 GB GPU arrives the week
of 29 Sep. The 12 GB out-of-memory failure will get rarer. Do not hang the paper
on it.

Switching-stability and the jitter test are paused. They are not the claim.

## Board

This is the sheet. An agent takes the first `todo`, sets it to `doing`, and does
nothing else. On success it sets `done`, writes the artifact path, and appends
`LOG.md`. It does not start the next row.

| ID | State | Task | Done when |
|---|---|---|---|
| L1 | done | Skill menu and step record. Typed skills: CONFIGURE, LAUNCH, RE-RUN, RESTART_CLEANUP, ACCEPT. A step record with skill, params, and the K status that produced it. | Unit tests pass. No simulator is launched. Code lives under `research/harness/`. `research/harness/skills.py` and `research/harness/test_skills.py`. |
| L2 | done | Preflight \(K^-\). Reject `context_length` other than 8, a Hydra delay that does not match the request, and a missing scene file. | Tests cover those three rejects and one accept. No simulator is launched. `research/harness/preflight.py` and `research/harness/test_preflight.py`. |
| L3 | done | Postflight \(K^+\). Read a finished run directory. Fail it if metrics are missing. Record at-fault and rear-contact separately. Note solver status when a controller CSV exists. | Tests use `diag/test_vavam_ctx8` and a fixture with no metrics file. `research/harness/postflight.py` and `research/harness/test_postflight.py`. |
| L4 | done | Hand-written recovery policy on the same menu. Missing metrics or a dead process becomes RE-RUN or RESTART_CLEANUP. A config \(K^-\) rejected is never launched. A clean run becomes ACCEPT. | A table test lists each status and the skill returned. `research/harness/policy.py` and `research/harness/test_policy.py`. |
| L5 | done | One real batch of three nominal launches driven by L4, written as step records. | Trace is `research/harness/l5_trace.jsonl`: three ACCEPT lines. No run directory is named in the trace. |
| L7 | done | Fix K⁺ and regenerate the trace. Lines 1 and 2 of `l7_trace.jsonl` can stand. Line 3 is false. | `research/harness/l7_trace.jsonl`. ctx8 line is `at_fault=False, rear=True`. `collision_any` is not at-fault. 8 postflight tests passed. |
| L6 | done | Model policy on the same menu, compared with L4 on injected failures. | `research/harness/comparison_table.txt`. Haiku agreed on 2 of 3 L7 cases. It does not beat the script. |
| L8 | done | One real wizard launch through the script. The trace names that run directory. Postflight records at-fault and rear contact from that directory. The `context_length: 1` case is still not launched. | `research/harness/l8_trace.jsonl`. `diag/l8_rerun` and `diag/l8_rerun/rollouts/clipgt-01d503d4-449b-46fc-8d78-9085e70d3554/c2db6d12-bb5b-11f1-9053-d5abd4aba270/metrics.parquet` exist. at_fault=False, rear=False. |
| L9 | done | Results table from files that already exist. One row per lie: ctx length 1, latency regex, missing metrics, solver status reported as solved. Each row says what a reader would have concluded and what the gate does. | `research/RESULTS.md`. Counts cite `diag/nominal_run_*`, `cp2_results.parquet`, `autolab_experiments/`, and `diag/solver_status_verify/controller/alpasim_controller_d8ee28e6-b2c9-11f1-b35d-5316127291ca.csv`. No new simulator run. |
| L10 | done | Outer loop, one page of code. A rule that reads only ACCEPT rows and picks the next config. Not a search method. | `research/harness/l10_trace.jsonl`. Next config is `diag/l8_rerun`. `diag/l8_ctx8`, the no-metrics fixture, and both `context_length: 1` rows have `becomes_next` false. |
| L11 | done | The figure. Batch timeline: skill, veto, recovery, and which runs stay in the dataset. Plus the L6 agreement line. | `research/batch_timeline.png`. L7 keeps `diag/test_vavam_ctx8` (at-fault false, rear true). L8 keeps `diag/l8_rerun` (at-fault false, rear false). L6 agreement is 2/3, model_wins no. |
| L12 | done | Six-page outline. Claim, figure, table, the one Loop 2 sentence, related work. | `research/OUTLINE.md`. Claim, `batch_timeline.png`, `RESULTS.md`, one Loop 2 sentence, related work. Unsupported claims are in the left-out list. |
| B1 | done | One unattended batch of 10 ctx8 runs. | `research/harness/b1_trace.jsonl`. 10/10 wrote metrics in 28 minutes. At-fault on `diag/b1_06` only. Rear contact 0. No recoveries, because nothing failed to write metrics. The one-frame veto is in the L8 trace, not in this loop. |
| W1 | done | Turn his while-loop into scripts. `read_state.py` returns READY, RUNNING, COMPLETE, FAILED, or DONE for a run directory. READY, RUNNING, and COMPLETE only call Python. FAILED is the only step a Claude session may diagnose, and `validate_diagnosis.py` can reject that diagnosis. | `research/harness/w1_trace.jsonl` (script) and `w1_model_trace.jsonl` (Haiku via `claude -p`). `diag/l8_ctx8` FAILED → diagnose, validate, recover. `diag/l8_rerun` COMPLETE → analyze, archive, ACCEPT. The ctx1 config FAILED at preflight → CONFIGURE `context_length` 8. Recovered runs are queued READY and not launched. Loop: `research/harness/loop.py`. No `plot.py` per run; the figure stays batch-level. 89 tests passed. |
| B2 | done | One unattended batch of 150 ctx8 runs through `loop.py`, Opus 5.5 on FAILED. | `research/harness/b2_trace.jsonl`, `b2_queue/results.jsonl`, numbers in `FACTS.md`. 537 min, 158 launches, 150/150 kept. 8 failures, all a Docker network leak from 29 earlier runs; Opus RESTART_CLEANUP freed nothing and a person removed the networks. 0 failures in 150 launches after `run_experiment.py` began taking each run down. At-fault 40/150, rear 6/150. |
| T1 | done | Stronger base. Machine check before every launch, CLEANUP_ENV for shared leftovers, and a tier 1 agent (`--policy agent`) that may investigate with read-only tools before choosing a skill. `trafficsim_device` joins CONFIGURE; `scene_id` joins the queue config and the landed check. | `environment.py`, `faults.py`, `diagnose.py`, `probe_fence.py` → `fence_probe.json` (5/5 forbidden actions denied), `compare_policies.py` → `comparison_opus.txt`. Numbers in `FACTS.md`. 106 tests passed. |
| S1 | todo | One run per local scene (101) through `loop.py --policy agent`. `enqueue_scenes.py research/harness/s1_queue s1`. | `research/harness/s1_trace.jsonl`. Which scenes finish and write metrics, and every failure the loop met. |
| T2 | done | Tier 2 auditor: one agent reads a finished batch (anonymized snapshot, read-only) and quarantines runs whose data does not measure what the batch claims. | `audit.py`, `advisor/AUDIT.md`, `eval_auditor.py` → `auditor_eval.json`. 46/46 planted lies caught with 0 false flags in A–D and F; 0/10 in E, the uniform batch with no reference. Numbers in `FACTS.md`. |
| F1 | done | Fault injectors for the campaign: kill, hang, delete_metrics, corrupt_metrics, drop_delay (persistent), fill_network_pool. HALT joins the menu so a persistent failure can stop early. | `faults.py`, `enqueue_campaign.py`, `score_campaign.py` (per fault kind, with the no-gate arm). 119 tests. |
| C0 | doing | Pilot campaign: one of each fault and two clean runs, tier 1. | `research/harness/c0_trace.jsonl`, `c0_queue/score.json`. Every injector fires and the loop finishes. |
| L13 | todo | Full draft. | A PDF or markdown draft Shao can read. Do not start until W1 exists. Target the week of 26 Oct. |
| L14 | todo | Revise from Shao. | Draft matches his comments. No new experiment unless a figure cell is empty. |
| L15 | todo | Submit to IV 2027. | Submitted by 13 Nov 2026 so the 15 Nov deadline is a buffer. |

L8 is done. The launch the trace names is `diag/l8_rerun`. L5's three ACCEPT lines are not that launch.

Paused, and not on this board: gain-switching sweeps, jitter test, Riccati-as-paper,
scene qualification for its own sake, Loop 2 as a search paper. Evidence for the
old rows stays in `FACTS.md` and `diag/`.

## Out of scope

- Free-text sim control.
- An agent that retunes MPC gains or hunts for crash scenarios.
- LoRA training.
- Treating 12 GB out-of-memory as the main failure mode after the 24 GB GPU arrives.
