# In pedestrian-crossing scenes, which combinations of ego speed at hand-off (0.6x–1.4x recorded) and pedestrian step-out time (±2 s) make the VaVAM policy with the linear MPC collide or leave the road? Find the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `hybrid_optuna`: 48 kept runs on 10 scenes, varying ego_speed_scale, actor_time_shift_s; 2 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 4 of 5 challenging settings confirmed, after 5 rounds.

## Answer

The study confirmed 4 of the 5 cases it was looking for. Each one is on a different scene, and repeats put its failure rate above 0.5: 0.8x / +0.5 s on 07981e6a (S3), 1.2x / +1.5 s on 0d4893f5 (S9), 1.4x / -0.5 s on 18f8dbd6 (S19) and 1.0x / +2 s on 1bbe02fc (S20). Each rests on only a few repeats, so the ranges are wide; they show the rate is high, not how high. None of the failures involved the pedestrian. In every one the policy drifted left, against a STRAIGHT or RIGHT command, into a car beside or ahead of it, into parked cars, or off the road. The study did not run 1.0x / 0 s on these four scenes, so it cannot say whether the speed and timing combination causes these failures or whether the scenes fail anyway. Also, the S20 failures are off-road flags only about 0.8–0.9 m from the human's path, which the triage marks as possibly a map-boundary quirk rather than a policy error.

## Findings

- Every run failed at 0.8x / +0.5 s on 07981e6a. The ego drifted left toward the curb lane of parked cars instead of turning right, and side-swiped or hit them. The policy was at fault; no pedestrian was involved.
  - S3: 07981e6a at ego_speed_scale 0.8, actor_time_shift_s 0.5: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_2hz_hybrid_optuna_009, pedestrian_ego_speed_2hz_hybrid_optuna_011, pedestrian_ego_speed_2hz_hybrid_optuna_012)
- Every run failed at 1.2x / +1.5 s on 0d4893f5. The ego drifted about 1.5 m left into vehicle 33, which was driving alongside it, while the command was STRAIGHT then RIGHT. The policy was at fault.
  - S9: 0d4893f5 at ego_speed_scale 1.2, actor_time_shift_s 1.5: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_2hz_hybrid_optuna_005, pedestrian_ego_speed_2hz_hybrid_optuna_013, pedestrian_ego_speed_2hz_hybrid_optuna_014)
- Every run failed at 1.4x / -0.5 s on 18f8dbd6. At about 12 m/s the policy cut left into the next lane and ran into slower car 2. The policy was at fault.
  - S19: 18f8dbd6 at ego_speed_scale 1.4, actor_time_shift_s -0.5: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_2hz_hybrid_optuna_006, pedestrian_ego_speed_2hz_hybrid_optuna_015, pedestrian_ego_speed_2hz_hybrid_optuna_016)
- Every run at 1.0x / +2 s on 1bbe02fc was flagged off-road at the stop line, 1.5 s after hand-off, with no contact. The ego was only about 0.8–0.9 m from the human's path, so triage marks fault as unclear and this case may be a map-edge artifact rather than a real departure from the road.
  - S20: 1bbe02fc at ego_speed_scale 1, actor_time_shift_s 2: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_2hz_hybrid_optuna_008, pedestrian_ego_speed_2hz_hybrid_optuna_017, pedestrian_ego_speed_2hz_hybrid_optuna_018)
