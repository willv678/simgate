# At intersections with a recorded crossing car, which combinations of the ego's speed at hand-off and the crossing car's arrival time make VaVAM with the linear MPC collide or leave the road? The goal is the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `intersection_ego_speed`: 49 kept runs on 6 scenes, varying ego_speed_scale, actor_time_shift_s; 0 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 2 of 5 challenging settings confirmed, after 7 rounds.

## Answer

The goal was not met: only 2 of the 5 cases were confirmed, on two scenes. In both, VaVAM with the linear MPC failed every run at 1.2x hand-off speed (S1 on 02eadd92 and S3 on 054b5901). The failure ranges sit above 0.5 but are wide, because each rests on only a few runs. Neither case is really about the crossing car's timing. On 054b5901 the ego ignored a RIGHT command and drove onto the median with no other car involved, whether the crossing car was shifted or not. On 02eadd92 the ego drifted left into the oncoming bus at the recorded timing; no other timing was tried there. All of these failures are flagged as possible simulator artifacts because the ego ended more than 3.5 m off the recorded path. Triage found that the policy steered off course first and the camera view was clean before each failure, so they look like the policy's errors, not rendering. Scene 13a9767e came close to the crossing car many times across timings and speeds but never failed, and the other three scenes showed nothing.

## Findings

- On 02eadd92 at 1.2x speed and recorded timing, every run failed. Each time the ego was given a RIGHT command but drifted left about 7 m off the recorded path and hit bus 127 head-on with almost no braking. This is the policy's fault. The run counts as an artifact only because it left the recorded path.
  - S1: 02eadd92 at ego_speed_scale 1.2, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (intersection_ego_speed_005, intersection_ego_speed_008, intersection_ego_speed_009)
- On 054b5901 at 1.2x speed, every run failed, whether the crossing car came 0.5 s early or on time. Each time the ego ignored a RIGHT command, kept straight while slowing, and ran onto the median island. No actor was involved, so the crossing car's timing played no part.
  - S3: 054b5901 at ego_speed_scale 1.2, actor_time_shift_s -0.5: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (intersection_ego_speed_004, intersection_ego_speed_010, intersection_ego_speed_015)
  - S4: 054b5901 at ego_speed_scale 1.2, actor_time_shift_s 0: 2/2 failed, rate 42%-100% (90%), 2 possibly the simulator's (intersection_ego_speed_011, intersection_ego_speed_049)
- On 054b5901 at the recorded speed and timing, the single run passed with a moderate near miss. This hints that the higher hand-off speed brings on the departure, but one run is not a rate.
  - S2: 054b5901 at ego_speed_scale 1, actor_time_shift_s 0: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_003)
  - S3: 054b5901 at ego_speed_scale 1.2, actor_time_shift_s -0.5: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (intersection_ego_speed_004, intersection_ego_speed_010, intersection_ego_speed_015)
  - S4: 054b5901 at ego_speed_scale 1.2, actor_time_shift_s 0: 2/2 failed, rate 42%-100% (90%), 2 possibly the simulator's (intersection_ego_speed_011, intersection_ego_speed_049)
