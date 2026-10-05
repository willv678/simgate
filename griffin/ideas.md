# Griffin's ideas for SimGate (Fri 2 Oct)

Each idea is a way a run could give wrong data that still looks fine, or a new
job for the system, plus the check that would catch it. Only one hour today, so
nothing is built yet; the evidence column says what was looked at.

| Idea | Track | What it catches or fixes | Changes what a run measures? | Built? | Evidence |
|---|---|---|---|---|---|
| `lateral_bias` fault: shift the planned path sideways | B | A steady sideways offset, like a miscalibrated camera. Would be caught by a check on the mean signed offset from the recording or lane centre over the run | It is a fault, so yes, on purpose | No | One existing pair, 1.0 m bias (note 1). All four physics bounds pass; `offroad` and `wrong_lane` stay 0 |
| `freeze_plan` fault: follow a plan up to 1 s old | B | Sensor dropout or planner lag. Would be caught by counting control steps where the plan does not change, if the rollout log records the plan | Fault, yes | No | Not run. Guess: hides on straight roads, shows in turns |
| `waypoint_noise` fault: jitter every waypoint | B | Sensor noise. Tests whether the dropped jerk bound should come back as a comparison with the reference run instead of a fixed number | Fault, yes | No | `rules/physics.json`: jerk was dropped because clean S1 runs reach 30-101 m/s³ |
| `truncate_horizon` fault: cut the plan short | B | Planner timeout. May be loud: the simulator raises an error when no waypoints are left, which tests the Investigator on a new error | Fault, yes | No | `src/runtime/alpasim_runtime/plan_fault_injection.py` raises `ValueError` |
| Test plan faults with configs hidden | B | The plan faults are written in `wizard-config.yaml`, so a one-line rule catches them trivially. The honest test hides configs, as `eval_physics_audit.py` does, so it stands for a code bug no setting names | No | No | `fault_injection.lateral_bias_m: 1.0` is at line 304 of the bias run's `wizard-config.yaml` |
| Count hidden rollout retries | C | The simulator quietly retries a crashed rollout up to 2 times inside one run and keeps only the one that finished. Record the count, and give it to the Auditor in `physics.txt` | No, it only records | No | `diag/s1_059` has 3 rollouts, 1 with `_complete`; `runtime.max_rollout_retries: 2` |
| Lane keeping agrees with metrics | C | The ego drove 1 m off its plan while `offroad` and `wrong_lane` stayed 0. Check that the motion's distance to the lane edge agrees with `min_distance_to_lane_boundary_m` | No | No | Note 1: `min_distance_to_lane_boundary_m` fell 0.26 → 0.10 m; the lane flags did not move |
| CONFIGURE `runtime.inference.max_batch_size` | A | GPU out of memory in the driving model | Should not, but unchecked: needs a clean run at two values with the same metrics | No | `max_batch_size: 32` in `diag/s1_001/wizard-config.yaml` |
| CONFIGURE `scene_provider.trajdata.num_workers` | A | Out of memory or slow scene loading on the CPU side | Should not (data loading only); unchecked | No | `num_workers: 4` in the same file |
| Auditor explains a scene that keeps failing | D | Question: why does scene X fail across batches? Sees that scene's failed runs and logs. Answers one cause from a fixed list. Code acts only if the cause matches a status K⁻/K⁺ already records | No | No | Idea only |
| Auditor compares two batches for drift | D | Question: did the same config give different results this week? Sees two anonymized batches of the same config. Answers flagged metrics. Code acts only when a fixed statistical test agrees | No | No | Idea only |

## Notes

1. `diag/fault_injection_baseline` vs `diag/fault_injection_bias` (lateral
   bias 1.0 m), one scene, one run each, so this is a hint and not a result:

   | | baseline | bias |
   |---|---|---|
   | `dist_to_gt_trajectory` (mean) | 0.44 | 3.43 |
   | `min_distance_to_lane_boundary_m` (mean) | 0.26 | 0.10 |
   | `offroad`, `wrong_lane` | 0, 0 | 0, 0 |
   | max accel / yaw rate | 4.6 / 0.19 | 4.9 / 0.35 (bounds 10 / 2) |
   | closest car ahead | 5.4 m | 0.25 m, a collision was scored |

   The physics bounds do not fire. `dist_to_gt_trajectory` moves a lot, but a
   policy that drives badly also moves it, so it is not a fault check by itself.

## Next steps

- Add `lateral_bias` and `freeze_plan` to `faults.py` with tests, then run
  4 + 4 + 2 clean in `research/harness/g_plan_queue`.
- Run the Auditor with configs hidden on that batch.
