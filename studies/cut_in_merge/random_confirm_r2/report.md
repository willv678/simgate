# In merge and cut-in scenes, which timings and speeds of the other cars make the VaVAM policy collide or leave the road? Find the 5 most challenging settings, each on a different scene and confirmed by repeats.

Study `random_confirm_r2`: 54 kept runs on 8 scenes, varying actor_time_shift_s, actor_speed_scale; 2 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 3 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The goal was not met. The automatic check confirmed three challenging settings: 09a95ffa at -1.5 s / 1.25x (S11), 023b7fcc at +0.5 s / 2x (S3) and 054b5901 at -1.0 s / 1.25x (S5). However, the video and log review found that none of the failures at those three settings were the policy's fault. In each one, a replayed car drives through the ego from behind before the handoff, and the overlap is scored as a front collision at the moment the policy takes over. So they are replay artifacts, or rear hits the plan said to ignore, and they say nothing about how the policy handles the retiming. Failures the policy did cause (drifting left against a RIGHT command, cutting into the next lane, leaving the road, or not braking for a stopped lead car) appeared on four scenes. Each rests on a single run, except 1c45ce3a at +2.0 s / 1.25x, where the failure-rate range still spans both sides of one half. This study found no confirmed policy-caused case, and no clear link between timing or speed and collisions.

## Findings

- The three settings the check counts as confirmed failed on every kept run. But every one of those failures was a replayed car driving through the ego from behind before the handoff, scored as a front collision the moment the policy took over. The policy was not at fault, and these are not evidence of policy failures in a cut-in or merge.
  - S3: 023b7fcc at actor_time_shift_s 0.5, actor_speed_scale 2.0: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_random_confirm_r2_005, cut_in_merge_random_confirm_r2_011, cut_in_merge_random_confirm_r2_020)
  - S5: 054b5901 at actor_time_shift_s -1.0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_random_confirm_r2_009, cut_in_merge_random_confirm_r2_013, cut_in_merge_random_confirm_r2_022)
  - S11: 09a95ffa at actor_time_shift_s -1.5, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_random_confirm_r2_001, cut_in_merge_random_confirm_r2_012, cut_in_merge_random_confirm_r2_021)
- The failure at 09a95ffa, -0.5 s / 1.5x, is the same pass-through replay artifact, not a policy error.
  - S13: 09a95ffa at actor_time_shift_s -0.5, actor_speed_scale 1.5: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_random_confirm_r2_017)
- On 023b7fcc, the policy caused failures at three different timings. At -2.0 s / 2x it did not brake for a stopped car directly ahead and steered left instead. At -0.5 s / 1x and +1.5 s / 1.25x it drifted left against a RIGHT command into an adjacent car. Each is a single run, so it is a hint, not a rate. The +1.5 s run is also flagged as a possible artifact because the ego was far from the recorded path.
  - S1: 023b7fcc at actor_time_shift_s -2.0, actor_speed_scale 2.0: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_random_confirm_r2_054)
  - S2: 023b7fcc at actor_time_shift_s -0.5, actor_speed_scale 1.0: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_random_confirm_r2_043)
  - S4: 023b7fcc at actor_time_shift_s 1.5, actor_speed_scale 1.25: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (cut_in_merge_random_confirm_r2_033)
- On 054b5901 at +2.0 s, the policy failed at both 1.0x and 1.25x: it drifted left of the route and either left the road at the median or ran into a car stopped at a red light. These are single runs, flagged as possible artifacts only because the ego had drifted far from the recorded path. The same scene passed at -1.0 s / 2x, -0.5 s / 2x and +1.0 s / 1.5x.
  - S9: 054b5901 at actor_time_shift_s 2.0, actor_speed_scale 1.0: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (cut_in_merge_random_confirm_r2_032)
  - S10: 054b5901 at actor_time_shift_s 2.0, actor_speed_scale 1.25: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (cut_in_merge_random_confirm_r2_036)
  - S6: 054b5901 at actor_time_shift_s -1.0, actor_speed_scale 2.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_random_confirm_r2_025)
  - S7: 054b5901 at actor_time_shift_s -0.5, actor_speed_scale 2.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_random_confirm_r2_006)
  - S8: 054b5901 at actor_time_shift_s 1.0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_random_confirm_r2_050)
