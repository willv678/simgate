# In cut-in and lead-vehicle scenes that pass as recorded, which combinations of the car's timing, the car's speed and the ego's speed at hand-off make the policy collide or leave the road? The aim is the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `optuna_confirm_r6`: 59 kept runs on 10 scenes, varying actor_time_shift_s, actor_speed_scale, ego_speed_scale; 4 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 2 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The study confirmed 2 of the 5 cases it was asked for, so the goal was not met. The two confirmed cases are scene 19f339ba with the car 0.5 s later, at 0.5x speed and ego at 1.2x (S24), and scene 1c45ce3a with the car 1.0 s earlier, at 0.75x speed and ego at 0.8x (S29). Every repeat at both settings failed, but each rests on only a few runs, so its range clears 0.5 without being tight. In neither scene did the retimed car cause the crash. In 19f339ba the policy braked hard for no visible reason and drifted left into a car passing in the next lane, which is clearly the policy's fault. In 1c45ce3a the ego fell well behind the recorded drive, and a replayed car merging from the right ran into space the ego still occupied. The triage marks most of those crashes as unclear fault, so this case may come from non-reactive replay traffic rather than from the policy. Scene 187e6244 (S19) is the strongest unconfirmed third case; the other scenes produced only near misses or no failures.

## Findings

- Scene 19f339ba is confirmed as a failing case with the car 0.5 s later, at 0.5x speed and ego at 1.2x: every run failed. In each, the policy braked hard on an open highway with nothing close ahead, drifted left and hit actor 1 in the left lane. The policy was at fault, and no failure was flagged as a possible rendering artifact.
  - S24: 19f339ba at actor_time_shift_s 0.5, actor_speed_scale 0.5, ego_speed_scale 1.2: 4/4 failed, rate 60%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_008, car_conflicts_3knobs_2hz_optuna_confirm_r6_011, car_conflicts_3knobs_2hz_optuna_confirm_r6_021, car_conflicts_3knobs_2hz_optuna_confirm_r6_056)
- In scene 19f339ba the same pattern (hard braking for no reason, then drifting left into actor 1) also appeared in single runs at other settings with the ego at 1.2x–1.4x. Single runs with the ego at 0.6x–1.2x and other car settings did not fail. This hints that the trouble depends more on the ego's hand-off speed than on the retimed car. Each of these settings has only one run, so it is a hint, not a rate.
  - S21: 19f339ba at actor_time_shift_s -2.0, actor_speed_scale 1.25, ego_speed_scale 1.2: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_049)
  - S26: 19f339ba at actor_time_shift_s 0.5, actor_speed_scale 2.0, ego_speed_scale 1.4: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_030)
  - S22: 19f339ba at actor_time_shift_s -1.5, actor_speed_scale 1.0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_037)
  - S23: 19f339ba at actor_time_shift_s -1.0, actor_speed_scale 0.75, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_017)
  - S25: 19f339ba at actor_time_shift_s 0.5, actor_speed_scale 1.25, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_050)
  - S27: 19f339ba at actor_time_shift_s 1.5, actor_speed_scale 0.5, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_048)
- Scene 1c45ce3a is confirmed as a failing case with the car 1.0 s earlier, at 0.75x speed and ego at 0.8x: every run failed. The crash was always with actor 24 coming from behind on the right, never with the retimed lead car 14. Twice the replayed actor 24 merged into the ego, which had fallen about 18 m behind the recorded drive (fault unclear). Once the ego drifted right into it (policy at fault). So this case may partly be an effect of replay traffic not reacting to the ego.
  - S29: 1c45ce3a at actor_time_shift_s -1.0, actor_speed_scale 0.75, ego_speed_scale 0.8: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_005, car_conflicts_3knobs_2hz_optuna_confirm_r6_012, car_conflicts_3knobs_2hz_optuna_confirm_r6_022_a2)
- A single run in scene 1c45ce3a with the car on time at 1.25x speed and ego at 0.8x failed the same way: actor 24 clipped the ego's front-right corner, fault unclear. It is on the same scene as S29, so it cannot count as a separate case.
  - S31: 1c45ce3a at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 0.8: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_057)
