# In pedestrian-crossing scenes, which combinations of ego speed at hand-off (0.6x–1.4x recorded) and pedestrian step-out time (±2 s) make the VaVAM policy with the linear MPC collide or leave the road? Find the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `hybrid`: 30 kept runs on 10 scenes, varying ego_speed_scale, actor_time_shift_s; 1 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 5 of 5 challenging settings confirmed, after 3 rounds.

## Answer

The study met its goal: five challenging settings were confirmed on five different scenes (S1, S2, S4, S11, S17). However, none of them answers the question about speed and timing. All five are at nominal settings (1.0x, 0 s), and none of their failures involve the pedestrian. In every case the policy steered left against a RIGHT or STRAIGHT route. It then hit oncoming or adjacent vehicles or parked cars, or drove onto a median. The few runs that changed ego speed or step-out time were on 0e002edd and 18f8dbd6, and none of them failed. These runs are hints, not rates: the 90% ranges at those settings still allow a high failure rate. So the study has not shown any speed and timing combination that makes the policy hit a pedestrian. Two cases have weaker evidence: S17's off-road flags may be a map-boundary artifact, and S1, S4 and S11 were all flagged as possible artifacts. Triage still puts the S1, S4 and S11 failures on the policy's own steering.

## Findings

- All five confirmed challenging settings are at nominal ego speed and pedestrian timing (1.0x, 0 s). They show the scene fails without any change to speed or timing, so they say nothing about how speed and step-out time combine.
  - S1: 048b974e at ego_speed_scale 1, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (pedestrian_ego_speed_hybrid_005, pedestrian_ego_speed_hybrid_021, pedestrian_ego_speed_hybrid_022)
  - S2: 07981e6a at ego_speed_scale 1, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_hybrid_006, pedestrian_ego_speed_hybrid_011, pedestrian_ego_speed_hybrid_012)
  - S4: 0caa8f1a at ego_speed_scale 1, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (pedestrian_ego_speed_hybrid_007, pedestrian_ego_speed_hybrid_023, pedestrian_ego_speed_hybrid_024)
  - S11: 18d28973 at ego_speed_scale 1, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (pedestrian_ego_speed_hybrid_009, pedestrian_ego_speed_hybrid_025, pedestrian_ego_speed_hybrid_026)
  - S17: 1bbe02fc at ego_speed_scale 1, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_hybrid_010, pedestrian_ego_speed_hybrid_015, pedestrian_ego_speed_hybrid_016)
- None of the confirmed failures involved the retimed pedestrian. Each came from the policy steering left against its route command. On 048b974e it turned into a side street and hit a van. On 0caa8f1a it crossed the centre line and hit oncoming vehicles head-on. On 07981e6a it drifted into parked cars. On 0d4893f5 it yawed into the car in the left lane. On 18d28973 it drove onto the palm-tree median.
  - S1: 048b974e at ego_speed_scale 1, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (pedestrian_ego_speed_hybrid_005, pedestrian_ego_speed_hybrid_021, pedestrian_ego_speed_hybrid_022)
  - S4: 0caa8f1a at ego_speed_scale 1, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (pedestrian_ego_speed_hybrid_007, pedestrian_ego_speed_hybrid_023, pedestrian_ego_speed_hybrid_024)
  - S2: 07981e6a at ego_speed_scale 1, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_hybrid_006, pedestrian_ego_speed_hybrid_011, pedestrian_ego_speed_hybrid_012)
  - S5: 0d4893f5 at ego_speed_scale 1, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_hybrid_008, pedestrian_ego_speed_hybrid_013, pedestrian_ego_speed_hybrid_014)
  - S11: 18d28973 at ego_speed_scale 1, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (pedestrian_ego_speed_hybrid_009, pedestrian_ego_speed_hybrid_025, pedestrian_ego_speed_hybrid_026)
- On 0d4893f5, every run at nominal settings failed by sideswiping car 33 in the left lane, with the policy at fault. This scene is just as confirmed as the goal's five, but the goal only took one setting per scene, and this setting is also nominal.
  - S5: 0d4893f5 at ego_speed_scale 1, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_hybrid_008, pedestrian_ego_speed_hybrid_013, pedestrian_ego_speed_hybrid_014)
