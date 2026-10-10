# In merge and cut-in scenes, which timings and speeds of the other cars make the VaVAM policy collide or leave the road? Find the 5 most challenging settings, each on a different scene and confirmed by repeats.

Study `hybrid_r3`: 36 kept runs on 9 scenes, varying actor_time_shift_s, actor_speed_scale; 0 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 5 of 5 challenging settings confirmed, after 4 rounds.

## Answer

The study's code counts its goal as met, with five settings confirmed on five scenes. However, only three of them show the policy itself failing: S1 and S7 (all cars at 1.25x speed) and S11 (all cars at 2x). In each of these the ego drifts left into a car beside it in the next lane, even though its command is STRAIGHT or RIGHT. The other two confirmed settings, S3 (1.5x) and S6 (2x), fail only because a replayed car drives through the ego from behind at or before the handoff. The ego is still on the recorded path at that point, so those failures come from the replay, not the policy. Every failure happened with no time shift. Timing was never varied, so the study says nothing about how earlier or later cars change the outcome. With only three to five runs per setting, each confirmed case is surely above one half, but the exact rates are loose.

## Findings

- The study's main finding is one policy failure that shows up on three scenes. When the recorded cars are sped up, the policy's plan bends left and the ego drifts into a car beside it in the next lane, against a STRAIGHT or RIGHT command. This is the ego leaving its lane, not another car cutting in.
  - S1: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1.25: 4/4 failed, rate 60%-100% (90%) (cut_in_merge_hybrid_r3_004, cut_in_merge_hybrid_r3_010, cut_in_merge_hybrid_r3_011, cut_in_merge_hybrid_r3_012)
  - S7: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25: 4/4 failed, rate 60%-100% (90%) (cut_in_merge_hybrid_r3_007, cut_in_merge_hybrid_r3_013, cut_in_merge_hybrid_r3_014, cut_in_merge_hybrid_r3_015)
  - S11: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 2: 5/5 failed, rate 65%-100% (90%) (cut_in_merge_hybrid_r3_022, cut_in_merge_hybrid_r3_023, cut_in_merge_hybrid_r3_028, cut_in_merge_hybrid_r3_029, cut_in_merge_hybrid_r3_030)
- On scene 023b7fcc (S1) and scene 09a95ffa (S7), every run with all cars at 1.25x speed failed this way. Triage blames the policy in every run, except one at S7 where fault was unclear.
  - S1: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1.25: 4/4 failed, rate 60%-100% (90%) (cut_in_merge_hybrid_r3_004, cut_in_merge_hybrid_r3_010, cut_in_merge_hybrid_r3_011, cut_in_merge_hybrid_r3_012)
  - S7: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25: 4/4 failed, rate 60%-100% (90%) (cut_in_merge_hybrid_r3_007, cut_in_merge_hybrid_r3_013, cut_in_merge_hybrid_r3_014, cut_in_merge_hybrid_r3_015)
- On scene 0e899dd3, all cars at 2x speed failed every run, while 1.25x and 1.5x passed every run. Most of the 2x failures were the ego turning into the slower car ahead-left of it. In one run, that car merged down onto the ego, and fault was unclear.
  - S9: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_hybrid_r3_009, cut_in_merge_hybrid_r3_016)
  - S10: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_hybrid_r3_017, cut_in_merge_hybrid_r3_024)
  - S11: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 2: 5/5 failed, rate 65%-100% (90%) (cut_in_merge_hybrid_r3_022, cut_in_merge_hybrid_r3_023, cut_in_merge_hybrid_r3_028, cut_in_merge_hybrid_r3_029, cut_in_merge_hybrid_r3_030)
- The confirmed cases on scene 054b5901 (1.5x) and scene 096988dd (2x) are not the policy's fault. In every run, a sped-up replayed car came from behind and drove through the ego at or before the 4.7 s handoff, while the ego was still exactly on the recorded path. The artifact flag missed these because the ego had not left its track. For these two scenes, no real policy failure has been found.
  - S3: 054b5901 at actor_time_shift_s 0, actor_speed_scale 1.5: 4/4 failed, rate 60%-100% (90%) (cut_in_merge_hybrid_r3_018, cut_in_merge_hybrid_r3_019, cut_in_merge_hybrid_r3_020, cut_in_merge_hybrid_r3_021)
  - S6: 096988dd at actor_time_shift_s 0, actor_speed_scale 2: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_hybrid_r3_034, cut_in_merge_hybrid_r3_035, cut_in_merge_hybrid_r3_036)
