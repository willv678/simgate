# In lead-vehicle scenes, which timing shifts and speed scalings of the recorded lead car (with up to 200 ms planner delay if needed) make VaVAM run into it? Find the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `hybrid`: 49 kept runs on 8 scenes, varying actor_time_shift_s, actor_speed_scale, planner_delay_us; 1 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 4 of 5 challenging settings confirmed, after 7 rounds.

## Answer

Four of the five cases were confirmed by repeats, so the goal was not met. Every run in those four failed. Three cases slow the lead car to 0.75x: S17 on 0e899dd3, S20 on 12855a41 and S10 on 09a95ffa. The fourth speeds it up to 1.25x (S23 on 19f339ba). All four ran at the full 200 ms planner delay with no time shift. However, the triage shows that no failure in the study was VaVAM rear-ending the lead car. On 12855a41 and 09a95ffa, VaVAM caused most of the failures itself: it braked behind the lead and then steered left against the route command, side-swiping a car in the next lane. On 0e899dd3 and 19f339ba, the failures were replayed cars that do not react to the ego driving into it from behind after it slowed or crept. Triage judged the policy not at fault in every 0e899dd3 run and in at least one 19f339ba run. The fault in the others was unclear. So these settings are hard for VaVAM, but not in the way the brief asked about, and two of the four mostly measure replay traffic, not the policy.

## Findings

- On 12855a41, slowing the lead car to 0.75x at 200 ms delay failed every run. In most of these runs the policy was at fault: with a RIGHT route command, it drifted or steered left and hit car 51 passing in the left lane. These are side collisions, not rear-ends. At 1.0x and 1.25x on this scene, no run failed.
  - S20: 12855a41 at actor_time_shift_s 0, actor_speed_scale 0.75, planner_delay_us 200000: 4/4 failed, rate 60%-100% (90%) (lead_vehicle_hybrid_025, lead_vehicle_hybrid_029, lead_vehicle_hybrid_030, lead_vehicle_hybrid_031)
  - S21: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1, planner_delay_us 200000: 0/2 failed, rate 0%-58% (90%) (lead_vehicle_hybrid_018, lead_vehicle_hybrid_024)
  - S22: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.25, planner_delay_us 200000: 0/2 failed, rate 0%-58% (90%) (lead_vehicle_hybrid_003, lead_vehicle_hybrid_014)
- On 09a95ffa, slowing the lead car to 0.75x at 200 ms delay failed every run. The ego braked hard behind lead car 1 and then moved left out of its lane against the route command. Either it hit car 33 alongside (policy at fault), or car 23 sideswiped it from behind (fault unclear). At 1.0x there was one failure, which the simulator may explain: the ego was 3 to 5 m off the recorded path and was hit from behind. At 1.25x, with or without a −0.5 s shift, no run failed.
  - S10: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 0.75, planner_delay_us 200000: 3/3 failed, rate 53%-100% (90%) (lead_vehicle_hybrid_032, lead_vehicle_hybrid_033, lead_vehicle_hybrid_036)
  - S11: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1, planner_delay_us 200000: 1/3 failed, rate 8%-75% (90%), 1 possibly the simulator's (lead_vehicle_hybrid_015, lead_vehicle_hybrid_022, lead_vehicle_hybrid_023)
  - S12: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25, planner_delay_us 200000: 0/3 failed, rate 0%-47% (90%) (lead_vehicle_hybrid_006, lead_vehicle_hybrid_010, lead_vehicle_hybrid_011)
  - S9: 09a95ffa at actor_time_shift_s -0.5, actor_speed_scale 1.25, planner_delay_us 200000: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_hybrid_021)
- On 0e899dd3, the confirmed case (0.75x, 200 ms) is not a policy failure. In every run the ego crept along well behind the lead car with a clear gap ahead. Replayed car 10 then drove into it from behind and through it, which tripped the front-collision flag. Triage judged the policy not at fault in every run. At 1.0x and 1.25x, no run failed.
  - S17: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 0.75, planner_delay_us 200000: 4/4 failed, rate 60%-100% (90%) (lead_vehicle_hybrid_034, lead_vehicle_hybrid_037, lead_vehicle_hybrid_038, lead_vehicle_hybrid_039_a2)
  - S18: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1, planner_delay_us 200000: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_hybrid_027)
  - S19: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.25, planner_delay_us 200000: 0/2 failed, rate 0%-58% (90%) (lead_vehicle_hybrid_020, lead_vehicle_hybrid_026)