- On 1bbe02fc, triage could not say the policy was at fault. Each failure is an off-road flag at the stop line with the ego only about half a metre from the recorded path. The policy's plan was wrong (it veered left instead of turning right), but the flag may come from a tight drivable-area boundary rather than a real departure from the road.
  - S17: 1bbe02fc at ego_speed_scale 1, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_hybrid_010, pedestrian_ego_speed_hybrid_015, pedestrian_ego_speed_hybrid_016)
- On 048b974e, 0caa8f1a and 18d28973, every failure is flagged as a possible artifact because the ego ended more than 3.5 m from the recorded trajectory. Triage reads that distance as the policy's own wrong turn, with a clean camera view before impact, so these look like real policy failures.
  - S1: 048b974e at ego_speed_scale 1, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (pedestrian_ego_speed_hybrid_005, pedestrian_ego_speed_hybrid_021, pedestrian_ego_speed_hybrid_022)
  - S4: 0caa8f1a at ego_speed_scale 1, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (pedestrian_ego_speed_hybrid_007, pedestrian_ego_speed_hybrid_023, pedestrian_ego_speed_hybrid_024)
  - S11: 18d28973 at ego_speed_scale 1, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (pedestrian_ego_speed_hybrid_009, pedestrian_ego_speed_hybrid_025, pedestrian_ego_speed_hybrid_026)
- On 0e002edd and 18f8dbd6, the runs that varied speed (1.2x) or step-out time (-1 s to +0.5 s) produced no failures. Each setting was run very few times, so a substantial failure rate there is not ruled out.
  - S6: 0e002edd at ego_speed_scale 1, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_hybrid_018)
  - S7: 0e002edd at ego_speed_scale 1, actor_time_shift_s 0: 0/2 failed, rate 0%-58% (90%) (pedestrian_ego_speed_hybrid_001, pedestrian_ego_speed_hybrid_027)
  - S8: 0e002edd at ego_speed_scale 1, actor_time_shift_s 0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_hybrid_028)
  - S9: 0e002edd at ego_speed_scale 1.2, actor_time_shift_s 0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_hybrid_017_a2)
  - S12: 18f8dbd6 at ego_speed_scale 1, actor_time_shift_s -1: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_hybrid_030)
  - S13: 18f8dbd6 at ego_speed_scale 1, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_hybrid_020)
  - S14: 18f8dbd6 at ego_speed_scale 1, actor_time_shift_s 0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_hybrid_002)
  - S15: 18f8dbd6 at ego_speed_scale 1.2, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_hybrid_029)
  - S16: 18f8dbd6 at ego_speed_scale 1.2, actor_time_shift_s 0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_hybrid_019)
- 0b10bce8 and 12a09194 did not fail at nominal settings, and neither was explored further. On 12a09194 the closest approach was never critical.
  - S3: 0b10bce8 at ego_speed_scale 1, actor_time_shift_s 0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_hybrid_004)
  - S10: 12a09194 at ego_speed_scale 1, actor_time_shift_s 0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_hybrid_003)

## Open

- Whether any combination of ego speed and step-out time makes the policy hit the pedestrian. The grid was barely searched: no setting went below 1.0x or above 1.2x, and no step-out shift went beyond ±1 s. Running the corners (0.6x and 1.4x combined with -2 s and +2 s) and the near-miss settings on 0e002edd and 18f8dbd6 (S8, S12–S16), with repeats, would settle it.
- 0b10bce8 and 12a09194 were only run at nominal settings. They need speed and timing sweeps before anyone can say they are robust.
- Whether 1bbe02fc truly fails (S17) or only trips a tight off-road boundary. Checking the drivable-area map at that stop line, or reading collision and off-road margins, would settle it.
- On the five scenes that fail at nominal settings, the wrong-way steering hides any pedestrian effect. To see one there, the route or command problem would have to be fixed first, or the scenes set aside. Otherwise extra runs on them cannot answer the question.
- Run 017 (0e002edd at 1.2x, 0 s) was not kept and was re-run as S9. Only the re-run counts as evidence.

