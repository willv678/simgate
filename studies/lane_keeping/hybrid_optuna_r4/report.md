# In straight lane-following scenes with other vehicles nearby, which combinations of sideways plan error and ego speed at hand-off make VaVAM leave its lane and hit someone or leave the road, and which 5 such cases, each on a different scene, are hardest?

Study `hybrid_optuna_r4`: 19 kept runs on 9 scenes, varying lateral_bias_m, ego_speed_scale; 1 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 5 of 5 challenging settings confirmed, after 2 rounds.

## Answer

The study found five hard cases, each on a different scene and each confirmed by repeats: S3 (+0.2 m, 1.4x), S6 (−0.2 m, 1.4x), S7 (−0.2 m, 1.2x), S8 (−0.3 m, 1.2x) and S9 (+0.2 m, 1.2x). Every repeat at these settings failed. The 90% ranges only show that each failure rate is above one half, not that it is near certain. The pattern is a small sideways error (±0.2 to 0.3 m) together with a hand-off speed of 1.2x to 1.4x. Triage puts every one of these failures on the policy, and none is flagged as a possible simulator artifact. Often the policy held a straight or drifting course while the route command or the road bent the other way. In S3, S6 and S8 the ego left its lane and hit another vehicle. In S7 and S9 it left the road with no one nearby. The study never ran these scenes without the error or at recorded speed, so it cannot say how much of each failure comes from the error, how much from the speed, and how much the scene would cause anyway. The large errors (±0.5 m) the plan meant to search first were barely tried.

## Findings

- These are the five confirmed hard cases, one per scene: +0.2 m at 1.4x, −0.2 m at 1.4x, −0.2 m at 1.2x, −0.3 m at 1.2x and +0.2 m at 1.2x. Every repeat at each setting failed, every failure was the policy's fault, and none was flagged as a possible artifact.
  - S3: 096988dd at lateral_bias_m 0.2, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (lane_keeping_hybrid_optuna_r4_005, lane_keeping_hybrid_optuna_r4_011, lane_keeping_hybrid_optuna_r4_012)
  - S6: 0cf6368d at lateral_bias_m -0.2, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (lane_keeping_hybrid_optuna_r4_004, lane_keeping_hybrid_optuna_r4_013, lane_keeping_hybrid_optuna_r4_014)
  - S7: 0dbb91dd at lateral_bias_m -0.2, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%) (lane_keeping_hybrid_optuna_r4_008, lane_keeping_hybrid_optuna_r4_015, lane_keeping_hybrid_optuna_r4_016)
  - S8: 12855a41 at lateral_bias_m -0.3, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%) (lane_keeping_hybrid_optuna_r4_002, lane_keeping_hybrid_optuna_r4_017, lane_keeping_hybrid_optuna_r4_018)
  - S9: 1b7d131a at lateral_bias_m 0.2, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%) (lane_keeping_hybrid_optuna_r4_010, lane_keeping_hybrid_optuna_r4_019, lane_keeping_hybrid_optuna_r4_020)
- At +0.2 m and 1.4x on scene 096988dd, every run had the ego swing left out of its lane on a straight highway and sideswipe the same vehicle coming up in the adjacent left lane. This matches the side of the error and is the closest match to the LSS overtaking-vehicle case.
  - S3: 096988dd at lateral_bias_m 0.2, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (lane_keeping_hybrid_optuna_r4_005, lane_keeping_hybrid_optuna_r4_011, lane_keeping_hybrid_optuna_r4_012)
- In slow, queued traffic with a LEFT command (scenes 0cf6368d and 12855a41), the ego cut toward the next lane without leaving room and hit a nearly stopped or slow vehicle at low speed. Here the ego moved toward the command, not always toward the side of the error: it went left at −0.2 m and −0.3 m, and in one run at −0.3 m it went right into the van.
  - S6: 0cf6368d at lateral_bias_m -0.2, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (lane_keeping_hybrid_optuna_r4_004, lane_keeping_hybrid_optuna_r4_013, lane_keeping_hybrid_optuna_r4_014)
  - S8: 12855a41 at lateral_bias_m -0.3, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%) (lane_keeping_hybrid_optuna_r4_002, lane_keeping_hybrid_optuna_r4_017, lane_keeping_hybrid_optuna_r4_018)