- On 19f339ba, speeding the lead car to 1.25x at 200 ms delay failed every run, but there was no lead-vehicle conflict. The ego slowed for no visible reason with nothing close ahead. Replayed car 28 then came up from behind on the right and merged into the ego's position. Triage judged fault unclear or not the policy's: the needless braking is the policy's part.
  - S23: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25, planner_delay_us 200000: 3/3 failed, rate 53%-100% (90%) (lead_vehicle_hybrid_002, lead_vehicle_hybrid_008, lead_vehicle_hybrid_009)
- Scene 096988dd did not fail at any setting tried: time shifts of −1.5 to 0 s, speed scales of 1.0x to 1.5x, all at 200 ms delay. It was the most heavily tested scene without a failure.
  - S3: 096988dd at actor_time_shift_s -1.5, actor_speed_scale 1.25, planner_delay_us 200000: 0/3 failed, rate 0%-47% (90%) (lead_vehicle_hybrid_046, lead_vehicle_hybrid_047, lead_vehicle_hybrid_048)
  - S4: 096988dd at actor_time_shift_s -1, actor_speed_scale 1.25, planner_delay_us 200000: 0/4 failed, rate 0%-40% (90%) (lead_vehicle_hybrid_040, lead_vehicle_hybrid_043, lead_vehicle_hybrid_044, lead_vehicle_hybrid_045)
  - S5: 096988dd at actor_time_shift_s -0.5, actor_speed_scale 1.25, planner_delay_us 200000: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_hybrid_035)
  - S6: 096988dd at actor_time_shift_s -0.5, actor_speed_scale 1.5, planner_delay_us 200000: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_hybrid_041)
  - S7: 096988dd at actor_time_shift_s 0, actor_speed_scale 1, planner_delay_us 200000: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_hybrid_016)
  - S8: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25, planner_delay_us 200000: 0/3 failed, rate 0%-47% (90%) (lead_vehicle_hybrid_004, lead_vehicle_hybrid_012, lead_vehicle_hybrid_028)
- Scene 0cf6368d (where the lead car also cuts in) did not fail at 1.0x, 1.25x or 1.5x with 200 ms delay.
  - S13: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1, planner_delay_us 200000: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_hybrid_017)
  - S14: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.25, planner_delay_us 200000: 0/3 failed, rate 0%-47% (90%) (lead_vehicle_hybrid_007, lead_vehicle_hybrid_013, lead_vehicle_hybrid_049)
  - S15: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.5, planner_delay_us 200000: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_hybrid_042)
- Scenes 023b7fcc and 0dbb91dd were barely tested. Each setting there had a single run with no failure, so this is a hint only, not evidence that they pass.
  - S1: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1, planner_delay_us 200000: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_hybrid_019)
  - S2: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1.25, planner_delay_us 200000: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_hybrid_005)
  - S16: 0dbb91dd at actor_time_shift_s 0, actor_speed_scale 1.25, planner_delay_us 200000: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_hybrid_001)

## Open

- The fifth case is missing. 0.75x is the speed scale that produced failures on three scenes, yet it was never tried on 096988dd, 0cf6368d, 023b7fcc or 0dbb91dd. Neither was 0.5x, the hardest stop allowed, on any scene. Repeated runs at 0.75x and 0.5x (200 ms) on those scenes, with 096988dd and 023b7fcc first since they had 0.0 m baseline approaches, could supply it.
- The study did not answer the question it was asked: no run showed VaVAM rear-ending the lead car. Whether any retiming within scope produces a true rear-end is still open. Slower lead speeds (0.5x) and positive time shifts (a later lead car, never tried) are the untested directions.
- Every run used the full 200 ms delay. The plan said to start at 0 delay, but no setting was run without delay. So the study cannot say whether the 0.75x failures on 12855a41 and 09a95ffa need the delay. Repeated runs of S20 and S10 at 0 delay would settle it.
- On 0e899dd3 and 19f339ba, the failures come from replayed cars that do not react to the ego hitting it from behind. Re-running S17 and S23 with reactive traffic, or retiming only the lead while excluding following cars from collision scoring, would show whether any policy failure remains. On 19f339ba it would also show whether the ego's unexplained braking is itself a problem.
- The single 1.0x failure on 09a95ffa may be the simulator's (the ego was over 3.5 m off the recorded path). More repeats would show whether 1.0x fails at all there.

