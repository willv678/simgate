# In straight lane-following scenes with other vehicles nearby, which combinations of sideways plan error and ego speed at hand-off make VaVAM leave its lane and hit someone or leave the road, and which 5 such cases, each on a different scene, are hardest?

Study `hybrid_optuna_r2`: 28 kept runs on 10 scenes, varying lateral_bias_m, ego_speed_scale; 2 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 5 of 5 challenging settings confirmed, after 3 rounds.

## Answer

The goal was met: five scenes each have a setting confirmed to fail more than half the time, namely S5, S7, S10, S3 and S8, and S9 also passed on a sixth scene. All of them are at high hand-off speed: 1.4x everywhere except S9 at 1.2x. Their sideways errors run from -0.5 m to +0.5 m, and in S5 there is no sideways error at all. The study did not show that the sideways error is what causes the failures. S5 fails with no shift, and in S3 and S7 the ego went left although the plan was shifted right. In most failures the policy ignored a LEFT or RIGHT route command where the road splits, bends or the traffic queues, so speed and command-following explain these failures at least as well as the plan error does. Every failure had the policy at fault and a clean camera view. The "possible artifact" flags only mark how far the ego ended up from the recording, which is the failure itself, so they do not point to the simulator.

## Findings

- Hardest case on clipgt-0ce6f2a3: every run with no sideways error at 1.4x left the road. The policy ignored a RIGHT command at a road split and went straight into the gore or median, so the sideways error played no part here.
  - S5: 0ce6f2a3 at lateral_bias_m 0, ego_speed_scale 1.4: 5/5 failed, rate 65%-100% (90%), 5 possibly the simulator's (lane_keeping_hybrid_optuna_r2_008, lane_keeping_hybrid_optuna_r2_019, lane_keeping_hybrid_optuna_r2_021, lane_keeping_hybrid_optuna_r2_022, lane_keeping_hybrid_optuna_r2_023)
- The same scene also went off the road the same way at +0.3 m and 0.8x, but from a single run. This scene's weakness looks like the split itself, whatever the speed or shift.
  - S6: 0ce6f2a3 at lateral_bias_m 0.3, ego_speed_scale 0.8: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (lane_keeping_hybrid_optuna_r2_009)
- Hardest case on clipgt-0cf6368d: every run at -0.3 m and 1.4x ended in a front collision. The ego was in slow queued traffic with a LEFT command and squeezed left between the car ahead and the car in the left lane. That is the opposite direction to the rightward shift. The car behind hit its rear only after the front collision.
  - S7: 0cf6368d at lateral_bias_m -0.3, ego_speed_scale 1.4: 5/5 failed, rate 65%-100% (90%), 5 possibly the simulator's (lane_keeping_hybrid_optuna_r2_002, lane_keeping_hybrid_optuna_r2_020, lane_keeping_hybrid_optuna_r2_024, lane_keeping_hybrid_optuna_r2_025, lane_keeping_hybrid_optuna_r2_026)
- Hardest case on clipgt-19f339ba: every run at -0.5 m and 1.4x had the ego brake hard and drift right, against a LEFT command, into a semi truck passing in the right lane. This is the clearest case where the drift goes the same way as the shift.
  - S10: 19f339ba at lateral_bias_m -0.5, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (lane_keeping_hybrid_optuna_r2_006, lane_keeping_hybrid_optuna_r2_013, lane_keeping_hybrid_optuna_r2_014)
- Hardest case on clipgt-05f35348: every run at -0.3 m and 1.4x ended with the ego, at highway speed, edging left along the recorded human's lane-change path and clipping an SUV in the left lane. At 1.4x the ego was well ahead of where the human was, so the higher speed put it alongside the SUV. The plan shift was to the right.
  - S3: 05f35348 at lateral_bias_m -0.3, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (lane_keeping_hybrid_optuna_r2_003, lane_keeping_hybrid_optuna_r2_011, lane_keeping_hybrid_optuna_r2_012)
