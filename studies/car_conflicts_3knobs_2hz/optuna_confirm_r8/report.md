# In cut-in and lead-vehicle scenes that pass as recorded, which combinations of the car's timing, the car's speed and the ego's speed at hand-off make the policy collide or leave the road? The aim is the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `optuna_confirm_r8`: 60 kept runs on 10 scenes, varying actor_time_shift_s, actor_speed_scale, ego_speed_scale; 4 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 1 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The goal was not met. Only one challenging case is confirmed: scene 19f339ba with the car 1 s early, at 0.5x speed, and the ego at 1.2x its recorded speed (S22). Every repeat there failed, and its 90% range lies above 0.5. All confirmed failures and most of the hints come from this one highway scene. There, after hand-off, the policy braked hard with no lead car close ahead and drifted left. It then hit the car in the left lane, or was side-swiped by a replayed car coming up from behind. In that scene the ego's hand-off speed seems to matter more than the retimed car's timing or speed: failures appeared across many car settings at 1.0x ego speed and above, and none at 0.6x or 0.8x. That pattern rests on one run per setting, so it is a hint, not a rate. No other scene produced a failure the policy was confirmed to cause, and none of the failures carry possible simulator artifacts.

## Findings

- The one confirmed challenging case is scene 19f339ba with the car 1 s early, at 0.5x speed, and the ego at 1.2x. Every repeat failed, and the 90% range lies above 0.5. In each run the policy braked hard on an open highway with no lead nearby, drifted left, and either hit actor 1 in the left lane or was struck on the side by the replayed actor 28.
  - S22: 19f339ba at actor_time_shift_s -1.0, actor_speed_scale 0.5, ego_speed_scale 1.2: 4/4 failed, rate 60%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_006, car_conflicts_3knobs_2hz_optuna_confirm_r8_011, car_conflicts_3knobs_2hz_optuna_confirm_r8_021, car_conflicts_3knobs_2hz_optuna_confirm_r8_056)
- On scene 19f339ba, the policy failed at many different timings and speeds of the car (from 2 s early to 1.5 s late, from 0.5x to 1.5x) whenever the ego took over at 1.0x its recorded speed or faster. The triage puts the nearest lead 40 m or more away in these runs, so the retimed car does not seem to be what triggers them. Only the 1.5 s-late, 0.75x setting was repeated, and it failed every time. The others are single runs.
  - S19: 19f339ba at actor_time_shift_s -2.0, actor_speed_scale 0.5, ego_speed_scale 1.0: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_058)
  - S20: 19f339ba at actor_time_shift_s -1.5, actor_speed_scale 0.5, ego_speed_scale 1.4: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_029)
  - S23: 19f339ba at actor_time_shift_s -1.0, actor_speed_scale 0.5, ego_speed_scale 1.4: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_003)
  - S26: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 1.5, ego_speed_scale 1.4: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_048)
  - S29: 19f339ba at actor_time_shift_s 1.5, actor_speed_scale 0.75, ego_speed_scale 1.4: 2/2 failed, rate 42%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_017, car_conflicts_3knobs_2hz_optuna_confirm_r8_046)
- On scene 19f339ba, every setting with the ego at 0.6x or 0.8x speed passed. One run at 1.2x with the car 2 s late at 1.0x also passed. These are single runs each.
  - S21: 19f339ba at actor_time_shift_s -1.0, actor_speed_scale 0.5, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_059)
  - S24: 19f339ba at actor_time_shift_s -1.0, actor_speed_scale 1.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_049)
  - S25: 19f339ba at actor_time_shift_s -1.0, actor_speed_scale 2.0, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_027_a2)
  - S27: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_047)
  - S28: 19f339ba at actor_time_shift_s 1.0, actor_speed_scale 1.5, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_002)
  - S30: 19f339ba at actor_time_shift_s 2.0, actor_speed_scale 1.0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_039)
- Several 19f339ba failures came from the replayed actor 28, which does not react to the ego, running into the ego after the policy slowed for no reason and straddled the lane line. The triage still blames the policy, because it braked without cause and drifted, but part of how these runs ended comes from non-reactive replay traffic.
  - S19: 19f339ba at actor_time_shift_s -2.0, actor_speed_scale 0.5, ego_speed_scale 1.0: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_058)
  - S20: 19f339ba at actor_time_shift_s -1.5, actor_speed_scale 0.5, ego_speed_scale 1.4: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_029)
  - S22: 19f339ba at actor_time_shift_s -1.0, actor_speed_scale 0.5, ego_speed_scale 1.2: 4/4 failed, rate 60%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_006, car_conflicts_3knobs_2hz_optuna_confirm_r8_011, car_conflicts_3knobs_2hz_optuna_confirm_r8_021, car_conflicts_3knobs_2hz_optuna_confirm_r8_056)
