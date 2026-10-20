# At intersections with a recorded crossing car, which combinations of the ego's speed at hand-off and the crossing car's arrival time make VaVAM with the linear MPC collide or leave the road? The goal is the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `optuna_confirm`: 49 kept runs on 6 scenes, varying ego_speed_scale, actor_time_shift_s; 0 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 1 of 5 challenging settings confirmed, after 7 rounds.

## Answer

The goal was not met. Only one challenging case was confirmed: scene 02eadd92 at 0.8x speed with the crossing bus arriving 1.5 s late (S7), where every repeat failed. No other scene produced a single failure. On 02eadd92 the cause is not really the speed and timing combination. The route says turn right, but the policy drifts left into the bus's lanes and hits it head-on, or drives off the left edge of the road. This happened at almost every speed and timing tried, but outside S7 each setting was run only once or twice, so those are hints, not rates. Every failure is flagged as a possible simulator artifact because the ego ended far from the recorded path. The triage says the drift began before the camera view smeared and puts the fault on the policy, but rendering's part can't be fully ruled out.

## Findings

- The one confirmed challenging case is scene 02eadd92 at 0.8x ego speed with the crossing bus 1.5 s late. Every repeat ended in a front collision with bus 127 after the ego drifted left against a RIGHT command. Every failure there is flagged as a possible artifact, though the triage blames the policy.
  - S7: 02eadd92 at ego_speed_scale 0.8, actor_time_shift_s 1.5: 6/6 failed, rate 69%-100% (90%), 6 possibly the simulator's (intersection_ego_speed_optuna_confirm_002, intersection_ego_speed_optuna_confirm_008, intersection_ego_speed_optuna_confirm_015, intersection_ego_speed_optuna_confirm_018, intersection_ego_speed_optuna_confirm_044, intersection_ego_speed_optuna_confirm_047)
- On 02eadd92 the failures barely depend on the two knobs. Single runs failed from 0.6x to 1.4x speed and from the bus arriving 2 s early to 2 s late. The one pass was a single run at 1.4x speed with the original timing.
  - S1: 02eadd92 at ego_speed_scale 0.6, actor_time_shift_s -2.0: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_optuna_confirm_026)
  - S2: 02eadd92 at ego_speed_scale 0.6, actor_time_shift_s -0.5: 2/2 failed, rate 42%-100% (90%), 2 possibly the simulator's (intersection_ego_speed_optuna_confirm_013, intersection_ego_speed_optuna_confirm_023)
  - S3: 02eadd92 at ego_speed_scale 0.6, actor_time_shift_s 1.5: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_optuna_confirm_041)
  - S4: 02eadd92 at ego_speed_scale 0.8, actor_time_shift_s -1.5: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_optuna_confirm_045)
  - S5: 02eadd92 at ego_speed_scale 0.8, actor_time_shift_s -0.5: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_optuna_confirm_038)
  - S6: 02eadd92 at ego_speed_scale 0.8, actor_time_shift_s 0.5: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_optuna_confirm_019)
  - S8: 02eadd92 at ego_speed_scale 0.8, actor_time_shift_s 2.0: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_optuna_confirm_021)
  - S9: 02eadd92 at ego_speed_scale 1.0, actor_time_shift_s 1.5: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_optuna_confirm_020)
  - S10: 02eadd92 at ego_speed_scale 1.2, actor_time_shift_s 1.0: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_optuna_confirm_030)
  - S11: 02eadd92 at ego_speed_scale 1.2, actor_time_shift_s 1.5: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_optuna_confirm_039)
  - S12: 02eadd92 at ego_speed_scale 1.4, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_optuna_confirm_028)
  - S13: 02eadd92 at ego_speed_scale 1.4, actor_time_shift_s 1.5: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_optuna_confirm_049)
- At 0.6x speed on 02eadd92, some failures were road departures with no other actor involved: the ego crossed the lanes to the left and went over the curb. They are not collisions with the crossing car.
  - S2: 02eadd92 at ego_speed_scale 0.6, actor_time_shift_s -0.5: 2/2 failed, rate 42%-100% (90%), 2 possibly the simulator's (intersection_ego_speed_optuna_confirm_013, intersection_ego_speed_optuna_confirm_023)
  - S3: 02eadd92 at ego_speed_scale 0.6, actor_time_shift_s 1.5: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_optuna_confirm_041)