- Hardest case on clipgt-0dbb91dd: every run at +0.3 m and 1.4x had the ego steer left against a RIGHT command. It either hit a vehicle in the left lane or crossed the left road edge, which matches the leftward shift.
  - S8: 0dbb91dd at lateral_bias_m 0.3, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (lane_keeping_hybrid_optuna_r2_004, lane_keeping_hybrid_optuna_r2_017, lane_keeping_hybrid_optuna_r2_018)
- A sixth scene, clipgt-187e6244, also met the confirmation bar at +0.5 m and 1.2x. Every run there steered left, against a RIGHT command, into the median guardrail with no actor involved.
  - S9: 187e6244 at lateral_bias_m 0.5, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (lane_keeping_hybrid_optuna_r2_001, lane_keeping_hybrid_optuna_r2_015, lane_keeping_hybrid_optuna_r2_016)
- Single runs gave mixed results. A +0.3 m, 1.2x run on clipgt-1b7d131a drifted left off the road on an empty road. Single runs at -0.2 m/1.4x and -0.3 m/1.2x on two other scenes did not fail, and two runs at -0.5 m/0.6x did not fail either. These are hints, not rates.
  - S11: 1b7d131a at lateral_bias_m 0.3, ego_speed_scale 1.2: 1/1 failed, rate 27%-100% (90%) (lane_keeping_hybrid_optuna_r2_029)
  - S1: 023b7fcc at lateral_bias_m -0.2, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_optuna_r2_007)
  - S2: 054b5901 at lateral_bias_m -0.3, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_optuna_r2_030)
  - S4: 096988dd at lateral_bias_m -0.5, ego_speed_scale 0.6: 0/2 failed, rate 0%-58% (90%) (lane_keeping_hybrid_optuna_r2_010, lane_keeping_hybrid_optuna_r2_027)
- No failure here is attributed to the simulator. Triage found the policy at fault in every failed run and the camera view clean before each failure. The many 'possible artifact' flags come from the ego ending up more than 3.5 m off the recorded path, which is part of how it failed.
  - S5: 0ce6f2a3 at lateral_bias_m 0, ego_speed_scale 1.4: 5/5 failed, rate 65%-100% (90%), 5 possibly the simulator's (lane_keeping_hybrid_optuna_r2_008, lane_keeping_hybrid_optuna_r2_019, lane_keeping_hybrid_optuna_r2_021, lane_keeping_hybrid_optuna_r2_022, lane_keeping_hybrid_optuna_r2_023)
  - S7: 0cf6368d at lateral_bias_m -0.3, ego_speed_scale 1.4: 5/5 failed, rate 65%-100% (90%), 5 possibly the simulator's (lane_keeping_hybrid_optuna_r2_002, lane_keeping_hybrid_optuna_r2_020, lane_keeping_hybrid_optuna_r2_024, lane_keeping_hybrid_optuna_r2_025, lane_keeping_hybrid_optuna_r2_026)
  - S8: 0dbb91dd at lateral_bias_m 0.3, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (lane_keeping_hybrid_optuna_r2_004, lane_keeping_hybrid_optuna_r2_017, lane_keeping_hybrid_optuna_r2_018)
  - S9: 187e6244 at lateral_bias_m 0.5, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (lane_keeping_hybrid_optuna_r2_001, lane_keeping_hybrid_optuna_r2_015, lane_keeping_hybrid_optuna_r2_016)
  - S10: 19f339ba at lateral_bias_m -0.5, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (lane_keeping_hybrid_optuna_r2_006, lane_keeping_hybrid_optuna_r2_013, lane_keeping_hybrid_optuna_r2_014)

## Open

