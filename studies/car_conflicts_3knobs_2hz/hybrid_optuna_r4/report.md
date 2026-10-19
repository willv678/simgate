# In cut-in and lead-vehicle scenes that pass as recorded, which combinations of the car's timing, the car's speed and the ego's speed at hand-off make the policy collide or leave the road? The aim is the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `hybrid_optuna_r4`: 58 kept runs on 10 scenes, varying actor_time_shift_s, actor_speed_scale, ego_speed_scale; 9 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 2 of 5 challenging settings confirmed, after 6 rounds.

## Answer

I could confirm two of the five cases the brief asked for, each on a different scene. Every run failed at each of them. On 096988dd, the failing setting is the car 1 s earlier at its recorded speed with the ego at 1.4x (S3). On 19f339ba, it is the car 1 s later at its recorded speed with the ego at 1.4x (S18). The S3 failures are clearly the policy's fault. It drifts left against a STRAIGHT/RIGHT command into a pickup passing in the next lane. The S18 failures are less clean. Each one starts with the hand-off putting the ego about 1 m behind the lead car at high speed. The ego then brakes hard and drifts left into a passing car, and the triage blames the policy in only some of those runs. In both cases the car the ego hits is a neighbour in the next lane, not the retimed car. Many other settings with the ego at 1.4x did not fail, so the full-speed ego is common to both failures but does not cause failure on its own. Only one other scene, 0cf6368d (S6), produced a policy-fault failure, and it failed once in several repeats. So the study ends short of its goal: two confirmed cases, one weak candidate and no others.

## Findings

- On 096988dd, the car retimed 1 s earlier at its recorded speed with the ego at 1.4x failed in every run, and the policy was at fault each time. The ego slowed and drifted left against a STRAIGHT-then-RIGHT command, and its front corner hit actor 41 passing in the left lane. Actor 41 is not the retimed car.
  - S3: 096988dd at actor_time_shift_s -1, actor_speed_scale 1, ego_speed_scale 1.4: 4/4 failed, rate 60%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r4_005, car_conflicts_3knobs_2hz_hybrid_optuna_r4_011, car_conflicts_3knobs_2hz_hybrid_optuna_r4_012, car_conflicts_3knobs_2hz_hybrid_optuna_r4_013)
- On 19f339ba, the car retimed 1 s later at its recorded speed with the ego at 1.4x failed in every run. The hand-off puts the ego about 1 m behind lead car 18 at high speed. The ego brakes hard, and actor 1 rear-ends it. It then drifts left into actor 1 passing on the left (in one run, actor 28 hits it from the right instead). The triage blames the policy in about half the runs and calls the rest unclear, so part of this case may come from how the scaled ego speed places the ego at hand-off.
  - S18: 19f339ba at actor_time_shift_s 1, actor_speed_scale 1, ego_speed_scale 1.4: 6/6 failed, rate 69%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r4_043, car_conflicts_3knobs_2hz_hybrid_optuna_r4_052, car_conflicts_3knobs_2hz_hybrid_optuna_r4_053, car_conflicts_3knobs_2hz_hybrid_optuna_r4_054, car_conflicts_3knobs_2hz_hybrid_optuna_r4_055, car_conflicts_3knobs_2hz_hybrid_optuna_r4_051_a2)
- On 19f339ba with the car at 1.5x and the ego at 0.6x, some runs failed, but the range does not settle whether the rate is above 0.5. The failures that were triaged are phantom braking on an open highway, after which a replayed car runs into the ego from behind or the side. That is a rear-end-type conflict the plan said to ignore, and the triage does not pin it on the policy. The setting is also on the same scene as S18, so it cannot be a separate case.
  - S17: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 0.6: 4/10 failed, rate 19%-65% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r4_002, car_conflicts_3knobs_2hz_hybrid_optuna_r4_017, car_conflicts_3knobs_2hz_hybrid_optuna_r4_018_a2, car_conflicts_3knobs_2hz_hybrid_optuna_r4_021, car_conflicts_3knobs_2hz_hybrid_optuna_r4_022, car_conflicts_3knobs_2hz_hybrid_optuna_r4_023, car_conflicts_3knobs_2hz_hybrid_optuna_r4_031, car_conflicts_3knobs_2hz_hybrid_optuna_r4_032, car_conflicts_3knobs_2hz_hybrid_optuna_r4_033, car_conflicts_3knobs_2hz_hybrid_optuna_r4_034)
