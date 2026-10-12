# In pedestrian-crossing scenes, which combinations of ego speed at hand-off (0.6x–1.4x recorded) and pedestrian step-out time (±2 s) make the VaVAM policy with the linear MPC collide or leave the road? Find the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `rules`: 50 kept runs on 10 scenes, varying ego_speed_scale, actor_time_shift_s; 0 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 4 of 5 challenging settings confirmed, after 5 rounds.

## Answer

The study did not find any combination of ego speed and pedestrian timing that makes the policy fail, so it does not answer the question. It confirmed four of the five cases it was asked for, on four different scenes (S1, S2, S11, S29). All four are at the nominal setting (1.0x speed, 0 s shift), and none involves the pedestrian. The ego hit parked or moving vehicles or left the road after ignoring or misreading the route command. Not every failure is clearly the policy's fault: some S11 and S29 failures are "unclear" in the review, and every S1 failure is flagged as a possible simulator artifact. No run at any other speed or timing failed, but most of those settings ran only once, which is a hint, not a rate. Most of the speed–timing grid was never run.

## Findings

- Four scenes fail at the nominal setting (1.0x, 0 s) on every repeat, and the ranges put their failure rates above 0.5. These are the four confirmed cases. Because they fail without any speed or timing change, they fill top-k slots without saying anything about speed or timing.
  - S1: 048b974e at ego_speed_scale 1.0, actor_time_shift_s 0.0: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (pedestrian_ego_speed_2hz_rules_005, pedestrian_ego_speed_2hz_rules_011, pedestrian_ego_speed_2hz_rules_021)
  - S2: 07981e6a at ego_speed_scale 1.0, actor_time_shift_s 0.0: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_2hz_rules_006, pedestrian_ego_speed_2hz_rules_012, pedestrian_ego_speed_2hz_rules_022)
  - S11: 0d4893f5 at ego_speed_scale 1.0, actor_time_shift_s 0.0: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_2hz_rules_008, pedestrian_ego_speed_2hz_rules_013, pedestrian_ego_speed_2hz_rules_023)
  - S29: 1bbe02fc at ego_speed_scale 1.0, actor_time_shift_s 0.0: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_2hz_rules_010, pedestrian_ego_speed_2hz_rules_014, pedestrian_ego_speed_2hz_rules_024)
- In none of the confirmed failures did the ego hit the pedestrian. The reviews of the runs show front collisions with vehicles (a van, a parked car, an adjacent-lane car) or leaving the road.
  - S1: 048b974e at ego_speed_scale 1.0, actor_time_shift_s 0.0: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (pedestrian_ego_speed_2hz_rules_005, pedestrian_ego_speed_2hz_rules_011, pedestrian_ego_speed_2hz_rules_021)
  - S2: 07981e6a at ego_speed_scale 1.0, actor_time_shift_s 0.0: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_2hz_rules_006, pedestrian_ego_speed_2hz_rules_012, pedestrian_ego_speed_2hz_rules_022)
  - S11: 0d4893f5 at ego_speed_scale 1.0, actor_time_shift_s 0.0: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_2hz_rules_008, pedestrian_ego_speed_2hz_rules_013, pedestrian_ego_speed_2hz_rules_023)
  - S29: 1bbe02fc at ego_speed_scale 1.0, actor_time_shift_s 0.0: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_2hz_rules_010, pedestrian_ego_speed_2hz_rules_014, pedestrian_ego_speed_2hz_rules_024)
- In 048b974e the policy turned the wrong way, or took a tight line on the turn, and drove into a white van at low speed without braking. The review blames the policy, but every failure here is flagged as a possible simulator artifact: the ego ended up far off the recorded path. So this case rests partly on runs the simulator may explain.
  - S1: 048b974e at ego_speed_scale 1.0, actor_time_shift_s 0.0: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (pedestrian_ego_speed_2hz_rules_005, pedestrian_ego_speed_2hz_rules_011, pedestrian_ego_speed_2hz_rules_021)
- In 07981e6a the route said turn right, but the policy kept going at about 11 m/s, drifted left into the parking lane and hit a parked car head-on. Every failure here is the policy's fault.
  - S2: 07981e6a at ego_speed_scale 1.0, actor_time_shift_s 0.0: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_2hz_rules_006, pedestrian_ego_speed_2hz_rules_012, pedestrian_ego_speed_2hz_rules_022)
