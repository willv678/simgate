# In cut-in and lead-vehicle scenes that pass as recorded, which combinations of the car's timing, the car's speed and the ego's speed at hand-off make the policy collide or leave the road? The aim is the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `hybrid`: 59 kept runs on 10 scenes, varying actor_time_shift_s, actor_speed_scale, ego_speed_scale; 6 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 2 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The goal was not met. Only two of the five cases the study aimed for were confirmed, each on a different scene. On 19f339ba, the policy failed in every run with the car on time, the car at 1.25x speed and the ego at 1.4x (S24). On 096988dd, it failed in every run with the car on time, the car at 1.25x and the ego at 1.2x (S3). The ranges for both settings lie above 0.5. A third candidate is 19f339ba with the ego at 1.2x (S23). It failed often, but its range still reaches below 0.5, so it is not confirmed.

In every confirmed failure, the ego's speed at hand-off was the knob that mattered. The policy was at fault each time, and none of the failures looks like a simulator artifact. The ego slowed (on 19f339ba it braked hard for no visible reason), drifted left against its route command, and hit a car passing in the left lane. That car was not the retimed one. The study barely varied the car's timing or speed, and the other eight scenes produced no failures in mostly single runs. So the study does not show which timing and car-speed combinations matter.

## Findings

- Confirmed case 1: on 19f339ba, with the car on time, the car at 1.25x and the ego at 1.4x, every kept run collided. Each time the ego braked hard with no close lead, drifted left across the lane line and hit actor 1 as it passed in the left lane. The policy was at fault in all of them, with no possible artifacts.
  - S24: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.4: 7/7 failed, rate 72%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_052, car_conflicts_3knobs_2hz_hybrid_053, car_conflicts_3knobs_2hz_hybrid_054, car_conflicts_3knobs_2hz_hybrid_055, car_conflicts_3knobs_2hz_hybrid_056, car_conflicts_3knobs_2hz_hybrid_057, car_conflicts_3knobs_2hz_hybrid_051_a2)
- Confirmed case 2: on 096988dd, with the car on time, the car at 1.25x and the ego at 1.2x, every run collided. The ego slowed in heavy traffic, drifted left even though the route said straight then right, and hit actor 41 alongside in the left lane. The policy was at fault in all of them.
  - S3: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 5/5 failed, rate 65%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_015, car_conflicts_3knobs_2hz_hybrid_021, car_conflicts_3knobs_2hz_hybrid_022, car_conflicts_3knobs_2hz_hybrid_023, car_conflicts_3knobs_2hz_hybrid_024)
- On 19f339ba with the ego at 1.2x, the same left-drift collision with actor 1 happened in most runs. This is a strong candidate, but its range does not yet lie surely above 0.5.
  - S23: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 7/10 failed, rate 44%-87% (90%) (car_conflicts_3knobs_2hz_hybrid_025, car_conflicts_3knobs_2hz_hybrid_026, car_conflicts_3knobs_2hz_hybrid_031, car_conflicts_3knobs_2hz_hybrid_032, car_conflicts_3knobs_2hz_hybrid_041, car_conflicts_3knobs_2hz_hybrid_042_a2, car_conflicts_3knobs_2hz_hybrid_043_a2, car_conflicts_3knobs_2hz_hybrid_058, car_conflicts_3knobs_2hz_hybrid_059, car_conflicts_3knobs_2hz_hybrid_060)
- On both failing scenes, the ego's speed at hand-off drives the failure, with the car's timing and speed held at 0 s and 1.25x. On 096988dd, the ego at 1.0x did not fail and the ego at 1.2x always failed. On 19f339ba, the failure rate rises from the ego at 1.0x to 1.2x to 1.4x.
  - S2: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_002, car_conflicts_3knobs_2hz_hybrid_014)
  - S3: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 5/5 failed, rate 65%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_015, car_conflicts_3knobs_2hz_hybrid_021, car_conflicts_3knobs_2hz_hybrid_022, car_conflicts_3knobs_2hz_hybrid_023, car_conflicts_3knobs_2hz_hybrid_024)
  - S22: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 1/4 failed, rate 6%-64% (90%) (car_conflicts_3knobs_2hz_hybrid_004, car_conflicts_3knobs_2hz_hybrid_011, car_conflicts_3knobs_2hz_hybrid_012, car_conflicts_3knobs_2hz_hybrid_013)
  - S23: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 7/10 failed, rate 44%-87% (90%) (car_conflicts_3knobs_2hz_hybrid_025, car_conflicts_3knobs_2hz_hybrid_026, car_conflicts_3knobs_2hz_hybrid_031, car_conflicts_3knobs_2hz_hybrid_032, car_conflicts_3knobs_2hz_hybrid_041, car_conflicts_3knobs_2hz_hybrid_042_a2, car_conflicts_3knobs_2hz_hybrid_043_a2, car_conflicts_3knobs_2hz_hybrid_058, car_conflicts_3knobs_2hz_hybrid_059, car_conflicts_3knobs_2hz_hybrid_060)
  - S24: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.4: 7/7 failed, rate 72%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_052, car_conflicts_3knobs_2hz_hybrid_053, car_conflicts_3knobs_2hz_hybrid_054, car_conflicts_3knobs_2hz_hybrid_055, car_conflicts_3knobs_2hz_hybrid_056, car_conflicts_3knobs_2hz_hybrid_057, car_conflicts_3knobs_2hz_hybrid_051_a2)