- On 02eadd92 the collisions are front or side hits on bus 127, the crossing car the study retimes. They happen only because the policy drove into lanes the recorded car never used.
  - S4: 02eadd92 at ego_speed_scale 0.8, actor_time_shift_s -1.5: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_optuna_confirm_045)
  - S5: 02eadd92 at ego_speed_scale 0.8, actor_time_shift_s -0.5: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_optuna_confirm_038)
  - S6: 02eadd92 at ego_speed_scale 0.8, actor_time_shift_s 0.5: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_optuna_confirm_019)
  - S7: 02eadd92 at ego_speed_scale 0.8, actor_time_shift_s 1.5: 6/6 failed, rate 69%-100% (90%), 6 possibly the simulator's (intersection_ego_speed_optuna_confirm_002, intersection_ego_speed_optuna_confirm_008, intersection_ego_speed_optuna_confirm_015, intersection_ego_speed_optuna_confirm_018, intersection_ego_speed_optuna_confirm_044, intersection_ego_speed_optuna_confirm_047)
  - S8: 02eadd92 at ego_speed_scale 0.8, actor_time_shift_s 2.0: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_optuna_confirm_021)
  - S9: 02eadd92 at ego_speed_scale 1.0, actor_time_shift_s 1.5: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_optuna_confirm_020)
  - S10: 02eadd92 at ego_speed_scale 1.2, actor_time_shift_s 1.0: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_optuna_confirm_030)
  - S11: 02eadd92 at ego_speed_scale 1.2, actor_time_shift_s 1.5: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_optuna_confirm_039)
  - S13: 02eadd92 at ego_speed_scale 1.4, actor_time_shift_s 1.5: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_optuna_confirm_049)
- Scene 13a9767e gave the strongest near misses but no failures. Its most repeated setting, 1.0x speed with the car 2 s early, passed every time, and its range rules out a failure rate above one half.
  - S26: 13a9767e at ego_speed_scale 0.6, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_optuna_confirm_033)
  - S27: 13a9767e at ego_speed_scale 0.8, actor_time_shift_s -1.0: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_optuna_confirm_034)
  - S28: 13a9767e at ego_speed_scale 1.0, actor_time_shift_s -2.0: 0/6 failed, rate 0%-31% (90%) (intersection_ego_speed_optuna_confirm_014, intersection_ego_speed_optuna_confirm_016, intersection_ego_speed_optuna_confirm_022, intersection_ego_speed_optuna_confirm_029, intersection_ego_speed_optuna_confirm_036, intersection_ego_speed_optuna_confirm_043)
  - S29: 13a9767e at ego_speed_scale 1.4, actor_time_shift_s 1.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_optuna_confirm_010)
- Scene 054b5901 had no failures, including the repeated setting at 1.0x speed with the car 1 s early, and its near misses were moderate.
  - S14: 054b5901 at ego_speed_scale 0.6, actor_time_shift_s -1.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_optuna_confirm_040)
  - S15: 054b5901 at ego_speed_scale 0.8, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_optuna_confirm_011)
  - S16: 054b5901 at ego_speed_scale 0.8, actor_time_shift_s 1.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_optuna_confirm_037)
  - S17: 054b5901 at ego_speed_scale 1.0, actor_time_shift_s -1.0: 0/3 failed, rate 0%-47% (90%) (intersection_ego_speed_optuna_confirm_001, intersection_ego_speed_optuna_confirm_009, intersection_ego_speed_optuna_confirm_017)