- On 0cf6368d, with the car 2 s earlier at half speed and the ego at 1.4x, one run failed and the rest did not. The failure was the policy's: in stop-and-go traffic it crept left into stopped car 24. This is a hint, not a confirmed case.
  - S6: 0cf6368d at actor_time_shift_s -2, actor_speed_scale 0.5, ego_speed_scale 1.4: 1/4 failed, rate 6%-64% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r4_001, car_conflicts_3knobs_2hz_hybrid_optuna_r4_014, car_conflicts_3knobs_2hz_hybrid_optuna_r4_015, car_conflicts_3knobs_2hz_hybrid_optuna_r4_016)
- Several settings were repeated and never failed, with ranges that stay below 0.5. They are unlikely to be challenging cases: 09a95ffa (car 2 s early at 1.5x, ego 1.4x), 0e899dd3 (car 0.5 s late at 2x, ego 1.4x), 187e6244 (car 1.5 s late, ego 1.4x) and 1c45ce3a (car 2 s early at 2x, ego 0.6x).
  - S4: 09a95ffa at actor_time_shift_s -2, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r4_009_a2, car_conflicts_3knobs_2hz_hybrid_optuna_r4_029, car_conflicts_3knobs_2hz_hybrid_optuna_r4_038, car_conflicts_3knobs_2hz_hybrid_optuna_r4_039)
  - S11: 0e899dd3 at actor_time_shift_s 0.5, actor_speed_scale 2, ego_speed_scale 1.4: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r4_008, car_conflicts_3knobs_2hz_hybrid_optuna_r4_019_a2, car_conflicts_3knobs_2hz_hybrid_optuna_r4_024, car_conflicts_3knobs_2hz_hybrid_optuna_r4_025)
  - S15: 187e6244 at actor_time_shift_s 1.5, actor_speed_scale 1, ego_speed_scale 1.4: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r4_046_a2, car_conflicts_3knobs_2hz_hybrid_optuna_r4_056, car_conflicts_3knobs_2hz_hybrid_optuna_r4_057, car_conflicts_3knobs_2hz_hybrid_optuna_r4_058)
  - S19: 1c45ce3a at actor_time_shift_s -2, actor_speed_scale 2, ego_speed_scale 0.6: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r4_030, car_conflicts_3knobs_2hz_hybrid_optuna_r4_035, car_conflicts_3knobs_2hz_hybrid_optuna_r4_037, car_conflicts_3knobs_2hz_hybrid_optuna_r4_036_a2)
