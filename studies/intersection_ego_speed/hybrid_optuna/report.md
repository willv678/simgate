# At intersections with a recorded crossing car, which combinations of the ego's speed at hand-off and the crossing car's arrival time make VaVAM with the linear MPC collide or leave the road? The goal is the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `hybrid_optuna`: 49 kept runs on 6 scenes, varying ego_speed_scale, actor_time_shift_s; 0 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 2 of 5 challenging settings confirmed, after 7 rounds.

## Answer

The goal was not met. Only two challenging settings were confirmed, both at the top of the speed range with the crossing car 2 s late: scene 02eadd92 at 1.4x and +2 s (S4), and scene 054b5901 at 1.4x and +2 s (S9). The two fail in different ways. In 02eadd92, the ego ignores its RIGHT command, drifts into the left lanes and hits the retimed bus 127 head-on, so the crossing actor's timing does matter there. In 054b5901 the ego runs onto the median island, and the crossing car is never involved. Every 1.4x run on 054b5901 failed, whatever the timing, so speed rather than timing seems to drive that scene. The objective said to ignore failures unrelated to the crossing car, so S9 is a weak case. Every failure is flagged as a possible artifact because the ego ended more than 3.5 m off the recording. Triage blames the policy's leftward drift, not rendering. Still, above 1.0x the ego starts off the recording, so the simulator's share can't be fully ruled out.

## Findings

- On scene 02eadd92, every run at 1.4x speed with the crossing bus 2 s late failed. In each one the ego ignored its RIGHT command, drifted into the left lanes and hit bus 127 (the retimed crossing actor) with its front while slowing only gently. The policy was at fault.
  - S4: 02eadd92 at ego_speed_scale 1.4, actor_time_shift_s 2: 4/4 failed, rate 60%-100% (90%), 4 possibly the simulator's (intersection_ego_speed_hybrid_optuna_018, intersection_ego_speed_hybrid_optuna_022, intersection_ego_speed_hybrid_optuna_023, intersection_ego_speed_hybrid_optuna_024)
- On scene 02eadd92, failures also appear at 1.2x: once with the bus 2 s early (a road departure toward the corner curb) and in the single run with it 1.5 s late (a head-on hit with the bus). The 1.2x/-2 s setting failed only rarely over its repeats. The 1.4x/+1 s setting passed its one run. Single runs are hints only.
  - S1: 02eadd92 at ego_speed_scale 1.2, actor_time_shift_s -2: 1/5 failed, rate 5%-56% (90%), 1 possibly the simulator's (intersection_ego_speed_hybrid_optuna_002, intersection_ego_speed_hybrid_optuna_012, intersection_ego_speed_hybrid_optuna_013, intersection_ego_speed_hybrid_optuna_015, intersection_ego_speed_hybrid_optuna_016)
  - S2: 02eadd92 at ego_speed_scale 1.2, actor_time_shift_s 1.5: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_hybrid_optuna_049)
  - S3: 02eadd92 at ego_speed_scale 1.4, actor_time_shift_s 1: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_optuna_048)
- On scene 054b5901, every run at 1.4x failed, whether the crossing car came 2 s early, on time, 0.5 s late or 2 s late. Each failure was the ego drifting left onto the median nose before the stop line, with no collision. Speed, not the crossing car's timing, appears to cause these. The one 1.0x run passed.
  - S9: 054b5901 at ego_speed_scale 1.4, actor_time_shift_s 2: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (intersection_ego_speed_hybrid_optuna_001, intersection_ego_speed_hybrid_optuna_008, intersection_ego_speed_hybrid_optuna_009)
  - S6: 054b5901 at ego_speed_scale 1.4, actor_time_shift_s -2: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_hybrid_optuna_046)
  - S7: 054b5901 at ego_speed_scale 1.4, actor_time_shift_s 0: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_hybrid_optuna_045)
  - S8: 054b5901 at ego_speed_scale 1.4, actor_time_shift_s 0.5: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_hybrid_optuna_047)
  - S5: 054b5901 at ego_speed_scale 1, actor_time_shift_s -1: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_optuna_007)
