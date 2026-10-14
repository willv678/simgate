# In straight lane-following scenes with other vehicles nearby, which combinations of sideways plan error and ego speed at hand-off make VaVAM leave its lane and hit someone or leave the road, and which 5 such cases, each on a different scene, are hardest?

Study `hybrid`: 50 kept runs on 10 scenes, varying lateral_bias_m, ego_speed_scale; 1 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 4 of 5 challenging settings confirmed, after 5 rounds.

## Answer

The goal was not met: four of the five scenes have a confirmed hard case and the fifth does not. In two of the four, VaVAM failed with no sideways error at all. Clip 19f339ba fails at recorded speed (S24) and clip 096988dd fails at 1.2x (S8), both by drifting left into a car in the next lane. Clip 0ce6f2a3 fails at 1.4x by running onto a median at a fork (S17). Only clip 09a95ffa needed a sideways error: it fails at +0.1 m and 1.4x but not at 0 m and 1.4x (S14 vs S13). Each of these four rests on a handful of repeats, so their failure ranges reach down only to about the low 0.5s–0.6. At S17 and S14 every failure is also flagged as a possible artifact, because the ego ended over 3.5 m from the recording. Triage blames the policy's own steering, not the rendering. The planned corners (±0.3–0.5 m, mostly at 1.2–1.4x) were never run, and negative (rightward) errors were tried only twice. So this shows which combinations break VaVAM in these scenes, not the worst ones in the grid.

## Findings

- On clip 19f339ba the policy fails with no sideways error at recorded speed: every run at 0 m / 1.0x failed. It braked hard for no reason, drifted left and its front hit the car in the adjacent left lane. The one run at 1.2x failed the same way. Speed and bias are not needed to break this scene, which goes against the plan's assumption that every chosen scene passed at baseline.
  - S24: 19f339ba at lateral_bias_m 0, ego_speed_scale 1: 3/3 failed, rate 53%-100% (90%) (lane_keeping_hybrid_004, lane_keeping_hybrid_011, lane_keeping_hybrid_012)
  - S25: 19f339ba at lateral_bias_m 0, ego_speed_scale 1.2: 1/1 failed, rate 27%-100% (90%) (lane_keeping_hybrid_013)
- On clip 096988dd every run at 0 m / 1.2x failed, and the single run at 1.4x also failed. In each, the plan bent left against a STRAIGHT/RIGHT command and the front struck a pickup passing on the left. The single run at 1.0x did not fail, which hints that speed above the recorded value triggers it.
  - S8: 096988dd at lateral_bias_m 0, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%) (lane_keeping_hybrid_018, lane_keeping_hybrid_021, lane_keeping_hybrid_022)
  - S9: 096988dd at lateral_bias_m 0, ego_speed_scale 1.4: 1/1 failed, rate 27%-100% (90%) (lane_keeping_hybrid_027)
  - S7: 096988dd at lateral_bias_m 0, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_002)
- On clip 0ce6f2a3 every run at 0 m / 1.4x left the road. The ego kept straight at a fork with a RIGHT command and ran onto the median nose. At 1.2x one run failed, and that one was a missed left curve into parked cars, a different cause. All failures at 1.4x are flagged as possible artifacts (the ego ended about 5 m off the recording), though triage says the camera was clean until the ego was on the median.
  - S17: 0ce6f2a3 at lateral_bias_m 0, ego_speed_scale 1.4: 4/4 failed, rate 60%-100% (90%), 4 possibly the simulator's (lane_keeping_hybrid_028, lane_keeping_hybrid_034, lane_keeping_hybrid_035, lane_keeping_hybrid_036)
  - S16: 0ce6f2a3 at lateral_bias_m 0, ego_speed_scale 1.2: 1/3 failed, rate 8%-75% (90%), 1 possibly the simulator's (lane_keeping_hybrid_020, lane_keeping_hybrid_023, lane_keeping_hybrid_024)
  - S15: 0ce6f2a3 at lateral_bias_m 0, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_008)