- On two scenes the failures were departures from the road with no other road user involved. At −0.2 m and 1.2x on scene 0dbb91dd the ego drifted right over the road edge, only about 0.7 m off the recorded path, while the road bent left. At +0.2 m and 1.2x on scene 1b7d131a it drifted left onto the shoulder while the route went right.
  - S7: 0dbb91dd at lateral_bias_m -0.2, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%) (lane_keeping_hybrid_optuna_r4_008, lane_keeping_hybrid_optuna_r4_015, lane_keeping_hybrid_optuna_r4_016)
  - S9: 1b7d131a at lateral_bias_m 0.2, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%) (lane_keeping_hybrid_optuna_r4_010, lane_keeping_hybrid_optuna_r4_019, lane_keeping_hybrid_optuna_r4_020)
- Four more single-run failures, including one with no sideways error (0 m at 1.4x) and one at −0.5 m and recorded speed, hint that higher speed or a large error alone may be enough. Each rests on one run, and each is flagged as a possible artifact because the ego ended more than 3.5 m off its recorded path, although triage reads all four as policy path-following errors.
  - S1: 054b5901 at lateral_bias_m 0, ego_speed_scale 1.4: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (lane_keeping_hybrid_optuna_r4_006)
  - S2: 05f35348 at lateral_bias_m -0.5, ego_speed_scale 1: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (lane_keeping_hybrid_optuna_r4_007)
  - S4: 09a95ffa at lateral_bias_m 0.2, ego_speed_scale 1.2: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (lane_keeping_hybrid_optuna_r4_009)
  - S5: 0ce6f2a3 at lateral_bias_m 0.2, ego_speed_scale 1.4: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (lane_keeping_hybrid_optuna_r4_003)
- In many failures the policy seems to ignore a turn command or a bend in the road, keeping straight or drifting while the route goes the other way. So the cause may be partly the policy's route following and not only the injected sideways error.
  - S3: 096988dd at lateral_bias_m 0.2, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (lane_keeping_hybrid_optuna_r4_005, lane_keeping_hybrid_optuna_r4_011, lane_keeping_hybrid_optuna_r4_012)
  - S5: 0ce6f2a3 at lateral_bias_m 0.2, ego_speed_scale 1.4: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (lane_keeping_hybrid_optuna_r4_003)
  - S7: 0dbb91dd at lateral_bias_m -0.2, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%) (lane_keeping_hybrid_optuna_r4_008, lane_keeping_hybrid_optuna_r4_015, lane_keeping_hybrid_optuna_r4_016)
  - S9: 1b7d131a at lateral_bias_m 0.2, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%) (lane_keeping_hybrid_optuna_r4_010, lane_keeping_hybrid_optuna_r4_019, lane_keeping_hybrid_optuna_r4_020)
  - S1: 054b5901 at lateral_bias_m 0, ego_speed_scale 1.4: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (lane_keeping_hybrid_optuna_r4_006)
  - S2: 05f35348 at lateral_bias_m -0.5, ego_speed_scale 1: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (lane_keeping_hybrid_optuna_r4_007)

## Open

- Baseline: run each of the five confirmed scenes at 0 m and 1.0x, and also at 0 m at the confirmed speed and at the confirmed error at 1.0x. This would separate the effect of the sideways error from the effect of speed and show whether these scenes fail anyway (S1 hints that 1.4x alone may be enough).
- Large errors were barely tested. The only kept run at ±0.5 m was S2 (−0.5 m, 1.0x). The run at +0.5 m and 1.2x on scene 19f339ba halted and was not kept. Run the ±0.3 to ±0.5 m corners at 1.2x to 1.4x.
- Repeat the single-run settings S1, S2, S4 and S5 to see whether their failures hold up. Each is flagged as a possible artifact because the ego ended far off its recorded path.
- Low speeds (0.6x to 0.9x) and the error sign opposite to each confirmed case were not tested, so the edges of the failing region are unknown.
- The goal was met after round 2, so about 30 runs of the budget were never used. They could cover the baselines above and the remaining scenes (023b7fcc, 187e6244, 19f339ba), which have no kept runs.
- Near misses were not ranked, and the study has no direct measure of drifting out of the lane, so departures that did not end in a crash or going off the road are not counted.
- Replayed traffic cannot react to the ego, so the side and rear contacts in queued traffic (S6, S8) may not happen among real, reactive traffic.

## Why the runs failed (triage from the video and log)

left_road 9, turned_into_actor 9, no_brake_for_lead 1