- In 0d4893f5 the ego drifted left into a car in the adjacent lane in some runs, which is the policy's fault. In one run that car cut into the ego's lane, so that failure is not clearly the policy's.
  - S11: 0d4893f5 at ego_speed_scale 1.0, actor_time_shift_s 0.0: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_2hz_rules_008, pedestrian_ego_speed_2hz_rules_013, pedestrian_ego_speed_2hz_rules_023)
- In 1bbe02fc the route command read STRAIGHT until the last moment before a right turn. The ego was flagged off-road at the stop line only about 0.8 m from the recorded path. The off-road calls are marginal and mostly marked unclear, so this case may come from the route command or the lane-boundary geometry rather than from the driving itself.
  - S29: 1bbe02fc at ego_speed_scale 1.0, actor_time_shift_s 0.0: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_2hz_rules_010, pedestrian_ego_speed_2hz_rules_014, pedestrian_ego_speed_2hz_rules_024)
- Three scenes never failed at the nominal setting across several repeats each: 0caa8f1a, 0e002edd and 18f8dbd6.
  - S9: 0caa8f1a at ego_speed_scale 1.0, actor_time_shift_s 0.0: 0/5 failed, rate 0%-35% (90%) (pedestrian_ego_speed_2hz_rules_007, pedestrian_ego_speed_2hz_rules_016, pedestrian_ego_speed_2hz_rules_026, pedestrian_ego_speed_2hz_rules_032, pedestrian_ego_speed_2hz_rules_043)
  - S14: 0e002edd at ego_speed_scale 1.0, actor_time_shift_s 0.0: 0/4 failed, rate 0%-40% (90%) (pedestrian_ego_speed_2hz_rules_001, pedestrian_ego_speed_2hz_rules_015, pedestrian_ego_speed_2hz_rules_025, pedestrian_ego_speed_2hz_rules_031)
  - S28: 18f8dbd6 at ego_speed_scale 1.0, actor_time_shift_s 0.0: 0/4 failed, rate 0%-40% (90%) (pedestrian_ego_speed_2hz_rules_002, pedestrian_ego_speed_2hz_rules_017, pedestrian_ego_speed_2hz_rules_027, pedestrian_ego_speed_2hz_rules_033)
- Settings off nominal (0.6x–1.2x speed, step-out 0.5 s earlier) had no failures. Almost all ran once or twice, so their ranges still allow high failure rates.
  - S3: 0b10bce8 at ego_speed_scale 0.6, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_035)
  - S4: 0b10bce8 at ego_speed_scale 0.6, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_029)
  - S5: 0b10bce8 at ego_speed_scale 0.8, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_045)
  - S6: 0b10bce8 at ego_speed_scale 0.8, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_019)
  - S8: 0caa8f1a at ego_speed_scale 0.8, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_038)
  - S10: 0caa8f1a at ego_speed_scale 1.2, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_049)
  - S12: 0e002edd at ego_speed_scale 0.6, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_048)
  - S13: 0e002edd at ego_speed_scale 0.8, actor_time_shift_s 0.0: 0/2 failed, rate 0%-58% (90%) (pedestrian_ego_speed_2hz_rules_037, pedestrian_ego_speed_2hz_rules_042)
  - S15: 12a09194 at ego_speed_scale 0.6, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_036)
  - S16: 12a09194 at ego_speed_scale 0.6, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_030)
  - S17: 12a09194 at ego_speed_scale 0.8, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_046)
  - S18: 12a09194 at ego_speed_scale 0.8, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_020)
  - S20: 18d28973 at ego_speed_scale 0.6, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_044)
  - S21: 18d28973 at ego_speed_scale 0.6, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_034)
  - S22: 18d28973 at ego_speed_scale 0.8, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_040)
  - S23: 18d28973 at ego_speed_scale 0.8, actor_time_shift_s 0.0: 0/2 failed, rate 0%-58% (90%) (pedestrian_ego_speed_2hz_rules_018, pedestrian_ego_speed_2hz_rules_028)
  - S24: 18d28973 at ego_speed_scale 1.0, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_050)
  - S26: 18f8dbd6 at ego_speed_scale 0.6, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_047)
  - S27: 18f8dbd6 at ego_speed_scale 0.8, actor_time_shift_s 0.0: 0/2 failed, rate 0%-58% (90%) (pedestrian_ego_speed_2hz_rules_039, pedestrian_ego_speed_2hz_rules_041)
