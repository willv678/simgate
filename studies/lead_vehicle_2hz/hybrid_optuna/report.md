# In lead-vehicle scenes, which timing shifts and speed scalings of the recorded lead car make VaVAM run into it? Find the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `hybrid_optuna`: 49 kept runs on 8 scenes, varying actor_time_shift_s, actor_speed_scale; 2 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 1 of 5 challenging settings confirmed, after 7 rounds.

## Answer

The study did not find five confirmed cases. Only one setting is confirmed: 096988dd with the lead car 2 s later and at 0.5x speed (S4), which failed in every run. Even there, and in all the other failures, the ego never rear-ended the retimed lead car. The triage shows every failure was the policy drifting left out of its lane into a car in the next lane, so the study found no retiming that makes VaVAM run into the car ahead. Two more settings came close but are not confirmed: 023b7fcc with a +2 s shift at 1x speed (S3) failed in most runs, but its range still reaches below 0.5, and 19f339ba with a +0.5 s shift at 0.5x speed (S18) failed in roughly half its many runs, so its rate is near or under 0.5. Without 2 Hz runs of the unaltered recording, we can't say whether the retiming caused these drifts.

## Findings

- On 096988dd, delaying the lead car by 2 s and halving its speed is the one confirmed challenging case: every run failed. In each one the ego drifted left against the STRAIGHT/RIGHT command and hit vehicle 41 in the left lane, not the lead car.
  - S4: 096988dd at actor_time_shift_s 2, actor_speed_scale 0.5: 3/3 failed, rate 53%-100% (90%) (lead_vehicle_2hz_hybrid_optuna_006, lead_vehicle_2hz_hybrid_optuna_008, lead_vehicle_2hz_hybrid_optuna_009)
- On 023b7fcc, shifting the lead car 2 s later at its recorded speed failed in most runs, but the range does not rule out a rate below 0.5, so it is a strong candidate rather than a confirmed case. The failures were side-swipes of car 56 in the left lane after the ego left its lane behind the lead car (actor 12). The 0.5x speed settings on this scene did not fail in their one or two runs.
  - S3: 023b7fcc at actor_time_shift_s 2, actor_speed_scale 1: 4/5 failed, rate 44%-95% (90%) (lead_vehicle_2hz_hybrid_optuna_040, lead_vehicle_2hz_hybrid_optuna_043, lead_vehicle_2hz_hybrid_optuna_044, lead_vehicle_2hz_hybrid_optuna_045, lead_vehicle_2hz_hybrid_optuna_046)
  - S1: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_hybrid_optuna_001)
  - S2: 023b7fcc at actor_time_shift_s 1, actor_speed_scale 0.5: 0/2 failed, rate 0%-58% (90%) (lead_vehicle_2hz_hybrid_optuna_020, lead_vehicle_2hz_hybrid_optuna_026)