- Scene 187e6244 with the car 1.0 s later, at 0.75x speed and ego at 0.8x is the strongest candidate for a third case. Both runs failed, and in both the policy was clearly at fault: following slow car 48, it steered left despite a RIGHT command and sideswiped actor 7. There are too few runs to confirm it. Its other settings did not fail.
  - S19: 187e6244 at actor_time_shift_s 1.0, actor_speed_scale 0.75, ego_speed_scale 0.8: 2/2 failed, rate 42%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_047, car_conflicts_3knobs_2hz_optuna_confirm_r6_051)
  - S17: 187e6244 at actor_time_shift_s -1.0, actor_speed_scale 1.5, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_003)
  - S18: 187e6244 at actor_time_shift_s 0.5, actor_speed_scale 2.0, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_004)
  - S20: 187e6244 at actor_time_shift_s 2.0, actor_speed_scale 0.5, ego_speed_scale 1.2: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_028, car_conflicts_3knobs_2hz_optuna_confirm_r6_034, car_conflicts_3knobs_2hz_optuna_confirm_r6_044)
- Scene 023b7fcc produced one failure at the car 1.0 s later, at 0.5x speed and ego at 0.6x, with fault unclear: the ego was rear-ended while slow, then had a side collision. The other runs at that setting, and every run at its other setting, passed.
  - S1: 023b7fcc at actor_time_shift_s 1.0, actor_speed_scale 0.5, ego_speed_scale 0.6: 1/3 failed, rate 8%-75% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_029, car_conflicts_3knobs_2hz_optuna_confirm_r6_031, car_conflicts_3knobs_2hz_optuna_confirm_r6_041)
  - S2: 023b7fcc at actor_time_shift_s 1.5, actor_speed_scale 0.75, ego_speed_scale 1.2: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_020, car_conflicts_3knobs_2hz_optuna_confirm_r6_024, car_conflicts_3knobs_2hz_optuna_confirm_r6_054)
- Scenes 096988dd, 12855a41 and 0cf6368d came close to failing but never failed. Each was repeated at its most critical setting without a failure, so those settings sit below 0.5. They are near misses, which the brief ranks next.
  - S3: 096988dd at actor_time_shift_s -1.5, actor_speed_scale 1.5, ego_speed_scale 0.8: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_010, car_conflicts_3knobs_2hz_optuna_confirm_r6_013, car_conflicts_3knobs_2hz_optuna_confirm_r6_023, car_conflicts_3knobs_2hz_optuna_confirm_r6_032_a2, car_conflicts_3knobs_2hz_optuna_confirm_r6_043, car_conflicts_3knobs_2hz_optuna_confirm_r6_053)
  - S14: 12855a41 at actor_time_shift_s -1.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_009, car_conflicts_3knobs_2hz_optuna_confirm_r6_014, car_conflicts_3knobs_2hz_optuna_confirm_r6_025, car_conflicts_3knobs_2hz_optuna_confirm_r6_033)
  - S16: 12855a41 at actor_time_shift_s 1.5, actor_speed_scale 0.5, ego_speed_scale 0.8: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_040, car_conflicts_3knobs_2hz_optuna_confirm_r6_042, car_conflicts_3knobs_2hz_optuna_confirm_r6_052)
  - S9: 0cf6368d at actor_time_shift_s -1.0, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_001, car_conflicts_3knobs_2hz_optuna_confirm_r6_015, car_conflicts_3knobs_2hz_optuna_confirm_r6_035, car_conflicts_3knobs_2hz_optuna_confirm_r6_045, car_conflicts_3knobs_2hz_optuna_confirm_r6_055)
- Scenes 09a95ffa, 0e899dd3 and 0dbb91dd had only single runs and no failures. 0dbb91dd showed no criticality at all at the settings tried.
  - S6: 09a95ffa at actor_time_shift_s -1.0, actor_speed_scale 0.75, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_019)
  - S7: 09a95ffa at actor_time_shift_s -0.5, actor_speed_scale 0.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_038)
  - S8: 09a95ffa at actor_time_shift_s 0.5, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_059)
  - S13: 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 1.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_016)
  - S11: 0dbb91dd at actor_time_shift_s 0.5, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_036)
  - S12: 0dbb91dd at actor_time_shift_s 1.0, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_058)

## Open