- Scenes 0d76134f and 118a3400 showed no failures and no near misses at any setting tried. Scene 1a7b81b8 showed no failures and only weak near misses.
  - S18: 0d76134f at ego_speed_scale 0.6, actor_time_shift_s 0.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_optuna_confirm_027)
  - S19: 0d76134f at ego_speed_scale 0.8, actor_time_shift_s 1.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_optuna_confirm_035)
  - S20: 0d76134f at ego_speed_scale 1.0, actor_time_shift_s 1.0: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_optuna_confirm_007)
  - S21: 0d76134f at ego_speed_scale 1.4, actor_time_shift_s -1.5: 0/2 failed, rate 0%-58% (90%) (intersection_ego_speed_optuna_confirm_003, intersection_ego_speed_optuna_confirm_004)
  - S22: 118a3400 at ego_speed_scale 0.6, actor_time_shift_s 2.0: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_optuna_confirm_032)
  - S23: 118a3400 at ego_speed_scale 0.8, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_optuna_confirm_024)
  - S24: 118a3400 at ego_speed_scale 0.8, actor_time_shift_s 1.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_optuna_confirm_046)
  - S25: 118a3400 at ego_speed_scale 1.2, actor_time_shift_s 1.5: 0/2 failed, rate 0%-58% (90%) (intersection_ego_speed_optuna_confirm_005, intersection_ego_speed_optuna_confirm_006)
  - S30: 1a7b81b8 at ego_speed_scale 0.6, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_optuna_confirm_025)
  - S31: 1a7b81b8 at ego_speed_scale 0.8, actor_time_shift_s 1.0: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_optuna_confirm_012)
  - S32: 1a7b81b8 at ego_speed_scale 0.8, actor_time_shift_s 1.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_optuna_confirm_048)
  - S33: 1a7b81b8 at ego_speed_scale 1.2, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_optuna_confirm_031)
  - S34: 1a7b81b8 at ego_speed_scale 1.4, actor_time_shift_s -1.0: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_optuna_confirm_042)

## Open

- Four of the five cases are missing. Repeating the near-miss settings on 13a9767e at 1.4x with the car 1.5 s late (S29) and at 0.8x with the car 1 s early (S27), and on 054b5901 at 1.0x with the car 1 s early (S17) and at 0.6x with the car 1.5 s early (S14), would show whether any of them fail at all.
- Whether the 02eadd92 failures are the policy's or partly the renderer's. Every one is flagged as a possible artifact. Checking the early frames of the S7 runs for when the left drift starts against when the view degrades would settle it.
- Whether 02eadd92 fails even with no crossing car: the left drift happens at every timing. A few runs at 1.0x speed with the original timing, and with bus 127 removed, would show whether the bus timing matters at all.
- Turning across traffic was not tested: every scene in the study goes straight. The four scenes that already failed at default settings were also left out.

## Why the runs failed (triage from the video and log)

turned_into_actor 10, other 3, left_road 3, no_brake_for_lead 2

