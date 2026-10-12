# In merge and cut-in scenes, which timings and speeds of the other cars make the VaVAM policy collide or leave the road? Find the 5 most challenging settings, each on a different scene and confirmed by repeats.

Study `random_confirm`: 54 kept runs on 9 scenes, varying actor_time_shift_s, actor_speed_scale; 2 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 4 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The goal was not met. By the code's count, four of the five cases cleared the bar: 096988dd with cars shifted +2 s at 1.25x speed (S11), 023b7fcc at −2 s and 1.5x (S2), 19f339ba at −0.5 s and 1.5x (S28), and 1c45ce3a at 0 s and 0.75x (S32). Each has only a few repeats, so the true failure rate is only known to be above one half. Triage of the videos and logs shows that only two of these four are failures by the policy. In S11 and S28 the policy drifted left into the next lane and hit a car driving alongside, even at 2 Hz planning. S2's failures are rear contacts that began before the policy took over. S32's are a replayed car cutting in and clipping the ego, which stayed in its lane. One more scene, 09a95ffa at 0 s and 1.25x (S12), also shows the policy's left drift, but its failure rate was not shown to be above one half.

## Findings

- On 096988dd, shifting the cars +2 s at 1.25x speed made every run fail. Each time the policy steered left against a STRAIGHT/RIGHT command and its front hit the car beside it in the left lane. This is a confirmed failure caused by the policy.
  - S11: 096988dd at actor_time_shift_s 2.0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_2hz_random_confirm_002, cut_in_merge_2hz_random_confirm_011, cut_in_merge_2hz_random_confirm_020)
- On 19f339ba, shifting the cars −0.5 s at 1.5x speed made every run fail. Each time the ego crawled at about 4 m/s, drifted about 2 m left and was hit side-on by a car passing in the left lane. This is a confirmed failure caused by the policy.
  - S28: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 1.5: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_2hz_random_confirm_004, cut_in_merge_2hz_random_confirm_012, cut_in_merge_2hz_random_confirm_021)
- The code counts 023b7fcc at −2 s and 1.5x as confirmed, but none of its failures were the policy's. A replayed car behind was already in rear contact before handoff, and that contact was scored as a side collision at the moment the policy took over. The brief says to ignore rear-end hits, so this case should not count.
  - S2: 023b7fcc at actor_time_shift_s -2.0, actor_speed_scale 1.5: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_2hz_random_confirm_026, cut_in_merge_2hz_random_confirm_028, cut_in_merge_2hz_random_confirm_037)
- The code counts 1c45ce3a at 0 s and 0.75x as confirmed, but the ego kept its lane and slowed gently each time. The retimed cut-in car (track 14) passed on the right and cut left into the ego's front-right corner. Triage judged these failures not the policy's fault, or unclear, so whether the ego could have avoided them is open.
  - S32: 1c45ce3a at actor_time_shift_s 0.0, actor_speed_scale 0.75: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_2hz_random_confirm_005, cut_in_merge_2hz_random_confirm_010, cut_in_merge_2hz_random_confirm_019_a2)
- On 09a95ffa at 0 s and 1.25x, most runs failed through the same left drift into a car overtaking in the left lane. The failure rate's range still reaches below one half, so this case is not confirmed.
  - S12: 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 1.25: 3/5 failed, rate 27%-86% (90%) (cut_in_merge_2hz_random_confirm_003, cut_in_merge_2hz_random_confirm_013, cut_in_merge_2hz_random_confirm_022, cut_in_merge_2hz_random_confirm_029, cut_in_merge_2hz_random_confirm_038)
- The other failures on 09a95ffa, and those on 096988dd at +2 s and 0.75x, 023b7fcc at 0 s and 0.5x, and 19f339ba at +1.5 s and 2x, happened before handoff. The ego was still replaying the log, its box already overlapped a lead or passing car, or the actor track was inconsistent. They are setup artifacts, not policy failures, even though the artifact flag did not catch them.
  - S15: 09a95ffa at actor_time_shift_s 1.5, actor_speed_scale 0.75: 2/2 failed, rate 42%-100% (90%) (cut_in_merge_2hz_random_confirm_042, cut_in_merge_2hz_random_confirm_046)
  - S16: 09a95ffa at actor_time_shift_s 2.0, actor_speed_scale 1.0: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_2hz_random_confirm_044)
  - S10: 096988dd at actor_time_shift_s 2.0, actor_speed_scale 0.75: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_2hz_random_confirm_035)
  - S3: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 0.5: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_2hz_random_confirm_041)
  - S29: 19f339ba at actor_time_shift_s 1.5, actor_speed_scale 2.0: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_2hz_random_confirm_033)