- The single failure on 19f339ba with the ego at 1.0x is a different kind of failure. After braking for no reason, the ego was struck by replayed actor 18 coming up from behind on the right. Triage could not say whether the policy was at fault, so this run is weak evidence.
  - S22: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 1/4 failed, rate 6%-64% (90%) (car_conflicts_3knobs_2hz_hybrid_004, car_conflicts_3knobs_2hz_hybrid_011, car_conflicts_3knobs_2hz_hybrid_012, car_conflicts_3knobs_2hz_hybrid_013)
- The failures did not come from conflicts with the retimed car. In both failing scenes, the ego hit a different car in the adjacent left lane (actors 1 and 41) after slowing and drifting left. The failure mode is the policy's own unprompted braking and lateral drift, not a cut-in or a braking lead.
  - S3: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 5/5 failed, rate 65%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_015, car_conflicts_3knobs_2hz_hybrid_021, car_conflicts_3knobs_2hz_hybrid_022, car_conflicts_3knobs_2hz_hybrid_023, car_conflicts_3knobs_2hz_hybrid_024)
  - S23: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 7/10 failed, rate 44%-87% (90%) (car_conflicts_3knobs_2hz_hybrid_025, car_conflicts_3knobs_2hz_hybrid_026, car_conflicts_3knobs_2hz_hybrid_031, car_conflicts_3knobs_2hz_hybrid_032, car_conflicts_3knobs_2hz_hybrid_041, car_conflicts_3knobs_2hz_hybrid_042_a2, car_conflicts_3knobs_2hz_hybrid_043_a2, car_conflicts_3knobs_2hz_hybrid_058, car_conflicts_3knobs_2hz_hybrid_059, car_conflicts_3knobs_2hz_hybrid_060)
  - S24: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.4: 7/7 failed, rate 72%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_052, car_conflicts_3knobs_2hz_hybrid_053, car_conflicts_3knobs_2hz_hybrid_054, car_conflicts_3knobs_2hz_hybrid_055, car_conflicts_3knobs_2hz_hybrid_056, car_conflicts_3knobs_2hz_hybrid_057, car_conflicts_3knobs_2hz_hybrid_051_a2)
- No failures were found on the other eight scenes in this search: 023b7fcc, 09a95ffa, 0cf6368d, 0dbb91dd, 0e899dd3, 12855a41, 187e6244 and 1c45ce3a. Most settings there have only one or two runs, which is a hint rather than a rate. 12855a41 held up in a few repeats at the ego 1.2x settings.
  - S1: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_001)
  - S4: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_008)
  - S5: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_020)
  - S6: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_030)
  - S7: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_038)
  - S8: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_007)
  - S9: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_040)
  - S10: 0dbb91dd at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_006)
  - S11: 0e899dd3 at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_037)
  - S12: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_009, car_conflicts_3knobs_2hz_hybrid_050)
  - S13: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_019)
  - S14: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_036)
  - S15: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_035)
  - S16: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_003)
  - S17: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_018, car_conflicts_3knobs_2hz_hybrid_027, car_conflicts_3knobs_2hz_hybrid_033)
  - S18: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_028)
  - S19: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_034, car_conflicts_3knobs_2hz_hybrid_044, car_conflicts_3knobs_2hz_hybrid_045)
  - S20: 12855a41 at actor_time_shift_s 0, actor_speed_scale 2, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_046)
  - S21: 187e6244 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_005)
  - S25: 1c45ce3a at actor_time_shift_s -1, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_049)
  - S26: 1c45ce3a at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_039, car_conflicts_3knobs_2hz_hybrid_048)
  - S27: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_010, car_conflicts_3knobs_2hz_hybrid_016)
  - S28: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_029)
  - S29: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_017)