- intersection_ego_speed_optuna_confirm_002: no_brake_for_lead, policy at fault: yes. The ego had drifted about 9 m left of the recorded path, into a left lane, even though the command was RIGHT. Bus 127 merged diagonally into that lane ahead and straightened out there. The ego slowed only gradually (7.3 to 3.4 m/s) and ran into the back of the slow bus; the rear contact recorded for this run came after this front collision.
- intersection_ego_speed_optuna_confirm_008: other, policy at fault: yes. The route command was RIGHT and the recorded car stayed in the right lane, but the ego drifted about 9 m left into what appear to be oncoming lanes. Bus 127 came out of the intersection head-on in that lane and struck the ego's front. The ego was slowing (7.3 to 3.7 m/s) but never moved back out of the bus's path.
- intersection_ego_speed_optuna_confirm_013: left_road, policy at fault: yes. The route command was RIGHT, but the ego went the other way. It turned left across the multi-lane road, away from the route on the right, and slowly drove over the left edge of the road into the building frontage, where it went offroad at 10.2 s about 13 m from the recorded path. No other actors were involved. The camera view smears more as the ego gets further from the recorded path, but the wrong-way turn had already started before that.
- intersection_ego_speed_optuna_confirm_015: other, policy at fault: yes. With a RIGHT command, the ego drifted left and ended up about 8.6 m from the recorded path, in the leftmost lanes. Bus 127 turned in from the cross street into that lane heading toward the ego, which looks like oncoming traffic. The ego slowed from 7 to 3.3 m/s but didn't stop or move back right, and its front hit the bus (the camera view at impact is smeared). The ego was also rear-ended later.
- intersection_ego_speed_optuna_confirm_018: turned_into_actor, policy at fault: yes. The route command was RIGHT, but after handoff the ego veered left, ending up about 9 m left of the recorded path near the left curb. Bus 127 swung out of the intersection into those lanes heading toward the ego. The ego slowed from 7.2 to 3.1 m/s but was still in the bus's path, and the two hit front-on at 10.3 s.
- intersection_ego_speed_optuna_confirm_019: turned_into_actor, policy at fault: yes. After handoff, the ego drifted about 10 m left of the recorded path, which was far to the right for the upcoming RIGHT command, and travelled in the left lanes. It then steered right toward the route and hit bus 127, which was in the adjacent lane and approaching. The ego was braking from 7.5 to 3.6 m/s but too late, and the front contact counts as at fault.
- intersection_ego_speed_optuna_confirm_020: turned_into_actor, policy at fault: yes. The route said turn RIGHT, but the policy drifted left, off the recorded path (about 10 m off by the end), toward the left lanes. It drove at the city bus (127), which was turning out of the cross street into those lanes, and only began braking late (8.6 to 5.5 m/s). The ego's front hit the bus nearly head-on; the bus was clearly visible in the camera beforehand.
- intersection_ego_speed_optuna_confirm_021: turned_into_actor, policy at fault: yes. The route command was RIGHT, but the ego steered left across several lanes toward the left curb, ending about 11.6 m from the recorded path, and slowed almost to a stop. Bus 127, in the next lane, came alongside and the ego's side hit it (lateral collision at 11.0 s); a rear contact also happened at some point.
- intersection_ego_speed_optuna_confirm_023: left_road, policy at fault: yes. The route command was RIGHT and the recorded path ran down and to the right through the lanes, but the policy's planned path kept bending left toward the road edge. The ego left the recorded trajectory, slowly crossed the road boundary at about 3–4 m/s and went off-road into the sidewalk and building area at 10.2 s, about 13.5 m from the recorded path. No other actor was involved.
- intersection_ego_speed_optuna_confirm_026: turned_into_actor, policy at fault: yes. The route command was RIGHT, but after handoff the policy steered left across several lanes, away from the recorded path (7.3 m off by the failure). It drove into bus 127, which was in the far-left lane, and hit it head-on with its front at about 4–5 m/s.
- intersection_ego_speed_optuna_confirm_030: turned_into_actor, policy at fault: yes. The route command was RIGHT, but after handoff the ego drifted about 8 m left of the recorded path, which stayed in the right-hand lanes, and ended up in the left lanes. There it hit bus 127 front-on as the bus turned in from the intersection and came toward the ego. The ego slowed only gently (9.0 to 6.5 m/s) and never braked hard, even though the bus was clearly visible on camera from 7.3 s.
- intersection_ego_speed_optuna_confirm_038: no_brake_for_lead, policy at fault: yes. Although the route command was RIGHT, the ego drifted left, about 7 m off the recorded path, into the lane of bus 127, which was moving slower ahead of it. It kept going at about 7.4 m/s and slowed only to 5.6 m/s, too late, so it hit the back of the bus with its front. The rear contact flagged in the run came after this at-fault front collision.
- intersection_ego_speed_optuna_confirm_039: turned_into_actor, policy at fault: yes. The route said RIGHT, but the ego drifted left across lanes, ending about 9 m off the recorded path. A bus (127) turned onto the road from the cross street into those left lanes, and the ego braked late (from 8.9 to 5.5 m/s) and hit it head-on. A follower then hit the ego's rear, but only after the front collision.
- intersection_ego_speed_optuna_confirm_041: left_road, policy at fault: yes. With a RIGHT command, the ego left its route along the multi-lane road. It steered across the lanes toward the road edge, slowing from 6 to 2.9 m/s, then crossed the curb toward a building wall and sidewalk at about 10.2 s, by then 13.7 m from the human's path. No other actor was involved, and the camera view stayed recognizable before the failure, so the policy's planned path caused it.
- intersection_ego_speed_optuna_confirm_044: turned_into_actor, policy at fault: yes. The route said turn RIGHT, but the ego drifted left, away from the recorded path (5.4 m off by 8.2 s and 9.4 m off at the failure), into the lanes used by bus 127, which was coming toward it. The ego slowed from 7.4 to 3.0 m/s but still hit the bus head-on at 10.2 s. The camera smearing came after the drift had started, so it is a result of the drift, not the cause.
- intersection_ego_speed_optuna_confirm_045: turned_into_actor, policy at fault: yes. The route said RIGHT, but the ego drifted left of the recorded path, ending about 6.4 m off it. It steered into the next lane over and hit oncoming bus 127 front-first at about 7 m/s as the bus passed, slowing only slightly before contact.
- intersection_ego_speed_optuna_confirm_047: other, policy at fault: yes. The command was RIGHT, but after handoff the ego drifted about 9 m left of the recorded human path, and its planned path kept bending further left. Bus 127, which replays its recorded motion, made a turn from the intersection into the lane the ego now occupied and came toward it. The ego slowed from 7.4 to 3.5 m/s but hit the bus head-on. The bus did not react to the ego, but the collision only happened because the policy drove into a lane the real car never used.
- intersection_ego_speed_optuna_confirm_049: turned_into_actor, policy at fault: yes. The route said RIGHT, but the ego drifted left, about 7 m off the recorded human path, into the left lane. A bus (127) was turning out of the intersection into that same lane and coming toward the ego. The ego slowed only gradually, from 10 to 6.4 m/s, and its front hit the bus head-on.

