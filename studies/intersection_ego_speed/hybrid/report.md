# At intersections with a recorded crossing car, which combinations of the ego's speed at hand-off and the crossing car's arrival time make VaVAM with the linear MPC collide or leave the road? The goal is the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `hybrid`: 49 kept runs on 6 scenes, varying ego_speed_scale, actor_time_shift_s; 0 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 2 of 5 challenging settings confirmed, after 7 rounds.

## Answer

Only 2 of the 5 cases were confirmed, so the goal was not met. The confirmed cases are scene 02eadd92 at the recorded speed and timing (S1) and scene 054b5901 at 1.2x speed with the recorded timing (S4); every run at both failed. Neither case comes from retiming the crossing car. Both are at 0 s shift, S1 fails at the default settings, and on 054b5901 the ego left the road or ran into the back of a different car (car 9), not crossing track 93. In every failure the policy ignored a RIGHT command and drifted left, more than 3.5 m off its recorded path, so every failure is also flagged as a possible simulator artifact. Shifting the crossing car's timing never caused a collision with it on any scene, so the study found no speed-and-timing combination that makes VaVAM with the linear MPC fail against the crossing car.

## Findings

- Scene 02eadd92 fails at the default settings (1.0x, 0 s) in every run, and the single run at 1.2x also failed. Each time, the ego ignored a RIGHT command, drifted left across lanes and hit bus 127, the scene's crossing track, mostly head-on. Because this happens without any retiming, it is a lane-choice failure of the policy, not an effect of the crossing car's timing. It also contradicts the plan's assumption that this scene passes at the default settings.
  - S1: 02eadd92 at ego_speed_scale 1, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (intersection_ego_speed_hybrid_001, intersection_ego_speed_hybrid_007, intersection_ego_speed_hybrid_008)
  - S2: 02eadd92 at ego_speed_scale 1.2, actor_time_shift_s 0: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_hybrid_009)
- Scene 054b5901 failed in every run at 1.2x with the recorded timing. The one run at 1.0x passed and the one run at 1.4x failed. That hints at a speed threshold between 1.0x and 1.2x, but the 1.0x and 1.4x results are single runs. The ego stayed in the left or straight lane despite a RIGHT command, then either ran off toward the median nose or hit the back of car 9 stopped at a red light. None of these failures involved the crossing car (track 93).
  - S3: 054b5901 at ego_speed_scale 1, actor_time_shift_s 0: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_002)
  - S4: 054b5901 at ego_speed_scale 1.2, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (intersection_ego_speed_hybrid_021, intersection_ego_speed_hybrid_022, intersection_ego_speed_hybrid_023)
  - S5: 054b5901 at ego_speed_scale 1.4, actor_time_shift_s 0: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_hybrid_024)
- Every failure in the study is flagged as a possible artifact because the ego was more than 3.5 m off the recorded trajectory. The triage reads all of them as the policy's fault: it drifted left against the route command. Even so, the rendering is less reliable that far off the recording, and both confirmed cases rest only on these flagged runs.
  - S1: 02eadd92 at ego_speed_scale 1, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (intersection_ego_speed_hybrid_001, intersection_ego_speed_hybrid_007, intersection_ego_speed_hybrid_008)
  - S2: 02eadd92 at ego_speed_scale 1.2, actor_time_shift_s 0: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_hybrid_009)
  - S4: 054b5901 at ego_speed_scale 1.2, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (intersection_ego_speed_hybrid_021, intersection_ego_speed_hybrid_022, intersection_ego_speed_hybrid_023)
  - S5: 054b5901 at ego_speed_scale 1.4, actor_time_shift_s 0: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_hybrid_024)
  - S20: 13a9767e at ego_speed_scale 1, actor_time_shift_s 0.5: 1/7 failed, rate 3%-45% (90%), 1 possibly the simulator's (intersection_ego_speed_hybrid_017, intersection_ego_speed_hybrid_025, intersection_ego_speed_hybrid_036, intersection_ego_speed_hybrid_037, intersection_ego_speed_hybrid_038, intersection_ego_speed_hybrid_043, intersection_ego_speed_hybrid_044)