- The scene with a marked cut-in car that got the most runs, 12855a41, held up at every speed tried. At 2x, no run failed and the failure rate is surely below one half. The two other marked cut-in scenes, 0cf6368d and 1c45ce3a, passed at the speeds tried, but each setting there had only one run.
  - S12: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r3_002)
  - S13: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r3_025)
  - S14: 12855a41 at actor_time_shift_s 0, actor_speed_scale 2: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_hybrid_r3_031, cut_in_merge_hybrid_r3_032, cut_in_merge_hybrid_r3_033)
  - S8: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r3_001)
  - S16: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r3_003)
  - S17: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r3_026)
- Scene 19f339ba passed its only run, at 1.25x, without coming close to a collision. That is one run, not a rate.
  - S15: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r3_006)

## Open

- Timing was never varied: every run used no time shift. Runs at -2 s to +2 s are needed to say which timings cause collisions.
- No setting was run at the recorded speed (1.0x) in replay. Without it, we can't tell whether the 1.25x speed-up causes the left drift at S1 and S7 or whether those scenes fail anyway. Repeats at 1.0x on 023b7fcc and 09a95ffa would settle this.
- Two of the five confirmed cases (S3, S6) come from the replay, not the policy. To fill those two slots with real policy failures, try settings on 054b5901 and 096988dd that don't send a following car through the ego, such as 0.5x to 1x speed or time shifts. Alternatively, search the scenes not yet tested enough: 0cf6368d, 1c45ce3a and 19f339ba.
- Near misses worth probing: 096988dd at 1.5x (S5), 12855a41 at 1.5x (S13) and 054b5901 at 1.25x (S2). Each had a single run.
- The gate's validity checks should flag failures where a replayed car passes through the ego before handoff, so they don't count toward the goal.

## Why the runs failed (triage from the video and log)

turned_into_actor 12, actor_hit_ego 8

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

## Every setting

- S1: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1.25: 4/4 failed, rate 60%-100% (90%) (cut_in_merge_hybrid_r3_004, cut_in_merge_hybrid_r3_010, cut_in_merge_hybrid_r3_011, cut_in_merge_hybrid_r3_012)
- S2: 054b5901 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r3_008)
- S3: 054b5901 at actor_time_shift_s 0, actor_speed_scale 1.5: 4/4 failed, rate 60%-100% (90%) (cut_in_merge_hybrid_r3_018, cut_in_merge_hybrid_r3_019, cut_in_merge_hybrid_r3_020, cut_in_merge_hybrid_r3_021)
- S4: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r3_005)
- S5: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r3_027)
- S6: 096988dd at actor_time_shift_s 0, actor_speed_scale 2: 3/3 failed, rate 53%-100% (90%) (cut_in_merge_hybrid_r3_034, cut_in_merge_hybrid_r3_035, cut_in_merge_hybrid_r3_036)
- S7: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25: 4/4 failed, rate 60%-100% (90%) (cut_in_merge_hybrid_r3_007, cut_in_merge_hybrid_r3_013, cut_in_merge_hybrid_r3_014, cut_in_merge_hybrid_r3_015)
- S8: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r3_001)
- S9: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_hybrid_r3_009, cut_in_merge_hybrid_r3_016)
- S10: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_hybrid_r3_017, cut_in_merge_hybrid_r3_024)
- S11: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 2: 5/5 failed, rate 65%-100% (90%) (cut_in_merge_hybrid_r3_022, cut_in_merge_hybrid_r3_023, cut_in_merge_hybrid_r3_028, cut_in_merge_hybrid_r3_029, cut_in_merge_hybrid_r3_030)
- S12: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r3_002)
- S13: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r3_025)
- S14: 12855a41 at actor_time_shift_s 0, actor_speed_scale 2: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_hybrid_r3_031, cut_in_merge_hybrid_r3_032, cut_in_merge_hybrid_r3_033)
- S15: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r3_006)
- S16: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r3_003)
- S17: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_r3_026)

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
- Only the three scenes with a marked cut-in car can isolate it.). Report written by claude-opus-5-5 from `results` in 21 s; every count above is computed from the queue, not written by the model.

36 of 36 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
