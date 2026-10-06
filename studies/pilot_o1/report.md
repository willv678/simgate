# How does the policy's failure rate on each candidate scene change with planner delay in microseconds (camera frame to the controller receiving the plan made from it)? Find the fragile scenes and roughly where each breaks.

Study `pilot_o1`: 15 kept runs on 4 scenes, varying planner_delay_us; 0 runs not kept by the gate. Counts are kept runs only.

## Answer

Of the 8 candidate scenes, only one shows a failure pattern that tracks planner delay: clipgt-02eadd92. On that scene the policy passed 3 of 3 runs at 0–100 ms and failed 5 of 5 at 150–400 ms, so it appears to break somewhere between 100 and 150 ms. Every one of those failures is the policy not braking for, or steering into, a car slowing at a red light. Each delay setting has only one or two runs, though, so this break point is a hint rather than a measured rate: at 100 ms the 90% range on the failure rate reaches 0.58, and at 150 ms it starts at 0.42. Two other scenes also fail with no added delay, so they are not delay-fragile in any sense this study can show:
- clipgt-01d503d4 failed 4 of 4 runs at 0–200 ms. In three of those, whether the policy was at fault is unclear, and in two of the three a replayed car cut into the ego's lane.
- clipgt-026d6a39 failed 1 of 1 run at 0 ms by driving off the road. That run is flagged as a possible simulator artifact, although the video review found the camera view doesn't explain the mistake.
On clipgt-023b7fcc the policy passed at 200 ms, failed at 300 ms and passed at 400 ms, one run each, which is no clear trend. The remaining four scenes were never run.

## Findings

- clipgt-02eadd92 is the one scene whose failures line up with delay. It passed every run at 0 and 100 ms (3 runs in total) and failed every run at 150, 200 and 400 ms (4 runs in total), which puts its break roughly between 100 and 150 ms. Each setting has only one or two runs.
  - S8: 02eadd92 at planner_delay_us 0: 0/1 failed, rate 0%-73% (90%) (o1_009)
  - S9: 02eadd92 at planner_delay_us 100000: 0/2 failed, rate 0%-58% (90%) (o1_006, o1_013)
  - S10: 02eadd92 at planner_delay_us 150000: 2/2 failed, rate 42%-100% (90%), 1 possibly the simulator's (o1_011, o1_012)
  - S11: 02eadd92 at planner_delay_us 200000: 1/1 failed, rate 27%-100% (90%) (o1_003)
  - S12: 02eadd92 at planner_delay_us 400000: 1/1 failed, rate 27%-100% (90%) (o1_004)
- All four failures on clipgt-02eadd92 were the policy's fault, and they look alike. In each, the ego was in the lane left of the recorded path, only eased off while a car ahead slowed for a red light, and either rear-ended it or steered into it. One of the runs at 150 ms is flagged as a possible artifact (the ego was more than 3.5 m off the recorded trajectory), but the video review says the lead car was clearly visible before the crash.
  - S10: 02eadd92 at planner_delay_us 150000: 2/2 failed, rate 42%-100% (90%), 1 possibly the simulator's (o1_011, o1_012)
  - S11: 02eadd92 at planner_delay_us 200000: 1/1 failed, rate 27%-100% (90%) (o1_003)
  - S12: 02eadd92 at planner_delay_us 400000: 1/1 failed, rate 27%-100% (90%) (o1_004)
- clipgt-01d503d4 fails even with no added delay: it failed 2 of 2 runs at 0 ms and 1 of 1 at each of 100 and 200 ms. So delay is not what makes it fail. In 3 of the 4 failures it is unclear whether the policy was at fault: in two, actor 27 cut into the ego's lane in slow traffic, and in one the collision happened before the clip starts. Only the 100 ms run is a clear policy fault (the ego drifted left into a car beside it).
  - S1: 01d503d4 at planner_delay_us 0: 2/2 failed, rate 42%-100% (90%) (o1_010, o1_014)
  - S2: 01d503d4 at planner_delay_us 100000: 1/1 failed, rate 27%-100% (90%) (o1_007)
  - S3: 01d503d4 at planner_delay_us 200000: 1/1 failed, rate 27%-100% (90%) (o1_001)