- On 13a9767e the ego came close to the crossing car at every speed and timing tried, closest at recorded speed with the crossing car 1 to 2 s early. It never collided, even at the settings repeated several times. Its failure rate there is likely below one half, but this is not shown to be zero.
  - S13: 13a9767e at ego_speed_scale 1, actor_time_shift_s -2: 0/4 failed, rate 0%-40% (90%) (intersection_ego_speed_039, intersection_ego_speed_046, intersection_ego_speed_047, intersection_ego_speed_048)
  - S14: 13a9767e at ego_speed_scale 1, actor_time_shift_s -1.5: 0/4 failed, rate 0%-40% (90%) (intersection_ego_speed_038, intersection_ego_speed_043, intersection_ego_speed_044, intersection_ego_speed_045)
  - S15: 13a9767e at ego_speed_scale 1, actor_time_shift_s -1: 0/3 failed, rate 0%-47% (90%) (intersection_ego_speed_030, intersection_ego_speed_036, intersection_ego_speed_037)
  - S18: 13a9767e at ego_speed_scale 1, actor_time_shift_s 0.5: 0/3 failed, rate 0%-47% (90%) (intersection_ego_speed_013, intersection_ego_speed_024, intersection_ego_speed_029)
  - S10: 13a9767e at ego_speed_scale 0.8, actor_time_shift_s -1: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_041)
  - S11: 13a9767e at ego_speed_scale 0.8, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_042)
  - S12: 13a9767e at ego_speed_scale 0.8, actor_time_shift_s 0.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_017)
  - S16: 13a9767e at ego_speed_scale 1, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_026)
  - S17: 13a9767e at ego_speed_scale 1, actor_time_shift_s 0: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_001)
  - S19: 13a9767e at ego_speed_scale 1, actor_time_shift_s 1: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_016)
  - S20: 13a9767e at ego_speed_scale 1, actor_time_shift_s 1.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_032)
  - S21: 13a9767e at ego_speed_scale 1.2, actor_time_shift_s -1: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_040)
  - S22: 13a9767e at ego_speed_scale 1.2, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_012)
  - S23: 13a9767e at ego_speed_scale 1.2, actor_time_shift_s 0: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_002)
  - S24: 13a9767e at ego_speed_scale 1.2, actor_time_shift_s 0.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_025)
  - S25: 13a9767e at ego_speed_scale 1.2, actor_time_shift_s 1: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_031)
  - S26: 13a9767e at ego_speed_scale 1.4, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_023)
  - S27: 13a9767e at ego_speed_scale 1.4, actor_time_shift_s 0: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_018)
  - S28: 13a9767e at ego_speed_scale 1.4, actor_time_shift_s 0.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_022)
- On 118a3400, 1a7b81b8 and 0d76134f no run failed and almost none came close, across speeds of 0.8x to 1.4x and timing shifts of -2 s to +2 s. Each setting was run only once.
  - S5: 0d76134f at ego_speed_scale 1.4, actor_time_shift_s 0: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_020)
  - S6: 118a3400 at ego_speed_scale 0.8, actor_time_shift_s 1: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_028)
  - S7: 118a3400 at ego_speed_scale 1.2, actor_time_shift_s -1: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_021)
  - S8: 118a3400 at ego_speed_scale 1.4, actor_time_shift_s -2: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_035)
  - S9: 118a3400 at ego_speed_scale 1.4, actor_time_shift_s 0: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_007)
  - S29: 1a7b81b8 at ego_speed_scale 1.2, actor_time_shift_s 0: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_006)
  - S30: 1a7b81b8 at ego_speed_scale 1.2, actor_time_shift_s 1: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_019)
  - S31: 1a7b81b8 at ego_speed_scale 1.4, actor_time_shift_s -1.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_033)
  - S32: 1a7b81b8 at ego_speed_scale 1.4, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_014)
  - S33: 1a7b81b8 at ego_speed_scale 1.4, actor_time_shift_s 1: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_027)
  - S34: 1a7b81b8 at ego_speed_scale 1.4, actor_time_shift_s 2: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_034)

## Open

- Whether timing matters on 02eadd92: only recorded timing was run. Runs at 1.2x with the bus shifted by about ±1 s, plus runs at 1.0x and 0.8x, would show whether the collision depends on the bus's timing or only on the left drift.
- The speed threshold on 054b5901: repeats at 1.0x (S2 has one run) and runs at 1.1x and 1.4x would show where the departure onto the median begins.
- Three more scenes are needed for the goal. 13a9767e is the best candidate. Repeats of its closest near misses, at recorded speed with the crossing car 1 to 2 s early, plus untried slow-speed settings such as 0.6x, could show whether any combination tips it into a collision.
- The plan lists all six scenes as going straight, yet the triage of both failing scenes shows a RIGHT command and a recorded path curving right. The turn tags should be checked: if these scenes are right turns, the failures concern turning, not crossing traffic.
- None of the failures was caused by the crossing car's timing. Turning across traffic, the four scenes left out, and planner delay or perception error were not covered.

## Why the runs failed (triage from the video and log)

left_road 5, turned_into_actor 3

