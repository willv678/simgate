# In cut-in and lead-vehicle scenes that pass as recorded, which combinations of the car's timing, the car's speed and the ego's speed at hand-off make the policy collide or leave the road? The aim is the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `hybrid_v2_r2`: 60 kept runs on 10 scenes, varying actor_time_shift_s, actor_speed_scale, ego_speed_scale; 3 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 2 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The goal was not met: only 2 of the 5 cases were confirmed, on two different scenes. On 19f339ba, with the car on recorded timing at 1.25x speed and the ego at 1.4x, every run failed (S38). On 096988dd, with the car at 1.25x and the ego at 1.2x, every run also failed (S4). For both settings the 90% range sits just above 0.5, so each rests on only a few runs. In both scenes the ego's hand-off speed made the difference: the same car setting with the ego at 1.0x did not fail (S3, S36), and on 19f339ba the ego at 1.2x failed in most runs but was not confirmed (S37). None of the failures were rendering artifacts, and triage put the policy at fault in all of them. However, the policy did not hit the retimed car: it braked hard for no reason or drifted left, then struck a car in the next lane. So this is evidence about the policy's left drift and unneeded braking at raised ego speed, not about the retimed car's timing or speed. No other scene produced a failure.

## Findings

- Confirmed case 1: scene 19f339ba, car on recorded timing at 1.25x speed, ego at 1.4x. Every run failed. The ego braked hard with the lead car 40 m or more ahead, angled left, and its front-left corner hit actor 1 in the left lane. Actor 1 is not the retimed car.
  - S38: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_031, car_conflicts_3knobs_2hz_hybrid_v2_r2_032, car_conflicts_3knobs_2hz_hybrid_v2_r2_041)
- Confirmed case 2: scene 096988dd, car on recorded timing at 1.25x speed, ego at 1.2x. Every run failed. The policy's plan bent left even though the route command was straight and then right, and the ego hit actor 41 in the left lane, about 1.6–1.7 m left of the human's path.
  - S4: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_011, car_conflicts_3knobs_2hz_hybrid_v2_r2_021, car_conflicts_3knobs_2hz_hybrid_v2_r2_022)
- On these two scenes the ego's hand-off speed is what tipped the policy into failure. At the same car setting with the ego at 1.0x neither scene failed. On 19f339ba the ego at 1.2x failed in most runs, by the same mechanism (unneeded hard braking, then drifting left into actor 1), but its range still reaches below 0.5. The car's own speed was held at 1.25x in all of these, so its effect was not isolated.
  - S3: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_002)
  - S4: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_011, car_conflicts_3knobs_2hz_hybrid_v2_r2_021, car_conflicts_3knobs_2hz_hybrid_v2_r2_022)
  - S36: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_004)
  - S37: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 3/4 failed, rate 36%-94% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_015, car_conflicts_3knobs_2hz_hybrid_v2_r2_023, car_conflicts_3knobs_2hz_hybrid_v2_r2_024, car_conflicts_3knobs_2hz_hybrid_v2_r2_033)
  - S38: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_031, car_conflicts_3knobs_2hz_hybrid_v2_r2_032, car_conflicts_3knobs_2hz_hybrid_v2_r2_041)
- Every failure was a front or side impact that triage counted as the policy's fault. Where the ego was also hit from behind, that came from its own unneeded hard braking. None of the failures was flagged as a possible simulator artifact.
  - S4: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_011, car_conflicts_3knobs_2hz_hybrid_v2_r2_021, car_conflicts_3knobs_2hz_hybrid_v2_r2_022)
  - S37: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 3/4 failed, rate 36%-94% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_015, car_conflicts_3knobs_2hz_hybrid_v2_r2_023, car_conflicts_3knobs_2hz_hybrid_v2_r2_024, car_conflicts_3knobs_2hz_hybrid_v2_r2_033)
  - S38: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_031, car_conflicts_3knobs_2hz_hybrid_v2_r2_032, car_conflicts_3knobs_2hz_hybrid_v2_r2_041)
- Scenes 09a95ffa, 0cf6368d and 0e899dd3 did not fail even with repeats at the harshest settings tried (car 0.5–1 s earlier at 1.25x, ego at 1.4x). Their ranges stay below 0.5, so a high failure rate at those settings is unlikely.
  - S5: 09a95ffa at actor_time_shift_s -1, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_051, car_conflicts_3knobs_2hz_hybrid_v2_r2_052, car_conflicts_3knobs_2hz_hybrid_v2_r2_053)
  - S11: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_013, car_conflicts_3knobs_2hz_hybrid_v2_r2_034, car_conflicts_3knobs_2hz_hybrid_v2_r2_035)
  - S14: 0cf6368d at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_057, car_conflicts_3knobs_2hz_hybrid_v2_r2_058, car_conflicts_3knobs_2hz_hybrid_v2_r2_059)
  - S20: 0e899dd3 at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_054, car_conflicts_3knobs_2hz_hybrid_v2_r2_055, car_conflicts_3knobs_2hz_hybrid_v2_r2_056_a2)
