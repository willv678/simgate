# In merge and cut-in scenes, which timings and speeds of the other cars make the VaVAM policy collide or leave the road? Find the 5 most challenging settings, each on a different scene and confirmed by repeats.

Study `hybrid_r3`: 54 kept runs on 9 scenes, varying actor_time_shift_s, actor_speed_scale; 1 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 3 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The goal was not met: only 3 of the 5 challenging settings were confirmed, and all three are at the recorded timing (0 s shift) with the cars sped up. They are 023b7fcc at 1.25x speed, 09a95ffa at 1.5x and 096988dd at 2x. Every repeat at each of these settings failed. Each still has only a few runs, so its 90% range only just clears one half. In the first two, the policy itself was at fault: it drifted left out of its lane, even at 2 Hz planning. In 023b7fcc it hit a car driving alongside, and in 09a95ffa it closed on a slow car ahead without braking. The 096988dd case is weak evidence. Car 9 already overlaps the ego at handoff and looks like a smeared ghost on camera, which points to a bad replayed track rather than the policy, even though no run was flagged as a possible artifact. The other six scenes never failed at any setting tried. Most of those settings had one or two runs, so this is a hint that they are safe, not a measured rate.

## Findings

- On 023b7fcc, speeding the cars to 1.25x at the recorded timing made every run fail. Each time the policy sped up, drifted left out of its lane against a straight route, and hit the car driving alongside in the left lane. The policy was at fault in every run.
  - S1: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_2hz_hybrid_r3_004, cut_in_merge_2hz_hybrid_r3_010, cut_in_merge_2hz_hybrid_r3_011)
- On 09a95ffa at 1.5x speed and recorded timing, every run failed. The ego drifted about one lane left of the recorded path and held about 6 m/s into slow car 87 ahead without braking. The policy was at fault each time, and the camera still showed car 87 clearly.
  - S9: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.5: 4/4 failed, rate 60%-100% (90%) (cut_in_merge_2hz_hybrid_r3_021, cut_in_merge_2hz_hybrid_r3_028, cut_in_merge_2hz_hybrid_r3_029, cut_in_merge_2hz_hybrid_r3_030)
- On 09a95ffa at 1.25x, failures were mixed. One was a policy left drift into an adjacent car. Another was car 33 cutting into the ego's lane and hitting it, which was not the policy's fault. This setting is not a reliable failure.
  - S8: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25: 2/5 failed, rate 14%-73% (90%) (cut_in_merge_2hz_hybrid_r3_007, cut_in_merge_2hz_hybrid_r3_012, cut_in_merge_2hz_hybrid_r3_013, cut_in_merge_2hz_hybrid_r3_019, cut_in_merge_2hz_hybrid_r3_020)
- On 096988dd, every run at 2x failed, but the confirmation is doubtful. Car 9 already overlaps the ego at handoff and shows up on camera as a smeared, see-through ghost. Two of the three failures were judged not clearly the policy's fault, which points to a bad replayed track. At 1.25x and 1.5x the scene did not fail.
  - S7: 096988dd at actor_time_shift_s 0, actor_speed_scale 2: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_2hz_hybrid_r3_052, cut_in_merge_2hz_hybrid_r3_053, cut_in_merge_2hz_hybrid_r3_054)
  - S5: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r3_005)
  - S6: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r3_042)
- No setting tried failed on 054b5901, 0cf6368d, 0e899dd3, 12855a41, 19f339ba or 1c45ce3a. That covers speeds 1.25x to 2x and time shifts from -0.5 s to +1 s. Most of these settings ran only once or twice, so they are hints, not rates.
  - S2: 054b5901 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r3_008)
  - S3: 054b5901 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r3_044)
  - S4: 054b5901 at actor_time_shift_s 0, actor_speed_scale 2: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_r3_049, cut_in_merge_2hz_hybrid_r3_050, cut_in_merge_2hz_hybrid_r3_051)
  - S10: 0cf6368d at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r3_036)
  - S11: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r3_001)
  - S12: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r3_027)
  - S13: 0cf6368d at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r3_045)
  - S14: 0e899dd3 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r3_026)
  - S15: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r3_009)
  - S16: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r3_018)
  - S17: 0e899dd3 at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r3_035)
  - S18: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r3_025)
  - S19: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_hybrid_r3_002, cut_in_merge_2hz_hybrid_r3_016)
  - S20: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_hybrid_r3_017, cut_in_merge_2hz_hybrid_r3_041)
  - S21: 12855a41 at actor_time_shift_s 0, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r3_024)
  - S22: 12855a41 at actor_time_shift_s 0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r3_034)
  - S23: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r3_032)
  - S24: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_hybrid_r3_006, cut_in_merge_2hz_hybrid_r3_014)
  - S25: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.5: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_r3_015, cut_in_merge_2hz_hybrid_r3_022, cut_in_merge_2hz_hybrid_r3_031)
  - S26: 19f339ba at actor_time_shift_s 0, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r3_023)
  - S27: 19f339ba at actor_time_shift_s 0.5, actor_speed_scale 1.5: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_r3_033, cut_in_merge_2hz_hybrid_r3_037, cut_in_merge_2hz_hybrid_r3_038)
  - S28: 19f339ba at actor_time_shift_s 0.5, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r3_040)
  - S29: 19f339ba at actor_time_shift_s 1, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r3_039)
  - S30: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r3_003_a2)
  - S31: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r3_043)
  - S32: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 2: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_r3_046, cut_in_merge_2hz_hybrid_r3_047, cut_in_merge_2hz_hybrid_r3_048)
