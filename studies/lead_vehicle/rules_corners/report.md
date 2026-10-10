# In lead-vehicle scenes, which timing shifts and speed scalings of the recorded lead car (with up to 200 ms planner delay if needed) make VaVAM run into it? Find the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `rules_corners`: 49 kept runs on 8 scenes, varying actor_time_shift_s, actor_speed_scale, planner_delay_us; 2 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 0 of 5 challenging settings confirmed, after 7 rounds.

## Answer

The study found no case where VaVAM runs into the lead car, so none of the 5 challenging cases was confirmed. Every kept run passed. But all of them used one setting on each of the eight scenes: no time shift, the lead car at 1.25x its recorded speed (faster, which should make the stop easier), and the maximum 200 ms planner delay. The question of which timings and speeds cause rear-ends is still open. Earlier or later timing and slower lead cars (0.5x to 1x) were never tried. The result only shows that this one fairly easy setting rarely or never fails on seven of the scenes. On 0dbb91dd it rests on a single run, which is a hint, not a rate.

## Findings

- With no time shift, the lead car at 1.25x speed and 200 ms planner delay, every repeated run passed on 023b7fcc, 096988dd, 09a95ffa, 0cf6368d, 12855a41 and 19f339ba. Each range stays well below the goal's 0.5 threshold, so this setting is not a challenging case on any of these scenes.
  - S1: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000: 0/7 failed, rate 0%-28% (90%) (lead_vehicle_rules_corners_005, lead_vehicle_rules_corners_013, lead_vehicle_rules_corners_021, lead_vehicle_rules_corners_028, lead_vehicle_rules_corners_035, lead_vehicle_rules_corners_042, lead_vehicle_rules_corners_049)
  - S2: 096988dd at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000: 0/7 failed, rate 0%-28% (90%) (lead_vehicle_rules_corners_004, lead_vehicle_rules_corners_009, lead_vehicle_rules_corners_017, lead_vehicle_rules_corners_024, lead_vehicle_rules_corners_031, lead_vehicle_rules_corners_038, lead_vehicle_rules_corners_045)
  - S3: 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000: 0/7 failed, rate 0%-28% (90%) (lead_vehicle_rules_corners_006, lead_vehicle_rules_corners_008, lead_vehicle_rules_corners_016, lead_vehicle_rules_corners_023, lead_vehicle_rules_corners_030, lead_vehicle_rules_corners_037, lead_vehicle_rules_corners_043)
  - S4: 0cf6368d at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000: 0/7 failed, rate 0%-28% (90%) (lead_vehicle_rules_corners_007, lead_vehicle_rules_corners_011, lead_vehicle_rules_corners_019, lead_vehicle_rules_corners_026, lead_vehicle_rules_corners_033, lead_vehicle_rules_corners_040, lead_vehicle_rules_corners_047)
  - S7: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000: 0/7 failed, rate 0%-28% (90%) (lead_vehicle_rules_corners_003, lead_vehicle_rules_corners_012, lead_vehicle_rules_corners_020, lead_vehicle_rules_corners_027, lead_vehicle_rules_corners_034, lead_vehicle_rules_corners_041, lead_vehicle_rules_corners_048)
  - S8: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000: 0/7 failed, rate 0%-28% (90%) (lead_vehicle_rules_corners_002, lead_vehicle_rules_corners_010, lead_vehicle_rules_corners_018, lead_vehicle_rules_corners_025, lead_vehicle_rules_corners_032, lead_vehicle_rules_corners_039, lead_vehicle_rules_corners_046)
- On 0e899dd3 every kept run at the same setting also passed. Two runs had to be re-run and are not counted as evidence.
  - S6: 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000: 0/6 failed, rate 0%-31% (90%) (lead_vehicle_rules_corners_014_a2, lead_vehicle_rules_corners_015, lead_vehicle_rules_corners_022, lead_vehicle_rules_corners_029_a2, lead_vehicle_rules_corners_036, lead_vehicle_rules_corners_044)
- On 0dbb91dd this setting got only one run, which passed. That is too few to say whether the setting fails.
  - S5: 0dbb91dd at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_rules_corners_001)