- The best candidate for a fifth case, 1.4x / -1 s on 18d28973, failed in only some of many repeats, and its range does not clear 0.5. Its failures came from not braking for slowing car 99 while going straight against a RIGHT command. A neighbouring setting and lower speeds on this scene did not fail in their few runs.
  - S17: 18d28973 at ego_speed_scale 1.4, actor_time_shift_s -1: 3/11 failed, rate 11%-52% (90%) (pedestrian_ego_speed_2hz_hybrid_optuna_034, pedestrian_ego_speed_2hz_hybrid_optuna_041, pedestrian_ego_speed_2hz_hybrid_optuna_042, pedestrian_ego_speed_2hz_hybrid_optuna_043, pedestrian_ego_speed_2hz_hybrid_optuna_044, pedestrian_ego_speed_2hz_hybrid_optuna_045, pedestrian_ego_speed_2hz_hybrid_optuna_046, pedestrian_ego_speed_2hz_hybrid_optuna_047, pedestrian_ego_speed_2hz_hybrid_optuna_048, pedestrian_ego_speed_2hz_hybrid_optuna_049, pedestrian_ego_speed_2hz_hybrid_optuna_050)
  - S18: 18d28973 at ego_speed_scale 1.4, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_hybrid_optuna_035)
  - S15: 18d28973 at ego_speed_scale 1.2, actor_time_shift_s 0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_hybrid_optuna_028)
  - S16: 18d28973 at ego_speed_scale 1.2, actor_time_shift_s 0.5: 0/2 failed, rate 0%-58% (90%) (pedestrian_ego_speed_2hz_hybrid_optuna_001, pedestrian_ego_speed_2hz_hybrid_optuna_025)
- Across the failing scenes, the failures came from the same policy behaviour: a left drift away from the route, not a reaction to the pedestrian's timing. This suggests the left drift is still there at 2 Hz planning.
  - S3: 07981e6a at ego_speed_scale 0.8, actor_time_shift_s 0.5: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_2hz_hybrid_optuna_009, pedestrian_ego_speed_2hz_hybrid_optuna_011, pedestrian_ego_speed_2hz_hybrid_optuna_012)
  - S9: 0d4893f5 at ego_speed_scale 1.2, actor_time_shift_s 1.5: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_2hz_hybrid_optuna_005, pedestrian_ego_speed_2hz_hybrid_optuna_013, pedestrian_ego_speed_2hz_hybrid_optuna_014)
  - S19: 18f8dbd6 at ego_speed_scale 1.4, actor_time_shift_s -0.5: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_2hz_hybrid_optuna_006, pedestrian_ego_speed_2hz_hybrid_optuna_015, pedestrian_ego_speed_2hz_hybrid_optuna_016)
  - S17: 18d28973 at ego_speed_scale 1.4, actor_time_shift_s -1: 3/11 failed, rate 11%-52% (90%) (pedestrian_ego_speed_2hz_hybrid_optuna_034, pedestrian_ego_speed_2hz_hybrid_optuna_041, pedestrian_ego_speed_2hz_hybrid_optuna_042, pedestrian_ego_speed_2hz_hybrid_optuna_043, pedestrian_ego_speed_2hz_hybrid_optuna_044, pedestrian_ego_speed_2hz_hybrid_optuna_045, pedestrian_ego_speed_2hz_hybrid_optuna_046, pedestrian_ego_speed_2hz_hybrid_optuna_047, pedestrian_ego_speed_2hz_hybrid_optuna_048, pedestrian_ego_speed_2hz_hybrid_optuna_049, pedestrian_ego_speed_2hz_hybrid_optuna_050)