- The study ran no baselines: no confirmed setting has a matching run with no sideways error at the same speed, or at 1.0x with the same shift. The sideways error and the speed cannot be told apart. To settle it, rerun S3, S7, S8, S9 and S10 with 0 m at the same speed, and with the same shift at 1.0x, about 3 runs each.
- Many of these 'no turn' scenes contain LEFT/RIGHT route commands, splits or merges, and most failures are the policy ignoring the command. Whether the sideways error matters on truly straight roads needs scenes with no command change, or a check of the command timeline before choosing scenes.
- At 1.4x the ego starts behind its recorded start and pulls ahead of the replayed traffic, as in S3. Some collisions may come from that timing mismatch rather than from lane keeping, and replayed traffic cannot react.
- Only one run each at S1, S2, S6 and S11, and two at S4. Low speeds (0.6x to 0.8x) and most of the bias × speed grid are barely sampled, so how far the failure region extends is unknown.
- Near misses were not ranked, because every confirmed case failed outright. Closest approach in the passing runs (S1, S2, S4) was not analysed.
- Two runs (+0.5 m, 1.4x on clipgt-19f339ba and clipgt-096988dd) halted and were not kept. That corner is untested on those scenes.

## Why the runs failed (triage from the video and log)

left_road 12, turned_into_actor 11, no_brake_for_lead 1