- On 023b7fcc, the one run at +1 s and 1.5x failed because the policy veered left into a car alongside. This is a hint of a policy failure only, not a rate. The run at +1.5 s and 1.5x was a sideswipe whose cause is unclear.
  - S4: 023b7fcc at actor_time_shift_s 1.0, actor_speed_scale 1.5: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_2hz_random_confirm_054)
  - S5: 023b7fcc at actor_time_shift_s 1.5, actor_speed_scale 1.5: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_2hz_random_confirm_036)
- No run failed on 12855a41, 0e899dd3, 0cf6368d or 054b5901. At 12855a41 (+1.5 s, 0.5x) and 0e899dd3 (−1.5 s, 1.0x), repeated runs put the failure rate below one half, even though both settings had near misses.
  - S25: 12855a41 at actor_time_shift_s 1.5, actor_speed_scale 0.5: 0/4 failed, rate 0%-40% (90%) (cut_in_merge_2hz_random_confirm_017, cut_in_merge_2hz_random_confirm_030, cut_in_merge_2hz_random_confirm_039, cut_in_merge_2hz_random_confirm_047)
  - S20: 0e899dd3 at actor_time_shift_s -1.5, actor_speed_scale 1.0: 0/4 failed, rate 0%-40% (90%) (cut_in_merge_2hz_random_confirm_009, cut_in_merge_2hz_random_confirm_031, cut_in_merge_2hz_random_confirm_040, cut_in_merge_2hz_random_confirm_048)
  - S21: 12855a41 at actor_time_shift_s -2.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_034)
  - S22: 12855a41 at actor_time_shift_s -1.5, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_043)
  - S23: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_006)
  - S24: 12855a41 at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_random_confirm_008, cut_in_merge_2hz_random_confirm_053)
  - S26: 12855a41 at actor_time_shift_s 1.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_015_a2)
  - S19: 0e899dd3 at actor_time_shift_s -2.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_051)
  - S17: 0cf6368d at actor_time_shift_s -1.5, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_023)
  - S18: 0cf6368d at actor_time_shift_s -0.5, actor_speed_scale 1.5: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_random_confirm_045, cut_in_merge_2hz_random_confirm_049)
  - S7: 054b5901 at actor_time_shift_s 1.0, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_016)

## Open

- Only two scenes (S11, S28) are confirmed failures caused by the policy. To find a third, repeat 09a95ffa at 0 s and 1.25x (S12) and 023b7fcc at +1 s and 1.5x (S4) until each range separates from one half.
- Fix or exclude the setups where boxes already overlap before handoff (023b7fcc at −2 s; 09a95ffa at +1.5–2 s; 096988dd at +2 s and 0.75x) and rerun them. Today their failures say nothing about the policy, and the artifact flag missed them.
- On 1c45ce3a (S32), it is unsettled whether braking or yielding could have avoided the cut-in, so it is unclear whether the case shows a policy weakness. Settings where the cut-in car leaves more room would show whether the ego reacts.
- 054b5901 had only a single run and 0cf6368d only a few, so the search did not establish that those scenes are safe.
- The comparison with the 10 Hz study cut_in_merge needs that study's results side by side. These results show only that the left drift into an adjacent car still happens at 2 Hz, not whether it happens less often.

## Why the runs failed (triage from the video and log)

turned_into_actor 10, actor_hit_ego 8, other 5

