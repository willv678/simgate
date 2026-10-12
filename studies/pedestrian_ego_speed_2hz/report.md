# In pedestrian-crossing scenes, which combinations of ego speed at hand-off (0.6x–1.4x recorded) and pedestrian step-out time (±2 s) make the VaVAM policy with the linear MPC collide or leave the road? Find the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `pedestrian_ego_speed_2hz`: 49 kept runs on 9 scenes, varying ego_speed_scale, actor_time_shift_s; 2 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 4 of 5 challenging settings confirmed, after 5 rounds.

## Answer

The study confirmed 4 of the 5 cases it was asked for, each on a different scene. They are 0d4893f5 at 1.2x / −0.5 s, 0e002edd at 1.4x / 0 s, 18f8dbd6 at 1.4x / 0 s and 1bbe02fc at 1.2x / −0.5 s. The fifth candidate, 18d28973 at 1.4x / −1 s, failed only about half the time, and its range does not clear 0.5. None of the triaged failures involved the pedestrian. The ego drifted left into a car in the next lane, cut a right turn into parked cars, failed to brake for a slowing car ahead, or was flagged off-road. Every failure happened at 1.2x or 1.4x speed, and on the scenes tried at several step-out times, changing the pedestrian's timing did not change the outcome. So these cases show what makes the policy fail at higher hand-off speed, not what makes it fail with the pedestrian. Two of the four cases are weaker than the rest. The 1bbe02fc failures are marginal off-road flags that may come from the map's road edge. The 0e002edd failures are all marked as possible artifacts, but the triage reads them as real over-tight turns by the policy, not rendering faults.

## Findings

- 0d4893f5 at 1.2x / −0.5 s failed in every repeat. Each time the ego drifted left while crossing the intersection and hit vehicle 33, which was driving alongside, without braking. The policy was at fault, and the pedestrian was not involved.
  - S8: 0d4893f5 at ego_speed_scale 1.2, actor_time_shift_s -0.5: 4/4 failed, rate 60%-100% (90%) (pedestrian_ego_speed_2hz_029, pedestrian_ego_speed_2hz_034, pedestrian_ego_speed_2hz_035, pedestrian_ego_speed_2hz_036)
- 18f8dbd6 at 1.4x failed in every repeat at 0 s and in its single run at −0.5 s. Each time the ego held about 12 m/s, drifted left out of its lane against a RIGHT route, and hit car 2 with no meaningful braking. This left drift still appears with 2 Hz planning.
  - S24: 18f8dbd6 at ego_speed_scale 1.4, actor_time_shift_s 0: 4/4 failed, rate 60%-100% (90%) (pedestrian_ego_speed_2hz_005, pedestrian_ego_speed_2hz_011, pedestrian_ego_speed_2hz_012, pedestrian_ego_speed_2hz_013)
  - S23: 18f8dbd6 at ego_speed_scale 1.4, actor_time_shift_s -0.5: 1/1 failed, rate 27%-100% (90%) (pedestrian_ego_speed_2hz_014)
- 0e002edd at 1.4x failed at −0.5 s, 0 s and +0.5 s. At 0 s it failed in every repeat; the other two times have one run each. Each time the ego made the commanded right turn too tight at about 3–4 m/s and hit parked cars at the curb, about 7–8 m off the recorded path, which is why these runs are flagged as possible artifacts. The triage reads them as real policy errors, not rendering faults. At 0.8x–1.2x on the same scene, every run passed.
  - S14: 0e002edd at ego_speed_scale 1.4, actor_time_shift_s 0: 4/4 failed, rate 60%-100% (90%), 4 possibly the simulator's (pedestrian_ego_speed_2hz_015, pedestrian_ego_speed_2hz_021, pedestrian_ego_speed_2hz_022, pedestrian_ego_speed_2hz_023_a2)
  - S13: 0e002edd at ego_speed_scale 1.4, actor_time_shift_s -0.5: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (pedestrian_ego_speed_2hz_016)
  - S15: 0e002edd at ego_speed_scale 1.4, actor_time_shift_s 0.5: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (pedestrian_ego_speed_2hz_017)
  - S9: 0e002edd at ego_speed_scale 0.8, actor_time_shift_s 0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_003)
  - S10: 0e002edd at ego_speed_scale 1, actor_time_shift_s -1: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_010)
  - S11: 0e002edd at ego_speed_scale 1.2, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_001)
  - S12: 0e002edd at ego_speed_scale 1.2, actor_time_shift_s 0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_002)
