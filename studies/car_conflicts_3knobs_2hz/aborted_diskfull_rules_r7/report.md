# In cut-in and lead-vehicle scenes that pass as recorded, which combinations of the car's timing, the car's speed and the ego's speed at hand-off make the policy collide or leave the road? The aim is the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `rules_r7`: 20 kept runs on 10 scenes, varying actor_time_shift_s, actor_speed_scale, ego_speed_scale; 43 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 0 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The study did not find a combination that makes the policy collide or leave the road, and it confirmed none of the 5 cases it was looking for. That fits the verdict above. This is not evidence that the policy is safe across the space, because the search never really explored it. Every kept run used the same setting on all ten scenes: car timing 0 s, car speed 1.25x, ego speed 1.0x. The ego-speed and timing knobs were never varied in a run that was kept. None of these runs failed, but the 90% ranges at each scene are wide and still allow a large failure rate at this setting. Two scenes rest on a single run, which is a hint and not a rate. The run-to-run spread came almost entirely from the gate: about two thirds of the budget was not kept, so it counts for nothing.

## Findings

- At car timing 0 s, car speed 1.25x and ego speed 1.0x, no kept run failed on any of the ten scenes. There were no possible simulator artifacts and nothing to triage.
  - S1: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_rules_r7_001, car_conflicts_3knobs_2hz_rules_r7_016)
  - S2: 096988dd at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_rules_r7_002, car_conflicts_3knobs_2hz_rules_r7_021)
  - S3: 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_rules_r7_008_a2, car_conflicts_3knobs_2hz_rules_r7_015)
  - S4: 0cf6368d at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_rules_r7_007, car_conflicts_3knobs_2hz_rules_r7_018)
  - S5: 0dbb91dd at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_rules_r7_006)
  - S6: 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_rules_r7_009, car_conflicts_3knobs_2hz_rules_r7_014)
  - S7: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_rules_r7_003_a3, car_conflicts_3knobs_2hz_rules_r7_012, car_conflicts_3knobs_2hz_rules_r7_022)
  - S8: 187e6244 at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_rules_r7_005)
  - S9: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_rules_r7_004, car_conflicts_3knobs_2hz_rules_r7_013, car_conflicts_3knobs_2hz_rules_r7_023)
  - S10: 1c45ce3a at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_rules_r7_010, car_conflicts_3knobs_2hz_rules_r7_017)
- The kept runs cover only one point of the three-knob space. Ego speed stayed at 1.0x and car timing at 0 s everywhere, so the study says nothing about earlier or later cut-ins, slower lead cars, or a faster or slower ego at hand-off.
  - S1: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_rules_r7_001, car_conflicts_3knobs_2hz_rules_r7_016)
  - S2: 096988dd at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_rules_r7_002, car_conflicts_3knobs_2hz_rules_r7_021)
  - S3: 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_rules_r7_008_a2, car_conflicts_3knobs_2hz_rules_r7_015)
  - S4: 0cf6368d at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_rules_r7_007, car_conflicts_3knobs_2hz_rules_r7_018)
  - S5: 0dbb91dd at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_rules_r7_006)
  - S6: 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_rules_r7_009, car_conflicts_3knobs_2hz_rules_r7_014)
  - S7: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_rules_r7_003_a3, car_conflicts_3knobs_2hz_rules_r7_012, car_conflicts_3knobs_2hz_rules_r7_022)
  - S8: 187e6244 at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_rules_r7_005)
  - S9: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_rules_r7_004, car_conflicts_3knobs_2hz_rules_r7_013, car_conflicts_3knobs_2hz_rules_r7_023)
  - S10: 1c45ce3a at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_rules_r7_010, car_conflicts_3knobs_2hz_rules_r7_017)
- The best leads for a near miss are the scenes with the highest criticality at this setting: 096988dd, then 12855a41 and 19f339ba. They are the best places to start searching for rare failures.
  - S2: 096988dd at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_rules_r7_002, car_conflicts_3knobs_2hz_rules_r7_021)
  - S7: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_rules_r7_003_a3, car_conflicts_3knobs_2hz_rules_r7_012, car_conflicts_3knobs_2hz_rules_r7_022)
  - S9: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_rules_r7_004, car_conflicts_3knobs_2hz_rules_r7_013, car_conflicts_3knobs_2hz_rules_r7_023)
- 0dbb91dd scored zero criticality at this setting in its single kept run, so it looks like the least promising scene here. One run is only a hint.
  - S5: 0dbb91dd at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_rules_r7_006)
- Even where the most runs were kept, the 90% range still includes rates close to the 0.5 confirmation bar. The scenes with a single run (0dbb91dd, 187e6244) allow even higher rates. A clean record at this setting therefore cannot rule out a real failure rate.
  - S7: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_rules_r7_003_a3, car_conflicts_3knobs_2hz_rules_r7_012, car_conflicts_3knobs_2hz_rules_r7_022)
  - S9: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_rules_r7_004, car_conflicts_3knobs_2hz_rules_r7_013, car_conflicts_3knobs_2hz_rules_r7_023)
  - S5: 0dbb91dd at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_rules_r7_006)
  - S8: 187e6244 at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_rules_r7_005)

## Open

