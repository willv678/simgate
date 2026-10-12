# In merge and cut-in scenes, which timings and speeds of the other cars make the VaVAM policy collide or leave the road? Find the 5 most challenging settings, each on a different scene and confirmed by repeats.

Study `hybrid_r3`: 54 kept runs on 9 scenes, varying actor_time_shift_s, actor_speed_scale; 0 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 5 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The goal check counts five confirmed settings, but only four are real policy failures. Every one has the recorded timing (0 s shift) with the cars sped up: 023b7fcc at 1.25x (S1), 09a95ffa at 1.25x (S8), 0e899dd3 at 2x (S14), 19f339ba at 2x (S23) and 096988dd at 2x (S7). In the first four, the policy almost always steered left into a car beside it or passing it in the next lane, even though the command was STRAIGHT or RIGHT. These are not reactions to another car cutting in. The fifth case, S7 on 096988dd, does not hold up: in every run a replayed car hit the ego from behind and drove through it before the policy took control, which is a rear-end hit the plan said to ignore. So the study shows four policy cases, not five. S23 and S7 rest on three runs each, so their ranges only just clear one half. Timing was hardly tested, so the study cannot say which timings cause failures.

## Findings

- On 023b7fcc at the recorded timing and 1.25x speed, every run failed. In each one the policy left a straight route by steering left into car 56, which was driving alongside in the next lane. The policy was at fault in all of them.
  - S1: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1.25: 4/4 failed, rate 60%-100% (90%) (cut_in_merge_hybrid_r3_004, cut_in_merge_hybrid_r3_010, cut_in_merge_hybrid_r3_011, cut_in_merge_hybrid_r3_012)
- On 09a95ffa at the recorded timing and 1.25x speed, every run failed the same way: the ego drifted left into car 33 coming up alongside, while the command was STRAIGHT or RIGHT. In one run, triage could not tell whether the policy was at fault.
  - S8: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25: 4/4 failed, rate 60%-100% (90%) (cut_in_merge_hybrid_r3_007, cut_in_merge_hybrid_r3_013, cut_in_merge_hybrid_r3_014, cut_in_merge_hybrid_r3_015)
- On 0e899dd3, every run at 2x speed failed: the ego mostly angled left into the slower car 23 ahead and to its left, while the recorded driver moved right. In one run, car 23 (replayed, so it does not react) cut down onto the ego as it slowed, and fault there is unclear. The few runs at 1.25x and 1.5x did not fail.
  - S14: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 2: 5/5 failed, rate 65%-100% (90%) (cut_in_merge_hybrid_r3_022, cut_in_merge_hybrid_r3_023, cut_in_merge_hybrid_r3_028, cut_in_merge_hybrid_r3_029, cut_in_merge_hybrid_r3_030)
  - S12: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_hybrid_r3_009, cut_in_merge_hybrid_r3_016)
  - S13: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_hybrid_r3_017, cut_in_merge_hybrid_r3_024)
- On 19f339ba, every run at 2x speed failed. The policy braked hard with nothing close ahead, then drifted left into car 24 passing in the next lane. One run at 1.5x failed the same way and the single run at 1.25x passed, which hints that risk rises with car speed.
  - S23: 19f339ba at actor_time_shift_s 0, actor_speed_scale 2: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_hybrid_r3_046, cut_in_merge_hybrid_r3_047, cut_in_merge_hybrid_r3_048)
  - S22: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.5: 1/2 failed, rate 12%-88% (90%) (cut_in_merge_hybrid_r3_041, cut_in_merge_hybrid_r3_042)
  - S21: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r3_006)
- The 096988dd case at 2x is not a policy failure. In every run, replayed car 9 hit the ego's rear and drove through it before the policy took over; the overlap was then logged as a front collision. The ego was still on the recorded path. Lower speeds on this scene did not fail in single runs.
  - S7: 096988dd at actor_time_shift_s 0, actor_speed_scale 2: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_hybrid_r3_034, cut_in_merge_hybrid_r3_035, cut_in_merge_hybrid_r3_036)
  - S5: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r3_005)
  - S6: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r3_027)