- Scene 13a9767e never failed, though it had repeated near misses with the crossing car. At 1.0x/+0.5 s it is unlikely to fail often, and 1.2x/+2 s and 1.4x/+1.5 s showed no failures either.
  - S19: 13a9767e at ego_speed_scale 1, actor_time_shift_s 0.5: 0/8 failed, rate 0%-25% (90%) (intersection_ego_speed_hybrid_optuna_031, intersection_ego_speed_hybrid_optuna_032, intersection_ego_speed_hybrid_optuna_036, intersection_ego_speed_hybrid_optuna_037, intersection_ego_speed_hybrid_optuna_038, intersection_ego_speed_hybrid_optuna_039, intersection_ego_speed_hybrid_optuna_043, intersection_ego_speed_hybrid_optuna_044)
  - S20: 13a9767e at ego_speed_scale 1.2, actor_time_shift_s 2: 0/6 failed, rate 0%-31% (90%) (intersection_ego_speed_hybrid_optuna_005, intersection_ego_speed_hybrid_optuna_010, intersection_ego_speed_hybrid_optuna_011, intersection_ego_speed_hybrid_optuna_017, intersection_ego_speed_hybrid_optuna_029, intersection_ego_speed_hybrid_optuna_030)
  - S21: 13a9767e at ego_speed_scale 1.4, actor_time_shift_s 1.5: 0/3 failed, rate 0%-47% (90%) (intersection_ego_speed_hybrid_optuna_014, intersection_ego_speed_hybrid_optuna_025, intersection_ego_speed_hybrid_optuna_026)
  - S18: 13a9767e at ego_speed_scale 0.8, actor_time_shift_s -2: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_optuna_040)
- Scenes 0d76134f, 118a3400 and 1a7b81b8 produced no failures and showed little or no criticality at any setting tried, including 1.4x with large timing shifts. They are unlikely to give the remaining cases.
  - S10: 0d76134f at ego_speed_scale 1, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_optuna_034)
  - S11: 0d76134f at ego_speed_scale 1.4, actor_time_shift_s -2: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_optuna_021)
  - S12: 0d76134f at ego_speed_scale 1.4, actor_time_shift_s -1.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_optuna_003)
  - S13: 0d76134f at ego_speed_scale 1.4, actor_time_shift_s 2: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_optuna_027)
  - S14: 118a3400 at ego_speed_scale 0.8, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_optuna_035)
  - S15: 118a3400 at ego_speed_scale 1, actor_time_shift_s 1: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_optuna_020)
  - S16: 118a3400 at ego_speed_scale 1.4, actor_time_shift_s -1: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_optuna_004)
  - S17: 118a3400 at ego_speed_scale 1.4, actor_time_shift_s 2: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_optuna_028)
  - S22: 1a7b81b8 at ego_speed_scale 0.8, actor_time_shift_s 1.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_optuna_042)
  - S23: 1a7b81b8 at ego_speed_scale 1, actor_time_shift_s 2: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_optuna_006)
  - S24: 1a7b81b8 at ego_speed_scale 1.2, actor_time_shift_s 0.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_optuna_033)
  - S25: 1a7b81b8 at ego_speed_scale 1.4, actor_time_shift_s -1.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_optuna_041)
  - S26: 1a7b81b8 at ego_speed_scale 1.4, actor_time_shift_s 1: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_optuna_019)
- Every failure was flagged as a possible artifact because the ego ended far off the recorded path. Triage reads the drift itself as the policy's mistake: the camera view was intact before the failure, and smearing came only afterwards.
  - S1: 02eadd92 at ego_speed_scale 1.2, actor_time_shift_s -2: 1/5 failed, rate 5%-56% (90%), 1 possibly the simulator's (intersection_ego_speed_hybrid_optuna_002, intersection_ego_speed_hybrid_optuna_012, intersection_ego_speed_hybrid_optuna_013, intersection_ego_speed_hybrid_optuna_015, intersection_ego_speed_hybrid_optuna_016)
  - S2: 02eadd92 at ego_speed_scale 1.2, actor_time_shift_s 1.5: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_hybrid_optuna_049)
  - S4: 02eadd92 at ego_speed_scale 1.4, actor_time_shift_s 2: 4/4 failed, rate 60%-100% (90%), 4 possibly the simulator's (intersection_ego_speed_hybrid_optuna_018, intersection_ego_speed_hybrid_optuna_022, intersection_ego_speed_hybrid_optuna_023, intersection_ego_speed_hybrid_optuna_024)
  - S6: 054b5901 at ego_speed_scale 1.4, actor_time_shift_s -2: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_hybrid_optuna_046)
  - S7: 054b5901 at ego_speed_scale 1.4, actor_time_shift_s 0: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_hybrid_optuna_045)
  - S8: 054b5901 at ego_speed_scale 1.4, actor_time_shift_s 0.5: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_hybrid_optuna_047)
  - S9: 054b5901 at ego_speed_scale 1.4, actor_time_shift_s 2: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (intersection_ego_speed_hybrid_optuna_001, intersection_ego_speed_hybrid_optuna_008, intersection_ego_speed_hybrid_optuna_009)