## Open

- Three more confirmed cases on distinct scenes are still needed. The nearest is 19f339ba with the ego at 1.2x (S23), but it shares a scene with S24. A few more repeats there would show whether it is above 0.5, but they would not count toward the distinct-scene goal.
- Most of the space was never explored. Car timing was only tried at 0, -0.5 and -1 s, never later than recorded. Car speed was only tried at 1.25x to 2x, never slower than recorded. The ego speed was never tried below 1.0x. Runs with a slower lead car (0.5x to 0.75x) and a later cut-in (+1 to +2 s) are needed to test the cut-in and lead-vehicle conflicts the question asks about.
- The ego at 1.4x was only tried on 09a95ffa and 12855a41, once each. Repeating the ego at 1.2x to 1.4x on the scenes with the highest scores, 12855a41, 0e899dd3, 1c45ce3a and 09a95ffa, is the most direct way to find more cases.
- Whether the single failure on 19f339ba with the ego at 1.0x (S22, actor 18 hitting a braking ego) was the policy's fault is unclear. More repeats there would tell whether the ego at 1.0x fails at all.
- The 2 Hz rate was set through control_timestep_us 500000. Nothing in the results confirms that the policy itself planned at VaVAM's 2 Hz rhythm.
- Several runs were not kept (RE-RUN, or HALT on 1c45ce3a at -0.5 s). They are not evidence, and that setting on 1c45ce3a has fewer valid runs than planned.

## Why the runs failed (triage from the video and log)

turned_into_actor 19, actor_hit_ego 1

