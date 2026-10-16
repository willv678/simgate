# In cut-in and lead-vehicle scenes that pass as recorded, which combinations of the car's timing, the car's speed and the ego's speed at hand-off make the policy collide or leave the road? The aim is the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `hybrid_r2`: 60 kept runs on 10 scenes, varying actor_time_shift_s, actor_speed_scale, ego_speed_scale; 2 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 2 of 5 challenging settings confirmed, after 6 rounds.

## Answer

Only two of the five cases were confirmed, so the goal was not met. On 096988dd the policy failed in every run with the car on time, the car at 1.25x speed and the ego at 1.2x (S5). On 19f339ba it failed in every run with the same car settings and the ego at 1.4x (S29). In both cases the 90% range lies above 0.5, and none of the failures are flagged as possible simulator artifacts. On both scenes the ego's own hand-off speed is what tipped the outcome. With the car settings unchanged and the ego slower, no run failed (S4; S27, S28). Even so, the crash was not with the retimed car. The policy drifted left out of its lane and hit a car passing beside it, which is the policy's fault. No other scene produced a single failure, and most settings were run only once or twice, so their passes are hints rather than rates.

## Findings

- Confirmed case 1, scene 096988dd: car on time at 1.25x, ego at 1.2x. Every run failed, and the range lies above 0.5. With the ego at its recorded speed and the same car settings, no run failed. So the faster hand-off is what triggers it, though that comparison rests on only a couple of runs.
  - S5: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 5/5 failed, rate 65%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_017, car_conflicts_3knobs_2hz_hybrid_r2_021, car_conflicts_3knobs_2hz_hybrid_r2_022, car_conflicts_3knobs_2hz_hybrid_r2_023, car_conflicts_3knobs_2hz_hybrid_r2_024)
  - S4: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_002, car_conflicts_3knobs_2hz_hybrid_r2_016)
- In 096988dd every failure was the policy's own. The route command was RIGHT (or STRAIGHT and then RIGHT), but the ego slowed, drifted left out of its lane and drove its front into actor 41, a pickup passing in the left lane. Actor 41 is not the retimed car (track 2).
  - S5: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 5/5 failed, rate 65%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_017, car_conflicts_3knobs_2hz_hybrid_r2_021, car_conflicts_3knobs_2hz_hybrid_r2_022, car_conflicts_3knobs_2hz_hybrid_r2_023, car_conflicts_3knobs_2hz_hybrid_r2_024)
- Confirmed case 2, scene 19f339ba: car on time at 1.25x, ego at 1.4x. Every run failed, and the range lies above 0.5. With the ego at 1.0x or 1.2x, or with the car at 1.5x and the ego at 1.2x, no run failed. Each of those settings has only one run, so these are hints, not rates.
  - S29: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.4: 4/4 failed, rate 60%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_025, car_conflicts_3knobs_2hz_hybrid_r2_031, car_conflicts_3knobs_2hz_hybrid_r2_032, car_conflicts_3knobs_2hz_hybrid_r2_033)
  - S27: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_004)
  - S28: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_019)
  - S30: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_026)
- In 19f339ba every failure was the policy braking hard for no visible reason, with the nearest car ahead 40 m or more away and pulling off. While braking it drifted left, and its front-left corner swung into actor 1 coming up in the left lane. Some runs also show a rear-end contact from traffic behind; that is a consequence of the braking for nothing and not counted as the failure.
  - S29: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.4: 4/4 failed, rate 60%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_025, car_conflicts_3knobs_2hz_hybrid_r2_031, car_conflicts_3knobs_2hz_hybrid_r2_032, car_conflicts_3knobs_2hz_hybrid_r2_033)