- No failures occurred, so nothing was triaged. The study gives no evidence on how the policy fails with a lead car, and none of the results depends on possible simulator artifacts.
  - S1: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000: 0/7 failed, rate 0%-28% (90%) (lead_vehicle_rules_corners_005, lead_vehicle_rules_corners_013, lead_vehicle_rules_corners_021, lead_vehicle_rules_corners_028, lead_vehicle_rules_corners_035, lead_vehicle_rules_corners_042, lead_vehicle_rules_corners_049)
  - S2: 096988dd at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000: 0/7 failed, rate 0%-28% (90%) (lead_vehicle_rules_corners_004, lead_vehicle_rules_corners_009, lead_vehicle_rules_corners_017, lead_vehicle_rules_corners_024, lead_vehicle_rules_corners_031, lead_vehicle_rules_corners_038, lead_vehicle_rules_corners_045)
  - S3: 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000: 0/7 failed, rate 0%-28% (90%) (lead_vehicle_rules_corners_006, lead_vehicle_rules_corners_008, lead_vehicle_rules_corners_016, lead_vehicle_rules_corners_023, lead_vehicle_rules_corners_030, lead_vehicle_rules_corners_037, lead_vehicle_rules_corners_043)
  - S4: 0cf6368d at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000: 0/7 failed, rate 0%-28% (90%) (lead_vehicle_rules_corners_007, lead_vehicle_rules_corners_011, lead_vehicle_rules_corners_019, lead_vehicle_rules_corners_026, lead_vehicle_rules_corners_033, lead_vehicle_rules_corners_040, lead_vehicle_rules_corners_047)
  - S5: 0dbb91dd at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_rules_corners_001)
  - S6: 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000: 0/6 failed, rate 0%-31% (90%) (lead_vehicle_rules_corners_014_a2, lead_vehicle_rules_corners_015, lead_vehicle_rules_corners_022, lead_vehicle_rules_corners_029_a2, lead_vehicle_rules_corners_036, lead_vehicle_rules_corners_044)
  - S7: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000: 0/7 failed, rate 0%-28% (90%) (lead_vehicle_rules_corners_003, lead_vehicle_rules_corners_012, lead_vehicle_rules_corners_020, lead_vehicle_rules_corners_027, lead_vehicle_rules_corners_034, lead_vehicle_rules_corners_041, lead_vehicle_rules_corners_048)
  - S8: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000: 0/7 failed, rate 0%-28% (90%) (lead_vehicle_rules_corners_002, lead_vehicle_rules_corners_010, lead_vehicle_rules_corners_018, lead_vehicle_rules_corners_025, lead_vehicle_rules_corners_032, lead_vehicle_rules_corners_039, lead_vehicle_rules_corners_046)

## Open

- The search never ran the settings the brief describes as harder: a slower lead car (0.5x to 1x speed) and time shifts between -2 s and +2 s. On each scene, start by screening 0.5x speed with shifts of -2, 0 and +2 s at no planner delay, then add delay up to 200 ms only where retiming alone does not fail.
- The whole budget went on repeating one corner setting where the lead car is faster than recorded, which is probably the easiest point in the range. A new study should spread its first rounds across the speed and timing grid and repeat only settings that fail or come close.
- 0dbb91dd was tried only once. It needs its own screen at slow lead speeds.
- Near-miss ranking (closest approach) is not in these results, so the study cannot say which scenes came closest to a collision.

## Every setting