- No settings tried on 0e002edd, 048b974e or 0caa8f1a failed. On 12a09194 the runs never came close to any actor (criticality 0), consistent with its pedestrian staying far away. These are hints from few runs per setting, not evidence that the scenes are safe.
  - S10: 0e002edd at ego_speed_scale 1, actor_time_shift_s 0.5: 0/3 failed, rate 0%-47% (90%) (pedestrian_ego_speed_2hz_hybrid_optuna_030, pedestrian_ego_speed_2hz_hybrid_optuna_031, pedestrian_ego_speed_2hz_hybrid_optuna_032)
  - S11: 0e002edd at ego_speed_scale 1.2, actor_time_shift_s -0.5: 0/3 failed, rate 0%-47% (90%) (pedestrian_ego_speed_2hz_hybrid_optuna_004, pedestrian_ego_speed_2hz_hybrid_optuna_021, pedestrian_ego_speed_2hz_hybrid_optuna_022)
  - S1: 048b974e at ego_speed_scale 1.2, actor_time_shift_s 2: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_hybrid_optuna_026)
  - S2: 048b974e at ego_speed_scale 1.4, actor_time_shift_s 1.5: 0/4 failed, rate 0%-40% (90%) (pedestrian_ego_speed_2hz_hybrid_optuna_003, pedestrian_ego_speed_2hz_hybrid_optuna_019, pedestrian_ego_speed_2hz_hybrid_optuna_020, pedestrian_ego_speed_2hz_hybrid_optuna_033)
  - S5: 0caa8f1a at ego_speed_scale 0.8, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_hybrid_optuna_039)
  - S6: 0caa8f1a at ego_speed_scale 1, actor_time_shift_s -1: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_hybrid_optuna_038)
  - S7: 0caa8f1a at ego_speed_scale 1.2, actor_time_shift_s 1: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_hybrid_optuna_029)
  - S8: 0caa8f1a at ego_speed_scale 1.4, actor_time_shift_s 0: 0/3 failed, rate 0%-47% (90%) (pedestrian_ego_speed_2hz_hybrid_optuna_007, pedestrian_ego_speed_2hz_hybrid_optuna_023, pedestrian_ego_speed_2hz_hybrid_optuna_024)
  - S12: 12a09194 at ego_speed_scale 0.6, actor_time_shift_s 0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_hybrid_optuna_010)
  - S13: 12a09194 at ego_speed_scale 1.2, actor_time_shift_s -2: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_hybrid_optuna_037)
  - S14: 12a09194 at ego_speed_scale 1.4, actor_time_shift_s 1: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_hybrid_optuna_036)
- 0b10bce8 is almost untested: only one run (1.0x / -1.5 s) was kept, and it did not fail. Both runs at 1.4x halted and were not kept.
  - S4: 0b10bce8 at ego_speed_scale 1, actor_time_shift_s -1.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_hybrid_optuna_040)

## Open

- Is the speed and timing combination the cause? Run 1.0x / 0 s a few times on 07981e6a, 0d4893f5, 18f8dbd6 and 1bbe02fc. If they fail there too, the four cases reflect the policy's left drift, not the pedestrian parameters.
- A fifth confirmed case: more repeats near S17 on 18d28973 (e.g. 1.4x / -1.5 s or -2 s), or searching 0e002edd or 048b974e at the grid corners, which got few runs.
- Whether the S20 off-road flags are real: check the drivable-area map at the 1bbe02fc stop line, or rerun with a looser boundary check.
- Why 0b10bce8 halts at 1.4x, and runs there that the gate keeps.
- No failure involved the pedestrian, so the study did not find a combination where the policy hits the person. Finding one may need settings that put the pedestrian in the ego's lane at the moment the ego arrives.
- Comparison with the 10 Hz study pedestrian_ego_speed: this study's results alone cannot say whether 2 Hz planning reduced the left-drift failures; set the matching settings side by side.

## Why the runs failed (triage from the video and log)

turned_into_actor 7, left_road 4, no_brake_for_lead 4