- The failure the policy itself causes in these scenes is a lane drift to the left into a car beside it or passing it, against a STRAIGHT or RIGHT command. It is not a failure to handle a car cutting in.
  - S1: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1.25: 4/4 failed, rate 60%-100% (90%) (cut_in_merge_hybrid_r3_004, cut_in_merge_hybrid_r3_010, cut_in_merge_hybrid_r3_011, cut_in_merge_hybrid_r3_012)
  - S8: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25: 4/4 failed, rate 60%-100% (90%) (cut_in_merge_hybrid_r3_007, cut_in_merge_hybrid_r3_013, cut_in_merge_hybrid_r3_014, cut_in_merge_hybrid_r3_015)
  - S14: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 2: 5/5 failed, rate 65%-100% (90%) (cut_in_merge_hybrid_r3_022, cut_in_merge_hybrid_r3_023, cut_in_merge_hybrid_r3_028, cut_in_merge_hybrid_r3_029, cut_in_merge_hybrid_r3_030)
  - S23: 19f339ba at actor_time_shift_s 0, actor_speed_scale 2: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_hybrid_r3_046, cut_in_merge_hybrid_r3_047, cut_in_merge_hybrid_r3_048)
  - S22: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.5: 1/2 failed, rate 12%-88% (90%) (cut_in_merge_hybrid_r3_041, cut_in_merge_hybrid_r3_042)
- 054b5901 produced no policy failures at any speed tested. At 1.5x, replayed car 16 drove through the ego from behind at the moment of handoff, the same simulator artifact, and those runs were not scored as failures.
  - S2: 054b5901 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r3_008)
  - S3: 054b5901 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/4 failed, rate 0%-40% (90%) (cut_in_merge_hybrid_r3_018, cut_in_merge_hybrid_r3_019, cut_in_merge_hybrid_r3_020, cut_in_merge_hybrid_r3_021)
  - S4: 054b5901 at actor_time_shift_s 0, actor_speed_scale 2: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_hybrid_r3_037, cut_in_merge_hybrid_r3_038)
- The three scenes where only the marked cut-in car was retimed (0cf6368d, 12855a41, 1c45ce3a) produced no failures at any speed tested. This includes 12855a41 with the car shifted 0.5 s earlier or later.
  - S9: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r3_001)
  - S10: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r3_045)
  - S11: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 2: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_hybrid_r3_052, cut_in_merge_hybrid_r3_053, cut_in_merge_hybrid_r3_054)
  - S15: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r3_043)
  - S16: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r3_002)
  - S17: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r3_025)
  - S18: 12855a41 at actor_time_shift_s 0, actor_speed_scale 2: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_hybrid_r3_031, cut_in_merge_hybrid_r3_032, cut_in_merge_hybrid_r3_033)
  - S19: 12855a41 at actor_time_shift_s 0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r3_044)
  - S20: 12855a41 at actor_time_shift_s 0.5, actor_speed_scale 2: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_hybrid_r3_049, cut_in_merge_hybrid_r3_050, cut_in_merge_hybrid_r3_051)
  - S24: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r3_003)
  - S25: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r3_026)
  - S26: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 2: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_hybrid_r3_039, cut_in_merge_hybrid_r3_040)

## Open

- There is no valid fifth case. S7 on 096988dd fails only because a replayed car drives through the ego from behind. To find a fifth, search the scenes with no confirmed case (054b5901, 0cf6368d, 12855a41, 1c45ce3a) and 096988dd under the policy's control. Timing shifts of ±1 to 2 s and speeds below 1x are untried there.
- Timing was barely explored: every confirmed case is at a 0 s shift, and the only other shifts tried were ±0.5 s on one scene. Runs at -2, -1, +1 and +2 s on the four confirmed scenes would show whether timing matters, beyond car speed.
- No 0.5x speed setting was run anywhere, so the effect of slower cars is unknown.
- S23 and S7 each rest on three runs, so their ranges only just clear one half. Two or three more runs at S23 would firm it up.
- The minimum speed that triggers failure is not settled. 0e899dd3 at 1.25x and 1.5x, and 19f339ba at 1.25x and 1.5x, had only one or two runs each. Repeats there would show where the failures start.
- Replayed cars driving through the ego (096988dd at 2x, 054b5901 at 1.5x) need a fix in the simulator before those settings can say anything about the policy.
- Whether the brief's actual subject, the ego reacting to another car cutting in, causes collisions is not shown. The failures found are the ego's own drift to the left.

## Why the runs failed (triage from the video and log)

turned_into_actor 16, actor_hit_ego 8