- On 09a95ffa at -1.5 s / 2x, the policy steered back toward the route from the wrong lane and hit a car in the adjacent lane. This is a single run, flagged as a possible artifact because of the ego's offset from the path.
  - S12: 09a95ffa at actor_time_shift_s -1.5, actor_speed_scale 2.0: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (cut_in_merge_random_confirm_r2_041)
- On 1c45ce3a at +2.0 s / 1.25x, the policy left the road on the left side of a freeway while ignoring a RIGHT command, with no other car nearby. It did so in some repeats but not all, and the range does not show a rate above one half. The failure looks like route-following, not a reaction to the retimed car.
  - S33: 1c45ce3a at actor_time_shift_s 2.0, actor_speed_scale 1.25: 2/6 failed, rate 12%-65% (90%), 2 possibly the simulator's (cut_in_merge_random_confirm_r2_003_a2, cut_in_merge_random_confirm_r2_010, cut_in_merge_random_confirm_r2_019, cut_in_merge_random_confirm_r2_028, cut_in_merge_random_confirm_r2_037_a2, cut_in_merge_random_confirm_r2_046)
- A common pattern in the failures the policy caused is drifting left when the command was RIGHT. That points to a route-following weakness rather than a reaction to the timing or speed of a cut-in car.
  - S2: 023b7fcc at actor_time_shift_s -0.5, actor_speed_scale 1.0: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_random_confirm_r2_043)
  - S4: 023b7fcc at actor_time_shift_s 1.5, actor_speed_scale 1.25: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (cut_in_merge_random_confirm_r2_033)
  - S9: 054b5901 at actor_time_shift_s 2.0, actor_speed_scale 1.0: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (cut_in_merge_random_confirm_r2_032)
  - S10: 054b5901 at actor_time_shift_s 2.0, actor_speed_scale 1.25: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (cut_in_merge_random_confirm_r2_036)
  - S12: 09a95ffa at actor_time_shift_s -1.5, actor_speed_scale 2.0: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (cut_in_merge_random_confirm_r2_041)
  - S33: 1c45ce3a at actor_time_shift_s 2.0, actor_speed_scale 1.25: 2/6 failed, rate 12%-65% (90%), 2 possibly the simulator's (cut_in_merge_random_confirm_r2_003_a2, cut_in_merge_random_confirm_r2_010, cut_in_merge_random_confirm_r2_019, cut_in_merge_random_confirm_r2_028, cut_in_merge_random_confirm_r2_037_a2, cut_in_merge_random_confirm_r2_046)
- Settings repeated without a failure look safe: 0e899dd3 at +1.0 s / 0.75x and 12855a41 at +1.0 s / 1.5x (the range rules out a rate above one half), and 19f339ba at -1.5 s / 1.25x. No run on 0cf6368d, 0e899dd3, 12855a41 or 19f339ba failed.
  - S22: 0e899dd3 at actor_time_shift_s 1.0, actor_speed_scale 0.75: 0/4 failed, rate 0%-40% (90%) (cut_in_merge_random_confirm_r2_015, cut_in_merge_random_confirm_r2_023, cut_in_merge_random_confirm_r2_029, cut_in_merge_random_confirm_r2_048)
  - S26: 12855a41 at actor_time_shift_s 1.0, actor_speed_scale 1.5: 0/4 failed, rate 0%-40% (90%) (cut_in_merge_random_confirm_r2_026, cut_in_merge_random_confirm_r2_030, cut_in_merge_random_confirm_r2_039, cut_in_merge_random_confirm_r2_049)
  - S27: 19f339ba at actor_time_shift_s -1.5, actor_speed_scale 1.25: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_random_confirm_r2_002, cut_in_merge_random_confirm_r2_031, cut_in_merge_random_confirm_r2_040)
  - S16: 0cf6368d at actor_time_shift_s -2.0, actor_speed_scale 2.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_random_confirm_r2_018)
  - S17: 0cf6368d at actor_time_shift_s -1.0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_random_confirm_r2_044)
  - S18: 0cf6368d at actor_time_shift_s -0.5, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_random_confirm_r2_014)
  - S19: 0cf6368d at actor_time_shift_s -0.5, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_random_confirm_r2_027)
  - S20: 0cf6368d at actor_time_shift_s 0.5, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_random_confirm_r2_035)
  - S21: 0e899dd3 at actor_time_shift_s -1.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_random_confirm_r2_052)
  - S23: 0e899dd3 at actor_time_shift_s 1.5, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_random_confirm_r2_034, cut_in_merge_random_confirm_r2_038)
  - S24: 0e899dd3 at actor_time_shift_s 2.0, actor_speed_scale 2.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_random_confirm_r2_042)
  - S25: 12855a41 at actor_time_shift_s 0.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_random_confirm_r2_053)
  - S28: 19f339ba at actor_time_shift_s -1.5, actor_speed_scale 1.5: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_random_confirm_r2_045, cut_in_merge_random_confirm_r2_047)
  - S29: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_random_confirm_r2_007)