- car_conflicts_3knobs_2hz_hybrid_004: actor_hit_ego, policy at fault: unclear. On a straight, open highway the ego braked hard for no visible reason, slowing from 15.7 to 6.6 m/s with the nearest vehicle ahead 50+ m away. It fell about 20 m behind where the recorded car was at that time. Replayed actor 18, coming up from behind slightly to the ego's right, drove into the slowed ego, and the contact was scored as a front collision.
- car_conflicts_3knobs_2hz_hybrid_015: turned_into_actor, policy at fault: yes. The ego slowed from 6.7 to 4.4 m/s in heavy highway traffic. While a white pickup (actor 41) passed on its left, the ego drifted and steered left about 1.5 m off the recorded path and across the lane line, even though the route command said RIGHT. Its front hit the pickup's side.
- car_conflicts_3knobs_2hz_hybrid_021: turned_into_actor, policy at fault: yes. On a multi-lane highway in the rain, the policy planned a path drifting left (the route command was STRAIGHT, then RIGHT, and the recorded path went slightly right) and slowed from 6.7 to 4.4 m/s. It moved into the adjacent left lane and its front hit actor 41, which was coming up alongside in that lane.
- car_conflicts_3knobs_2hz_hybrid_022: turned_into_actor, policy at fault: yes. On a multi-lane highway, the ego slowed from 6.7 to 4.6 m/s and drifted left across the lane line, even though the route command was STRAIGHT and then RIGHT. Its front hit actor 41, which was moving alongside in the lane to the left. At impact the ego was 1.7 m off the human trajectory, which stayed in the ego's own lane.
- car_conflicts_3knobs_2hz_hybrid_023: turned_into_actor, policy at fault: yes. The route command was STRAIGHT and then RIGHT, but the policy's planned path kept bending left. The ego drifted out of its lane into the adjacent left lane while slowing from about 6.7 to 4.5 m/s, and its front hit vehicle 41, which was travelling alongside in that lane. At impact the ego was 1.7 m left of the recorded human path.
- car_conflicts_3knobs_2hz_hybrid_024: turned_into_actor, policy at fault: yes. The ego was slowing down on a multi-lane highway and drifted left toward the next lane, even though the route command was RIGHT and the recorded path stayed in or to the right of its lane. Its front hit vehicle 41 as 41 passed on the left and moved just ahead of it.
- car_conflicts_3knobs_2hz_hybrid_025: turned_into_actor, policy at fault: yes. After handoff the ego braked hard for no reason, from 20.3 to 7.9 m/s with the nearest car ahead 40–53 m away. While braking, it drifted left off its planned path toward the next lane. Actor 1 had been driving alongside on the left and pulled ahead as the ego slowed, so the ego's front-left hit it. The ego was also rear-ended at some point, which is consistent with the unneeded hard braking.
- car_conflicts_3knobs_2hz_hybrid_026: turned_into_actor, policy at fault: yes. On a clear highway with the nearest car ahead 40–50 m away, the policy braked for no visible reason, slowing from 20 to 8 m/s, and drifted toward the left lane. Actor 1, which had been beside it on the left, moved ahead, and at 7.6 s the ego's front-left hit actor 1's rear (about 12 m behind where the recorded drive was at that moment). The ego was also rear-ended at some point, likely because of the hard braking.
- car_conflicts_3knobs_2hz_hybrid_032: turned_into_actor, policy at fault: yes. On an open multi-lane highway with the nearest car ahead 40–50 m away, the ego braked hard for no clear reason (20.3 → 8.1 m/s) while drifting left toward the lane line. Actor 1, passing in the left lane, drew level and moved ahead, and the ego's front-left corner hit its rear quarter, about 1.2 m left of the recorded path. Separately, the hard braking led to a vehicle hitting the ego's rear.
- car_conflicts_3knobs_2hz_hybrid_041: turned_into_actor, policy at fault: yes. On an open highway with no lead within about 40 m, the ego braked hard for no clear reason (20.3 to 8.0 m/s) while its planned path veered left across the lane line. Actor 1, in the left lane, overtook the slowing ego, and the ego's front drifted into it at 7.6 s; the later rear contact came after this front collision.
- car_conflicts_3knobs_2hz_hybrid_052: turned_into_actor, policy at fault: yes. On an open highway, the ego braked hard for no clear reason, from 23.7 to 6.6 m/s, while the lead vehicle was 40–50 m ahead and pulling away. As it slowed, it drifted left onto the lane line, and its front-left hit actor 1, which was passing in the left lane.
- car_conflicts_3knobs_2hz_hybrid_053: turned_into_actor, policy at fault: yes. On a straight multi-lane highway, the ego braked hard for no clear reason (23.7 to 6.6 m/s, with the lead vehicle 40–50 m ahead) while drifting left across the lane line. Its front clipped actor 1 as that car came past in the adjacent left lane.
- car_conflicts_3knobs_2hz_hybrid_054: turned_into_actor, policy at fault: yes. On an open highway the ego braked hard for no visible reason, from 23.7 to 6.7 m/s with the lead about 40–50 m ahead and pulling away. While slowing it drifted left toward the lane line, and its front corner hit actor 1, which was coming up alongside in the left lane. The ego was also rear-ended at some point, which is consistent with the sudden braking.
- car_conflicts_3knobs_2hz_hybrid_055: turned_into_actor, policy at fault: yes. On an open highway, with the nearest vehicle ahead 40–53 m away and the gap growing, the ego braked hard for no visible reason, from 23.7 to 6.9 m/s. At the same time it drifted left off the recorded path, toward the next lane over. Actor 1, which had been behind in that lane, came up alongside, and the ego's front corner hit its side at 7.6 s.
- car_conflicts_3knobs_2hz_hybrid_056: turned_into_actor, policy at fault: yes. On an open highway with no close lead (the gap ahead was 40–53 m and growing), the ego braked hard for no clear reason, from 23.7 to 7 m/s, then drifted left toward the next lane. Its front hit actor 1, which was coming up alongside on the left.
- car_conflicts_3knobs_2hz_hybrid_057: turned_into_actor, policy at fault: yes. On a clear highway with no close lead (gap 40–53 m), the ego braked hard for no visible reason, slowing from 23.7 to 6.8 m/s, and drifted about 1.2 m left off the recorded path. Actor 1, coming up from behind in the lane to its left, drew alongside, and the ego's front-left corner struck it at 7.6 s.
- car_conflicts_3knobs_2hz_hybrid_058: turned_into_actor, policy at fault: yes. On a straight highway the policy braked hard for no clear reason (20 to 8 m/s, nothing in its lane within 40 m) and drifted left across the lane line, and its front hit actor 1, which had pulled just ahead in the left lane. The unprompted braking probably also caused the rear-ending.
- car_conflicts_3knobs_2hz_hybrid_059: turned_into_actor, policy at fault: yes. After handoff on a straight multi-lane highway, the ego braked hard for no clear reason (20 → 8 m/s) while the recorded human kept going. Actor 1 in the left lane moved up alongside and then ahead, and the ego's path bent left into that lane, so its front-left hit actor 1. The command at that moment was RIGHT. The ego was rear-ended later, after the front collision, likely because of its hard braking.
- car_conflicts_3knobs_2hz_hybrid_060: turned_into_actor, policy at fault: yes. On a clear multi-lane highway with the nearest lead vehicle 40–50 m ahead, the policy braked hard for no visible reason, dropping from 20.6 to 9.1 m/s, and drifted left toward the lane line while the recorded path bore right. Its front-left corner then struck actor 1, which was moving up beside it in the left lane. The rear contact flagged in the input came from this braking but did not start the failure.
- car_conflicts_3knobs_2hz_hybrid_051_a2: turned_into_actor, policy at fault: yes. On an open highway with no lead within about 40 m, the ego braked hard for no visible reason, slowing from 23.7 to 6.7 m/s. Its planned path also bent left toward the next lane. Actor 1 was coming up from behind on the left, and the ego's front swung into it as the actor drew alongside, which was recorded as an at-fault front collision.

