# How does the policy's failure rate on each candidate scene change with planner delay in microseconds (camera frame to the controller receiving the plan made from it)? Find the fragile scenes and roughly where each breaks.

Study `pilot_o1`: 15 kept runs on 4 scenes, varying planner_delay_us; 0 runs not kept by the gate. Counts are kept runs only.

## Answer

Only one scene, 02eadd92, looks sensitive to planner delay. It passed every run at 0 and 100 ms and failed every run from 150 ms up. It most likely breaks somewhere between 100 and 150 ms, but each setting has only one or two runs, so this is a strong hint, not a measured rate. Two other scenes fail even with no delay (01d503d4 and 026d6a39), so delay doesn't explain them. A third, 023b7fcc, failed once at 300 ms but passed at 400 ms, so it has no clear breaking point. Four of the eight candidate scenes were never run.

## Findings

- Scene 02eadd92 passed every run at 0 and 100 ms and failed every run at 150, 200 and 400 ms, so it most likely breaks between 100 and 150 ms. With only one or two runs per setting, the ranges at 0 and 100 ms still allow a substantial failure rate.
  - S8: 02eadd92 at planner_delay_us 0: 0/1 failed, rate 0%-73% (90%) (o1_009)
  - S9: 02eadd92 at planner_delay_us 100000: 0/2 failed, rate 0%-58% (90%) (o1_006, o1_013)
  - S10: 02eadd92 at planner_delay_us 150000: 2/2 failed, rate 42%-100% (90%), 1 possibly the simulator's (o1_011, o1_012)
  - S11: 02eadd92 at planner_delay_us 200000: 1/1 failed, rate 27%-100% (90%) (o1_003)
  - S12: 02eadd92 at planner_delay_us 400000: 1/1 failed, rate 27%-100% (90%) (o1_004)
- The failures on 02eadd92 were the policy's fault, and the same thing happened each time. The ego sat about one lane left of the recorded path while approaching a red light, braked only gently behind car 22 as it slowed, and rear-ended it or hit its corner. One run at 150 ms was flagged as a possible simulator artifact because the ego was over 3.5 m off the recorded path. Its triage found the camera view clear until just before impact, so the artifact doesn't explain the crash, and the other run at 150 ms failed the same way without the flag.
  - S10: 02eadd92 at planner_delay_us 150000: 2/2 failed, rate 42%-100% (90%), 1 possibly the simulator's (o1_011, o1_012)
  - S11: 02eadd92 at planner_delay_us 200000: 1/1 failed, rate 27%-100% (90%) (o1_003)
  - S12: 02eadd92 at planner_delay_us 400000: 1/1 failed, rate 27%-100% (90%) (o1_004)
- Scene 01d503d4 failed at every delay tested, including 0 ms, so its failures don't come from delay. It is slow highway traffic where actor 27, in the next lane, cuts in or runs alongside. In two failures (0 and 200 ms) the actor hit the ego, and it is unclear whether the policy was at fault. A third failure at 0 ms has no visible collision and its cause is unclear. Only the 100 ms failure, where the ego drifted left into car 27, is clearly the policy's.
  - S1: 01d503d4 at planner_delay_us 0: 2/2 failed, rate 42%-100% (90%) (o1_010, o1_014)
  - S2: 01d503d4 at planner_delay_us 100000: 1/1 failed, rate 27%-100% (90%) (o1_007)
  - S3: 01d503d4 at planner_delay_us 200000: 1/1 failed, rate 27%-100% (90%) (o1_001)
- Scene 026d6a39 failed at 0 ms, its only setting. The ego started one lane left of the recorded path, kept bending further left, and drove over a curb with no actors nearby (policy at fault). The run was flagged as a possible artifact because the ego ended about 8 m off the recorded path, but triage found the road ahead clear before the failure.
  - S7: 026d6a39 at planner_delay_us 0: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (o1_005)
- Scene 023b7fcc shows no consistent trend with delay. It passed at 200 and 400 ms and failed at 300 ms, where the ego drifted left behind a slower vehicle and didn't brake enough (policy at fault). Each of these settings has a single run.
  - S4: 023b7fcc at planner_delay_us 200000: 0/1 failed, rate 0%-73% (90%) (o1_002)
  - S5: 023b7fcc at planner_delay_us 300000: 1/1 failed, rate 27%-100% (90%) (o1_015)
  - S6: 023b7fcc at planner_delay_us 400000: 0/1 failed, rate 0%-73% (90%) (o1_008)
- Across the scenes, almost every failure the policy caused followed the same pattern: the ego drifted or sat left of the recorded path and then braked too weakly for a slowing car ahead.
  - S2: 01d503d4 at planner_delay_us 100000: 1/1 failed, rate 27%-100% (90%) (o1_007)
  - S5: 023b7fcc at planner_delay_us 300000: 1/1 failed, rate 27%-100% (90%) (o1_015)
  - S7: 026d6a39 at planner_delay_us 0: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (o1_005)
  - S10: 02eadd92 at planner_delay_us 150000: 2/2 failed, rate 42%-100% (90%), 1 possibly the simulator's (o1_011, o1_012)
  - S11: 02eadd92 at planner_delay_us 200000: 1/1 failed, rate 27%-100% (90%) (o1_003)
  - S12: 02eadd92 at planner_delay_us 400000: 1/1 failed, rate 27%-100% (90%) (o1_004)

## Open

- Scenes 0245ff75, 02e075b9, 032b6f21 and 04394343 were never run, so whether they are fragile is unknown. Sweeping each from 0 to 400 ms would settle it.
- Exactly where 02eadd92 breaks: repeated runs (about 5 per setting) at 100, 125 and 150 ms would narrow the threshold and confirm that the scene passes at 0 and 100 ms.
- Whether delay affects 01d503d4 at all: the scene fails at 0 ms, and most of its failures are cut-ins by actor 27 where the policy's fault is unclear. Repeated runs at 0 ms and at higher delays, plus checking how the replayed cut-in plays out, would show whether the scene is a usable test.
- Whether 023b7fcc's single failure at 300 ms is noise or a real effect of delay: repeated runs at 200, 300 and 400 ms would tell.
- 026d6a39 was run only at 0 ms. More runs there, and at higher delays, would show whether it always leaves the road and whether the flagged camera smearing plays any part.

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

Plan: `plan.json` (rationale: fixed by the pilot script (run_pilot.sh), not planned from a brief). Report written by claude-opus-5-5 from `results` in 20 s; every count above is computed from the queue, not written by the model.