- pedestrian_ego_speed_2hz_hybrid_optuna_005: turned_into_actor, policy at fault: yes. Approaching the intersection at about 9.5 m/s, the ego's plan bent left toward the adjacent lane even though the route command was STRAIGHT and then RIGHT. The ego drifted about 1.5 m left of the recorded path and hit actor 33, which was driving alongside it in the left lane. Actor 33 was not a lead vehicle: the car ahead stayed about 18 m away.
- pedestrian_ego_speed_2hz_hybrid_optuna_006: turned_into_actor, policy at fault: yes. The ego was driving straight in the right lane at about 12 m/s. After handoff, the policy's planned path cut left into the next lane, while the recorded human path stayed right. The ego kept its speed and its front hit the slower silver car (actor 2) in that lane, closing from 27.6 m to 4.6 m in half a second.
- pedestrian_ego_speed_2hz_hybrid_optuna_008: left_road, policy at fault: unclear. The ego entered a large intersection at about 7 m/s with no lead conflict, and was flagged offroad at 6.2 s, just 1.5 s after handoff. At that moment it was only 0.8 m left of the human's recorded path and looks to be inside the intersection lanes, so this may be a quirk of the map boundary rather than a real departure, though the policy's orange plan was already bending straight/left away from the right-turn route.
- pedestrian_ego_speed_2hz_hybrid_optuna_009: turned_into_actor, policy at fault: yes. Approaching an intersection where it was told to turn RIGHT, the ego went the other way at about 9.5 m/s: it drifted left from the travel lane toward the curb lane full of parked cars. At 8.6 s its side scraped parked car 6. The recorded human path stayed to the right.
- pedestrian_ego_speed_2hz_hybrid_optuna_011: no_brake_for_lead, policy at fault: yes. The command was RIGHT and the route stayed in the right lane, but the ego drove at about 9.5 m/s in the left lane, which is lined with parked cars (3, 87/2). It drifted left toward the parked cars, slowed only slightly (to 8.4 m/s), and its front hit parked car 3 when the gap reached 0.7 m. The rear contact came after this front collision.
- pedestrian_ego_speed_2hz_hybrid_optuna_012: left_road, policy at fault: yes. The route said turn right, but the ego steered left out of its lane toward the curb on the left at about 9.5 m/s without braking. At 8.6 s it side-swiped parked car 87/2 and was also flagged as off-road. The camera view was clear before the crash.
- pedestrian_ego_speed_2hz_hybrid_optuna_013: turned_into_actor, policy at fault: yes. The ego was going straight through the intersection at about 9.5 m/s, with actor 33 driving alongside in the lane to its left. The ego drifted about 1.6 m left of the recorded path into that lane, and its front hit 33. It barely slowed, and the gap dropped from 18 m to 0.7 m once 33 counted as the actor ahead. The route command at that point was RIGHT, the opposite of the drift.
- pedestrian_ego_speed_2hz_hybrid_optuna_014: turned_into_actor, policy at fault: yes. The ego was going straight at about 9.5 m/s toward an intersection. Its planned path kept bending left out of its lane into the left lane, where vehicle 33 was driving alongside it. By 7.2 s the ego had cut left into vehicle 33 and hit it with its front corner, even though the route command was STRAIGHT and then RIGHT.
- pedestrian_ego_speed_2hz_hybrid_optuna_015: turned_into_actor, policy at fault: yes. After handoff the policy drifted left into the adjacent lane while the recorded path stayed in its lane (and the command became RIGHT). Holding about 12 m/s, the ego ran its front into actor 2, which was travelling ahead in that left lane.
- pedestrian_ego_speed_2hz_hybrid_optuna_016: turned_into_actor, policy at fault: yes. After handoff, the ego was going about 12 m/s in its lane. Its planned path drifted left into the next lane, while the recorded route stayed in its lane and then went right. The ego cut in behind actor 2 without slowing down and hit it with its front bumper. The gap to the car ahead first showed up at 27.5 m and was 4.4 m half a second later, which fits a lane change rather than a car braking ahead.
- pedestrian_ego_speed_2hz_hybrid_optuna_017: left_road, policy at fault: unclear. The ego was approaching the junction stop line at about 7 m/s, with no actor close ahead. Its planned path bent left across the junction while the route turned right. At 6.2 s it was flagged offroad at the stop line, drifted only 0.8 m left of the recorded human trajectory, which suggests a strict drivable-area boundary there rather than a clear departure from the road.
- pedestrian_ego_speed_2hz_hybrid_optuna_018: left_road, policy at fault: unclear. The route turned right at the intersection, but after handoff the policy planned straight and then left across the tram tracks, drifting left off the recorded path, and was flagged offroad at the stop line at about 7 m/s. No contact was recorded (collision_any stayed 0; the lead car was about 30 m ahead). The ego was only 0.9 m from the human's path and still looked to be inside the mapped lanes, so the offroad flag may be a map-edge artifact.
- pedestrian_ego_speed_2hz_hybrid_optuna_034: no_brake_for_lead, policy at fault: yes. The route said RIGHT and the human trajectory went right, but the ego kept going straight and edged slightly left into the path of white car 99. Car 99 was nearly stopped ahead at the intersection. The gap closed from 28 m to 4 m while the ego only slowed from 12.6 to 11.4 m/s, and its front hit 99. The rear contact reported in the run came after this frontal collision.
- pedestrian_ego_speed_2hz_hybrid_optuna_041: no_brake_for_lead, policy at fault: yes. The ego stayed in its lane at about 12 m/s even though the route said RIGHT and the recorded human moved one lane right. It closed on the white car ahead (actor 99), which was slowing as it approached the intersection: the gap shrank from 28 m to 4 m over 2 s while the ego slowed only from 12.6 to 11.2 m/s. It hit the car's rear with its front-left corner at 8.6 s. The rear contact on the ego came after this front collision.
- pedestrian_ego_speed_2hz_hybrid_optuna_045: no_brake_for_lead, policy at fault: yes. The ego was told to turn RIGHT but kept going straight toward the intersection at about 12–13 m/s, straddling the lane line on its left. It closed on a slow white car (actor 99) ahead and to the left at roughly 12 m/s, from about 28 m to contact in 2 seconds, and hit it with its front while barely slowing.