- 1bbe02fc at 1.2x / −0.5 s failed in every repeat, but only as off-road flags with no collision. The ego was only about 0.8 m from the human's path, and the command showed STRAIGHT on a route that turns right. The triage marks policy fault as unclear in most of these runs and says the flag may come from the map's road boundary. This is the weakest of the four confirmed cases.
  - S25: 1bbe02fc at ego_speed_scale 1.2, actor_time_shift_s -0.5: 4/4 failed, rate 60%-100% (90%) (pedestrian_ego_speed_2hz_030, pedestrian_ego_speed_2hz_037, pedestrian_ego_speed_2hz_038, pedestrian_ego_speed_2hz_039)
- 18d28973 at 1.4x / −1 s failed about half the time, so it is not confirmed above 0.5. Its failures were rear-end crashes into a slowing sedan (actor 99): the ego went straight, straddling the lane line, on a RIGHT route and only eased off. Nearby settings on this scene each passed, but each had only one run.
  - S19: 18d28973 at ego_speed_scale 1.4, actor_time_shift_s -1: 5/10 failed, rate 27%-73% (90%) (pedestrian_ego_speed_2hz_024, pedestrian_ego_speed_2hz_031, pedestrian_ego_speed_2hz_032, pedestrian_ego_speed_2hz_033, pedestrian_ego_speed_2hz_041, pedestrian_ego_speed_2hz_042, pedestrian_ego_speed_2hz_043, pedestrian_ego_speed_2hz_044, pedestrian_ego_speed_2hz_045, pedestrian_ego_speed_2hz_046)
  - S17: 18d28973 at ego_speed_scale 1.2, actor_time_shift_s -1: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_019)
  - S18: 18d28973 at ego_speed_scale 1.2, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_009)
  - S20: 18d28973 at ego_speed_scale 1.4, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_018)
  - S21: 18d28973 at ego_speed_scale 1.4, actor_time_shift_s 0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_025)
- 048b974e had no failures, even at 1.4x / −1 s with repeats. 0caa8f1a, 12a09194 and 0b10bce8 had no failures either, but each setting tried there had only one run, so that is only a hint. One run on 0b10bce8 was not kept.
  - S1: 048b974e at ego_speed_scale 1.2, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_028)
  - S2: 048b974e at ego_speed_scale 1.4, actor_time_shift_s -1: 0/4 failed, rate 0%-40% (90%) (pedestrian_ego_speed_2hz_047, pedestrian_ego_speed_2hz_048, pedestrian_ego_speed_2hz_049, pedestrian_ego_speed_2hz_050)
  - S3: 048b974e at ego_speed_scale 1.4, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_040)
  - S5: 0caa8f1a at ego_speed_scale 1.2, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_020)
  - S6: 0caa8f1a at ego_speed_scale 1.4, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_026)
  - S7: 0caa8f1a at ego_speed_scale 1.4, actor_time_shift_s 0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_027)
  - S16: 12a09194 at ego_speed_scale 1.4, actor_time_shift_s -1.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_008)
  - S4: 0b10bce8 at ego_speed_scale 1.2, actor_time_shift_s 0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_007)
- No triaged failure was a collision with the retimed pedestrian. Every collision was with another vehicle or a parked car, and the rest were off-road flags. The pedestrian step-out knob did not drive any confirmed failure.
  - S8: 0d4893f5 at ego_speed_scale 1.2, actor_time_shift_s -0.5: 4/4 failed, rate 60%-100% (90%) (pedestrian_ego_speed_2hz_029, pedestrian_ego_speed_2hz_034, pedestrian_ego_speed_2hz_035, pedestrian_ego_speed_2hz_036)
  - S14: 0e002edd at ego_speed_scale 1.4, actor_time_shift_s 0: 4/4 failed, rate 60%-100% (90%), 4 possibly the simulator's (pedestrian_ego_speed_2hz_015, pedestrian_ego_speed_2hz_021, pedestrian_ego_speed_2hz_022, pedestrian_ego_speed_2hz_023_a2)
  - S24: 18f8dbd6 at ego_speed_scale 1.4, actor_time_shift_s 0: 4/4 failed, rate 60%-100% (90%) (pedestrian_ego_speed_2hz_005, pedestrian_ego_speed_2hz_011, pedestrian_ego_speed_2hz_012, pedestrian_ego_speed_2hz_013)
  - S25: 1bbe02fc at ego_speed_scale 1.2, actor_time_shift_s -0.5: 4/4 failed, rate 60%-100% (90%) (pedestrian_ego_speed_2hz_030, pedestrian_ego_speed_2hz_037, pedestrian_ego_speed_2hz_038, pedestrian_ego_speed_2hz_039)
  - S19: 18d28973 at ego_speed_scale 1.4, actor_time_shift_s -1: 5/10 failed, rate 27%-73% (90%) (pedestrian_ego_speed_2hz_024, pedestrian_ego_speed_2hz_031, pedestrian_ego_speed_2hz_032, pedestrian_ego_speed_2hz_033, pedestrian_ego_speed_2hz_041, pedestrian_ego_speed_2hz_042, pedestrian_ego_speed_2hz_043, pedestrian_ego_speed_2hz_044, pedestrian_ego_speed_2hz_045, pedestrian_ego_speed_2hz_046)

