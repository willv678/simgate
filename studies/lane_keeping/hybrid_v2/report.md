# In straight lane-following scenes with other vehicles nearby, which combinations of sideways plan error and ego speed at hand-off make VaVAM leave its lane and hit someone or leave the road, and which 5 such cases, each on a different scene, are hardest?

Study `hybrid_v2`: 49 kept runs on 10 scenes, varying lateral_bias_m, ego_speed_scale; 1 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 5 of 5 challenging settings confirmed, after 5 rounds.

## Answer

The goal was met: five settings on five different scenes failed on every repeat (S9, S12, S17, S24, S30). However, they mostly show VaVAM drifting out of its lane at small or zero perturbation, not failures caused by the bias and speed knobs. Two of the five (S9, S24) fail with no bias at recorded speed. Of the other three, S17 adds only speed (1.4x), and S12 and S30 add only +0.1 m of bias (at 1.0x and 1.2x). The planned corners (±0.3 to ±0.5 m at 1.2 to 1.4x) were never run, so the study does not show how larger perception errors behave. With three runs per setting, each confirmed range only just clears 0.5, and the true rates could be anywhere from about half to always. All of S9 and S12's failures, and part of S17's, need caveats. In S9 and S12 every failure ended more than 3.5 m from the recorded path, so the rendering could play a part, although triage blamed the policy each time. One of S17's three failures involved a pedestrian, and fault there is unclear.

## Findings

- On scene 19f339ba the policy fails even with no bias at recorded speed. Every run braked hard for no clear reason and steered left into a vehicle alongside. Triage blamed the policy, and none of the failures may be a rendering artifact. A single run at 1.2x also failed the same way.
  - S24: 19f339ba at lateral_bias_m 0, ego_speed_scale 1: 3/3 failed, rate 53%-100% (90%) (lane_keeping_hybrid_v2_003, lane_keeping_hybrid_v2_011, lane_keeping_hybrid_v2_012)
  - S25: 19f339ba at lateral_bias_m 0, ego_speed_scale 1.2: 1/1 failed, rate 27%-100% (90%) (lane_keeping_hybrid_v2_019)
- On scene 05f35348 every run at zero bias and recorded speed braked hard, drifted left against a RIGHT or STRAIGHT command, and left the road onto the median shoulder. Every failure ended more than 3.5 m off the recorded path, so the rendering may have played a part, though triage put each on the policy.
  - S9: 05f35348 at lateral_bias_m 0, ego_speed_scale 1: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (lane_keeping_hybrid_v2_006, lane_keeping_hybrid_v2_013, lane_keeping_hybrid_v2_014)
- On scene 09a95ffa a +0.1 m bias at recorded speed failed on every repeat. The ego drifted left across lanes against a RIGHT command and cut into a vehicle passing on the left. A single run at +0.2 m failed the same way, while single runs at zero bias passed. Every one of these failures was more than 3.5 m off the recorded path (possible artifact).
  - S12: 09a95ffa at lateral_bias_m 0.1, ego_speed_scale 1: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (lane_keeping_hybrid_v2_018, lane_keeping_hybrid_v2_021, lane_keeping_hybrid_v2_022)
  - S13: 09a95ffa at lateral_bias_m 0.2, ego_speed_scale 1: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (lane_keeping_hybrid_v2_023)
  - S10: 09a95ffa at lateral_bias_m 0, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_v2_008)
  - S11: 09a95ffa at lateral_bias_m 0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_v2_017)
- On scene 1b7d131a a +0.1 m bias at 1.2x failed on every repeat. The ego held a straight, slightly left heading on a right-bending road, crossed the centre line and left the road toward the guardrail. No artifacts were flagged. Single runs with only the bias or only the speed passed, as did 1.4x with no bias, which hints that the two combine on this scene.
  - S30: 1b7d131a at lateral_bias_m 0.1, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%) (lane_keeping_hybrid_v2_041, lane_keeping_hybrid_v2_042, lane_keeping_hybrid_v2_043)
  - S29: 1b7d131a at lateral_bias_m 0.1, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_v2_029)
  - S27: 1b7d131a at lateral_bias_m 0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_v2_028)
  - S28: 1b7d131a at lateral_bias_m 0, ego_speed_scale 1.4: 0/2 failed, rate 0%-58% (90%) (lane_keeping_hybrid_v2_033, lane_keeping_hybrid_v2_034)
  - S26: 1b7d131a at lateral_bias_m 0, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_v2_007)