- On clip 09a95ffa a +0.1 m (leftward) error at 1.4x made every run steer left out of its lane into a vehicle in the left lane. Without the error, no run failed at 1.4x or 1.2x, so here the sideways error is what causes the failure. All of these failures are flagged as possible artifacts (the ego ended about 4.9 m off the recording).
  - S14: 09a95ffa at lateral_bias_m 0.1, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (lane_keeping_hybrid_039, lane_keeping_hybrid_041, lane_keeping_hybrid_042)
  - S13: 09a95ffa at lateral_bias_m 0, ego_speed_scale 1.4: 0/3 failed, rate 0%-47% (90%) (lane_keeping_hybrid_026, lane_keeping_hybrid_037, lane_keeping_hybrid_038)
  - S12: 09a95ffa at lateral_bias_m 0, ego_speed_scale 1.2: 0/2 failed, rate 0%-58% (90%) (lane_keeping_hybrid_017, lane_keeping_hybrid_025)
  - S10: 09a95ffa at lateral_bias_m -0.1, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_040)
- On three more scenes a leftward error of +0.1 to +0.2 m brought failures where 0 m had none, all by leaving the road to the left. But each has too few failing repeats to confirm it. Clip 023b7fcc fails more often as the error grows from 0 to +0.1 to +0.2 m. Clips 12855a41 and 1b7d131a each failed in their single run at +0.1 m / 1.0x. On 12855a41 the single run at -0.1 m did not fail.
  - S1: 023b7fcc at lateral_bias_m 0, ego_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (lane_keeping_hybrid_001, lane_keeping_hybrid_015)
  - S2: 023b7fcc at lateral_bias_m 0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_014)
  - S3: 023b7fcc at lateral_bias_m 0.1, ego_speed_scale 1: 1/4 failed, rate 6%-64% (90%), 1 possibly the simulator's (lane_keeping_hybrid_029, lane_keeping_hybrid_031, lane_keeping_hybrid_032, lane_keeping_hybrid_033_a2)
  - S4: 023b7fcc at lateral_bias_m 0.1, ego_speed_scale 1.2: 1/3 failed, rate 8%-75% (90%), 1 possibly the simulator's (lane_keeping_hybrid_046, lane_keeping_hybrid_047, lane_keeping_hybrid_048)
  - S5: 023b7fcc at lateral_bias_m 0.2, ego_speed_scale 1: 2/3 failed, rate 25%-92% (90%), 2 possibly the simulator's (lane_keeping_hybrid_043, lane_keeping_hybrid_044, lane_keeping_hybrid_045)
  - S22: 12855a41 at lateral_bias_m 0.1, ego_speed_scale 1: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (lane_keeping_hybrid_050)
  - S28: 1b7d131a at lateral_bias_m 0.1, ego_speed_scale 1: 1/1 failed, rate 27%-100% (90%) (lane_keeping_hybrid_049)
  - S19: 12855a41 at lateral_bias_m -0.1, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_030)
  - S20: 12855a41 at lateral_bias_m 0, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_003)
  - S21: 12855a41 at lateral_bias_m 0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_016)
  - S26: 1b7d131a at lateral_bias_m 0, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_009)
  - S27: 1b7d131a at lateral_bias_m 0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_019)