- On 19f339ba, a +0.5 s shift at 0.5x speed failed in about half of many repeats, so its rate sits near or below 0.5 and is not confirmed. The failures were hard braking on an open highway for no visible reason (17 to about 9.5 m/s, nothing in the ego's lane within about 50 m) plus a left drift into actor 1 in the next lane. The rear contacts in some of these runs were followers hitting the braking ego.
  - S18: 19f339ba at actor_time_shift_s 0.5, actor_speed_scale 0.5: 5/12 failed, rate 22%-64% (90%) (lead_vehicle_2hz_hybrid_optuna_021, lead_vehicle_2hz_hybrid_optuna_022, lead_vehicle_2hz_hybrid_optuna_023, lead_vehicle_2hz_hybrid_optuna_029, lead_vehicle_2hz_hybrid_optuna_030, lead_vehicle_2hz_hybrid_optuna_036, lead_vehicle_2hz_hybrid_optuna_037, lead_vehicle_2hz_hybrid_optuna_038, lead_vehicle_2hz_hybrid_optuna_039, lead_vehicle_2hz_hybrid_optuna_047, lead_vehicle_2hz_hybrid_optuna_048, lead_vehicle_2hz_hybrid_optuna_049_a3)
  - S17: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (lead_vehicle_2hz_hybrid_optuna_014, lead_vehicle_2hz_hybrid_optuna_016)
- Every failure in the study was the policy's fault and of the turned_into_actor kind (a lateral drift left into an adjacent-lane vehicle). None was a rear-end of the retimed lead car, and no failure was flagged as a possible simulator artifact.
  - S3: 023b7fcc at actor_time_shift_s 2, actor_speed_scale 1: 4/5 failed, rate 44%-95% (90%) (lead_vehicle_2hz_hybrid_optuna_040, lead_vehicle_2hz_hybrid_optuna_043, lead_vehicle_2hz_hybrid_optuna_044, lead_vehicle_2hz_hybrid_optuna_045, lead_vehicle_2hz_hybrid_optuna_046)
  - S4: 096988dd at actor_time_shift_s 2, actor_speed_scale 0.5: 3/3 failed, rate 53%-100% (90%) (lead_vehicle_2hz_hybrid_optuna_006, lead_vehicle_2hz_hybrid_optuna_008, lead_vehicle_2hz_hybrid_optuna_009)
  - S18: 19f339ba at actor_time_shift_s 0.5, actor_speed_scale 0.5: 5/12 failed, rate 22%-64% (90%) (lead_vehicle_2hz_hybrid_optuna_021, lead_vehicle_2hz_hybrid_optuna_022, lead_vehicle_2hz_hybrid_optuna_023, lead_vehicle_2hz_hybrid_optuna_029, lead_vehicle_2hz_hybrid_optuna_030, lead_vehicle_2hz_hybrid_optuna_036, lead_vehicle_2hz_hybrid_optuna_037, lead_vehicle_2hz_hybrid_optuna_038, lead_vehicle_2hz_hybrid_optuna_039, lead_vehicle_2hz_hybrid_optuna_047, lead_vehicle_2hz_hybrid_optuna_048, lead_vehicle_2hz_hybrid_optuna_049_a3)
- No setting failed on the other five scenes (09a95ffa, 0cf6368d, 0dbb91dd, 0e899dd3, 12855a41). The repeated harsh settings there (0.5x speed with shifts of -1, -0.5 or +2 s) passed all their runs and are probably below 0.5, but several near misses had high criticality.
  - S5: 09a95ffa at actor_time_shift_s -1, actor_speed_scale 0.5: 0/4 failed, rate 0%-40% (90%) (lead_vehicle_2hz_hybrid_optuna_005, lead_vehicle_2hz_hybrid_optuna_010, lead_vehicle_2hz_hybrid_optuna_015, lead_vehicle_2hz_hybrid_optuna_031)
  - S6: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_hybrid_optuna_035)
  - S7: 09a95ffa at actor_time_shift_s 1, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_hybrid_optuna_042)
  - S8: 0cf6368d at actor_time_shift_s -2, actor_speed_scale 0.75: 0/2 failed, rate 0%-58% (90%) (lead_vehicle_2hz_hybrid_optuna_013, lead_vehicle_2hz_hybrid_optuna_028)
  - S9: 0cf6368d at actor_time_shift_s -0.5, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_hybrid_optuna_002)
  - S10: 0cf6368d at actor_time_shift_s 2, actor_speed_scale 0.5: 0/2 failed, rate 0%-58% (90%) (lead_vehicle_2hz_hybrid_optuna_027, lead_vehicle_2hz_hybrid_optuna_034)
  - S11: 0dbb91dd at actor_time_shift_s -1.5, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_hybrid_optuna_004)
  - S12: 0dbb91dd at actor_time_shift_s 2, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_hybrid_optuna_019)
  - S13: 0e899dd3 at actor_time_shift_s -2, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (lead_vehicle_2hz_hybrid_optuna_007, lead_vehicle_2hz_hybrid_optuna_012)
  - S14: 0e899dd3 at actor_time_shift_s 2, actor_speed_scale 0.5: 0/4 failed, rate 0%-40% (90%) (lead_vehicle_2hz_hybrid_optuna_018, lead_vehicle_2hz_hybrid_optuna_024, lead_vehicle_2hz_hybrid_optuna_025, lead_vehicle_2hz_hybrid_optuna_032)
  - S15: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 0.5: 0/4 failed, rate 0%-40% (90%) (lead_vehicle_2hz_hybrid_optuna_003, lead_vehicle_2hz_hybrid_optuna_011, lead_vehicle_2hz_hybrid_optuna_017, lead_vehicle_2hz_hybrid_optuna_033)
  - S16: 12855a41 at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_hybrid_optuna_041)

