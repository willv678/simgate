# In cut-in and lead-vehicle scenes that pass as recorded, which combinations of the car's timing, the car's speed and the ego's speed at hand-off make the policy collide or leave the road? The aim is the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `llm_r5`: 60 kept runs on 9 scenes, varying actor_time_shift_s, actor_speed_scale, ego_speed_scale; 0 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 2 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The study confirmed 2 of the 5 cases it was looking for, so the goal was not met. Both confirmed cases are on different scenes and both use the fastest ego hand-off speed (1.4x). On 19f339ba the failing setting is the car 1 s earlier at 1.5x speed (S32). On 096988dd it is the car at its recorded timing and speed (S11), and every run there failed. In every failure the policy drifted left out of its lane into a car in the next lane, against a STRAIGHT or RIGHT command. It was never a failure to brake for the cut-in or lead car. On 19f339ba the policy also braked hard on an open road with no car close ahead. That means the car the study retimed was not the one hit, and the fast ego hand-off looks like the real trigger. No failure is flagged as a possible simulator artifact, and triage blames the policy in every case. The other eight scenes produced no confirmed case. The range for S11 only just clears 0.5, and most other settings were run once or twice, which hints at a rate but does not measure one.

## Findings

- Confirmed case 1 (scene 19f339ba): the car 1 s earlier at 1.5x speed with the ego at 1.4x makes the policy fail in most repeats. On a clear highway it brakes hard for no visible reason, drifts left across the lane line, and sideswipes actor 1 coming up in the left lane.
  - S32: 19f339ba at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1.4: 9/11 failed, rate 57%-94% (90%) (car_conflicts_3knobs_2hz_llm_r5_005, car_conflicts_3knobs_2hz_llm_r5_014, car_conflicts_3knobs_2hz_llm_r5_015, car_conflicts_3knobs_2hz_llm_r5_021, car_conflicts_3knobs_2hz_llm_r5_022, car_conflicts_3knobs_2hz_llm_r5_023, car_conflicts_3knobs_2hz_llm_r5_031, car_conflicts_3knobs_2hz_llm_r5_032, car_conflicts_3knobs_2hz_llm_r5_033, car_conflicts_3knobs_2hz_llm_r5_041, car_conflicts_3knobs_2hz_llm_r5_042)
- On 19f339ba, the recorded car timing and speed with the ego at 1.2x or 1.4x passed in single runs. So the failure there seems to need the earlier, faster car as well as the fast ego, but these are single runs only.
  - S33: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r5_006)
  - S34: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r5_016)
  - S32: 19f339ba at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1.4: 9/11 failed, rate 57%-94% (90%) (car_conflicts_3knobs_2hz_llm_r5_005, car_conflicts_3knobs_2hz_llm_r5_014, car_conflicts_3knobs_2hz_llm_r5_015, car_conflicts_3knobs_2hz_llm_r5_021, car_conflicts_3knobs_2hz_llm_r5_022, car_conflicts_3knobs_2hz_llm_r5_023, car_conflicts_3knobs_2hz_llm_r5_031, car_conflicts_3knobs_2hz_llm_r5_032, car_conflicts_3knobs_2hz_llm_r5_033, car_conflicts_3knobs_2hz_llm_r5_041, car_conflicts_3knobs_2hz_llm_r5_042)
- Confirmed case 2 (scene 096988dd): with the car at its recorded timing and speed and the ego at 1.4x, every run failed. The ego slows, drifts left against a STRAIGHT then RIGHT command, and hits actor 41 in the left lane. The car ahead was 17–35 m away and played no part.
  - S11: 096988dd at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_llm_r5_002, car_conflicts_3knobs_2hz_llm_r5_011, car_conflicts_3knobs_2hz_llm_r5_012)