- clipgt-026d6a39 failed its only run, at 0 ms. The policy started one lane off the recorded path and drove over the curb. This run is flagged as a possible artifact because the ego ended about 8 m off the recorded path, but the video review judged it the policy's fault because the road ahead was clearly visible. Delay was never varied on this scene.
  - S7: 026d6a39 at planner_delay_us 0: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (o1_005)
- clipgt-023b7fcc shows no clear trend with delay. It passed at 200 ms, failed at 300 ms by rear-ending a slower car, and passed at 400 ms, with one run at each setting.
  - S4: 023b7fcc at planner_delay_us 200000: 0/1 failed, rate 0%-73% (90%) (o1_002)
  - S5: 023b7fcc at planner_delay_us 300000: 1/1 failed, rate 27%-100% (90%) (o1_015)
  - S6: 023b7fcc at planner_delay_us 400000: 0/1 failed, rate 0%-73% (90%) (o1_008)

## Open

- Exactly where clipgt-02eadd92 breaks. Repeat runs (about 5 each) at 100, 125 and 150 ms would narrow it down; at the moment the range rests on 2 runs at 100 ms and 2 at 150 ms.
- Whether clipgt-01d503d4 really fails at its baseline because of the policy, or because of the replayed cut-in by actor 27. More runs at 0 ms, with triage of who caused each contact, would settle this. Delay can't be studied on this scene until its baseline is understood.
- Whether clipgt-026d6a39 fails reliably at 0 ms, and how it behaves with added delay. Its only run is a single failure that may be a simulator artifact; repeat runs at 0 ms and a few delays would settle it.
- Whether clipgt-023b7fcc is sensitive to delay at all. It needs several runs each at 200, 300 and 400 ms.
- Four scenes were never run: clipgt-0245ff75, clipgt-02e075b9, clipgt-032b6f21 and clipgt-04394343. Each needs at least one run at 0 ms and one at about 200 ms before anyone can say whether it is fragile.

## Why the runs failed (triage from the video and log)

no_brake_for_lead 4, actor_hit_ego 2, turned_into_actor 2, left_road 1, other 1

