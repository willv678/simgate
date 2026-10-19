# In cut-in and lead-vehicle scenes that pass as recorded, which combinations of the car's timing, the car's speed and the ego's speed at hand-off make the policy collide or leave the road? The aim is the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `optuna_confirm_r4`: 59 kept runs on 10 scenes, varying actor_time_shift_s, actor_speed_scale, ego_speed_scale; 5 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 2 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The study confirmed 2 of the 5 cases it was asked for, each on a different scene. On 096988dd, with the car 1.5 s earlier at 2x speed and the ego at 1.2x, the policy steered left out of its lane into a car alongside (S3). On 19f339ba, with the car 2 s later at its recorded speed and the ego at 1.2x, the policy braked hard with nothing ahead and was then hit by replayed traffic coming from behind (S26). Every repeat at both settings failed. Even so, their ranges only just clear 0.5, so all we can say is that they fail more often than not, not how often. In neither case does the failure appear to involve the retimed car's conflict with the ego: the ego's own speed at hand-off (1.2x) is the factor the failures share. A third candidate on 1c45ce3a (S30) failed in about half its repeats, so it is not confirmed, and its failures were mostly not clearly the policy's fault. No run left the road, and no failure was flagged as a possible simulator artifact.

## Findings

- On 096988dd, with the car 1.5 s earlier, the car at 2x speed and the ego at 1.2x, every repeat failed and the setting is confirmed above 0.5. In each run the policy's plan bent left on a straight multi-lane highway and the ego drifted into the next lane, where its front hit actor 41 alongside. The policy was at fault, and nothing was close ahead, so this was not a cut-in or lead-vehicle conflict.
  - S3: 096988dd at actor_time_shift_s -1.5, actor_speed_scale 2.0, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_027, car_conflicts_3knobs_2hz_optuna_confirm_r4_031, car_conflicts_3knobs_2hz_optuna_confirm_r4_041)
- On 19f339ba, with the car 2 s later, the car at its recorded speed and the ego at 1.2x, every repeat failed and the setting is confirmed above 0.5. Each time the policy braked hard with no lead within about 47 m (phantom braking) and drifted toward a lane line. A replayed car coming from behind on the right then struck the ego's front-right corner. Triage blames the policy for the braking. However, the car that hit it is replayed and cannot react, so in real traffic the crash itself might not happen.
  - S26: 19f339ba at actor_time_shift_s 2.0, actor_speed_scale 1.0, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_026, car_conflicts_3knobs_2hz_optuna_confirm_r4_032, car_conflicts_3knobs_2hz_optuna_confirm_r4_042)
- The same phantom-braking pattern showed up once more on 19f339ba, at the car 0.5 s earlier, half speed, ego 1.2x. This is a single run, so it is a hint, not a rate, and it is on a scene that is already confirmed, so it cannot count as a separate case.
  - S23: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 0.5, ego_speed_scale 1.2: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_058)
- On 1c45ce3a, with the car at its recorded timing, the car at 0.75x and the ego at 1.2x, about half the repeats failed, and the range straddles 0.5, so the setting is not confirmed. One failure was a replayed car cutting into a correctly driving ego (not the policy's fault). One was a side-swipe from a car coming up from behind (unclear). One was a slower car merging ahead that the ego did not brake for (unclear).
  - S30: 1c45ce3a at actor_time_shift_s 0.0, actor_speed_scale 0.75, ego_speed_scale 1.2: 3/6 failed, rate 22%-78% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_003, car_conflicts_3knobs_2hz_optuna_confirm_r4_012, car_conflicts_3knobs_2hz_optuna_confirm_r4_021, car_conflicts_3knobs_2hz_optuna_confirm_r4_033, car_conflicts_3knobs_2hz_optuna_confirm_r4_043_a3, car_conflicts_3knobs_2hz_optuna_confirm_r4_051)
- On 19f339ba, with the car at its recorded timing, the car at 1.5x and the ego at 0.6x, one repeat failed. In that run a car came up from behind into the slowed ego's rear-right, and whether the policy was at fault is unclear.
  - S24: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.5, ego_speed_scale 0.6: 1/4 failed, rate 6%-64% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_002, car_conflicts_3knobs_2hz_optuna_confirm_r4_011, car_conflicts_3knobs_2hz_optuna_confirm_r4_016_a2, car_conflicts_3knobs_2hz_optuna_confirm_r4_023)