- cut_in_merge_2hz_random_confirm_002: turned_into_actor, policy at fault: yes. On a multi-lane highway, the route said RIGHT and the recorded path stayed in the ego's lane or bore right. Instead, the policy steered left toward the next lane (orange path) at about 4 m/s. Its front corner hit actor 41, which was driving alongside in that left lane.
- cut_in_merge_2hz_random_confirm_003: turned_into_actor, policy at fault: yes. After handoff the ego drove straight on the highway at about 8 m/s but drifted left, about 0.9 m off the human's path, into the next lane. Its front-left corner hit actor 33 as that car came alongside in the left lane, even though the route command had just changed to RIGHT.
- cut_in_merge_2hz_random_confirm_004: turned_into_actor, policy at fault: yes. The ego was moving slowly (about 4 m/s) on a multi-lane highway. Its planned path veered left of the recorded trajectory (about 2 m off), so it drifted across the lane line into the left lane. Vehicle 29 had come up from behind in that lane, and the ego's front-left struck it at 11.6 s.
- cut_in_merge_2hz_random_confirm_005: actor_hit_ego, policy at fault: unclear. On a multi-lane highway with no lead vehicle, the ego stayed in its lane (0.3 m from the recorded path) but slowed from 13.6 to 10 m/s. Actor 14 passed it on the right and merged left into the ego's lane, clipping the ego's front-right corner. A rear contact was also logged during the run.
- cut_in_merge_2hz_random_confirm_010: actor_hit_ego, policy at fault: no. The ego was going straight in its lane on a highway and slowing gently (13.6 to 10 m/s) while staying within 0.4 m of the recorded path. Actor 14 came up from behind on the right, passed alongside and cut left into the ego's lane, clipping the ego's front-right corner.
- cut_in_merge_2hz_random_confirm_011: turned_into_actor, policy at fault: yes. The ego slowed to about 4 m/s behind the white truck (actor 2), then drifted left into the next lane over, even though the command was STRAIGHT and then RIGHT. Its front hit vehicle 41, which was travelling in that left lane and was right beside the ego at 7.7 s.
- cut_in_merge_2hz_random_confirm_012: turned_into_actor, policy at fault: yes. On a straight multi-lane highway, the ego slowed from 4.6 to 3.4 m/s and wandered left, ending about 2 m left of the recorded path, instead of following its planned route line one lane to the right. At 11.6 s its left side hit actor 29, a small vehicle that had come up alongside in the left lane, as a lateral collision.
- cut_in_merge_2hz_random_confirm_013: turned_into_actor, policy at fault: yes. Cruising straight at about 8 m/s on a multi-lane freeway, the ego drifted about 0.9 m left of the recorded path, into the lane edge where actor 33 was passing on the left. The ego's front-left clipped actor 33 at 6.6 s. The lead vehicle was more than 25 m ahead, so braking for a lead was not the issue.
- cut_in_merge_2hz_random_confirm_020: turned_into_actor, policy at fault: yes. On a multi-lane highway in the rain, the ego steered left out of its lane even though the command was STRAIGHT and then RIGHT, and the recorded path stayed to the right. Moving at about 4 m/s, it cut into the left lane and its front hit actor 41, which was alongside it in that lane.
- cut_in_merge_2hz_random_confirm_021: turned_into_actor, policy at fault: yes. On a multi-lane highway, the ego was crawling at about 4 m/s, far below traffic speed and about 68 m behind where the human driver was. It also drifted about 2 m left toward the lane line, and a small actor (id 2) passing on its left made side contact at 11.6 s. The ego's slow speed and its drift into the next lane's space put it in the passing vehicle's path; nothing was close ahead of it.
- cut_in_merge_2hz_random_confirm_026: actor_hit_ego, policy at fault: no. Actor 66 came up behind the ego and was already overlapping its rear by 3.7s, before the policy took over (the rear-collision flag fires then). By 4.7s it had pushed further into the ego's box, so a lateral collision was recorded at the very moment of handoff (4.7s), while the ego was still cruising at about 4.2 m/s on the logged path with the lead car 11 m ahead.
- cut_in_merge_2hz_random_confirm_019_a2: actor_hit_ego, policy at fault: no. The ego was going straight in its lane, slowing from about 12 to 10 m/s and staying within 0.3 m of the recorded path. Actor 14 came up from behind on the right, passed it, and cut left into the ego's lane, so the rear of actor 14 clipped the ego's front-right corner. The ego was also rear-ended at some point in the run, so this was an actor hitting the ego rather than the ego driving into anything.
- cut_in_merge_2hz_random_confirm_028: actor_hit_ego, policy at fault: no. Actor 66, following in the ego's lane, ran into the ego's rear (rear contact already at 3.7s) while the ego was still replaying the recorded trajectory and the lead car was pulling away. At the 4.7s handoff the overlap had deepened and was counted as a side collision, so the 'at-fault' flag is an artifact; the policy had no chance to act.
- cut_in_merge_2hz_random_confirm_029: turned_into_actor, policy at fault: yes. On a straight multi-lane freeway at about 8 m/s, the policy's path bent left toward the next lane while actor 33 was overtaking in that lane. By 6.6 s the ego had moved about 0.9 m left of the recorded path, and its front-left corner hit actor 33 as the car came alongside.
- cut_in_merge_2hz_random_confirm_033: actor_hit_ego, policy at fault: no. On a straight multi-lane highway at about 17 m/s, replayed actors 28 and then 31 came up from behind in the ego's lane and drove straight through its box. The rear contact with 28 at 4.1s happened before the policy took over at 4.6s. By 5.1s actor 31 overlaps the ego and 28 has passed through to sit just ahead, so the "front" collision is a side effect of these non-reactive actors overlapping the ego, which stayed within 0.1 m of the recorded human path the whole time.
- cut_in_merge_2hz_random_confirm_035: other, policy at fault: no. The ego followed the recorded human path (0.0 m off) behind truck 2 in the same lane, and its box was already touching the truck at 3.7s (collision_any = 1 in that frame), which is before the policy took over at 4.7s. The front collision with truck 2 happened during log replay, probably because the actor or ego box is too large for the real gap (2.9 m), so it was flagged the moment the policy took over and the policy never really drove.
- cut_in_merge_2hz_random_confirm_036: actor_hit_ego, policy at fault: unclear. The ego stayed in its lane and sped up from 4.5 to 6.7 m/s. The recorded human trajectory, by contrast, drifted left. Actor 56 came up from behind on the ego's left, and at 7.2 s the two had a sideswipe (lateral) contact while the ego was about 1.4 m from the recorded path, with no clear steer by the ego into 56.
- cut_in_merge_2hz_random_confirm_037: actor_hit_ego, policy at fault: no. Actor 66 came up behind the ego and was already in rear contact by 3.7 s, before the policy took over at 4.7 s. At handoff the ego was exactly on the recorded path, slowing gently with a growing gap to the car ahead. The contact still in progress was then scored as an at-fault side collision.
- cut_in_merge_2hz_random_confirm_041: other, policy at fault: no. The ego was still replaying the recorded human trajectory (0 m off the recording) in slow traffic. Its box was already overlapping the lead car 12 in the same lane by 3.7 s, when collision_front first registers. The policy only took over at 4.7 s, the same moment the failure was counted, so this looks like an artifact of the scenario setup or actor-track overlap in the log rather than a decision by the policy.
- cut_in_merge_2hz_random_confirm_042: other, policy at fault: no. Before handoff the ego was replaying the recorded trajectory (0.0 m off the recording) at a steady 8 m/s, closing on actor 1 ahead from 7.6 m to 0 m. A front collision was already flagged at 3.6 s, and by the 4.6 s handoff the ego box sat completely on top of actor 1. The camera shows no vehicle in that spot, so actor 1 is probably a badly placed or ghost reconstruction, and the failure was scored at the first moment the policy took over, before it could do anything.
- cut_in_merge_2hz_random_confirm_044: other, policy at fault: no. The ego was still replaying the recorded human drive at a steady ~8 m/s. Its box already overlapped lead actor 1 from 2.6 s on (collision_front Per-Ts = 1 in every frame, gap only 2–3 m), so the collision was flagged the instant the policy took over at 4.6 s. This is a log or bounding-box overlap artifact, not anything the policy did.
- cut_in_merge_2hz_random_confirm_046: other, policy at fault: no. The ego was still replaying the recorded human trajectory (0.0 m off the log), and the collision happened at 4.6 s, the same moment as handoff, so the policy never controlled the car. Lead actor 1's track closed in on the ego's logged path at a steady 2.6 m/s until the two boxes overlapped (camera smeared at 3.6 s, full overlap at 4.6 s). This points to an inconsistent actor track in the reconstruction, not a driving mistake.
- cut_in_merge_2hz_random_confirm_054: turned_into_actor, policy at fault: yes. On a multi-lane highway with the command STRAIGHT (RIGHT at the end), the ego sped up from 4.5 to 6.7 m/s and followed a planned path that veered left, away from the recorded route. It drifted into the adjacent left lane and its front hit vehicle 56, which was travelling alongside in that lane. The rear contact came afterwards.