- On 096988dd the car 1 s earlier at 1.5x with the ego at 1.4x also failed every run, the same way. There were too few repeats to confirm it above 0.5, and it is on the same scene as S11, so it adds no new case. Together these suggest the ego's hand-off speed, not the car's retiming, drives the failure on this scene.
  - S10: 096988dd at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1.4: 2/2 failed, rate 42%-100% (90%) (car_conflicts_3knobs_2hz_llm_r5_001, car_conflicts_3knobs_2hz_llm_r5_013)
  - S11: 096988dd at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_llm_r5_002, car_conflicts_3knobs_2hz_llm_r5_011, car_conflicts_3knobs_2hz_llm_r5_012)
- The best candidate for a third case is 12855a41 with the car 1.5 s later at 0.5x and the ego at 1.4x. It failed once, again by drifting left into car 51 in the adjacent lane against a RIGHT command. The neighbouring settings (0.75x car speed, or 1–2 s shifts) did not fail.
  - S26: 12855a41 at actor_time_shift_s 1.5, actor_speed_scale 0.5, ego_speed_scale 1.4: 1/4 failed, rate 6%-64% (90%) (car_conflicts_3knobs_2hz_llm_r5_026, car_conflicts_3knobs_2hz_llm_r5_034, car_conflicts_3knobs_2hz_llm_r5_035, car_conflicts_3knobs_2hz_llm_r5_049)
  - S27: 12855a41 at actor_time_shift_s 1.5, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_llm_r5_058, car_conflicts_3knobs_2hz_llm_r5_059, car_conflicts_3knobs_2hz_llm_r5_060)
  - S23: 12855a41 at actor_time_shift_s 1, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r5_050)
  - S25: 12855a41 at actor_time_shift_s 1, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r5_018)
  - S28: 12855a41 at actor_time_shift_s 2, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r5_036)
  - S29: 12855a41 at actor_time_shift_s 2, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r5_027)
- 023b7fcc and 0e899dd3 produced no failures across many timing and speed combinations with the ego at 1.2x–1.4x, including repeated settings. Their closest approaches came near (near misses), but these scenes look robust at 2 Hz.
  - S5: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_llm_r5_025, car_conflicts_3knobs_2hz_llm_r5_047)
  - S7: 023b7fcc at actor_time_shift_s 0.5, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_llm_r5_055, car_conflicts_3knobs_2hz_llm_r5_056, car_conflicts_3knobs_2hz_llm_r5_057)
  - S8: 023b7fcc at actor_time_shift_s 0.5, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r5_038)
  - S9: 023b7fcc at actor_time_shift_s 0.5, actor_speed_scale 1, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r5_024)
  - S19: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1.4: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_llm_r5_030, car_conflicts_3knobs_2hz_llm_r5_040, car_conflicts_3knobs_2hz_llm_r5_043)
  - S20: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_llm_r5_051, car_conflicts_3knobs_2hz_llm_r5_052, car_conflicts_3knobs_2hz_llm_r5_053, car_conflicts_3knobs_2hz_llm_r5_054)
  - S21: 0e899dd3 at actor_time_shift_s 0.5, actor_speed_scale 1, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r5_045)
- Every failure was the policy's fault: a sideswipe after drifting left into an adjacent-lane car. None was a failure to brake for the retimed lead or cut-in car, and none is flagged as a possible rendering artifact.
  - S10: 096988dd at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1.4: 2/2 failed, rate 42%-100% (90%) (car_conflicts_3knobs_2hz_llm_r5_001, car_conflicts_3knobs_2hz_llm_r5_013)
  - S11: 096988dd at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_llm_r5_002, car_conflicts_3knobs_2hz_llm_r5_011, car_conflicts_3knobs_2hz_llm_r5_012)
  - S26: 12855a41 at actor_time_shift_s 1.5, actor_speed_scale 0.5, ego_speed_scale 1.4: 1/4 failed, rate 6%-64% (90%) (car_conflicts_3knobs_2hz_llm_r5_026, car_conflicts_3knobs_2hz_llm_r5_034, car_conflicts_3knobs_2hz_llm_r5_035, car_conflicts_3knobs_2hz_llm_r5_049)
  - S32: 19f339ba at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1.4: 9/11 failed, rate 57%-94% (90%) (car_conflicts_3knobs_2hz_llm_r5_005, car_conflicts_3knobs_2hz_llm_r5_014, car_conflicts_3knobs_2hz_llm_r5_015, car_conflicts_3knobs_2hz_llm_r5_021, car_conflicts_3knobs_2hz_llm_r5_022, car_conflicts_3knobs_2hz_llm_r5_023, car_conflicts_3knobs_2hz_llm_r5_031, car_conflicts_3knobs_2hz_llm_r5_032, car_conflicts_3knobs_2hz_llm_r5_033, car_conflicts_3knobs_2hz_llm_r5_041, car_conflicts_3knobs_2hz_llm_r5_042)