- On scene 0cf6368d speed alone (1.4x, no bias) failed on every repeat in queued traffic. In two runs the ego drifted right and clipped a queued car at walking pace. The third was a front contact with a replayed pedestrian, and fault there is unclear. Single runs at 1.0x and 1.2x passed.
  - S17: 0cf6368d at lateral_bias_m 0, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (lane_keeping_hybrid_v2_026, lane_keeping_hybrid_v2_031, lane_keeping_hybrid_v2_032)
  - S15: 0cf6368d at lateral_bias_m 0, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_v2_001)
  - S16: 0cf6368d at lateral_bias_m 0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_v2_020)
  - S18: 0cf6368d at lateral_bias_m 0.1, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_v2_027)
- On scene 12855a41 a +0.1 m bias at 1.2x failed in both kept runs: the ego drifted left off the road toward the median. Both failures may be artifacts, and two runs fall short of confirmation. Settings with no bias up to 1.4x did not fail.
  - S23: 12855a41 at lateral_bias_m 0.1, ego_speed_scale 1.2: 2/2 failed, rate 42%-100% (90%), 2 possibly the simulator's (lane_keeping_hybrid_v2_045, lane_keeping_hybrid_v2_046)
  - S20: 12855a41 at lateral_bias_m 0, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_v2_002)
  - S21: 12855a41 at lateral_bias_m 0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_v2_030)
  - S22: 12855a41 at lateral_bias_m 0, ego_speed_scale 1.4: 0/2 failed, rate 0%-58% (90%) (lane_keeping_hybrid_v2_035, lane_keeping_hybrid_v2_036)
- Scene 023b7fcc did not fail at any setting tried (biases of -0.1, 0 and +0.1 m at speeds of 1.0x to 1.4x), but these settings came close (high criticality). It is the strongest near-miss scene.
  - S1: 023b7fcc at lateral_bias_m -0.1, ego_speed_scale 1: 0/3 failed, rate 0%-47% (90%) (lane_keeping_hybrid_v2_047, lane_keeping_hybrid_v2_048, lane_keeping_hybrid_v2_049)
  - S2: 023b7fcc at lateral_bias_m -0.1, ego_speed_scale 1.2: 0/2 failed, rate 0%-58% (90%) (lane_keeping_hybrid_v2_039, lane_keeping_hybrid_v2_040)
  - S3: 023b7fcc at lateral_bias_m 0, ego_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (lane_keeping_hybrid_v2_009, lane_keeping_hybrid_v2_050)
  - S4: 023b7fcc at lateral_bias_m 0, ego_speed_scale 1.2: 0/3 failed, rate 0%-47% (90%) (lane_keeping_hybrid_v2_015, lane_keeping_hybrid_v2_037, lane_keeping_hybrid_v2_038)
  - S5: 023b7fcc at lateral_bias_m 0, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_v2_024)
  - S6: 023b7fcc at lateral_bias_m 0.1, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_v2_016)
  - S7: 023b7fcc at lateral_bias_m 0.1, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_v2_025)
- Across scenes the failures share one pattern. The policy drifts left, often while braking hard for no reason and ignoring a RIGHT route command, and ends up either in the adjacent lane's traffic or off the left edge. Speed-only failures in queued traffic were the exception: there the drift went right.
  - S9: 05f35348 at lateral_bias_m 0, ego_speed_scale 1: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (lane_keeping_hybrid_v2_006, lane_keeping_hybrid_v2_013, lane_keeping_hybrid_v2_014)
  - S12: 09a95ffa at lateral_bias_m 0.1, ego_speed_scale 1: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (lane_keeping_hybrid_v2_018, lane_keeping_hybrid_v2_021, lane_keeping_hybrid_v2_022)
  - S24: 19f339ba at lateral_bias_m 0, ego_speed_scale 1: 3/3 failed, rate 53%-100% (90%) (lane_keeping_hybrid_v2_003, lane_keeping_hybrid_v2_011, lane_keeping_hybrid_v2_012)
  - S30: 1b7d131a at lateral_bias_m 0.1, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%) (lane_keeping_hybrid_v2_041, lane_keeping_hybrid_v2_042, lane_keeping_hybrid_v2_043)
  - S23: 12855a41 at lateral_bias_m 0.1, ego_speed_scale 1.2: 2/2 failed, rate 42%-100% (90%), 2 possibly the simulator's (lane_keeping_hybrid_v2_045, lane_keeping_hybrid_v2_046)
  - S17: 0cf6368d at lateral_bias_m 0, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (lane_keeping_hybrid_v2_026, lane_keeping_hybrid_v2_031, lane_keeping_hybrid_v2_032)

## Open