- Both confirmed failures are side-swipes into a car in the next lane during an unprompted left drift. Neither is a collision with the retimed cut-in or lead car. The search found a weakness in keeping the lane at higher hand-off speeds, not in reacting to the retimed car.
  - S5: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 5/5 failed, rate 65%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_017, car_conflicts_3knobs_2hz_hybrid_r2_021, car_conflicts_3knobs_2hz_hybrid_r2_022, car_conflicts_3knobs_2hz_hybrid_r2_023, car_conflicts_3knobs_2hz_hybrid_r2_024)
  - S29: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.4: 4/4 failed, rate 60%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_025, car_conflicts_3knobs_2hz_hybrid_r2_031, car_conflicts_3knobs_2hz_hybrid_r2_032, car_conflicts_3knobs_2hz_hybrid_r2_033)
- Several settings were repeated without a single failure, and their ranges lie below 0.5. These include 12855a41 with the car 0.5 s early at 1.25x and the ego at 1.2x, and 1c45ce3a with the car on time at 1.5x and the ego at 1.0x. Settings with three runs and no failure also sit below 0.5: 09a95ffa and 12855a41 with the car on time at 1.25x and the ego at 1.0x, and 0cf6368d with the ego at 1.2x.
  - S21: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_049, car_conflicts_3knobs_2hz_hybrid_r2_051, car_conflicts_3knobs_2hz_hybrid_r2_052, car_conflicts_3knobs_2hz_hybrid_r2_053, car_conflicts_3knobs_2hz_hybrid_r2_054)
  - S33: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_040, car_conflicts_3knobs_2hz_hybrid_r2_055, car_conflicts_3knobs_2hz_hybrid_r2_056, car_conflicts_3knobs_2hz_hybrid_r2_057, car_conflicts_3knobs_2hz_hybrid_r2_058)
  - S7: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_008, car_conflicts_3knobs_2hz_hybrid_r2_014, car_conflicts_3knobs_2hz_hybrid_r2_038)
  - S22: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_003, car_conflicts_3knobs_2hz_hybrid_r2_011, car_conflicts_3knobs_2hz_hybrid_r2_039)
  - S12: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_036, car_conflicts_3knobs_2hz_hybrid_r2_059, car_conflicts_3knobs_2hz_hybrid_r2_060)
- Scenes 023b7fcc, 0cf6368d, 0e899dd3, 09a95ffa, 0dbb91dd, 187e6244 and 1c45ce3a produced no failure at any setting tried. This includes the ego at 1.4x on 023b7fcc, 0cf6368d and 0e899dd3, the combination that broke 19f339ba.
  - S3: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_043, car_conflicts_3knobs_2hz_hybrid_r2_044)
  - S13: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_041, car_conflicts_3knobs_2hz_hybrid_r2_042)
  - S18: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_034, car_conflicts_3knobs_2hz_hybrid_r2_035)
  - S19: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_045, car_conflicts_3knobs_2hz_hybrid_r2_046)
  - S15: 0e899dd3 at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_047_a3)
  - S9: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_027)
  - S14: 0dbb91dd at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_006)
  - S26: 187e6244 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_005)
  - S34: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_048)
- The near misses, which the brief ranks next, are the non-failing settings with the highest criticality. They are 19f339ba with the car at 1.5x and the ego at 1.2x, 19f339ba with the car at 1.25x and the ego at 1.2x, 09a95ffa with the car on time at 1.25x and the ego at 1.0x, 12855a41 with the car 0.5 s early, and 096988dd with the ego at 1.0x. Each is one or a few runs.
  - S30: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_026)
  - S28: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_019)
  - S7: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_008, car_conflicts_3knobs_2hz_hybrid_r2_014, car_conflicts_3knobs_2hz_hybrid_r2_038)
  - S20: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_029)
  - S4: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_002, car_conflicts_3knobs_2hz_hybrid_r2_016)

## Open