## Every setting

- S1: 02eadd92 at ego_speed_scale 0.6, actor_time_shift_s -2.0: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_optuna_confirm_026)
- S2: 02eadd92 at ego_speed_scale 0.6, actor_time_shift_s -0.5: 2/2 failed, rate 42%-100% (90%), 2 possibly the simulator's (intersection_ego_speed_optuna_confirm_013, intersection_ego_speed_optuna_confirm_023)
- S3: 02eadd92 at ego_speed_scale 0.6, actor_time_shift_s 1.5: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_optuna_confirm_041)
- S4: 02eadd92 at ego_speed_scale 0.8, actor_time_shift_s -1.5: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_optuna_confirm_045)
- S5: 02eadd92 at ego_speed_scale 0.8, actor_time_shift_s -0.5: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_optuna_confirm_038)
- S6: 02eadd92 at ego_speed_scale 0.8, actor_time_shift_s 0.5: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_optuna_confirm_019)
- S7: 02eadd92 at ego_speed_scale 0.8, actor_time_shift_s 1.5: 6/6 failed, rate 69%-100% (90%), 6 possibly the simulator's (intersection_ego_speed_optuna_confirm_002, intersection_ego_speed_optuna_confirm_008, intersection_ego_speed_optuna_confirm_015, intersection_ego_speed_optuna_confirm_018, intersection_ego_speed_optuna_confirm_044, intersection_ego_speed_optuna_confirm_047)
- S8: 02eadd92 at ego_speed_scale 0.8, actor_time_shift_s 2.0: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_optuna_confirm_021)
- S9: 02eadd92 at ego_speed_scale 1.0, actor_time_shift_s 1.5: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_optuna_confirm_020)
- S10: 02eadd92 at ego_speed_scale 1.2, actor_time_shift_s 1.0: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_optuna_confirm_030)
- S11: 02eadd92 at ego_speed_scale 1.2, actor_time_shift_s 1.5: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_optuna_confirm_039)
- S12: 02eadd92 at ego_speed_scale 1.4, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_optuna_confirm_028)
- S13: 02eadd92 at ego_speed_scale 1.4, actor_time_shift_s 1.5: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (intersection_ego_speed_optuna_confirm_049)
- S14: 054b5901 at ego_speed_scale 0.6, actor_time_shift_s -1.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_optuna_confirm_040)
- S15: 054b5901 at ego_speed_scale 0.8, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_optuna_confirm_011)
- S16: 054b5901 at ego_speed_scale 0.8, actor_time_shift_s 1.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_optuna_confirm_037)
- S17: 054b5901 at ego_speed_scale 1.0, actor_time_shift_s -1.0: 0/3 failed, rate 0%-47% (90%) (intersection_ego_speed_optuna_confirm_001, intersection_ego_speed_optuna_confirm_009, intersection_ego_speed_optuna_confirm_017)
- S18: 0d76134f at ego_speed_scale 0.6, actor_time_shift_s 0.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_optuna_confirm_027)
- S19: 0d76134f at ego_speed_scale 0.8, actor_time_shift_s 1.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_optuna_confirm_035)
- S20: 0d76134f at ego_speed_scale 1.0, actor_time_shift_s 1.0: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_optuna_confirm_007)
- S21: 0d76134f at ego_speed_scale 1.4, actor_time_shift_s -1.5: 0/2 failed, rate 0%-58% (90%) (intersection_ego_speed_optuna_confirm_003, intersection_ego_speed_optuna_confirm_004)
- S22: 118a3400 at ego_speed_scale 0.6, actor_time_shift_s 2.0: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_optuna_confirm_032)
- S23: 118a3400 at ego_speed_scale 0.8, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_optuna_confirm_024)
- S24: 118a3400 at ego_speed_scale 0.8, actor_time_shift_s 1.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_optuna_confirm_046)
- S25: 118a3400 at ego_speed_scale 1.2, actor_time_shift_s 1.5: 0/2 failed, rate 0%-58% (90%) (intersection_ego_speed_optuna_confirm_005, intersection_ego_speed_optuna_confirm_006)
- S26: 13a9767e at ego_speed_scale 0.6, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_optuna_confirm_033)
- S27: 13a9767e at ego_speed_scale 0.8, actor_time_shift_s -1.0: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_optuna_confirm_034)
- S28: 13a9767e at ego_speed_scale 1.0, actor_time_shift_s -2.0: 0/6 failed, rate 0%-31% (90%) (intersection_ego_speed_optuna_confirm_014, intersection_ego_speed_optuna_confirm_016, intersection_ego_speed_optuna_confirm_022, intersection_ego_speed_optuna_confirm_029, intersection_ego_speed_optuna_confirm_036, intersection_ego_speed_optuna_confirm_043)
- S29: 13a9767e at ego_speed_scale 1.4, actor_time_shift_s 1.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_optuna_confirm_010)
- S30: 1a7b81b8 at ego_speed_scale 0.6, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_optuna_confirm_025)
- S31: 1a7b81b8 at ego_speed_scale 0.8, actor_time_shift_s 1.0: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_optuna_confirm_012)
- S32: 1a7b81b8 at ego_speed_scale 0.8, actor_time_shift_s 1.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_optuna_confirm_048)
- S33: 1a7b81b8 at ego_speed_scale 1.2, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_optuna_confirm_031)
- S34: 1a7b81b8 at ego_speed_scale 1.4, actor_time_shift_s -1.0: 0/1 failed, rate 0%-73% (90%) (intersection_ego_speed_optuna_confirm_042)

