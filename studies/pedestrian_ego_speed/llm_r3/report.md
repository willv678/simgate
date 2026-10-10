# In pedestrian-crossing scenes, which combinations of ego speed at hand-off (0.6x–1.4x recorded) and pedestrian step-out time (±2 s) make the VaVAM policy with the linear MPC collide or leave the road? Find the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `llm_r3`: 39 kept runs on 9 scenes, varying ego_speed_scale, actor_time_shift_s; 3 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 5 of 5 challenging settings confirmed, after 4 rounds.

## Answer

The goal was met after four rounds: five settings on five different scenes failed on every repeat, and all five 90% ranges sit just above 0.5 (S1, S4, S12, S14, S21). But these settings do not answer the question that was asked. None of the failures involved the pedestrian. Every confirmed case has the pedestrian at its recorded timing (0 s), and in every case the policy ignored a RIGHT route command: it drifted left into parked cars, oncoming traffic or a median, or turned too tightly into a parked car. At 1.2x ego speed the failure is confirmed on four scenes. On 18d28973 the ego fails even at nominal speed (S14), and the three failures on 1bbe02fc (S21) may be an off-road flag at the map edge rather than a real departure. So the study shows that higher hand-off speed is linked to route-following failures. It does not show any speed and step-out timing combination that makes the policy hit a pedestrian.

## Findings

- No failure in the study involved the retimed pedestrian. The triage traces every failure at the confirmed settings to the ego hitting a parked car, an oncoming or adjacent vehicle, or leaving the road.
  - S1: 048b974e at ego_speed_scale 1.2, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_llm_r3_026, pedestrian_ego_speed_llm_r3_033, pedestrian_ego_speed_llm_r3_034)
  - S4: 0caa8f1a at ego_speed_scale 1.2, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (pedestrian_ego_speed_llm_r3_030, pedestrian_ego_speed_llm_r3_039, pedestrian_ego_speed_llm_r3_040)
  - S12: 0e002edd at ego_speed_scale 1.4, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (pedestrian_ego_speed_llm_r3_014, pedestrian_ego_speed_llm_r3_022, pedestrian_ego_speed_llm_r3_021_a2)
  - S14: 18d28973 at ego_speed_scale 1, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (pedestrian_ego_speed_llm_r3_010, pedestrian_ego_speed_llm_r3_019, pedestrian_ego_speed_llm_r3_032)
  - S21: 1bbe02fc at ego_speed_scale 1.2, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_llm_r3_029, pedestrian_ego_speed_llm_r3_037, pedestrian_ego_speed_llm_r3_038)
  - S5: 0d4893f5 at ego_speed_scale 1.2, actor_time_shift_s -0.5: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_llm_r3_028, pedestrian_ego_speed_llm_r3_035, pedestrian_ego_speed_llm_r3_036)
  - S9: 0e002edd at ego_speed_scale 1.2, actor_time_shift_s 0: 2/4 failed, rate 18%-82% (90%), 1 possibly the simulator's (pedestrian_ego_speed_llm_r3_001, pedestrian_ego_speed_llm_r3_011, pedestrian_ego_speed_llm_r3_012, pedestrian_ego_speed_llm_r3_013_a2)
  - S10: 0e002edd at ego_speed_scale 1.2, actor_time_shift_s 0.5: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (pedestrian_ego_speed_llm_r3_015)
  - S11: 0e002edd at ego_speed_scale 1.4, actor_time_shift_s -0.5: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (pedestrian_ego_speed_llm_r3_020)
  - S15: 18d28973 at ego_speed_scale 1.2, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (pedestrian_ego_speed_llm_r3_018, pedestrian_ego_speed_llm_r3_023, pedestrian_ego_speed_llm_r3_031)
- The common cause is the policy not following a RIGHT route command. It drifts or steers left (onto a median, across the centre line into oncoming traffic, or toward the left curb), or it cuts the right turn too tightly into a parked car. The policy is at fault in these runs; the camera view was clean before the error.
  - S1: 048b974e at ego_speed_scale 1.2, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_llm_r3_026, pedestrian_ego_speed_llm_r3_033, pedestrian_ego_speed_llm_r3_034)
  - S4: 0caa8f1a at ego_speed_scale 1.2, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (pedestrian_ego_speed_llm_r3_030, pedestrian_ego_speed_llm_r3_039, pedestrian_ego_speed_llm_r3_040)
  - S12: 0e002edd at ego_speed_scale 1.4, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (pedestrian_ego_speed_llm_r3_014, pedestrian_ego_speed_llm_r3_022, pedestrian_ego_speed_llm_r3_021_a2)
  - S14: 18d28973 at ego_speed_scale 1, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (pedestrian_ego_speed_llm_r3_010, pedestrian_ego_speed_llm_r3_019, pedestrian_ego_speed_llm_r3_032)
  - S15: 18d28973 at ego_speed_scale 1.2, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (pedestrian_ego_speed_llm_r3_018, pedestrian_ego_speed_llm_r3_023, pedestrian_ego_speed_llm_r3_031)