- Why runs r7_026 to r7_060 were not kept (their gate verdict is None). They make up most of the budget, and they all repeat the same setting instead of searching. The search or the gate needs fixing before the study is re-run.
- Why runs r7_011, 019, 020, 024 and 025 halted, and why r7_003 and r7_008 needed re-runs. These are possible problems with the simulator or setup.
- The only probe off the starting setting, timing -0.5 s on 0dbb91dd (r7_020, 030, 040, 050, 060), produced no kept run. That point is still untested.
- The question itself is still open. The search needs to vary all three knobs (timing ±2 s, car speed 0.5x–2x, ego speed 0.6x–1.4x), starting on 096988dd, 12855a41 and 19f339ba. Any setting that fails should be repeated about five times to confirm it.
- The 2 Hz planning rate (control_timestep_us 500000) was configured but not checked in the runs.

## Every setting

- S1: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_rules_r7_001, car_conflicts_3knobs_2hz_rules_r7_016)
- S2: 096988dd at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_rules_r7_002, car_conflicts_3knobs_2hz_rules_r7_021)
- S3: 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_rules_r7_008_a2, car_conflicts_3knobs_2hz_rules_r7_015)
- S4: 0cf6368d at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_rules_r7_007, car_conflicts_3knobs_2hz_rules_r7_018)
- S5: 0dbb91dd at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_rules_r7_006)
- S6: 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_rules_r7_009, car_conflicts_3knobs_2hz_rules_r7_014)
- S7: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_rules_r7_003_a3, car_conflicts_3knobs_2hz_rules_r7_012, car_conflicts_3knobs_2hz_rules_r7_022)
- S8: 187e6244 at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_rules_r7_005)
- S9: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_rules_r7_004, car_conflicts_3knobs_2hz_rules_r7_013, car_conflicts_3knobs_2hz_rules_r7_023)
- S10: 1c45ce3a at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_rules_r7_010, car_conflicts_3knobs_2hz_rules_r7_017)

## Not kept by the gate

- car_conflicts_3knobs_2hz_rules_r7_003: not kept: RE-RUN
- car_conflicts_3knobs_2hz_rules_r7_008: not kept: RE-RUN
- car_conflicts_3knobs_2hz_rules_r7_003_a2: not kept: RE-RUN
- car_conflicts_3knobs_2hz_rules_r7_011: not kept: HALT
- car_conflicts_3knobs_2hz_rules_r7_019: not kept: HALT
- car_conflicts_3knobs_2hz_rules_r7_020: not kept: HALT
- car_conflicts_3knobs_2hz_rules_r7_024: not kept: HALT
- car_conflicts_3knobs_2hz_rules_r7_025: not kept: HALT
- car_conflicts_3knobs_2hz_rules_r7_026: not kept: None
- car_conflicts_3knobs_2hz_rules_r7_027: not kept: None
- car_conflicts_3knobs_2hz_rules_r7_028: not kept: None
- car_conflicts_3knobs_2hz_rules_r7_029: not kept: None
- car_conflicts_3knobs_2hz_rules_r7_030: not kept: None
- car_conflicts_3knobs_2hz_rules_r7_031: not kept: None
- car_conflicts_3knobs_2hz_rules_r7_032: not kept: None
- car_conflicts_3knobs_2hz_rules_r7_033: not kept: None
- car_conflicts_3knobs_2hz_rules_r7_034: not kept: None
- car_conflicts_3knobs_2hz_rules_r7_035: not kept: None
- car_conflicts_3knobs_2hz_rules_r7_036: not kept: None
- car_conflicts_3knobs_2hz_rules_r7_037: not kept: None
- car_conflicts_3knobs_2hz_rules_r7_038: not kept: None
- car_conflicts_3knobs_2hz_rules_r7_039: not kept: None
- car_conflicts_3knobs_2hz_rules_r7_040: not kept: None
- car_conflicts_3knobs_2hz_rules_r7_041: not kept: None
- car_conflicts_3knobs_2hz_rules_r7_042: not kept: None
- car_conflicts_3knobs_2hz_rules_r7_043: not kept: None
- car_conflicts_3knobs_2hz_rules_r7_044: not kept: None
- car_conflicts_3knobs_2hz_rules_r7_045: not kept: None
- car_conflicts_3knobs_2hz_rules_r7_046: not kept: None
- car_conflicts_3knobs_2hz_rules_r7_047: not kept: None
- car_conflicts_3knobs_2hz_rules_r7_048: not kept: None
- car_conflicts_3knobs_2hz_rules_r7_049: not kept: None
- car_conflicts_3knobs_2hz_rules_r7_050: not kept: None
- car_conflicts_3knobs_2hz_rules_r7_051: not kept: None
- car_conflicts_3knobs_2hz_rules_r7_052: not kept: None
- car_conflicts_3knobs_2hz_rules_r7_053: not kept: None
- car_conflicts_3knobs_2hz_rules_r7_054: not kept: None
- car_conflicts_3knobs_2hz_rules_r7_055: not kept: None
- car_conflicts_3knobs_2hz_rules_r7_056: not kept: None
- car_conflicts_3knobs_2hz_rules_r7_057: not kept: None
- car_conflicts_3knobs_2hz_rules_r7_058: not kept: None
- car_conflicts_3knobs_2hz_rules_r7_059: not kept: None
- car_conflicts_3knobs_2hz_rules_r7_060: not kept: None

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
- A scale above 1 starts the ego behind its recorded start, so for the first second or two of the warm-up it is off the recording.). Report written by claude-opus-5-5 from `results` in 21 s; every count above is computed from the queue, not written by the model.

0 of 63 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
