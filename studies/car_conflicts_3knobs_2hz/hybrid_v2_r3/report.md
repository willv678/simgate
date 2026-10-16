# In cut-in and lead-vehicle scenes that pass as recorded, which combinations of the car's timing, the car's speed and the ego's speed at hand-off make the policy collide or leave the road? The aim is the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `hybrid_v2_r3`: 60 kept runs on 10 scenes, varying actor_time_shift_s, actor_speed_scale, ego_speed_scale; 3 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 3 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The goal was not met. Repeats confirmed three settings, each on a different scene, and the policy is clearly at fault in only two of them. Every repeat failed at 096988dd with the car at 1.25x and the ego at 1.2x (S4), and at 19f339ba with the car at 2x and the ego at 1.2x (S41). In both, the policy steered into a car in the next lane: at 096988dd it drifted left against a RIGHT command, and at 19f339ba it braked hard on an open road for no clear reason. The third setting, 1c45ce3a with the car at 1.25x and the ego at 0.8x (S44), also failed every repeat. But in most of those runs a replayed car that does not react cut into the ego from the right, so this case says more about replayed traffic than about the policy. All three rest on a handful of repeats, so their ranges only just clear 0.5. In none of them did the ego hit the retimed car itself. What seems to matter is the ego's speed at hand-off, which moves the ego relative to the replayed traffic beside it. No failure was flagged as a possible simulator artifact.

## Findings

- At 096988dd, every run with the car at 1.25x, no time shift and the ego at 1.2x failed. In each one the policy drifted left out of its lane, against a RIGHT command, and its front hit vehicle 41 in the left lane.
  - S4: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_014, car_conflicts_3knobs_2hz_hybrid_v2_r3_021, car_conflicts_3knobs_2hz_hybrid_v2_r3_022)
- At 096988dd the failure region looks wider than the confirmed setting: single runs with a faster ego (1.4x) or a faster car (1.5x at ego 1.2x) failed the same way. At the recorded ego speed, the same scene passed. Each of these settings had only one run, so they are hints.
  - S5: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.4: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_023)
  - S6: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1.2: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_024)
  - S3: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_002)
  - S2: 096988dd at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_015)
- At 19f339ba, every run with the car at 2x, no time shift and the ego at 1.2x failed. Each time the policy braked hard on an open highway with no lead car near, drifted left, and clipped car 1 as it passed in the left lane. The same car speed with the ego at 1.0x or 0.8x passed, in one run each.
  - S41: 19f339ba at actor_time_shift_s 0, actor_speed_scale 2, ego_speed_scale 1.2: 4/4 failed, rate 60%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_047, car_conflicts_3knobs_2hz_hybrid_v2_r3_051, car_conflicts_3knobs_2hz_hybrid_v2_r3_052, car_conflicts_3knobs_2hz_hybrid_v2_r3_053)
  - S40: 19f339ba at actor_time_shift_s 0, actor_speed_scale 2, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_035)
  - S39: 19f339ba at actor_time_shift_s 0, actor_speed_scale 2, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_046)
- At 1c45ce3a, every run with the car at 1.25x and the ego slowed to 0.8x failed, and the code counts it as confirmed. But in most of those runs the replayed car 24 cut into the ego from the right lane: triage puts one not on the policy and one unclear, and only one was a policy drift to the right. The same car speed with the ego at 1.0x or 1.2x passed in single runs.
  - S44: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 0.8: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_040, car_conflicts_3knobs_2hz_hybrid_v2_r3_041, car_conflicts_3knobs_2hz_hybrid_v2_r3_042)
  - S45: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_010)
  - S46: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_011_a2)
- In three scenes, many combinations of car speed (1.25x–2x) and ego speed (0.8x–1.4x) produced no failure, including settings repeated up to three times. These scenes look hard to break in the range that was searched.
  - S7: 09a95ffa at actor_time_shift_s -0.5, actor_speed_scale 1.5, ego_speed_scale 1: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_054, car_conflicts_3knobs_2hz_hybrid_v2_r3_055, car_conflicts_3knobs_2hz_hybrid_v2_r3_056)
  - S8: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_008)
  - S9: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_029)
  - S10: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_037)
  - S11: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_045, car_conflicts_3knobs_2hz_hybrid_v2_r3_060)
  - S12: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_038)
  - S13: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 2, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_044)
  - S16: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_009)
  - S17: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_020)
  - S18: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_050)
  - S19: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_030_a2)
  - S20: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 2, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_049)
  - S21: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 2, ego_speed_scale 1.2: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_057, car_conflicts_3knobs_2hz_hybrid_v2_r3_058, car_conflicts_3knobs_2hz_hybrid_v2_r3_059_a2)
  - S22: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_034)
  - S23: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_019)
  - S24: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_003)
  - S25: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_018)
  - S26: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_025)
  - S27: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_043)
  - S28: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_026)
  - S29: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_032)
  - S30: 12855a41 at actor_time_shift_s 0, actor_speed_scale 2, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_031)
  - S31: 12855a41 at actor_time_shift_s 0.5, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_033)
