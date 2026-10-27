# In cut-in and lead-vehicle scenes that pass as recorded, which combinations of the car's timing, the car's speed and the ego's speed at hand-off make the policy collide or leave the road? The aim is the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `hybrid_optuna_r7`: 9 kept runs on 7 scenes, varying actor_time_shift_s, actor_speed_scale, ego_speed_scale; 51 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 0 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The study did not answer the question: it confirmed none of the 5 challenging cases it was looking for. Only one kept run failed. That was on 096988dd with the car 1 s earlier at 0.5x speed and the ego at 1.4x (S2). The ego's front touched a slower truck even though the policy braked hard. However, the gap was already very short at hand-off, and that came from the replay, so it is unclear whether the policy was at fault. A single failure is a hint, not a rate, and the range it leaves is too wide to say the setting fails more than half the time. The study was meant to confirm settings by repeating them, but the gate kept none of the many repeats. The other kept settings each ran once and passed, so they show nothing either way.

## Findings

- The only failure was on 096988dd: the car 1 s earlier at 0.5x speed, with the ego at 1.4x at hand-off. The ego caught up with a slower truck in its lane and touched it while braking hard. The short gap at hand-off came from the replay, not from the policy's driving. Triage could not say whether the policy was at fault, and the contact may be a replay artifact. This is one run, and its many repeats were not kept, so it is a candidate, not a confirmed case.
  - S2: 096988dd at actor_time_shift_s -1, actor_speed_scale 0.5, ego_speed_scale 1.4: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r7_008)
- No collisions or road departures occurred on the other kept settings. They covered 023b7fcc, 09a95ffa, 0cf6368d, 0e899dd3, 12855a41 and 19f339ba. Each setting ran only once, so none rules out failure. The broad ranges allow failure rates well above half.
  - S1: 023b7fcc at actor_time_shift_s -2, actor_speed_scale 2, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r7_004)
  - S3: 09a95ffa at actor_time_shift_s -2, actor_speed_scale 0.5, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r7_007)
  - S4: 0cf6368d at actor_time_shift_s -1.5, actor_speed_scale 2, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r7_011)
  - S5: 0cf6368d at actor_time_shift_s 0.5, actor_speed_scale 2, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r7_003)
  - S6: 0e899dd3 at actor_time_shift_s 0.5, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r7_002)
  - S7: 0e899dd3 at actor_time_shift_s 2, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r7_012)
  - S8: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 0.75, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r7_006)
  - S9: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 2, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r7_009)
- The closest calls among the passing runs, which the brief ranks next, scored highest on criticality. They were: 0e899dd3 with the car 2 s later at 1.5x and the ego at 1.2x; 023b7fcc with the car 2 s earlier at 2x and the ego at 1x; 19f339ba with the car 0.5 s earlier at 2x and the ego at 0.8x; and 12855a41 with the car 0.5 s earlier at 0.75x and the ego at 1x. They are the best places to search next, but each rests on a single run.
  - S7: 0e899dd3 at actor_time_shift_s 2, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r7_012)
  - S1: 023b7fcc at actor_time_shift_s -2, actor_speed_scale 2, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r7_004)
  - S9: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 2, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r7_009)
  - S8: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 0.75, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r7_006)
- On 0cf6368d, the setting with the car 1.5 s earlier at 2x and the ego slowed to 0.6x was the least critical of the kept settings. A faster car combined with a slower ego tended to open the gap rather than close it here.
  - S4: 0cf6368d at actor_time_shift_s -1.5, actor_speed_scale 2, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r7_011)
  - S5: 0cf6368d at actor_time_shift_s 0.5, actor_speed_scale 2, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r7_003)

## Open

- The study did not keep most of its runs. The repeats meant to confirm the candidates were all left out with no reason recorded ('not kept: None'). These were S2 on 096988dd, S1 on 023b7fcc, S7 on 0e899dd3, S9 on 19f339ba and S8 on 12855a41. Find out why the gate dropped them, then rerun about 5 repeats at each to confirm or rule out these settings.
- Is the failure on 096988dd (the car 1 s earlier at 0.5x, the ego at 1.4x) the policy's fault or a replay artifact? Repeats at that setting, plus one at the ego's recorded speed with the same car timing, would show whether the policy can avoid the contact when the replay does not hand it a tiny gap.
- Three scenes have no kept evidence at all because their runs halted: 187e6244, 1c45ce3a and 0dbb91dd. The cause of the halts needs fixing before they can be searched.
- Because so few runs were kept, most of the grid of the three knobs is unexplored. Whether 5 distinct scenes with failure rates above 0.5 exist at 2 Hz is still unknown.
- Nothing in the runs checks that the policy actually ran at the 2 Hz planning rate (only the control timestep was set to 500 ms).

## Why the runs failed (triage from the video and log)

no_brake_for_lead 1