## Why the runs failed (triage from the video and log)

actor_hit_ego 10, turned_into_actor 5

- lead_vehicle_hybrid_002: actor_hit_ego, policy at fault: unclear. On an open highway, with the nearest lead vehicle more than 50 m ahead, the ego kept slowing for no visible reason, from 13 to 7.8 m/s, and fell about 21 m behind where the recorded car was. Actor 28 is replayed from the recording and does not react to the ego. It came up from behind on the ego's right and moved into the ego's lane, overlapping its front-right corner at 9.0 s. A rear collision had already been flagged earlier in the run.
- lead_vehicle_hybrid_008: actor_hit_ego, policy at fault: no. On a straight highway, the ego slowed from 13 to 8 m/s with nothing close ahead and fell about 21 m behind where the recorded car was. Actor 28, a replayed vehicle that doesn't react to the ego, then came in from behind and the right and ran into the ego's spot, which the sim scores as a front/lateral hit with not-at-fault metrics and a run-level rear collision.
- lead_vehicle_hybrid_009: actor_hit_ego, policy at fault: unclear. On a clear multi-lane highway, the ego slowed steadily from 12.9 to 8.1 m/s for no visible reason and fell about 20 m behind where the real car was at that time. A replayed actor (28) coming up from the right and behind then merged into the ego's position (the gap to the actor ahead dropped from 58 m to 0.1 m) and overlapped the ego's front-right corner. The actor followed its recorded path without reacting, but the ego's needless braking is what put the two vehicles in the same place.
- lead_vehicle_hybrid_015: actor_hit_ego, policy at fault: unclear. The route command was RIGHT, but the ego had moved one lane left of the recorded path (about 3–5 m off it) and kept a steady ~7.5 m/s. Actor 33, a replayed car coming up behind in that lane, ran into the ego from behind (rear collision already showing at 8.6s) and overlapped it until a front collision registered at 10.6s; the nearest car ahead was still about 14.5 m away.
- lead_vehicle_hybrid_025: turned_into_actor, policy at fault: yes. In slow highway traffic with a RIGHT command, the recorded path moved right toward the lane with actor 5. The ego instead held a path about 1.8 m to the left, straddling the boundary with the left lane, and edged left as actor 51 came up alongside in that lane, so its front-left corner hit 51 at 10.6 s.
- lead_vehicle_hybrid_029: turned_into_actor, policy at fault: yes. The ego was in slow highway traffic at about 3–4 m/s with a RIGHT command. Instead of following the recorded path, which bears right, it held its heading and drifted left of its lane by about 1.8 m. Vehicle 51 was passing on the left, and the ego's front corner ran into its side and rear as it went by.
- lead_vehicle_hybrid_030: turned_into_actor, policy at fault: yes. In slow highway traffic (about 3–4 m/s), the ego's plan steered left, away from the recorded path, even though the route command was RIGHT. It moved into the lane on its left just as vehicle 51 was coming up alongside in that lane, and the ego's front clipped 51's right side.
- lead_vehicle_hybrid_031: actor_hit_ego, policy at fault: unclear. The route said RIGHT and the recorded human path moved right toward actor 5's lane, but the ego stayed in its own lane at about 3.7 m/s. Actor 51, replayed from the recording, came up from behind on the left and moved right into the space the human driver had left, so its rear clipped the ego's front-left corner.
- lead_vehicle_hybrid_032: turned_into_actor, policy at fault: yes. On a multi-lane highway, the ego braked hard behind lead vehicle 1 (from 7.9 to about 3.6 m/s) and then steered left into the adjacent lane, even though the route command said RIGHT. Its left side hit vehicle 33, which was coming up alongside in that lane at 7.5 s; this was a lateral collision.
- lead_vehicle_hybrid_033: actor_hit_ego, policy at fault: unclear. On a multi-lane freeway, the ego braked hard behind lead car 1 (7.9 → about 3.6 m/s with a gap of about 8 m) and drifted slightly left toward the lane the human driver moved into. That left it about 9 m behind where the human was at that moment. Car 23, replayed from the recording, came up from behind on the left and sideswiped the ego's left rear quarter (lateral collision at 7.5 s).
- lead_vehicle_hybrid_034: actor_hit_ego, policy at fault: no. The ego was creeping straight in its lane at about 2.5 m/s, roughly 15–17 m behind where the human drove, with the lead car (5) more than 20 m ahead. Actor 10, a replayed vehicle following the recorded path, came up from behind, rear-ended the ego (collision_rear at 10.5 s) and kept moving forward until it overlapped the ego's front, which is what set off the collision_front flag at 11.5 s.
- lead_vehicle_hybrid_036: turned_into_actor, policy at fault: yes. Behind lead car 1 on a multi-lane freeway, the ego slowed and then steered left out of its lane, even though the route command was STRAIGHT and then RIGHT. Its front-left corner hit actor 33, which was moving up in the left lane beside it.
- lead_vehicle_hybrid_037: actor_hit_ego, policy at fault: no. The ego was crawling straight in slow highway traffic at about 2.5 m/s, 15–18 m behind where the human drove, with the nearest lead about 19 m ahead. Actor 10, replayed from the recording and not reacting to the ego, came up from behind: it registered as a rear collision at 10.4 s and by 11.4 s had driven through the ego's box, which tripped the front-collision flag.
- lead_vehicle_hybrid_038: actor_hit_ego, policy at fault: no. The ego crept straight along its lane at about 2.5 m/s, with a clear 25 m gap ahead, and ended up 12–17 m behind where the human drove. Actor 10, replayed from the recording, came up from behind in the same lane, hit the ego's rear at 10.5 s (collision_rear) and kept driving into and through it, which set off the front-collision flag at 11.5 s.
- lead_vehicle_hybrid_039_a2: actor_hit_ego, policy at fault: no. The ego was creeping straight in slow highway traffic at about 2.5 m/s, 14–17 m behind where the human drove, with the lead vehicle about 18 m ahead and no brake needed. Actor 10 was replayed from the recording and does not react to the ego. It came up from behind, hit the ego's rear at 10.5s, then drove through it until it overlapped the ego's front at 11.5s, which triggered the front-collision flag. The ego did not hit anything itself, and the run's collision_at_fault metric is 0.