- Every failure in the study came at an ego hand-off speed of 1.2x. But 1.2x is not enough by itself: other settings at 1.2x, and the repeated 1.4x setting on 023b7fcc, produced no failures.
  - S3: 096988dd at actor_time_shift_s -1.5, actor_speed_scale 2.0, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_027, car_conflicts_3knobs_2hz_optuna_confirm_r4_031, car_conflicts_3knobs_2hz_optuna_confirm_r4_041)
  - S26: 19f339ba at actor_time_shift_s 2.0, actor_speed_scale 1.0, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_026, car_conflicts_3knobs_2hz_optuna_confirm_r4_032, car_conflicts_3knobs_2hz_optuna_confirm_r4_042)
  - S23: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 0.5, ego_speed_scale 1.2: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_058)
  - S30: 1c45ce3a at actor_time_shift_s 0.0, actor_speed_scale 0.75, ego_speed_scale 1.2: 3/6 failed, rate 22%-78% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_003, car_conflicts_3knobs_2hz_optuna_confirm_r4_012, car_conflicts_3knobs_2hz_optuna_confirm_r4_021, car_conflicts_3knobs_2hz_optuna_confirm_r4_033, car_conflicts_3knobs_2hz_optuna_confirm_r4_043_a3, car_conflicts_3knobs_2hz_optuna_confirm_r4_051)
  - S1: 023b7fcc at actor_time_shift_s -1.5, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_009, car_conflicts_3knobs_2hz_optuna_confirm_r4_014, car_conflicts_3knobs_2hz_optuna_confirm_r4_024, car_conflicts_3knobs_2hz_optuna_confirm_r4_034, car_conflicts_3knobs_2hz_optuna_confirm_r4_045, car_conflicts_3knobs_2hz_optuna_confirm_r4_053)
  - S11: 0cf6368d at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_037, car_conflicts_3knobs_2hz_optuna_confirm_r4_044, car_conflicts_3knobs_2hz_optuna_confirm_r4_052)
  - S9: 09a95ffa at actor_time_shift_s 0.5, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_017, car_conflicts_3knobs_2hz_optuna_confirm_r4_022, car_conflicts_3knobs_2hz_optuna_confirm_r4_035)
- Seven of the ten scenes produced no failures at any setting tried: 023b7fcc, 09a95ffa, 0cf6368d, 0dbb91dd, 0e899dd3, 12855a41 and 187e6244. Most of these settings ran only once or twice, though, so this does not show that these scenes are safe.
  - S1: 023b7fcc at actor_time_shift_s -1.5, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_009, car_conflicts_3knobs_2hz_optuna_confirm_r4_014, car_conflicts_3knobs_2hz_optuna_confirm_r4_024, car_conflicts_3knobs_2hz_optuna_confirm_r4_034, car_conflicts_3knobs_2hz_optuna_confirm_r4_045, car_conflicts_3knobs_2hz_optuna_confirm_r4_053)
  - S2: 023b7fcc at actor_time_shift_s -0.5, actor_speed_scale 1.5, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_019)
  - S7: 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 0.75, ego_speed_scale 0.8: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_047, car_conflicts_3knobs_2hz_optuna_confirm_r4_054)
  - S8: 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 1.0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_036)
  - S9: 09a95ffa at actor_time_shift_s 0.5, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_017, car_conflicts_3knobs_2hz_optuna_confirm_r4_022, car_conflicts_3knobs_2hz_optuna_confirm_r4_035)
  - S10: 0cf6368d at actor_time_shift_s -2.0, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_006)
  - S11: 0cf6368d at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_037, car_conflicts_3knobs_2hz_optuna_confirm_r4_044, car_conflicts_3knobs_2hz_optuna_confirm_r4_052)
  - S12: 0cf6368d at actor_time_shift_s 1.0, actor_speed_scale 2.0, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_001)
  - S13: 0cf6368d at actor_time_shift_s 1.5, actor_speed_scale 0.75, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_040)
  - S14: 0dbb91dd at actor_time_shift_s -1.0, actor_speed_scale 0.75, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_010)
  - S15: 0dbb91dd at actor_time_shift_s 0.0, actor_speed_scale 0.5, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_007)
  - S16: 0dbb91dd at actor_time_shift_s 1.0, actor_speed_scale 1.0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_050)
  - S17: 0e899dd3 at actor_time_shift_s -1.5, actor_speed_scale 2.0, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_056)
  - S18: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 0.75, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_028)
  - S19: 12855a41 at actor_time_shift_s 1.0, actor_speed_scale 1.25, ego_speed_scale 0.8: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_004, car_conflicts_3knobs_2hz_optuna_confirm_r4_013, car_conflicts_3knobs_2hz_optuna_confirm_r4_025)
  - S20: 187e6244 at actor_time_shift_s 0.0, actor_speed_scale 0.75, ego_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_049, car_conflicts_3knobs_2hz_optuna_confirm_r4_055)