- Scene 13a9767e produced the closest near misses, highest at 1.0x with +0.5 s, but its only failure was at that setting, against a parked car (148) rather than the crossing car. The failure-rate range at that setting stays below 0.5. Other timings from -1 s to +1 s, and speeds of 0.8x and 1.2x, never failed.
  - S15: 13a9767e at ego_speed_scale 0.8, actor_time_shift_s -0.5: 0/2 failed, rate 0%-58% (90%) (intersection_ego_speed_hybrid_029, intersection_ego_speed_hybrid_030)
  - S16: 13a9767e at ego_speed_scale 0.8, actor_time_shift_s 0.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_039)
  - S17: 13a9767e at ego_speed_scale 1, actor_time_shift_s -1: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_031)
  - S18: 13a9767e at ego_speed_scale 1, actor_time_shift_s -0.5: 0/2 failed, rate 0%-58% (90%) (intersection_ego_speed_hybrid_016, intersection_ego_speed_hybrid_032)
  - S19: 13a9767e at ego_speed_scale 1, actor_time_shift_s 0: 0/3 failed, rate 0%-47% (90%) (intersection_ego_speed_hybrid_005, intersection_ego_speed_hybrid_010, intersection_ego_speed_hybrid_011)
  - S20: 13a9767e at ego_speed_scale 1, actor_time_shift_s 0.5: 1/7 failed, rate 3%-45% (90%), 1 possibly the simulator's (intersection_ego_speed_hybrid_017, intersection_ego_speed_hybrid_025, intersection_ego_speed_hybrid_036, intersection_ego_speed_hybrid_037, intersection_ego_speed_hybrid_038, intersection_ego_speed_hybrid_043, intersection_ego_speed_hybrid_044)
  - S21: 13a9767e at ego_speed_scale 1, actor_time_shift_s 1: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_027)
  - S22: 13a9767e at ego_speed_scale 1.2, actor_time_shift_s 0: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_015)
  - S23: 13a9767e at ego_speed_scale 1.2, actor_time_shift_s 0.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_026)
- Scene 118a3400 never failed at speeds from 0.8x to 1.2x with the crossing car arriving up to 2 s early. Its near-miss score stayed flat across these settings, so earlier arrival did not make it more critical.
  - S7: 118a3400 at ego_speed_scale 0.8, actor_time_shift_s -2: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_049)
  - S8: 118a3400 at ego_speed_scale 0.8, actor_time_shift_s -1.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_042)
  - S9: 118a3400 at ego_speed_scale 0.8, actor_time_shift_s -1: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_035)
  - S10: 118a3400 at ego_speed_scale 1, actor_time_shift_s -1.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_048)
  - S11: 118a3400 at ego_speed_scale 1, actor_time_shift_s -1: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_028)
  - S12: 118a3400 at ego_speed_scale 1, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_019)
  - S13: 118a3400 at ego_speed_scale 1, actor_time_shift_s 0: 0/3 failed, rate 0%-47% (90%) (intersection_ego_speed_hybrid_004, intersection_ego_speed_hybrid_012, intersection_ego_speed_hybrid_013)
  - S14: 118a3400 at ego_speed_scale 1.2, actor_time_shift_s 0: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_018)
- Scene 1a7b81b8 never failed at speeds from 0.8x to 1.2x with shifts from -1 s to +0.5 s. 0.8x was its least critical speed.
  - S24: 1a7b81b8 at ego_speed_scale 0.8, actor_time_shift_s 0: 0/2 failed, rate 0%-58% (90%) (intersection_ego_speed_hybrid_033, intersection_ego_speed_hybrid_034)
  - S25: 1a7b81b8 at ego_speed_scale 1, actor_time_shift_s -1: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_047)
  - S26: 1a7b81b8 at ego_speed_scale 1, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_041)
  - S27: 1a7b81b8 at ego_speed_scale 1, actor_time_shift_s 0: 0/2 failed, rate 0%-58% (90%) (intersection_ego_speed_hybrid_006, intersection_ego_speed_hybrid_014)
  - S28: 1a7b81b8 at ego_speed_scale 1, actor_time_shift_s 0.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_040)
  - S29: 1a7b81b8 at ego_speed_scale 1.2, actor_time_shift_s -0.5: 0/2 failed, rate 0%-58% (90%) (intersection_ego_speed_hybrid_045, intersection_ego_speed_hybrid_046)
  - S30: 1a7b81b8 at ego_speed_scale 1.2, actor_time_shift_s 0: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_020)