- Large biases (±0.3 to ±0.5 m), any bias below -0.1 m, and speeds below 1.0x were never run. Running the planned corner settings on the confirmed scenes would show how failure grows with bias and speed.
- On scenes 05f35348 and 19f339ba the policy fails with no perturbation, even though these scenes were screened as passing. Repeat nominal runs there to check whether the screening pass was luck, and treat these scenes as baseline failures rather than bias or speed cases.
- Zero bias at recorded speed was run only once on scenes 09a95ffa, 1b7d131a and 0cf6368d. Two or three more nominal runs on each would show whether the +0.1 m bias or the higher speed is actually needed.
- S23 (scene 12855a41, +0.1 m, 1.2x) has two failures; one run there was not kept (HALT) and is not evidence. One or two more repeats would confirm it as a sixth case.
- All failures in S9, S12 and S23 ended more than 3.5 m off the recorded trajectory. Reviewing the frames for rendering problems, or rerunning with a shorter horizon, would show whether these failures hold.
- One of S17's failures was a front contact with a replayed pedestrian, and fault there is unclear. Another repeat at 1.4x would show whether the lane-drift contacts alone confirm this setting.
- Scenes 054b5901, 0ce6f2a3 and 0dbb91dd got only a single nominal run, so their response to bias and speed is unknown.

## Why the runs failed (triage from the video and log)

turned_into_actor 10, left_road 8, other 1