## Open

- Whether any setting really causes policy failures at a rate above one half is still unknown. All three settings the check counted as confirmed rest on replay artifacts, so the stopping rule should leave out failures that happen before the handoff, or ego pass-throughs. One fix is to move the handoff earlier or drop the overlapping replayed car on 023b7fcc, 054b5901 and 09a95ffa, then rerun S3, S5 and S11.
- The policy-caused single-run failures need repeats to see whether they hold up: about four runs each at S1 (023b7fcc -2.0 s / 2x), S2 (023b7fcc -0.5 s / 1x), S10 or S9 (054b5901 +2.0 s) and S12 (09a95ffa -1.5 s / 2x).
- S33 (1c45ce3a +2.0 s / 1.25x) needs more repeats to tell whether its failure rate is above one half. Running it at 0 s / 1x would show whether the left-side road departure happens regardless of the retiming.
- We still don't know whether the timing and speed knobs matter at all. The policy's failures look like route-following errors (drifting left against a RIGHT command). Running the failing scenes at the recorded timing would show whether they fail regardless of the knobs.
- Only four of the five required scenes produced any policy failure, and four scenes never failed. Near-miss settings there (for example 0e899dd3 -1.0 s / 1.25x and 19f339ba -1.5 s / 1.5x) are unprobed neighbours worth searching for a fifth case.
- Merges where the ego changes lanes and cut-ins by another car could not be told apart. The six scenes that retimed every car can't isolate which car caused a given failure.

## Why the runs failed (triage from the video and log)

actor_hit_ego 6, other 4, left_road 3, turned_into_actor 3, no_brake_for_lead 2