- The closest calls without a failure were 19f339ba at 0 s/1.25x and +0.5 s/1.5x, 1c45ce3a at 1.5x, 054b5901 at 1.5x and 12855a41 at 1.5x. These are the best places to look for the two missing cases.
  - S24: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_hybrid_r3_006, cut_in_merge_2hz_hybrid_r3_014)
  - S27: 19f339ba at actor_time_shift_s 0.5, actor_speed_scale 1.5: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_r3_033, cut_in_merge_2hz_hybrid_r3_037, cut_in_merge_2hz_hybrid_r3_038)
  - S31: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r3_043)
  - S3: 054b5901 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r3_044)
  - S20: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_hybrid_r3_017, cut_in_merge_2hz_hybrid_r3_041)

## Open

- Two of the five cases are still missing. The near-miss settings ran only once: 1c45ce3a at 1.5x (S31) and 054b5901 at 1.5x (S3). Repeating them, and trying nearby speeds such as 1.75x, could find failures.
- Most of the timing range was never tried: there were no shifts beyond -0.5 s or +1 s, and nothing near ±2 s or at 0.5x speed. Shifting timing at a fixed speed on 19f339ba, 12855a41 and 0cf6368d would show whether timing matters at all.
- Is the 096988dd 2x case (S7) real? The run videos and the replayed track of car 9 need checking, or the setting should be rerun after fixing the track. Until then, treat it as possibly the simulator's.
- The three confirmed settings each have only a few runs, so their ranges only just clear one half. More repeats of S1, S9 and S7 would tighten them.
- Comparing with the 10 Hz study cut_in_merge needs its report side by side. Here, the two policy-caused cases are both left drifts, so this study does not show that the slower 2 Hz planning prevents those failures.
- Run cut_in_merge_2hz_hybrid_r3_003 (1c45ce3a, 1.25x) was not kept and was rerun, so it is not evidence.

## Why the runs failed (triage from the video and log)

no_brake_for_lead 6, turned_into_actor 4, actor_hit_ego 1, other 1