## Open

- Three more confirmed cases on distinct scenes are still missing. The best next step is about 5 repeats of S26 (12855a41, +1.5 s, 0.5x, ego 1.4x).
- Whether the failures on 096988dd and 19f339ba come from the ego's 1.4x hand-off speed alone. Runs at ego 1.0x and 1.2x with the S11 and S32 car settings would settle it.
- Ego speeds below 1.0x (down to 0.6x) and car shifts beyond ±1 s on most scenes were never tested. Nearly all runs used the ego at 1.4x, so the slow-ego half of the space is unexplored.
- Scenes 09a95ffa, 0cf6368d, 0dbb91dd and 187e6244 got only one or two runs each, and 1c45ce3a got none, so they cannot be ruled out.
- On 0dbb91dd (S15) the closest-approach score was zero, which does not match its recorded 0.23 m near miss. Its retiming setup is worth checking.
- The failures involve cars the study did not retime (actors 1, 41, 51), so whether retiming the key cut-in or lead car can cause a collision with that car is still unanswered.

## Why the runs failed (triage from the video and log)

turned_into_actor 15

- car_conflicts_3knobs_2hz_llm_r5_001: turned_into_actor, policy at fault: yes. On a multi-lane highway, the ego slowed from about 8 to 5 m/s and drifted left out of its lane, following its leftward-veering orange trajectory, even though the route command was STRAIGHT and then RIGHT. Its front-left corner struck vehicle 41, which was moving up in the adjacent left lane, while the ego was about 1.7 m off the recorded human path.
- car_conflicts_3knobs_2hz_llm_r5_002: turned_into_actor, policy at fault: yes. On a multi-lane highway, the ego slowed down and then drifted left out of its lane, toward the orange planned path, even though the route said STRAIGHT and later RIGHT. It hit actor 41, which was driving beside it in the left lane, with its front-left corner. The vehicle ahead was still 17–35 m away, so this was a side-swipe during an unprompted lane change, not a failure to brake for the lead.
- car_conflicts_3knobs_2hz_llm_r5_005: turned_into_actor, policy at fault: yes. After handoff, the ego braked hard on an open highway for no apparent reason, slowing from 23.7 to 7.2 m/s even though the nearest vehicle ahead was more than 40 m away, and it fell well behind the recorded human position. At the same time it drifted left across the lane line, and its front clipped actor 1, which was coming up alongside in the left lane.
- car_conflicts_3knobs_2hz_llm_r5_011: turned_into_actor, policy at fault: yes. The ego was slowing on a multi-lane highway, but instead of holding its lane or moving right as the RIGHT command asked, it steered left toward the next lane. Its front hit actor 41, which was driving alongside in that left lane, while the recorded human path stayed in the original lane about 1.7 m to the right.
- car_conflicts_3knobs_2hz_llm_r5_012: turned_into_actor, policy at fault: yes. On a multi-lane highway with a STRAIGHT command (later RIGHT), the ego slowed from 7.9 to 4.4 m/s and drifted left out of its lane toward the left lane, following its own leftward planned path. Its front-left corner then hit the side of actor 41, which was passing on the left. The recorded human path went straight; the vehicle ahead was 18–35 m away, so it was not involved.
- car_conflicts_3knobs_2hz_llm_r5_013: turned_into_actor, policy at fault: yes. After handoff on a multi-lane highway, the policy drifted left out of its lane even though the human trajectory went straight and the command was STRAIGHT, then RIGHT. Its planned path pointed into the adjacent left lane. At 7.2s it sideswiped vehicle 41, which was alongside in that lane (a lateral collision).
- car_conflicts_3knobs_2hz_llm_r5_014: turned_into_actor, policy at fault: yes. On a clear multi-lane highway with no lead vehicle within about 43 m, the ego braked hard for no visible reason, slowing from 23.7 to 7.1 m/s, while the recorded human kept going. It also drifted left toward the lane line. Actor 1 was coming up in the left lane, and as it drew alongside, the ego's front corner hit it.
- car_conflicts_3knobs_2hz_llm_r5_021: turned_into_actor, policy at fault: yes. After handoff, the ego braked hard on an open highway (23.7 to 7.4 m/s, with the lead vehicle 43+ m ahead) while drifting left across the lane line. Vehicle 1, coming up from behind in the left lane, drew alongside, and the ego's front-left clipped it.
- car_conflicts_3knobs_2hz_llm_r5_022: turned_into_actor, policy at fault: yes. On a clear highway with no lead within about 44 m, the ego braked hard for no visible reason (23.7 to 7.4 m/s) and drifted left off the recorded path across the lane line. Its front then struck actor 1, which was coming up from behind in the left lane and was now alongside.
- car_conflicts_3knobs_2hz_llm_r5_031: turned_into_actor, policy at fault: yes. On a clear highway, the ego braked hard for no visible reason (23.7 to 7.3 m/s, with the lead vehicle more than 40 m ahead) and fell behind its recorded position. While braking, it drifted left across the lane line into the adjacent lane, where actor 1 was coming up alongside, and the two collided side to side.
- car_conflicts_3knobs_2hz_llm_r5_032: turned_into_actor, policy at fault: yes. On an open multi-lane highway with no close lead (gap of 43 m or more), the ego braked hard for no clear reason, from 23.7 to 7.5 m/s. Its planned path wobbled left, and it drifted about 1.3 m left of the recorded path across the lane line. It sideswiped actor 1, which had been behind it in the left lane and was now alongside because the ego had slowed.
- car_conflicts_3knobs_2hz_llm_r5_033: turned_into_actor, policy at fault: yes. On a straight highway with no lead within about 43 m, the ego braked hard without a clear reason (23.7 to 7.3 m/s over 3 s) and drifted about 1 m left toward the lane line. Actor 1, a replayed car coming up from behind in the left lane, then made side contact with the ego's left side. The ego's recorded position was about 8.7 m further ahead.
- car_conflicts_3knobs_2hz_llm_r5_041: turned_into_actor, policy at fault: yes. On an open highway, with the nearest car ahead more than 43 m away, the ego braked hard for no clear reason (23.7 to 7.1 m/s) and its path drifted left toward the lane line. Actor 1, coming up in the left lane, drew level and the ego's left side hit it (a lateral collision); the hard braking also got the ego rear-ended.
- car_conflicts_3knobs_2hz_llm_r5_042: turned_into_actor, policy at fault: yes. On a straight multi-lane highway with no lead vehicle within 43 m, the ego braked hard for no visible reason (23.7 to 7.5 m/s) and drifted left toward the lane line. Actor 1, a logged car following its recording in the left-adjacent lane, caught up from behind and there was a side-swipe on the ego's left side.
- car_conflicts_3knobs_2hz_llm_r5_049: turned_into_actor, policy at fault: yes. In slow highway traffic (about 2.5–3 m/s), the ego left its recorded lane and drifted left, about 2 m off the human path, even though the route command was RIGHT. Its front clipped car 51, which was coming up alongside in the left lane. The nearest car ahead in its lane was over 30 m away, so this was not a lead-vehicle crash.