## Every setting

- S1: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1, planner_delay_us 200000: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_hybrid_019)
- S2: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1.25, planner_delay_us 200000: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_hybrid_005)
- S3: 096988dd at actor_time_shift_s -1.5, actor_speed_scale 1.25, planner_delay_us 200000: 0/3 failed, rate 0%-47% (90%) (lead_vehicle_hybrid_046, lead_vehicle_hybrid_047, lead_vehicle_hybrid_048)
- S4: 096988dd at actor_time_shift_s -1, actor_speed_scale 1.25, planner_delay_us 200000: 0/4 failed, rate 0%-40% (90%) (lead_vehicle_hybrid_040, lead_vehicle_hybrid_043, lead_vehicle_hybrid_044, lead_vehicle_hybrid_045)
- S5: 096988dd at actor_time_shift_s -0.5, actor_speed_scale 1.25, planner_delay_us 200000: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_hybrid_035)
- S6: 096988dd at actor_time_shift_s -0.5, actor_speed_scale 1.5, planner_delay_us 200000: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_hybrid_041)
- S7: 096988dd at actor_time_shift_s 0, actor_speed_scale 1, planner_delay_us 200000: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_hybrid_016)
- S8: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25, planner_delay_us 200000: 0/3 failed, rate 0%-47% (90%) (lead_vehicle_hybrid_004, lead_vehicle_hybrid_012, lead_vehicle_hybrid_028)
- S9: 09a95ffa at actor_time_shift_s -0.5, actor_speed_scale 1.25, planner_delay_us 200000: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_hybrid_021)
- S10: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 0.75, planner_delay_us 200000: 3/3 failed, rate 53%-100% (90%) (lead_vehicle_hybrid_032, lead_vehicle_hybrid_033, lead_vehicle_hybrid_036)
- S11: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1, planner_delay_us 200000: 1/3 failed, rate 8%-75% (90%), 1 possibly the simulator's (lead_vehicle_hybrid_015, lead_vehicle_hybrid_022, lead_vehicle_hybrid_023)
- S12: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25, planner_delay_us 200000: 0/3 failed, rate 0%-47% (90%) (lead_vehicle_hybrid_006, lead_vehicle_hybrid_010, lead_vehicle_hybrid_011)
- S13: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1, planner_delay_us 200000: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_hybrid_017)
- S14: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.25, planner_delay_us 200000: 0/3 failed, rate 0%-47% (90%) (lead_vehicle_hybrid_007, lead_vehicle_hybrid_013, lead_vehicle_hybrid_049)
- S15: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.5, planner_delay_us 200000: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_hybrid_042)
- S16: 0dbb91dd at actor_time_shift_s 0, actor_speed_scale 1.25, planner_delay_us 200000: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_hybrid_001)
- S17: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 0.75, planner_delay_us 200000: 4/4 failed, rate 60%-100% (90%) (lead_vehicle_hybrid_034, lead_vehicle_hybrid_037, lead_vehicle_hybrid_038, lead_vehicle_hybrid_039_a2)
- S18: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1, planner_delay_us 200000: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_hybrid_027)
- S19: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.25, planner_delay_us 200000: 0/2 failed, rate 0%-58% (90%) (lead_vehicle_hybrid_020, lead_vehicle_hybrid_026)
- S20: 12855a41 at actor_time_shift_s 0, actor_speed_scale 0.75, planner_delay_us 200000: 4/4 failed, rate 60%-100% (90%) (lead_vehicle_hybrid_025, lead_vehicle_hybrid_029, lead_vehicle_hybrid_030, lead_vehicle_hybrid_031)
- S21: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1, planner_delay_us 200000: 0/2 failed, rate 0%-58% (90%) (lead_vehicle_hybrid_018, lead_vehicle_hybrid_024)
- S22: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.25, planner_delay_us 200000: 0/2 failed, rate 0%-58% (90%) (lead_vehicle_hybrid_003, lead_vehicle_hybrid_014)
- S23: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25, planner_delay_us 200000: 3/3 failed, rate 53%-100% (90%) (lead_vehicle_hybrid_002, lead_vehicle_hybrid_008, lead_vehicle_hybrid_009)