- On 18d28973 the ego leaves the road onto the median on every run at the nominal setting (1.0x, 0 s), just as it does at 1.2x. This case fails regardless of speed or timing and fills a top-5 slot without answering the question.
  - S14: 18d28973 at ego_speed_scale 1, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (pedestrian_ego_speed_llm_r3_010, pedestrian_ego_speed_llm_r3_019, pedestrian_ego_speed_llm_r3_032)
  - S15: 18d28973 at ego_speed_scale 1.2, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (pedestrian_ego_speed_llm_r3_018, pedestrian_ego_speed_llm_r3_023, pedestrian_ego_speed_llm_r3_031)
- On 1bbe02fc at 1.2x, 0 s, every run was flagged off-road about one second after hand-off, only about 0.5 m from the recorded path. The triage cannot say whether the policy was at fault; the flag may come from the map edge at the stop line. Treat this case as unconfirmed as a policy failure.
  - S21: 1bbe02fc at ego_speed_scale 1.2, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_llm_r3_029, pedestrian_ego_speed_llm_r3_037, pedestrian_ego_speed_llm_r3_038)
- On 0caa8f1a at 1.2x, 0 s, the ego crosses the centre line and hits an oncoming vehicle head-on on every run. On 0e002edd at 1.4x, 0 s, it turns into parked car 90 on every run. These runs are flagged as possible artifacts only because the ego ended more than 3.5 m off the recorded path. The triage shows that this offset is the policy's own drift, not a rendering fault.
  - S4: 0caa8f1a at ego_speed_scale 1.2, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (pedestrian_ego_speed_llm_r3_030, pedestrian_ego_speed_llm_r3_039, pedestrian_ego_speed_llm_r3_040)
  - S12: 0e002edd at ego_speed_scale 1.4, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (pedestrian_ego_speed_llm_r3_014, pedestrian_ego_speed_llm_r3_022, pedestrian_ego_speed_llm_r3_021_a2)
- On 0e002edd, failures increase with ego speed. Single runs at 1.0x passed, 1.2x at 0 s was mixed, and 1.4x at 0 s failed on every repeat. Shifting the pedestrian by ±0.5 s did not clearly change the outcome. This is the clearest speed effect in the study, but the settings other than 1.4x, 0 s rest on one run each.
  - S6: 0e002edd at ego_speed_scale 1, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_llm_r3_002)
  - S7: 0e002edd at ego_speed_scale 1, actor_time_shift_s 0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_llm_r3_004)
  - S8: 0e002edd at ego_speed_scale 1.2, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_llm_r3_003)
  - S9: 0e002edd at ego_speed_scale 1.2, actor_time_shift_s 0: 2/4 failed, rate 18%-82% (90%), 1 possibly the simulator's (pedestrian_ego_speed_llm_r3_001, pedestrian_ego_speed_llm_r3_011, pedestrian_ego_speed_llm_r3_012, pedestrian_ego_speed_llm_r3_013_a2)
  - S10: 0e002edd at ego_speed_scale 1.2, actor_time_shift_s 0.5: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (pedestrian_ego_speed_llm_r3_015)
  - S11: 0e002edd at ego_speed_scale 1.4, actor_time_shift_s -0.5: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (pedestrian_ego_speed_llm_r3_020)
  - S12: 0e002edd at ego_speed_scale 1.4, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (pedestrian_ego_speed_llm_r3_014, pedestrian_ego_speed_llm_r3_022, pedestrian_ego_speed_llm_r3_021_a2)
- A sixth scene, 0d4893f5 at 1.2x with the pedestrian 0.5 s early, also failed on every repeat. In each run the ego sideswiped a vehicle in the adjacent left lane, not the pedestrian.
  - S5: 0d4893f5 at ego_speed_scale 1.2, actor_time_shift_s -0.5: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_llm_r3_028, pedestrian_ego_speed_llm_r3_035, pedestrian_ego_speed_llm_r3_036)
