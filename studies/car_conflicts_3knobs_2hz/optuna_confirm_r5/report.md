# In cut-in and lead-vehicle scenes that pass as recorded, which combinations of the car's timing, the car's speed and the ego's speed at hand-off make the policy collide or leave the road? The aim is the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `optuna_confirm_r5`: 58 kept runs on 10 scenes, varying actor_time_shift_s, actor_speed_scale, ego_speed_scale; 3 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 3 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The study confirmed 3 of the 5 cases it was asked to find, so the goal was not met. On three scenes, a failure rate above 0.5 is confirmed at one combination each. On 096988dd the car runs 1.5 s early at recorded speed and the ego starts at 1.2x (S9). On 187e6244 the car runs 1 s late at 0.75x and the ego starts at 1.2x (S30). On 023b7fcc the car keeps its recorded timing at 0.75x and the ego starts at 0.6x (S4). In nearly every failure the policy steered left into the next lane, often against a RIGHT or STRAIGHT route command, and hit a car already there. No run left the road, and no failure was flagged as a possible rendering artifact. S30's confirmation is weaker than it looks: in most of its failures the replayed car cut into the ego's lane, so the policy's fault is unclear. A fourth scene, 09a95ffa (S14), failed every time it was run, but it has too few repeats to clear 0.5, and in one of its failures the replayed car hit the ego.

## Findings

- On 096988dd, a car 1.5 s early at recorded speed with the ego at 1.2x failed every repeat. Each failure was the policy turning left into car 41 in the adjacent lane, with the policy at fault. Single runs nearby, one at car speed 0.75x and ego 0.8x and one at car speed 0.5x and ego 1.4x, passed.
  - S9: 096988dd at actor_time_shift_s -1.5, actor_speed_scale 1.0, ego_speed_scale 1.2: 4/4 failed, rate 60%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_001, car_conflicts_3knobs_2hz_optuna_confirm_r5_011, car_conflicts_3knobs_2hz_optuna_confirm_r5_022, car_conflicts_3knobs_2hz_optuna_confirm_r5_026)
  - S8: 096988dd at actor_time_shift_s -1.5, actor_speed_scale 0.75, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_030)
  - S7: 096988dd at actor_time_shift_s -1.5, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_058)
- On 023b7fcc, a car at recorded timing and 0.75x speed with the ego slowed to 0.6x failed every repeat. Each time the policy sideswiped car 56 while moving left out of its lane, with the policy at fault. Single runs that changed only the timing (−2 s with the ego at 1.0x, or +1 s with the car at 1.0x) passed, a hint that the failure is confined to a narrow region.
  - S4: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 0.75, ego_speed_scale 0.6: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_014, car_conflicts_3knobs_2hz_optuna_confirm_r5_021, car_conflicts_3knobs_2hz_optuna_confirm_r5_031)
  - S1: 023b7fcc at actor_time_shift_s -2.0, actor_speed_scale 0.75, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_049)
  - S6: 023b7fcc at actor_time_shift_s 1.0, actor_speed_scale 1.0, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_057)
- On 187e6244, a car 1 s late at 0.75x with the ego at 1.2x failed every repeat. In most of these failures, replayed car 7 cut into the ego's lane just ahead, and fault is unclear. In the other, the ego drifted left into car 7. This case may partly reflect replayed traffic not reacting to the faster ego, not the policy alone.
  - S30: 187e6244 at actor_time_shift_s 1.0, actor_speed_scale 0.75, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_036, car_conflicts_3knobs_2hz_optuna_confirm_r5_041, car_conflicts_3knobs_2hz_optuna_confirm_r5_051_a2)
- On 09a95ffa, a car 0.5 s late at 0.75x with the ego at 0.6x failed every time it was run, but it is not yet confirmed above 0.5. One failure was the policy changing lanes left into vehicle 33. The other was the replayed vehicle 33 closing on the slower ego, with fault unclear. On the same scene, the car 2 s late with the ego at 1.2x did not fail.
  - S14: 09a95ffa at actor_time_shift_s 0.5, actor_speed_scale 0.75, ego_speed_scale 0.6: 2/2 failed, rate 42%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_046, car_conflicts_3knobs_2hz_optuna_confirm_r5_052)
  - S15: 09a95ffa at actor_time_shift_s 2.0, actor_speed_scale 1.0, ego_speed_scale 1.2: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_040, car_conflicts_3knobs_2hz_optuna_confirm_r5_043)