- With the ego at 1.4x, settings on 023b7fcc, 09a95ffa, 0cf6368d, 0e899dd3, 12855a41 and 187e6244 produced no failures. A full-speed ego is common to both confirmed cases, but it does not cause failure by itself.
  - S1: 023b7fcc at actor_time_shift_s -1.5, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r4_007, car_conflicts_3knobs_2hz_hybrid_optuna_r4_020, car_conflicts_3knobs_2hz_hybrid_optuna_r4_040)
  - S4: 09a95ffa at actor_time_shift_s -2, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r4_009_a2, car_conflicts_3knobs_2hz_hybrid_optuna_r4_029, car_conflicts_3knobs_2hz_hybrid_optuna_r4_038, car_conflicts_3knobs_2hz_hybrid_optuna_r4_039)
  - S7: 0cf6368d at actor_time_shift_s -1, actor_speed_scale 1, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r4_041)
  - S8: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r4_042)
  - S10: 0e899dd3 at actor_time_shift_s -1.5, actor_speed_scale 1, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r4_048)
  - S11: 0e899dd3 at actor_time_shift_s 0.5, actor_speed_scale 2, ego_speed_scale 1.4: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r4_008, car_conflicts_3knobs_2hz_hybrid_optuna_r4_019_a2, car_conflicts_3knobs_2hz_hybrid_optuna_r4_024, car_conflicts_3knobs_2hz_hybrid_optuna_r4_025)
  - S13: 12855a41 at actor_time_shift_s 2, actor_speed_scale 1, ego_speed_scale 1.4: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r4_047, car_conflicts_3knobs_2hz_hybrid_optuna_r4_059, car_conflicts_3knobs_2hz_hybrid_optuna_r4_060)
  - S15: 187e6244 at actor_time_shift_s 1.5, actor_speed_scale 1, ego_speed_scale 1.4: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r4_046_a2, car_conflicts_3knobs_2hz_hybrid_optuna_r4_056, car_conflicts_3knobs_2hz_hybrid_optuna_r4_057, car_conflicts_3knobs_2hz_hybrid_optuna_r4_058)

## Open

- Three of the five cases are still missing. 0cf6368d is the only other scene with a policy-fault failure, so its setting (car -2 s, 0.5x, ego 1.4x) needs about four more runs. Its neighbours (car at 0.75x, or -1.5 s) are also worth trying.
- Whether S18 is the policy's failure or comes from the hand-off placing the ego about 1 m behind lead 18. Repeating it with the ego at 1.2x, or with the car shifted to +1.5 s or +2 s, would show whether the left drift into actor 1 survives without the near-contact at hand-off.
- Whether the S3 left drift on 096988dd depends on the knobs at all: run the recorded car timing and speed with the ego at 1.4x, and the S3 car timing with the ego at 1.0x.
- Scenes that got only one or two runs and no failures: 0dbb91dd (S9), 023b7fcc (S2), 09a95ffa (S5), 0cf6368d (S7, S8), 0e899dd3 (S10) and 12855a41 (S12). Each needs more search before it can be ruled out.
- On 1c45ce3a, two runs with the ego at 1.4x halted and were not kept, so the scene was effectively searched only at ego 0.6x (S19).
- The plan assumed the 2 Hz planning rate but nothing checked it. The fixed control timestep is 500 ms, but whether the policy itself planned at 2 Hz was not verified.

## Why the runs failed (triage from the video and log)

turned_into_actor 10, actor_hit_ego 4, other 1