- lane_keeping_hybrid_v2_003: turned_into_actor, policy at fault: yes. After the 4.6 s handoff, the ego was driving straight on a multi-lane highway. It braked hard for no clear reason, dropping from about 16 to 8 m/s, and swerved left into the next lane. Its front hit actor 1, which was driving alongside in that lane; the hard braking also likely caused the rear contact.
- lane_keeping_hybrid_v2_006: left_road, policy at fault: yes. The route said RIGHT and the human driver moved to the right lanes. After handoff, the ego instead drifted left across its lane and braked hard on the highway, slowing from 25.7 to 12.8 m/s, which probably caused the rear-end contact. By 8.2 s it had crossed the left edge line onto the shoulder by the median, 5.1 m from the recorded path.
- lane_keeping_hybrid_v2_011: turned_into_actor, policy at fault: yes. After handoff at 4.6 s on a straight multi-lane highway, the ego braked hard for no clear reason (17 → 8 m/s while the lead car stayed about 20 m ahead) and steered left into the next lane. Its front hit actor 1, which had been travelling alongside in that lane and was now just ahead. The rear-end contact happened only after this front collision and comes from the ego's sudden braking.
- lane_keeping_hybrid_v2_012: turned_into_actor, policy at fault: yes. On a straight multi-lane highway at about 17 m/s, the policy took over at 4.6 s. It braked hard for no clear reason (down to 8 m/s, with the lead car 20+ m ahead and pulling away) and steered left out of its lane. That put its front into actor 1, which the ego's slowdown had brought alongside in the left lane. The hard, needless braking also got the ego rear-ended by traffic behind.
- lane_keeping_hybrid_v2_013: left_road, policy at fault: yes. After the handoff at 4.6 s, the ego braked hard on the highway, dropping from 29 to 13.5 m/s, which probably caused the rear contact by a following car. It also steered left, away from the recorded path, while the route command was STRAIGHT and then RIGHT, and drifted across the leftmost lane onto the left shoulder, where it went off-road at 7.7 s. Vehicle 40, which was passing on the right, overlapped the ego at that same moment.
- lane_keeping_hybrid_v2_014: left_road, policy at fault: yes. After handoff on a straight highway, the ego braked hard for no clear reason (28.8 down to 13.4 m/s) and was rear-ended by motorcycle 7 early on. It then drifted left across the leftmost lane onto the shoulder beside the median barrier, while the recorded path and the RIGHT command went right. By 7.8 s it was off-road and touching car 10, which had come up alongside it.
- lane_keeping_hybrid_v2_018: turned_into_actor, policy at fault: yes. On a multi-lane freeway with a RIGHT command, the ego ignored the recorded path to the right, kept planning a drift to the left, and steered into the lane on its left. Its front hit actor 28, which was passing on that side, about 4.8 m off the recorded trajectory.
- lane_keeping_hybrid_v2_019: turned_into_actor, policy at fault: yes. On a multi-lane highway with clear space ahead, the policy took over at 4.6s and braked hard for no visible reason, dropping from 20 to 11.5 m/s, while drifting about 1 m left of the recorded path. This brought it into side contact with actor 1, which was overtaking in the adjacent left lane. The rear contact came later, after the side collision, and probably follows from the sudden braking.
- lane_keeping_hybrid_v2_021: turned_into_actor, policy at fault: yes. The route command was RIGHT and the recorded human moved right, but after handoff the ego drifted left across the lane line into the next lane, ending 4.7 m from the recorded path. Actor 28 was passing in that lane, and the ego's front corner hit it as the ego cut in.
- lane_keeping_hybrid_v2_022: turned_into_actor, policy at fault: yes. On a multi-lane freeway the route command was STRAIGHT and then RIGHT, but the ego steered left out of its recorded lane, ending up 4.8 m from the human path. Holding about 7.3 m/s without braking, it hit vehicle 28 with its front as it merged into that vehicle's lane.
- lane_keeping_hybrid_v2_023: turned_into_actor, policy at fault: yes. After handoff, the ego left its lane and drifted left across the freeway lanes. Its planned path bent left even though the command was STRAIGHT and then RIGHT, and the recorded human path went right. Actor 28 was overtaking in the lane to the left, and the ego cut into it, hitting it with the ego's front at about 7 m/s, 4.8 m off the recorded trajectory.
- lane_keeping_hybrid_v2_026: other, policy at fault: unclear. In slow traffic with a STRAIGHT command, the ego crept forward and slowed to 0.5 m/s, staying 4.6 m behind lead car 24, while drifting about 2.8 m left of the recorded path. A pedestrian (the orange marker) passing between the queued cars overlapped the ego's front, causing a front collision at 8.6 s. The pedestrian can't be seen in the camera view, and it was probably replayed along a path the human driver never blocked.
- lane_keeping_hybrid_v2_031: turned_into_actor, policy at fault: yes. The ego was slowing in queued traffic with the command STRAIGHT. Instead of staying behind lead 24, which stayed about 4.6 m ahead, it drifted right until it straddled the line into the next lane, about 2.9 m off the recorded path. At about 0.1 m/s it made front contact with the car queued in that lane, most likely actor 21 just ahead on its front-right.
- lane_keeping_hybrid_v2_032: turned_into_actor, policy at fault: yes. The ego was slowing behind stopped traffic (3.1 to 0.5 m/s) and drifted right off the recorded path (about 2.8 m off by the end) until it straddled the line between car 24's lane and car 21's lane. At about 0.5 m/s its front clipped a queued car, most likely the rear corner of car 24 just ahead on its left.
- lane_keeping_hybrid_v2_041: left_road, policy at fault: yes. The road bends gently right and the command is RIGHT, but the ego kept a straight heading while slowing from 18 to 15 m/s. It drifted left across the yellow centre line and off the left edge toward the guardrail, about 1.7 m from the recorded path, which stays in the right lane. The camera image was blurred along the left edge but the road and lane markings were clear, so the drift was the policy's own lateral error.
- lane_keeping_hybrid_v2_042: left_road, policy at fault: yes. With a RIGHT command and an open road ahead, the policy's planned path kept heading straight or slightly left instead of following the route to the right. The ego drifted over the yellow left edge line onto the shoulder by the guardrail and went offroad at 9.9 s, about 1.7 m from the human's path.
- lane_keeping_hybrid_v2_043: left_road, policy at fault: yes. On a curving two-lane road with the command RIGHT, the policy ignored the route, which bore right into the right lane. Instead it held a straight, slightly left path, drifted across the double-yellow centerline and onto the left shoulder toward the guardrail, and was flagged offroad at 10.0 s, 1.7 m from the human trajectory. It slowed from about 20 to 16 m/s but never steered back toward its lane; no other actors were involved, and the camera view was clear until the shoulder.
- lane_keeping_hybrid_v2_045: left_road, policy at fault: yes. On a multi-lane highway with a RIGHT command, the policy steered its plan left, away from the recorded path, and drifted out of the leftmost lane toward the concrete median barrier at about 5 m/s. It went offroad at 8.4s, 3.6 m from the recorded trajectory. No actor was involved, and the camera view was clear enough before the drift.
- lane_keeping_hybrid_v2_046: left_road, policy at fault: yes. On a multi-lane highway with a RIGHT route command, the ego was in the leftmost lane at about 4–5 m/s. Its planned path kept curving left toward the median concrete barrier while the route went right, and it drifted over the left edge line and left the road at 8.6s, 3.7 m off the human trajectory.

## Every setting

