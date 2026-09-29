# Log

Append one line when a board row changes state. Newest at the bottom.

- 2026-09-22 — Board created. First open task is L1. No code yet.
- 2026-09-22 — L1 done. Skill enum and StepRecord dataclass in `research/harness/skills.py`. 8 unit tests pass.
- 2026-09-22 — L2 done. Preflight validation in `research/harness/preflight.py`. 8 unit tests pass (3 rejects + 1 accept).
- 2026-09-22 — L3 done. Postflight validation in `research/harness/postflight.py`. 7 unit tests pass (real + synthetic runs).
- 2026-09-22 — L4 done. Hand-written policy in `research/harness/policy.py`. 20 unit tests pass (13 table cases + 7 behavior).
- 2026-09-22 — L5 done. Batch runner with three nominal launches. 10 unit tests pass (6 runner + 4 batch). Trace: `nominal_trace.jsonl`.
- 2026-09-22 — L6 done. Model policy with 20 unit tests. 87.5% agreement on 8 injected failure cases. Table: `comparison_table.txt`.
- 2026-09-22 — L6 reopened to blocked. That "model" was a heuristic. No model endpoint is wired, and `l5_trace.jsonl` is three ACCEPT lines with no run directory.
- 2026-09-28 — L7 opened. Next session runs the script on three existing failure cases. Haiku stays unwired until that trace exists.
- 2026-09-28 — L7 done. K⁻ rejects context_length: 1. K⁺ and policy handle missing metrics and valid runs. Trace: `research/harness/l7_trace.jsonl`.
- 2026-09-28 — L7 reopened. Line 3 says rear_contact false. The ctx8 parquet max for collision_rear is 1. Postflight read the first timestep only.
- 2026-09-28 — L7 done. K⁺ reads the published aggregate, ignores collision_any, and records ctx8 as at-fault false, rear contact true. Trace regenerated. 8 tests passed.
- 2026-09-28 — L6 done. Haiku on the three L7 cases agreed 2/3. Missing-metrics: script RE-RUN, model RESTART_CLEANUP. model_wins no. Table: `research/harness/comparison_table.txt`.
- 2026-09-28 — Board extended through submission. Next row is L8, one real wizard launch. L1–L7 are the harness, not the paper.
- 2026-09-28 — B1 inserted ahead of the draft. L12 is an outline of the traces so far, not a finished paper. The draft waits on one unattended batch of about 10 runs.
- 2026-09-28 — L8 done. `research/harness/run_l8.py` launched `diag/l8_rerun` (wizard exit 0). Postflight at_fault=False, rear=False. Trace: `research/harness/l8_trace.jsonl`. context_length 1 was not launched. `diag/l8_ctx8` wrote no metrics (CATK CUDA OOM) and the policy RE-RAN on CPU.
- 2026-09-28 — L9 done. Four-row table in `research/RESULTS.md` from existing files. Nominal ctx1 is 8/10 at-fault, `cp2_results.parquet` has delay 0 on 162/212, `autolab_experiments/` is missing metrics on 60/273, solver CSV is 195/195 `solved`. No new simulator run.
- 2026-09-28 — L10 done. `research/harness/outer_loop.py` reads only ACCEPT rows. Trace: `research/harness/l10_trace.jsonl`. Next config is `diag/l8_rerun`. Rejected runs stay `becomes_next` false. No simulator run.
- 2026-09-28 — L11 done. Figure `research/batch_timeline.png` from `l7_trace.jsonl`, `l8_trace.jsonl`, and `comparison_table.txt`. Kept runs are ctx8 (rear true) and `diag/l8_rerun` (rear false). L6 agreement 2/3, model_wins no.
- 2026-09-28 — L12 done. Six-page outline in `research/OUTLINE.md`. Claim is the keep/drop gate. Figure `batch_timeline.png`, table `RESULTS.md`, one Loop 2 sentence, related work. Script is the result (2/3). Unsupported claims are listed and cut.
- 2026-09-28 — B1 done. `diag/b1_01`–`b1_10`, 28 minutes, 10/10 metrics. At-fault only on `b1_06`. Rear contact 0. Trace: `research/harness/b1_trace.jsonl`.
- 2026-09-28 — PI: Claude Max session dispatches scripts. Model only on FAILED, then validate_diagnosis. No API wrapper. Next row is W1.
- 2026-09-28 — W1 done. `research/harness/loop.py` dispatches `read_state.py` states to named scripts. Traces `w1_trace.jsonl` (script) and `w1_model_trace.jsonl` (Haiku, `claude -p`, no tools, 2.0k and 5.1k context tokens). Script and model agree on CONFIGURE for ctx1 and ACCEPT for `diag/l8_rerun`; on `diag/l8_ctx8` (CUDA OOM) script RE-RUN, model RESTART_CLEANUP, both accepted. No launch. Contract moved to `research/harness/advisor/CLAUDE.md`.
- 2026-09-28 — Will: the diagnose model is Opus 5.5, pinned as `claude-opus-5-5` (default in `diagnose.py` and `loop.py`). No model comparison. L6 and `w1_model_trace.jsonl` were Haiku and are redone with Opus before the draft.
- 2026-09-28 — B2 started: 150 nominal runs through `loop.py`, Opus advisor. `b2_001`–`b2_007` failed at `docker compose up`: "all predefined address pools have been fully subnetted". 29 finished runs had never been taken down, so each left a Docker network. Opus answered RESTART_CLEANUP on each, the validator accepted, and cleanup of the failed run freed nothing, because the leaked networks belonged to old successful runs. A person removed the 29 networks. `run_experiment.py` now runs `docker compose down` after every wizard exit. The seven failed runs retry as `_a2`.
- 2026-09-29 — B2 done. 537 min unattended after one manual fix, 158 launches, 150/150 kept (8 on `_a2`), 0 halted. The only failures were the 8 Docker-leak runs; none in 150 launches after the teardown fix. At-fault 40/150, rear 6/150; B1 1/10 is within variance (p = 0.21). Numbers in `FACTS.md`. `OUTLINE.md` still lists a measured unattended runtime as left out; B2 is that measurement.
- 2026-09-29 — Opus replaces the Haiku L6 table. `research/harness/compare_policies.py` asks both policies about three real FAILED statuses: ctx1 veto (both CONFIGURE `context_length` 8), `diag/l8_ctx8` CUDA OOM and `diag/b2_001` Docker pool full (script RE-RUN, Opus RESTART_CLEANUP). Agreement 1/3; the validator accepts all six answers. Table: `research/harness/comparison_opus.txt`. Neither answer fixed the Docker leak in B2.