- car_conflicts_3knobs_2hz_hybrid_optuna_r4_001: turned_into_actor, policy at fault: yes. In stop-and-go traffic with a LEFT command, the ego crept forward at about 1 m/s while edging left across the lane line toward the lane of stopped car 24. It closed the gap and its front ran into 24's rear corner, about 3.3 m off the recorded path.
- car_conflicts_3knobs_2hz_hybrid_optuna_r4_005: turned_into_actor, policy at fault: yes. On a multi-lane highway, the ego slowed from 7.9 to 4.5 m/s while its plan (orange) pulled it left, even though the route command was STRAIGHT and then RIGHT. Its front corner hit actor 41 (the white pickup), which was passing in the lane to the left.
- car_conflicts_3knobs_2hz_hybrid_optuna_r4_011: turned_into_actor, policy at fault: yes. On a multi-lane highway the ego slowed from 7.9 to 4.5 m/s and drifted left toward the next lane, even though the route command was STRAIGHT and then RIGHT and the human drove straight. Its front corner hit the white pickup (actor 41) as it came up alongside on the left.
- car_conflicts_3knobs_2hz_hybrid_optuna_r4_012: turned_into_actor, policy at fault: yes. On a multi-lane highway, the ego slowed from 7.9 to 4.4 m/s while its plan drifted left, even though the route command was STRAIGHT and then RIGHT. Its front hit actor 41, a white SUV that was overtaking in the adjacent left lane; at impact the ego's box is across the lane line under 41's rear.
- car_conflicts_3knobs_2hz_hybrid_optuna_r4_013: turned_into_actor, policy at fault: yes. On a multi-lane highway the command was STRAIGHT, then RIGHT. Instead of following it, the ego drifted left out of its lane toward the left lane line while slowing from 7.9 to 4.3 m/s. Actor 41 was passing on the left, and the ego's front struck it as the ego moved into that lane, about 1.7 m off the recorded path, which stayed straight and bore right.
- car_conflicts_3knobs_2hz_hybrid_optuna_r4_018_a2: other, policy at fault: unclear. On a clear multi-lane highway with no lead vehicle (gap null after handoff), the policy slowed for no reason, from 10.1 to 6.9 m/s, falling about 20 m behind where the human drove. Actor 28, which replays the logged drive and cannot react, came up from behind and overlapped the ego's rear at 7.1 s. That overlap was scored as an at-fault front collision, even though it is really a rear-end set off by the ego's phantom braking.
- car_conflicts_3knobs_2hz_hybrid_optuna_r4_021: actor_hit_ego, policy at fault: unclear. On an open highway with no lead vehicle, the ego stayed on the recorded path (0.4 m off) but slowed from about 10 to 6.9 m/s for no visible reason, ending up about 20 m behind where the human was. Replayed actor 23 came up from behind on the right, cut into the ego's lane and overlapped the ego's front-right corner. This was logged as a front collision, and the run also shows rear contact.
- car_conflicts_3knobs_2hz_hybrid_optuna_r4_022: actor_hit_ego, policy at fault: unclear. On a clear highway with no lead vehicle within 50 m, the ego slowed for no apparent reason from 10.1 to 6.8 m/s after handoff, ending up about 20 m behind where the human drove. Actor 23, which replays the recorded drive and doesn't react to the ego, came up from behind and slightly to the right and drove into the slowed ego at 7.1 s. The overlap was recorded as a front collision, but the run is also flagged rear_ended.
- car_conflicts_3knobs_2hz_hybrid_optuna_r4_033: actor_hit_ego, policy at fault: unclear. On an open multi-lane highway with no close lead (gap about 57 m), the ego slowed steadily for no clear reason, from 10.1 to 6.8 m/s after handoff, and fell about 20 m behind the recorded drive. At 7.1 s, replayed actor 18 coming up from behind overlaps the ego's rear-right corner; this is logged as a front collision but looks like the follower running into the slowed ego.
- car_conflicts_3knobs_2hz_hybrid_optuna_r4_043: turned_into_actor, policy at fault: unclear. Right after handoff on a straight highway, replayed actor 18 overlapped the ego's rear (a rear contact at 5.6s) and drove through it. The ego then braked hard, from 23.7 to 6.2 m/s, and ended up about 10 m behind where the recorded car was; drifting slightly left (1.2 m off the recorded path), its front-left corner hit actor 1, which was passing in the left lane at 7.6s.
- car_conflicts_3knobs_2hz_hybrid_optuna_r4_052: turned_into_actor, policy at fault: yes. At handoff the ego was going 23.7 m/s only 1.3 m behind actor 18, with boxes touching at 5.6 s. It then braked hard to 5.8 m/s even though the lane ahead had cleared to about 50 m, and drifted left off its planned path into the next lane, where its front-left corner hit actor 1 as actor 1 passed the slowing ego at 7.6 s.
- car_conflicts_3knobs_2hz_hybrid_optuna_r4_053: turned_into_actor, policy at fault: yes. The policy took over on the highway already about 1 m behind actor 18. It braked hard (23.7 to 6.3 m/s) even after 18 pulled away, and actor 1 hit the ego's rear around 5.6 s. With the ego slow and its nose drifting left toward the adjacent lane, its front-left then struck actor 1 as actor 1 came alongside at 7.6 s.
- car_conflicts_3knobs_2hz_hybrid_optuna_r4_054: turned_into_actor, policy at fault: yes. The policy took over at 23.7 m/s only 1.3 m behind lead car 18. It braked hard, down to 6.5 m/s, and actor 1 rear-ended it at about 5.6 s. Actor 1 then pulled up on the ego's left, and at 7.6 s the ego's planned path hooked left and its front struck actor 1, even though the lane ahead was clear (54 m gap).
- car_conflicts_3knobs_2hz_hybrid_optuna_r4_055: turned_into_actor, policy at fault: unclear. The policy took over only 1.3 m behind actor 18. It braked hard from 23.7 to 6.5 m/s while the recorded human kept going, and actor 1 hit its rear at about 5.6 s. Still braking, the ego then drifted about 1.2 m left of its recorded line toward the left lane. At 7.6 s its front-left hit actor 1, which by then was moving into the left lane and was alongside.
- car_conflicts_3knobs_2hz_hybrid_optuna_r4_051_a2: actor_hit_ego, policy at fault: unclear. The ego got within about 1 m of lead vehicle 18 at 18 m/s and then braked hard, dropping to about 5 m/s on an open highway lane (the gap ahead had grown to 54 m) and drifting slightly left. By 8.6 s it was about 20 m behind where the recorded car was, and vehicle 28, replayed from the recording and coming up from behind on the right, drove into the ego's front-right side, which counted as a front collision.

