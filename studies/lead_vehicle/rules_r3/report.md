# In lead-vehicle scenes, which timing shifts and speed scalings of the recorded lead car (with up to 200 ms planner delay if needed) make VaVAM run into it? Find the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `rules_r3`: 49 kept runs on 8 scenes, varying actor_time_shift_s, actor_speed_scale, planner_delay_us; 1 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 0 of 5 challenging settings confirmed, after 7 rounds.

## Answer

The study found none of the 5 challenging cases it was asked for. No setting caused VaVAM to rear-end the lead car, leave the road or have any other counted collision, so the goal was not met. All kept runs used one setting: no time shift, the lead car at 1.25x its recorded speed, and the maximum 200 ms planner delay. Every run at that setting passed on all eight scenes. On seven scenes the repeats rule out a high failure rate there: the true rate is at most about a third. On 0dbb91dd only one run was kept, which is a hint, not a rate. A faster lead car makes the stop easier for the ego, and no slower speeds or time shifts were tried. So the study cannot say which timings or speeds would make the policy hit the car ahead.

## Findings

- With no time shift, the lead car at 1.25x its recorded speed and a 200 ms planner delay, VaVAM did not fail in any repeated run on 023b7fcc, 096988dd, 09a95ffa, 0cf6368d, 0e899dd3, 12855a41 or 19f339ba. The ranges rule out a failure rate above one half on each of these scenes at this setting.
  - S1: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000: 0/7 failed, rate 0%-28% (90%) (lead_vehicle_rules_r3_005, lead_vehicle_rules_r3_013, lead_vehicle_rules_r3_021, lead_vehicle_rules_r3_028, lead_vehicle_rules_r3_035, lead_vehicle_rules_r3_042, lead_vehicle_rules_r3_049)
  - S2: 096988dd at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000: 0/7 failed, rate 0%-28% (90%) (lead_vehicle_rules_r3_004, lead_vehicle_rules_r3_009, lead_vehicle_rules_r3_016, lead_vehicle_rules_r3_023, lead_vehicle_rules_r3_030, lead_vehicle_rules_r3_037, lead_vehicle_rules_r3_044)
  - S3: 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000: 0/7 failed, rate 0%-28% (90%) (lead_vehicle_rules_r3_006, lead_vehicle_rules_r3_008, lead_vehicle_rules_r3_015, lead_vehicle_rules_r3_022, lead_vehicle_rules_r3_029, lead_vehicle_rules_r3_036, lead_vehicle_rules_r3_043)
  - S4: 0cf6368d at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000: 0/7 failed, rate 0%-28% (90%) (lead_vehicle_rules_r3_007, lead_vehicle_rules_r3_011, lead_vehicle_rules_r3_019, lead_vehicle_rules_r3_026, lead_vehicle_rules_r3_033, lead_vehicle_rules_r3_040, lead_vehicle_rules_r3_047)
  - S6: 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000: 0/6 failed, rate 0%-31% (90%) (lead_vehicle_rules_r3_014, lead_vehicle_rules_r3_018, lead_vehicle_rules_r3_024, lead_vehicle_rules_r3_031, lead_vehicle_rules_r3_038, lead_vehicle_rules_r3_045)
  - S7: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000: 0/7 failed, rate 0%-28% (90%) (lead_vehicle_rules_r3_003, lead_vehicle_rules_r3_012, lead_vehicle_rules_r3_020, lead_vehicle_rules_r3_027, lead_vehicle_rules_r3_034, lead_vehicle_rules_r3_041_a2, lead_vehicle_rules_r3_048)
  - S8: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000: 0/7 failed, rate 0%-28% (90%) (lead_vehicle_rules_r3_002, lead_vehicle_rules_r3_010, lead_vehicle_rules_r3_017, lead_vehicle_rules_r3_025, lead_vehicle_rules_r3_032, lead_vehicle_rules_r3_039, lead_vehicle_rules_r3_046)
- On 0dbb91dd only one run was kept at this setting. It passed, but one run cannot rule out a high failure rate, and its criticality was the lowest of all settings.
  - S5: 0dbb91dd at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_rules_r3_001)