- The failure mode found is lateral. The policy leaves its lane to the left into an occupied lane, not a failure to brake for the lead car. Both ego speed directions can trigger it: faster (1.2x) on two scenes, slower (0.6x) on two.
  - S9: 096988dd at actor_time_shift_s -1.5, actor_speed_scale 1.0, ego_speed_scale 1.2: 4/4 failed, rate 60%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_001, car_conflicts_3knobs_2hz_optuna_confirm_r5_011, car_conflicts_3knobs_2hz_optuna_confirm_r5_022, car_conflicts_3knobs_2hz_optuna_confirm_r5_026)
  - S4: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 0.75, ego_speed_scale 0.6: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_014, car_conflicts_3knobs_2hz_optuna_confirm_r5_021, car_conflicts_3knobs_2hz_optuna_confirm_r5_031)
  - S30: 187e6244 at actor_time_shift_s 1.0, actor_speed_scale 0.75, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_036, car_conflicts_3knobs_2hz_optuna_confirm_r5_041, car_conflicts_3knobs_2hz_optuna_confirm_r5_051_a2)
  - S14: 09a95ffa at actor_time_shift_s 0.5, actor_speed_scale 0.75, ego_speed_scale 0.6: 2/2 failed, rate 42%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_046, car_conflicts_3knobs_2hz_optuna_confirm_r5_052)
- Repeated settings on 19f339ba, 12855a41, 0cf6368d and 0e899dd3 never failed, and their ranges sit below 0.5. Every run on 0dbb91dd had zero criticality, so it showed no near misses at all.
  - S31: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 1.5, ego_speed_scale 0.6: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_008, car_conflicts_3knobs_2hz_optuna_confirm_r5_012, car_conflicts_3knobs_2hz_optuna_confirm_r5_024, car_conflicts_3knobs_2hz_optuna_confirm_r5_033, car_conflicts_3knobs_2hz_optuna_confirm_r5_042, car_conflicts_3knobs_2hz_optuna_confirm_r5_053)
  - S27: 12855a41 at actor_time_shift_s -1.5, actor_speed_scale 2.0, ego_speed_scale 1.0: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_018, car_conflicts_3knobs_2hz_optuna_confirm_r5_023, car_conflicts_3knobs_2hz_optuna_confirm_r5_034, car_conflicts_3knobs_2hz_optuna_confirm_r5_044, car_conflicts_3knobs_2hz_optuna_confirm_r5_054)
  - S17: 0cf6368d at actor_time_shift_s 0.5, actor_speed_scale 1.0, ego_speed_scale 1.2: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_027, car_conflicts_3knobs_2hz_optuna_confirm_r5_035, car_conflicts_3knobs_2hz_optuna_confirm_r5_045, car_conflicts_3knobs_2hz_optuna_confirm_r5_055)
  - S25: 0e899dd3 at actor_time_shift_s -1.0, actor_speed_scale 2.0, ego_speed_scale 1.2: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_006, car_conflicts_3knobs_2hz_optuna_confirm_r5_013, car_conflicts_3knobs_2hz_optuna_confirm_r5_025)
  - S19: 0dbb91dd at actor_time_shift_s -2.0, actor_speed_scale 0.5, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_010)
  - S20: 0dbb91dd at actor_time_shift_s -1.5, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_037)
  - S21: 0dbb91dd at actor_time_shift_s 0.0, actor_speed_scale 1.0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_007)
  - S22: 0dbb91dd at actor_time_shift_s 1.0, actor_speed_scale 1.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_009)
  - S23: 0dbb91dd at actor_time_shift_s 1.5, actor_speed_scale 1.5, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_015)
  - S24: 0dbb91dd at actor_time_shift_s 2.0, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_003)