## Open

- Whether retiming causes the failures at all: there are no 2 Hz runs of the unaltered recording (0 s shift, 1x speed) on 096988dd, 023b7fcc or 19f339ba. A few baseline repeats on each would show whether the left drift happens anyway.
- Whether S3 (023b7fcc, +2 s, 1x speed) is above 0.5: a few more repeats would settle it.
- Whether S18 (19f339ba, +0.5 s, 0.5x speed) is at or above 0.5: its range straddles that value even after many runs, so it needs many more repeats, or a neighbouring setting should be tried instead.
- No cases on the other five scenes: the near-miss settings with the highest criticality (0e899dd3 at +2 s/0.5x, 09a95ffa at -1 s/0.5x, 12855a41 at -0.5 s/0.5x and +0.5 s/1.25x) could be pushed further, or tried at untested shift and speed combinations.
- The brief's premise that 2 Hz planning halves the left drift doesn't fit this study: left drift explains every failure. A comparison with the 10 Hz lead_vehicle study on the same settings would show whether 2 Hz drifts less or more.
- Two runs at the S18 setting were re-run and not kept, so they are not evidence.

## Why the runs failed (triage from the video and log)

turned_into_actor 12

- lead_vehicle_2hz_hybrid_optuna_006: turned_into_actor, policy at fault: yes. On a multi-lane highway at about 5 m/s, the ego's planned path veered left, away from the route line, which was going straight and then right. The ego drifted into the left lane and its front hit vehicle 41, which was travelling alongside and just ahead in that lane.
- lead_vehicle_2hz_hybrid_optuna_008: turned_into_actor, policy at fault: yes. Driving straight on a wet multi-lane highway at about 5.5 m/s, the policy's planned path (orange) bent left toward the next lane while the recorded human path went straight and then right. The command was STRAIGHT, then RIGHT at 7.2 s. At 7.2 s the ego, now 1.5 m off the recorded path, swung its nose into actor 41, which was alongside in the left lane, and the collision counted as a front collision.
- lead_vehicle_2hz_hybrid_optuna_009: turned_into_actor, policy at fault: yes. On a multi-lane highway at about 5.5 m/s, the ego's planned path kept bending left, even though the route command had switched to RIGHT. The ego drifted out of its lane into the left lane, and its front hit vehicle 41, which was travelling alongside and slightly ahead in that lane.
- lead_vehicle_2hz_hybrid_optuna_021: turned_into_actor, policy at fault: yes. On a straight multi-lane highway with the command STRAIGHT, the ego slowed hard (17 to 9.5 m/s) while the recorded drive kept going, ending 10 m behind it. It also drifted left out of its lane, and at 7.1 s its front hit actor 1, which was travelling just ahead in the lane to the left. The lane ahead was clear (the gap to the next car was about 50 m), so nothing forced either the lane drift or the braking.
- lead_vehicle_2hz_hybrid_optuna_029: turned_into_actor, policy at fault: yes. On a clear multi-lane highway, the policy braked hard for no visible reason (17 → 9 m/s, with no lead within about 50 m), and its planned path also edged left. Actor 1 had been beside it in the left lane and pulled ahead as the ego slowed, so at 7.1 s the ego's front-left drifted into actor 1's rear-right. The ego was also rear-ended at some point.
- lead_vehicle_2hz_hybrid_optuna_037: turned_into_actor, policy at fault: yes. After handoff the ego braked hard on an open highway (17 → 9.7 m/s, nothing close ahead), fell behind its recorded position and drifted left. Its front-left corner then hit actor 1, which was travelling just ahead in the adjacent left lane. The later rear contact was most likely a follower hitting the ego after it braked for no reason.
- lead_vehicle_2hz_hybrid_optuna_039: turned_into_actor, policy at fault: yes. On a clear multi-lane highway with no lead vehicle in its lane, the ego braked hard for no visible reason (17 → 9.5 m/s) and edged left toward the lane line. Its front corner hit actor 1, which was alongside in the left lane. The hard braking also let a vehicle behind run into the ego's rear.
- lead_vehicle_2hz_hybrid_optuna_040: turned_into_actor, policy at fault: yes. On a multi-lane highway at about 4–5 m/s, the ego left its lane behind actor 12 and cut left, which went against the STRAIGHT and then RIGHT route commands. At 8.2 s its side hit actor 56, which was alongside it in the left lane (lateral collision).
- lead_vehicle_2hz_hybrid_optuna_044: turned_into_actor, policy at fault: yes. The ego was in slow highway traffic about 4–7 m behind car 12. It left the recorded path and steered left into the next lane, even though the route command said STRAIGHT and then RIGHT. At 8.2 s its side hit car 56, which was driving alongside in that lane.
- lead_vehicle_2hz_hybrid_optuna_045: turned_into_actor, policy at fault: yes. On a multi-lane road, the recorded human driver kept right as the command changed to RIGHT, but the policy's plan veered left. The ego drifted about 1.9 m left toward the next lane and side-swiped actor 56, which was travelling alongside it in that lane (lateral collision at 8.7 s).
- lead_vehicle_2hz_hybrid_optuna_046: turned_into_actor, policy at fault: yes. In slow freeway traffic, the policy left the recorded path (green) and steered left toward the next lane, following its orange plan toward the gap behind vehicle 15. At 8.2 s, while speeding up to about 4.9 m/s, it moved sideways into vehicle 56, which was driving alongside in that lane, causing a side collision.
- lead_vehicle_2hz_hybrid_optuna_049_a3: turned_into_actor, policy at fault: yes. After handoff on a straight multi-lane highway, the policy braked hard for no visible reason (17 to 9.5 m/s, with no lead vehicle in its own lane) and veered left toward the adjacent lane. Its front-left corner hit actor 1, which was driving just ahead in that left lane, while the recorded human kept going straight in the original lane. A later rear contact is likely a result of the unnecessary braking.