- Scenes 18f8dbd6, 0b10bce8 and 12a09194 did not fail at any setting tried, including 1.4x with the pedestrian up to 1 s early. Most of these settings have only one run, so this is a hint, not a low failure rate.
  - S2: 0b10bce8 at ego_speed_scale 1.4, actor_time_shift_s -1: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_llm_r3_008)
  - S3: 0b10bce8 at ego_speed_scale 1.4, actor_time_shift_s 0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_llm_r3_007)
  - S13: 12a09194 at ego_speed_scale 1.2, actor_time_shift_s -1: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_llm_r3_009)
  - S16: 18f8dbd6 at ego_speed_scale 1.2, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_llm_r3_006)
  - S17: 18f8dbd6 at ego_speed_scale 1.2, actor_time_shift_s 0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_llm_r3_005)
  - S18: 18f8dbd6 at ego_speed_scale 1.4, actor_time_shift_s -1: 0/2 failed, rate 0%-58% (90%) (pedestrian_ego_speed_llm_r3_017, pedestrian_ego_speed_llm_r3_024)
  - S19: 18f8dbd6 at ego_speed_scale 1.4, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_llm_r3_025)
  - S20: 18f8dbd6 at ego_speed_scale 1.4, actor_time_shift_s 0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_llm_r3_016)

## Open

- Whether pedestrian step-out timing matters at all. No pedestrian contact occurred, and the confirmed settings all use 0 s. Sweeping actor_time_shift_s from -2 s to +2 s at a fixed speed on the scenes where the pedestrian actually comes near the ego's path would settle this, starting with 0e002edd and 18f8dbd6, where near misses scored high.
- Whether speed causes the failures on 048b974e, 0caa8f1a, 0d4893f5 and 1bbe02fc. None of these scenes was run at the nominal 1.0x, 0 s setting. Three repeats at nominal on each would show whether they fail anyway, as 18d28973 does.
- Whether the off-road flags on 1bbe02fc (S21) are real departures or map-edge artifacts. This needs a look at the map boundary near the stop line, or a re-run with a tolerance on the off-road check.
- Whether the failure check can tell a pedestrian hit apart from other collisions. As it stands, the study counts any front or side contact or off-road event, so it cannot answer a question about pedestrians directly.
- Scene 07981e6a has no kept runs: its only run was halted, so nothing is known about it.
- Each confirmed case rests on three repeats, so its range only just clears 0.5. More repeats would tighten the ranges, and the 1.2x and 1.4x single-run settings on 0e002edd (S10, S11) need repeats too.

## Why the runs failed (triage from the video and log)

turned_into_actor 14, left_road 9, no_brake_for_lead 1, other 1

