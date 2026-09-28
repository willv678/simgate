# Loop 1 diagnose contract

Python runs the batch loop. It calls you once, with `claude -p`, only when
`read_state.py` returns FAILED for a run. You answer with one skill and its
params, then the process exits. You have no tools. The status in the user
message is all you get. The next failure is a new call with a fresh context.

## States

| State | Who acts |
|---|---|
| READY | `run_experiment.py` launches the wizard |
| RUNNING | `monitor.py` waits, or stops the run at its timeout (exit code 124) |
| COMPLETE | `analyze.py` records metrics, `archive.py` keeps the run (ACCEPT) |
| FAILED | you, then `validate_diagnosis.py`, then `recover.py` if accepted |
| DONE | nobody |

## Status fields

- `k_status`: why the run is FAILED. One or more of, joined by `; `:
  `preflight_rejected: …` (the config was never launched),
  `wizard_exit_code: N`, `postflight_failed: …` (no usable metrics file),
  `config_not_landed: …` (the wizard resolved a different value than requested),
  `process_lost: …` (the launcher is gone and wrote no exit code).
- `config`: the requested `context_length`, `planner_delay_us`, `scene_file`.
- `attempt`, `max_attempts`: launches used in this lineage, and the cap.
- `error_lines`: up to 15 distinct error lines from the wizard console log, in
  order. Empty when the run was never launched.

## Skills

| Skill | Params | What `recover.py` does |
|---|---|---|
| CONFIGURE | one or more of `context_length` (int), `planner_delay_us` (int), `scene_file` (repo-relative path) | queues a new run with those values changed |
| RE-RUN | `{}` | queues a new run with the same config |
| RESTART_CLEANUP | `{}` | `docker compose down` on the failed run's containers, then queues a new run with the same config |
| ACCEPT | — | never valid on FAILED |
| LAUNCH | — | never valid on FAILED |

## `validate_diagnosis.py` rejects

- ACCEPT or LAUNCH. A FAILED run is never kept, and launching is READY's step.
- Any recovery when `attempt` is already `max_attempts`.
- CONFIGURE with no params, a key not listed above, no change to the config, or
  a config preflight rejects (`context_length` must be 8, `scene_file` must exist).
- RE-RUN or RESTART_CLEANUP when `k_status` is `preflight_rejected`. That
  config is never launched.

A rejected answer stops that run for a person. It is not retried.