- lane_keeping_hybrid_optuna_r2_001: left_road, policy at fault: yes. After taking over at 4.7 s, the policy left the recorded path, which kept to its lane and bent right. Instead it steered steadily left across the leftmost lane and the shoulder line, and drove into the median guardrail at about 5 m/s by 8.0 s, even though the route command was RIGHT. The camera view was clean while it drifted. No actor was involved: the flagged contact is with the barrier, since all the actor-collision metrics read 0.
- lane_keeping_hybrid_optuna_r2_002: no_brake_for_lead, policy at fault: yes. The route said LEFT, and the ego crept forward in a stopped queue while edging left toward the gap between actor 21 (directly ahead) and actor 24 (in the left lane). It closed the gap from 10 m to 4.5 m at about 3 m/s and barely slowed, then hit 21's rear-left with its front. The lead car stayed clearly visible in the camera even as the rendering smeared, so the rear contact from 23 came after the front hit, which was the policy's fault.
- lane_keeping_hybrid_optuna_r2_003: turned_into_actor, policy at fault: yes. On the highway at about 41 m/s with a STRAIGHT command, the ego drifted left onto the lane line, toward where the recorded human changed lanes. It was still closing on the white SUV (actor 5) in the left lane, and its front clipped that SUV's rear corner at 6.9 s. The run was also flagged offroad and rear-ended; the rear contact likely came from a replayed actor, after the frontal collision had already begun.
- lane_keeping_hybrid_optuna_r2_004: left_road, policy at fault: yes. With a RIGHT command, the ego ended up in the leftmost lane, about 10 m left of the recorded path, which heads right. It slowed from 7.8 to 2.2 m/s but kept angling left toward the strip-mall side and crossed the left road edge at 11.2 s. The camera smearing comes from being so far off the recording; it is not a clear cause, since the ego was already off course in the first frame.
- lane_keeping_hybrid_optuna_r2_006: turned_into_actor, policy at fault: yes. After handoff on a multi-lane highway, the ego braked hard for no clear reason (21 → 8 m/s), while the recorded human kept speed and moved left. The ego's plan also drifted right, against a LEFT command, into the lane of semi truck 5, which was passing on its right; the ego's front corner hit the truck's side or rear (front collision at 8.0 s, 4.7 m off the recorded path).
- lane_keeping_hybrid_optuna_r2_008: left_road, policy at fault: yes. The route command switched from STRAIGHT to RIGHT, and the route bent toward a right-turn lane. The ego slowed from about 24 to 16 m/s but kept heading straight instead of following it, and at 7.2 s it ran into the non-drivable gore area between the through lanes and the right-turn lane, about 5 m off the recorded path. No other actor was close, and the camera view was clean before the failure.
- lane_keeping_hybrid_optuna_r2_009: left_road, policy at fault: yes. The command switched to RIGHT, and the recorded path bears right where the road splits around a median island. The ego instead held a slightly left-of-centre line and steered into the curbed median gore, going off-road at 7.0 s at about 12 m/s, 4.1 m from the recorded path. No other actors were close, and the camera view was clean before the failure.
- lane_keeping_hybrid_optuna_r2_011: turned_into_actor, policy at fault: yes. The ego stayed at about 41 m/s on the highway, running about 27 m ahead of where the human was at that point in the recording. It then edged left along the human's lane-change path toward the left lane and struck the white SUV (actor 5) in that lane with its front, swerving back right only at the last moment. The flagged off-road and rear contact came after this front collision.
- lane_keeping_hybrid_optuna_r2_012: turned_into_actor, policy at fault: yes. On the highway at about 41 m/s, the ego drifted left out of its lane and into the lane of slower actor 5, never slowing down, and its front hit that car's rear right corner at 6.9s. The recorded human made a similar move left but was about 27 m further back, so it was behind actor 5. The ego was ahead of that position, and its planned path only swung back right at the moment of impact.
- lane_keeping_hybrid_optuna_r2_013: turned_into_actor, policy at fault: yes. On a multi-lane highway that bends left, the ego braked hard (from 19.6 to 7.7 m/s) and kept heading straight instead of following the lanes. That put it across the right lane line into the lane of semi truck 5, which was passing on the right, and the ego's front struck the truck's side about 4.8 m right of the recorded human path, even though the route command was LEFT. The camera smear at impact is just the truck being too close to render; earlier frames were clean.
- lane_keeping_hybrid_optuna_r2_014: turned_into_actor, policy at fault: yes. After handoff the ego braked hard (20 → 8 m/s) and steered right toward the slower semi-truck (actor 5) in the next lane, even though the recorded human path and the LEFT command both went left. The ego's front ran into the rear-left of the truck as it merged into that lane.
- lane_keeping_hybrid_optuna_r2_015: left_road, policy at fault: yes. The route said RIGHT and the recorded path went ahead and to the right. Instead, the policy steered left at about 6 m/s, out of its lane and across the leftmost lane, and ran off the drivable area into the median guardrail. It ended about 7 m from the human's path. The camera view was clean before the drift, and there was no vehicle in the ego's way.
- lane_keeping_hybrid_optuna_r2_016: left_road, policy at fault: yes. The ego was on a freeway with a RIGHT command. Its planned path curved left across the yellow edge line into the left shoulder, where it ended up against the median guardrail. By 7.9 s it was off the road, about 7 m from the human's trajectory. The camera view was clean before it drifted and there was no actor in its way.
- lane_keeping_hybrid_optuna_r2_017: turned_into_actor, policy at fault: yes. The route command was RIGHT and the route line pulled right, but after handoff the ego braked and steered left across the lanes. Its front hit vehicle 32, which was in the lane to its left, and it ended up heading toward the left road edge, about 7.3 m off the recorded human path.
- lane_keeping_hybrid_optuna_r2_018: left_road, policy at fault: yes. With a RIGHT route command, the ego was already in the leftmost lane about 10 m left of the recorded path, and it planned and steered further left. Slowing from 8 to 2 m/s, it crossed the left road boundary toward the parking lot and went offroad at 11.2s, with no other actor involved.
- lane_keeping_hybrid_optuna_r2_019: left_road, policy at fault: yes. The command changed to RIGHT, but the policy ignored it and kept a straight, slightly left path while slowing from about 23 to 16 m/s. The ego drifted left away from the recorded right-hand path (5 m off) and ran onto the nose of the median island, hitting the median sign, so it was flagged offroad.
- lane_keeping_hybrid_optuna_r2_020: turned_into_actor, policy at fault: yes. In slow queued traffic with a LEFT route command, the ego steered left out of its lane, about 5 m off the recorded path, and tried to squeeze between car 21 ahead and car 24 in the left lane. Its front corner hit car 24 at about 2.7 m/s. Car 23 struck the ego's rear only after this.
- lane_keeping_hybrid_optuna_r2_021: left_road, policy at fault: yes. After the route command switched to RIGHT, the policy kept planning and driving straight instead of bearing right with the route. The ego drifted about 5 m left of the recorded path into the median and U-turn lane area and went off the road at 16.4 m/s. There was no vehicle ahead and the camera view was clean before the failure.
- lane_keeping_hybrid_optuna_r2_022: left_road, policy at fault: yes. The command changed to RIGHT as the ego approached an intersection, but it kept going straight and drifted left at about 16–18 m/s. It ended up on the median nose between the through and U-turn lanes, 4.9 m from where the human drove, who bore right. No other actors were nearby and the camera view was clean.
- lane_keeping_hybrid_optuna_r2_023: left_road, policy at fault: yes. The route command changed to RIGHT and the recorded path bore right at the road split, but the policy kept going straight, slowing from about 21 to 17 m/s. It ended up about 5 m from the recorded path, out of the drivable lanes in the gore/median area of the split. There was no actor ahead, and the camera view was clean before the failure.
- lane_keeping_hybrid_optuna_r2_024: turned_into_actor, policy at fault: yes. In slow queued traffic with a LEFT command, the ego left its lane behind actor 21 and squeezed left toward the next lane while still creeping forward at about 3 m/s. Its front hit the car stopped in that lane (actor 24, at the edge of 21), and the gap fell from 11.7 m to 4.6 m. The rear contact from actor 23 came after the front collision.
- lane_keeping_hybrid_optuna_r2_025: turned_into_actor, policy at fault: yes. In slow traffic with a LEFT command, the ego left the recorded path (about 5 m off by the end) and tried to squeeze left out of its lane into the narrow gap between car 24 on its left and car 21 just ahead. It kept rolling at about 2.5–3 m/s while the gap to the nearly stopped car ahead shrank from 11 m to 4.4 m, and its front hit one of those cars (most likely 21). Car 23 behind then touched its rear, but only after the front collision.
- lane_keeping_hybrid_optuna_r2_026: turned_into_actor, policy at fault: yes. In slow queued traffic with a LEFT command, the ego left its lane behind car 21 and edged left toward the next lane, where car 24 was alongside. Moving at about 2.4 m/s and about 5 m off the recorded path, it made front contact between cars 24 and 21 while merging. Something hit its rear afterwards, but the front collision came first.
- lane_keeping_hybrid_optuna_r2_029: left_road, policy at fault: yes. On a clear, empty road at about 28 m/s, the ego slowed and drifted left instead of following the route right (the command changed to RIGHT and the recorded path bears right). By 7.0 s it was over the yellow edge line on the left and was flagged offroad, 2.1 m from the recorded path.