- lane_keeping_hybrid_optuna_r4_002: no_brake_for_lead, policy at fault: yes. In slow highway traffic, the ego was told to go LEFT but stayed partly in its lane, behind and slightly left of the slow grey van ahead (actor 13). Over the last 2 s the gap closed from 6.4 m to 3.9 m while the ego held about 2 m/s without braking further, and its front-right clipped the van's rear as it finally shifted left. The rear contact came only after that front collision.
- lane_keeping_hybrid_optuna_r4_003: left_road, policy at fault: yes. The route command switched to RIGHT and the route bent right, but the policy kept its trajectory straight and slightly left while slowing from 23 to 16 m/s. By 6.7 s it was 4.9 m off the recorded path and had driven onto the nose of the raised median island between the lanes. The camera view was clean beforehand, so this is a policy path-following error, not a rendering problem.
- lane_keeping_hybrid_optuna_r4_004: turned_into_actor, policy at fault: yes. With a LEFT command, the ego started a slow lane change to the left from behind car 21, into the lane where car 24 was stopped or creeping in traffic. It moved its nose into that lane without leaving room and hit car 24's rear corner with its front at about 2.7 m/s, while the gap had shrunk to about 4 m.
- lane_keeping_hybrid_optuna_r4_005: turned_into_actor, policy at fault: yes. On a straight highway (command STRAIGHT, then RIGHT), the policy's plan swung left out of the recorded lane after handoff. The ego cut into the adjacent left lane and sideswiped actor 41, which was coming up alongside from behind-left (lateral collision at 6.5 s, about 2 m off the recorded path).
- lane_keeping_hybrid_optuna_r4_006: left_road, policy at fault: yes. The command was RIGHT and the route (green) curved right toward the right-turn lanes, but the policy kept its plan (orange) straight ahead and slightly left. While slowing down behind lead vehicle 9 (which was in a lane to its right), it drifted left and left the drivable area at the nose of the left median just before the stop line, about 7.6 m from the recorded path.
- lane_keeping_hybrid_optuna_r4_007: left_road, policy at fault: yes. On a highway that bends left, the ego braked from about 29.6 to 16 m/s but kept heading straight instead of following the curve. It crossed the right edge line onto the shoulder toward the guardrail and was off the road at 7.0 s, 3.8 m from the human path, even though the route said LEFT and its planned path followed the curve.
- lane_keeping_hybrid_optuna_r4_008: left_road, policy at fault: yes. The ego was in the rightmost lane, braking gently from about 15 to 11 m/s, when the road began curving slightly left. Its planned path kept going straight and then wiggled to the right, so it drifted across the right lane edge onto the shoulder and was flagged offroad at 6.9s, about 0.7 m from the recorded human path.
- lane_keeping_hybrid_optuna_r4_009: turned_into_actor, policy at fault: yes. On a multi-lane highway, with the route command STRAIGHT and then RIGHT, the policy planned a path veering left across lanes, away from the recorded path. The ego drifted about 5 m left into the adjacent lane and struck vehicle 28 with its front at 7.2 s.
- lane_keeping_hybrid_optuna_r4_010: left_road, policy at fault: yes. The ego was in the left lane at about 28 m/s and slowing. It kept heading slightly left and crossed the yellow edge line onto the left shoulder, while the recorded human path and the RIGHT route command went to the right. There were no actors nearby and the camera view was clear, so the policy simply steered off the drivable area.
- lane_keeping_hybrid_optuna_r4_011: turned_into_actor, policy at fault: yes. On a multi-lane highway with a STRAIGHT and then RIGHT command, the policy moved left out of its lane while the recorded path stayed straight and bore slightly right. At 6.5 s it cut into the adjacent left lane and sideswiped vehicle 41, which was alongside and slightly behind it.
- lane_keeping_hybrid_optuna_r4_012: turned_into_actor, policy at fault: yes. After the 4.7 s handoff on a wet multi-lane highway, the ego left its lane and drifted left, while the recorded path stayed straight and then went right. It then side-swiped actor 41, which was traveling in the adjacent left lane just beside and behind it. The ego was going about 5.7 m/s and was 1.9 m off the human trajectory at the time of contact.
- lane_keeping_hybrid_optuna_r4_013: turned_into_actor, policy at fault: yes. In slow, dense traffic with a LEFT command, the ego (about 3 m/s) tried to merge left from the right lane toward the route lane. Its planned path cut into the side of vehicle 24, which was close ahead in the left lane, and the ego's front struck it at 7.4 s.
- lane_keeping_hybrid_optuna_r4_014: turned_into_actor, policy at fault: yes. The route command was LEFT in slow, queued traffic, and the ego's plan swung left toward the lane where car 24 sat stopped or creeping ahead. The ego kept moving at about 3 m/s as it cut across the lane line, and its front hit the rear of car 24 (the gap closed from 9 m to 4 m in the last second). The camera only breaks up at the moment of impact, and the rear contact came after the front collision.
- lane_keeping_hybrid_optuna_r4_015: left_road, policy at fault: yes. The ego was in the rightmost lane, slowing from about 15 to 11 m/s with no lead vehicle close by. The road bends gently left, but the policy's planned path stayed straight and wobbled toward the right curb instead of following the recorded path, which curved left, so the ego went over the right lane edge at 6.9s, about 0.7 m off the recorded trajectory.
- lane_keeping_hybrid_optuna_r4_016: left_road, policy at fault: yes. The ego was going straight in the rightmost lane at about 11–15 m/s and slowing as the road bent gently left. Its planned path (orange) kinked right toward the curb instead of following the lane, and the ego's right side crossed the road edge at 6.9 s. It was only about 0.7 m from the recorded human path, so this was a marginal edge violation, not a large departure.
- lane_keeping_hybrid_optuna_r4_017: turned_into_actor, policy at fault: yes. In slow highway traffic with a LEFT command, the ego steered right toward the next lane, into the silver van (actor 13) moving alongside it. Its front clipped the van at about 1.9 m/s while about 2 m off the recorded path; the rear contact came later.
- lane_keeping_hybrid_optuna_r4_018: turned_into_actor, policy at fault: yes. In slow, dense highway traffic, the ego was ordered to go LEFT and slowly pulled out from behind actor 13 toward the left lane, where the human drove. It stayed about 1.9 m right of the human's path and moved too little laterally, so its front-right corner clipped the rear-left of actor 13 at about 1.6 m/s.
- lane_keeping_hybrid_optuna_r4_019: left_road, policy at fault: yes. The command was RIGHT, and the recorded human moved over into the right lane. The ego instead slowed from about 29 to 19 m/s and drifted slightly left until it crossed the yellow left edge line onto the shoulder at 7.2 s, with no other actors nearby. The camera view was a little blurry at the left edge but the road was clear, so the policy is to blame.
- lane_keeping_hybrid_optuna_r4_020: left_road, policy at fault: yes. On a clear, straight road with no lead vehicle, the ego slowed from about 29 to 19 m/s. Meanwhile it drifted left onto and across the yellow center line, even though the command had changed to RIGHT and the recorded path angled right. It went offroad on the left side at 7.1 s, about 2 m from the human's path.