- Scene 0d76134f was tested only once, at the default settings. It passed with no near miss, so it adds nothing toward a case.
  - S6: 0d76134f at ego_speed_scale 1, actor_time_shift_s 0: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_003)
- No setting with the ego below its recorded speed (0.8x) ever failed, on any scene.
  - S7: 118a3400 at ego_speed_scale 0.8, actor_time_shift_s -2: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_049)
  - S8: 118a3400 at ego_speed_scale 0.8, actor_time_shift_s -1.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_042)
  - S9: 118a3400 at ego_speed_scale 0.8, actor_time_shift_s -1: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_035)
  - S15: 13a9767e at ego_speed_scale 0.8, actor_time_shift_s -0.5: 0/2 failed, rate 0%-58% (90%) (intersection_ego_speed_hybrid_029, intersection_ego_speed_hybrid_030)
  - S16: 13a9767e at ego_speed_scale 0.8, actor_time_shift_s 0.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_039)
  - S24: 1a7b81b8 at ego_speed_scale 0.8, actor_time_shift_s 0: 0/2 failed, rate 0%-58% (90%) (intersection_ego_speed_hybrid_033, intersection_ego_speed_hybrid_034)

## Open

- The crossing car's timing was never varied on the two failing scenes, 02eadd92 and 054b5901. Runs there with shifts from -2 s to +2 s would show whether timing matters at all once the policy's lane choice is already wrong.
- On 054b5901, the 1.0x and 1.4x results are single runs. Repeats at 1.0x, 1.1x and 1.4x would pin down the speed threshold and confirm the rise with speed.
- The ends of the range are barely covered. 0.6x was never run, 1.4x was run once, and shifts beyond +1 s were never run. Repeats at those ends, mainly on 13a9767e and 1a7b81b8, would show whether any combination brings the crossing car itself into contact.
- Three more scenes are needed for the 5 cases, and 0d76134f, 118a3400 and 1a7b81b8 show no failures yet. Reaching 5 probably needs scenes the plan left out.
- All failures are flagged as possible artifacts (more than 3.5 m off the recorded trajectory). Checking the videos for rendering faults, or rerunning in a setup that renders off-trajectory views faithfully, would settle whether the two confirmed cases hold.
- Turns across traffic were not covered, because all the scenes go straight in the recording.

## Why the runs failed (triage from the video and log)

turned_into_actor 4, no_brake_for_lead 3, left_road 2

