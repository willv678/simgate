# In cut-in and lead-vehicle scenes that pass as recorded, which combinations of the car's timing, the car's speed and the ego's speed at hand-off make the policy collide or leave the road? The aim is the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `rules_r5`: 60 kept runs on 10 scenes, varying actor_time_shift_s, actor_speed_scale, ego_speed_scale; 1 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 0 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The study found no combination that makes the policy collide or leave the road, and it confirmed none of the 5 cases it was looking for (the goal was not met). No kept run failed, so there was nothing to triage. This says little about the three-knob space, because the search barely covered it. Nine of the ten scenes were only run at one setting: the car on time, at 1.25x speed, with the ego at its recorded speed. Those repeats only show that this setting fails rarely: each scene's failure rate there is below about a third. The ego's speed was never changed, and the car's speed never went outside 1.0x to 1.25x. So rare failures elsewhere in the space are not ruled out.

## Findings

- With the car on time, at 1.25x speed, and the ego at its recorded speed, no repeated run failed on any of the nine scenes run there. Each scene's failure rate at this setting is below about a third, well short of the 0.5 the goal required.
  - S1: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r5_001, car_conflicts_3knobs_2hz_rules_r5_018, car_conflicts_3knobs_2hz_rules_r5_028, car_conflicts_3knobs_2hz_rules_r5_038, car_conflicts_3knobs_2hz_rules_r5_047, car_conflicts_3knobs_2hz_rules_r5_058)
  - S2: 096988dd at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r5_002, car_conflicts_3knobs_2hz_rules_r5_012, car_conflicts_3knobs_2hz_rules_r5_021, car_conflicts_3knobs_2hz_rules_r5_031, car_conflicts_3knobs_2hz_rules_r5_041, car_conflicts_3knobs_2hz_rules_r5_051)
  - S3: 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r5_008, car_conflicts_3knobs_2hz_rules_r5_015, car_conflicts_3knobs_2hz_rules_r5_024, car_conflicts_3knobs_2hz_rules_r5_034, car_conflicts_3knobs_2hz_rules_r5_044, car_conflicts_3knobs_2hz_rules_r5_056)
  - S4: 0cf6368d at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r5_007, car_conflicts_3knobs_2hz_rules_r5_017, car_conflicts_3knobs_2hz_rules_r5_027, car_conflicts_3knobs_2hz_rules_r5_037, car_conflicts_3knobs_2hz_rules_r5_048_a2, car_conflicts_3knobs_2hz_rules_r5_057)
  - S11: 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r5_009, car_conflicts_3knobs_2hz_rules_r5_016, car_conflicts_3knobs_2hz_rules_r5_025, car_conflicts_3knobs_2hz_rules_r5_036, car_conflicts_3knobs_2hz_rules_r5_046, car_conflicts_3knobs_2hz_rules_r5_055)
  - S12: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r5_003, car_conflicts_3knobs_2hz_rules_r5_013, car_conflicts_3knobs_2hz_rules_r5_023, car_conflicts_3knobs_2hz_rules_r5_033, car_conflicts_3knobs_2hz_rules_r5_045, car_conflicts_3knobs_2hz_rules_r5_054)
  - S13: 187e6244 at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r5_005, car_conflicts_3knobs_2hz_rules_r5_019, car_conflicts_3knobs_2hz_rules_r5_029, car_conflicts_3knobs_2hz_rules_r5_039, car_conflicts_3knobs_2hz_rules_r5_049, car_conflicts_3knobs_2hz_rules_r5_059)
  - S14: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r5_004, car_conflicts_3knobs_2hz_rules_r5_014, car_conflicts_3knobs_2hz_rules_r5_022, car_conflicts_3knobs_2hz_rules_r5_032, car_conflicts_3knobs_2hz_rules_r5_042, car_conflicts_3knobs_2hz_rules_r5_053)
  - S15: 1c45ce3a at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r5_010, car_conflicts_3knobs_2hz_rules_r5_011, car_conflicts_3knobs_2hz_rules_r5_026, car_conflicts_3knobs_2hz_rules_r5_035, car_conflicts_3knobs_2hz_rules_r5_043, car_conflicts_3knobs_2hz_rules_r5_052)