## Open

- Three of the five required cases were not found. 13a9767e has the strongest near misses, so a denser search around 1.0–1.4x and +0.5 to +2 s with repeats is the best chance for a third scene. 1a7b81b8 shows only weak signals.
- Whether S9 counts as a crossing-car case: rerunning 054b5901 at 1.4x with the crossing car removed, or at 1.1–1.3x across timings, would show whether the median departure depends on the crossing car at all.
- The single-run hints on 02eadd92 need repeats to tell whether the bus collision reaches down to 1.2x and to other bus timings: 1.2x/+1.5 s (S2) and 1.4x/+1 s (S3).
- Whether starting the ego off the recording above 1.0x (rendering during warm-up) contributes to the leftward drift. All confirmed failures are at 1.4x and flagged as possible artifacts. Checking the early frames, or runs at 1.0x with a matching time shift, would separate the simulator's share from the policy's.
- Turning across traffic was not covered: all scenes go straight in the recording.

## Why the runs failed (triage from the video and log)

left_road 7, turned_into_actor 2, other 2, no_brake_for_lead 1

- intersection_ego_speed_hybrid_optuna_001: left_road, policy at fault: yes. The command was RIGHT, but the ego's plan (orange) drifted left of the recorded path and of the lead car 9 while it slowed from 11 to 6 m/s approaching the intersection. It ended up past the left lane edge, at the median island near the stop line, about 7.5 m from where the human drove.
- intersection_ego_speed_hybrid_optuna_008: left_road, policy at fault: yes. On the approach to a signalized intersection, the policy's planned path bent left away from the recorded route, which went straight and then right (command STRAIGHT, then RIGHT). The ego slowed from 14 to 7 m/s and drifted left toward the raised median nose, going off the drivable area about 7.5 m from the human path, with no collision.
- intersection_ego_speed_hybrid_optuna_009: left_road, policy at fault: yes. The ego was approaching a signalized intersection with a RIGHT command, slowing from about 14 to 6.6 m/s behind lead vehicle 9. Instead of holding its lane, it yawed left (the map shows the lane lines tilting away from its heading) and drifted onto the left median island before the stop line, ending up about 7.5 m off the recorded path. That registered as offroad; there was no collision.
- intersection_ego_speed_hybrid_optuna_012: left_road, policy at fault: yes. The route command was RIGHT, but the ego drifted to the far-left edge of the approach and planned a path curving up-left toward the corner curb, not into the right turn. It slowed from 8.8 to 5.0 m/s and went off the road at 12.2 s, 15.6 m from where the human drove. The camera smearing appears only after the ego has already strayed far from the recorded path, so it looks like a result of the mistake, not the cause.
- intersection_ego_speed_hybrid_optuna_018: turned_into_actor, policy at fault: yes. With a RIGHT command, the ego drifted left of its route into the left lanes, ending up 7.4 m from the recorded human path. There it drove into bus 127, which was turning through the intersection into those lanes toward the ego. The ego slowed only gradually (10 to 6.3 m/s) and hit the bus with its front at 9.8 s.
- intersection_ego_speed_hybrid_optuna_022: no_brake_for_lead, policy at fault: yes. The route said RIGHT, but the policy kept going straight in a left lane, about 7.5 m off the human's path. Bus 127 was turning across the intersection ahead and ended up in the ego's lane. The ego only eased off (10.1 to 6.1 m/s) as the gap shrank from 31 m to 6.5 m, and its front hit the bus. The bus hit the ego's rear later, which doesn't change the cause.
- intersection_ego_speed_hybrid_optuna_023: turned_into_actor, policy at fault: yes. The route command was RIGHT, but the ego drifted left, about 7.6 m off the recorded path, into the lane that bus 127 was turning into from the cross street. It slowed only gradually, from 10 to 6.4 m/s, while the gap closed from 23 m to 4 m, and its front hit the bus head-on.
- intersection_ego_speed_hybrid_optuna_024: other, policy at fault: yes. The command was RIGHT and the recorded path stayed in the right lanes, but the ego stayed in the left lanes and drifted further left, ending 7.6 m off the recording. A bus (127) turning left out of the intersection then crossed into those lanes. The ego could see the bus for about 2 s but only slowed gently from 10 to 6 m/s and hit it head-on.
- intersection_ego_speed_hybrid_optuna_045: left_road, policy at fault: yes. The route command was RIGHT, but while slowing toward the red light (14 down to 6.6 m/s) the ego steered left, away from the recorded path. It went over the left lane edge at the nose of the median just before the stop line, ending 7.5 m from where the human drove. No collision occurred, and the camera view looked fine before the failure (the smearing only shows up near the end).
- intersection_ego_speed_hybrid_optuna_046: left_road, policy at fault: yes. On the approach to the intersection, the ego slowed from 14.6 to 7.5 m/s but drifted left, off the green route path (which curves right for the RIGHT command). It then drove onto the nose of the left median island, about 7.4 m from the recorded human trajectory. No collision was involved, and the camera view was still reasonably intact before the drift.
- intersection_ego_speed_hybrid_optuna_047: left_road, policy at fault: yes. The route command was RIGHT and the route path curved right through the intersection. The ego instead stayed in a lane left of that path, and its own planned path (orange) bent left toward the median island. It slowed from about 10 to 6 m/s and ran off the road at the nose of the median by the stop line, about 7.5 m from the recorded trajectory. No collision was involved, and the camera view looked fine before the failure.
- intersection_ego_speed_hybrid_optuna_049: other, policy at fault: yes. Although the route command was RIGHT, the ego went straight and drifted about 9 m left of the recorded path into the left-side lanes, which appear to be oncoming traffic. A bus (127) visible in the camera from 7.4 s turned out of the intersection into those lanes and came toward the ego, and the ego hit it head-on at about 7 m/s after braking only slightly from 9 m/s.