- intersection_ego_speed_hybrid_001: no_brake_for_lead, policy at fault: yes. The route command was RIGHT, but the ego drifted left out of its recorded lane, about 7 m off the recorded trajectory, into the lane of bus 127, which was moving slowly. It then held about 8.5 m/s and closed a 38 m gap with almost no braking, hitting the bus's rear with its front.
- intersection_ego_speed_hybrid_007: turned_into_actor, policy at fault: yes. The route said RIGHT, but the ego drifted left, away from the recorded path (7 m off by the time of impact), into lanes where bus 127 was. The gap closed at about 15 m/s while the ego was only doing about 8.6 m/s, so the bus was moving toward it. The ego barely slowed (8.7 to 7.5 m/s) and hit the bus head-on with its front.
- intersection_ego_speed_hybrid_008: turned_into_actor, policy at fault: yes. The route command was RIGHT and the recorded path ran to the right, but the ego steered left across lanes at about 8.5 m/s, ending up 7 m off the recorded path. That put it in the path of bus 127, which had turned in ahead and was facing the ego. The gap closed faster than the ego's own speed, and the ego barely slowed (8.5 to 7.7 m/s) before hitting the bus head-on.
- intersection_ego_speed_hybrid_009: turned_into_actor, policy at fault: yes. The route command was RIGHT, but the ego drifted left away from the recorded path (about 7 m off by the end) at about 8.5 m/s. That put it into the lane of bus 127, which it was passing on the bus's right. By 9.4 s it had cut into the bus's side, and this was logged as an at-fault front collision.
- intersection_ego_speed_hybrid_021: left_road, policy at fault: yes. The command was RIGHT and the route curved right through the intersection, but the ego kept drifting left, away from both the route and the human trajectory (about 4 m off at 7.7 s, 7.5 m at 9.7 s). It slowed from 10 to 6.3 m/s and ran off the drivable area toward the median nose on the left at 9.7 s. Car 9 stayed ahead and to the right with no visible contact, and the table's collision metrics are 0, even though the input flags front and lateral collisions.
- intersection_ego_speed_hybrid_022: left_road, policy at fault: yes. The route command was RIGHT, and the recorded path curved right through the intersection. Instead, the ego stayed in the far-left lane, drifted further from the recorded path (3.9 m at 7.8 s, 7.7 m at 9.8 s) and slowed from about 10 to 6 m/s. At 9.8 s its planned path bent left into the raised median nose, and it was flagged offroad.
- intersection_ego_speed_hybrid_023: no_brake_for_lead, policy at fault: yes. With a RIGHT command, the ego stayed in the lane to the left of where the recorded human drove (the human went into the right-turn lane, 7 m off) and closed on vehicle 9, which was stopped or creeping at the red light. It slowed gradually from 9.1 to 2.9 m/s, but not enough, and hit 9's rear at about 3 m/s.
- intersection_ego_speed_hybrid_024: no_brake_for_lead, policy at fault: yes. The command was RIGHT and the recorded route curved into the right-turn lane, but the ego stayed in the straight lane behind a silver sedan (actor 9) that was slowing for a red light. The ego slowed only gradually, from 12.8 to 5.6 m/s, while the gap closed from 15.8 m to 4.7 m, and it hit the sedan's rear at 9.8 s.
- intersection_ego_speed_hybrid_044: turned_into_actor, policy at fault: yes. The route command was RIGHT, but the ego steered left, away from the recorded path and toward the curb-side parking lane, as it neared the intersection. Its front corner hit parked car 148 at about 6 m/s while it was still slowing; by then it was about 4 m off the recorded trajectory.

## Every setting