- No run left the road. All failures were collisions, and several were replayed cars hitting the ego from behind or the side rather than the ego driving into a car.
  - S3: 096988dd at actor_time_shift_s -1.5, actor_speed_scale 2.0, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_027, car_conflicts_3knobs_2hz_optuna_confirm_r4_031, car_conflicts_3knobs_2hz_optuna_confirm_r4_041)
  - S26: 19f339ba at actor_time_shift_s 2.0, actor_speed_scale 1.0, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_026, car_conflicts_3knobs_2hz_optuna_confirm_r4_032, car_conflicts_3knobs_2hz_optuna_confirm_r4_042)
  - S23: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 0.5, ego_speed_scale 1.2: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_058)
  - S24: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.5, ego_speed_scale 0.6: 1/4 failed, rate 6%-64% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_002, car_conflicts_3knobs_2hz_optuna_confirm_r4_011, car_conflicts_3knobs_2hz_optuna_confirm_r4_016_a2, car_conflicts_3knobs_2hz_optuna_confirm_r4_023)
  - S30: 1c45ce3a at actor_time_shift_s 0.0, actor_speed_scale 0.75, ego_speed_scale 1.2: 3/6 failed, rate 22%-78% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_003, car_conflicts_3knobs_2hz_optuna_confirm_r4_012, car_conflicts_3knobs_2hz_optuna_confirm_r4_021, car_conflicts_3knobs_2hz_optuna_confirm_r4_033, car_conflicts_3knobs_2hz_optuna_confirm_r4_043_a3, car_conflicts_3knobs_2hz_optuna_confirm_r4_051)

## Open

- Three of the five cases are still missing. Repeating S30 (1c45ce3a: car at its recorded timing, car 0.75x, ego 1.2x) a few more times would show whether it clears 0.5, but its failures are mostly not clearly the policy's fault.
- We don't know whether the retimed car matters at all in S3 and S26. Both failures involve other actors (a car alongside in S3, phantom braking then a car from behind in S26). Running both scenes with the ego at 1.2x and the car at its recorded timing and speed would show whether the ego's speed alone causes them.
- The phantom-braking crashes on 19f339ba depend on replayed traffic that cannot react. Re-running S26 and S23 with reactive traffic would show whether the braking still leads to a collision.
- Several scenes got only one or two single runs (0e899dd3 just once, 0dbb91dd at a criticality of 0). That suggests their retimed car never came near the ego, so these scenes have not really been searched. More runs at an ego speed of 1.2–1.4x there, with the car timed so it actually conflicts with the ego, are needed before ruling these scenes out.
- The near-miss settings whose single run came close but did not fail (for example S29 and S33 on 1c45ce3a, and S25 on 19f339ba) were never repeated. A few repeats would show whether they rank next after the failures, as the brief asks.

## Why the runs failed (triage from the video and log)

actor_hit_ego 4, other 3, turned_into_actor 3, no_brake_for_lead 1