- intersection_ego_speed_004: left_road, policy at fault: yes. The command was RIGHT, and the recorded route curved right toward the turn lanes. Instead the policy kept the ego straight and then drifted left across the lanes onto the median/island at the intersection while slowing from 12.5 to 7.6 m/s. It went off-road about 8 m from the human path; the camera view was clean before the failure.
- intersection_ego_speed_005: turned_into_actor, policy at fault: yes. The route command was RIGHT, but the ego drifted left out of its recorded lane, ending 6.9 m off the human's path. That put it in the lane of bus 127, which was coming the other way: the gap shrank by about 15 m/s while the ego was only doing about 8.5 m/s. The ego barely slowed (8.9→8.2 m/s), and its front hit the bus at 9.0 s.
- intersection_ego_speed_008: turned_into_actor, policy at fault: yes. The route command was RIGHT and the recorded path stayed to the right, but the ego steered left into the next lane, where bus 127 had just turned in and was moving slowly. The ego kept going at about 8.5 m/s while the gap closed from 32 m to 10 m and hit the bus with its front. The rear contact happened at some other point.
- intersection_ego_speed_009: turned_into_actor, policy at fault: yes. Although the command was RIGHT, the ego veered left off the recorded path (about 7 m off by the end) and into the lane of bus 127. The bus was coming toward it, and the gap closed from 39 m to 10 m. The ego's front hit the bus at about 8 m/s with almost no braking.
- intersection_ego_speed_010: left_road, policy at fault: yes. The route command was RIGHT and the recorded path curved right through the intersection. Instead, the ego stayed a lane or more to the left of the recorded path, kept its plan pointed straight ahead, and slowed from 11.6 to 6.7 m/s before running into the nose of the median island on its left, 7.5 m off the recording. The camera view was mostly clean before the failure, and no actor was involved.
- intersection_ego_speed_011: left_road, policy at fault: yes. The route command was RIGHT and the recorded path curves right toward the turn lanes, but the ego kept going straight with a slight drift left while slowing from 12.6 to 7.2 m/s. It ran onto the median island at the intersection approach, about 7.5 m off the recorded path. The camera view looked fine before the failure.
- intersection_ego_speed_015: left_road, policy at fault: yes. The route command was RIGHT and the recorded path curves right toward the right-turn lanes. The policy instead held a straight, slightly left-drifting line along the left edge of the lanes, slowing from about 12 to 7 m/s. At 9.4 s it ran onto the median/curb at the intersection, about 7.6 m from the recorded path; it did not hit anything, and the camera view was still intact before the failure.
- intersection_ego_speed_049: left_road, policy at fault: yes. The route command was RIGHT, and the recorded path curved right through the intersection. The ego instead held a straight, slightly left-drifting path along the left edge of the lanes while slowing from 10 to 7 m/s. At 9.5 s it ran onto the raised median nose ahead of the stop line, about 7.5 m from the recorded path. No other actor was involved, and the camera view was clear enough to show the lanes, apart from smearing that grew as the ego moved further from the recorded path.

## Every setting