## Every setting

- S1: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_hybrid_optuna_001)
- S2: 023b7fcc at actor_time_shift_s 1, actor_speed_scale 0.5: 0/2 failed, rate 0%-58% (90%) (lead_vehicle_2hz_hybrid_optuna_020, lead_vehicle_2hz_hybrid_optuna_026)
- S3: 023b7fcc at actor_time_shift_s 2, actor_speed_scale 1: 4/5 failed, rate 44%-95% (90%) (lead_vehicle_2hz_hybrid_optuna_040, lead_vehicle_2hz_hybrid_optuna_043, lead_vehicle_2hz_hybrid_optuna_044, lead_vehicle_2hz_hybrid_optuna_045, lead_vehicle_2hz_hybrid_optuna_046)
- S4: 096988dd at actor_time_shift_s 2, actor_speed_scale 0.5: 3/3 failed, rate 53%-100% (90%) (lead_vehicle_2hz_hybrid_optuna_006, lead_vehicle_2hz_hybrid_optuna_008, lead_vehicle_2hz_hybrid_optuna_009)
- S5: 09a95ffa at actor_time_shift_s -1, actor_speed_scale 0.5: 0/4 failed, rate 0%-40% (90%) (lead_vehicle_2hz_hybrid_optuna_005, lead_vehicle_2hz_hybrid_optuna_010, lead_vehicle_2hz_hybrid_optuna_015, lead_vehicle_2hz_hybrid_optuna_031)
- S6: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_hybrid_optuna_035)
- S7: 09a95ffa at actor_time_shift_s 1, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_hybrid_optuna_042)
- S8: 0cf6368d at actor_time_shift_s -2, actor_speed_scale 0.75: 0/2 failed, rate 0%-58% (90%) (lead_vehicle_2hz_hybrid_optuna_013, lead_vehicle_2hz_hybrid_optuna_028)
- S9: 0cf6368d at actor_time_shift_s -0.5, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_hybrid_optuna_002)
- S10: 0cf6368d at actor_time_shift_s 2, actor_speed_scale 0.5: 0/2 failed, rate 0%-58% (90%) (lead_vehicle_2hz_hybrid_optuna_027, lead_vehicle_2hz_hybrid_optuna_034)
- S11: 0dbb91dd at actor_time_shift_s -1.5, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_hybrid_optuna_004)
- S12: 0dbb91dd at actor_time_shift_s 2, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_hybrid_optuna_019)
- S13: 0e899dd3 at actor_time_shift_s -2, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (lead_vehicle_2hz_hybrid_optuna_007, lead_vehicle_2hz_hybrid_optuna_012)
- S14: 0e899dd3 at actor_time_shift_s 2, actor_speed_scale 0.5: 0/4 failed, rate 0%-40% (90%) (lead_vehicle_2hz_hybrid_optuna_018, lead_vehicle_2hz_hybrid_optuna_024, lead_vehicle_2hz_hybrid_optuna_025, lead_vehicle_2hz_hybrid_optuna_032)
- S15: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 0.5: 0/4 failed, rate 0%-40% (90%) (lead_vehicle_2hz_hybrid_optuna_003, lead_vehicle_2hz_hybrid_optuna_011, lead_vehicle_2hz_hybrid_optuna_017, lead_vehicle_2hz_hybrid_optuna_033)
- S16: 12855a41 at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_hybrid_optuna_041)
- S17: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (lead_vehicle_2hz_hybrid_optuna_014, lead_vehicle_2hz_hybrid_optuna_016)
- S18: 19f339ba at actor_time_shift_s 0.5, actor_speed_scale 0.5: 5/12 failed, rate 22%-64% (90%) (lead_vehicle_2hz_hybrid_optuna_021, lead_vehicle_2hz_hybrid_optuna_022, lead_vehicle_2hz_hybrid_optuna_023, lead_vehicle_2hz_hybrid_optuna_029, lead_vehicle_2hz_hybrid_optuna_030, lead_vehicle_2hz_hybrid_optuna_036, lead_vehicle_2hz_hybrid_optuna_037, lead_vehicle_2hz_hybrid_optuna_038, lead_vehicle_2hz_hybrid_optuna_039, lead_vehicle_2hz_hybrid_optuna_047, lead_vehicle_2hz_hybrid_optuna_048, lead_vehicle_2hz_hybrid_optuna_049_a3)

