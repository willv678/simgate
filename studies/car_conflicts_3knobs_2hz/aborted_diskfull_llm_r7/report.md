# In cut-in and lead-vehicle scenes that pass as recorded, which combinations of the car's timing, the car's speed and the ego's speed at hand-off make the policy collide or leave the road? The aim is the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `llm_r7`: 11 kept runs on 6 scenes, varying actor_time_shift_s, actor_speed_scale, ego_speed_scale; 49 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 0 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The study did not find the 5 confirmed challenging cases. It confirmed none, which agrees with the goal status. Only one kept run failed, on scene 096988dd with the car's timing and speed as recorded and the ego at 1.4x its recorded speed at hand-off. The policy was at fault: it steered left out of its path and hit a car coming up from behind-left in the next lane. That car (actor 41) is not the retimed one, so this failure points to the ego's speed rather than the cut-in car's timing or speed. That is one run, so it is a hint, not a rate; its range still reaches well below 0.5. Most of the budget was lost, because the gate kept only a small part of the runs. Every attempt to repeat the failing setting was dropped, so the main question is still open.

## Findings

- The only failure came on 096988dd at actor shift 0 s, actor speed 1.0x and ego speed 1.4x. The policy turned left out of its lane into a car (actor 41) coming up from behind-left and hit it with the front of the ego. The policy was at fault. This is a single run and is not confirmed.
  - S6: 096988dd at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1.4: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_llm_r7_002)
- On the same scene, the same car timing and speed with the ego at its recorded speed passed, and so did a 0.5 s earlier, 1.25x faster car at the recorded ego speed. In this scene, the higher ego speed at hand-off is the knob linked to the failure.
  - S5: 096988dd at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r7_012)
  - S4: 096988dd at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r7_011)
  - S6: 096988dd at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1.4: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_llm_r7_002)
- The same combination that failed on 096988dd (recorded car timing and speed, ego at 1.4x) passed on 12855a41, so it is not a failure across scenes.
  - S9: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r7_008)
  - S6: 096988dd at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1.4: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_llm_r7_002)
- Pushing all three knobs hard (car 1 s earlier, 1.5x speed, ego 1.4x) caused no failure on 023b7fcc, 12855a41, 187e6244 or 0dbb91dd. Each of these settings had a single run. On 0dbb91dd that setting produced no conflict at all.
  - S2: 023b7fcc at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r7_003)
  - S8: 12855a41 at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r7_007)
  - S10: 187e6244 at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r7_009)
  - S7: 0dbb91dd at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r7_010)
- The closest calls that did not fail, which the brief ranks next, were on 096988dd (car 0.5 s earlier at 1.25x, ego at recorded speed) and on 023b7fcc and 19f339ba with strong car retiming. They are the best candidates to search around.
  - S4: 096988dd at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r7_011)
  - S2: 023b7fcc at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r7_003)
  - S11: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r7_015)

## Open

- Whether the S6 failure repeats: about 20 repeats of 096988dd at shift 0 s, car speed 1.0x, ego 1.4x were run, but the gate kept none of them. Most were dropped with no reason given (verdict 'None'), so the gate or pipeline problem needs fixing first. Then about 5 kept repeats at that setting would settle whether its failure rate is above 0.5.
- Why most runs were not kept: early runs ended in HALT, and later runs were dropped with no verdict. Until this is fixed, the 60-run budget cannot cover the search, let alone confirmation.
- No failure was found on 023b7fcc, 12855a41, 187e6244, 0dbb91dd or 19f339ba, and none at all was tried on 0cf6368d, 09a95ffa, 0e899dd3 or 1c45ce3a. With single runs per setting, rare failures cannot be ruled out anywhere. More of the grid needs kept runs, especially around the near misses at S4, S2 and S11 and at car shifts later than recorded (positive values), which were never tried.
- Whether the S6 failure is about the retimed car at all: the car hit was not the retimed car 2. Runs on 096988dd at ego 1.4x with different car timings would show whether it is purely the ego's speed.
- The 2 Hz planning rate was set through control_timestep_us 500 ms, but nothing in the results confirms the policy actually planned at 2 Hz.

## Why the runs failed (triage from the video and log)

turned_into_actor 1

- car_conflicts_3knobs_2hz_llm_r7_002: turned_into_actor, policy at fault: yes. On a multi-lane freeway with a STRAIGHT command (later RIGHT), the policy slowed down and steered left toward the next lane over, leaving the recorded path. It cut into actor 41, which was coming up in that left lane from behind-left, and the front of the ego hit it at 7.2s.

## Every setting