- Is scene 187e6244 at car +1.0 s, 0.75x speed and ego 0.8x (S19) a real third case? A few more repeats there would settle whether its range clears 0.5.
- Are the 1c45ce3a failures (S29, S31) the policy's or the replay's? Rerunning S29 with reactive traffic, or with actor 24 retimed, would show whether the crash survives when that car responds to the ego.
- Does 19f339ba fail mainly because of the ego's hand-off speed? Repeating, for example, ego 1.2x with the car untouched (time shift 0, speed 1.0x), and ego 1.0x at the S24 car settings, would separate the ego-speed effect from the car knobs.
- Can 023b7fcc (S1) be confirmed? It needs more repeats, plus neighbouring settings with low ego speed.
- Scenes 096988dd, 12855a41 and 0cf6368d only came close to failing; a fourth and fifth case would need a search near their most critical settings (S3, S14, S16, S9). 09a95ffa, 0e899dd3 and 0dbb91dd are barely explored, with one run per setting.

## Why the runs failed (triage from the video and log)

turned_into_actor 10, actor_hit_ego 3

- car_conflicts_3knobs_2hz_optuna_confirm_r6_005: actor_hit_ego, policy at fault: unclear. The ego was driving straight in its lane and slowing gently (8.6 to 7.1 m/s) with a growing gap to lead 14. Meanwhile actor 24 came up from behind on the right and moved left across the lane line into the ego's front-right corner. Actor 24 was replaying the recorded drive, and the ego was about 18 m behind where the human car had been at that point (but only 0.8 m off its path), so the actor merged into a space the ego still occupied.
- car_conflicts_3knobs_2hz_optuna_confirm_r6_008: turned_into_actor, policy at fault: yes. On a straight multi-lane highway, the ego braked hard for no visible reason (20.3 to 8.4 m/s, with the lane ahead clear and the recorded human car pulling away) while its planned path bent left. Actor 1, a faster car in the left lane, came up alongside, and the ego's front-left corner hit it as the ego drifted into that lane. A car behind also rear-ended the ego because of the braking.
- car_conflicts_3knobs_2hz_optuna_confirm_r6_011: turned_into_actor, policy at fault: yes. On a clear multi-lane highway with nothing ahead, the ego braked hard for no reason (20 → 8.5 m/s) and fell behind the recorded trajectory. It then drifted left into the next lane, and its front struck actor 1, which had pulled alongside and ahead on the left (the command at that moment was RIGHT).
- car_conflicts_3knobs_2hz_optuna_confirm_r6_012: turned_into_actor, policy at fault: yes. On a straight freeway, the ego slowed from 8.7 to 6.8 m/s, well below the recorded drive, and ended up about 18 m behind where the human car was. It also drifted about 1 m right of the recorded path, toward the lane line. Actor 24 is a replayed vehicle passing in the right lane, and the ego's front-right corner clipped it as it came alongside. Actor 14, the car ahead, was still about 26 m away, so this was not a lead-vehicle crash.
- car_conflicts_3knobs_2hz_optuna_confirm_r6_021: turned_into_actor, policy at fault: yes. On a clear multi-lane highway, the ego slowed hard for no visible reason (20 to 9 m/s, falling behind the recorded human position). It also drifted left across the lane line into actor 1 in the adjacent left lane, hitting it with its front-left corner. The command was STRAIGHT and then RIGHT.
- car_conflicts_3knobs_2hz_optuna_confirm_r6_029: turned_into_actor, policy at fault: unclear. Shortly after handoff, the ego was moving slowly (about 2.5–3 m/s) and actor 12 ran into its rear by 5.7 s. Then, with a RIGHT command, the ego drifted about 2 m left of the recorded path toward the lane boundary. At 7.7 s it had a side collision, probably with actor 56 coming up in the left lane, though it could also have been actor 12 still pressed against it.
- car_conflicts_3knobs_2hz_optuna_confirm_r6_030: turned_into_actor, policy at fault: yes. On a clear multi-lane highway with no lead vehicle within about 43 m, the ego braked hard for no visible reason, slowing from 23.7 to 7.3 m/s, so actor 1 in the lane to its left caught up and came alongside. The ego's planned path then bent left, and its front struck actor 1 as it drifted toward that lane.
- car_conflicts_3knobs_2hz_optuna_confirm_r6_022_a2: actor_hit_ego, policy at fault: unclear. The ego was going straight in its lane on a multi-lane highway, slowing from 8.7 to 7.3 m/s with plenty of room to the lead car (14), when actor 24 came up from behind on the right and moved into the ego's right side. The collision registered on the ego's front-right corner. The ego was only 0.9 m off the recorded path, but it was about 17.6 m behind where the human driver was at that moment, which suggests the replayed actor 24 was closing into space the human car had already left.
- car_conflicts_3knobs_2hz_optuna_confirm_r6_047: turned_into_actor, policy at fault: yes. On a crowded highway, the ego was following slow car 48 in its lane. Even though the command was RIGHT, it steered left toward the adjacent lane (the orange planned path bends left) and sideswiped actor 7, which was passing on its left, at 8.2s (lateral collision, ego 1.6 m off the recorded path).
- car_conflicts_3knobs_2hz_optuna_confirm_r6_049: turned_into_actor, policy at fault: yes. On a straight highway with no lead vehicle nearby, the ego braked hard for no clear reason (20 to 9 m/s) and drifted left toward the lane line. Actor 1 in the left lane caught up and drew alongside, and the ego's front-left corner hit it. The hard braking probably also caused the later rear contact.
- car_conflicts_3knobs_2hz_optuna_confirm_r6_051: turned_into_actor, policy at fault: yes. On a congested freeway, the ego slowed behind lead car 48 and then steered left toward the adjacent lane, even though the route command was RIGHT. It sideswiped actor 7, which was coming up alongside in that lane (a lateral collision at 7.7 s, about 1.8 m off the recorded path).
- car_conflicts_3knobs_2hz_optuna_confirm_r6_056: turned_into_actor, policy at fault: yes. On an open highway, the ego braked hard for no visible reason, slowing from 20.3 to 8.5 m/s even though the nearest car ahead was about 50 m away. While braking, it drifted about 1.2 m left of the recorded path toward the next lane. Its front-left corner then clipped the rear of actor 1, which was passing it in that lane. A rear-end contact was also recorded, apparently from traffic behind reacting to the ego's sudden braking.
- car_conflicts_3knobs_2hz_optuna_confirm_r6_057: actor_hit_ego, policy at fault: unclear. On a straight multi-lane highway, the ego slowed gently from 8.7 to 7.5 m/s and fell about 20 m behind where the human drove. Actor 24 was coming up from behind in the lane to the right. By 9.2 s it had drawn level with the ego and clipped its front-right corner, while the ego had drifted only about 0.6 m to the right of the recorded path, toward the lane line.