## Open

- Whether the four confirmed scenes also fail at nominal settings (1.0x, 0 s). No nominal run was made on 0d4893f5, 18f8dbd6 or 1bbe02fc, and 0e002edd had only one run at 1.0x (at −1 s). A few repeats at 1.0x / 0 s on each would show whether speed is the cause.
- Whether pedestrian timing matters at all. Sweeping the step-out time from −2 s to +2 s at the failing speed on 0d4893f5 and 1bbe02fc, and repeating 0e002edd at ±0.5 s, would test whether the outcome changes with timing. The single runs so far suggest it does not.
- A fifth case on a distinct scene. More repeats of 18d28973 at 1.4x / −1 s are needed to see whether its rate clears 0.5. A first search of 048b974e, 0caa8f1a and 12a09194 at 0.6x–0.8x would cover lower speeds, which were barely tried anywhere.
- Whether the 1bbe02fc off-road flags are real. That needs a check of the map's road boundary at the intersection entry, or a rerun with a corrected route command.
- How these results compare with the 10 Hz study. This data cannot show whether 2 Hz planning halves the left drift; the left drift is still present in 0d4893f5 and 18f8dbd6.

## Why the runs failed (triage from the video and log)

turned_into_actor 15, no_brake_for_lead 5, left_road 4