- pedestrian_ego_speed_llm_r3_001: turned_into_actor, policy at fault: yes. At an intersection with a RIGHT command, the ego crept forward at about 2 m/s. It drifted left of its planned right-turn path, ending about 3.2 m off the recorded trajectory. It drove into the path of actor 112, which was turning left across the intersection toward the ego's side. The ego slowed only slightly (2.4 to 1.7 m/s) as the gap closed from 26 m to 4.6 m, and hit 112 with its front.
- pedestrian_ego_speed_llm_r3_010: left_road, policy at fault: yes. The command was RIGHT and the recorded path curved right toward the turn. Instead, the ego kept drifting left across lanes at about 9–10 m/s, then ran over the left lane edge onto the grass median near the intersection at 9.0 s, about 6.2 m from the recorded path. The camera view was clean before the failure, so the policy's steering caused this.
- pedestrian_ego_speed_llm_r3_011: turned_into_actor, policy at fault: yes. The route said turn right, but the ego crept into the intersection at about 2.6 m/s and steered left of its route, ending about 4 m off the recorded path. Oncoming car 112 was turning left across the intersection in plain view, and the ego hit it head-on with its front without yielding or braking in time.
- pedestrian_ego_speed_llm_r3_014: turned_into_actor, policy at fault: yes. On the RIGHT command, the ego turned right at the intersection much more sharply than the recorded human path. It cut toward the curb and drove front-first into parked car 90 at about 4 m/s, ending 7 m off the recorded path.
- pedestrian_ego_speed_llm_r3_015: turned_into_actor, policy at fault: yes. On a RIGHT command at an urban intersection, the ego crept through the turn at about 3 m/s. Its planned path (orange) hooked toward the curb lane of parked cars, and it drove its front into parked car 90 (dark sedan, close on the left of the camera at 9.6s), ending 5.3 m off the human trajectory and partly off the drivable area.
- pedestrian_ego_speed_llm_r3_018: left_road, policy at fault: yes. The command was RIGHT and the route bent right toward the intersection, but the policy kept planning a path that veered left. The ego drifted left out of its lane at about 9–10 m/s and ran onto the planted median with palm trees, ending 6.1 m from the recorded trajectory. The camera view was clean before the drift, so a rendering problem does not explain the mistake.
- pedestrian_ego_speed_llm_r3_019: left_road, policy at fault: yes. The route command was RIGHT, but the ego stayed in the leftmost lane at about 10 m/s while the recorded path moved right. Its plan then curved left, and the ego drove onto the landscaped median with palm trees at 8.9 s, about 6 m off the recorded trajectory.
- pedestrian_ego_speed_llm_r3_020: turned_into_actor, policy at fault: yes. With a RIGHT command at the intersection, the ego turned right far too tightly and early instead of following the recorded path, which kept going farther through the intersection before turning. It cut into the curbside parking lane and drove its front at about 4 m/s into parked car 90 near the corner, about 7 m off the recorded path. The camera view was clean before the turn and only smeared at impact.
- pedestrian_ego_speed_llm_r3_022: turned_into_actor, policy at fault: yes. The ego was told to turn RIGHT at the intersection. Instead of following the recorded turn, it took a wider path at about 4 m/s and ended up pointing straight across the street, about 6.7 m off the recorded path, where its front hit parked car 90 at the curb. A rear contact was also logged, but the front collision came first.
- pedestrian_ego_speed_llm_r3_023: left_road, policy at fault: yes. The route command was RIGHT and the recorded path moved right, but the ego's plan kept bending left out of its lane. At about 10 m/s it drove onto the left median with the palm trees, about 6.3 m from the recorded path. No other actor was involved, and the camera view was clean until the ego was already on the median.
- pedestrian_ego_speed_llm_r3_026: turned_into_actor, policy at fault: yes. The ego was finishing a right turn at about 4 m/s into a narrow street lined with parked cars. Instead of following the recorded path toward the middle or right of the street, it kept to the left and its front hit parked car 68 at the corner of the street entrance, about 1.5 m off the recorded path.
- pedestrian_ego_speed_llm_r3_028: turned_into_actor, policy at fault: yes. After the policy took over at 4.7 s, the ego kept going at about 9.5 m/s and its planned path bent left, away from the recorded path (about 1.2 m off by the end). Its front-left corner hit actor 33, which was moving alongside in the left lane, at 6.4 s, while the lead vehicle was still about 17 m ahead.
- pedestrian_ego_speed_llm_r3_029: left_road, policy at fault: unclear. One second after the policy took over, the ego was flagged offroad at the stop line of a large intersection at about 8.9 m/s. The route turns right here, but the policy's plan went straight and then veered left, and the command showed STRAIGHT until the failure frame. Even so, the ego was only 0.5 m from the human's recorded path when flagged, so the offroad call may come from the map edge at the intersection entrance rather than a real departure.
- pedestrian_ego_speed_llm_r3_030: turned_into_actor, policy at fault: yes. Despite a RIGHT command, the ego steered left across the yellow centre line. It drove at about 11.5 m/s in the oncoming lane, about 10 m off the recorded path, and hit oncoming van 86 head-on without braking.
- pedestrian_ego_speed_llm_r3_021_a2: turned_into_actor, policy at fault: yes. While turning right at the intersection at about 4 m/s, the ego cut the corner far tighter than the recorded human path (6.9 m off it at failure). Its front hit car 90, which was parked along the curb of the street it was turning into.
- pedestrian_ego_speed_llm_r3_031: left_road, policy at fault: yes. The route command was RIGHT and the recorded path bore right, but after handoff the ego steered left out of its lane. It slowed from 12 to 9.5 m/s and drove onto the planted median by the trees at 8.7 s, about 6.3 m from the recorded path. No contact with any actor appears in the frames; the camera view was clean before the drift.
- pedestrian_ego_speed_llm_r3_032: left_road, policy at fault: yes. The route command was RIGHT, but after handoff the ego stayed in the far-left lanes, 1–6 m left of the recorded path, and kept steering left. It drove at about 10 m/s onto the grass median with the palm trees by 9.1 s, which is where it was flagged off-road. The metrics table shows no actual collision (collision_any is 0), so the failure is the off-road event, and the camera view stayed clean until the ego reached the median.
- pedestrian_ego_speed_llm_r3_033: no_brake_for_lead, policy at fault: yes. The route command was RIGHT, but the ego went straight north through the intersection and held its line toward the left curb, at about 4 m/s. Parked car 68 sat in that path, and the ego never braked as the gap closed from 10 m to 4 m, so its front hit the parked car. The rear contact came only after this.
- pedestrian_ego_speed_llm_r3_034: other, policy at fault: yes. After crossing the intersection at a steady ~3.8 m/s, the ego drifted about 1.8 m left of the human path toward the left curb. It ran its front into parked car 68 (the dark Audi) without braking or steering away, while the gap closed from 22 m to 4 m. This was a lateral drift into a parked roadside car, not a lead vehicle in its lane, a turn, or leaving the road; the rear contact came later.
- pedestrian_ego_speed_llm_r3_035: turned_into_actor, policy at fault: yes. The policy took over at 4.7 s while going straight at about 9.8 m/s. It then planned a path drifting left toward the adjacent lane and steered into actor 33, which was driving alongside on its left. This was a side collision at 6.4 s, while the recorded human path kept the ego in its lane.
- pedestrian_ego_speed_llm_r3_036: turned_into_actor, policy at fault: yes. After the 4.7s handoff the policy steered left toward the adjacent left lane while holding about 9.5 m/s, approaching an intersection where the route turns RIGHT. It sideswiped actor 33, which was driving alongside in that lane, at 6.3s (lateral collision). The lead car stayed about 17 m ahead, so the collision did not involve it.
- pedestrian_ego_speed_llm_r3_037: left_road, policy at fault: unclear. One second after handoff, the ego was flagged offroad at the stop line, just where the right curb starts to curve. It was going about 9 m/s straight down its lane, with no actor close by and only 0.5 m from the human's recorded path. The policy's planned path points straight or slightly left, even though the command had just switched to RIGHT, so this looks more like a small edge-of-lane or map-boundary clip than a clear steering mistake.
- pedestrian_ego_speed_llm_r3_038: left_road, policy at fault: unclear. The ego was slowly approaching an intersection at about 9 m/s. One second after handoff it was flagged offroad at the stop line, only 0.5 m from the recorded human path; it most likely clipped the right road edge where the right-turn lane starts. Its plan pointed straight or slightly left even though the route turns right, and the command only changed from STRAIGHT to RIGHT in the failure frame.
- pedestrian_ego_speed_llm_r3_039: turned_into_actor, policy at fault: yes. Even though the route command was RIGHT, the ego drifted left across the double-yellow centerline into the oncoming lanes, ending up 8.2 m off the recorded path. It held about 10.9 m/s and hit oncoming vehicle 85 head-on without braking.
- pedestrian_ego_speed_llm_r3_040: turned_into_actor, policy at fault: yes. Although the route command was RIGHT, the ego drifted left across the double yellow centre line into the oncoming lanes and kept going at about 11 m/s. It hit the front of oncoming vehicle 85, which was stopped or nearly stopped in its own lane with its headlights facing the ego, braking only slightly before impact.