- car_conflicts_3knobs_2hz_hybrid_optuna_r7_008: no_brake_for_lead, policy at fault: unclear. The ego was going straight on a wet freeway and closing fast on a slower white utility truck (actor 2) in its lane. At handoff (4.7 s) the gap was only 7.2 m with the ego at 7.9 m/s. The policy braked hard, down to 3.8 m/s, but its front still touched the truck at 5.7 s, and actor 41 behind then hit its rear. The ego stayed within about 0.4 m of where the human driver was, so this setup came from the replay before handoff, and the contact may be an artifact of how close the replayed truck was to the human's car.

## Every setting

- S1: 023b7fcc at actor_time_shift_s -2, actor_speed_scale 2, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r7_004)
- S2: 096988dd at actor_time_shift_s -1, actor_speed_scale 0.5, ego_speed_scale 1.4: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r7_008)
- S3: 09a95ffa at actor_time_shift_s -2, actor_speed_scale 0.5, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r7_007)
- S4: 0cf6368d at actor_time_shift_s -1.5, actor_speed_scale 2, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r7_011)
- S5: 0cf6368d at actor_time_shift_s 0.5, actor_speed_scale 2, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r7_003)
- S6: 0e899dd3 at actor_time_shift_s 0.5, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r7_002)
- S7: 0e899dd3 at actor_time_shift_s 2, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r7_012)
- S8: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 0.75, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r7_006)
- S9: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 2, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r7_009)

## Not kept by the gate

- car_conflicts_3knobs_2hz_hybrid_optuna_r7_001: not kept: HALT
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_005: not kept: HALT
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_010: not kept: HALT
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_013: not kept: HALT
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_014: not kept: HALT
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_015: not kept: HALT
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_016: not kept: HALT
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_017: not kept: None
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_018: not kept: None
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_019: not kept: None
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_020: not kept: None
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_021: not kept: None
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_022: not kept: None
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_023: not kept: None
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_024: not kept: None
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_025: not kept: None
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_026: not kept: None
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_027: not kept: None
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_028: not kept: None
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_029: not kept: None
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_030: not kept: None
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_031: not kept: None
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_032: not kept: None
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_033: not kept: None
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_034: not kept: None
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_035: not kept: None
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_036: not kept: None
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_037: not kept: None
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_038: not kept: None
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_039: not kept: None
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_040: not kept: None
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_041: not kept: None
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_042: not kept: None
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_043: not kept: None
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_044: not kept: None
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_045: not kept: None
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_046: not kept: None
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_047: not kept: None
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_048: not kept: None
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_049: not kept: None
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_050: not kept: None
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_051: not kept: None
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_052: not kept: None
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_053: not kept: None
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_054: not kept: None
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_055: not kept: None
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_056: not kept: None
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_057: not kept: None
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_058: not kept: None
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_059: not kept: None
- car_conflicts_3knobs_2hz_hybrid_optuna_r7_060: not kept: None

## Provenance

Plan: `plan.json` (rationale: Scene choice: these are the scenes tagged merge_cut_in or lead_vehicle that did not fail in the earlier run at the recorded setting, have a recorded car the study can retime (lead_vehicle or cut_in), and drove far enough for a conflict to develop. Most of them already came close to another actor as recorded: 023b7fcc came within 0.02 m, 096988dd 0.01 m, 19f339ba 0.03 m, 12855a41 0.08 m, and 0dbb91dd and 187e6244 0.23 m. Those are the most promising places to look for rare failures.

Left out:
- Scenes that were nearly stationary (0fa7060f, 15dd433e, 0ac02819, 10d64934) or very slow (01d503d4, 098e2482, 11fce928, 1bfd39ec).
- Scenes with no car the study can retime (for example 04749bb9, 05f35348, 0ce6f2a3, 166fe701).
- Scenes whose only key actor is a crossing vehicle at an intersection (02eadd92, 054b5901).

Note that 01d503d4 appears twice in the scene list.

Retiming and settings:
- Traffic is replay, as the brief asks, with retime_class automobile.
- Each scene retimes only its key car. In 12855a41 that is the cut-in car 31 rather than the lead car 5.
- All three knobs span exactly the ranges in the brief: timing ±2 s, car speed 0.5x to 2x, ego speed 0.6x to 1.4x.
- The controller is linear MPC.

Goal: top_k with k=5, distinct scenes, high_min 0.5. This matches the request for the 5 most challenging cases, each confirmed by repeats.

Limits:
- The budget is tight. With 90% ranges, a setting needs roughly 5 failures out of 5 runs to lie surely above 0.5. Confirming 5 cases therefore takes about 25 runs, which leaves about 35 runs to search a 270-cell grid on 10 scenes. If failures are as rare as the brief expects, the study may end with fewer than 5 confirmed cases. It would then report the strongest candidates and the near misses, which the brief ranks next.
- The 2 Hz planning rate is not a knob in this interface. The plan assumes the runs use VaVAM's 2 Hz rhythm as configured; nothing here sets it or checks it. planner_delay_us, lateral_bias_m and waypoint_noise_std stay at their defaults.
- A scale above 1 starts the ego behind its recorded start, so for the first second or two of the warm-up it is off the recording.). Report written by claude-opus-5-5 from `results` in 17 s; every count above is computed from the queue, not written by the model.

0 of 60 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