## Every setting

- S1: 048b974e at ego_speed_scale 1.2, actor_time_shift_s 2: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_hybrid_optuna_026)
- S2: 048b974e at ego_speed_scale 1.4, actor_time_shift_s 1.5: 0/4 failed, rate 0%-40% (90%) (pedestrian_ego_speed_2hz_hybrid_optuna_003, pedestrian_ego_speed_2hz_hybrid_optuna_019, pedestrian_ego_speed_2hz_hybrid_optuna_020, pedestrian_ego_speed_2hz_hybrid_optuna_033)
- S3: 07981e6a at ego_speed_scale 0.8, actor_time_shift_s 0.5: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_2hz_hybrid_optuna_009, pedestrian_ego_speed_2hz_hybrid_optuna_011, pedestrian_ego_speed_2hz_hybrid_optuna_012)
- S4: 0b10bce8 at ego_speed_scale 1, actor_time_shift_s -1.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_hybrid_optuna_040)
- S5: 0caa8f1a at ego_speed_scale 0.8, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_hybrid_optuna_039)
- S6: 0caa8f1a at ego_speed_scale 1, actor_time_shift_s -1: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_hybrid_optuna_038)
- S7: 0caa8f1a at ego_speed_scale 1.2, actor_time_shift_s 1: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_hybrid_optuna_029)
- S8: 0caa8f1a at ego_speed_scale 1.4, actor_time_shift_s 0: 0/3 failed, rate 0%-47% (90%) (pedestrian_ego_speed_2hz_hybrid_optuna_007, pedestrian_ego_speed_2hz_hybrid_optuna_023, pedestrian_ego_speed_2hz_hybrid_optuna_024)
- S9: 0d4893f5 at ego_speed_scale 1.2, actor_time_shift_s 1.5: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_2hz_hybrid_optuna_005, pedestrian_ego_speed_2hz_hybrid_optuna_013, pedestrian_ego_speed_2hz_hybrid_optuna_014)
- S10: 0e002edd at ego_speed_scale 1, actor_time_shift_s 0.5: 0/3 failed, rate 0%-47% (90%) (pedestrian_ego_speed_2hz_hybrid_optuna_030, pedestrian_ego_speed_2hz_hybrid_optuna_031, pedestrian_ego_speed_2hz_hybrid_optuna_032)
- S11: 0e002edd at ego_speed_scale 1.2, actor_time_shift_s -0.5: 0/3 failed, rate 0%-47% (90%) (pedestrian_ego_speed_2hz_hybrid_optuna_004, pedestrian_ego_speed_2hz_hybrid_optuna_021, pedestrian_ego_speed_2hz_hybrid_optuna_022)
- S12: 12a09194 at ego_speed_scale 0.6, actor_time_shift_s 0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_hybrid_optuna_010)
- S13: 12a09194 at ego_speed_scale 1.2, actor_time_shift_s -2: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_hybrid_optuna_037)
- S14: 12a09194 at ego_speed_scale 1.4, actor_time_shift_s 1: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_hybrid_optuna_036)
- S15: 18d28973 at ego_speed_scale 1.2, actor_time_shift_s 0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_hybrid_optuna_028)
- S16: 18d28973 at ego_speed_scale 1.2, actor_time_shift_s 0.5: 0/2 failed, rate 0%-58% (90%) (pedestrian_ego_speed_2hz_hybrid_optuna_001, pedestrian_ego_speed_2hz_hybrid_optuna_025)
- S17: 18d28973 at ego_speed_scale 1.4, actor_time_shift_s -1: 3/11 failed, rate 11%-52% (90%) (pedestrian_ego_speed_2hz_hybrid_optuna_034, pedestrian_ego_speed_2hz_hybrid_optuna_041, pedestrian_ego_speed_2hz_hybrid_optuna_042, pedestrian_ego_speed_2hz_hybrid_optuna_043, pedestrian_ego_speed_2hz_hybrid_optuna_044, pedestrian_ego_speed_2hz_hybrid_optuna_045, pedestrian_ego_speed_2hz_hybrid_optuna_046, pedestrian_ego_speed_2hz_hybrid_optuna_047, pedestrian_ego_speed_2hz_hybrid_optuna_048, pedestrian_ego_speed_2hz_hybrid_optuna_049, pedestrian_ego_speed_2hz_hybrid_optuna_050)
- S18: 18d28973 at ego_speed_scale 1.4, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_hybrid_optuna_035)
- S19: 18f8dbd6 at ego_speed_scale 1.4, actor_time_shift_s -0.5: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_2hz_hybrid_optuna_006, pedestrian_ego_speed_2hz_hybrid_optuna_015, pedestrian_ego_speed_2hz_hybrid_optuna_016)
- S20: 1bbe02fc at ego_speed_scale 1, actor_time_shift_s 2: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_2hz_hybrid_optuna_008, pedestrian_ego_speed_2hz_hybrid_optuna_017, pedestrian_ego_speed_2hz_hybrid_optuna_018)