## Every setting

- S1: 023b7fcc at actor_time_shift_s -1.5, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r4_007, car_conflicts_3knobs_2hz_hybrid_optuna_r4_020, car_conflicts_3knobs_2hz_hybrid_optuna_r4_040)
- S2: 023b7fcc at actor_time_shift_s -1, actor_speed_scale 1, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r4_050)
- S3: 096988dd at actor_time_shift_s -1, actor_speed_scale 1, ego_speed_scale 1.4: 4/4 failed, rate 60%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r4_005, car_conflicts_3knobs_2hz_hybrid_optuna_r4_011, car_conflicts_3knobs_2hz_hybrid_optuna_r4_012, car_conflicts_3knobs_2hz_hybrid_optuna_r4_013)
- S4: 09a95ffa at actor_time_shift_s -2, actor_speed_scale 1.5, ego_speed_scale 1.4: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r4_009_a2, car_conflicts_3knobs_2hz_hybrid_optuna_r4_029, car_conflicts_3knobs_2hz_hybrid_optuna_r4_038, car_conflicts_3knobs_2hz_hybrid_optuna_r4_039)
- S5: 09a95ffa at actor_time_shift_s -1, actor_speed_scale 0.75, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r4_049_a2)
- S6: 0cf6368d at actor_time_shift_s -2, actor_speed_scale 0.5, ego_speed_scale 1.4: 1/4 failed, rate 6%-64% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r4_001, car_conflicts_3knobs_2hz_hybrid_optuna_r4_014, car_conflicts_3knobs_2hz_hybrid_optuna_r4_015, car_conflicts_3knobs_2hz_hybrid_optuna_r4_016)
- S7: 0cf6368d at actor_time_shift_s -1, actor_speed_scale 1, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r4_041)
- S8: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r4_042)
- S9: 0dbb91dd at actor_time_shift_s 1, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r4_006)
- S10: 0e899dd3 at actor_time_shift_s -1.5, actor_speed_scale 1, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r4_048)
- S11: 0e899dd3 at actor_time_shift_s 0.5, actor_speed_scale 2, ego_speed_scale 1.4: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r4_008, car_conflicts_3knobs_2hz_hybrid_optuna_r4_019_a2, car_conflicts_3knobs_2hz_hybrid_optuna_r4_024, car_conflicts_3knobs_2hz_hybrid_optuna_r4_025)
- S12: 12855a41 at actor_time_shift_s 1, actor_speed_scale 1.25, ego_speed_scale 0.8: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r4_004, car_conflicts_3knobs_2hz_hybrid_optuna_r4_028)
- S13: 12855a41 at actor_time_shift_s 2, actor_speed_scale 1, ego_speed_scale 1.4: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r4_047, car_conflicts_3knobs_2hz_hybrid_optuna_r4_059, car_conflicts_3knobs_2hz_hybrid_optuna_r4_060)
- S14: 187e6244 at actor_time_shift_s 1, actor_speed_scale 0.5, ego_speed_scale 1: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r4_010, car_conflicts_3knobs_2hz_hybrid_optuna_r4_026, car_conflicts_3knobs_2hz_hybrid_optuna_r4_027)
- S15: 187e6244 at actor_time_shift_s 1.5, actor_speed_scale 1, ego_speed_scale 1.4: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r4_046_a2, car_conflicts_3knobs_2hz_hybrid_optuna_r4_056, car_conflicts_3knobs_2hz_hybrid_optuna_r4_057, car_conflicts_3knobs_2hz_hybrid_optuna_r4_058)
- S16: 19f339ba at actor_time_shift_s -1, actor_speed_scale 0.5, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r4_044)
- S17: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 0.6: 4/10 failed, rate 19%-65% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r4_002, car_conflicts_3knobs_2hz_hybrid_optuna_r4_017, car_conflicts_3knobs_2hz_hybrid_optuna_r4_018_a2, car_conflicts_3knobs_2hz_hybrid_optuna_r4_021, car_conflicts_3knobs_2hz_hybrid_optuna_r4_022, car_conflicts_3knobs_2hz_hybrid_optuna_r4_023, car_conflicts_3knobs_2hz_hybrid_optuna_r4_031, car_conflicts_3knobs_2hz_hybrid_optuna_r4_032, car_conflicts_3knobs_2hz_hybrid_optuna_r4_033, car_conflicts_3knobs_2hz_hybrid_optuna_r4_034)
- S18: 19f339ba at actor_time_shift_s 1, actor_speed_scale 1, ego_speed_scale 1.4: 6/6 failed, rate 69%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r4_043, car_conflicts_3knobs_2hz_hybrid_optuna_r4_052, car_conflicts_3knobs_2hz_hybrid_optuna_r4_053, car_conflicts_3knobs_2hz_hybrid_optuna_r4_054, car_conflicts_3knobs_2hz_hybrid_optuna_r4_055, car_conflicts_3knobs_2hz_hybrid_optuna_r4_051_a2)
- S19: 1c45ce3a at actor_time_shift_s -2, actor_speed_scale 2, ego_speed_scale 0.6: 0/4 failed, rate 0%-40% (90%) (car_conflicts_3knobs_2hz_hybrid_optuna_r4_030, car_conflicts_3knobs_2hz_hybrid_optuna_r4_035, car_conflicts_3knobs_2hz_hybrid_optuna_r4_037, car_conflicts_3knobs_2hz_hybrid_optuna_r4_036_a2)

## Not kept by the gate

- car_conflicts_3knobs_2hz_hybrid_optuna_r4_003: not kept: HALT
- car_conflicts_3knobs_2hz_hybrid_optuna_r4_009: not kept: RE-RUN
- car_conflicts_3knobs_2hz_hybrid_optuna_r4_018: not kept: RE-RUN
- car_conflicts_3knobs_2hz_hybrid_optuna_r4_019: not kept: RE-RUN
- car_conflicts_3knobs_2hz_hybrid_optuna_r4_036: not kept: RE-RUN
- car_conflicts_3knobs_2hz_hybrid_optuna_r4_045: not kept: HALT
- car_conflicts_3knobs_2hz_hybrid_optuna_r4_046: not kept: RE-RUN
- car_conflicts_3knobs_2hz_hybrid_optuna_r4_049: not kept: RE-RUN
- car_conflicts_3knobs_2hz_hybrid_optuna_r4_051: not kept: RE-RUN

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

0 of 67 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