- cut_in_merge_random_confirm_r2_001: other, policy at fault: no. This is a simulation artifact, not a driving error. Actor 21 starts out overlapping the ego's box: at 2.6s the frame already shows a rear collision. It then moves forward through the ego and is still touching the ego's front at 4.6s, which is exactly when the policy takes over (handoff), so the collision is counted immediately. The ego was still exactly on the recorded human path (0.0 m off) at a steady ~8 m/s, so the policy had no chance to act.
- cut_in_merge_random_confirm_r2_005: actor_hit_ego, policy at fault: no. The ego was going straight down its lane at about 4.4 m/s, exactly on the recorded human path, when actor 13 came up from behind and drove into it: by 3.7 s it overlaps the ego's rear and the metrics show a rear collision. Actor 13 kept going through the ego and ended up just ahead of it, so at 4.7 s, the moment the policy took over, the overlap was scored as a front collision that the policy had no chance to avoid.
- cut_in_merge_random_confirm_r2_009: actor_hit_ego, policy at fault: no. Actor 16 came up from behind and drove through the ego (rear overlap at 2.7s, full overlap at 3.7s, front overlap at 4.7s) while the ego was still exactly on the recorded human path before handoff. The front collision was counted at the handoff moment (4.7s), so the policy never had a chance to react. This is likely a replay artifact where the other car's recorded track overlaps the ego's.
- cut_in_merge_random_confirm_r2_003_a2: left_road, policy at fault: yes. On a multi-lane freeway with a RIGHT command, the ego (about 8.7 m/s, no lead vehicle) kept planning straight and slightly left instead of following the recorded path toward the right. It drifted onto the left yellow edge line and over it onto the left shoulder/median, and was flagged offroad at 12.2 s about 4.8 m from the human trajectory. The 12.2 s frame file was missing, so this is based on the 10.2 s and 11.2 s frames; the camera was clean at 10.2 s, when the drift was already underway.
- cut_in_merge_random_confirm_r2_010: left_road, policy at fault: yes. On a freeway with a RIGHT command, the ego drove about 9 m/s along the far-left edge, straddling the yellow edge line, while the recorded path went off to the right. Its planned path stayed hugging the left boundary, and as the road curved right it went off the road on the left at 12.2 s. No other vehicle was close, and the camera view was clean before the failure.
- cut_in_merge_random_confirm_r2_011: actor_hit_ego, policy at fault: no. At 3.7s, before the handoff, the ego was still on the recorded path at about 4.4 m/s when actor 13 came up from behind in the same lane and drove into it (collision_rear). Actor 13 then went through the ego's footprint and came out just ahead (gap 0.8 m, then 3.6 m), so at the 4.7s handoff the overlap counts as a front collision; the policy had no time to act.
- cut_in_merge_random_confirm_r2_012: other, policy at fault: no. The replayed vehicle 21 already overlapped the ego's footprint while the ego was still replaying the human drive at about 8 m/s (rear contact flagged at 2.6 s, front overlap by 3.6 s). The collision was counted the moment the policy took over at 4.6 s, so this is a pre-existing overlap from the log replay, not a driving mistake.
- cut_in_merge_random_confirm_r2_013: actor_hit_ego, policy at fault: no. Replayed actor 16 came up from behind and drove straight through the ego, which was exactly on the recorded path at ~14 m/s: it is behind at 2.7s, overlapping at 3.7s (rear-collision flag, smeared camera), and ahead at 4.7s. So the "front collision" at 4.7s is the actor still overlapping as it leaves through the ego's nose. The failure was logged at the same moment as the handoff (4.7s), so the policy never got to act.
- cut_in_merge_random_confirm_r2_017: actor_hit_ego, policy at fault: no. Before the policy took over, while the ego was replaying the logged drive at about 8 m/s, actor 21 came from behind and drove through it (rear contact at about 3.6 s), ending up just ahead of the ego. The front collision with actor 21 was logged at 4.6 s, the same instant the policy took control, so the policy had no time to respond.
- cut_in_merge_random_confirm_r2_020: actor_hit_ego, policy at fault: no. Actor 13 came up from behind in the ego's lane, hit the ego's rear at about 3.7 s while the ego was still replaying the human log, then drove through the ego and came out just ahead of it. That is why a front collision was recorded at 4.7 s, the same moment the policy took over. The ego was exactly on the recorded trajectory at a steady ~4.3 m/s, so the policy had no chance to act.
- cut_in_merge_random_confirm_r2_021: other, policy at fault: no. Before handoff, replayed actor 21 in the ego's lane was already overlapping the ego and drove through it from behind. A rear collision was recorded at 2.6 s, the actor fully overlapped the ego at 3.6 s, and it was just ahead when the policy took over at 4.6 s. The front contact counted as the failure is a log-replay artifact (an actor overlapping the ego while the ego followed the recorded path, 0 m off it), not a policy decision.
- cut_in_merge_random_confirm_r2_022: other, policy at fault: no. Actor 16 began just behind the ego in the same lane at 2.7s, overlapped it at 3.7s, and was still overlapping the ego's front at 4.7s, so it drove through the ego. This looks like a duplicate or ghost of the ego's own logged vehicle, not a real collision. The failure was recorded at 4.7s, the same moment the policy took over, so the policy never had control before the contact.
- cut_in_merge_random_confirm_r2_032: left_road, policy at fault: yes. With a RIGHT command, the ego drifted left instead of right after the handoff. It ended up in the leftmost lanes, about 7.7 m left of the recorded path, which kept to the right lanes. Slowing to about 6 m/s on the approach to the intersection, it crossed the edge of the median island on its left and was flagged offroad at 10.0 s, with no collision.
- cut_in_merge_random_confirm_r2_033: turned_into_actor, policy at fault: yes. Despite a RIGHT command, the ego drifted a lane left of the recorded path and kept steering left across the lane line. Its left-rear side then touched vehicle 85, which was travelling in the lane the ego was moving into.
- cut_in_merge_random_confirm_r2_036: no_brake_for_lead, policy at fault: yes. The ego had drifted about 7 m left of the recorded path, into the left lane instead of the right-turn lane. There it closed on car 9, which was stopped at a red light, and slowed only gradually (7.0 to 3.3 m/s) as the gap shrank from 11 m to 4.8 m, so it hit car 9's rear at 12.2 s. The lead car was clearly visible in the camera, so the policy simply didn't brake hard enough. The 12.2 s frame file was missing, so this is based on the 10.2 s and 11.2 s frames plus the motion data.
- cut_in_merge_random_confirm_r2_041: turned_into_actor, policy at fault: yes. The ego was about 6 m left of the recorded route, which keeps right. It steered right toward the route and front-hit actor 87, which was ahead of it in the adjacent right lane. The ego was going about 5 m/s and slowed only a little. The lead gap fell from 29 m to 4.5 m as 87 came into the ego's path. The run also logged a rear contact, but the front collision started first.
- cut_in_merge_random_confirm_r2_043: turned_into_actor, policy at fault: yes. After handoff the policy planned a drift left across lane lines, while the human drove straight and then bore right, which matched the RIGHT command. The ego cut into the left lane and made side contact with vehicle 56, which was alongside and slightly behind it. That was followed by rear contact.
- cut_in_merge_random_confirm_r2_054: no_brake_for_lead, policy at fault: yes. Vehicle 66, directly ahead in the ego's lane, was stopped or nearly stopped. The gap shrank from 10.7 m to contact while the ego held about 4.2 m/s and never braked. After the policy took over at 4.7 s (gap about 9 m), its planned path swung left toward the next lane instead of slowing, and the ego's front hit 66 at 5.6 s.