- pedestrian_ego_speed_2hz_005: turned_into_actor, policy at fault: yes. After handoff the ego, going about 12 m/s in the right lane with the route continuing straight and then right, steered left into the adjacent lane and hit the front of car 2, which was ahead in that lane, without braking. The ego was 1.5 m off the recorded path when it hit.
- pedestrian_ego_speed_2hz_011: turned_into_actor, policy at fault: yes. After handoff the policy kept about 12 m/s and drifted left out of its lane into the next lane, which the recorded human did not do (the human path stays right, and the command turns RIGHT). It ran its front into the silver car (actor 2) driving in that lane and never braked meaningfully.
- pedestrian_ego_speed_2hz_012: turned_into_actor, policy at fault: yes. On a straight multi-lane road, the policy took over and drifted left out of its lane toward the adjacent lane, while the recorded human path stayed right. Holding about 12 m/s with no braking, it cut in close behind/beside actor 2 in that lane and hit it with its front.
- pedestrian_ego_speed_2hz_013: turned_into_actor, policy at fault: yes. After handoff the ego held about 12 m/s and drifted left into the next lane, while the recorded route went straight and then right. That put it right behind the slower actor 2. The gap to actor 2 fell from 27.6 m to 4.5 m in half a second, and the ego hit its rear with almost no braking.
- pedestrian_ego_speed_2hz_014: turned_into_actor, policy at fault: yes. After handoff, the ego held about 12 m/s and veered left into the next lane instead of following the recorded path, which stays right (the command changes to RIGHT). Its front hit car 2, a slower vehicle in that lane, without braking. The gap to car 2 fell from 27.6 m to 4.5 m in the last half second.
- pedestrian_ego_speed_2hz_015: turned_into_actor, policy at fault: yes. On a RIGHT command, the ego made a tight, slow right turn (about 3.5 m/s) that drifted almost 8 m off the recorded path toward the curb and the parked cars on the new street. Its front hit vehicle 112, which was turning into the same street just ahead and to its side (gap 4.1 m at 9.6 s), and the ego also left the drivable area at the corner.
- pedestrian_ego_speed_2hz_016: turned_into_actor, policy at fault: yes. While making the commanded right turn at the intersection, the ego turned much more sharply than the recorded human path. By 9.6 s it was pointing almost straight at the curb and drove front-first into the parked cars along the curb (actors 90/16), about 7.5 m off the recorded path.
- pedestrian_ego_speed_2hz_017: turned_into_actor, policy at fault: yes. On the commanded right turn, the ego turned far too tightly at about 3.5 m/s and left the recorded path by about 8 m. It headed across the lane toward the curb and hit a car parked there (actor 90/119 area) with its front. By 10.1 s the camera shows the ego pointed straight at the sidewalk and a brick wall.
- pedestrian_ego_speed_2hz_021: turned_into_actor, policy at fault: yes. With a RIGHT command at the intersection, the ego turned too wide and too sharply at about 3–4 m/s. It ran across the travel lane into the curbside parking lane and hit parked car 90 with its front, ending 7.6 m from the recorded human path. Its own planned path (orange) pointed into the row of parked cars the whole time.
- pedestrian_ego_speed_2hz_022: turned_into_actor, policy at fault: yes. On the RIGHT command, the ego turned right at the intersection. It cut the turn tighter than the human path and sped up from 3.2 to 4.0 m/s, and its front hit parked car 90 at the curb of the cross street, about 6.8 m off the recorded trajectory. Car 112, which was crossing behind, also touched the ego's rear, and the run was flagged offroad as the ego went into the curb-side parking area.
- pedestrian_ego_speed_2hz_024: no_brake_for_lead, policy at fault: yes. The route said RIGHT, but the ego went straight and drifted slightly left into the path of the white sedan (actor 99), which was braking to a near stop ahead of it before the intersection. The ego only eased from about 13 to 10 m/s while the gap shrank from 34 m to 0.5 m, so it hit the sedan with its front. It was rear-ended only after that.
- pedestrian_ego_speed_2hz_029: turned_into_actor, policy at fault: yes. After handoff the ego was going straight at about 9.5 m/s. Its path bent left toward the next lane while it crossed the intersection, so it moved into that lane and hit actor 33, which was driving next to it on the left. The lead vehicle stayed about 18 m ahead, and the camera view looked clean until the moment of impact.
- pedestrian_ego_speed_2hz_030: left_road, policy at fault: unclear. The route turns right at the intersection, but after handoff at 4.7s the policy kept planning straight and slightly left, and the ego was flagged offroad at 6.2s as it reached the stop line at about 9 m/s. It was only 0.8 m from the human's path and its box still looks inside the lanes on the map, so the offroad flag may come from the map's road boundary rather than a real departure.
- pedestrian_ego_speed_2hz_023_a2: turned_into_actor, policy at fault: yes. On a RIGHT command, the ego made the turn at about 3–4 m/s but turned too wide and never straightened into the lane like the human did. It ended up nearly crosswise to the new street, about 7 m off the recorded path, and drove its front into parked car 90 at the curb, which also put it off the road.
- pedestrian_ego_speed_2hz_031: no_brake_for_lead, policy at fault: yes. The route said turn right and the recorded path bore right, but the ego went straight while straddling the lane line to its left. Actor 99, a white sedan that was nearly stopped and partly in the ego's path, was ahead. The gap shrank by about 11 m/s from 34 m to 0.4 m, but the ego only eased off from 12.9 to 10.1 m/s and hit 99's rear corner with its front.
- pedestrian_ego_speed_2hz_032: no_brake_for_lead, policy at fault: yes. A white car (actor 99) was stopped just ahead of the ego, a little to the left. The ego had drifted about 2 m left of the recorded right-turn path, toward that car. It barely slowed (12.9 to 10.1 m/s) while the gap closed at about 11 m/s, from 34 m to 0.5 m, and its front hit the stopped car at 9.1 s. The rear contact happened later and does not explain the crash.
- pedestrian_ego_speed_2hz_034: turned_into_actor, policy at fault: yes. Approaching the intersection at about 9–10 m/s, the policy's planned path (orange) kept angling left, away from the recorded straight path in its own lane. The ego drifted into the left lane and hit vehicle 33 with its front corner. Vehicle 33 had been driving alongside in that lane.
- pedestrian_ego_speed_2hz_035: turned_into_actor, policy at fault: yes. While approaching the intersection at about 9 m/s, the ego drifted left out of its lane, about 1.3 m off the recorded path. Its front-left corner hit actor 33, which was driving alongside in the left lane. The car ahead was still about 18 m away, so this was not a lead-vehicle crash, and the rear contact came only after this front collision.
- pedestrian_ego_speed_2hz_036: turned_into_actor, policy at fault: yes. While going straight through the intersection at about 9.5 m/s, the ego drifted about 2 m left of the recorded path into the adjacent left lane and ran its front into vehicle 33, which was driving alongside. It never braked, and the 0.6 m gap at the end is vehicle 33 becoming the actor ahead, not a sudden stop by the lead car.
- pedestrian_ego_speed_2hz_037: left_road, policy at fault: unclear. At about 9 m/s, the ego was entering a signalized intersection with a green light, and the policy's plan ran straight ahead. The route, which the command showed as STRAIGHT until the last frame, actually turns right. At 6.2 s the ego was flagged offroad at the intersection entry while only 0.8 m from the recorded human path, and there was no contact with any actor.
- pedestrian_ego_speed_2hz_038: left_road, policy at fault: unclear. The ego was approaching an intersection at about 9 m/s. The route turned right, but the command stayed STRAIGHT until the last frame, and the policy planned straight ahead and slightly left. At the stop line it was flagged offroad, only 0.8 m from where the human drove, with no collision and the lead car about 29 m ahead.
- pedestrian_ego_speed_2hz_039: left_road, policy at fault: yes. The route turns right at the intersection, but the command showed STRAIGHT until the last frame. After the 4.7 s handoff the policy planned a straight, slightly left-bearing path across the intersection instead of following the right curve. At about 9 m/s the ego's box crossed the drivable-area edge as it entered the intersection. It was only 0.8 m off the human trajectory at that point, so this is a marginal clip, and there was no collision.
- pedestrian_ego_speed_2hz_043: no_brake_for_lead, policy at fault: yes. The ego was told to keep right but stayed in the left lane, straddling the lane line, behind the white sedan (actor 99), which was slowing toward the intersection. The ego only eased from 13 to 10.4 m/s while the gap fell from 34 m to 0, and its front hit the sedan's rear-right corner.
- pedestrian_ego_speed_2hz_045: no_brake_for_lead, policy at fault: yes. The route said RIGHT and the recorded path turned right, but the ego kept going straight toward the intersection with its body over the lane line to its left. That put it partly in the path of a white sedan (actor 99), which was slowing ahead of it. The ego only eased off from about 13 to 10 m/s while the gap shrank from 34 m to 0.4 m, and its front hit the sedan at 9.1 s. The rear contact came after this front collision.