- Even at the 200 ms delay cap, some scenes came closer to the lead car than others. Ranked by criticality, the nearest misses were 09a95ffa, then 0e899dd3, 096988dd and 19f339ba, then 0cf6368d. These are the best places to look for failures next.
  - S3: 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000: 0/7 failed, rate 0%-28% (90%) (lead_vehicle_rules_r3_006, lead_vehicle_rules_r3_008, lead_vehicle_rules_r3_015, lead_vehicle_rules_r3_022, lead_vehicle_rules_r3_029, lead_vehicle_rules_r3_036, lead_vehicle_rules_r3_043)
  - S6: 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000: 0/6 failed, rate 0%-31% (90%) (lead_vehicle_rules_r3_014, lead_vehicle_rules_r3_018, lead_vehicle_rules_r3_024, lead_vehicle_rules_r3_031, lead_vehicle_rules_r3_038, lead_vehicle_rules_r3_045)
  - S2: 096988dd at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000: 0/7 failed, rate 0%-28% (90%) (lead_vehicle_rules_r3_004, lead_vehicle_rules_r3_009, lead_vehicle_rules_r3_016, lead_vehicle_rules_r3_023, lead_vehicle_rules_r3_030, lead_vehicle_rules_r3_037, lead_vehicle_rules_r3_044)
  - S8: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000: 0/7 failed, rate 0%-28% (90%) (lead_vehicle_rules_r3_002, lead_vehicle_rules_r3_010, lead_vehicle_rules_r3_017, lead_vehicle_rules_r3_025, lead_vehicle_rules_r3_032, lead_vehicle_rules_r3_039, lead_vehicle_rules_r3_046)
  - S4: 0cf6368d at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000: 0/7 failed, rate 0%-28% (90%) (lead_vehicle_rules_r3_007, lead_vehicle_rules_r3_011, lead_vehicle_rules_r3_019, lead_vehicle_rules_r3_026, lead_vehicle_rules_r3_033, lead_vehicle_rules_r3_040, lead_vehicle_rules_r3_047)
- No failures were triaged, and no kept run was flagged as a possible simulator artifact, so these results are not distorted by rendering problems. One re-run on 12855a41 was not kept and does not count as evidence.
  - S7: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000: 0/7 failed, rate 0%-28% (90%) (lead_vehicle_rules_r3_003, lead_vehicle_rules_r3_012, lead_vehicle_rules_r3_020, lead_vehicle_rules_r3_027, lead_vehicle_rules_r3_034, lead_vehicle_rules_r3_041_a2, lead_vehicle_rules_r3_048)

## Open

- The question is not answered: the study never varied the time shift or speed scale. Every run used the same setting: no shift, the lead car at 1.25x speed, 200 ms delay. The next study should screen slower lead speeds (0.5x to 0.75x, which force a harder stop) and time shifts of -2 s to +2 s, one or two runs each. It should start at 0 delay and add delay only where retiming alone does not cause failures, then spend its repeats only on settings that fail.
- Start that screening on the scenes with the closest misses (09a95ffa, 0e899dd3, 096988dd, 19f339ba), where the policy is most likely to tip into a collision.
- 0dbb91dd has only one kept run here. It needs either repeats at this setting or screening at slower lead speeds before it can be ranked.
- Most of the budget went on seven near-identical repeats per scene of one passing setting. Repeats should stop as soon as a setting clearly passes.

## Every setting