- In 12a09194 the pedestrian never came close (criticality zero at every setting tried), and in 0b10bce8 the ego barely moved. Neither scene is a useful test of speed and timing at the settings tried.
  - S3: 0b10bce8 at ego_speed_scale 0.6, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_035)
  - S4: 0b10bce8 at ego_speed_scale 0.6, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_029)
  - S5: 0b10bce8 at ego_speed_scale 0.8, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_045)
  - S6: 0b10bce8 at ego_speed_scale 0.8, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_019)
  - S7: 0b10bce8 at ego_speed_scale 1.0, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_004)
  - S15: 12a09194 at ego_speed_scale 0.6, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_036)
  - S16: 12a09194 at ego_speed_scale 0.6, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_030)
  - S17: 12a09194 at ego_speed_scale 0.8, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_046)
  - S18: 12a09194 at ego_speed_scale 0.8, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_020)
  - S19: 12a09194 at ego_speed_scale 1.0, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_003)

## Open

- Most of the grid was never run: no 1.4x speed, no later step-outs, and no shifts beyond 0.5 s earlier. Single runs at 1.2x–1.4x combined with step-outs 1–2 s earlier and later on the scenes that pass at nominal (0caa8f1a, 0e002edd, 18f8dbd6, 18d28973) would show whether speed and timing can cause a failure at all. 0caa8f1a at 1.2x (S10) is the closest to a failure so far.
- The fifth case is still missing. It needs repeats at any off-nominal setting that fails once, on a scene other than the four confirmed ones.
- The four failing scenes were never run away from nominal, so we cannot tell whether speed or timing makes them better or worse. They also never involve the pedestrian. Runs at 0.6x–1.4x on 07981e6a and 0d4893f5 would show whether the failures depend on speed.
- Whether S1's failures (all flagged as possible artifacts) and S29's marginal off-road calls are real policy failures needs a check of the videos and the lane geometry. For S29, a run with the correct RIGHT command from the start would separate a route-command problem from a driving failure.
- The failure check cannot tell a pedestrian hit from a vehicle hit. Another check is needed to answer the pedestrian question directly.
- Comparing with the 10 Hz study pedestrian_ego_speed needs that study's results side by side. Whether planning at 2 Hz reduces the leftward drift that dominates these failures is not settled here.

## Why the runs failed (triage from the video and log)

turned_into_actor 6, left_road 5, actor_hit_ego 1