- Scene 023b7fcc has one failure the policy caused, which needs confirming. With the car 0.5 s early at 0.5x and the ego at 1.2x, the ego bent left against its route command and side-swiped a car in the next lane, in dense, slow traffic. Of the two runs at this setting, one failed.
  - S1: 023b7fcc at actor_time_shift_s -0.5, actor_speed_scale 0.5, ego_speed_scale 1.2: 1/2 failed, rate 12%-88% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_030_a2, car_conflicts_3knobs_2hz_optuna_confirm_r8_031)
- The failures on scene 1c45ce3a are not the policy's. With the car 1 s early at 0.5x and the ego at 0.8x, a replayed car from the right lane merged into the ego's lane and struck its front-right corner. Triage judged one of these runs not the policy's fault and the other unclear.
  - S31: 1c45ce3a at actor_time_shift_s -1.0, actor_speed_scale 0.5, ego_speed_scale 0.8: 2/3 failed, rate 25%-92% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_036, car_conflicts_3knobs_2hz_optuna_confirm_r8_041, car_conflicts_3knobs_2hz_optuna_confirm_r8_051)
- Scenes 0e899dd3, 096988dd and 09a95ffa held up under repeats at their most critical settings. No run failed there, and the upper ends of their ranges sit below 0.5.
  - S13: 0e899dd3 at actor_time_shift_s -2.0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_004, car_conflicts_3knobs_2hz_optuna_confirm_r8_014, car_conflicts_3knobs_2hz_optuna_confirm_r8_025, car_conflicts_3knobs_2hz_optuna_confirm_r8_034, car_conflicts_3knobs_2hz_optuna_confirm_r8_044, car_conflicts_3knobs_2hz_optuna_confirm_r8_054)
  - S6: 096988dd at actor_time_shift_s 0.5, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_001, car_conflicts_3knobs_2hz_optuna_confirm_r8_024, car_conflicts_3knobs_2hz_optuna_confirm_r8_033, car_conflicts_3knobs_2hz_optuna_confirm_r8_043, car_conflicts_3knobs_2hz_optuna_confirm_r8_053)
  - S9: 09a95ffa at actor_time_shift_s 1.0, actor_speed_scale 2.0, ego_speed_scale 1.2: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_020, car_conflicts_3knobs_2hz_optuna_confirm_r8_023, car_conflicts_3knobs_2hz_optuna_confirm_r8_032, car_conflicts_3knobs_2hz_optuna_confirm_r8_042, car_conflicts_3knobs_2hz_optuna_confirm_r8_052)
- Scenes 0cf6368d, 0dbb91dd, 12855a41 and 187e6244 produced no failures, but each setting there ran only once or twice, so these scenes are barely searched rather than shown safe.
  - S10: 0cf6368d at actor_time_shift_s -2.0, actor_speed_scale 0.75, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_008)
  - S11: 0cf6368d at actor_time_shift_s 1.5, actor_speed_scale 1.5, ego_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_009, car_conflicts_3knobs_2hz_optuna_confirm_r8_015)
  - S12: 0dbb91dd at actor_time_shift_s 1.5, actor_speed_scale 0.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_038)
  - S14: 12855a41 at actor_time_shift_s -1.5, actor_speed_scale 0.5, ego_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_026, car_conflicts_3knobs_2hz_optuna_confirm_r8_035)
  - S15: 12855a41 at actor_time_shift_s -1.0, actor_speed_scale 1.0, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_018)
  - S16: 187e6244 at actor_time_shift_s -1.0, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_050)
  - S17: 187e6244 at actor_time_shift_s 0.5, actor_speed_scale 0.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_060)
  - S18: 187e6244 at actor_time_shift_s 0.5, actor_speed_scale 1.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_005)

## Open