## Not kept by the gate

- lead_vehicle_hybrid_039: not kept: RE-RUN

## Provenance

Plan: `plan.json` (rationale: Scene choice: all eight scenes are tagged lead_vehicle, have an identified lead car, did not fail in the earlier run at 0 delay, and the ego drove far enough (6 to 19 m/s, about 35 to 130 m) to actually close on the car ahead. Several already came very close (0dbb91dd 0.23 m, 19f339ba 0.03 m, 12855a41 0.08 m, 096988dd and 023b7fcc 0.0 m), so they are likely to tip into failure. I left out lead_vehicle scenes that already fail at baseline, because they cannot show that the retiming caused the failure. I also left out scenes where the ego barely moved (for example 0fa7060f, 15dd433e, 0ac02819, 10d64934) and tagged scenes with no identified lead car (166fe701, 1bccdc21, 0ce02937, 1a5da90a).

Retiming: traffic is replay, as the brief asks, so the lead car follows its recorded path while being retimed. Only the lead car is retimed in each scene (via retime_tracks), not every car. That keeps the failures about the car ahead rather than about crossing traffic being shifted. 0cf6368d's lead car is also its cut-in car, so a failure there may be a cut-in rather than a pure braking case.

Goal: top_k with k=5, one setting per scene, and each setting's failure rate surely above 0.5. This matches 'the 5 most challenging cases, each on a different scene, confirmed by repeats'. The plan is 7 rounds of 7 runs (49, close to the brief's 50 and within the 60 cap), so the proposer can screen broadly and then repeat.

Limits:
(1) Budget. Confirming a rate above 0.5 at 90% takes about 4 to 5 failures per setting, so 5 confirmed cases need roughly 25 runs or more. That leaves little room for screening, and the study may end with fewer than 5 confirmed.
(2) Failure is any front or side collision or leaving the road. The check cannot tell a rear-end from other contact, and near misses are only a soft ranking for the proposer, not part of the goal.
(3) The 200 ms delay cap is given to the proposer as an instruction. The knob itself allows up to 400 ms, so the code does not enforce the cap.
(4) Under replay the lead car never reacts to the ego, and changing its speed stretches its recorded braking profile rather than making a new braking event.). Report written by claude-opus-5-5 from `results` in 23 s; every count above is computed from the queue, not written by the model.

50 of 50 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