## Every setting

- S1: 023b7fcc at actor_time_shift_s -2.0, actor_speed_scale 2.0: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_random_confirm_r2_054)
- S2: 023b7fcc at actor_time_shift_s -0.5, actor_speed_scale 1.0: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_random_confirm_r2_043)
- S3: 023b7fcc at actor_time_shift_s 0.5, actor_speed_scale 2.0: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_random_confirm_r2_005, cut_in_merge_random_confirm_r2_011, cut_in_merge_random_confirm_r2_020)
- S4: 023b7fcc at actor_time_shift_s 1.5, actor_speed_scale 1.25: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (cut_in_merge_random_confirm_r2_033)
- S5: 054b5901 at actor_time_shift_s -1.0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_random_confirm_r2_009, cut_in_merge_random_confirm_r2_013, cut_in_merge_random_confirm_r2_022)
- S6: 054b5901 at actor_time_shift_s -1.0, actor_speed_scale 2.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_random_confirm_r2_025)
- S7: 054b5901 at actor_time_shift_s -0.5, actor_speed_scale 2.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_random_confirm_r2_006)
- S8: 054b5901 at actor_time_shift_s 1.0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_random_confirm_r2_050)
- S9: 054b5901 at actor_time_shift_s 2.0, actor_speed_scale 1.0: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (cut_in_merge_random_confirm_r2_032)
- S10: 054b5901 at actor_time_shift_s 2.0, actor_speed_scale 1.25: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (cut_in_merge_random_confirm_r2_036)
- S11: 09a95ffa at actor_time_shift_s -1.5, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_random_confirm_r2_001, cut_in_merge_random_confirm_r2_012, cut_in_merge_random_confirm_r2_021)
- S12: 09a95ffa at actor_time_shift_s -1.5, actor_speed_scale 2.0: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (cut_in_merge_random_confirm_r2_041)
- S13: 09a95ffa at actor_time_shift_s -0.5, actor_speed_scale 1.5: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_random_confirm_r2_017)
- S14: 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_random_confirm_r2_051)
- S15: 09a95ffa at actor_time_shift_s 0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_random_confirm_r2_016)
- S16: 0cf6368d at actor_time_shift_s -2.0, actor_speed_scale 2.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_random_confirm_r2_018)
- S17: 0cf6368d at actor_time_shift_s -1.0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_random_confirm_r2_044)
- S18: 0cf6368d at actor_time_shift_s -0.5, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_random_confirm_r2_014)
- S19: 0cf6368d at actor_time_shift_s -0.5, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_random_confirm_r2_027)
- S20: 0cf6368d at actor_time_shift_s 0.5, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_random_confirm_r2_035)
- S21: 0e899dd3 at actor_time_shift_s -1.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_random_confirm_r2_052)
- S22: 0e899dd3 at actor_time_shift_s 1.0, actor_speed_scale 0.75: 0/4 failed, rate 0%-40% (90%) (cut_in_merge_random_confirm_r2_015, cut_in_merge_random_confirm_r2_023, cut_in_merge_random_confirm_r2_029, cut_in_merge_random_confirm_r2_048)
- S23: 0e899dd3 at actor_time_shift_s 1.5, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_random_confirm_r2_034, cut_in_merge_random_confirm_r2_038)
- S24: 0e899dd3 at actor_time_shift_s 2.0, actor_speed_scale 2.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_random_confirm_r2_042)
- S25: 12855a41 at actor_time_shift_s 0.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_random_confirm_r2_053)
- S26: 12855a41 at actor_time_shift_s 1.0, actor_speed_scale 1.5: 0/4 failed, rate 0%-40% (90%) (cut_in_merge_random_confirm_r2_026, cut_in_merge_random_confirm_r2_030, cut_in_merge_random_confirm_r2_039, cut_in_merge_random_confirm_r2_049)
- S27: 19f339ba at actor_time_shift_s -1.5, actor_speed_scale 1.25: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_random_confirm_r2_002, cut_in_merge_random_confirm_r2_031, cut_in_merge_random_confirm_r2_040)
- S28: 19f339ba at actor_time_shift_s -1.5, actor_speed_scale 1.5: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_random_confirm_r2_045, cut_in_merge_random_confirm_r2_047)
- S29: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_random_confirm_r2_007)
- S30: 1c45ce3a at actor_time_shift_s -2.0, actor_speed_scale 2.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_random_confirm_r2_008)
- S31: 1c45ce3a at actor_time_shift_s -1.0, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_random_confirm_r2_024)
- S32: 1c45ce3a at actor_time_shift_s -0.5, actor_speed_scale 2.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_random_confirm_r2_004)
- S33: 1c45ce3a at actor_time_shift_s 2.0, actor_speed_scale 1.25: 2/6 failed, rate 12%-65% (90%), 2 possibly the simulator's (cut_in_merge_random_confirm_r2_003_a2, cut_in_merge_random_confirm_r2_010, cut_in_merge_random_confirm_r2_019, cut_in_merge_random_confirm_r2_028, cut_in_merge_random_confirm_r2_037_a2, cut_in_merge_random_confirm_r2_046)