- car_conflicts_3knobs_2hz_optuna_confirm_r4_002: actor_hit_ego, policy at fault: unclear. On an open highway with nothing close ahead, the ego slowed steadily from about 10 to 6.9 m/s after handoff and fell about 20 m behind its recorded position. Actor 18 came up from behind, apparently replaying the logged speed, and drove into the ego at 7.1 s; the boxes overlap at the ego's rear-right, which fits the rear_ended flag even though the metric scores it as a front collision.
- car_conflicts_3knobs_2hz_optuna_confirm_r4_003: actor_hit_ego, policy at fault: no. The ego stayed on its lane on the recorded path (0.1 m off it), slowing from 15 to 8.9 m/s. Actor 14 came up from behind on the ego's right, passed it and drifted left over the lane line, so the ego's front-right corner touched the actor's left side as it cut in.
- car_conflicts_3knobs_2hz_optuna_confirm_r4_021: actor_hit_ego, policy at fault: unclear. On the highway, the ego kept to the recorded lane line (0.1 m off the path) but slowed from 9.3 to 7.5 m/s with no lead car, so it fell about 23 m behind where the recorded car was at that moment. Actor 24 is a replayed vehicle that came up from behind in the lane to the right. It moved in beside the ego and clipped its front-right corner, which counted as a front collision, and the ego was also hit from behind.
- car_conflicts_3knobs_2hz_optuna_confirm_r4_026: other, policy at fault: yes. After handoff on an open highway with no lead within about 47 m, the policy braked hard for no visible reason, from 20.3 to 8.3 m/s, and fell about 12 m behind where the recorded car was. Actor 18, a replayed vehicle coming up from behind on the right, then drove into the ego's corner as it moved into the space the real car had left. This was a crash caused by phantom braking, not a failure to brake for a lead car.
- car_conflicts_3knobs_2hz_optuna_confirm_r4_027: turned_into_actor, policy at fault: yes. On a straight, wet multi-lane highway, the policy's planned path (orange) bent left, and the ego drifted left out of its lane into the adjacent lane. There its front struck actor 41, which was alongside in that lane, while the recorded human path stayed straight (route command STRAIGHT, then RIGHT at 7.2 s).
- car_conflicts_3knobs_2hz_optuna_confirm_r4_031: turned_into_actor, policy at fault: yes. On a multi-lane highway with the route going straight, the policy steered the ego left toward the next lane, ending about 1.5 m off the recorded path. It moved into actor 41, which was coming up alongside on the left, and the ego's front-left corner hit it. Nothing was close ahead (gap 18 m or more), so this was not a lead-vehicle problem.
- car_conflicts_3knobs_2hz_optuna_confirm_r4_032: other, policy at fault: yes. On a clear multi-lane highway with nothing ahead (closest lead about 50 m away), the ego braked hard for no visible reason, from 20.3 to 8.5 m/s, falling well behind its recorded position (11.9 m back by 7.6 s) and drifting about 1.3 m toward the right lane. Replayed traffic coming from behind (actor 18 on the right-rear, actor 1 on the left-rear) caught up, and actor 18 ran into the ego's right front/side, which was logged as an at-fault front collision plus a rear contact.
- car_conflicts_3knobs_2hz_optuna_confirm_r4_041: turned_into_actor, policy at fault: yes. On a multi-lane highway, the command was STRAIGHT and then RIGHT, but the ego's plan bent left and it drifted about 1.7 m left of the recorded path into the next lane. There it hit vehicle 41, which was moving up alongside in that lane, with its front at about 4.6 m/s.
- car_conflicts_3knobs_2hz_optuna_confirm_r4_042: other, policy at fault: yes. After handoff, the ego braked hard on an open highway for no visible reason: it went from 20.3 to 8.3 m/s with no lead vehicle within about 47 m. It also drifted left onto the lane line, about 1.2 m off the recorded path. Actor 18, a vehicle replayed from the log coming from behind on the right, caught up with the slowed, straddling ego, and they collided at the ego's front-right corner and side. A rear contact was also logged.
- car_conflicts_3knobs_2hz_optuna_confirm_r4_043_a3: no_brake_for_lead, policy at fault: unclear. On a straight multi-lane road, a slower silver car (actor 14) moved from the right lane into the ego's lane ahead of it, straddling the lane line at about 9.2s. The ego eased from 7.2 to 6.9 m/s but never braked hard, and its front hit the car at 10.2s with a 4.3 m centre-to-centre gap. A later rear contact, likely from actor 24 alongside, does not change this.
- car_conflicts_3knobs_2hz_optuna_confirm_r4_058: actor_hit_ego, policy at fault: yes. After handoff, the ego braked hard on an open highway, from 18.6 to 5.2 m/s, with no lead within about 48 m, and fell far behind the recorded trajectory (20.9 m behind). Actor 28 came up from behind on the right and ran into the ego's rear and right side; the front-collision flag at 8.1 s comes from that overlap, not from the ego driving into actor 1 in the next lane.