## Every setting

- S1: 023b7fcc at actor_time_shift_s -2.0, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_052)
- S2: 023b7fcc at actor_time_shift_s -2.0, actor_speed_scale 1.5: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_2hz_random_confirm_026, cut_in_merge_2hz_random_confirm_028, cut_in_merge_2hz_random_confirm_037)
- S3: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 0.5: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_2hz_random_confirm_041)
- S4: 023b7fcc at actor_time_shift_s 1.0, actor_speed_scale 1.5: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_2hz_random_confirm_054)
- S5: 023b7fcc at actor_time_shift_s 1.5, actor_speed_scale 1.5: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_2hz_random_confirm_036)
- S6: 023b7fcc at actor_time_shift_s 2.0, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_032)
- S7: 054b5901 at actor_time_shift_s 1.0, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_016)
- S8: 096988dd at actor_time_shift_s 0.0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_025)
- S9: 096988dd at actor_time_shift_s 0.5, actor_speed_scale 2.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_050)
- S10: 096988dd at actor_time_shift_s 2.0, actor_speed_scale 0.75: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_2hz_random_confirm_035)
- S11: 096988dd at actor_time_shift_s 2.0, actor_speed_scale 1.25: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_2hz_random_confirm_002, cut_in_merge_2hz_random_confirm_011, cut_in_merge_2hz_random_confirm_020)
- S12: 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 1.25: 3/5 failed, rate 27%-86% (90%) (cut_in_merge_2hz_random_confirm_003, cut_in_merge_2hz_random_confirm_013, cut_in_merge_2hz_random_confirm_022, cut_in_merge_2hz_random_confirm_029, cut_in_merge_2hz_random_confirm_038)
- S13: 09a95ffa at actor_time_shift_s 1.0, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_001)
- S14: 09a95ffa at actor_time_shift_s 1.0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_018)
- S15: 09a95ffa at actor_time_shift_s 1.5, actor_speed_scale 0.75: 2/2 failed, rate 42%-100% (90%) (cut_in_merge_2hz_random_confirm_042, cut_in_merge_2hz_random_confirm_046)
- S16: 09a95ffa at actor_time_shift_s 2.0, actor_speed_scale 1.0: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_2hz_random_confirm_044)
- S17: 0cf6368d at actor_time_shift_s -1.5, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_023)
- S18: 0cf6368d at actor_time_shift_s -0.5, actor_speed_scale 1.5: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_random_confirm_045, cut_in_merge_2hz_random_confirm_049)
- S19: 0e899dd3 at actor_time_shift_s -2.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_051)
- S20: 0e899dd3 at actor_time_shift_s -1.5, actor_speed_scale 1.0: 0/4 failed, rate 0%-40% (90%) (cut_in_merge_2hz_random_confirm_009, cut_in_merge_2hz_random_confirm_031, cut_in_merge_2hz_random_confirm_040, cut_in_merge_2hz_random_confirm_048)
- S21: 12855a41 at actor_time_shift_s -2.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_034)
- S22: 12855a41 at actor_time_shift_s -1.5, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_043)
- S23: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_006)
- S24: 12855a41 at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_2hz_random_confirm_008, cut_in_merge_2hz_random_confirm_053)
- S25: 12855a41 at actor_time_shift_s 1.5, actor_speed_scale 0.5: 0/4 failed, rate 0%-40% (90%) (cut_in_merge_2hz_random_confirm_017, cut_in_merge_2hz_random_confirm_030, cut_in_merge_2hz_random_confirm_039, cut_in_merge_2hz_random_confirm_047)
- S26: 12855a41 at actor_time_shift_s 1.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_015_a2)
- S27: 19f339ba at actor_time_shift_s -1.0, actor_speed_scale 2.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_024)
- S28: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 1.5: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_2hz_random_confirm_004, cut_in_merge_2hz_random_confirm_012, cut_in_merge_2hz_random_confirm_021)
- S29: 19f339ba at actor_time_shift_s 1.5, actor_speed_scale 2.0: 1/1 failed, rate 27%-100% (90%) (cut_in_merge_2hz_random_confirm_033)
- S30: 1c45ce3a at actor_time_shift_s -1.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_014)
- S31: 1c45ce3a at actor_time_shift_s 0.0, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_007)
- S32: 1c45ce3a at actor_time_shift_s 0.0, actor_speed_scale 0.75: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_2hz_random_confirm_005, cut_in_merge_2hz_random_confirm_010, cut_in_merge_2hz_random_confirm_019_a2)
- S33: 1c45ce3a at actor_time_shift_s 1.0, actor_speed_scale 2.0: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_2hz_random_confirm_027)

## Not kept by the gate

- cut_in_merge_2hz_random_confirm_015: not kept: RE-RUN
- cut_in_merge_2hz_random_confirm_019: not kept: RE-RUN

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
- Only the three scenes with a marked cut-in car can isolate it.). Report written by claude-opus-5-5 from `results` in 24 s; every count above is computed from the queue, not written by the model.

56 of 56 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