## Every setting

- S1: 054b5901 at lateral_bias_m 0, ego_speed_scale 1.4: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (lane_keeping_hybrid_optuna_r4_006)
- S2: 05f35348 at lateral_bias_m -0.5, ego_speed_scale 1: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (lane_keeping_hybrid_optuna_r4_007)
- S3: 096988dd at lateral_bias_m 0.2, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (lane_keeping_hybrid_optuna_r4_005, lane_keeping_hybrid_optuna_r4_011, lane_keeping_hybrid_optuna_r4_012)
- S4: 09a95ffa at lateral_bias_m 0.2, ego_speed_scale 1.2: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (lane_keeping_hybrid_optuna_r4_009)
- S5: 0ce6f2a3 at lateral_bias_m 0.2, ego_speed_scale 1.4: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (lane_keeping_hybrid_optuna_r4_003)
- S6: 0cf6368d at lateral_bias_m -0.2, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (lane_keeping_hybrid_optuna_r4_004, lane_keeping_hybrid_optuna_r4_013, lane_keeping_hybrid_optuna_r4_014)
- S7: 0dbb91dd at lateral_bias_m -0.2, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%) (lane_keeping_hybrid_optuna_r4_008, lane_keeping_hybrid_optuna_r4_015, lane_keeping_hybrid_optuna_r4_016)
- S8: 12855a41 at lateral_bias_m -0.3, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%) (lane_keeping_hybrid_optuna_r4_002, lane_keeping_hybrid_optuna_r4_017, lane_keeping_hybrid_optuna_r4_018)
- S9: 1b7d131a at lateral_bias_m 0.2, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%) (lane_keeping_hybrid_optuna_r4_010, lane_keeping_hybrid_optuna_r4_019, lane_keeping_hybrid_optuna_r4_020)

## Not kept by the gate

- lane_keeping_hybrid_optuna_r4_001: not kept: HALT

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
- 50 runs over 12 scenes and 45 settings is a sparse search. It may miss hard cases and cannot map the full grid.). Report written by claude-opus-5-5 from `results` in 26 s; every count above is computed from the queue, not written by the model.

0 of 20 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