## Why the runs failed (triage from the video and log)

turned_into_actor 9, left_road 7, no_brake_for_lead 1, other 1

- pedestrian_ego_speed_hybrid_005: turned_into_actor, policy at fault: yes. The route command was RIGHT, but the ego turned left at the intersection and left the recorded path (6.3 m off). It drove into the left-side street and hit the front of the oncoming van (actor 155) at about 3.9 m/s without braking. The camera view was clean before impact.
- pedestrian_ego_speed_hybrid_006: no_brake_for_lead, policy at fault: yes. On a narrow residential street, the ego kept about 11 m/s and its planned path ran along the left edge of its lane, so it never moved toward the right-turn route (the green line). It ran straight into parked car 6, which sat partly in its path. The gap closed from 37.6 m to 4.1 m with only light slowing (11.1 to 10.3 m/s), and the front collision happened at 7.5 s.
- pedestrian_ego_speed_hybrid_007: turned_into_actor, policy at fault: yes. The route command was RIGHT, but the ego drifted left, about 8 m away from the recorded path, and crossed the yellow centre line into the oncoming lanes while speeding up from 11 to 12.5 m/s. It then hit oncoming vehicle 86 (a white van) head-on: the gap closed at about 28 m/s, and the ego never braked or steered back.
- pedestrian_ego_speed_hybrid_008: turned_into_actor, policy at fault: yes. The ego was going straight at about 8 m/s and approaching an intersection. Its output trajectory (orange) kept bending left, and the ego yawed left out of its lane. Its front corner hit car 33, which was driving alongside in the adjacent left lane. The lead car was about 19 m ahead and was not involved.
- pedestrian_ego_speed_hybrid_009: left_road, policy at fault: yes. The command was RIGHT and the recorded path moved right toward the turn. Instead, the ego went the other way: its plan bent left across the lane markings, and the ego drifted onto the landscaped median with the palm trees on the left side of the road. It went off-road at 9.1 s, 6.3 m from the human trajectory. Before that, the camera view was clean and no actor was close (the lead car was more than 20 m ahead), so the policy's steering caused this.
- pedestrian_ego_speed_hybrid_010: left_road, policy at fault: unclear. The ego was approaching a signalized intersection at about 7 m/s in a lane whose route turns right. It was flagged offroad at the stop line while only about 0.6 m from the recorded human path. The command read STRAIGHT until the last frame, and the policy's plan went straight and then veered left across the intersection instead of following the right turn, but the actual deviation was so small that this may be a lane-edge or map-boundary edge case rather than a real departure from the road.
- pedestrian_ego_speed_hybrid_011: turned_into_actor, policy at fault: yes. The route said STRAIGHT and then RIGHT, and the human drove right toward the intersection. The ego instead drifted left at about 11 m/s, out of its lane and into the line of parked cars on the left side of the street. It never slowed meaningfully and drove front-first into parked car 6 (the gap shrank from 31 m to 4 m); the camera view was clean beforehand.
- pedestrian_ego_speed_hybrid_012: left_road, policy at fault: yes. On a straight residential street with cars parked along both curbs, the ego's own planned path (orange) took it left toward the parking lane, away from the recorded route (green), which bears right for the upcoming RIGHT turn. Over the last two seconds it barely slowed (11.0 to 10.1 m/s) as the gap shrank from 25.7 m to 4.1 m, and its front hit parked car 6 at the left curb.
- pedestrian_ego_speed_hybrid_013: turned_into_actor, policy at fault: yes. The ego was driving at a steady 8.2 m/s, and its planned path kept bending left toward the next lane. At 6.2 s it turned sharply left into that lane and hit actor 33 with its front corner. Actor 33 was driving next to it on the left, a little behind. The route command was STRAIGHT and changed to RIGHT, so turning left was the policy's own mistake. The lead vehicle stayed about 19 m ahead, so it played no part.
- pedestrian_ego_speed_hybrid_014: turned_into_actor, policy at fault: yes. The ego was driving straight at about 8.3 m/s on a clear multi-lane street, with car 33 alongside in the lane to its left. As it reached the intersection, the policy's planned path (orange) swung left away from the route (green), and the ego yawed left into car 33's lane, hitting it with its front-left corner.
- pedestrian_ego_speed_hybrid_015: left_road, policy at fault: unclear. The ego was approaching an intersection at about 7 m/s, and the route bends right (the command switches from STRAIGHT to RIGHT at 5.7 s). Its planned path instead swung left across the intersection, and the offroad flag tripped at the stop line. At that moment the ego was only about 0.5 m from where the human drove, so the flag may come from a tight drivable-area boundary rather than a real departure, even though the plan was clearly wrong.
- pedestrian_ego_speed_hybrid_016: left_road, policy at fault: unclear. The ego was approaching the intersection at about 7 m/s, close to the human trajectory, and was flagged offroad right at the stop line where its lane splits into a right-turn branch. It was only about 0.5 m off the recorded path. The command read STRAIGHT until the failure frame, when it switched to RIGHT. The ego's planned path (orange) heads straight and veers left across the intersection, away from the right-turn route, but the actual offroad call came from a slight drift at the lane edge, which looks marginal.
- pedestrian_ego_speed_hybrid_021: turned_into_actor, policy at fault: yes. The ego was in the intersection with a RIGHT command and the recorded path going straight, but it turned left into the side street, about 6 m off the recording. It drove front-first into a white van (actor 155) standing in that street at about 3.4 m/s and barely slowed.
- pedestrian_ego_speed_hybrid_022: turned_into_actor, policy at fault: yes. The route command was RIGHT and the recorded path went up and to the right, but the ego turned left at the intersection into a narrow street lined with parked cars. Partway through that left turn, at about 3.4 m/s, its front hit actor 155, which looks like a parked white van on the left side of the street.
- pedestrian_ego_speed_hybrid_023: other, policy at fault: yes. With a RIGHT command, the ego left the human's path (it was 8.8 m off by the end). It drifted left across the double yellow line and drove at about 10 m/s in the oncoming lane next to parked cars, then hit oncoming vehicle 85 head-on. The gap shrank much faster than the ego's own speed (38 m to 3 m in 1 s), so 85 was coming toward it, and the ego never braked or steered back.
- pedestrian_ego_speed_hybrid_024: turned_into_actor, policy at fault: yes. Although the route command was RIGHT, the ego steered left across the double-yellow centerline into the oncoming lanes and hit oncoming vehicle 85 head-on at about 10 m/s without braking. The gap to the actor closed far faster than the ego's own speed explains, so the actor was coming toward it, and the ego ended 8.6 m off the human trajectory.
- pedestrian_ego_speed_hybrid_025: left_road, policy at fault: yes. The command was RIGHT and the recorded human path moved right toward the right-turn lanes. The ego instead stayed in the leftmost lane at about 9–10 m/s and planned a path that curved left. At 9.1s it drifted over the left lane edge onto the landscaped median with the palm trees, about 6.3 m from the human path. The camera view was clean before the failure; the smearing only appears once the ego is on the median.
- pedestrian_ego_speed_hybrid_026: left_road, policy at fault: yes. The route command was RIGHT and the recorded path bore right, but the ego jogged left out of its lane at about 10 m/s and kept heading left onto the palm-tree median. By 8.9 s it was off the drivable area, about 6 m from the recorded trajectory, with front and side collision flags set at the moment it went off-road (it most likely hit median objects such as the trees), while the camera view was clean beforehand.