- pedestrian_ego_speed_2hz_rules_005: turned_into_actor, policy at fault: yes. While turning right at the intersection, the ego took a tight line toward the right-hand parking row. It drove front-first into vehicle 155 (a white van that was parked or crawling at the right edge of the target road). The gap closed from 7.7 m to 3.7 m while the ego barely slowed, staying around 3.5 m/s.
- pedestrian_ego_speed_2hz_rules_006: left_road, policy at fault: yes. The route said RIGHT, but at about 11 m/s the ego ignored the turn and kept drifting left into the curbside parking lane. It struck parked car 3 head-on at 8.6 s, about 2.2 m off the recorded path, barely slowing (11.1 to 9.9 m/s) as the gap closed to 3.6 m.
- pedestrian_ego_speed_2hz_rules_008: turned_into_actor, policy at fault: yes. While going straight through the intersection at about 8.4 m/s, the ego drifted left out of its lane (about 1.7 m off the human path, which went straight and then right). It ran its front into actor 33 in the adjacent left lane without braking.
- pedestrian_ego_speed_2hz_rules_010: left_road, policy at fault: unclear. The route turns right at the intersection, but the command read STRAIGHT until the moment of failure. The policy's plan veered straight and to the left, away from the right-turn path. At 6.2 s the ego, going about 7 m/s, was flagged offroad at the stop line while only 0.8 m off the human trajectory, so the offroad call is marginal and may come from the narrow lane-boundary geometry or the late switch in the command.
- pedestrian_ego_speed_2hz_rules_011: turned_into_actor, policy at fault: yes. The route command was RIGHT, but the ego turned left at the intersection, off the recorded path, which went straight/right. It then drove at about 3.5 m/s into a white van (actor 155) facing it in the side street. The gap shrank from 9.3 m to 3.3 m without the ego braking meaningfully, and the hit was to the ego's front.
- pedestrian_ego_speed_2hz_rules_012: turned_into_actor, policy at fault: yes. The route said turn RIGHT, but the policy held about 11 m/s and drifted left out of its travel lane into the parking lane on the left. It ran into parked car 3 head-on without braking: the gap closed from 25 m to 3 m and speed only dropped to 10.2 m/s. Before the impact the camera view was clear and the parked cars were easy to see.
- pedestrian_ego_speed_2hz_rules_013: turned_into_actor, policy at fault: yes. While going straight through the intersection at about 8 m/s, the policy's path drifted left out of the ego's lane and into actor 33, which was driving alongside in the left lane. The ego's front struck it about 1.6 m off the human trajectory. The car ahead in the ego's own lane stayed about 20 m away, and the route command had just changed to RIGHT.
- pedestrian_ego_speed_2hz_rules_014: left_road, policy at fault: yes. The route turns right at the intersection, but the command read STRAIGHT until the last frame. The policy's plan (orange) went straight and then veered left across the junction. At about 7 m/s the ego drifted left of its lane at the stop line, ending 0.8 m off the recorded path and over the drivable-area boundary. No actor was involved.
- pedestrian_ego_speed_2hz_rules_021: turned_into_actor, policy at fault: yes. The route command was RIGHT, but the ego turned left at about 3.5 m/s across the intersection into the cross street. Its front hit vehicle 155, a white van on the left side of that street near the parked cars, about 6.5 m from where the human drove. The rear contact in this run is listed only as secondary; the front collision came first.
- pedestrian_ego_speed_2hz_rules_022: left_road, policy at fault: yes. Approaching an intersection where the route said turn RIGHT, the ego went straight and slowly drifted left out of its travel lane into the line of parked cars on the left curb. It kept going at about 10–11 m/s and hit parked car 3 with its front at 8.6 s, about 2.3 m off the recorded path.
- pedestrian_ego_speed_2hz_rules_023: actor_hit_ego, policy at fault: unclear. The ego drove straight toward the intersection at a steady 8.1–8.3 m/s and stayed in its lane. Actor 33, which had been beside it in the left lane, sped up and cut right into the ego's lane just ahead of it at the stop line, so the gap ahead dropped from 21.5 m to 4.4 m. The ego never braked and its front clipped car 33 as it cut in.
- pedestrian_ego_speed_2hz_rules_024: left_road, policy at fault: unclear. The route turns right at the intersection, but the camera command read STRAIGHT until the last frame, and the policy's planned path (orange) kept heading straight and slightly left across the junction. At 6.2 s, moving about 7.4 m/s, the ego was flagged offroad at the stop line, only 0.8 m from the recorded human path. Its box appears to just clip the curb corner where the right-turn lane begins.

## Every setting