- The closest near misses that did not fail were single runs: 023b7fcc with the car 1.5 s early at 1.5x and the ego at 0.6x, and 096988dd with the car at recorded timing and 0.5x and the ego at 1.2x, or 0.5 s early at 1.25x with the ego at 1.0x. They sit on scenes that already have a confirmed case.
  - S2: 023b7fcc at actor_time_shift_s -1.5, actor_speed_scale 1.5, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_050)
  - S11: 096988dd at actor_time_shift_s 0.0, actor_speed_scale 0.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_056)
  - S10: 096988dd at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_017)

## Open

- Whether 09a95ffa (S14) is a confirmed fourth case: a few more repeats of S14 would settle it. It would still be worth checking how many failures are the policy's and how many come from replayed vehicle 33.
- Whether S30 is really a policy failure: in most of its failures a replayed car cut in ahead, with fault unclear. Repeats with reactive traffic, or a review of the cut-in timing, would tell whether the policy itself fails there.
- No fifth scene has any failure. The best remaining candidates are on scenes with high criticality but only single runs: 12855a41 (S28, S29), 1c45ce3a (S33) and 0e899dd3 (S26). Settings near these that push the ego toward an occupied left lane are the place to search next.
- 1c45ce3a with the ego at 1.4x is unexplored: both runs there halted and were not kept (car at +1 s and 1.25x, and car at 0 s and 1.5x). They need re-running.
- How large each failing region is: the neighbours of S4 and S9 that passed were single runs, so they only hint that the failures are local. A few runs one step away on each knob would map it.
- The plan sets the control timestep to 500 ms, but the plan itself says nothing checks that the runs actually planned at 2 Hz. That still needs to be verified from the run logs.

## Why the runs failed (triage from the video and log)

turned_into_actor 9, actor_hit_ego 3

- car_conflicts_3knobs_2hz_optuna_confirm_r5_001: turned_into_actor, policy at fault: yes. On a wet multi-lane highway, the policy steered left out of its lane even though the route said STRAIGHT and then RIGHT, and the recorded human path stayed to the right. It moved into the next lane, where actor 41 was driving beside it and slightly ahead, and the ego's front hit 41 at about 4 m/s.
- car_conflicts_3knobs_2hz_optuna_confirm_r5_011: turned_into_actor, policy at fault: yes. On a multi-lane highway in the rain, the ego slowed from 6.7 to 4.7 m/s and turned left toward the adjacent lane. Vehicle 41 was coming up alongside in that lane, and the ego's front corner hit it at 7.2 s. The recorded human also moved left, but later, after 41 had passed. The ego cut in while the lane was still occupied, and the camera view was clear beforehand.
- car_conflicts_3knobs_2hz_optuna_confirm_r5_014: turned_into_actor, policy at fault: yes. The route said RIGHT and the recorded human path went right, but the ego steered left into the next lane over while speeding up from 2.5 to 5.3 m/s. It sideswiped actor 56, which was alongside and slightly behind it in that lane (a lateral collision at 7.7 s).
- car_conflicts_3knobs_2hz_optuna_confirm_r5_021: turned_into_actor, policy at fault: yes. On a multi-lane road with the command STRAIGHT, the ego left the recorded path, which stayed in its lane behind car 12, and drifted left into the next lane. Car 56 was already in that lane, coming up from behind on the left, and the ego hit it side-on (lateral collision at 7.7s, 1.8 m off the recording).
- car_conflicts_3knobs_2hz_optuna_confirm_r5_022: turned_into_actor, policy at fault: yes. On a wet multi-lane freeway, the ego slowed and drifted left toward the next lane over, even though the route command was RIGHT and the recorded human path went right. Its front then struck actor 41, a pickup that was overtaking in that left lane and had pulled just ahead of the ego.
- car_conflicts_3knobs_2hz_optuna_confirm_r5_026: turned_into_actor, policy at fault: yes. On a multi-lane highway with a STRAIGHT command, the policy's plan (orange) veered left toward the adjacent lane while the recorded path stayed straight. By 7.2s the ego had angled left into the side of car 41, which was driving alongside it in that lane, and the left-front corner made contact.
- car_conflicts_3knobs_2hz_optuna_confirm_r5_031: turned_into_actor, policy at fault: yes. The ego was going about 5 m/s in slow highway traffic and steered left out of its lane, even though the recorded path went straight and the command then changed to RIGHT. It cut across the lane line into the left lane and sideswiped actor 56, which was alongside and slightly behind it. The rear-contact flag likely comes from that same merge.
- car_conflicts_3knobs_2hz_optuna_confirm_r5_036: actor_hit_ego, policy at fault: unclear. On the highway, the ego stayed in its lane and kept speeding up (4.2 to 5.9 m/s). The recorded human had moved left out of that lane. Actor 7, a replayed car from the left lane, passed the ego and cut right into the ego's lane only about 4 m ahead, and the ego's front corner clipped its rear.
- car_conflicts_3knobs_2hz_optuna_confirm_r5_041: actor_hit_ego, policy at fault: unclear. The ego was going straight in its lane on a freeway, speeding up from 4.1 to 5.5 m/s with an open lane ahead. Actor 7, in the lane to its left and slightly ahead, drifted right into the ego's lane, and the ego's front-left corner struck it at 11.2s. The ego was about 18 m ahead of where the human driver was at that point, so it reached the spot where the replayed actor merged, and it didn't slow down or yield to the car moving over.
- car_conflicts_3knobs_2hz_optuna_confirm_r5_046: turned_into_actor, policy at fault: yes. The ego was following vehicle 1 at a safe gap (about 10 m). It then started to change lanes to the left, against a RIGHT route command, and its front hit vehicle 33, which was right alongside in the left lane. That vehicle shows as a smeared car at the left edge of the camera view at impact.
- car_conflicts_3knobs_2hz_optuna_confirm_r5_052: actor_hit_ego, policy at fault: unclear. The ego followed lead car 1 at about 3.4–4.3 m/s and fell about 12.6 m behind where the human car was at the same time. Actor 33 then came up fast from behind in the lane to the left and moved into the ego's front-left corner. The ego was not moving left; its planned path pointed right. The likely cause is that actor 33 is replayed from the recording and closed a gap that the slower ego was still occupying.
- car_conflicts_3knobs_2hz_optuna_confirm_r5_051_a2: turned_into_actor, policy at fault: yes. In slow freeway traffic, the ego sped up from 3.6 to 5.2 m/s and drifted left until it was straddling the lane line. Its front corner then hit actor 7, which was driving alongside in the left lane. The car ahead (48) was always more than 8 m away and was not involved.