- S1: 02eadd92 at ego_speed_scale 1, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (intersection_ego_speed_hybrid_001, intersection_ego_speed_hybrid_007, intersection_ego_speed_hybrid_008)
- S2: 02eadd92 at ego_speed_scale 1.2, actor_time_shift_s 0: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_hybrid_009)
- S3: 054b5901 at ego_speed_scale 1, actor_time_shift_s 0: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_002)
- S4: 054b5901 at ego_speed_scale 1.2, actor_time_shift_s 0: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (intersection_ego_speed_hybrid_021, intersection_ego_speed_hybrid_022, intersection_ego_speed_hybrid_023)
- S5: 054b5901 at ego_speed_scale 1.4, actor_time_shift_s 0: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_hybrid_024)
- S6: 0d76134f at ego_speed_scale 1, actor_time_shift_s 0: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_003)
- S7: 118a3400 at ego_speed_scale 0.8, actor_time_shift_s -2: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_049)
- S8: 118a3400 at ego_speed_scale 0.8, actor_time_shift_s -1.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_042)
- S9: 118a3400 at ego_speed_scale 0.8, actor_time_shift_s -1: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_035)
- S10: 118a3400 at ego_speed_scale 1, actor_time_shift_s -1.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_048)
- S11: 118a3400 at ego_speed_scale 1, actor_time_shift_s -1: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_028)
- S12: 118a3400 at ego_speed_scale 1, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_019)
- S13: 118a3400 at ego_speed_scale 1, actor_time_shift_s 0: 0/3 failed, rate 0%-47% (90%) (intersection_ego_speed_hybrid_004, intersection_ego_speed_hybrid_012, intersection_ego_speed_hybrid_013)
- S14: 118a3400 at ego_speed_scale 1.2, actor_time_shift_s 0: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_018)
- S15: 13a9767e at ego_speed_scale 0.8, actor_time_shift_s -0.5: 0/2 failed, rate 0%-58% (90%) (intersection_ego_speed_hybrid_029, intersection_ego_speed_hybrid_030)
- S16: 13a9767e at ego_speed_scale 0.8, actor_time_shift_s 0.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_039)
- S17: 13a9767e at ego_speed_scale 1, actor_time_shift_s -1: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_031)
- S18: 13a9767e at ego_speed_scale 1, actor_time_shift_s -0.5: 0/2 failed, rate 0%-58% (90%) (intersection_ego_speed_hybrid_016, intersection_ego_speed_hybrid_032)
- S19: 13a9767e at ego_speed_scale 1, actor_time_shift_s 0: 0/3 failed, rate 0%-47% (90%) (intersection_ego_speed_hybrid_005, intersection_ego_speed_hybrid_010, intersection_ego_speed_hybrid_011)
- S20: 13a9767e at ego_speed_scale 1, actor_time_shift_s 0.5: 1/7 failed, rate 3%-45% (90%), 1 possibly the simulator's (intersection_ego_speed_hybrid_017, intersection_ego_speed_hybrid_025, intersection_ego_speed_hybrid_036, intersection_ego_speed_hybrid_037, intersection_ego_speed_hybrid_038, intersection_ego_speed_hybrid_043, intersection_ego_speed_hybrid_044)
- S21: 13a9767e at ego_speed_scale 1, actor_time_shift_s 1: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_027)
- S22: 13a9767e at ego_speed_scale 1.2, actor_time_shift_s 0: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_015)
- S23: 13a9767e at ego_speed_scale 1.2, actor_time_shift_s 0.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_026)
- S24: 1a7b81b8 at ego_speed_scale 0.8, actor_time_shift_s 0: 0/2 failed, rate 0%-58% (90%) (intersection_ego_speed_hybrid_033, intersection_ego_speed_hybrid_034)
- S25: 1a7b81b8 at ego_speed_scale 1, actor_time_shift_s -1: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_047)
- S26: 1a7b81b8 at ego_speed_scale 1, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_041)
- S27: 1a7b81b8 at ego_speed_scale 1, actor_time_shift_s 0: 0/2 failed, rate 0%-58% (90%) (intersection_ego_speed_hybrid_006, intersection_ego_speed_hybrid_014)
- S28: 1a7b81b8 at ego_speed_scale 1, actor_time_shift_s 0.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_040)
- S29: 1a7b81b8 at ego_speed_scale 1.2, actor_time_shift_s -0.5: 0/2 failed, rate 0%-58% (90%) (intersection_ego_speed_hybrid_045, intersection_ego_speed_hybrid_046)
- S30: 1a7b81b8 at ego_speed_scale 1.2, actor_time_shift_s 0: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_hybrid_020)

## Provenance

Plan: `plan.json` (rationale: Ten scenes are tagged intersection and have a recorded crossing vehicle. Four of them already failed at the default speed and timing: 048b974e, 05a1d902, 0e02fb8c and 0f1f60d5. Three of those four failures had a closest approach above 1 m, so they were probably road departures with no link to the crossing car. Cases found there would not show the effect of the ego's speed or the crossing car's timing, so these four are left out.

The 6 remaining scenes passed at the default settings. Several came close to the crossing car: 054b5901 at 0.26 m and 13a9767e at 0.12 m, so they are good candidates. 0d76134f is weak: the ego drove only 7 m there, but it is kept so that 5 different scenes stay reachable.

Other actors follow their recorded tracks, as in Euro NCAP tests. The retime class is automobile. retime_tracks shifts only the crossing car in each scene, so the other recorded cars stay as recorded.

The budget is 49 runs (7 rounds of 7), close to the ~50 asked for. The goal is the top 5 settings, one per scene, whose failure rate is surely above 0.5. Confirming one setting takes about 5 runs, almost all failures, so confirming 5 takes about 25 runs. That leaves about 24 for exploration, so the goal may not be met in full. If it is not, the study reports the strongest cases found and their near misses.

What the plan cannot answer:
- All 6 scenes are recorded as going straight ('turn: none'). None has both a recorded crossing car and a turn while also passing at the default settings, so turning across traffic is not covered.
- Above ×1.0, the ego starts behind its recorded position and is off the recording for the first second or two of the warm-up.
- The crossing car keeps its recorded speed, as the brief asked. Only its timing changes.
- No planner delay or perception error is applied.). Report written by claude-opus-5-5 from `results` in 30 s; every count above is computed from the queue, not written by the model.

49 of 49 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