- Four more cases on distinct scenes are still needed. The best lead is the 023b7fcc setting (car 0.5 s early, 0.5x speed, ego 1.2x), where the policy was at fault. About four more repeats there would confirm or drop it (S1).
- Whether the 19f339ba failures depend on the retimed car at all is untested. Running the car as recorded (no shift, 1.0x) with the ego at 1.0x, 1.2x and 1.4x, a few repeats each, would show whether the ego's hand-off speed alone drives the phantom braking (S19, S20, S22, S23, S26, S29).
- The phantom braking with a left drift on 19f339ba may be a general fault of the policy at higher hand-off speeds rather than a cut-in or lead-vehicle conflict. Checking it on other open-highway scenes would tell which.
- Scenes 0dbb91dd, 187e6244, 0cf6368d and 12855a41 got only a few single runs. Close approaches as recorded made 0dbb91dd and 187e6244 promising, and they need more search before they can be ruled out.
- Near misses cannot be ranked from these results, because closest-approach distances are not reported. The brief ranks near misses next after failures, so the missing confirmed cases cannot be backfilled with them.

## Why the runs failed (triage from the video and log)

turned_into_actor 7, other 4, actor_hit_ego 2

- car_conflicts_3knobs_2hz_optuna_confirm_r8_003: turned_into_actor, policy at fault: yes. On an open multi-lane highway, the ego braked hard for no visible reason (21.9 → 5.9 m/s, with the nearest lead more than 40 m away), so actor 1 in the left lane caught up and drew alongside. The ego's planned path then bent left and its front hit actor 1 as that car passed on the left. The ego was also rear-ended by traffic behind it.
- car_conflicts_3knobs_2hz_optuna_confirm_r8_006: turned_into_actor, policy at fault: yes. On a multi-lane highway, the ego braked hard from about 20 to 8 m/s with no lead nearby (the nearest was about 48 m ahead). Actor 1 in the left lane kept its speed and pulled ahead. Meanwhile the ego's plan bent left into that lane, and the ego cut across the lane line and hit actor 1's rear-right corner with its front. The phantom braking probably also caused the separate rear-end contact from behind.
- car_conflicts_3knobs_2hz_optuna_confirm_r8_011: turned_into_actor, policy at fault: yes. On a clear multi-lane highway, the ego braked hard after handoff (20.6 to 7.6 m/s) with no lead vehicle close (gap about 48 m or none). Actor 1 in the left lane overtook it, and the ego's planned path veered left into that lane, so the ego's front-left corner struck actor 1. The rear-end contact recorded for this run happened after that collision and was likely caused by the unneeded braking.
- car_conflicts_3knobs_2hz_optuna_confirm_r8_017: turned_into_actor, policy at fault: yes. On an open multi-lane highway with no close lead (gap over 40 m), the ego braked hard for no clear reason, from 23.7 to 7.5 m/s. While slowing, it drifted left toward the adjacent lane, where actor 1 was coming up from behind-left. The ego's front hit actor 1's side as the two came alongside.
- car_conflicts_3knobs_2hz_optuna_confirm_r8_021: other, policy at fault: yes. Unprompted hard braking on an open highway: after handoff the ego slowed from 18.6 to 5 m/s with nothing close ahead (the lead was about 48 m away) and drifted about 1.6 m left of the recorded path. Actor 28, a replayed car that had been following on the recorded path and does not react to the ego, caught up and struck the ego's right side (and rear).
- car_conflicts_3knobs_2hz_optuna_confirm_r8_029: other, policy at fault: yes. On an open highway, the ego braked hard for no visible reason. It slowed from 18 to 4.4 m/s while the nearest vehicle ahead in its lane stayed 43–57 m away, and it fell far behind the recorded trajectory (20.8 m). Actor 28, which was following the recorded path in the ego's lane, came up from behind. Because the ego had drifted slightly left, actor 28 struck it along the right front and side, so the contact was scored as an at-fault front collision even though the ego was also rear-ended.
- car_conflicts_3knobs_2hz_optuna_confirm_r8_030_a2: turned_into_actor, policy at fault: yes. The ego was speeding up from 3.5 to 7 m/s in dense multi-lane traffic. Its planned path (orange) bent left toward actor 15's lane, so it drifted about 1.5 m left of the recorded trajectory, onto the lane line, and side-swiped actor 56 in the adjacent left lane. The route command was STRAIGHT and then RIGHT, so the left move went against it.
- car_conflicts_3knobs_2hz_optuna_confirm_r8_036: actor_hit_ego, policy at fault: unclear. The ego was going straight in its highway lane with no vehicle ahead, slowing gently from 8.8 to 7.6 m/s, and fell about 20 m behind where the human car was at that point. Actor 24 came up from behind in the right lane, moved left into the ego's lane at 9.2 s and hit the ego's front-right corner. In the real drive that actor probably merged into a gap behind the faster human car, so this looks like a replayed actor that doesn't react to the ego, plus the ego's unexplained slowdown.
- car_conflicts_3knobs_2hz_optuna_confirm_r8_046: turned_into_actor, policy at fault: yes. On a clear multi-lane highway with no close lead (the gap was more than 40 m or empty), the policy braked hard from 23.7 to 7.1 m/s and drifted left out of its lane. Its front-left corner hit actor 1, which had been behind it in the left lane and was passing the slowing ego.
- car_conflicts_3knobs_2hz_optuna_confirm_r8_048: turned_into_actor, policy at fault: yes. On a clear multi-lane highway, the policy braked hard for no visible reason, slowing from 23.7 to 7.1 m/s with the nearest vehicle ahead 43 m or more away. As it slowed, it drifted about 1.2 m left toward the adjacent lane. Actor 1, coming up from behind in that lane, drew alongside, and the ego's front-left touched it (an at-fault front collision; a rear contact was also flagged).
- car_conflicts_3knobs_2hz_optuna_confirm_r8_051: actor_hit_ego, policy at fault: no. The ego was going straight and steady in its highway lane at about 8 m/s, roughly 20 m behind where the recorded car was at that point. Actor 24 came up from behind in the right lane, moved left into the ego's lane and struck the ego's right-front corner; there was no lead vehicle, and the ego kept to its lane.
- car_conflicts_3knobs_2hz_optuna_confirm_r8_056: other, policy at fault: yes. With no lead vehicle, the ego braked hard on an open highway (18.6 to 5.1 m/s) and drifted about 1.6 m left of the recorded path, toward the lane behind actor 1. Actor 28 was following in the ego's original lane, replaying the recorded drive. It caught up with the now much slower ego, which still straddled the lane, and side-swiped its right side. Some actor also hit the ego's rear.
- car_conflicts_3knobs_2hz_optuna_confirm_r8_058: other, policy at fault: yes. After handoff on an open highway, the ego braked hard for no visible reason, slowing from 16.9 to 5.5 m/s with no lead vehicle within about 50 m, while the recorded human kept going (the ego was 20 m behind the human's position by the end). Non-reactive traffic following the recorded speed caught up: the ego had already been rear-ended, and at 7.6 s actor 28 came up alongside on the right and overlapped the ego, which counts as a front/side collision.

## Every setting

- S1: 023b7fcc at actor_time_shift_s -0.5, actor_speed_scale 0.5, ego_speed_scale 1.2: 1/2 failed, rate 12%-88% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_030_a2, car_conflicts_3knobs_2hz_optuna_confirm_r8_031)
- S2: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_016_a2, car_conflicts_3knobs_2hz_optuna_confirm_r8_022)
- S3: 023b7fcc at actor_time_shift_s 2.0, actor_speed_scale 0.75, ego_speed_scale 0.6: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_007, car_conflicts_3knobs_2hz_optuna_confirm_r8_013, car_conflicts_3knobs_2hz_optuna_confirm_r8_045, car_conflicts_3knobs_2hz_optuna_confirm_r8_055_a2)
- S4: 096988dd at actor_time_shift_s -1.0, actor_speed_scale 0.75, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_037)
- S5: 096988dd at actor_time_shift_s 0.0, actor_speed_scale 0.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_057)
- S6: 096988dd at actor_time_shift_s 0.5, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_001, car_conflicts_3knobs_2hz_optuna_confirm_r8_024, car_conflicts_3knobs_2hz_optuna_confirm_r8_033, car_conflicts_3knobs_2hz_optuna_confirm_r8_043, car_conflicts_3knobs_2hz_optuna_confirm_r8_053)
- S7: 096988dd at actor_time_shift_s 1.0, actor_speed_scale 0.75, ego_speed_scale 0.6: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_010, car_conflicts_3knobs_2hz_optuna_confirm_r8_012)
- S8: 09a95ffa at actor_time_shift_s -1.0, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_019)
- S9: 09a95ffa at actor_time_shift_s 1.0, actor_speed_scale 2.0, ego_speed_scale 1.2: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_020, car_conflicts_3knobs_2hz_optuna_confirm_r8_023, car_conflicts_3knobs_2hz_optuna_confirm_r8_032, car_conflicts_3knobs_2hz_optuna_confirm_r8_042, car_conflicts_3knobs_2hz_optuna_confirm_r8_052)
- S10: 0cf6368d at actor_time_shift_s -2.0, actor_speed_scale 0.75, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_008)
- S11: 0cf6368d at actor_time_shift_s 1.5, actor_speed_scale 1.5, ego_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_009, car_conflicts_3knobs_2hz_optuna_confirm_r8_015)
- S12: 0dbb91dd at actor_time_shift_s 1.5, actor_speed_scale 0.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_038)
- S13: 0e899dd3 at actor_time_shift_s -2.0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_004, car_conflicts_3knobs_2hz_optuna_confirm_r8_014, car_conflicts_3knobs_2hz_optuna_confirm_r8_025, car_conflicts_3knobs_2hz_optuna_confirm_r8_034, car_conflicts_3knobs_2hz_optuna_confirm_r8_044, car_conflicts_3knobs_2hz_optuna_confirm_r8_054)
- S14: 12855a41 at actor_time_shift_s -1.5, actor_speed_scale 0.5, ego_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_026, car_conflicts_3knobs_2hz_optuna_confirm_r8_035)
- S15: 12855a41 at actor_time_shift_s -1.0, actor_speed_scale 1.0, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_018)
- S16: 187e6244 at actor_time_shift_s -1.0, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_050)
- S17: 187e6244 at actor_time_shift_s 0.5, actor_speed_scale 0.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_060)
- S18: 187e6244 at actor_time_shift_s 0.5, actor_speed_scale 1.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_005)
- S19: 19f339ba at actor_time_shift_s -2.0, actor_speed_scale 0.5, ego_speed_scale 1.0: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_058)
- S20: 19f339ba at actor_time_shift_s -1.5, actor_speed_scale 0.5, ego_speed_scale 1.4: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_029)
- S21: 19f339ba at actor_time_shift_s -1.0, actor_speed_scale 0.5, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_059)
- S22: 19f339ba at actor_time_shift_s -1.0, actor_speed_scale 0.5, ego_speed_scale 1.2: 4/4 failed, rate 60%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_006, car_conflicts_3knobs_2hz_optuna_confirm_r8_011, car_conflicts_3knobs_2hz_optuna_confirm_r8_021, car_conflicts_3knobs_2hz_optuna_confirm_r8_056)
- S23: 19f339ba at actor_time_shift_s -1.0, actor_speed_scale 0.5, ego_speed_scale 1.4: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_003)
- S24: 19f339ba at actor_time_shift_s -1.0, actor_speed_scale 1.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_049)
- S25: 19f339ba at actor_time_shift_s -1.0, actor_speed_scale 2.0, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_027_a2)
- S26: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 1.5, ego_speed_scale 1.4: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_048)
- S27: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_047)
- S28: 19f339ba at actor_time_shift_s 1.0, actor_speed_scale 1.5, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_002)
- S29: 19f339ba at actor_time_shift_s 1.5, actor_speed_scale 0.75, ego_speed_scale 1.4: 2/2 failed, rate 42%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_017, car_conflicts_3knobs_2hz_optuna_confirm_r8_046)
- S30: 19f339ba at actor_time_shift_s 2.0, actor_speed_scale 1.0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_039)
- S31: 1c45ce3a at actor_time_shift_s -1.0, actor_speed_scale 0.5, ego_speed_scale 0.8: 2/3 failed, rate 25%-92% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_036, car_conflicts_3knobs_2hz_optuna_confirm_r8_041, car_conflicts_3knobs_2hz_optuna_confirm_r8_051)
- S32: 1c45ce3a at actor_time_shift_s -1.0, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_028)
- S33: 1c45ce3a at actor_time_shift_s 0.5, actor_speed_scale 0.5, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r8_040)

## Not kept by the gate

- car_conflicts_3knobs_2hz_optuna_confirm_r8_016: not kept: RE-RUN
- car_conflicts_3knobs_2hz_optuna_confirm_r8_027: not kept: RE-RUN
- car_conflicts_3knobs_2hz_optuna_confirm_r8_030: not kept: RE-RUN
- car_conflicts_3knobs_2hz_optuna_confirm_r8_055: not kept: RE-RUN

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
