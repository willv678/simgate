# Outline

IEEE IV 2027. Six pages, including the figure, the table, and references.
Deadline 15 Nov 2026. This outline uses `l7_trace.jsonl`, `l8_trace.jsonl`,
`l10_trace.jsonl`, `comparison_table.txt`, `research/batch_timeline.png`, and
`research/RESULTS.md`. A sentence with no line in those files is left out.

## Claim

A run stays in the dataset only after preflight accepts the config and postflight
reads a metrics file. On these traces that means: `context_length` 1 is not
launched, a directory with no metrics is not accepted, and the real launch that
stays is `diag/l8_rerun` (at-fault false, rear contact false). The hand-written
policy is the result. On the three L7 cases the model agrees 2/3 and does not win.

## Pages

**1. Introduction.** One simulation batch, a finite skill menu, and a record of
which runs are kept. Name the menu: CONFIGURE, LAUNCH, RE-RUN, RESTART_CLEANUP,
ACCEPT. The menu emits a skill and parameters. Preflight \(K^-\) rejects a config
that must not launch. Postflight \(K^+\) turns a missing metrics file into a
status the next skill can use. The contribution is that gate. The figure and the
table are the evidence.

**2. The gate.** Preflight rejects `context_length` other than 8, a Hydra delay
that does not match the request, and a missing scene file. Postflight fails a
directory with no metrics parquet, and records at-fault and rear contact
separately. The hand-written policy maps those statuses to the menu: a rejected
config becomes CONFIGURE, missing metrics becomes RE-RUN, a run with metrics
becomes ACCEPT. `collision_any` is not at-fault. `l7_trace.jsonl` keeps
`diag/test_vavam_ctx8` with at-fault false and rear contact true.

**3. Figure.** `research/batch_timeline.png`, drawn from `l7_trace.jsonl` and
`l8_trace.jsonl`. L7: CONFIGURE vetoes context length 1 (out); RE-RUN on missing
metrics (out); ACCEPT keeps the ctx8 run. L8: context length 1 is not launched;
`diag/l8_ctx8` has no metrics and is a RE-RUN (out); `diag/l8_rerun` is ACCEPT
and stays, at-fault false, rear contact false. Caption the L6 line on the figure:
agreement 2/3, script/model CONFIGURE/CONFIGURE, RE-RUN/RESTART_CLEANUP,
ACCEPT/ACCEPT, `model_wins` no.

**4. Table.** `research/RESULTS.md`, one row per lie, each number already cited
there.

| Lie | Reader's conclusion the files support | Gate |
|---|---|---|
| Context length 1 | 8 of 10 nominal runs (`diag/nominal_run_1`–`10`) are at-fault, and each of those driver configs has `context_length` 1. | Preflight rejects it. Both traces leave it unlaunched. |
| Latency regex | `cp2_results.parquet`: `planner_delay_us` is 0 on 162 of 212 rows. The first-match regex and the leading 0 in `base_config.yaml` are the recorded mechanism. The 212 saved wizard configs now match that column. | Preflight rejects a delay that does not match the request. The reader takes `runtime.simulation_config.planner_delay_us`. |
| Missing metrics | 60 of 273 directories in `autolab_experiments/` have no `metrics.parquet`. | Postflight fails the run. The no-metrics fixture and `diag/l8_ctx8` become RE-RUN. |
| Solver status `solved` | The old rule wrote `solved` when `make_step()` did not raise. The verify CSV has 195 data rows, all `solved`. | The controller maps `solver_stats`. Postflight on `diag/solver_status_verify` returns `solver_status` None, because it looks for the CSV two directories above the run. |

**5. Script, model, and one Loop 2 sentence.** Same menu. `comparison_table.txt`:
the model matches the script on the context-length veto and on ACCEPT, and on
missing metrics it answers RESTART_CLEANUP where the script answers RE-RUN.
Agreement 2/3. `model_wins` no. The script is the result.

Loop 2, one sentence: a rule that reads only ACCEPT rows repeats the latest
accepted run, `diag/l8_rerun` in `l10_trace.jsonl`, and a rejected run does not
become the next experiment.

**6. Related work and references.** One short column, then the bibliography.
Cite only to mark the boundary. Confirm venue and theorem text before the draft;
the identifiers below are the ones in `FACTS.md`.

| Work | Sentence the traces support |
|---|---|
| AURORA, arXiv 2511.07768 | A supervisory redesign with a dwell-time theorem. This paper does not use that theorem. |
| DiffTune-MPC, arXiv 2312.11384 | Analytical MPC cost tuning. This paper does not choose gains. |
| Poirot, ISSTA 2026; DVCA; CF-RCA | Blame by swapping interior modules. This paper has a skill menu and a keep/drop gate. |
| Bench2Drive-Robust, arXiv 2605.18059 | A latency benchmark for end-to-end policies. This paper's latency row is a config-parse gate. |

## Left out

The traces do not support these, so they are not in the six pages.

- A measured unattended runtime, or an answer to how long the batch runs without a person.
- `l5_trace.jsonl` as launches. Those three ACCEPT lines name no run directory.
- The model beating the script.
- RESTART_CLEANUP as a skill the script executed. It appears only as the model's reply on the missing-metrics case.
- Loop 2 as a search over scenes, delays, or gains.
- A switching-stability or dwell-time result.
- The 12 GB out-of-memory event as the paper's failure mode. `diag/l8_ctx8` is in the figure only as a run with no metrics that the policy drops.
- A claim that postflight recorded solver status on `diag/solver_status_verify`.
- A claim that the 162 zero-delay rows disagree with the wizard configs now on disk. They match. The supported point is how that column was parsed, and that preflight blocks a delay that did not land.