- S1: 023b7fcc at lateral_bias_m -0.1, ego_speed_scale 1: 0/3 failed, rate 0%-47% (90%) (lane_keeping_hybrid_v2_047, lane_keeping_hybrid_v2_048, lane_keeping_hybrid_v2_049)
- S2: 023b7fcc at lateral_bias_m -0.1, ego_speed_scale 1.2: 0/2 failed, rate 0%-58% (90%) (lane_keeping_hybrid_v2_039, lane_keeping_hybrid_v2_040)
- S3: 023b7fcc at lateral_bias_m 0, ego_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (lane_keeping_hybrid_v2_009, lane_keeping_hybrid_v2_050)
- S4: 023b7fcc at lateral_bias_m 0, ego_speed_scale 1.2: 0/3 failed, rate 0%-47% (90%) (lane_keeping_hybrid_v2_015, lane_keeping_hybrid_v2_037, lane_keeping_hybrid_v2_038)
- S5: 023b7fcc at lateral_bias_m 0, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_v2_024)
- S6: 023b7fcc at lateral_bias_m 0.1, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_v2_016)
- S7: 023b7fcc at lateral_bias_m 0.1, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_v2_025)
- S8: 054b5901 at lateral_bias_m 0, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_v2_005)
- S9: 05f35348 at lateral_bias_m 0, ego_speed_scale 1: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (lane_keeping_hybrid_v2_006, lane_keeping_hybrid_v2_013, lane_keeping_hybrid_v2_014)
- S10: 09a95ffa at lateral_bias_m 0, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_v2_008)
- S11: 09a95ffa at lateral_bias_m 0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_v2_017)
- S12: 09a95ffa at lateral_bias_m 0.1, ego_speed_scale 1: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (lane_keeping_hybrid_v2_018, lane_keeping_hybrid_v2_021, lane_keeping_hybrid_v2_022)
- S13: 09a95ffa at lateral_bias_m 0.2, ego_speed_scale 1: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (lane_keeping_hybrid_v2_023)
- S14: 0ce6f2a3 at lateral_bias_m 0, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_v2_010)
- S15: 0cf6368d at lateral_bias_m 0, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_v2_001)
- S16: 0cf6368d at lateral_bias_m 0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_v2_020)
- S17: 0cf6368d at lateral_bias_m 0, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (lane_keeping_hybrid_v2_026, lane_keeping_hybrid_v2_031, lane_keeping_hybrid_v2_032)
- S18: 0cf6368d at lateral_bias_m 0.1, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_v2_027)
- S19: 0dbb91dd at lateral_bias_m 0, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_v2_004)
- S20: 12855a41 at lateral_bias_m 0, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_v2_002)
- S21: 12855a41 at lateral_bias_m 0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_v2_030)
- S22: 12855a41 at lateral_bias_m 0, ego_speed_scale 1.4: 0/2 failed, rate 0%-58% (90%) (lane_keeping_hybrid_v2_035, lane_keeping_hybrid_v2_036)
- S23: 12855a41 at lateral_bias_m 0.1, ego_speed_scale 1.2: 2/2 failed, rate 42%-100% (90%), 2 possibly the simulator's (lane_keeping_hybrid_v2_045, lane_keeping_hybrid_v2_046)
- S24: 19f339ba at lateral_bias_m 0, ego_speed_scale 1: 3/3 failed, rate 53%-100% (90%) (lane_keeping_hybrid_v2_003, lane_keeping_hybrid_v2_011, lane_keeping_hybrid_v2_012)
- S25: 19f339ba at lateral_bias_m 0, ego_speed_scale 1.2: 1/1 failed, rate 27%-100% (90%) (lane_keeping_hybrid_v2_019)
- S26: 1b7d131a at lateral_bias_m 0, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_v2_007)
- S27: 1b7d131a at lateral_bias_m 0, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_v2_028)
- S28: 1b7d131a at lateral_bias_m 0, ego_speed_scale 1.4: 0/2 failed, rate 0%-58% (90%) (lane_keeping_hybrid_v2_033, lane_keeping_hybrid_v2_034)
- S29: 1b7d131a at lateral_bias_m 0.1, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (lane_keeping_hybrid_v2_029)
- S30: 1b7d131a at lateral_bias_m 0.1, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%) (lane_keeping_hybrid_v2_041, lane_keeping_hybrid_v2_042, lane_keeping_hybrid_v2_043)

## Not kept by the gate

- lane_keeping_hybrid_v2_044: not kept: HALT

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
- 50 runs over 12 scenes and 45 settings is a sparse search. It may miss hard cases and cannot map the full grid.). Report written by claude-opus-5-5 from `results` in 27 s; every count above is computed from the queue, not written by the model.

0 of 50 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