- Four scenes got only one run each, at car 1.25x and the recorded ego speed, and passed. They were barely searched.
  - S1: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_001)
  - S14: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_007)
  - S15: 0dbb91dd at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_006)
  - S32: 187e6244 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_005)

## Open

- Two more confirmed cases are needed for the goal of five. Candidates are the four barely searched scenes (023b7fcc, 0cf6368d, 0dbb91dd, 187e6244), run with the ego at 1.2x–1.4x, since that is the knob tied to the confirmed failures.
- The car's timing was barely explored: only ±0.5 s was tried, and the brief allows ±2 s. Settings with a large time shift combined with a raised ego speed are untested.
- Whether S44 (1c45ce3a) is a policy failure at all: with non-reactive replayed traffic, it should be re-checked, or swapped for a case where the policy is clearly at fault.
- How far the 096988dd failure region extends: repeats at S5 (ego 1.4x) and S6 (car 1.5x, ego 1.2x) would show whether they fail as reliably as S4.
- Why the policy brakes hard on an open road at 19f339ba at ego 1.2x: an ego-1.2x run with the car at its recorded speed would show whether the car's speed matters there at all.
- The three confirmed settings have only a few repeats each, and their ranges only just clear 0.5. A few more repeats each would firm up the rates.

## Why the runs failed (triage from the video and log)

turned_into_actor 8, actor_hit_ego 2, other 2

- car_conflicts_3knobs_2hz_hybrid_v2_r3_014: turned_into_actor, policy at fault: yes. On a multi-lane highway with the command switching to RIGHT, the ego slowed and drifted left out of its lane, away from the recorded path, which kept straight and a little to the right. It cut into the left lane and its front hit vehicle 41, which was travelling alongside in that lane, about 1.6 m off the human trajectory.
- car_conflicts_3knobs_2hz_hybrid_v2_r3_021: turned_into_actor, policy at fault: yes. On a multi-lane highway, the ego's plan bent left and it drifted into the adjacent left lane, even though the command was RIGHT and the recorded human path stayed to the right. Its front hit actor 41, a white pickup travelling in that lane just ahead-left of it, at 7.7s.
- car_conflicts_3knobs_2hz_hybrid_v2_r3_022: turned_into_actor, policy at fault: yes. On a multi-lane highway, the command switched to RIGHT, but the ego drifted left of its route toward the next lane over. It ran its front into the side of actor 41, a white pickup that was passing on its left, at about 4.3 m/s.
- car_conflicts_3knobs_2hz_hybrid_v2_r3_023: turned_into_actor, policy at fault: yes. On a multi-lane highway with a STRAIGHT command (RIGHT by the last frame), the policy's planned path kept bending left toward the next lane while the recorded path stayed straight. The ego drifted about 1.4 m left and side-swiped actor 41, which was driving alongside in the left lane.
- car_conflicts_3knobs_2hz_hybrid_v2_r3_024: turned_into_actor, policy at fault: yes. On a multi-lane highway with the command STRAIGHT, the policy planned a leftward lane change (orange path) while slowing from 6.6 to 5.0 m/s. Vehicle 41 was coming up in the left lane from behind, and the ego's front-left cut into it as the two came alongside each other.
- car_conflicts_3knobs_2hz_hybrid_v2_r3_040: actor_hit_ego, policy at fault: unclear. The ego was going straight in its lane at about 8 m/s, gradually slowing, and ended up about 20 m behind where the recorded car was at the same time. Actor 24 came up from behind in the lane to the right and cut left into the ego's lane right beside the ego's front, and the ego's front clipped it (no actor ahead until the 2.3 m gap at impact). The replayed actor was merging into the gap the human driver had left, so a large part of the blame goes to the actor not reacting. The ego's slow pace and late response share some of it.
- car_conflicts_3knobs_2hz_hybrid_v2_r3_041: turned_into_actor, policy at fault: yes. The ego was going straight on a multi-lane highway at about 8 m/s and drifted right, about 0.8 m off the recorded path, onto the right lane line. Vehicle 24 was overtaking in the adjacent right lane and side-swiped the ego (a lateral collision) as it pulled alongside at 8.7 s.
- car_conflicts_3knobs_2hz_hybrid_v2_r3_042: actor_hit_ego, policy at fault: no. The ego was going straight and staying in its lane at a steady ~8.3 m/s, about 20 m behind where the human car had been. Logged actor 24 came up from behind in the right lane and, by 9.2 s, was moving left over the lane line into the ego's right front, triggering a front collision. The replayed actor does not react to the ego, so it cut into the ego's space, most likely along a path that was clear in the original drive.
- car_conflicts_3knobs_2hz_hybrid_v2_r3_047: turned_into_actor, policy at fault: yes. On an open highway with nothing close ahead, the ego braked hard for no clear reason (20.3 to 8.2 m/s after handoff) and fell about 12 m behind the recorded car. While actor 1 passed it in the lane to the left, the ego's planned path angled left toward that lane, and the ego's front-left clipped actor 1's rear-right. The later rear contact is likely a follower catching the ego as it slowed.
- car_conflicts_3knobs_2hz_hybrid_v2_r3_051: turned_into_actor, policy at fault: yes. On an open multi-lane highway with no lead vehicle close by, the ego braked hard for no clear reason (20.3 to 8.6 m/s) and drifted left toward the lane line, about 1.2 m off the recorded path. Actor 1 in the left lane drew level and then pulled ahead, and the ego's front-left corner hit it. The later rear contact was most likely a following car catching the ego after this unneeded braking.
- car_conflicts_3knobs_2hz_hybrid_v2_r3_052: other, policy at fault: yes. On an open highway with nothing ahead, the ego braked hard for no visible reason, slowing from 20 to 9 m/s, and drifted about 1 m left of the human's path. Car 1, replaying the recorded drive in the left lane, caught up and moved over toward the ego's lane, and the ego's front-left clipped its rear-right. The rear-end that followed came from the same unprompted braking.
- car_conflicts_3knobs_2hz_hybrid_v2_r3_053: other, policy at fault: yes. The ego was on an open highway with no lead vehicle within about 47 m, but it braked hard for no clear reason, slowing from 20.3 to 8.5 m/s, and drifted about 1.2 m left of the recorded path. Because of that, actor 1, a replayed car in the left lane that the human driver had been passing, ended up alongside and ahead of the ego and edging toward its lane, and the ego's front-left clipped it. The hard braking also got the ego rear-ended afterwards.