- S1: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000: 0/7 failed, rate 0%-28% (90%) (lead_vehicle_rules_r3_005, lead_vehicle_rules_r3_013, lead_vehicle_rules_r3_021, lead_vehicle_rules_r3_028, lead_vehicle_rules_r3_035, lead_vehicle_rules_r3_042, lead_vehicle_rules_r3_049)
- S2: 096988dd at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000: 0/7 failed, rate 0%-28% (90%) (lead_vehicle_rules_r3_004, lead_vehicle_rules_r3_009, lead_vehicle_rules_r3_016, lead_vehicle_rules_r3_023, lead_vehicle_rules_r3_030, lead_vehicle_rules_r3_037, lead_vehicle_rules_r3_044)
- S3: 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000: 0/7 failed, rate 0%-28% (90%) (lead_vehicle_rules_r3_006, lead_vehicle_rules_r3_008, lead_vehicle_rules_r3_015, lead_vehicle_rules_r3_022, lead_vehicle_rules_r3_029, lead_vehicle_rules_r3_036, lead_vehicle_rules_r3_043)
- S4: 0cf6368d at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000: 0/7 failed, rate 0%-28% (90%) (lead_vehicle_rules_r3_007, lead_vehicle_rules_r3_011, lead_vehicle_rules_r3_019, lead_vehicle_rules_r3_026, lead_vehicle_rules_r3_033, lead_vehicle_rules_r3_040, lead_vehicle_rules_r3_047)
- S5: 0dbb91dd at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_rules_r3_001)
- S6: 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000: 0/6 failed, rate 0%-31% (90%) (lead_vehicle_rules_r3_014, lead_vehicle_rules_r3_018, lead_vehicle_rules_r3_024, lead_vehicle_rules_r3_031, lead_vehicle_rules_r3_038, lead_vehicle_rules_r3_045)
- S7: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000: 0/7 failed, rate 0%-28% (90%) (lead_vehicle_rules_r3_003, lead_vehicle_rules_r3_012, lead_vehicle_rules_r3_020, lead_vehicle_rules_r3_027, lead_vehicle_rules_r3_034, lead_vehicle_rules_r3_041_a2, lead_vehicle_rules_r3_048)
- S8: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000: 0/7 failed, rate 0%-28% (90%) (lead_vehicle_rules_r3_002, lead_vehicle_rules_r3_010, lead_vehicle_rules_r3_017, lead_vehicle_rules_r3_025, lead_vehicle_rules_r3_032, lead_vehicle_rules_r3_039, lead_vehicle_rules_r3_046)

## Not kept by the gate

- lead_vehicle_rules_r3_041: not kept: RE-RUN

## Provenance

Plan: `plan.json` (rationale: Scene choice: all eight scenes are tagged lead_vehicle, have an identified lead car, did not fail in the earlier run at 0 delay, and the ego drove far enough (6 to 19 m/s, about 35 to 130 m) to actually close on the car ahead. Several already came very close (0dbb91dd 0.23 m, 19f339ba 0.03 m, 12855a41 0.08 m, 096988dd and 023b7fcc 0.0 m), so they are likely to tip into failure. I left out lead_vehicle scenes that already fail at baseline, because they cannot show that the retiming caused the failure. I also left out scenes where the ego barely moved (for example 0fa7060f, 15dd433e, 0ac02819, 10d64934) and tagged scenes with no identified lead car (166fe701, 1bccdc21, 0ce02937, 1a5da90a).

Retiming: traffic is replay, as the brief asks, so the lead car follows its recorded path while being retimed. Only the lead car is retimed in each scene (via retime_tracks), not every car. That keeps the failures about the car ahead rather than about crossing traffic being shifted. 0cf6368d's lead car is also its cut-in car, so a failure there may be a cut-in rather than a pure braking case.

Goal: top_k with k=5, one setting per scene, and each setting's failure rate surely above 0.5. This matches 'the 5 most challenging cases, each on a different scene, confirmed by repeats'. The plan is 7 rounds of 7 runs (49, close to the brief's 50 and within the 60 cap), so the proposer can screen broadly and then repeat.

Limits:
(1) Budget. Confirming a rate above 0.5 at 90% takes about 4 to 5 failures per setting, so 5 confirmed cases need roughly 25 runs or more. That leaves little room for screening, and the study may end with fewer than 5 confirmed.
(2) Failure is any front or side collision or leaving the road. The check cannot tell a rear-end from other contact, and near misses are only a soft ranking for the proposer, not part of the goal.
(3) The 200 ms delay cap is given to the proposer as an instruction. The knob itself allows up to 400 ms, so the code does not enforce the cap.
(4) Under replay the lead car never reacts to the ego, and changing its speed stretches its recorded braking profile rather than making a new braking event.). Report written by claude-opus-5-5 from `results` in 13 s; every count above is computed from the queue, not written by the model.

50 of 50 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