## Not kept by the gate

- cut_in_merge_random_confirm_r2_003: not kept: RE-RUN
- cut_in_merge_random_confirm_r2_037: not kept: RE-RUN

## Provenance

Plan: `plan.json` (rationale: Scope and settings follow the brief. Traffic is replayed as recorded. Only recorded cars (class automobile) are retimed, using the knobs' full ranges: -2 s to +2 s and 0.5x to 2x speed.

Scene choice: 31 scenes carry the merge_cut_in tag. I kept 9 that passed at 0 delay and have a car identified as a key actor. Scenes that already fail with the recorded timing would fill the top 5 without showing what the retiming does, so I left them out. Three scenes have a car marked as cutting in (0cf6368d track 21, 12855a41 track 31, 1c45ce3a track 14). In those, only that car is retimed. The other six retime every car in the scene: with only a lead or crossing car identified, retiming that car alone could miss the car that actually changes lanes. Several picks already came close at baseline (023b7fcc and 096988dd at 0.0 m, 19f339ba at 0.03 m, 12855a41 at 0.08 m, 054b5901 at 0.26 m), so they are good places to look first.

Budget and stopping rule: 6 rounds of 9 runs gives 54 runs, close to the brief's ~50 and under the cap of 60. The goal is top_k with k=5, one case per scene, failure rate surely above 0.5. A setting needs about 4 failures in 4 runs to clear that bar, so confirming 5 cases costs about 20 to 25 runs. That leaves roughly 30 runs to search, and the study stops early once 5 cases are confirmed.

What this plan cannot do:
- If fewer than 5 scenes break reliably within the budget, the study will report fewer than 5 confirmed cases.
- Near misses can guide the search, but the stopping rule only counts failures, so they are not a checked ranking.
- The tags do not say whether the ego merges or another car cuts in, so the two cases cannot be told apart.
- The 0-delay results were recorded with learned (CATK) traffic, not replay, so the pass/fail used to pick scenes is only a guide.
- Retiming a whole class moves every car in the scene, not only the one changing lanes.
- Only the three scenes with a marked cut-in car can isolate it.). Report written by claude-opus-5-5 from `results` in 27 s; every count above is computed from the queue, not written by the model.

56 of 56 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