## Every setting

- S1: 048b974e at ego_speed_scale 1.2, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_llm_r3_026, pedestrian_ego_speed_llm_r3_033, pedestrian_ego_speed_llm_r3_034)
- S2: 0b10bce8 at ego_speed_scale 1.4, actor_time_shift_s -1: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_llm_r3_008)
- S3: 0b10bce8 at ego_speed_scale 1.4, actor_time_shift_s 0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_llm_r3_007)
- S4: 0caa8f1a at ego_speed_scale 1.2, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (pedestrian_ego_speed_llm_r3_030, pedestrian_ego_speed_llm_r3_039, pedestrian_ego_speed_llm_r3_040)
- S5: 0d4893f5 at ego_speed_scale 1.2, actor_time_shift_s -0.5: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_llm_r3_028, pedestrian_ego_speed_llm_r3_035, pedestrian_ego_speed_llm_r3_036)
- S6: 0e002edd at ego_speed_scale 1, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_llm_r3_002)
- S7: 0e002edd at ego_speed_scale 1, actor_time_shift_s 0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_llm_r3_004)
- S8: 0e002edd at ego_speed_scale 1.2, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_llm_r3_003)
- S9: 0e002edd at ego_speed_scale 1.2, actor_time_shift_s 0: 2/4 failed, rate 18%-82% (90%), 1 possibly the simulator's (pedestrian_ego_speed_llm_r3_001, pedestrian_ego_speed_llm_r3_011, pedestrian_ego_speed_llm_r3_012, pedestrian_ego_speed_llm_r3_013_a2)
- S10: 0e002edd at ego_speed_scale 1.2, actor_time_shift_s 0.5: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (pedestrian_ego_speed_llm_r3_015)
- S11: 0e002edd at ego_speed_scale 1.4, actor_time_shift_s -0.5: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (pedestrian_ego_speed_llm_r3_020)
- S12: 0e002edd at ego_speed_scale 1.4, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (pedestrian_ego_speed_llm_r3_014, pedestrian_ego_speed_llm_r3_022, pedestrian_ego_speed_llm_r3_021_a2)
- S13: 12a09194 at ego_speed_scale 1.2, actor_time_shift_s -1: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_llm_r3_009)
- S14: 18d28973 at ego_speed_scale 1, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (pedestrian_ego_speed_llm_r3_010, pedestrian_ego_speed_llm_r3_019, pedestrian_ego_speed_llm_r3_032)
- S15: 18d28973 at ego_speed_scale 1.2, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (pedestrian_ego_speed_llm_r3_018, pedestrian_ego_speed_llm_r3_023, pedestrian_ego_speed_llm_r3_031)
- S16: 18f8dbd6 at ego_speed_scale 1.2, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_llm_r3_006)
- S17: 18f8dbd6 at ego_speed_scale 1.2, actor_time_shift_s 0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_llm_r3_005)
- S18: 18f8dbd6 at ego_speed_scale 1.4, actor_time_shift_s -1: 0/2 failed, rate 0%-58% (90%) (pedestrian_ego_speed_llm_r3_017, pedestrian_ego_speed_llm_r3_024)
- S19: 18f8dbd6 at ego_speed_scale 1.4, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_llm_r3_025)
- S20: 18f8dbd6 at ego_speed_scale 1.4, actor_time_shift_s 0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_llm_r3_016)
- S21: 1bbe02fc at ego_speed_scale 1.2, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_llm_r3_029, pedestrian_ego_speed_llm_r3_037, pedestrian_ego_speed_llm_r3_038)