- At that same setting, the closest calls came on 096988dd, then 19f339ba, 12855a41 and 0e899dd3. These are the best places to look next. 187e6244, 023b7fcc and 0cf6368d were the least critical.
  - S2: 096988dd at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r5_002, car_conflicts_3knobs_2hz_rules_r5_012, car_conflicts_3knobs_2hz_rules_r5_021, car_conflicts_3knobs_2hz_rules_r5_031, car_conflicts_3knobs_2hz_rules_r5_041, car_conflicts_3knobs_2hz_rules_r5_051)
  - S14: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r5_004, car_conflicts_3knobs_2hz_rules_r5_014, car_conflicts_3knobs_2hz_rules_r5_022, car_conflicts_3knobs_2hz_rules_r5_032, car_conflicts_3knobs_2hz_rules_r5_042, car_conflicts_3knobs_2hz_rules_r5_053)
  - S12: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r5_003, car_conflicts_3knobs_2hz_rules_r5_013, car_conflicts_3knobs_2hz_rules_r5_023, car_conflicts_3knobs_2hz_rules_r5_033, car_conflicts_3knobs_2hz_rules_r5_045, car_conflicts_3knobs_2hz_rules_r5_054)
  - S11: 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r5_009, car_conflicts_3knobs_2hz_rules_r5_016, car_conflicts_3knobs_2hz_rules_r5_025, car_conflicts_3knobs_2hz_rules_r5_036, car_conflicts_3knobs_2hz_rules_r5_046, car_conflicts_3knobs_2hz_rules_r5_055)
  - S13: 187e6244 at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r5_005, car_conflicts_3knobs_2hz_rules_r5_019, car_conflicts_3knobs_2hz_rules_r5_029, car_conflicts_3knobs_2hz_rules_r5_039, car_conflicts_3knobs_2hz_rules_r5_049, car_conflicts_3knobs_2hz_rules_r5_059)
  - S1: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r5_001, car_conflicts_3knobs_2hz_rules_r5_018, car_conflicts_3knobs_2hz_rules_r5_028, car_conflicts_3knobs_2hz_rules_r5_038, car_conflicts_3knobs_2hz_rules_r5_047, car_conflicts_3knobs_2hz_rules_r5_058)
  - S4: 0cf6368d at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r5_007, car_conflicts_3knobs_2hz_rules_r5_017, car_conflicts_3knobs_2hz_rules_r5_027, car_conflicts_3knobs_2hz_rules_r5_037, car_conflicts_3knobs_2hz_rules_r5_048_a2, car_conflicts_3knobs_2hz_rules_r5_057)
- On 0dbb91dd, moving the car anywhere from 2 s earlier to on time (at 1.25x, plus one run at 1.0x and 2 s earlier) never failed. It also scored zero criticality, which suggests the retimed car may never have come near the ego there. These are single runs, so they are hints, not rates.
  - S5: 0dbb91dd at actor_time_shift_s -2.0, actor_speed_scale 1.0, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_rules_r5_060)
  - S6: 0dbb91dd at actor_time_shift_s -2.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_rules_r5_050)
  - S7: 0dbb91dd at actor_time_shift_s -1.5, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_rules_r5_040)
  - S8: 0dbb91dd at actor_time_shift_s -1.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_rules_r5_030)
  - S9: 0dbb91dd at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_rules_r5_020)
  - S10: 0dbb91dd at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_rules_r5_006)
- No failures came from the simulator. Every kept run passed, none was flagged as a possible artifact, and the one run the gate dropped (a re-run on 0cf6368d) was replaced and also passed.
  - S4: 0cf6368d at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r5_007, car_conflicts_3knobs_2hz_rules_r5_017, car_conflicts_3knobs_2hz_rules_r5_027, car_conflicts_3knobs_2hz_rules_r5_037, car_conflicts_3knobs_2hz_rules_r5_048_a2, car_conflicts_3knobs_2hz_rules_r5_057)

## Open

- The ego's speed at hand-off was never varied (every run used 1.0x). Run 0.6x and 1.4x on the most critical scenes (096988dd, 19f339ba, 12855a41, 0e899dd3), with the car shifted by up to ±2 s.
- The car's speed was never tried below 1.0x or above 1.25x. A slow lead (0.5x) combined with a fast ego (1.4x), and a fast cut-in (2x) arriving 1 to 2 s earlier, are the most likely ways to fail and were not run.
- Timing was only explored on 0dbb91dd, where the car seems never to have come near the ego. On the other scenes, try timing changes away from 0 s, one run per cell, and save repeats for settings that fail or nearly fail.
- The 2 Hz planning rate was set through the control timestep but not checked independently. Confirm that the runs actually planned every 500 ms.
- If no setting fails after a broader search, the brief's fallback is to rank near misses. That needs runs across the corners of the grid, not more repeats of the one setting run here.