## Every setting

- S1: 023b7fcc at actor_time_shift_s 1.0, actor_speed_scale 0.5, ego_speed_scale 0.6: 1/3 failed, rate 8%-75% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_029, car_conflicts_3knobs_2hz_optuna_confirm_r6_031, car_conflicts_3knobs_2hz_optuna_confirm_r6_041)
- S2: 023b7fcc at actor_time_shift_s 1.5, actor_speed_scale 0.75, ego_speed_scale 1.2: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_020, car_conflicts_3knobs_2hz_optuna_confirm_r6_024, car_conflicts_3knobs_2hz_optuna_confirm_r6_054)
- S3: 096988dd at actor_time_shift_s -1.5, actor_speed_scale 1.5, ego_speed_scale 0.8: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_010, car_conflicts_3knobs_2hz_optuna_confirm_r6_013, car_conflicts_3knobs_2hz_optuna_confirm_r6_023, car_conflicts_3knobs_2hz_optuna_confirm_r6_032_a2, car_conflicts_3knobs_2hz_optuna_confirm_r6_043, car_conflicts_3knobs_2hz_optuna_confirm_r6_053)
- S4: 096988dd at actor_time_shift_s -0.5, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_002)
- S5: 096988dd at actor_time_shift_s 0.5, actor_speed_scale 1.0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_039)
- S6: 09a95ffa at actor_time_shift_s -1.0, actor_speed_scale 0.75, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_019)
- S7: 09a95ffa at actor_time_shift_s -0.5, actor_speed_scale 0.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_038)
- S8: 09a95ffa at actor_time_shift_s 0.5, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_059)
- S9: 0cf6368d at actor_time_shift_s -1.0, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_001, car_conflicts_3knobs_2hz_optuna_confirm_r6_015, car_conflicts_3knobs_2hz_optuna_confirm_r6_035, car_conflicts_3knobs_2hz_optuna_confirm_r6_045, car_conflicts_3knobs_2hz_optuna_confirm_r6_055)
- S10: 0cf6368d at actor_time_shift_s 2.0, actor_speed_scale 0.5, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_027)
- S11: 0dbb91dd at actor_time_shift_s 0.5, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_036)
- S12: 0dbb91dd at actor_time_shift_s 1.0, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_058)
- S13: 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 1.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_016)
- S14: 12855a41 at actor_time_shift_s -1.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_009, car_conflicts_3knobs_2hz_optuna_confirm_r6_014, car_conflicts_3knobs_2hz_optuna_confirm_r6_025, car_conflicts_3knobs_2hz_optuna_confirm_r6_033)
- S15: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 1.5, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_007)
- S16: 12855a41 at actor_time_shift_s 1.5, actor_speed_scale 0.5, ego_speed_scale 0.8: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_040, car_conflicts_3knobs_2hz_optuna_confirm_r6_042, car_conflicts_3knobs_2hz_optuna_confirm_r6_052)
- S17: 187e6244 at actor_time_shift_s -1.0, actor_speed_scale 1.5, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_003)
- S18: 187e6244 at actor_time_shift_s 0.5, actor_speed_scale 2.0, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_004)
- S19: 187e6244 at actor_time_shift_s 1.0, actor_speed_scale 0.75, ego_speed_scale 0.8: 2/2 failed, rate 42%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_047, car_conflicts_3knobs_2hz_optuna_confirm_r6_051)
- S20: 187e6244 at actor_time_shift_s 2.0, actor_speed_scale 0.5, ego_speed_scale 1.2: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_028, car_conflicts_3knobs_2hz_optuna_confirm_r6_034, car_conflicts_3knobs_2hz_optuna_confirm_r6_044)
- S21: 19f339ba at actor_time_shift_s -2.0, actor_speed_scale 1.25, ego_speed_scale 1.2: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_049)
- S22: 19f339ba at actor_time_shift_s -1.5, actor_speed_scale 1.0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_037)
- S23: 19f339ba at actor_time_shift_s -1.0, actor_speed_scale 0.75, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_017)
- S24: 19f339ba at actor_time_shift_s 0.5, actor_speed_scale 0.5, ego_speed_scale 1.2: 4/4 failed, rate 60%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_008, car_conflicts_3knobs_2hz_optuna_confirm_r6_011, car_conflicts_3knobs_2hz_optuna_confirm_r6_021, car_conflicts_3knobs_2hz_optuna_confirm_r6_056)
- S25: 19f339ba at actor_time_shift_s 0.5, actor_speed_scale 1.25, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_050)
- S26: 19f339ba at actor_time_shift_s 0.5, actor_speed_scale 2.0, ego_speed_scale 1.4: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_030)
- S27: 19f339ba at actor_time_shift_s 1.5, actor_speed_scale 0.5, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_048)
- S28: 1c45ce3a at actor_time_shift_s -2.0, actor_speed_scale 2.0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_006)
- S29: 1c45ce3a at actor_time_shift_s -1.0, actor_speed_scale 0.75, ego_speed_scale 0.8: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_005, car_conflicts_3knobs_2hz_optuna_confirm_r6_012, car_conflicts_3knobs_2hz_optuna_confirm_r6_022_a2)
- S30: 1c45ce3a at actor_time_shift_s 0.0, actor_speed_scale 0.5, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_026)
- S31: 1c45ce3a at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 0.8: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_057)
- S32: 1c45ce3a at actor_time_shift_s 0.5, actor_speed_scale 0.75, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_018)
- S33: 1c45ce3a at actor_time_shift_s 2.0, actor_speed_scale 0.75, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r6_060_a2)

## Not kept by the gate

- car_conflicts_3knobs_2hz_optuna_confirm_r6_022: not kept: RE-RUN
- car_conflicts_3knobs_2hz_optuna_confirm_r6_032: not kept: RE-RUN
- car_conflicts_3knobs_2hz_optuna_confirm_r6_046: not kept: HALT
- car_conflicts_3knobs_2hz_optuna_confirm_r6_060: not kept: RE-RUN

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

0 of 63 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