- Scenes 023b7fcc, 0dbb91dd, 187e6244, 1c45ce3a and 12855a41 got only one or two runs per setting, all near the recorded timing. None failed, but that is a hint, not a rate.
  - S1: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_001)
  - S18: 0dbb91dd at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_006)
  - S34: 187e6244 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_005)
  - S39: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_010)
  - S40: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_029)
  - S28: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_018)
  - S29: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_003, car_conflicts_3knobs_2hz_hybrid_v2_r2_040)
  - S30: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_017)
  - S31: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_030)
  - S32: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_048_a2)
  - S33: 12855a41 at actor_time_shift_s 0, actor_speed_scale 2, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_047)

## Open

- Three more confirmed cases on different scenes are still needed. The closest candidate scenes did not fail at the ego speeds tried. To look for more, run ego at 1.4x on 12855a41, 023b7fcc, 187e6244, 0dbb91dd and 1c45ce3a, then repeat any setting that fails until it reaches about 5 runs.
- Does the retimed car matter at all? Rerun S4's and S38's ego speeds with the car at 1.0x speed and at 0.5x–0.75x speed. If they still fail, the failure comes from the ego speed alone (unneeded braking and left drift into a neighbouring car).
- Most of the knob space was not tested: car timing beyond ±1 s, car speed below 1.0x or up to 2x on most scenes, and ego speed below 1.0x. A slowing lead car (car speed 0.5x, car earlier by 1–2 s) is the classic lead-vehicle conflict, and it was never tried.
- S37 (19f339ba, ego 1.2x) needs a few more runs to settle whether its failure rate is above 0.5.
- The study set the 2 Hz planning rate (control_timestep_us 500000) but did not check it in the runs.

## Why the runs failed (triage from the video and log)

turned_into_actor 8, other 1

- car_conflicts_3knobs_2hz_hybrid_v2_r2_011: turned_into_actor, policy at fault: yes. On a multi-lane highway in the rain, the policy's plan bent left even though the route command was STRAIGHT and then RIGHT, and the ego drifted toward the lane on its left. Actor 41 was passing in that lane, and at 7.7 s the ego's front-left hit it, about 1.7 m to the left of where the human drove.
- car_conflicts_3knobs_2hz_hybrid_v2_r2_015: turned_into_actor, policy at fault: yes. On an open highway with the lead vehicle more than 40 m ahead, the ego braked hard for no clear reason (20.3 to 7.8 m/s) and drifted left about 1.25 m off the recorded path, across the lane line. Actor 1, overtaking in the left lane, was struck by the ego's front-left corner. The rear contact the ego received came from its own unnecessary hard braking.
- car_conflicts_3knobs_2hz_hybrid_v2_r2_021: turned_into_actor, policy at fault: yes. On a multi-lane highway, the policy steered left toward the next lane over even though the route command was STRAIGHT and then RIGHT, and the recorded path stayed in lane or moved right. The ego's front corner hit actor 41 (a white SUV) driving alongside in that left lane at about 7.7 s.
- car_conflicts_3knobs_2hz_hybrid_v2_r2_022: turned_into_actor, policy at fault: yes. On a multi-lane highway with a STRAIGHT and then RIGHT command, the ego slowed from 6.7 to 4.4 m/s and drifted left, following its own leftward planned path, into the next lane. Vehicle 41 was coming up alongside in that lane, and the ego's front-left corner hit it, ending 1.6 m left of the recorded human path.
- car_conflicts_3knobs_2hz_hybrid_v2_r2_024: turned_into_actor, policy at fault: yes. On a clear multi-lane highway, the ego braked hard for no visible reason (20.3 to 7.9 m/s, with the nearest car in its lane 40–53 m ahead). Its planned path bent left, and it drifted toward the left lane just as actor 1, which had been alongside, moved ahead of it. The ego's front hit actor 1's rear-right at 7.6 s, and the hard braking probably also got the ego rear-ended.
- car_conflicts_3knobs_2hz_hybrid_v2_r2_031: other, policy at fault: yes. On an open highway, with the nearest car ahead 40–50 m away, the ego braked hard for no visible reason after handoff, slowing from 23.7 to 6.8 m/s. Actor 1, a replayed car that does not react to the ego, was coming up from behind on the left and moved toward the ego's lane. Because the ego was now well behind where the human driver had been (9.6 m), actor 1 ended up overlapping its front-left, which counted as an at-fault front collision; the run also recorded a rear contact.
- car_conflicts_3knobs_2hz_hybrid_v2_r2_032: turned_into_actor, policy at fault: yes. On an open highway with the nearest lead 40–50 m ahead and pulling away, the ego braked hard for no visible reason (23.7 to 7.1 m/s) while its path wobbled left. Actor 1 in the left lane caught up and came alongside, and the ego's front-left corner, angled toward the left lane, struck it.
- car_conflicts_3knobs_2hz_hybrid_v2_r2_033: turned_into_actor, policy at fault: yes. On an open multi-lane highway, the ego braked hard for no clear reason, dropping from 20.3 to 7.9 m/s with the nearest vehicle ahead 40–56 m away, while its planned path drifted left. Actor 1, which had been beside it in the left lane, moved ahead, and the ego's front left corner hit it as the ego edged into that lane. The ego was later rear-ended because of the unneeded hard braking.
- car_conflicts_3knobs_2hz_hybrid_v2_r2_041: turned_into_actor, policy at fault: yes. On an open highway, the ego braked hard for no visible reason, slowing from 23.7 to 6.7 m/s while the lead vehicle pulled further ahead (gap grew from 40 to 54 m). Actor 1, coming up from behind in the lane to the left, drew alongside, and the ego's front-left corner clipped it as the ego angled slightly left toward that lane. The rear contact flag likely comes from traffic behind the ego after it braked so hard.