## Every setting

- S1: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r5_001, car_conflicts_3knobs_2hz_rules_r5_018, car_conflicts_3knobs_2hz_rules_r5_028, car_conflicts_3knobs_2hz_rules_r5_038, car_conflicts_3knobs_2hz_rules_r5_047, car_conflicts_3knobs_2hz_rules_r5_058)
- S2: 096988dd at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r5_002, car_conflicts_3knobs_2hz_rules_r5_012, car_conflicts_3knobs_2hz_rules_r5_021, car_conflicts_3knobs_2hz_rules_r5_031, car_conflicts_3knobs_2hz_rules_r5_041, car_conflicts_3knobs_2hz_rules_r5_051)
- S3: 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r5_008, car_conflicts_3knobs_2hz_rules_r5_015, car_conflicts_3knobs_2hz_rules_r5_024, car_conflicts_3knobs_2hz_rules_r5_034, car_conflicts_3knobs_2hz_rules_r5_044, car_conflicts_3knobs_2hz_rules_r5_056)
- S4: 0cf6368d at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r5_007, car_conflicts_3knobs_2hz_rules_r5_017, car_conflicts_3knobs_2hz_rules_r5_027, car_conflicts_3knobs_2hz_rules_r5_037, car_conflicts_3knobs_2hz_rules_r5_048_a2, car_conflicts_3knobs_2hz_rules_r5_057)
- S5: 0dbb91dd at actor_time_shift_s -2.0, actor_speed_scale 1.0, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_rules_r5_060)
- S6: 0dbb91dd at actor_time_shift_s -2.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_rules_r5_050)
- S7: 0dbb91dd at actor_time_shift_s -1.5, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_rules_r5_040)
- S8: 0dbb91dd at actor_time_shift_s -1.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_rules_r5_030)
- S9: 0dbb91dd at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_rules_r5_020)
- S10: 0dbb91dd at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_rules_r5_006)
- S11: 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r5_009, car_conflicts_3knobs_2hz_rules_r5_016, car_conflicts_3knobs_2hz_rules_r5_025, car_conflicts_3knobs_2hz_rules_r5_036, car_conflicts_3knobs_2hz_rules_r5_046, car_conflicts_3knobs_2hz_rules_r5_055)
- S12: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r5_003, car_conflicts_3knobs_2hz_rules_r5_013, car_conflicts_3knobs_2hz_rules_r5_023, car_conflicts_3knobs_2hz_rules_r5_033, car_conflicts_3knobs_2hz_rules_r5_045, car_conflicts_3knobs_2hz_rules_r5_054)
- S13: 187e6244 at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r5_005, car_conflicts_3knobs_2hz_rules_r5_019, car_conflicts_3knobs_2hz_rules_r5_029, car_conflicts_3knobs_2hz_rules_r5_039, car_conflicts_3knobs_2hz_rules_r5_049, car_conflicts_3knobs_2hz_rules_r5_059)
- S14: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r5_004, car_conflicts_3knobs_2hz_rules_r5_014, car_conflicts_3knobs_2hz_rules_r5_022, car_conflicts_3knobs_2hz_rules_r5_032, car_conflicts_3knobs_2hz_rules_r5_042, car_conflicts_3knobs_2hz_rules_r5_053)
- S15: 1c45ce3a at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r5_010, car_conflicts_3knobs_2hz_rules_r5_011, car_conflicts_3knobs_2hz_rules_r5_026, car_conflicts_3knobs_2hz_rules_r5_035, car_conflicts_3knobs_2hz_rules_r5_043, car_conflicts_3knobs_2hz_rules_r5_052)

## Not kept by the gate

- car_conflicts_3knobs_2hz_rules_r5_048: not kept: RE-RUN

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
- A scale above 1 starts the ego behind its recorded start, so for the first second or two of the warm-up it is off the recording.). Report written by claude-opus-5-5 from `results` in 14 s; every count above is computed from the queue, not written by the model.

0 of 61 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