- S1: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000: 0/7 failed, rate 0%-28% (90%) (lead_vehicle_rules_corners_005, lead_vehicle_rules_corners_013, lead_vehicle_rules_corners_021, lead_vehicle_rules_corners_028, lead_vehicle_rules_corners_035, lead_vehicle_rules_corners_042, lead_vehicle_rules_corners_049)
- S2: 096988dd at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000: 0/7 failed, rate 0%-28% (90%) (lead_vehicle_rules_corners_004, lead_vehicle_rules_corners_009, lead_vehicle_rules_corners_017, lead_vehicle_rules_corners_024, lead_vehicle_rules_corners_031, lead_vehicle_rules_corners_038, lead_vehicle_rules_corners_045)
- S3: 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000: 0/7 failed, rate 0%-28% (90%) (lead_vehicle_rules_corners_006, lead_vehicle_rules_corners_008, lead_vehicle_rules_corners_016, lead_vehicle_rules_corners_023, lead_vehicle_rules_corners_030, lead_vehicle_rules_corners_037, lead_vehicle_rules_corners_043)
- S4: 0cf6368d at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000: 0/7 failed, rate 0%-28% (90%) (lead_vehicle_rules_corners_007, lead_vehicle_rules_corners_011, lead_vehicle_rules_corners_019, lead_vehicle_rules_corners_026, lead_vehicle_rules_corners_033, lead_vehicle_rules_corners_040, lead_vehicle_rules_corners_047)
- S5: 0dbb91dd at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_rules_corners_001)
- S6: 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000: 0/6 failed, rate 0%-31% (90%) (lead_vehicle_rules_corners_014_a2, lead_vehicle_rules_corners_015, lead_vehicle_rules_corners_022, lead_vehicle_rules_corners_029_a2, lead_vehicle_rules_corners_036, lead_vehicle_rules_corners_044)
- S7: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000: 0/7 failed, rate 0%-28% (90%) (lead_vehicle_rules_corners_003, lead_vehicle_rules_corners_012, lead_vehicle_rules_corners_020, lead_vehicle_rules_corners_027, lead_vehicle_rules_corners_034, lead_vehicle_rules_corners_041, lead_vehicle_rules_corners_048)
- S8: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000: 0/7 failed, rate 0%-28% (90%) (lead_vehicle_rules_corners_002, lead_vehicle_rules_corners_010, lead_vehicle_rules_corners_018, lead_vehicle_rules_corners_025, lead_vehicle_rules_corners_032, lead_vehicle_rules_corners_039, lead_vehicle_rules_corners_046)

## Not kept by the gate

- lead_vehicle_rules_corners_014: not kept: RE-RUN
- lead_vehicle_rules_corners_029: not kept: RE-RUN

## Provenance

Plan: `plan.json` (rationale: Scene choice: all eight scenes are tagged lead_vehicle, have an identified lead car, did not fail in the earlier run at 0 delay, and the ego drove far enough (6 to 19 m/s, about 35 to 130 m) to actually close on the car ahead. Several already came very close (0dbb91dd 0.23 m, 19f339ba 0.03 m, 12855a41 0.08 m, 096988dd and 023b7fcc 0.0 m), so they are likely to tip into failure. I left out lead_vehicle scenes that already fail at baseline, because they cannot show that the retiming caused the failure. I also left out scenes where the ego barely moved (for example 0fa7060f, 15dd433e, 0ac02819, 10d64934) and tagged scenes with no identified lead car (166fe701, 1bccdc21, 0ce02937, 1a5da90a).

Retiming: traffic is replay, as the brief asks, so the lead car follows its recorded path while being retimed. Only the lead car is retimed in each scene (via retime_tracks), not every car. That keeps the failures about the car ahead rather than about crossing traffic being shifted. 0cf6368d's lead car is also its cut-in car, so a failure there may be a cut-in rather than a pure braking case.

Goal: top_k with k=5, one setting per scene, and each setting's failure rate surely above 0.5. This matches 'the 5 most challenging cases, each on a different scene, confirmed by repeats'. The plan is 7 rounds of 7 runs (49, close to the brief's 50 and within the 60 cap), so the proposer can screen broadly and then repeat.

Limits:
(1) Budget. Confirming a rate above 0.5 at 90% takes about 4 to 5 failures per setting, so 5 confirmed cases need roughly 25 runs or more. That leaves little room for screening, and the study may end with fewer than 5 confirmed.
(2) Failure is any front or side collision or leaving the road. The check cannot tell a rear-end from other contact, and near misses are only a soft ranking for the proposer, not part of the goal.
(3) The 200 ms delay cap is given to the proposer as an instruction. The knob itself allows up to 400 ms, so the code does not enforce the cap.
(4) Under replay the lead car never reacts to the ego, and changing its speed stretches its recorded braking profile rather than making a new braking event.). Report written by claude-opus-5-5 from `results` in 12 s; every count above is computed from the queue, not written by the model.

51 of 51 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