- Triage put every kept failure on the policy, and almost all of them are a leftward departure. Many happen where the route command turns RIGHT at a fork or split: the policy goes straight or left instead of following it. So many of these failures are failures to follow the route command more than plain lane-keeping drift. A leftward (positive) error pushes the same way the policy already drifts.
  - S5: 023b7fcc at lateral_bias_m 0.2, ego_speed_scale 1: 2/3 failed, rate 25%-92% (90%), 2 possibly the simulator's (lane_keeping_hybrid_043, lane_keeping_hybrid_044, lane_keeping_hybrid_045)
  - S14: 09a95ffa at lateral_bias_m 0.1, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (lane_keeping_hybrid_039, lane_keeping_hybrid_041, lane_keeping_hybrid_042)
  - S17: 0ce6f2a3 at lateral_bias_m 0, ego_speed_scale 1.4: 4/4 failed, rate 60%-100% (90%), 4 possibly the simulator's (lane_keeping_hybrid_028, lane_keeping_hybrid_034, lane_keeping_hybrid_035, lane_keeping_hybrid_036)
  - S22: 12855a41 at lateral_bias_m 0.1, ego_speed_scale 1: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (lane_keeping_hybrid_050)
  - S28: 1b7d131a at lateral_bias_m 0.1, ego_speed_scale 1: 1/1 failed, rate 27%-100% (90%) (lane_keeping_hybrid_049)
  - S8: 096988dd at lateral_bias_m 0, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%) (lane_keeping_hybrid_018, lane_keeping_hybrid_021, lane_keeping_hybrid_022)
  - S24: 19f339ba at lateral_bias_m 0, ego_speed_scale 1: 3/3 failed, rate 53%-100% (90%) (lane_keeping_hybrid_004, lane_keeping_hybrid_011, lane_keeping_hybrid_012)

## Open

- Fifth scene: no fourth or fifth repeat landed on a candidate. Repeats at clip 1b7d131a +0.1 m / 1.0x (S28), clip 12855a41 +0.1 m / 1.0x (S22), or clip 023b7fcc +0.2 m / 1.0x (S5) would probably settle it.
- The corners the plan targeted (±0.3 to ±0.5 m at 1.2–1.4x) were never run, so the hardest combinations in the grid are unknown.
- Rightward errors (negative bias) were tried only twice (S10, S19), so whether VaVAM fails symmetrically, or mainly drifts left, is untested.
- Clip 19f339ba fails at 0 m / 1.0x (S24), and clips 0ce6f2a3 and 096988dd fail with 0 m bias. Several failures also come from ignoring a RIGHT route command at a fork. Re-checking these scenes at baseline, and picking scenes whose route really is straight, would separate lane-keeping drift from route-command failures.
- Every failure at S17 and S14 is flagged as a possible rendering artifact. Triage says the policy drifted first, but these confirmations depend on that reading of the videos.
- Speed scales below 1.0 (0.6–0.8x) were never run, so the low-speed half of the question is open.

## Why the runs failed (triage from the video and log)

turned_into_actor 11, left_road 10, no_brake_for_lead 1