## Provenance

Plan: `plan.json` (rationale: Ten scenes are tagged intersection and have a recorded crossing vehicle. Four of them already failed at the default speed and timing: 048b974e, 05a1d902, 0e02fb8c and 0f1f60d5. Three of those four failures had a closest approach above 1 m, so they were probably road departures with no link to the crossing car. Cases found there would not show the effect of the ego's speed or the crossing car's timing, so these four are left out.

The 6 remaining scenes passed at the default settings. Several came close to the crossing car: 054b5901 at 0.26 m and 13a9767e at 0.12 m, so they are good candidates. 0d76134f is weak: the ego drove only 7 m there, but it is kept so that 5 different scenes stay reachable.

Other actors follow their recorded tracks, as in Euro NCAP tests. The retime class is automobile. retime_tracks shifts only the crossing car in each scene, so the other recorded cars stay as recorded.

The budget is 49 runs (7 rounds of 7), close to the ~50 asked for. The goal is the top 5 settings, one per scene, whose failure rate is surely above 0.5. Confirming one setting takes about 5 runs, almost all failures, so confirming 5 takes about 25 runs. That leaves about 24 for exploration, so the goal may not be met in full. If it is not, the study reports the strongest cases found and their near misses.

What the plan cannot answer:
- All 6 scenes are recorded as going straight ('turn: none'). None has both a recorded crossing car and a turn while also passing at the default settings, so turning across traffic is not covered.
- Above ×1.0, the ego starts behind its recorded position and is off the recording for the first second or two of the warm-up.
- The crossing car keeps its recorded speed, as the brief asked. Only its timing changes.
- No planner delay or perception error is applied.). Report written by claude-opus-5-5 from `results` in 18 s; every count above is computed from the queue, not written by the model.

49 of 49 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