## Every setting

- S1: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_001)
- S2: 096988dd at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_015)
- S3: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_002)
- S4: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_014, car_conflicts_3knobs_2hz_hybrid_v2_r3_021, car_conflicts_3knobs_2hz_hybrid_v2_r3_022)
- S5: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.4: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_023)
- S6: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1.2: 1/1 failed, rate 27%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_024)
- S7: 09a95ffa at actor_time_shift_s -0.5, actor_speed_scale 1.5, ego_speed_scale 1: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_054, car_conflicts_3knobs_2hz_hybrid_v2_r3_055, car_conflicts_3knobs_2hz_hybrid_v2_r3_056)
- S8: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_008)
- S9: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_029)
- S10: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_037)
- S11: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_045, car_conflicts_3knobs_2hz_hybrid_v2_r3_060)
- S12: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_038)
- S13: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 2, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_044)
- S14: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_007)
- S15: 0dbb91dd at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_006)
- S16: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_009)
- S17: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_020)
- S18: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_050)
- S19: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_030_a2)
- S20: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 2, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_049)
- S21: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 2, ego_speed_scale 1.2: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_057, car_conflicts_3knobs_2hz_hybrid_v2_r3_058, car_conflicts_3knobs_2hz_hybrid_v2_r3_059_a2)
- S22: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_034)
- S23: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_019)
- S24: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_003)
- S25: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_018)
- S26: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_025)
- S27: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_043)
- S28: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_026)
- S29: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_032)
- S30: 12855a41 at actor_time_shift_s 0, actor_speed_scale 2, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_031)
- S31: 12855a41 at actor_time_shift_s 0.5, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_033)
- S32: 187e6244 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_005)
- S33: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 1.5, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_036)
- S34: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 2, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_048)
- S35: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_017)
- S36: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_004)
- S37: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_016)
- S38: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_028)
- S39: 19f339ba at actor_time_shift_s 0, actor_speed_scale 2, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_046)
- S40: 19f339ba at actor_time_shift_s 0, actor_speed_scale 2, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_035)
- S41: 19f339ba at actor_time_shift_s 0, actor_speed_scale 2, ego_speed_scale 1.2: 4/4 failed, rate 60%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_047, car_conflicts_3knobs_2hz_hybrid_v2_r3_051, car_conflicts_3knobs_2hz_hybrid_v2_r3_052, car_conflicts_3knobs_2hz_hybrid_v2_r3_053)
- S42: 1c45ce3a at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_013)
- S43: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_012)
- S44: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 0.8: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_040, car_conflicts_3knobs_2hz_hybrid_v2_r3_041, car_conflicts_3knobs_2hz_hybrid_v2_r3_042)
- S45: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_010)
- S46: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_011_a2)
- S47: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_027)
- S48: 1c45ce3a at actor_time_shift_s 0.5, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r3_039)

## Not kept by the gate

- car_conflicts_3knobs_2hz_hybrid_v2_r3_011: not kept: RE-RUN
- car_conflicts_3knobs_2hz_hybrid_v2_r3_030: not kept: RE-RUN
- car_conflicts_3knobs_2hz_hybrid_v2_r3_059: not kept: RE-RUN

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
- A scale above 1 starts the ego behind its recorded start, so for the first second or two of the warm-up it is off the recording.). Report written by claude-opus-5-5 from `results` in 23 s; every count above is computed from the queue, not written by the model.

0 of 63 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