- S1: 02eadd92 at ego_speed_scale 1.2, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (intersection_ego_speed_005, intersection_ego_speed_008, intersection_ego_speed_009)
- S2: 054b5901 at ego_speed_scale 1, actor_time_shift_s 0: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_003)
- S3: 054b5901 at ego_speed_scale 1.2, actor_time_shift_s -0.5: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (intersection_ego_speed_004, intersection_ego_speed_010, intersection_ego_speed_015)
- S4: 054b5901 at ego_speed_scale 1.2, actor_time_shift_s 0: 2/2 failed, rate 42%-100% (90%), 2 possibly the simulator's (intersection_ego_speed_011, intersection_ego_speed_049)
- S5: 0d76134f at ego_speed_scale 1.4, actor_time_shift_s 0: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_020)
- S6: 118a3400 at ego_speed_scale 0.8, actor_time_shift_s 1: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_028)
- S7: 118a3400 at ego_speed_scale 1.2, actor_time_shift_s -1: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_021)
- S8: 118a3400 at ego_speed_scale 1.4, actor_time_shift_s -2: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_035)
- S9: 118a3400 at ego_speed_scale 1.4, actor_time_shift_s 0: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_007)
- S10: 13a9767e at ego_speed_scale 0.8, actor_time_shift_s -1: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_041)
- S11: 13a9767e at ego_speed_scale 0.8, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_042)
- S12: 13a9767e at ego_speed_scale 0.8, actor_time_shift_s 0.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_017)
- S13: 13a9767e at ego_speed_scale 1, actor_time_shift_s -2: 0/4 failed, rate 0%-40% (90%) (intersection_ego_speed_039, intersection_ego_speed_046, intersection_ego_speed_047, intersection_ego_speed_048)
- S14: 13a9767e at ego_speed_scale 1, actor_time_shift_s -1.5: 0/4 failed, rate 0%-40% (90%) (intersection_ego_speed_038, intersection_ego_speed_043, intersection_ego_speed_044, intersection_ego_speed_045)
- S15: 13a9767e at ego_speed_scale 1, actor_time_shift_s -1: 0/3 failed, rate 0%-47% (90%) (intersection_ego_speed_030, intersection_ego_speed_036, intersection_ego_speed_037)
- S16: 13a9767e at ego_speed_scale 1, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_026)
- S17: 13a9767e at ego_speed_scale 1, actor_time_shift_s 0: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_001)
- S18: 13a9767e at ego_speed_scale 1, actor_time_shift_s 0.5: 0/3 failed, rate 0%-47% (90%) (intersection_ego_speed_013, intersection_ego_speed_024, intersection_ego_speed_029)
- S19: 13a9767e at ego_speed_scale 1, actor_time_shift_s 1: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_016)
- S20: 13a9767e at ego_speed_scale 1, actor_time_shift_s 1.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_032)
- S21: 13a9767e at ego_speed_scale 1.2, actor_time_shift_s -1: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_040)
- S22: 13a9767e at ego_speed_scale 1.2, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_012)
- S23: 13a9767e at ego_speed_scale 1.2, actor_time_shift_s 0: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_002)
- S24: 13a9767e at ego_speed_scale 1.2, actor_time_shift_s 0.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_025)
- S25: 13a9767e at ego_speed_scale 1.2, actor_time_shift_s 1: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_031)
- S26: 13a9767e at ego_speed_scale 1.4, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_023)
- S27: 13a9767e at ego_speed_scale 1.4, actor_time_shift_s 0: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_018)
- S28: 13a9767e at ego_speed_scale 1.4, actor_time_shift_s 0.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_022)
- S29: 1a7b81b8 at ego_speed_scale 1.2, actor_time_shift_s 0: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_006)
- S30: 1a7b81b8 at ego_speed_scale 1.2, actor_time_shift_s 1: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_019)
- S31: 1a7b81b8 at ego_speed_scale 1.4, actor_time_shift_s -1.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_033)
- S32: 1a7b81b8 at ego_speed_scale 1.4, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_014)
- S33: 1a7b81b8 at ego_speed_scale 1.4, actor_time_shift_s 1: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_027)
- S34: 1a7b81b8 at ego_speed_scale 1.4, actor_time_shift_s 2: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_034)

## Provenance

Plan: `plan.json` (rationale: Ten scenes are tagged intersection and have a recorded crossing vehicle. Four of them already failed at the default speed and timing: 048b974e, 05a1d902, 0e02fb8c and 0f1f60d5. Three of those four failures had a closest approach above 1 m, so they were probably road departures with no link to the crossing car. Cases found there would not show the effect of the ego's speed or the crossing car's timing, so these four are left out.

The 6 remaining scenes passed at the default settings. Several came close to the crossing car: 054b5901 at 0.26 m and 13a9767e at 0.12 m, so they are good candidates. 0d76134f is weak: the ego drove only 7 m there, but it is kept so that 5 different scenes stay reachable.

Other actors follow their recorded tracks, as in Euro NCAP tests. The retime class is automobile. retime_tracks shifts only the crossing car in each scene, so the other recorded cars stay as recorded.

The budget is 49 runs (7 rounds of 7), close to the ~50 asked for. The goal is the top 5 settings, one per scene, whose failure rate is surely above 0.5. Confirming one setting takes about 5 runs, almost all failures, so confirming 5 takes about 25 runs. That leaves about 24 for exploration, so the goal may not be met in full. If it is not, the study reports the strongest cases found and their near misses.

What the plan cannot answer:
- All 6 scenes are recorded as going straight ('turn: none'). None has both a recorded crossing car and a turn while also passing at the default settings, so turning across traffic is not covered.
- Above ×1.0, the ego starts behind its recorded position and is off the recording for the first second or two of the warm-up.
- The crossing car keeps its recorded speed, as the brief asked. Only its timing changes.
- No planner delay or perception error is applied.). Report written by claude-opus-5-5 from `results` in 21 s; every count above is computed from the queue, not written by the model.

49 of 49 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