## Every setting

- S1: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_001)
- S2: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_002, car_conflicts_3knobs_2hz_hybrid_014)
- S3: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 5/5 failed, rate 65%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_015, car_conflicts_3knobs_2hz_hybrid_021, car_conflicts_3knobs_2hz_hybrid_022, car_conflicts_3knobs_2hz_hybrid_023, car_conflicts_3knobs_2hz_hybrid_024)
- S4: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_008)
- S5: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_020)
- S6: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_030)
- S7: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_038)
- S8: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_007)
- S9: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_040)
- S10: 0dbb91dd at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_006)
- S11: 0e899dd3 at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_037)
- S12: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_009, car_conflicts_3knobs_2hz_hybrid_050)
- S13: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_019)
- S14: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_036)
- S15: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_035)
- S16: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_003)
- S17: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_018, car_conflicts_3knobs_2hz_hybrid_027, car_conflicts_3knobs_2hz_hybrid_033)
- S18: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_028)
- S19: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_034, car_conflicts_3knobs_2hz_hybrid_044, car_conflicts_3knobs_2hz_hybrid_045)
- S20: 12855a41 at actor_time_shift_s 0, actor_speed_scale 2, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_046)
- S21: 187e6244 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_005)
- S22: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 1/4 failed, rate 6%-64% (90%) (car_conflicts_3knobs_2hz_hybrid_004, car_conflicts_3knobs_2hz_hybrid_011, car_conflicts_3knobs_2hz_hybrid_012, car_conflicts_3knobs_2hz_hybrid_013)
- S23: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 7/10 failed, rate 44%-87% (90%) (car_conflicts_3knobs_2hz_hybrid_025, car_conflicts_3knobs_2hz_hybrid_026, car_conflicts_3knobs_2hz_hybrid_031, car_conflicts_3knobs_2hz_hybrid_032, car_conflicts_3knobs_2hz_hybrid_041, car_conflicts_3knobs_2hz_hybrid_042_a2, car_conflicts_3knobs_2hz_hybrid_043_a2, car_conflicts_3knobs_2hz_hybrid_058, car_conflicts_3knobs_2hz_hybrid_059, car_conflicts_3knobs_2hz_hybrid_060)
- S24: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.4: 7/7 failed, rate 72%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_052, car_conflicts_3knobs_2hz_hybrid_053, car_conflicts_3knobs_2hz_hybrid_054, car_conflicts_3knobs_2hz_hybrid_055, car_conflicts_3knobs_2hz_hybrid_056, car_conflicts_3knobs_2hz_hybrid_057, car_conflicts_3knobs_2hz_hybrid_051_a2)
- S25: 1c45ce3a at actor_time_shift_s -1, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_049)
- S26: 1c45ce3a at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_039, car_conflicts_3knobs_2hz_hybrid_048)
- S27: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_010, car_conflicts_3knobs_2hz_hybrid_016)
- S28: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_029)
- S29: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_017)

## Not kept by the gate

- car_conflicts_3knobs_2hz_hybrid_042: not kept: RE-RUN
- car_conflicts_3knobs_2hz_hybrid_043: not kept: RE-RUN
- car_conflicts_3knobs_2hz_hybrid_047: not kept: RE-RUN
- car_conflicts_3knobs_2hz_hybrid_047_a2: not kept: RE-RUN
- car_conflicts_3knobs_2hz_hybrid_047_a3: not kept: HALT
- car_conflicts_3knobs_2hz_hybrid_051: not kept: RE-RUN

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

0 of 65 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