## Every setting

- S1: 02eadd92 at ego_speed_scale 1.2, actor_time_shift_s -2: 1/5 failed, rate 5%-56% (90%), 1 possibly the simulator's (intersection_ego_speed_hybrid_optuna_002, intersection_ego_speed_hybrid_optuna_012, intersection_ego_speed_hybrid_optuna_013, intersection_ego_speed_hybrid_optuna_015, intersection_ego_speed_hybrid_optuna_016)
- S2: 02eadd92 at ego_speed_scale 1.2, actor_time_shift_s 1.5: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_hybrid_optuna_049)
- S3: 02eadd92 at ego_speed_scale 1.4, actor_time_shift_s 1: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_optuna_048)
- S4: 02eadd92 at ego_speed_scale 1.4, actor_time_shift_s 2: 4/4 failed, rate 60%-100% (90%), 4 possibly the simulator's (intersection_ego_speed_hybrid_optuna_018, intersection_ego_speed_hybrid_optuna_022, intersection_ego_speed_hybrid_optuna_023, intersection_ego_speed_hybrid_optuna_024)
- S5: 054b5901 at ego_speed_scale 1, actor_time_shift_s -1: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_optuna_007)
- S6: 054b5901 at ego_speed_scale 1.4, actor_time_shift_s -2: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_hybrid_optuna_046)
- S7: 054b5901 at ego_speed_scale 1.4, actor_time_shift_s 0: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_hybrid_optuna_045)
- S8: 054b5901 at ego_speed_scale 1.4, actor_time_shift_s 0.5: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_hybrid_optuna_047)
- S9: 054b5901 at ego_speed_scale 1.4, actor_time_shift_s 2: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (intersection_ego_speed_hybrid_optuna_001, intersection_ego_speed_hybrid_optuna_008, intersection_ego_speed_hybrid_optuna_009)
- S10: 0d76134f at ego_speed_scale 1, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_optuna_034)
- S11: 0d76134f at ego_speed_scale 1.4, actor_time_shift_s -2: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_optuna_021)
- S12: 0d76134f at ego_speed_scale 1.4, actor_time_shift_s -1.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_optuna_003)
- S13: 0d76134f at ego_speed_scale 1.4, actor_time_shift_s 2: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_optuna_027)
- S14: 118a3400 at ego_speed_scale 0.8, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_optuna_035)
- S15: 118a3400 at ego_speed_scale 1, actor_time_shift_s 1: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_optuna_020)
- S16: 118a3400 at ego_speed_scale 1.4, actor_time_shift_s -1: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_optuna_004)
- S17: 118a3400 at ego_speed_scale 1.4, actor_time_shift_s 2: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_optuna_028)
- S18: 13a9767e at ego_speed_scale 0.8, actor_time_shift_s -2: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_optuna_040)
- S19: 13a9767e at ego_speed_scale 1, actor_time_shift_s 0.5: 0/8 failed, rate 0%-25% (90%) (intersection_ego_speed_hybrid_optuna_031, intersection_ego_speed_hybrid_optuna_032, intersection_ego_speed_hybrid_optuna_036, intersection_ego_speed_hybrid_optuna_037, intersection_ego_speed_hybrid_optuna_038, intersection_ego_speed_hybrid_optuna_039, intersection_ego_speed_hybrid_optuna_043, intersection_ego_speed_hybrid_optuna_044)
- S20: 13a9767e at ego_speed_scale 1.2, actor_time_shift_s 2: 0/6 failed, rate 0%-31% (90%) (intersection_ego_speed_hybrid_optuna_005, intersection_ego_speed_hybrid_optuna_010, intersection_ego_speed_hybrid_optuna_011, intersection_ego_speed_hybrid_optuna_017, intersection_ego_speed_hybrid_optuna_029, intersection_ego_speed_hybrid_optuna_030)
- S21: 13a9767e at ego_speed_scale 1.4, actor_time_shift_s 1.5: 0/3 failed, rate 0%-47% (90%) (intersection_ego_speed_hybrid_optuna_014, intersection_ego_speed_hybrid_optuna_025, intersection_ego_speed_hybrid_optuna_026)
- S22: 1a7b81b8 at ego_speed_scale 0.8, actor_time_shift_s 1.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_optuna_042)
- S23: 1a7b81b8 at ego_speed_scale 1, actor_time_shift_s 2: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_optuna_006)
- S24: 1a7b81b8 at ego_speed_scale 1.2, actor_time_shift_s 0.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_optuna_033)
- S25: 1a7b81b8 at ego_speed_scale 1.4, actor_time_shift_s -1.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_optuna_041)
- S26: 1a7b81b8 at ego_speed_scale 1.4, actor_time_shift_s 1: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_optuna_019)