## Every setting

- S1: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_001)
- S2: 096988dd at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_012)
- S3: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_002)
- S4: 096988dd at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_011, car_conflicts_3knobs_2hz_hybrid_v2_r2_021, car_conflicts_3knobs_2hz_hybrid_v2_r2_022)
- S5: 09a95ffa at actor_time_shift_s -1, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_051, car_conflicts_3knobs_2hz_hybrid_v2_r2_052, car_conflicts_3knobs_2hz_hybrid_v2_r2_053)
- S6: 09a95ffa at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_036, car_conflicts_3knobs_2hz_hybrid_v2_r2_042)
- S7: 09a95ffa at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_043, car_conflicts_3knobs_2hz_hybrid_v2_r2_060)
- S8: 09a95ffa at actor_time_shift_s -0.5, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_044)
- S9: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_014)
- S10: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_008)
- S11: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_013, car_conflicts_3knobs_2hz_hybrid_v2_r2_034, car_conflicts_3knobs_2hz_hybrid_v2_r2_035)
- S12: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_025)
- S13: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_026)
- S14: 0cf6368d at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_057, car_conflicts_3knobs_2hz_hybrid_v2_r2_058, car_conflicts_3knobs_2hz_hybrid_v2_r2_059)
- S15: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_007)
- S16: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_039)
- S17: 0cf6368d at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_049)
- S18: 0dbb91dd at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_006)
- S19: 0e899dd3 at actor_time_shift_s -0.5, actor_speed_scale 1, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_038)
- S20: 0e899dd3 at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/3 failed, rate 0%-47% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_054, car_conflicts_3knobs_2hz_hybrid_v2_r2_055, car_conflicts_3knobs_2hz_hybrid_v2_r2_056_a2)
- S21: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 0.75, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_028)
- S22: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_020, car_conflicts_3knobs_2hz_hybrid_v2_r2_037_a2)
- S23: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_027)
- S24: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_009)
- S25: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_019, car_conflicts_3knobs_2hz_hybrid_v2_r2_050)
- S26: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.4: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_045)
- S27: 0e899dd3 at actor_time_shift_s 0.5, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_046)
- S28: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_018)
- S29: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_003, car_conflicts_3knobs_2hz_hybrid_v2_r2_040)
- S30: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_017)
- S31: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_030)
- S32: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1.5, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_048_a2)
- S33: 12855a41 at actor_time_shift_s 0, actor_speed_scale 2, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_047)
- S34: 187e6244 at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_005)
- S35: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_016)
- S36: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_004)
- S37: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 3/4 failed, rate 36%-94% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_015, car_conflicts_3knobs_2hz_hybrid_v2_r2_023, car_conflicts_3knobs_2hz_hybrid_v2_r2_024, car_conflicts_3knobs_2hz_hybrid_v2_r2_033)
- S38: 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.4: 3/3 failed, rate 53%-100% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_031, car_conflicts_3knobs_2hz_hybrid_v2_r2_032, car_conflicts_3knobs_2hz_hybrid_v2_r2_041)
- S39: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_010)
- S40: 1c45ce3a at actor_time_shift_s 0, actor_speed_scale 1.25, ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_hybrid_v2_r2_029)

## Not kept by the gate

- car_conflicts_3knobs_2hz_hybrid_v2_r2_037: not kept: RE-RUN
- car_conflicts_3knobs_2hz_hybrid_v2_r2_048: not kept: RE-RUN
- car_conflicts_3knobs_2hz_hybrid_v2_r2_056: not kept: RE-RUN

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
- A scale above 1 starts the ego behind its recorded start, so for the first second or two of the warm-up it is off the recording.). Report written by claude-opus-5-5 from `results` in 22 s; every count above is computed from the queue, not written by the model.

0 of 63 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