## Every setting

- S1: 048b974e at ego_speed_scale 1.2, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_028)
- S2: 048b974e at ego_speed_scale 1.4, actor_time_shift_s -1: 0/4 failed, rate 0%-40% (90%) (pedestrian_ego_speed_2hz_047, pedestrian_ego_speed_2hz_048, pedestrian_ego_speed_2hz_049, pedestrian_ego_speed_2hz_050)
- S3: 048b974e at ego_speed_scale 1.4, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_040)
- S4: 0b10bce8 at ego_speed_scale 1.2, actor_time_shift_s 0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_007)
- S5: 0caa8f1a at ego_speed_scale 1.2, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_020)
- S6: 0caa8f1a at ego_speed_scale 1.4, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_026)
- S7: 0caa8f1a at ego_speed_scale 1.4, actor_time_shift_s 0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_027)
- S8: 0d4893f5 at ego_speed_scale 1.2, actor_time_shift_s -0.5: 4/4 failed, rate 60%-100% (90%) (pedestrian_ego_speed_2hz_029, pedestrian_ego_speed_2hz_034, pedestrian_ego_speed_2hz_035, pedestrian_ego_speed_2hz_036)
- S9: 0e002edd at ego_speed_scale 0.8, actor_time_shift_s 0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_003)
- S10: 0e002edd at ego_speed_scale 1, actor_time_shift_s -1: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_010)
- S11: 0e002edd at ego_speed_scale 1.2, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_001)
- S12: 0e002edd at ego_speed_scale 1.2, actor_time_shift_s 0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_002)
- S13: 0e002edd at ego_speed_scale 1.4, actor_time_shift_s -0.5: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (pedestrian_ego_speed_2hz_016)
- S14: 0e002edd at ego_speed_scale 1.4, actor_time_shift_s 0: 4/4 failed, rate 60%-100% (90%), 4 possibly the simulator's (pedestrian_ego_speed_2hz_015, pedestrian_ego_speed_2hz_021, pedestrian_ego_speed_2hz_022, pedestrian_ego_speed_2hz_023_a2)
- S15: 0e002edd at ego_speed_scale 1.4, actor_time_shift_s 0.5: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (pedestrian_ego_speed_2hz_017)
- S16: 12a09194 at ego_speed_scale 1.4, actor_time_shift_s -1.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_008)
- S17: 18d28973 at ego_speed_scale 1.2, actor_time_shift_s -1: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_019)
- S18: 18d28973 at ego_speed_scale 1.2, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_009)
- S19: 18d28973 at ego_speed_scale 1.4, actor_time_shift_s -1: 5/10 failed, rate 27%-73% (90%) (pedestrian_ego_speed_2hz_024, pedestrian_ego_speed_2hz_031, pedestrian_ego_speed_2hz_032, pedestrian_ego_speed_2hz_033, pedestrian_ego_speed_2hz_041, pedestrian_ego_speed_2hz_042, pedestrian_ego_speed_2hz_043, pedestrian_ego_speed_2hz_044, pedestrian_ego_speed_2hz_045, pedestrian_ego_speed_2hz_046)
- S20: 18d28973 at ego_speed_scale 1.4, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_018)
- S21: 18d28973 at ego_speed_scale 1.4, actor_time_shift_s 0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_025)
- S22: 18f8dbd6 at ego_speed_scale 1.2, actor_time_shift_s -1: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_004)
- S23: 18f8dbd6 at ego_speed_scale 1.4, actor_time_shift_s -0.5: 1/1 failed, rate 27%-100% (90%) (pedestrian_ego_speed_2hz_014)
- S24: 18f8dbd6 at ego_speed_scale 1.4, actor_time_shift_s 0: 4/4 failed, rate 60%-100% (90%) (pedestrian_ego_speed_2hz_005, pedestrian_ego_speed_2hz_011, pedestrian_ego_speed_2hz_012, pedestrian_ego_speed_2hz_013)
- S25: 1bbe02fc at ego_speed_scale 1.2, actor_time_shift_s -0.5: 4/4 failed, rate 60%-100% (90%) (pedestrian_ego_speed_2hz_030, pedestrian_ego_speed_2hz_037, pedestrian_ego_speed_2hz_038, pedestrian_ego_speed_2hz_039)