## Not kept by the gate

- pedestrian_ego_speed_llm_r3_013: not kept: RE-RUN
- pedestrian_ego_speed_llm_r3_021: not kept: RE-RUN
- pedestrian_ego_speed_llm_r3_027: not kept: HALT

## Provenance

Plan: `plan.json` (rationale: Scenes: these are the 10 scenes tagged pedestrian_crossing that have a recorded pedestrian key actor. Each scene's pedestrian is set in retime_tracks, so actor_time_shift_s moves only that person. actor_speed_scale stays at 1.0, so the pedestrian walks at the recorded speed. Traffic is replay, which keeps the scenario scripted as in Euro NCAP pedestrian tests. There is no delay, bias or noise.

Two other tagged scenes are left out: 095cf563 and 13a9767e. Neither has a pedestrian key actor, so a person-class retime there might hit no actor or the wrong one.

Budget: 5 rounds of 10 runs gives 50 runs, as the brief asks. The goal is top_k with k=5, high_min=0.5 and distinct scenes. With 90% ranges, each confirmed case needs about 4–5 failures out of 5 repeats, so roughly 25 runs go to confirmation and about 25 to searching the 5×9 grid. That is tight, and with partial results the study may confirm fewer than 5 cases.

Caveats:
- 6 of the scenes (048b974e, 07981e6a, 0caa8f1a, 0d4893f5, 18d28973, 1bbe02fc) failed at 0 delay in an earlier CATK run. That run used reactive traffic, not replay, so it may not carry over. If one still fails at 1.0x / 0 s, its failures may not come from speed or timing, and it fills a top_k slot cheaply without answering the question.
- 0e002edd, 18f8dbd6, 12a09194 and 0b10bce8 are the cleaner tests. In 0b10bce8 the ego barely moved (8.9 m), and in 12a09194 the pedestrian stayed far away (11.5 m).
- The failure check counts any front or side collision or leaving the road. It cannot tell whether the ego hit the pedestrian or another actor. Near misses are reported as closest approach to any actor, not ranked as failures.
- With ego_speed_scale above 1, the first second or two of the warm-up starts off the recorded scene.). Report written by claude-opus-5-5 from `results` in 24 s; every count above is computed from the queue, not written by the model.

42 of 42 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