- S1: 048b974e at ego_speed_scale 1.0, actor_time_shift_s 0.0: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (pedestrian_ego_speed_2hz_rules_005, pedestrian_ego_speed_2hz_rules_011, pedestrian_ego_speed_2hz_rules_021)
- S2: 07981e6a at ego_speed_scale 1.0, actor_time_shift_s 0.0: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_2hz_rules_006, pedestrian_ego_speed_2hz_rules_012, pedestrian_ego_speed_2hz_rules_022)
- S3: 0b10bce8 at ego_speed_scale 0.6, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_035)
- S4: 0b10bce8 at ego_speed_scale 0.6, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_029)
- S5: 0b10bce8 at ego_speed_scale 0.8, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_045)
- S6: 0b10bce8 at ego_speed_scale 0.8, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_019)
- S7: 0b10bce8 at ego_speed_scale 1.0, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_004)
- S8: 0caa8f1a at ego_speed_scale 0.8, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_038)
- S9: 0caa8f1a at ego_speed_scale 1.0, actor_time_shift_s 0.0: 0/5 failed, rate 0%-35% (90%) (pedestrian_ego_speed_2hz_rules_007, pedestrian_ego_speed_2hz_rules_016, pedestrian_ego_speed_2hz_rules_026, pedestrian_ego_speed_2hz_rules_032, pedestrian_ego_speed_2hz_rules_043)
- S10: 0caa8f1a at ego_speed_scale 1.2, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_049)
- S11: 0d4893f5 at ego_speed_scale 1.0, actor_time_shift_s 0.0: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_2hz_rules_008, pedestrian_ego_speed_2hz_rules_013, pedestrian_ego_speed_2hz_rules_023)
- S12: 0e002edd at ego_speed_scale 0.6, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_048)
- S13: 0e002edd at ego_speed_scale 0.8, actor_time_shift_s 0.0: 0/2 failed, rate 0%-58% (90%) (pedestrian_ego_speed_2hz_rules_037, pedestrian_ego_speed_2hz_rules_042)
- S14: 0e002edd at ego_speed_scale 1.0, actor_time_shift_s 0.0: 0/4 failed, rate 0%-40% (90%) (pedestrian_ego_speed_2hz_rules_001, pedestrian_ego_speed_2hz_rules_015, pedestrian_ego_speed_2hz_rules_025, pedestrian_ego_speed_2hz_rules_031)
- S15: 12a09194 at ego_speed_scale 0.6, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_036)
- S16: 12a09194 at ego_speed_scale 0.6, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_030)
- S17: 12a09194 at ego_speed_scale 0.8, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_046)
- S18: 12a09194 at ego_speed_scale 0.8, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_020)
- S19: 12a09194 at ego_speed_scale 1.0, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_003)
- S20: 18d28973 at ego_speed_scale 0.6, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_044)
- S21: 18d28973 at ego_speed_scale 0.6, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_034)
- S22: 18d28973 at ego_speed_scale 0.8, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_040)
- S23: 18d28973 at ego_speed_scale 0.8, actor_time_shift_s 0.0: 0/2 failed, rate 0%-58% (90%) (pedestrian_ego_speed_2hz_rules_018, pedestrian_ego_speed_2hz_rules_028)
- S24: 18d28973 at ego_speed_scale 1.0, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_050)
- S25: 18d28973 at ego_speed_scale 1.0, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_009)
- S26: 18f8dbd6 at ego_speed_scale 0.6, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_047)
- S27: 18f8dbd6 at ego_speed_scale 0.8, actor_time_shift_s 0.0: 0/2 failed, rate 0%-58% (90%) (pedestrian_ego_speed_2hz_rules_039, pedestrian_ego_speed_2hz_rules_041)
- S28: 18f8dbd6 at ego_speed_scale 1.0, actor_time_shift_s 0.0: 0/4 failed, rate 0%-40% (90%) (pedestrian_ego_speed_2hz_rules_002, pedestrian_ego_speed_2hz_rules_017, pedestrian_ego_speed_2hz_rules_027, pedestrian_ego_speed_2hz_rules_033)
- S29: 1bbe02fc at ego_speed_scale 1.0, actor_time_shift_s 0.0: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_2hz_rules_010, pedestrian_ego_speed_2hz_rules_014, pedestrian_ego_speed_2hz_rules_024)

## Provenance

Plan: `plan.json` (rationale: Copied from studies/pedestrian_ego_speed/plan.json (10 Hz) with the policy planning every 500 ms, so the method comparison can be repeated at 2 Hz. Scenes: these are the 10 scenes tagged pedestrian_crossing that have a recorded pedestrian key actor. Each scene's pedestrian is set in retime_tracks, so actor_time_shift_s moves only that person. actor_speed_scale stays at 1.0, so the pedestrian walks at the recorded speed. Traffic is replay, which keeps the scenario scripted as in Euro NCAP pedestrian tests. There is no delay, bias or noise.

Two other tagged scenes are left out: 095cf563 and 13a9767e. Neither has a pedestrian key actor, so a person-class retime there might hit no actor or the wrong one.

Budget: 5 rounds of 10 runs gives 50 runs, as the brief asks. The goal is top_k with k=5, high_min=0.5 and distinct scenes. With 90% ranges, each confirmed case needs about 4–5 failures out of 5 repeats, so roughly 25 runs go to confirmation and about 25 to searching the 5×9 grid. That is tight, and with partial results the study may confirm fewer than 5 cases.

Caveats:
- 6 of the scenes (048b974e, 07981e6a, 0caa8f1a, 0d4893f5, 18d28973, 1bbe02fc) failed at 0 delay in an earlier CATK run. That run used reactive traffic, not replay, so it may not carry over. If one still fails at 1.0x / 0 s, its failures may not come from speed or timing, and it fills a top_k slot cheaply without answering the question.
- 0e002edd, 18f8dbd6, 12a09194 and 0b10bce8 are the cleaner tests. In 0b10bce8 the ego barely moved (8.9 m), and in 12a09194 the pedestrian stayed far away (11.5 m).
- The failure check counts any front or side collision or leaving the road. It cannot tell whether the ego hit the pedestrian or another actor. Near misses are reported as closest approach to any actor, not ranked as failures.
- With ego_speed_scale above 1, the first second or two of the warm-up starts off the recorded scene.). Report written by claude-opus-5-5 from `results` in 22 s; every count above is computed from the queue, not written by the model.

50 of 50 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
