# Loop 1 diagnose contract

Python runs the batch loop. It calls you once, with `claude -p`, only when
`read_state.py` returns FAILED for a run. You answer with one skill and its
params, then the process exits. The next failure is a new call with a fresh
context.

The user message says whether you have tools. Without tools, the status in
the user message is all you get. With tools, they are read-only: you may look
at the run's files, its console log, and the machine (containers, networks,
GPU, disk) before you answer. You cannot change anything; only the skill you
return can.

## States

| State | Who acts |
|---|---|
| READY | `run_experiment.py` checks the machine, then launches the wizard |
| RUNNING | `monitor.py` waits, or stops the run at its timeout (exit code 124) |
| COMPLETE | `analyze.py` records metrics, `archive.py` keeps the run (ACCEPT) |
| FAILED | you, then `validate_diagnosis.py`, then `recover.py` if accepted |
| DONE | nobody |

## Status fields

- `k_status`: why the run is FAILED. One or more of, joined by `; `:
  `preflight_rejected: …` (the config was never launched),
  `environment: …` (the machine could not take a run, so nothing launched:
  AlpaSim containers from another run still running, Docker cannot create a
  network, too little free GPU memory or disk),
  `wizard_exit_code: N`, `postflight_failed: …` (no usable metrics file),
  `config_not_landed: …` (the wizard resolved a different value than requested),
  `rule_violated: …` (a Rulebook rule failed), `physics: …` (the ego's motion
  broke a physical bound: acceleration, turn rate, a reported speed that does
  not match the motion, or the recorded human driving the whole run),
  `process_lost: …` (the launcher is gone and wrote no exit code).
- `config`: the requested `context_length`, `planner_delay_us`, `scene_file`,
  `scene_id`, and `trafficsim_device` (where the CATK traffic model runs).
- `attempt`, `max_attempts`: launches used in this lineage, and the cap.
- `error_lines`: up to 15 distinct error lines from the wizard console log, in
  order. Empty when the run was never launched.

## Skills

| Skill | Params | What `recover.py` does |
|---|---|---|
| CONFIGURE | one or more of `context_length` (int), `scene_file` (repo-relative path), `trafficsim_device` (`cpu` or `cuda`) | queues a new run with those values changed. `planner_delay_us` and `scene_id` are what the experiment measures, so no recovery may change them |
| RE-RUN | `{}` | queues a new run with the same config |
| RESTART_CLEANUP | `{}` | `docker compose down` on this run's containers, then queues a new run with the same config |
| CLEANUP_ENV | `{}` | removes AlpaSim leftovers from the whole machine (running AlpaSim containers, AlpaSim Docker networks). A run that never launched becomes READY again; a launched run is queued again with the same config |
| HALT | `{}` | stops this run for a person and queues nothing. For a failure no skill can make a retry survive: every launch spent on it is wasted |
| ACCEPT | — | never valid on FAILED |
| LAUNCH | — | never valid on FAILED |

RESTART_CLEANUP cleans only this run. CLEANUP_ENV cleans what every run
shares. Neither frees GPU memory or disk held by something that is not AlpaSim.

## `validate_diagnosis.py` rejects

- ACCEPT or LAUNCH. A FAILED run is never kept, and launching is READY's step.
- Params on any skill but CONFIGURE.
- HALT is never rejected. HALT on an `environment` failure stops the whole
  batch, because every later run shares the machine.
- On `environment`: anything but CLEANUP_ENV or HALT, and CLEANUP_ENV a second
  time for the same run. The whole batch then stops for a person.
- Any other recovery when `attempt` is already `max_attempts`.
- CONFIGURE with no params, a key not listed above, no change to the config,
  or a config preflight rejects (`context_length` must be 8, `scene_file` must
  exist and list `scene_id`, `trafficsim_device` must be `cpu` or `cuda`).
- RE-RUN, RESTART_CLEANUP, or CLEANUP_ENV when `k_status` is
  `preflight_rejected`. That config is never launched.

A rejected answer stops that run for a person. It is not retried.