- cut_in_merge_hybrid_r3_004: turned_into_actor, policy at fault: yes. On a multi-lane highway with the command STRAIGHT, the policy's planned path (orange) swung left toward the adjacent lane, away from the route (green). The ego steered left into actor 56, which was driving alongside it in that lane. The result was a front/side collision at 6.7 s about 1.1 m off the recorded path; the later rear contact came after this collision.
- cut_in_merge_hybrid_r3_007: turned_into_actor, policy at fault: yes. After the 4.6 s handoff, the ego was cruising at about 8 m/s on the highway. Its plan (orange) bent left toward the next lane, and the ego drifted left into actor 33, which was coming up alongside in that lane, so the ego's front-left corner hit it at 6.2 s. The route command at that moment was RIGHT, and the 25 m gap to the car ahead rules out a rear-end on a lead vehicle.
- cut_in_merge_hybrid_r3_010: turned_into_actor, policy at fault: yes. The route command was STRAIGHT (RIGHT at the final frame), but after handoff the policy began a lane change to the left on the highway. It sped up from 4.2 to 5.8 m/s and cut into the lane where actor 56 was driving alongside it, and its front hit that car.
- cut_in_merge_hybrid_r3_011: turned_into_actor, policy at fault: yes. Traffic was clear ahead, but the policy (orange path) changed lanes to the left. Vehicle 56 was in that lane, slightly behind and then alongside the ego, and the ego's front hit it at 6.7 s.
- cut_in_merge_hybrid_r3_012: turned_into_actor, policy at fault: yes. Right after handoff on a straight multi-lane highway, the policy's plan (orange) veered left toward the next lane while the recorded path went straight. The ego sped up from 4.2 to 5.8 m/s and its front hit vehicle 56, which was driving in the left lane slightly ahead of it.
- cut_in_merge_hybrid_r3_013: turned_into_actor, policy at fault: unclear. On a multi-lane highway the ego held about 8 m/s and stayed well back from the car ahead (gap over 24 m). Car 33 came up from behind in the lane to the left. By 6.2 s the ego had drifted about 0.9 m off the recorded path, apparently to the left, and its front-left overlapped car 33 as it went past, so this is a side-swipe of a passing car, not a lead-vehicle crash. The camera smear at impact is only the close-range reconstruction artifact.
- cut_in_merge_hybrid_r3_014: turned_into_actor, policy at fault: yes. On a multi-lane freeway with the command STRAIGHT, the ego drifted left out of its lane toward the adjacent left lane at about 8 m/s, while the recorded path stayed straight. Vehicle 33 was coming up alongside in that lane, and the ego's front swept into it at 6.2 s.
- cut_in_merge_hybrid_r3_015: turned_into_actor, policy at fault: yes. On a multi-lane highway at about 8 m/s, the policy took over at 4.6 s. Its planned path then swung left toward the adjacent lane while the recorded human path stayed straight in the lane, and the command later changed to RIGHT. At 6.2 s the ego's front-left cut into vehicle 33, which was alongside it in the left lane, causing a front collision.
- cut_in_merge_hybrid_r3_018: actor_hit_ego, policy at fault: no. At 3.7s, actor 16 was right behind the ego in the same lane. By 4.7s it had driven up into and over the ego's footprint, so its box overlaps the ego's front and the camera shows it as a smeared car right in front. The ego was still exactly on the recorded human path (0.0 m off) and the failure fell on the handoff instant, so the policy had no chance to act. This looks like a replayed actor overtaking through the ego, which got scored as a front collision.
- cut_in_merge_hybrid_r3_019: actor_hit_ego, policy at fault: no. At 3.7 s, actor 16 was directly behind the ego in the same lane. By 4.7 s it had driven into and through the ego, so it overlapped the ego's front, which registered as a front collision. The ego was still on the recorded human path (0.0 m off) and slowing slightly, and the failure came at the handoff moment (4.7 s), so the policy never had control.
- cut_in_merge_hybrid_r3_020: actor_hit_ego, policy at fault: no. At 3.7 s, actor 16 is directly behind the ego in the same lane, and by 4.7 s it overlaps the ego's front: the replayed actor drove up through the ego from behind. The ego was still exactly on the recorded human path (0.0 m off) at about 14 m/s. The front contact was logged at 4.7 s, the same moment the policy took over, so the policy had no chance to act.
- cut_in_merge_hybrid_r3_021: actor_hit_ego, policy at fault: no. At 3.7s actor 16 was directly behind the ego. By 4.7s, the handoff moment, it had moved up through the ego and overlapped its front, which counted as a front collision. The ego was still exactly on the recorded human path (0 m off) at about 14 m/s, so the policy had no time in control and this looks like an actor-replay artifact, not a policy mistake.
- cut_in_merge_hybrid_r3_022: turned_into_actor, policy at fault: yes. On a multi-lane highway the route command switched from STRAIGHT to RIGHT, and the human driver moved right, but the ego stayed on the left side of its lane and its planned path bent left toward actor 23, which was slower and just ahead-left. Actor 23 was also closing toward the ego's lane. The ego slowed to about 3 m/s but its front still clipped 23. The recorded ego position ends up about 1.5 m to the right. Rear contact from a following car came only after this collision.
- cut_in_merge_hybrid_r3_023: turned_into_actor, policy at fault: yes. On a crowded multi-lane highway the ego slowed from 6.5 to 3.3 m/s, but its output path (orange) veered left toward the next lane instead of following the route, even though the command was STRAIGHT and then RIGHT. It cut left into the slower vehicle 23 just ahead-left of it, and its front hit 23 at 7.7 s, about 1.4 m off the recorded human path.
- cut_in_merge_hybrid_r3_028: actor_hit_ego, policy at fault: unclear. On a multi-lane highway, the recorded human drifted right (the command was RIGHT) to make room for actor 23, which was merging in from the left lane. The policy instead stayed in its lane and slowed to about 3 m/s, so the replayed actor 23, which does not react to the ego, cut down onto it and its front-left corner made contact. Actor 21 also hit the ego from behind as it slowed.
- cut_in_merge_hybrid_r3_029: turned_into_actor, policy at fault: yes. In slow freeway traffic, the ego's plan bent left, away from the recorded path, even though the command was STRAIGHT and then RIGHT. The ego drifted into the left lane and its front hit vehicle 23 at about 3 m/s; it slowed but did not hold its lane. The left-side car in the camera view was heavily smeared, which may have contributed, but the policy steered into an occupied lane.
- cut_in_merge_hybrid_r3_030: turned_into_actor, policy at fault: yes. After handoff on a multi-lane highway, the human driver moved right, but the policy's plan (orange) angled left toward actor 23 in the adjacent left lane. The ego edged onto the lane line and, slowing only gradually from 3.8 to 3.0 m/s, its front hit 23 as the gap closed from 7.7 m to 4.2 m.
- cut_in_merge_hybrid_r3_034: actor_hit_ego, policy at fault: no. The ego was still replaying the recorded path on the highway (0.0 m off the recording) when actor 9 came up from behind and hit its rear at 3.7 s, before the policy took over. By 4.7 s, the moment of handoff, actor 9 had driven right through the ego and overlapped it, so a front collision was logged even though nothing ahead was within about 40 m just before.
- cut_in_merge_hybrid_r3_035: actor_hit_ego, policy at fault: no. At 3.7s, before the policy took over, the ego was replaying the recorded trajectory in its lane when actor 9 came up from behind and hit its rear (collision_rear = 1). Actor 9 then kept driving through the ego, and at handoff (4.7s) it overlapped the ego's front, so the run was flagged as a front collision at fault even though the ego had just been rear-ended.
- cut_in_merge_hybrid_r3_036: actor_hit_ego, policy at fault: no. The ego was still replaying the recorded trajectory, 0.0 m off it, at about 5.5 m/s in its highway lane. Replayed actor 9 came up from behind and hit the ego's rear by 3.7 s, then drove through and on top of the ego box, so by 4.7 s, the handoff moment, the overlap also counted as a front collision. The road ahead was clear, with the nearest lead about 40 m away.
- cut_in_merge_hybrid_r3_041: turned_into_actor, policy at fault: yes. On a multi-lane highway with a STRAIGHT command, the ego slowed to about 4 m/s and drifted left until it was straddling the lane line, and its planned path kept bending further left. A small actor (29), probably passing in the left lane, came up at the ego's front-left corner and the ego's front clipped it at 12.1s.
- cut_in_merge_hybrid_r3_046: turned_into_actor, policy at fault: yes. After the policy took over at 4.6s on the highway, it slowed hard for no reason (16.9 to 10.3 m/s, with nothing ahead closer than about 50 m) and planned a path that drifted left, away from the recorded path, which bears right (the command changes to RIGHT by 6.3s). At 6.3s the ego crossed the left lane line and its left side hit actor 24, which was coming up in the adjacent left lane. The braking with nothing ahead probably also explains the rear contact.
- cut_in_merge_hybrid_r3_047: turned_into_actor, policy at fault: yes. After the 4.6s handoff on a multi-lane highway, the ego braked hard (16.9 → 10.3 m/s) with no lead close ahead. It also drifted left onto the lane line, while the recorded path stayed in the lane and bent right. Vehicle 24 was passing in the adjacent left lane, and the ego's left side hit it at 6.3s (a lateral collision).
- cut_in_merge_hybrid_r3_048: turned_into_actor, policy at fault: yes. After handoff on a straight multi-lane highway, the policy braked hard for no visible reason (17 to 10 m/s; the nearest car ahead was 40–50 m away) and steered left off the recorded path. Its plan bent toward the next lane to the left. The ego's front-left crossed the lane line and side-swiped actor 24, which was coming up from behind in that lane, about 1.3 m left of where the human drove.