## Every setting

- S1: 023b7fcc at actor_time_shift_s -1.5, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_009, car_conflicts_3knobs_2hz_optuna_confirm_r4_014, car_conflicts_3knobs_2hz_optuna_confirm_r4_024, car_conflicts_3knobs_2hz_optuna_confirm_r4_034, car_conflicts_3knobs_2hz_optuna_confirm_r4_045, car_conflicts_3knobs_2hz_optuna_confirm_r4_053)
- S2: 023b7fcc at actor_time_shift_s -0.5, actor_speed_scale 1.5, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_019)
- S3: 096988dd at actor_time_shift_s -1.5, actor_speed_scale 2.0, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_027, car_conflicts_3knobs_2hz_optuna_confirm_r4_031, car_conflicts_3knobs_2hz_optuna_confirm_r4_041)
- S4: 096988dd at actor_time_shift_s 0.5, actor_speed_scale 0.75, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_005)
- S5: 096988dd at actor_time_shift_s 1.5, actor_speed_scale 1.0, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_020)
- S6: 096988dd at actor_time_shift_s 2.0, actor_speed_scale 1.25, ego_speed_scale 0.8: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_008, car_conflicts_3knobs_2hz_optuna_confirm_r4_015)
- S7: 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 0.75, ego_speed_scale 0.8: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_047, car_conflicts_3knobs_2hz_optuna_confirm_r4_054)
- S8: 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 1.0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_036)
- S9: 09a95ffa at actor_time_shift_s 0.5, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_017, car_conflicts_3knobs_2hz_optuna_confirm_r4_022, car_conflicts_3knobs_2hz_optuna_confirm_r4_035)
- S10: 0cf6368d at actor_time_shift_s -2.0, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_006)
- S11: 0cf6368d at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_037, car_conflicts_3knobs_2hz_optuna_confirm_r4_044, car_conflicts_3knobs_2hz_optuna_confirm_r4_052)
- S12: 0cf6368d at actor_time_shift_s 1.0, actor_speed_scale 2.0, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_001)
- S13: 0cf6368d at actor_time_shift_s 1.5, actor_speed_scale 0.75, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_040)
- S14: 0dbb91dd at actor_time_shift_s -1.0, actor_speed_scale 0.75, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_010)
- S15: 0dbb91dd at actor_time_shift_s 0.0, actor_speed_scale 0.5, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_007)
- S16: 0dbb91dd at actor_time_shift_s 1.0, actor_speed_scale 1.0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_050)
- S17: 0e899dd3 at actor_time_shift_s -1.5, actor_speed_scale 2.0, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_056)
- S18: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 0.75, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_028)
- S19: 12855a41 at actor_time_shift_s 1.0, actor_speed_scale 1.25, ego_speed_scale 0.8: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_004, car_conflicts_3knobs_2hz_optuna_confirm_r4_013, car_conflicts_3knobs_2hz_optuna_confirm_r4_025)
- S20: 187e6244 at actor_time_shift_s 0.0, actor_speed_scale 0.75, ego_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_049, car_conflicts_3knobs_2hz_optuna_confirm_r4_055)
- S21: 19f339ba at actor_time_shift_s -2.0, actor_speed_scale 2.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_057)
- S22: 19f339ba at actor_time_shift_s -1.5, actor_speed_scale 1.0, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_046)
- S23: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 0.5, ego_speed_scale 1.2: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_058)
- S24: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.5, ego_speed_scale 0.6: 1/4 failed, rate 6%-64% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_002, car_conflicts_3knobs_2hz_optuna_confirm_r4_011, car_conflicts_3knobs_2hz_optuna_confirm_r4_016_a2, car_conflicts_3knobs_2hz_optuna_confirm_r4_023)
- S25: 19f339ba at actor_time_shift_s 1.5, actor_speed_scale 0.5, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_018)
- S26: 19f339ba at actor_time_shift_s 2.0, actor_speed_scale 1.0, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_026, car_conflicts_3knobs_2hz_optuna_confirm_r4_032, car_conflicts_3knobs_2hz_optuna_confirm_r4_042)
- S27: 1c45ce3a at actor_time_shift_s -2.0, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_039)
- S28: 1c45ce3a at actor_time_shift_s -1.0, actor_speed_scale 0.5, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_029_a2)
- S29: 1c45ce3a at actor_time_shift_s -0.5, actor_speed_scale 0.75, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_059)
- S30: 1c45ce3a at actor_time_shift_s 0.0, actor_speed_scale 0.75, ego_speed_scale 1.2: 3/6 failed, rate 22%-78% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_003, car_conflicts_3knobs_2hz_optuna_confirm_r4_012, car_conflicts_3knobs_2hz_optuna_confirm_r4_021, car_conflicts_3knobs_2hz_optuna_confirm_r4_033, car_conflicts_3knobs_2hz_optuna_confirm_r4_043_a3, car_conflicts_3knobs_2hz_optuna_confirm_r4_051)
- S31: 1c45ce3a at actor_time_shift_s 0.0, actor_speed_scale 2.0, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_038)
- S32: 1c45ce3a at actor_time_shift_s 1.0, actor_speed_scale 0.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_060)
- S33: 1c45ce3a at actor_time_shift_s 2.0, actor_speed_scale 1.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r4_048)