## Every setting

- S1: 048b974e at ego_speed_scale 1, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (pedestrian_ego_speed_hybrid_005, pedestrian_ego_speed_hybrid_021, pedestrian_ego_speed_hybrid_022)
- S2: 07981e6a at ego_speed_scale 1, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_hybrid_006, pedestrian_ego_speed_hybrid_011, pedestrian_ego_speed_hybrid_012)
- S3: 0b10bce8 at ego_speed_scale 1, actor_time_shift_s 0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_hybrid_004)
- S4: 0caa8f1a at ego_speed_scale 1, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (pedestrian_ego_speed_hybrid_007, pedestrian_ego_speed_hybrid_023, pedestrian_ego_speed_hybrid_024)
- S5: 0d4893f5 at ego_speed_scale 1, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_hybrid_008, pedestrian_ego_speed_hybrid_013, pedestrian_ego_speed_hybrid_014)
- S6: 0e002edd at ego_speed_scale 1, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_hybrid_018)
- S7: 0e002edd at ego_speed_scale 1, actor_time_shift_s 0: 0/2 failed, rate 0%-58% (90%) (pedestrian_ego_speed_hybrid_001, pedestrian_ego_speed_hybrid_027)
- S8: 0e002edd at ego_speed_scale 1, actor_time_shift_s 0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_hybrid_028)
- S9: 0e002edd at ego_speed_scale 1.2, actor_time_shift_s 0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_hybrid_017_a2)
- S10: 12a09194 at ego_speed_scale 1, actor_time_shift_s 0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_hybrid_003)
- S11: 18d28973 at ego_speed_scale 1, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (pedestrian_ego_speed_hybrid_009, pedestrian_ego_speed_hybrid_025, pedestrian_ego_speed_hybrid_026)
- S12: 18f8dbd6 at ego_speed_scale 1, actor_time_shift_s -1: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_hybrid_030)
- S13: 18f8dbd6 at ego_speed_scale 1, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_hybrid_020)
- S14: 18f8dbd6 at ego_speed_scale 1, actor_time_shift_s 0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_hybrid_002)
- S15: 18f8dbd6 at ego_speed_scale 1.2, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_hybrid_029)
- S16: 18f8dbd6 at ego_speed_scale 1.2, actor_time_shift_s 0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_hybrid_019)
- S17: 1bbe02fc at ego_speed_scale 1, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_hybrid_010, pedestrian_ego_speed_hybrid_015, pedestrian_ego_speed_hybrid_016)