- S1: 023b7fcc at actor_time_shift_s -1, actor_speed_scale 1, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r7_014)
- S2: 023b7fcc at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r7_003)
- S3: 023b7fcc at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r7_013)
- S4: 096988dd at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r7_011)
- S5: 096988dd at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r7_012)
- S6: 096988dd at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1.4: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_llm_r7_002)
- S7: 0dbb91dd at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r7_010)
- S8: 12855a41 at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r7_007)
- S9: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r7_008)
- S10: 187e6244 at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r7_009)
- S11: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r7_015)

## Not kept by the gate

- car_conflicts_3knobs_2hz_llm_r7_001: not kept: HALT
- car_conflicts_3knobs_2hz_llm_r7_004: not kept: HALT
- car_conflicts_3knobs_2hz_llm_r7_005: not kept: HALT
- car_conflicts_3knobs_2hz_llm_r7_006: not kept: HALT
- car_conflicts_3knobs_2hz_llm_r7_016: not kept: HALT
- car_conflicts_3knobs_2hz_llm_r7_017: not kept: HALT
- car_conflicts_3knobs_2hz_llm_r7_018: not kept: None
- car_conflicts_3knobs_2hz_llm_r7_019: not kept: None
- car_conflicts_3knobs_2hz_llm_r7_020: not kept: None
- car_conflicts_3knobs_2hz_llm_r7_021: not kept: None
- car_conflicts_3knobs_2hz_llm_r7_022: not kept: None
- car_conflicts_3knobs_2hz_llm_r7_023: not kept: None
- car_conflicts_3knobs_2hz_llm_r7_024: not kept: None
- car_conflicts_3knobs_2hz_llm_r7_025: not kept: None
- car_conflicts_3knobs_2hz_llm_r7_026: not kept: None
- car_conflicts_3knobs_2hz_llm_r7_027: not kept: None
- car_conflicts_3knobs_2hz_llm_r7_028: not kept: None
- car_conflicts_3knobs_2hz_llm_r7_029: not kept: None
- car_conflicts_3knobs_2hz_llm_r7_030: not kept: None
- car_conflicts_3knobs_2hz_llm_r7_031: not kept: None
- car_conflicts_3knobs_2hz_llm_r7_032: not kept: None
- car_conflicts_3knobs_2hz_llm_r7_033: not kept: None
- car_conflicts_3knobs_2hz_llm_r7_034: not kept: None
- car_conflicts_3knobs_2hz_llm_r7_035: not kept: None
- car_conflicts_3knobs_2hz_llm_r7_036: not kept: None
- car_conflicts_3knobs_2hz_llm_r7_037: not kept: None
- car_conflicts_3knobs_2hz_llm_r7_038: not kept: None
- car_conflicts_3knobs_2hz_llm_r7_039: not kept: None
- car_conflicts_3knobs_2hz_llm_r7_040: not kept: None
- car_conflicts_3knobs_2hz_llm_r7_041: not kept: None
- car_conflicts_3knobs_2hz_llm_r7_042: not kept: None
- car_conflicts_3knobs_2hz_llm_r7_043: not kept: None
- car_conflicts_3knobs_2hz_llm_r7_044: not kept: None
- car_conflicts_3knobs_2hz_llm_r7_045: not kept: None
- car_conflicts_3knobs_2hz_llm_r7_046: not kept: None
- car_conflicts_3knobs_2hz_llm_r7_047: not kept: None
- car_conflicts_3knobs_2hz_llm_r7_048: not kept: None
- car_conflicts_3knobs_2hz_llm_r7_049: not kept: None
- car_conflicts_3knobs_2hz_llm_r7_050: not kept: None
- car_conflicts_3knobs_2hz_llm_r7_051: not kept: None
- car_conflicts_3knobs_2hz_llm_r7_052: not kept: None
- car_conflicts_3knobs_2hz_llm_r7_053: not kept: None
- car_conflicts_3knobs_2hz_llm_r7_054: not kept: None
- car_conflicts_3knobs_2hz_llm_r7_055: not kept: None
- car_conflicts_3knobs_2hz_llm_r7_056: not kept: None
- car_conflicts_3knobs_2hz_llm_r7_057: not kept: None
- car_conflicts_3knobs_2hz_llm_r7_058: not kept: None
- car_conflicts_3knobs_2hz_llm_r7_059: not kept: None
- car_conflicts_3knobs_2hz_llm_r7_060: not kept: None

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
- A scale above 1 starts the ego behind its recorded start, so for the first second or two of the warm-up it is off the recording.). Report written by claude-opus-5-5 from `results` in 27 s; every count above is computed from the queue, not written by the model.

0 of 60 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