- lane_keeping_hybrid_004: turned_into_actor, policy at fault: yes. On a multi-lane highway, the ego braked hard for no reason after handoff (17 to 8 m/s, with the lead car 19–21 m ahead), falling about 7 m behind where the human drove. It then drifted left toward the adjacent lane, and its front corner struck actor 1, a replayed car that was now beside it and slightly ahead on the left (a car behind also hit the ego's rear because of the hard braking).
- lane_keeping_hybrid_011: turned_into_actor, policy at fault: yes. After the 4.6s handoff on the highway, the ego braked hard for no clear reason (17 to 8 m/s while the gap to lead car 18 kept growing) and veered left toward the adjacent lane. Its front-left hit actor 1, which was travelling beside it in that lane. The hard braking also got the ego rear-ended, but the front collision came first.
- lane_keeping_hybrid_012: turned_into_actor, policy at fault: yes. After handoff at 4.6 s on a straight multi-lane highway, the policy braked hard for no visible reason (16.9 to 8.0 m/s while the lead car stayed about 20 m ahead) and steered left into the next lane, where its front hit car 1 alongside at 6.3 s. The route command was STRAIGHT and then RIGHT, so the move left was the policy's own. The later rear contact was probably caused by the needless hard braking.
- lane_keeping_hybrid_013: turned_into_actor, policy at fault: yes. On a straight multi-lane highway, after handoff the ego braked hard from about 20 to 11.6 m/s with no close lead (gap about 19 m and growing). It also drifted about 1 m left of the recorded path, across its lane line, and side-swiped actor 1 in the adjacent left lane. The sudden braking probably also caused the rear contact, which came after the side collision.
- lane_keeping_hybrid_018: turned_into_actor, policy at fault: yes. On a multi-lane highway, the policy steered the ego left of the recorded path (orange plan bending left), drifting about 1.3 m toward the adjacent left lane while slowing from 6.8 to 4.4 m/s. A white pickup (actor 41) was passing on the left, and the ego's front-left corner struck it as it drew alongside. The recorded human stayed in its lane to the right.
- lane_keeping_hybrid_020: no_brake_for_lead, policy at fault: yes. Commanded LEFT on a left-curving road, the ego didn't follow the curve and kept going nearly straight along the right curb, 15.7 m off the human path, toward parked cars 54 and 58. It barely slowed (11.3 to 10.7 m/s) as the gap to car 54 closed from 14.8 m to 9.2 m and hit it with its front.
- lane_keeping_hybrid_021: turned_into_actor, policy at fault: yes. On a straight multi-lane highway (route command STRAIGHT, then RIGHT), the policy's planned path kept bending left out of its lane. The ego drifted left, about 1.3 m off the recorded human path, and its front hit actor 41, which was travelling alongside in the adjacent left lane.
- lane_keeping_hybrid_022: turned_into_actor, policy at fault: yes. On a multi-lane highway, the ego slowed from about 6.8 to 4.5 m/s. Its planned path then bent left even though the command was STRAIGHT and later RIGHT. The ego crossed toward the left lane line about 1.3 m left of the recorded human path, and its front clipped actor 41, which was passing on the left.
- lane_keeping_hybrid_027: turned_into_actor, policy at fault: yes. On a multi-lane highway, the ego's planned path (orange) bent left away from the route (green). The ego drifted left into the next lane and its front hit actor 41, which was driving alongside in that lane, even though the command was STRAIGHT and then RIGHT. The lead vehicle stayed 17–21 m ahead the whole time, so braking for it was not the issue.
- lane_keeping_hybrid_028: left_road, policy at fault: yes. The ego was approaching an intersection at about 17–20 m/s with a RIGHT route command and no lead vehicle. Instead of moving right with the planned path, it drifted left and ran onto the nose of the median island (a sign is right beside the car at 7.2 s), about 5 m off the recorded trajectory.
- lane_keeping_hybrid_029: left_road, policy at fault: yes. The command was RIGHT and the recorded path curved right, but the policy held a straight-to-left heading at about 5–6 m/s. It cut diagonally across the lanes, away from the recorded path, and left the drivable area at 9.7s, 13 m from where the human drove. The camera was still mostly clean at 7.7s, when the ego had already moved off the path. The heavy smearing at 8.7s and 9.7s came after the drift, as the ego got far from the recorded drive, so it doesn't explain the mistake.
- lane_keeping_hybrid_034: left_road, policy at fault: yes. The route command switched to RIGHT and the recorded path bore right into the right-hand lanes at a split. The policy kept driving straight while slowing from about 21 to 16 m/s, ran onto the nose of the raised median between the two branches and left the drivable area 4.8 m from the recorded path. No actor was ahead, and the camera view was clean until the ego was on the median.
- lane_keeping_hybrid_035: left_road, policy at fault: yes. The road splits ahead and the route command changed to RIGHT, but the ego kept going straight and drifted left at about 17 m/s. It ended up about 5 m off the human's path, on the nose of the median island by the sign, and was flagged offroad. The metrics table shows no front or side collision, only offroad; the rear contact flag is incidental.
- lane_keeping_hybrid_036: left_road, policy at fault: yes. The route command switched to RIGHT. The human driver bore right into the right-hand lanes at the fork. The ego instead held a straight path at about 17–20 m/s and ran onto the island at the split, where the camera shows a sign post right in front of it. It went off-road about 5 m from the recorded path.
- lane_keeping_hybrid_039: turned_into_actor, policy at fault: yes. The route command was RIGHT, but on a multi-lane freeway the ego steered left after handoff, crossing out of its lane, about 4.9 m off the recorded path. It moved into the next lane to the left and hit vehicle 28 there with its front at about 7 m/s.
- lane_keeping_hybrid_041: turned_into_actor, policy at fault: yes. Although the route command was RIGHT, the policy steered the ego left, out of its lane and off the recorded path (4.85 m off at impact). Moving into the left lane, its front struck vehicle 28, which was coming up alongside in that lane.
- lane_keeping_hybrid_042: turned_into_actor, policy at fault: yes. The route command was RIGHT, but after handoff the ego slowed from 11 to 7 m/s and drifted left, away from the recorded path, until it was 4.9 m off it and crossing into the lane on its left. There it hit actor 28, which was driving in that lane next to the ego's left-front corner.
- lane_keeping_hybrid_043: left_road, policy at fault: yes. With the route command RIGHT, the policy planned and drove a path curving left across several lanes, away from the recorded path that went right. It kept going at about 5–6 m/s until it left the drivable area 13 m from the recorded path, without hitting anything. The camera was only mildly smeared before the error, and it broke up badly only after the ego was far off the recording.
- lane_keeping_hybrid_045: left_road, policy at fault: yes. The route command was RIGHT and the recorded path bent right, but the policy planned and steered left across the lanes. The ego slowed to about 5 m/s and was rear-ended around 8.7 s, then kept going left until it left the drivable area at 9.7 s, about 13 m off the recorded trajectory. The rear contact did not push it off the road; its own steering did.
- lane_keeping_hybrid_048: left_road, policy at fault: yes. The command was RIGHT and the route (green line) ran off to the ego's right, but after handoff the policy angled across a multi-lane road, with its plan at 8.2s bending left away from the route. By 10.2s it had drifted 13.5 m from the recorded human path and run off the drivable area while slowly swinging back right. The camera was badly smeared, but mostly because the ego was already far from where the real car drove; the drift came first.
- lane_keeping_hybrid_049: left_road, policy at fault: yes. The route command was RIGHT, but the ego's own plan held left and drifted across the yellow edge line onto the left shoulder by the guardrail, going offroad at 11.7s at about 14 m/s. Earlier, at 10.7s, replayed actor 91 clipped the ego's rear-right while passing on the right, but that contact didn't cause the drift. The camera view was mostly clear before the departure, with the yellow line plainly visible.
- lane_keeping_hybrid_050: left_road, policy at fault: yes. On a multi-lane highway with a RIGHT route command, the policy's planned path (orange) kept drifting left of the recorded path, which bore slightly right. At about 4.5 m/s the ego crossed the leftmost lane line toward the concrete median barrier and was flagged offroad at 8.9 s, 3.7 m from the human trajectory, with no other actor involved.

## Every setting

- S1: 023b7fcc at lateral_bias_m 0, ego_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (lane_keeping_hybrid_001, lane_keeping_hybrid_015)
- S2: 023b7fcc at lateral_bias_m 0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_014)
- S3: 023b7fcc at lateral_bias_m 0.1, ego_speed_scale 1: 1/4 failed, rate 6%-64% (90%), 1 possibly the simulator's (lane_keeping_hybrid_029, lane_keeping_hybrid_031, lane_keeping_hybrid_032, lane_keeping_hybrid_033_a2)
- S4: 023b7fcc at lateral_bias_m 0.1, ego_speed_scale 1.2: 1/3 failed, rate 8%-75% (90%), 1 possibly the simulator's (lane_keeping_hybrid_046, lane_keeping_hybrid_047, lane_keeping_hybrid_048)
- S5: 023b7fcc at lateral_bias_m 0.2, ego_speed_scale 1: 2/3 failed, rate 25%-92% (90%), 2 possibly the simulator's (lane_keeping_hybrid_043, lane_keeping_hybrid_044, lane_keeping_hybrid_045)
- S6: 054b5901 at lateral_bias_m 0, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_007)
- S7: 096988dd at lateral_bias_m 0, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_002)
- S8: 096988dd at lateral_bias_m 0, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%) (lane_keeping_hybrid_018, lane_keeping_hybrid_021, lane_keeping_hybrid_022)
- S9: 096988dd at lateral_bias_m 0, ego_speed_scale 1.4: 1/1 failed, rate 27%-100% (90%) (lane_keeping_hybrid_027)
- S10: 09a95ffa at lateral_bias_m -0.1, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_040)
- S11: 09a95ffa at lateral_bias_m 0, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_010)
- S12: 09a95ffa at lateral_bias_m 0, ego_speed_scale 1.2: 0/2 failed, rate 0%-58% (90%) (lane_keeping_hybrid_017, lane_keeping_hybrid_025)
- S13: 09a95ffa at lateral_bias_m 0, ego_speed_scale 1.4: 0/3 failed, rate 0%-47% (90%) (lane_keeping_hybrid_026, lane_keeping_hybrid_037, lane_keeping_hybrid_038)
- S14: 09a95ffa at lateral_bias_m 0.1, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (lane_keeping_hybrid_039, lane_keeping_hybrid_041, lane_keeping_hybrid_042)
- S15: 0ce6f2a3 at lateral_bias_m 0, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_008)
- S16: 0ce6f2a3 at lateral_bias_m 0, ego_speed_scale 1.2: 1/3 failed, rate 8%-75% (90%), 1 possibly the simulator's (lane_keeping_hybrid_020, lane_keeping_hybrid_023, lane_keeping_hybrid_024)
- S17: 0ce6f2a3 at lateral_bias_m 0, ego_speed_scale 1.4: 4/4 failed, rate 60%-100% (90%), 4 possibly the simulator's (lane_keeping_hybrid_028, lane_keeping_hybrid_034, lane_keeping_hybrid_035, lane_keeping_hybrid_036)
- S18: 0dbb91dd at lateral_bias_m 0, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_005)
- S19: 12855a41 at lateral_bias_m -0.1, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_030)
- S20: 12855a41 at lateral_bias_m 0, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_003)
- S21: 12855a41 at lateral_bias_m 0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_016)
- S22: 12855a41 at lateral_bias_m 0.1, ego_speed_scale 1: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (lane_keeping_hybrid_050)
- S23: 187e6244 at lateral_bias_m 0, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_006)
- S24: 19f339ba at lateral_bias_m 0, ego_speed_scale 1: 3/3 failed, rate 53%-100% (90%) (lane_keeping_hybrid_004, lane_keeping_hybrid_011, lane_keeping_hybrid_012)
- S25: 19f339ba at lateral_bias_m 0, ego_speed_scale 1.2: 1/1 failed, rate 27%-100% (90%) (lane_keeping_hybrid_013)
- S26: 1b7d131a at lateral_bias_m 0, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_009)
- S27: 1b7d131a at lateral_bias_m 0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_019)
- S28: 1b7d131a at lateral_bias_m 0.1, ego_speed_scale 1: 1/1 failed, rate 27%-100% (90%) (lane_keeping_hybrid_049)

## Not kept by the gate

- lane_keeping_hybrid_033: not kept: RE-RUN

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
- 50 runs over 12 scenes and 45 settings is a sparse search. It may miss hard cases and cannot map the full grid.). Report written by claude-opus-5-5 from `results` in 42 s; every count above is computed from the queue, not written by the model.

0 of 51 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