## Provenance

Plan: `plan.json` (rationale: Ten scenes are tagged intersection and have a recorded crossing vehicle. Four of them already failed at the default speed and timing: 048b974e, 05a1d902, 0e02fb8c and 0f1f60d5. Three of those four failures had a closest approach above 1 m, so they were probably road departures with no link to the crossing car. Cases found there would not show the effect of the ego's speed or the crossing car's timing, so these four are left out.

The 6 remaining scenes passed at the default settings. Several came close to the crossing car: 054b5901 at 0.26 m and 13a9767e at 0.12 m, so they are good candidates. 0d76134f is weak: the ego drove only 7 m there, but it is kept so that 5 different scenes stay reachable.

Other actors follow their recorded tracks, as in Euro NCAP tests. The retime class is automobile. retime_tracks shifts only the crossing car in each scene, so the other recorded cars stay as recorded.

The budget is 49 runs (7 rounds of 7), close to the ~50 asked for. The goal is the top 5 settings, one per scene, whose failure rate is surely above 0.5. Confirming one setting takes about 5 runs, almost all failures, so confirming 5 takes about 25 runs. That leaves about 24 for exploration, so the goal may not be met in full. If it is not, the study reports the strongest cases found and their near misses.

What the plan cannot answer:
- All 6 scenes are recorded as going straight ('turn: none'). None has both a recorded crossing car and a turn while also passing at the default settings, so turning across traffic is not covered.
- Above ×1.0, the ego starts behind its recorded position and is off the recording for the first second or two of the warm-up.
- The crossing car keeps its recorded speed, as the brief asked. Only its timing changes.
- No planner delay or perception error is applied.). Report written by claude-opus-5-5 from `results` in 27 s; every count above is computed from the queue, not written by the model.

49 of 49 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