- Three more distinct scenes are still needed to reach five. The search barely covered the space: the car's timing only went from 0.5 s early to 0.5 s late (never ±2 s), its speed only from 1.25x to 1.5x (never below 1x), and the ego's speed only from 1.0x to 1.4x (never below 1x). Runs at large timing shifts, slower cars and slower egos, especially on the near-miss scenes 09a95ffa and 12855a41, would show whether failures exist elsewhere.
- Ego at 1.4x on 096988dd was never tried, and ego at 1.4x on 09a95ffa, 12855a41 and 1c45ce3a was not tried either. Since the ego's speed was the trigger on both confirmed scenes, a few runs at 1.4x there are the cheapest next step.
- Is the boundary between pass and fail sharp? The neighbours of S5 and S29 that passed (S4; S27, S28, S30) have only one or two runs each. Repeating them, about five runs each, would show whether those settings really pass or only rarely fail.
- Scenes 0dbb91dd and 187e6244 got a single run each (S14, S26), even though the plan flagged them as close calls as recorded. They are essentially untested.
- Both confirmed failures involve an unprompted left drift into a car in the next lane, not the retimed car. Further runs would show whether the knob causes it through the retimed car's effect on the scene, or whether the ego's speed at hand-off alone causes it. For example: S5 and S29 with the retimed car at 1.0x, or with the left-lane car (41 or 1) removed or retimed.
- On 0e899dd3, the setting with the car 0.5 s early at 1.25x and the ego at 1.4x needed two re-runs before a run was kept (S15). Its single kept pass is thin evidence.

## Why the runs failed (triage from the video and log)

turned_into_actor 9

- car_conflicts_3knobs_2hz_hybrid_r2_017: turned_into_actor, policy at fault: yes. On a multi-lane highway the route command was RIGHT, but the ego's plan bent left and it drifted toward the adjacent left lane while slowing to about 4.4 m/s. Actor 41 was passing in that lane, and the ego's front-left corner hit it about 1.6 m left of the recorded path.
- car_conflicts_3knobs_2hz_hybrid_r2_021: turned_into_actor, policy at fault: yes. On the multi-lane highway, the ego slowed and steered left toward the next lane, even though the command was RIGHT and the recorded drive stayed in lane. Vehicle 41 was traveling alongside in that lane, and the ego's front hit it at 7.7s.
- car_conflicts_3knobs_2hz_hybrid_r2_022: turned_into_actor, policy at fault: yes. On a wet multi-lane highway the route command changed to RIGHT, but the ego drifted left out of its lane instead. Its front hit actor 41, a white pickup driving in the lane to its left (front collision at 7.7 s, ego about 1.7 m left of the recorded path).
- car_conflicts_3knobs_2hz_hybrid_r2_023: turned_into_actor, policy at fault: yes. On a multi-lane highway with the route command STRAIGHT and then RIGHT, the ego's plan bent left, away from the logged path, and it moved into the lane to its left. Its front hit the white pickup (actor 41), which was driving alongside and slightly ahead in that lane.
- car_conflicts_3knobs_2hz_hybrid_r2_024: turned_into_actor, policy at fault: yes. On a multi-lane highway, the ego slowed from 6.7 to 4.4 m/s and drifted left toward the next lane, even though the route command was STRAIGHT and then RIGHT. Car 41 was passing on the left and had just moved slightly ahead, and the ego's front corner cut into it.
- car_conflicts_3knobs_2hz_hybrid_r2_025: turned_into_actor, policy at fault: yes. On a clear multi-lane highway, the policy braked hard for no visible reason (23.7 to 6.8 m/s, with the lead 40+ m ahead and pulling away) while its path wandered left. Actor 1, a replayed vehicle in the left lane that had been behind, came up alongside, and the ego's front-left corner swung into it at 7.6 s.
- car_conflicts_3knobs_2hz_hybrid_r2_031: turned_into_actor, policy at fault: yes. On a clear highway with the nearest car ahead 40–53 m away, the policy braked hard for no visible reason (23.7 → 6.7 m/s) and drifted left off the recorded path. Actor 1, coming up in the left lane, was beside the ego when the ego's front-left corner swung into it. The ego was also rear-ended at some point, which fits a car following behind it while it braked for nothing.
- car_conflicts_3knobs_2hz_hybrid_r2_032: turned_into_actor, policy at fault: yes. On a straight highway with no lead closer than 40 m, the policy braked hard for no reason (23.7 to 7.1 m/s) while drifting left. Actor 1 caught up in the left lane, and the ego's front-left clipped it as the two came alongside. The sudden slowdown also likely caused the separate rear contact from traffic behind.
- car_conflicts_3knobs_2hz_hybrid_r2_033: turned_into_actor, policy at fault: yes. On an open highway with no lead vehicle within 40 m, the ego braked hard for no clear reason, slowing from 23.7 to 6.9 m/s, and drifted left toward the next lane. Actor 1 was passing on the left at that moment, and the ego's front-left corner hit its side.