- cut_in_merge_2hz_hybrid_r3_004: turned_into_actor, policy at fault: yes. The route said to go straight, and the human drove straight on (green line). The policy's planned path (orange) instead bent left into the next lane while speeding up from 4.4 to 6.6 m/s. The ego's front cut into car 56, which was driving alongside in that left lane, by 7.2 s. The camera view was clean until the moment of impact, and the rear contact came only after this front collision.
- cut_in_merge_2hz_hybrid_r3_007: turned_into_actor, policy at fault: yes. On a multi-lane freeway at about 8 m/s, with plenty of room to the car ahead (~26 m), the policy planned a drift to the left toward the next lane. Its front-left corner then hit actor 33, which was coming up alongside in that left lane. At impact the ego was angled left and about 0.9 m left of the human's path.
- cut_in_merge_2hz_hybrid_r3_010: turned_into_actor, policy at fault: yes. After handoff the ego sped up from 4.4 to 6.7 m/s and drifted left out of its lane toward the lane where actor 15 was, while the recorded path went straight and then bore right. Its front hit actor 56, which was driving next to it in the left lane, about 1.5 m off the recorded path.
- cut_in_merge_2hz_hybrid_r3_011: turned_into_actor, policy at fault: yes. Driving straight in heavy freeway traffic after handoff, the ego sped up from 4.4 to 6.4 m/s and drifted left, about 1.5 m off the recorded path, into the adjacent lane. Its front-left corner hit actor 56, which was alongside and slightly ahead in that lane. A rear contact was also logged, but the front/side collision started first.
- cut_in_merge_2hz_hybrid_r3_020: actor_hit_ego, policy at fault: no. The ego was holding its lane on the freeway at about 8 m/s, staying within 0.9 m of the recorded human path. Actor 33 came up from behind in the lane to the left, passed the ego and moved right into the ego's lane just ahead of it, so its rear-right corner hit the ego's front-left corner, which is why the contact is scored as a front collision.
- cut_in_merge_2hz_hybrid_r3_021: no_brake_for_lead, policy at fault: yes. On a multi-lane highway, the ego drifted about 3 m left of the recorded path, ending up straddling the lane line behind actor 87, which was nearly stopped. The ego held about 6 m/s while the gap closed from 14 m to 2.4 m, and its front hit 87's rear-right corner. (An earlier rear contact by another actor also happened, but the at-fault failure is this front collision.)
- cut_in_merge_2hz_hybrid_r3_028: no_brake_for_lead, policy at fault: yes. The ego stayed about one lane left of the recorded path, which shifted right, and held about 6 m/s while closing on slower actor 87 ahead in that lane. The gap shrank from 14.4 m to 2.2 m with almost no braking, and the ego's front ran into 87. The ego was rear-ended earlier, but that played no part in this front collision.
- cut_in_merge_2hz_hybrid_r3_029: no_brake_for_lead, policy at fault: yes. The ego drove about one lane left of the recorded path and held about 6 m/s while closing on slower actor 87 ahead in its lane, with the gap shrinking from 14.5 m to 2.4 m. It never braked and hit 87 with its front at 10.6 s. The earlier rear contact came before this, and 87 looks smeared in the camera but is still clearly visible.
- cut_in_merge_2hz_hybrid_r3_030: no_brake_for_lead, policy at fault: yes. The ego had drifted about 3 m left of the recorded path, into the lane to its left, even though the command was RIGHT. It then held about 6.5 m/s while the gap to the slower actor 87 ahead in that lane shrank from 16.5 m to 3.7 m, and it hit 87's rear with its front without braking. Nearby cars in the camera view were smeared, but 87 could still be seen as a vehicle, so this does not explain the failure to brake.
- cut_in_merge_2hz_hybrid_r3_052: no_brake_for_lead, policy at fault: yes. Lead vehicle 9 appeared right in front of the ego around handoff (gap fell from 43.6 m to 0.5 m, overlapping at 5.2 s). After separating to about 8 m at 6.2 s, the nearly stopped vehicle 9 was closing fast, but the ego only eased from 5.4 to 4.5 m/s and drove into its rear at 7.2 s.
- cut_in_merge_2hz_hybrid_r3_053: no_brake_for_lead, policy at fault: unclear. Actor 9 was already overlapping the ego's front in the ego's lane right at handoff (gap 0.5 m at 4.7 s; front contact in the 5.2 s frame), so the run started in a bad state. The gap then opened to about 8 m, but the ego held about 5.5 m/s and slowed only to 4.3 m/s, closed back in on the slower car and hit it again at 7.2 s. At that moment the ego was only 0.1 m from the recorded human path and the camera shows actor 9 as a smeared blob. Both suggest actor 9's reconstructed track may not match the real drive.
- cut_in_merge_2hz_hybrid_r3_054: other, policy at fault: unclear. At handoff (4.7 s), actor 9 was already sitting on top of the ego: the gap was 0.5 m, and the 5.2 s frame shows the boxes overlapping. Actor 9 then pulled about 8 m ahead and stopped abruptly, and the ego, braking only mildly (5.5 to 4.3 m/s), ran back into it at 7.2 s. The ego was only about 0.2 to 0.9 m from the human's recorded path, so the human car would also have overlapped actor 9. In the camera, actor 9 looks like a see-through smeared ghost, which suggests a bad replayed track rather than a real lead vehicle.

## Every setting