## Not kept by the gate

- pedestrian_ego_speed_hybrid_017: not kept: RE-RUN

## Provenance

Plan: `plan.json` (rationale: Scenes: these are the 10 scenes tagged pedestrian_crossing that have a recorded pedestrian key actor. Each scene's pedestrian is set in retime_tracks, so actor_time_shift_s moves only that person. actor_speed_scale stays at 1.0, so the pedestrian walks at the recorded speed. Traffic is replay, which keeps the scenario scripted as in Euro NCAP pedestrian tests. There is no delay, bias or noise.

Two other tagged scenes are left out: 095cf563 and 13a9767e. Neither has a pedestrian key actor, so a person-class retime there might hit no actor or the wrong one.

Budget: 5 rounds of 10 runs gives 50 runs, as the brief asks. The goal is top_k with k=5, high_min=0.5 and distinct scenes. With 90% ranges, each confirmed case needs about 4–5 failures out of 5 repeats, so roughly 25 runs go to confirmation and about 25 to searching the 5×9 grid. That is tight, and with partial results the study may confirm fewer than 5 cases.

Caveats:
- 6 of the scenes (048b974e, 07981e6a, 0caa8f1a, 0d4893f5, 18d28973, 1bbe02fc) failed at 0 delay in an earlier CATK run. That run used reactive traffic, not replay, so it may not carry over. If one still fails at 1.0x / 0 s, its failures may not come from speed or timing, and it fills a top_k slot cheaply without answering the question.
- 0e002edd, 18f8dbd6, 12a09194 and 0b10bce8 are the cleaner tests. In 0b10bce8 the ego barely moved (8.9 m), and in 12a09194 the pedestrian stayed far away (11.5 m).
- The failure check counts any front or side collision or leaving the road. It cannot tell whether the ego hit the pedestrian or another actor. Near misses are reported as closest approach to any actor, not ranked as failures.
- With ego_speed_scale above 1, the first second or two of the warm-up starts off the recorded scene.). Report written by claude-opus-5-5 from `results` in 21 s; every count above is computed from the queue, not written by the model.

31 of 31 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