## Not kept by the gate

- lead_vehicle_2hz_hybrid_optuna_049: not kept: RE-RUN
- lead_vehicle_2hz_hybrid_optuna_049_a2: not kept: RE-RUN

## Provenance

Plan: `plan.json` (rationale: Copied from studies/lead_vehicle/plan.json (10 Hz) with the policy planning every 500 ms, so the method comparison can be repeated at 2 Hz. Scene choice: all eight scenes are tagged lead_vehicle, have an identified lead car, did not fail in the earlier run at 0 delay, and the ego drove far enough (6 to 19 m/s, about 35 to 130 m) to actually close on the car ahead. Several already came very close (0dbb91dd 0.23 m, 19f339ba 0.03 m, 12855a41 0.08 m, 096988dd and 023b7fcc 0.0 m), so they are likely to tip into failure. I left out lead_vehicle scenes that already fail at baseline, because they cannot show that the retiming caused the failure. I also left out scenes where the ego barely moved (for example 0fa7060f, 15dd433e, 0ac02819, 10d64934) and tagged scenes with no identified lead car (166fe701, 1bccdc21, 0ce02937, 1a5da90a).

Retiming: traffic is replay, as the brief asks, so the lead car follows its recorded path while being retimed. Only the lead car is retimed in each scene (via retime_tracks), not every car. That keeps the failures about the car ahead rather than about crossing traffic being shifted. 0cf6368d's lead car is also its cut-in car, so a failure there may be a cut-in rather than a pure braking case.

Goal: top_k with k=5, one setting per scene, and each setting's failure rate surely above 0.5. This matches 'the 5 most challenging cases, each on a different scene, confirmed by repeats'. The plan is 7 rounds of 7 runs (49, close to the brief's 50 and within the 60 cap), so the proposer can screen broadly and then repeat.

Limits:
(1) Budget. Confirming a rate above 0.5 at 90% takes about 4 to 5 failures per setting, so 5 confirmed cases need roughly 25 runs or more. That leaves little room for screening, and the study may end with fewer than 5 confirmed.
(2) Failure is any front or side collision or leaving the road. The check cannot tell a rear-end from other contact, and near misses are only a soft ranking for the proposer, not part of the goal.
(3) The 200 ms delay cap is given to the proposer as an instruction. The knob itself allows up to 400 ms, so the code does not enforce the cap.
(4) Under replay the lead car never reacts to the ego, and changing its speed stretches its recorded braking profile rather than making a new braking event.). Report written by claude-opus-5-5 from `results` in 24 s; every count above is computed from the queue, not written by the model.

51 of 51 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