- o1_001: actor_hit_ego, policy at fault: unclear. The ego was creeping straight at about 2.7 m/s in slow highway traffic. Actor 27, in the next lane to the left and slightly ahead, angled into the ego's lane, and the ego's front corner hit its rear right side. The ego kept its speed and stayed about 1 m off the recorded human path, which may have placed it where the replayed cut-in would reach it; braking or yielding might have avoided the contact.
- o1_003: no_brake_for_lead, policy at fault: yes. Approaching a red light about 3 m to the left of the recorded human path, the ego followed actor 22, which was slowing to a near stop in its lane. The ego braked only gently (8.7 to 4.4 m/s while the gap closed from 26 m to 4.5 m) and rear-ended it.
- o1_004: turned_into_actor, policy at fault: yes. Going STRAIGHT toward a red light, the ego drifted left of the human's path (1.7 m off) and its planned path pointed into the neighbouring lane, where car 22 was slowing for the light. The ego braked only gently (9.0 to 6.2 m/s) while the gap closed from 28.5 m to 4.5 m, and its front hit the rear right corner of car 22.
- o1_005: left_road, policy at fault: yes. The ego started one lane to the left of the recorded human path. It drove straight across the intersection at about 9.5 m/s with no actors nearby, and its plan bent further left, so it never followed the recorded path (it ended about 8 m off). It ran over the curb at the far corner and left the drivable area. The ground in the camera view was smeared, but the road ahead and the buildings were clear before the failure, so the bad camera view doesn't explain the mistake.
- o1_007: turned_into_actor, policy at fault: yes. In slow highway traffic at about 3 m/s, the ego drifted left of the recorded path, about 1.2 m off by the end, even though the route command had changed to RIGHT. Its side hit vehicle 27, which was travelling alongside in the adjacent left lane. The lead vehicle stayed about 16 m ahead the whole time, so this was not a following problem.
- o1_010: actor_hit_ego, policy at fault: unclear. The ego was crawling straight in its lane at about 2.5 m/s in slow highway traffic, staying close to the recorded path (0.8 m off). Actor 27, just ahead-left, cut into the ego's lane and moved across the ego's front corner, which logged as a front collision; the vehicle 20 m ahead was never involved. The ego eased off only slightly (2.7 to 2.3 m/s) and did not yield hard to the merging car, so it may share some blame.
- o1_011: no_brake_for_lead, policy at fault: yes. The route said turn right, but the ego stayed about one lane left of the recorded path, which put it behind car 22. That car was slowing to a stop at a red light, and the ego only eased off gradually (8.3 → 4.4 m/s while the gap shrank from 17 m to 4 m), so it ran into the car's rear at about 4 m/s. The lead car was clearly visible in the camera until it got close, and the smearing there only shows up near the impact.
- o1_012: no_brake_for_lead, policy at fault: yes. The ego was in the lane left of the recorded human path (about 3 m off it) and approaching a red light, with car 22 nearly stopped ahead in the same lane. Over 3 s the ego only eased off from 8.5 to 3.9 m/s while the gap shrank from 24 m to 4.4 m, its planned path ran straight through car 22, and it hit car 22's rear.
- o1_014: other, policy at fault: unclear. The frames don't show the collision. The front-collision counter already reads 1.00 at 8.5s and the per-step value is 0 in every frame, so the contact happened before the clip starts. During the clip the ego slows from 2.1 to 1.2 m/s on a congested multi-lane road, stays about 16 m behind truck 18, and falls further behind the recorded human position (up to 4.2 m). Its planned path keeps hooking left toward vehicle 27 alongside, so a front-corner contact with 27 is possible, but I can't confirm the actor or who caused it.
- o1_015: no_brake_for_lead, policy at fault: yes. The route wanted the ego to keep right (command STRAIGHT, then RIGHT), but its planned path drifted left, off the recorded trajectory, and lined up behind slower vehicle 15. The ego kept going at about 6 m/s and only eased off a little (6.6 to 5.6 m/s) while the gap fell from 12.8 m to 4.6 m, then ran into the back of vehicle 15. The camera smear at the moment of impact doesn't count, because the earlier frames showed the lead car clearly.

## Every setting

- S1: 01d503d4 at planner_delay_us 0: 2/2 failed, rate 42%-100% (90%) (o1_010, o1_014)
- S2: 01d503d4 at planner_delay_us 100000: 1/1 failed, rate 27%-100% (90%) (o1_007)
- S3: 01d503d4 at planner_delay_us 200000: 1/1 failed, rate 27%-100% (90%) (o1_001)
- S4: 023b7fcc at planner_delay_us 200000: 0/1 failed, rate 0%-73% (90%) (o1_002)
- S5: 023b7fcc at planner_delay_us 300000: 1/1 failed, rate 27%-100% (90%) (o1_015)
- S6: 023b7fcc at planner_delay_us 400000: 0/1 failed, rate 0%-73% (90%) (o1_008)
- S7: 026d6a39 at planner_delay_us 0: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (o1_005)
- S8: 02eadd92 at planner_delay_us 0: 0/1 failed, rate 0%-73% (90%) (o1_009)
- S9: 02eadd92 at planner_delay_us 100000: 0/2 failed, rate 0%-58% (90%) (o1_006, o1_013)
- S10: 02eadd92 at planner_delay_us 150000: 2/2 failed, rate 42%-100% (90%), 1 possibly the simulator's (o1_011, o1_012)
- S11: 02eadd92 at planner_delay_us 200000: 1/1 failed, rate 27%-100% (90%) (o1_003)
- S12: 02eadd92 at planner_delay_us 400000: 1/1 failed, rate 27%-100% (90%) (o1_004)

## Provenance

Plan: `plan.json` (rationale: fixed by the pilot script (run_pilot.sh), not planned from a brief). Report written by claude-opus-5-5 from `results` in 23 s; every count above is computed from the queue, not written by the model.