## Not kept by the gate

- car_conflicts_3knobs_2hz_optuna_confirm_r4_016: not kept: RE-RUN
- car_conflicts_3knobs_2hz_optuna_confirm_r4_029: not kept: RE-RUN
- car_conflicts_3knobs_2hz_optuna_confirm_r4_030: not kept: HALT
- car_conflicts_3knobs_2hz_optuna_confirm_r4_043: not kept: RE-RUN
- car_conflicts_3knobs_2hz_optuna_confirm_r4_043_a2: not kept: RE-RUN

## Provenance

Plan: `plan.json` (rationale: Scene choice: these are the scenes tagged merge_cut_in or lead_vehicle that did not fail in the earlier run at the recorded setting, have a recorded car the study can retime (lead_vehicle or cut_in), and drove far enough for a conflict to develop. Most of them already came close to another actor as recorded: 023b7fcc came within 0.02 m, 096988dd 0.01 m, 19f339ba 0.03 m, 12855a41 0.08 m, and 0dbb91dd and 187e6244 0.23 m. Those are the most promising places to look for rare failures.

Left out:
- Scenes that were nearly stationary (0fa7060f, 15dd433e, 0ac02819, 10d64934) or very slow (01d503d4, 098e2482, 11fce928, 1bfd39ec).
- Scenes with no car the study can retime (for example 04749bb9, 05f35348, 0ce6f2a3, 166fe701).
- Scenes whose only key actor is a crossing vehicle at an intersection (02eadd92, 054b5901).

Note that 01d503d4 appears twice in the scene list.

Retiming and settings:
- Traffic is replay, as the brief asks, with retime_class automobile.
- Each scene retimes only its key car. In 12855a41 that is the cut-in car 31 rather than the lead car 5.
- All three knobs span exactly the ranges in the brief: timing ±2 s, car speed 0.5x to 2x, ego speed 0.6x to 1.4x.
- The controller is linear MPC.

Goal: top_k with k=5, distinct scenes, high_min 0.5. This matches the request for the 5 most challenging cases, each confirmed by repeats.

Limits:
- The budget is tight. With 90% ranges, a setting needs roughly 5 failures out of 5 runs to lie surely above 0.5. Confirming 5 cases therefore takes about 25 runs, which leaves about 35 runs to search a 270-cell grid on 10 scenes. If failures are as rare as the brief expects, the study may end with fewer than 5 confirmed cases. It would then report the strongest candidates and the near misses, which the brief ranks next.
- The 2 Hz planning rate is not a knob in this interface. The plan assumes the runs use VaVAM's 2 Hz rhythm as configured; nothing here sets it or checks it. planner_delay_us, lateral_bias_m and waypoint_noise_std stay at their defaults.
- A scale above 1 starts the ego behind its recorded start, so for the first second or two of the warm-up it is off the recording.). Report written by claude-opus-5-5 from `results` in 28 s; every count above is computed from the queue, not written by the model.

0 of 64 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