## Every setting

- S1: 023b7fcc at lateral_bias_m -0.2, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_optuna_r2_007)
- S2: 054b5901 at lateral_bias_m -0.3, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_optuna_r2_030)
- S3: 05f35348 at lateral_bias_m -0.3, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (lane_keeping_hybrid_optuna_r2_003, lane_keeping_hybrid_optuna_r2_011, lane_keeping_hybrid_optuna_r2_012)
- S4: 096988dd at lateral_bias_m -0.5, ego_speed_scale 0.6: 0/2 failed, rate 0%-58% (90%) (lane_keeping_hybrid_optuna_r2_010, lane_keeping_hybrid_optuna_r2_027)
- S5: 0ce6f2a3 at lateral_bias_m 0, ego_speed_scale 1.4: 5/5 failed, rate 65%-100% (90%), 5 possibly the simulator's (lane_keeping_hybrid_optuna_r2_008, lane_keeping_hybrid_optuna_r2_019, lane_keeping_hybrid_optuna_r2_021, lane_keeping_hybrid_optuna_r2_022, lane_keeping_hybrid_optuna_r2_023)
- S6: 0ce6f2a3 at lateral_bias_m 0.3, ego_speed_scale 0.8: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (lane_keeping_hybrid_optuna_r2_009)
- S7: 0cf6368d at lateral_bias_m -0.3, ego_speed_scale 1.4: 5/5 failed, rate 65%-100% (90%), 5 possibly the simulator's (lane_keeping_hybrid_optuna_r2_002, lane_keeping_hybrid_optuna_r2_020, lane_keeping_hybrid_optuna_r2_024, lane_keeping_hybrid_optuna_r2_025, lane_keeping_hybrid_optuna_r2_026)
- S8: 0dbb91dd at lateral_bias_m 0.3, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (lane_keeping_hybrid_optuna_r2_004, lane_keeping_hybrid_optuna_r2_017, lane_keeping_hybrid_optuna_r2_018)
- S9: 187e6244 at lateral_bias_m 0.5, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (lane_keeping_hybrid_optuna_r2_001, lane_keeping_hybrid_optuna_r2_015, lane_keeping_hybrid_optuna_r2_016)
- S10: 19f339ba at lateral_bias_m -0.5, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (lane_keeping_hybrid_optuna_r2_006, lane_keeping_hybrid_optuna_r2_013, lane_keeping_hybrid_optuna_r2_014)
- S11: 1b7d131a at lateral_bias_m 0.3, ego_speed_scale 1.2: 1/1 failed, rate 27%-100% (90%) (lane_keeping_hybrid_optuna_r2_029)