## Not kept by the gate

- pedestrian_ego_speed_2hz_006: not kept: HALT
- pedestrian_ego_speed_2hz_023: not kept: RE-RUN

## Provenance

Plan: `plan.json` (rationale: Copied from studies/pedestrian_ego_speed/plan.json (10 Hz) with the policy planning every 500 ms, so the method comparison can be repeated at 2 Hz. Scenes: these are the 10 scenes tagged pedestrian_crossing that have a recorded pedestrian key actor. Each scene's pedestrian is set in retime_tracks, so actor_time_shift_s moves only that person. actor_speed_scale stays at 1.0, so the pedestrian walks at the recorded speed. Traffic is replay, which keeps the scenario scripted as in Euro NCAP pedestrian tests. There is no delay, bias or noise.

Two other tagged scenes are left out: 095cf563 and 13a9767e. Neither has a pedestrian key actor, so a person-class retime there might hit no actor or the wrong one.

Budget: 5 rounds of 10 runs gives 50 runs, as the brief asks. The goal is top_k with k=5, high_min=0.5 and distinct scenes. With 90% ranges, each confirmed case needs about 4–5 failures out of 5 repeats, so roughly 25 runs go to confirmation and about 25 to searching the 5×9 grid. That is tight, and with partial results the study may confirm fewer than 5 cases.

Caveats:
- 6 of the scenes (048b974e, 07981e6a, 0caa8f1a, 0d4893f5, 18d28973, 1bbe02fc) failed at 0 delay in an earlier CATK run. That run used reactive traffic, not replay, so it may not carry over. If one still fails at 1.0x / 0 s, its failures may not come from speed or timing, and it fills a top_k slot cheaply without answering the question.
- 0e002edd, 18f8dbd6, 12a09194 and 0b10bce8 are the cleaner tests. In 0b10bce8 the ego barely moved (8.9 m), and in 12a09194 the pedestrian stayed far away (11.5 m).
- The failure check counts any front or side collision or leaving the road. It cannot tell whether the ego hit the pedestrian or another actor. Near misses are reported as closest approach to any actor, not ranked as failures.
- With ego_speed_scale above 1, the first second or two of the warm-up starts off the recorded scene.). Report written by claude-opus-5-5 from `results` in 27 s; every count above is computed from the queue, not written by the model.

51 of 51 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