## Every setting

- S1: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_001)
- S2: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_037)
- S3: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_043, car_conflicts_3knobs_2hz_hybrid_r2_044)
- S4: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_002, car_conflicts_3knobs_2hz_hybrid_r2_016)
- S5: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 5/5 failed, rate 65%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_017, car_conflicts_3knobs_2hz_hybrid_r2_021, car_conflicts_3knobs_2hz_hybrid_r2_022, car_conflicts_3knobs_2hz_hybrid_r2_023, car_conflicts_3knobs_2hz_hybrid_r2_024)
- S6: 09a95ffa at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_028)
- S7: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_008, car_conflicts_3knobs_2hz_hybrid_r2_014, car_conflicts_3knobs_2hz_hybrid_r2_038)
- S8: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_015)
- S9: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_027)
- S10: 09a95ffa at actor_time_shift_s 0.5, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_050)
- S11: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_007)
- S12: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_036, car_conflicts_3knobs_2hz_hybrid_r2_059, car_conflicts_3knobs_2hz_hybrid_r2_060)
- S13: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_041, car_conflicts_3knobs_2hz_hybrid_r2_042)
- S14: 0dbb91dd at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_006)
- S15: 0e899dd3 at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_047_a3)
- S16: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_009)
- S17: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_020)
- S18: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_034, car_conflicts_3knobs_2hz_hybrid_r2_035)
- S19: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_045, car_conflicts_3knobs_2hz_hybrid_r2_046)
- S20: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_029)
- S21: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_049, car_conflicts_3knobs_2hz_hybrid_r2_051, car_conflicts_3knobs_2hz_hybrid_r2_052, car_conflicts_3knobs_2hz_hybrid_r2_053, car_conflicts_3knobs_2hz_hybrid_r2_054)
- S22: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_003, car_conflicts_3knobs_2hz_hybrid_r2_011, car_conflicts_3knobs_2hz_hybrid_r2_039)
- S23: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_012)
- S24: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_013)
- S25: 12855a41 at actor_time_shift_s 0.5, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_030)
- S26: 187e6244 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_005)
- S27: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_004)
- S28: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_019)
- S29: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.4: 4/4 failed, rate 60%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_025, car_conflicts_3knobs_2hz_hybrid_r2_031, car_conflicts_3knobs_2hz_hybrid_r2_032, car_conflicts_3knobs_2hz_hybrid_r2_033)
- S30: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_026)
- S31: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_010)
- S32: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_018)
- S33: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_040, car_conflicts_3knobs_2hz_hybrid_r2_055, car_conflicts_3knobs_2hz_hybrid_r2_056, car_conflicts_3knobs_2hz_hybrid_r2_057, car_conflicts_3knobs_2hz_hybrid_r2_058)
- S34: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_r2_048)

## Not kept by the gate

- car_conflicts_3knobs_2hz_hybrid_r2_047: not kept: RE-RUN
- car_conflicts_3knobs_2hz_hybrid_r2_047_a2: not kept: RE-RUN

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

0 of 62 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