## Every setting

- S1: 023b7fcc at actor_time_shift_s -2.0, actor_speed_scale 0.75, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_049)
- S2: 023b7fcc at actor_time_shift_s -1.5, actor_speed_scale 1.5, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_050)
- S3: 023b7fcc at actor_time_shift_s -1.0, actor_speed_scale 0.5, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_048)
- S4: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 0.75, ego_speed_scale 0.6: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_014, car_conflicts_3knobs_2hz_optuna_confirm_r5_021, car_conflicts_3knobs_2hz_optuna_confirm_r5_031)
- S5: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 2.0, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_059)
- S6: 023b7fcc at actor_time_shift_s 1.0, actor_speed_scale 1.0, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_057)
- S7: 096988dd at actor_time_shift_s -1.5, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_058)
- S8: 096988dd at actor_time_shift_s -1.5, actor_speed_scale 0.75, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_030)
- S9: 096988dd at actor_time_shift_s -1.5, actor_speed_scale 1.0, ego_speed_scale 1.2: 4/4 failed, rate 60%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_001, car_conflicts_3knobs_2hz_optuna_confirm_r5_011, car_conflicts_3knobs_2hz_optuna_confirm_r5_022, car_conflicts_3knobs_2hz_optuna_confirm_r5_026)
- S10: 096988dd at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_017)
- S11: 096988dd at actor_time_shift_s 0.0, actor_speed_scale 0.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_056)
- S12: 096988dd at actor_time_shift_s 1.0, actor_speed_scale 2.0, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_019)
- S13: 096988dd at actor_time_shift_s 1.5, actor_speed_scale 1.0, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_039)
- S14: 09a95ffa at actor_time_shift_s 0.5, actor_speed_scale 0.75, ego_speed_scale 0.6: 2/2 failed, rate 42%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_046, car_conflicts_3knobs_2hz_optuna_confirm_r5_052)
- S15: 09a95ffa at actor_time_shift_s 2.0, actor_speed_scale 1.0, ego_speed_scale 1.2: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_040, car_conflicts_3knobs_2hz_optuna_confirm_r5_043)
- S16: 0cf6368d at actor_time_shift_s -2.0, actor_speed_scale 1.25, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_016)
- S17: 0cf6368d at actor_time_shift_s 0.5, actor_speed_scale 1.0, ego_speed_scale 1.2: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_027, car_conflicts_3knobs_2hz_optuna_confirm_r5_035, car_conflicts_3knobs_2hz_optuna_confirm_r5_045, car_conflicts_3knobs_2hz_optuna_confirm_r5_055)
- S18: 0cf6368d at actor_time_shift_s 2.0, actor_speed_scale 1.25, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_005)
- S19: 0dbb91dd at actor_time_shift_s -2.0, actor_speed_scale 0.5, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_010)
- S20: 0dbb91dd at actor_time_shift_s -1.5, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_037)
- S21: 0dbb91dd at actor_time_shift_s 0.0, actor_speed_scale 1.0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_007)
- S22: 0dbb91dd at actor_time_shift_s 1.0, actor_speed_scale 1.0, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_009)
- S23: 0dbb91dd at actor_time_shift_s 1.5, actor_speed_scale 1.5, ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_015)
- S24: 0dbb91dd at actor_time_shift_s 2.0, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_003)
- S25: 0e899dd3 at actor_time_shift_s -1.0, actor_speed_scale 2.0, ego_speed_scale 1.2: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_006, car_conflicts_3knobs_2hz_optuna_confirm_r5_013, car_conflicts_3knobs_2hz_optuna_confirm_r5_025)
- S26: 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 1.0, ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_047)
- S27: 12855a41 at actor_time_shift_s -1.5, actor_speed_scale 2.0, ego_speed_scale 1.0: 0/5 failed, rate 0%-35% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_018, car_conflicts_3knobs_2hz_optuna_confirm_r5_023, car_conflicts_3knobs_2hz_optuna_confirm_r5_034, car_conflicts_3knobs_2hz_optuna_confirm_r5_044, car_conflicts_3knobs_2hz_optuna_confirm_r5_054)
- S28: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 0.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_020)
- S29: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_038)
- S30: 187e6244 at actor_time_shift_s 1.0, actor_speed_scale 0.75, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_036, car_conflicts_3knobs_2hz_optuna_confirm_r5_041, car_conflicts_3knobs_2hz_optuna_confirm_r5_051_a2)
- S31: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 1.5, ego_speed_scale 0.6: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_008, car_conflicts_3knobs_2hz_optuna_confirm_r5_012, car_conflicts_3knobs_2hz_optuna_confirm_r5_024, car_conflicts_3knobs_2hz_optuna_confirm_r5_033, car_conflicts_3knobs_2hz_optuna_confirm_r5_042, car_conflicts_3knobs_2hz_optuna_confirm_r5_053)
- S32: 19f339ba at actor_time_shift_s 1.5, actor_speed_scale 1.0, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_002)
- S33: 1c45ce3a at actor_time_shift_s -1.5, actor_speed_scale 0.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_060)
- S34: 1c45ce3a at actor_time_shift_s -1.5, actor_speed_scale 1.0, ego_speed_scale 1.0: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_optuna_confirm_r5_028, car_conflicts_3knobs_2hz_optuna_confirm_r5_032)

## Not kept by the gate

- car_conflicts_3knobs_2hz_optuna_confirm_r5_004: not kept: HALT
- car_conflicts_3knobs_2hz_optuna_confirm_r5_029: not kept: HALT
- car_conflicts_3knobs_2hz_optuna_confirm_r5_051: not kept: RE-RUN

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
- A scale above 1 starts the ego behind its recorded start, so for the first second or two of the warm-up it is off the recording.). Report written by claude-opus-5-5 from `results` in 31 s; every count above is computed from the queue, not written by the model.

0 of 61 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