## Every setting

- S1: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1.25: 4/4 failed, rate 60%-100% (90%) (cut_in_merge_hybrid_r3_004, cut_in_merge_hybrid_r3_010, cut_in_merge_hybrid_r3_011, cut_in_merge_hybrid_r3_012)
- S2: 054b5901 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r3_008)
- S3: 054b5901 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/4 failed, rate 0%-40% (90%) (cut_in_merge_hybrid_r3_018, cut_in_merge_hybrid_r3_019, cut_in_merge_hybrid_r3_020, cut_in_merge_hybrid_r3_021)
- S4: 054b5901 at actor_time_shift_s 0, actor_speed_scale 2: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_hybrid_r3_037, cut_in_merge_hybrid_r3_038)
- S5: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r3_005)
- S6: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r3_027)
- S7: 096988dd at actor_time_shift_s 0, actor_speed_scale 2: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_hybrid_r3_034, cut_in_merge_hybrid_r3_035, cut_in_merge_hybrid_r3_036)
- S8: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25: 4/4 failed, rate 60%-100% (90%) (cut_in_merge_hybrid_r3_007, cut_in_merge_hybrid_r3_013, cut_in_merge_hybrid_r3_014, cut_in_merge_hybrid_r3_015)
- S9: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r3_001)
- S10: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r3_045)
- S11: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 2: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_hybrid_r3_052, cut_in_merge_hybrid_r3_053, cut_in_merge_hybrid_r3_054)
- S12: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_hybrid_r3_009, cut_in_merge_hybrid_r3_016)
- S13: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_hybrid_r3_017, cut_in_merge_hybrid_r3_024)
- S14: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 2: 5/5 failed, rate 65%-100% (90%) (cut_in_merge_hybrid_r3_022, cut_in_merge_hybrid_r3_023, cut_in_merge_hybrid_r3_028, cut_in_merge_hybrid_r3_029, cut_in_merge_hybrid_r3_030)
- S15: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r3_043)
- S16: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r3_002)
- S17: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r3_025)
- S18: 12855a41 at actor_time_shift_s 0, actor_speed_scale 2: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_hybrid_r3_031, cut_in_merge_hybrid_r3_032, cut_in_merge_hybrid_r3_033)
- S19: 12855a41 at actor_time_shift_s 0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r3_044)
- S20: 12855a41 at actor_time_shift_s 0.5, actor_speed_scale 2: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_hybrid_r3_049, cut_in_merge_hybrid_r3_050, cut_in_merge_hybrid_r3_051)
- S21: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r3_006)
- S22: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.5: 1/2 failed, rate 12%-88% (90%) (cut_in_merge_hybrid_r3_041, cut_in_merge_hybrid_r3_042)
- S23: 19f339ba at actor_time_shift_s 0, actor_speed_scale 2: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_hybrid_r3_046, cut_in_merge_hybrid_r3_047, cut_in_merge_hybrid_r3_048)
- S24: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r3_003)
- S25: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r3_026)
- S26: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 2: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_hybrid_r3_039, cut_in_merge_hybrid_r3_040)

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
- Only the three scenes with a marked cut-in car can isolate it.). Report written by claude-opus-5-5 from `results` in 32 s; every count above is computed from the queue, not written by the model.

54 of 54 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