- S1: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_2hz_hybrid_r3_004, cut_in_merge_2hz_hybrid_r3_010, cut_in_merge_2hz_hybrid_r3_011)
- S2: 054b5901 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r3_008)
- S3: 054b5901 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r3_044)
- S4: 054b5901 at actor_time_shift_s 0, actor_speed_scale 2: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_r3_049, cut_in_merge_2hz_hybrid_r3_050, cut_in_merge_2hz_hybrid_r3_051)
- S5: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r3_005)
- S6: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r3_042)
- S7: 096988dd at actor_time_shift_s 0, actor_speed_scale 2: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_2hz_hybrid_r3_052, cut_in_merge_2hz_hybrid_r3_053, cut_in_merge_2hz_hybrid_r3_054)
- S8: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25: 2/5 failed, rate 14%-73% (90%) (cut_in_merge_2hz_hybrid_r3_007, cut_in_merge_2hz_hybrid_r3_012, cut_in_merge_2hz_hybrid_r3_013, cut_in_merge_2hz_hybrid_r3_019, cut_in_merge_2hz_hybrid_r3_020)
- S9: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.5: 4/4 failed, rate 60%-100% (90%) (cut_in_merge_2hz_hybrid_r3_021, cut_in_merge_2hz_hybrid_r3_028, cut_in_merge_2hz_hybrid_r3_029, cut_in_merge_2hz_hybrid_r3_030)
- S10: 0cf6368d at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r3_036)
- S11: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r3_001)
- S12: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r3_027)
- S13: 0cf6368d at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r3_045)
- S14: 0e899dd3 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r3_026)
- S15: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r3_009)
- S16: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r3_018)
- S17: 0e899dd3 at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r3_035)
- S18: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r3_025)
- S19: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_hybrid_r3_002, cut_in_merge_2hz_hybrid_r3_016)
- S20: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_hybrid_r3_017, cut_in_merge_2hz_hybrid_r3_041)
- S21: 12855a41 at actor_time_shift_s 0, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r3_024)
- S22: 12855a41 at actor_time_shift_s 0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r3_034)
- S23: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r3_032)
- S24: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_hybrid_r3_006, cut_in_merge_2hz_hybrid_r3_014)
- S25: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.5: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_r3_015, cut_in_merge_2hz_hybrid_r3_022, cut_in_merge_2hz_hybrid_r3_031)
- S26: 19f339ba at actor_time_shift_s 0, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r3_023)
- S27: 19f339ba at actor_time_shift_s 0.5, actor_speed_scale 1.5: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_r3_033, cut_in_merge_2hz_hybrid_r3_037, cut_in_merge_2hz_hybrid_r3_038)
- S28: 19f339ba at actor_time_shift_s 0.5, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r3_040)
- S29: 19f339ba at actor_time_shift_s 1, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r3_039)
- S30: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r3_003_a2)
- S31: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_hybrid_r3_043)
- S32: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 2: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_2hz_hybrid_r3_046, cut_in_merge_2hz_hybrid_r3_047, cut_in_merge_2hz_hybrid_r3_048)

## Not kept by the gate

- cut_in_merge_2hz_hybrid_r3_003: not kept: RE-RUN

## Provenance

Plan: `plan.json` (rationale: Copied from studies/cut_in_merge/plan.json (10 Hz) with the policy planning every 500 ms, so the method comparison can be repeated at 2 Hz. Scope and settings follow the brief. Traffic is replayed as recorded. Only recorded cars (class automobile) are retimed, using the knobs' full ranges: -2 s to +2 s and 0.5x to 2x speed.

Scene choice: 31 scenes carry the merge_cut_in tag. I kept 9 that passed at 0 delay and have a car identified as a key actor. Scenes that already fail with the recorded timing would fill the top 5 without showing what the retiming does, so I left them out. Three scenes have a car marked as cutting in (0cf6368d track 21, 12855a41 track 31, 1c45ce3a track 14). In those, only that car is retimed. The other six retime every car in the scene: with only a lead or crossing car identified, retiming that car alone could miss the car that actually changes lanes. Several picks already came close at baseline (023b7fcc and 096988dd at 0.0 m, 19f339ba at 0.03 m, 12855a41 at 0.08 m, 054b5901 at 0.26 m), so they are good places to look first.

Budget and stopping rule: 6 rounds of 9 runs gives 54 runs, close to the brief's ~50 and under the cap of 60. The goal is top_k with k=5, one case per scene, failure rate surely above 0.5. A setting needs about 4 failures in 4 runs to clear that bar, so confirming 5 cases costs about 20 to 25 runs. That leaves roughly 30 runs to search, and the study stops early once 5 cases are confirmed.

What this plan cannot do:
- If fewer than 5 scenes break reliably within the budget, the study will report fewer than 5 confirmed cases.
- Near misses can guide the search, but the stopping rule only counts failures, so they are not a checked ranking.
- The tags do not say whether the ego merges or another car cuts in, so the two cases cannot be told apart.
- The 0-delay results were recorded with learned (CATK) traffic, not replay, so the pass/fail used to pick scenes is only a guide.
- Retiming a whole class moves every car in the scene, not only the one changing lanes.
- Only the three scenes with a marked cut-in car can isolate it.). Report written by claude-opus-5-5 from `results` in 23 s; every count above is computed from the queue, not written by the model.

55 of 55 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