## Every setting

- S1: 023b7fcc at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r5_003)
- S2: 023b7fcc at actor_time_shift_s -0.5, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r5_048)
- S3: 023b7fcc at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r5_004)
- S4: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r5_037)
- S5: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_llm_r5_025, car_conflicts_3knobs_2hz_llm_r5_047)
- S6: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r5_017)
- S7: 023b7fcc at actor_time_shift_s 0.5, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_llm_r5_055, car_conflicts_3knobs_2hz_llm_r5_056, car_conflicts_3knobs_2hz_llm_r5_057)
- S8: 023b7fcc at actor_time_shift_s 0.5, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r5_038)
- S9: 023b7fcc at actor_time_shift_s 0.5, actor_speed_scale 1, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r5_024)
- S10: 096988dd at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1.4: 2/2 failed, rate 42%-100% (90%) (car_conflicts_3knobs_2hz_llm_r5_001, car_conflicts_3knobs_2hz_llm_r5_013)
- S11: 096988dd at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_llm_r5_002, car_conflicts_3knobs_2hz_llm_r5_011, car_conflicts_3knobs_2hz_llm_r5_012)
- S12: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r5_029)
- S13: 0cf6368d at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r5_028)
- S14: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r5_020)
- S15: 0dbb91dd at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r5_010)
- S16: 0e899dd3 at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r5_046)
- S17: 0e899dd3 at actor_time_shift_s -0.5, actor_speed_scale 1, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r5_044)
- S18: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r5_039)
- S19: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1.4: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_llm_r5_030, car_conflicts_3knobs_2hz_llm_r5_040, car_conflicts_3knobs_2hz_llm_r5_043)
- S20: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_llm_r5_051, car_conflicts_3knobs_2hz_llm_r5_052, car_conflicts_3knobs_2hz_llm_r5_053, car_conflicts_3knobs_2hz_llm_r5_054)
- S21: 0e899dd3 at actor_time_shift_s 0.5, actor_speed_scale 1, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r5_045)
- S22: 12855a41 at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r5_007)
- S23: 12855a41 at actor_time_shift_s 1, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r5_050)
- S24: 12855a41 at actor_time_shift_s 1, actor_speed_scale 0.75, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r5_008)
- S25: 12855a41 at actor_time_shift_s 1, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r5_018)
- S26: 12855a41 at actor_time_shift_s 1.5, actor_speed_scale 0.5, ego_speed_scale 1.4: 1/4 failed, rate 6%-64% (90%) (car_conflicts_3knobs_2hz_llm_r5_026, car_conflicts_3knobs_2hz_llm_r5_034, car_conflicts_3knobs_2hz_llm_r5_035, car_conflicts_3knobs_2hz_llm_r5_049)
- S27: 12855a41 at actor_time_shift_s 1.5, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_llm_r5_058, car_conflicts_3knobs_2hz_llm_r5_059, car_conflicts_3knobs_2hz_llm_r5_060)
- S28: 12855a41 at actor_time_shift_s 2, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r5_036)
- S29: 12855a41 at actor_time_shift_s 2, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r5_027)
- S30: 187e6244 at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r5_009)
- S31: 187e6244 at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r5_019)
- S32: 19f339ba at actor_time_shift_s -1, actor_speed_scale 1.5, ego_speed_scale 1.4: 9/11 failed, rate 57%-94% (90%) (car_conflicts_3knobs_2hz_llm_r5_005, car_conflicts_3knobs_2hz_llm_r5_014, car_conflicts_3knobs_2hz_llm_r5_015, car_conflicts_3knobs_2hz_llm_r5_021, car_conflicts_3knobs_2hz_llm_r5_022, car_conflicts_3knobs_2hz_llm_r5_023, car_conflicts_3knobs_2hz_llm_r5_031, car_conflicts_3knobs_2hz_llm_r5_032, car_conflicts_3knobs_2hz_llm_r5_033, car_conflicts_3knobs_2hz_llm_r5_041, car_conflicts_3knobs_2hz_llm_r5_042)
- S33: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r5_006)
- S34: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_llm_r5_016)

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
- A scale above 1 starts the ego behind its recorded start, so for the first second or two of the warm-up it is off the recording.). Report written by claude-opus-5-5 from `results` in 24 s; every count above is computed from the queue, not written by the model.

0 of 60 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