## Not kept by the gate

- pedestrian_ego_speed_2hz_hybrid_optuna_002: not kept: HALT
- pedestrian_ego_speed_2hz_hybrid_optuna_027: not kept: HALT

## Provenance

Plan: `plan.json` (rationale: Copied from studies/pedestrian_ego_speed/plan.json (10 Hz) with the policy planning every 500 ms, so the method comparison can be repeated at 2 Hz. Scenes: these are the 10 scenes tagged pedestrian_crossing that have a recorded pedestrian key actor. Each scene's pedestrian is set in retime_tracks, so actor_time_shift_s moves only that person. actor_speed_scale stays at 1.0, so the pedestrian walks at the recorded speed. Traffic is replay, which keeps the scenario scripted as in Euro NCAP pedestrian tests. There is no delay, bias or noise.

Two other tagged scenes are left out: 095cf563 and 13a9767e. Neither has a pedestrian key actor, so a person-class retime there might hit no actor or the wrong one.

Budget: 5 rounds of 10 runs gives 50 runs, as the brief asks. The goal is top_k with k=5, high_min=0.5 and distinct scenes. With 90% ranges, each confirmed case needs about 4–5 failures out of 5 repeats, so roughly 25 runs go to confirmation and about 25 to searching the 5×9 grid. That is tight, and with partial results the study may confirm fewer than 5 cases.

Caveats:
- 6 of the scenes (048b974e, 07981e6a, 0caa8f1a, 0d4893f5, 18d28973, 1bbe02fc) failed at 0 delay in an earlier CATK run. That run used reactive traffic, not replay, so it may not carry over. If one still fails at 1.0x / 0 s, its failures may not come from speed or timing, and it fills a top_k slot cheaply without answering the question.
- 0e002edd, 18f8dbd6, 12a09194 and 0b10bce8 are the cleaner tests. In 0b10bce8 the ego barely moved (8.9 m), and in 12a09194 the pedestrian stayed far away (11.5 m).
- The failure check counts any front or side collision or leaving the road. It cannot tell whether the ego hit the pedestrian or another actor. Near misses are reported as closest approach to any actor, not ranked as failures.
- With ego_speed_scale above 1, the first second or two of the warm-up starts off the recorded scene.). Report written by claude-opus-5-5 from `results` in 24 s; every count above is computed from the queue, not written by the model.

50 of 50 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