## Not kept by the gate

- lane_keeping_hybrid_optuna_r2_005: not kept: HALT
- lane_keeping_hybrid_optuna_r2_028: not kept: HALT

## Provenance

Plan: `plan.json` (rationale: **Scenes.** All 12 scenes have recorded turn "none" and passed at 0 delay, so any failure can be attributed to the bias and speed settings. Each is tagged lead_vehicle and/or merge_cut_in, which means a vehicle ahead or alongside. Each also had the ego actually driving (roughly 35 to 250 m, up to 6 to 30 m/s). Most came within about 1.3 m of another actor, so a sideways shift has someone to meet.

**Scenes left out:**
- scenes that already failed at 0 delay
- scenes that turn
- scenes where the ego barely moved (a few metres)
- scenes tagged mainly pedestrian_crossing

**Fixed settings.**
- Traffic is replayed as recorded, so the other actors follow their recorded tracks, like the scripted vehicles in Euro NCAP LSS. No actor knob is varied, so no retime_class is set.
- Planner delay stays at 0 and waypoint noise at 0, the defaults.

**Budget and goal.** Budget is 5 rounds × 10 runs = 50, as the brief asks. The goal is top_k with k=5, distinct scenes and high_min 0.5. It stops early once 5 scenes each have a setting whose 90% range lies above 0.5, which takes about 3 to 5 failing repeats per setting. That leaves roughly half the budget for searching the 9 bias × 5 speed grid.

**What this plan cannot answer:**
- The tags cannot tell whether a vehicle is in an adjacent, oncoming or overtaking lane, or ahead in the ego's own lane. So the LSS oncoming and overtaking cases cannot be chosen on purpose, only found if they happen.
- There is no separate lane-departure measure. Drifting out of the lane only counts when it ends in a collision or going off the road.
- Near misses are not part of the stopping goal. They can only be ranked from the reported closest approach.
- With speed scales above 1, the ego starts behind its recorded start, off the recording for the first second or two of the warm-up.
- Replayed traffic cannot react to the ego. Rear-end hits are excluded, so a slow ego (0.6x) may look safer than it would among reactive traffic.
- 50 runs over 12 scenes and 45 settings is a sparse search. It may miss hard cases and cannot map the full grid.). Report written by claude-opus-5-5 from `results` in 31 s; every count above is computed from the queue, not written by the model.

0 of 30 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
