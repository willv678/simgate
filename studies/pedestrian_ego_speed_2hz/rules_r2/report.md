# In pedestrian-crossing scenes, which combinations of ego speed at hand-off (0.6x–1.4x recorded) and pedestrian step-out time (±2 s) make the VaVAM policy with the linear MPC collide or leave the road? Find the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `rules_r2`: 50 kept runs on 10 scenes, varying ego_speed_scale, actor_time_shift_s; 0 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 4 of 5 challenging settings confirmed, after 5 rounds.

## Answer

The study did not find a speed and step-out combination that makes the 2 Hz VaVAM policy fail. Four of the five cases were confirmed, but all four are the nominal setting (1.0x, 0 s) on scenes that fail anyway: 048b974e, 07981e6a, 0d4893f5 and 1bbe02fc. Every failure analysed involved a parked car, a neighbouring car or the road edge. None involved the pedestrian. On 1bbe02fc the failures are borderline road-edge flags that may come from the map rather than the policy. No off-nominal setting failed. Those settings mostly ran once each, only between 0.6x and 1.2x and at shifts of −0.5 s or 0 s, so this says little about the rest of the grid.

## Findings

- On 048b974e the policy fails at the nominal setting by leaving the route at the intersection and driving its front into a parked van or car at the curb. The runs are flagged as possible artifacts because the ego was far off the recorded path, but the video review blames the policy's wrong turn, not rendering.
  - S1: 048b974e at ego_speed_scale 1.0, actor_time_shift_s 0.0: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (pedestrian_ego_speed_2hz_rules_r2_005, pedestrian_ego_speed_2hz_rules_r2_011, pedestrian_ego_speed_2hz_rules_r2_021)
- On 07981e6a the policy fails at the nominal setting. It ignores the RIGHT command, drifts left into the parked cars at about 10–11 m/s and barely brakes.
  - S2: 07981e6a at ego_speed_scale 1.0, actor_time_shift_s 0.0: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_2hz_rules_r2_006, pedestrian_ego_speed_2hz_rules_r2_012, pedestrian_ego_speed_2hz_rules_r2_022)
- On 0d4893f5 the policy fails at the nominal setting. It drifts left into the next lane and hits the car travelling alongside it without braking. This is a sideways drift, not a failure to stop for the car ahead.
  - S11: 0d4893f5 at ego_speed_scale 1.0, actor_time_shift_s 0.0: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_2hz_rules_r2_008, pedestrian_ego_speed_2hz_rules_r2_013, pedestrian_ego_speed_2hz_rules_r2_023)
- On 1bbe02fc every failure at the nominal setting is a road-edge flag at the stop line, with the ego under 1 m from where the human drove. The video review could not say whether the policy was at fault, so this confirmed case may be a map-edge artifact.
  - S27: 1bbe02fc at ego_speed_scale 1.0, actor_time_shift_s 0.0: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_2hz_rules_r2_010, pedestrian_ego_speed_2hz_rules_r2_014, pedestrian_ego_speed_2hz_rules_r2_024)
- None of the four confirmed cases comes from the ego's speed or the pedestrian's timing. All of them sit at 1.0x and 0 s, and none of the reviewed failures involved the pedestrian.
  - S1: 048b974e at ego_speed_scale 1.0, actor_time_shift_s 0.0: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (pedestrian_ego_speed_2hz_rules_r2_005, pedestrian_ego_speed_2hz_rules_r2_011, pedestrian_ego_speed_2hz_rules_r2_021)
  - S2: 07981e6a at ego_speed_scale 1.0, actor_time_shift_s 0.0: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_2hz_rules_r2_006, pedestrian_ego_speed_2hz_rules_r2_012, pedestrian_ego_speed_2hz_rules_r2_022)
  - S11: 0d4893f5 at ego_speed_scale 1.0, actor_time_shift_s 0.0: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_2hz_rules_r2_008, pedestrian_ego_speed_2hz_rules_r2_013, pedestrian_ego_speed_2hz_rules_r2_023)
  - S27: 1bbe02fc at ego_speed_scale 1.0, actor_time_shift_s 0.0: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_2hz_rules_r2_010, pedestrian_ego_speed_2hz_rules_r2_014, pedestrian_ego_speed_2hz_rules_r2_024)
- On 0e002edd the nominal setting failed only occasionally, in one run where the ego cut a right turn tight into a parked car. Its range does not clear the 0.5 bar, so it is not confirmed. Single runs at 0.8x and 1.2x did not fail.
  - S13: 0e002edd at ego_speed_scale 1.0, actor_time_shift_s 0.0: 1/5 failed, rate 5%-56% (90%), 1 possibly the simulator's (pedestrian_ego_speed_2hz_rules_r2_001, pedestrian_ego_speed_2hz_rules_r2_015, pedestrian_ego_speed_2hz_rules_r2_025, pedestrian_ego_speed_2hz_rules_r2_031, pedestrian_ego_speed_2hz_rules_r2_041)
  - S12: 0e002edd at ego_speed_scale 0.8, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_r2_037)
  - S14: 0e002edd at ego_speed_scale 1.2, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_r2_047)
- The scenes the plan expected to be cleaner tests, 0caa8f1a, 18d28973 and 18f8dbd6, did not fail at the nominal setting across repeats, nor at any nearby speed tried. Those include the original CATK failures 0caa8f1a and 18d28973.
  - S9: 0caa8f1a at ego_speed_scale 1.0, actor_time_shift_s 0.0: 0/5 failed, rate 0%-35% (90%) (pedestrian_ego_speed_2hz_rules_r2_007, pedestrian_ego_speed_2hz_rules_r2_016, pedestrian_ego_speed_2hz_rules_r2_026, pedestrian_ego_speed_2hz_rules_r2_032, pedestrian_ego_speed_2hz_rules_r2_043)
  - S8: 0caa8f1a at ego_speed_scale 0.8, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_r2_038)
  - S10: 0caa8f1a at ego_speed_scale 1.2, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_r2_049)
  - S22: 18d28973 at ego_speed_scale 0.8, actor_time_shift_s 0.0: 0/3 failed, rate 0%-47% (90%) (pedestrian_ego_speed_2hz_rules_r2_028, pedestrian_ego_speed_2hz_rules_r2_034, pedestrian_ego_speed_2hz_rules_r2_044)
  - S23: 18d28973 at ego_speed_scale 1.0, actor_time_shift_s 0.0: 0/2 failed, rate 0%-58% (90%) (pedestrian_ego_speed_2hz_rules_r2_009, pedestrian_ego_speed_2hz_rules_r2_018)
  - S20: 18d28973 at ego_speed_scale 0.6, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_r2_040)
  - S21: 18d28973 at ego_speed_scale 0.8, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_r2_050)
  - S26: 18f8dbd6 at ego_speed_scale 1.0, actor_time_shift_s 0.0: 0/4 failed, rate 0%-40% (90%) (pedestrian_ego_speed_2hz_rules_r2_002, pedestrian_ego_speed_2hz_rules_r2_017, pedestrian_ego_speed_2hz_rules_r2_027, pedestrian_ego_speed_2hz_rules_r2_033)
  - S25: 18f8dbd6 at ego_speed_scale 0.8, actor_time_shift_s 0.0: 0/2 failed, rate 0%-58% (90%) (pedestrian_ego_speed_2hz_rules_r2_039, pedestrian_ego_speed_2hz_rules_r2_042)
  - S24: 18f8dbd6 at ego_speed_scale 0.6, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_r2_048)
- On 12a09194 the pedestrian never came close (criticality stayed at 0), and 0b10bce8 stayed uneventful at every speed and timing tried. Neither scene is a useful test of the speed–timing question at the settings run.
  - S15: 12a09194 at ego_speed_scale 0.6, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_r2_036)
  - S16: 12a09194 at ego_speed_scale 0.6, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_r2_030)
  - S17: 12a09194 at ego_speed_scale 0.8, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_r2_046)
  - S18: 12a09194 at ego_speed_scale 0.8, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_r2_020)
  - S19: 12a09194 at ego_speed_scale 1.0, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_r2_003)
  - S3: 0b10bce8 at ego_speed_scale 0.6, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_r2_035)
  - S4: 0b10bce8 at ego_speed_scale 0.6, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_r2_029)
  - S5: 0b10bce8 at ego_speed_scale 0.8, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_r2_045)
  - S6: 0b10bce8 at ego_speed_scale 0.8, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_r2_019)
  - S7: 0b10bce8 at ego_speed_scale 1.0, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_r2_004)

## Open

- Most of the grid was never run: no runs at 1.4x, no step-outs later than recorded, and nothing earlier than −0.5 s. A scan of the extremes is needed, starting with the scenes where the ego and pedestrian came closest (0e002edd, 18f8dbd6, 0caa8f1a): 1.2x and 1.4x combined with step-out shifts of −2, −1, +1 and +2 s, one run each, then repeats at any setting that fails or nearly fails.
- The fifth case is missing. 0e002edd is the nearest candidate. More nominal repeats, or repeats at off-nominal settings once a failure appears there, would show whether it clears the 0.5 bar.
- It is unclear whether 1bbe02fc is a real policy failure or a map-edge artifact. Someone needs to check the lane and curb boundary geometry at the stop line, or run the replayed human trajectory through the same off-road check.
- Off-nominal settings mostly ran once each. A clean single run is only a hint, not evidence of safety at that setting.
- The four scenes that fail at nominal settings fail for reasons unrelated to pedestrians, mainly the policy drifting left or ignoring the route command. Retiming the pedestrian there can't show an effect unless the runs are cut short before that drift or those scenes are dropped.
- The comparison with the 10 Hz study (pedestrian_ego_speed) can't be made from these results alone. Its table is needed side by side, especially for whether the left drift on 0d4893f5 and 07981e6a also shows up at 10 Hz.

## Why the runs failed (triage from the video and log)

turned_into_actor 9, left_road 3, no_brake_for_lead 1

- pedestrian_ego_speed_2hz_rules_r2_005: turned_into_actor, policy at fault: yes. At the intersection the policy left the green route (which went straight) and turned left into the side street. It cut the corner toward the left curb and drove its front into vehicle 155, a white van that was parked or slow at the kerb, at about 3.5 m/s while still turning. By then it was about 7 m off the recorded trajectory, and the rear contact came only after the front collision.
- pedestrian_ego_speed_2hz_rules_r2_006: turned_into_actor, policy at fault: yes. The route said RIGHT, but the policy ignored it and kept going at about 11 m/s up the left side of the street. It drifted left into the line of parked cars at the curb and its front hit parked car 3/87, slowing only slightly (11.0 to 9.6 m/s) as the gap closed from 31 m to 3.9 m. The rear contact recorded for this run came after this front collision.
- pedestrian_ego_speed_2hz_rules_r2_008: turned_into_actor, policy at fault: yes. While crossing the intersection at a steady ~8.4 m/s, the ego drifted left of its route (1.7 m off the human trajectory) into the adjacent lane. Its front struck actor 33, which was travelling alongside on the left. The lead vehicle stayed ~20 m ahead throughout, so this was a lateral drift into a neighboring car, not a failure to brake.
- pedestrian_ego_speed_2hz_rules_r2_010: left_road, policy at fault: unclear. About 1.5 s after handoff, while approaching the stop line at about 7 m/s, the ego was flagged offroad: its box edged past the right lane boundary near the curb corner. It was only 0.8 m from the recorded human path at that moment. The policy's plan headed straight and slightly left, matching the STRAIGHT command it was given, while the route actually turned right and the command only changed to RIGHT at the moment of failure. Because the offroad came from such a small deviation right next to where the human drove, it may be a map-edge artifact rather than a real departure from the road.
- pedestrian_ego_speed_2hz_rules_r2_011: turned_into_actor, policy at fault: yes. The route said RIGHT, but at the intersection the ego turned left and steered toward the parked cars along the curb of the cross street. At about 3.4 m/s its front hit vehicle 155, a white van, roughly 7 m off the human's recorded path.
- pedestrian_ego_speed_2hz_rules_r2_012: turned_into_actor, policy at fault: yes. With a RIGHT command and the recorded path veering right at the upcoming intersection, the policy instead steered gradually left out of its lane into the parking lane at about 10 m/s, and its front hit parked car 3 on the left curb. Speed barely dropped as the gap fell from 20 m to 3.8 m. The later rear contact and offroad flag come after this front collision.
- pedestrian_ego_speed_2hz_rules_r2_013: turned_into_actor, policy at fault: yes. Going straight at about 8.3 m/s toward the intersection, the ego drifted about 1.8 m left of the recorded path into the lane of actor 33, which was alongside it. At 7.7 s its front hit the rear-right of actor 33, without braking. The human driver stayed in the right lane, which was clear.
- pedestrian_ego_speed_2hz_rules_r2_014: left_road, policy at fault: unclear. Coming up to an intersection at about 7 m/s, the ego was in a lane whose route turned right. The policy's planned path instead bent left and straight across the intersection, so the ego drifted slightly left and crossed the lane boundary at the stop line. That was flagged offroad at 6.2 s, though the ego was only 0.8 m from the human trajectory. The route command showed STRAIGHT until the last frame, when it switched to RIGHT, and the offroad call came from a small, borderline drift past the lane edge, so it is not clear the policy is to blame.
- pedestrian_ego_speed_2hz_rules_r2_021: turned_into_actor, policy at fault: yes. On a RIGHT command at an urban intersection, the ego's planned path wobbled and it did not follow the turn lane: it swung about 7.5 m off the recorded route and drove at roughly 3.7 m/s into the narrow street next to the parked cars. Its front hit the parked car 101 or the van 155 just ahead (the gap had shrunk to 4.9 m) without braking. Another actor hit the ego's rear only after this front collision.
- pedestrian_ego_speed_2hz_rules_r2_022: no_brake_for_lead, policy at fault: yes. On a RIGHT-command approach to an intersection, the ego left the recorded path, which kept right toward the turn. It drifted left into the line of cars parked along the left curb and drove into parked car 3 at about 10–11 m/s. The gap to that car shrank from 31 m to 3 m, but the ego only slowed from 11.1 to 10.0 m/s, so this was a front collision with a stationary car. The rear contact and offroad flags came after the frontal hit.
- pedestrian_ego_speed_2hz_rules_r2_023: turned_into_actor, policy at fault: yes. At about 8.3 m/s and without braking, the ego's planned path drifted left from the recorded straight path, so it moved into the left lane next to it. There it ran its front into the rear of actor 33 at the intersection stop line (1.8 m off the recording when it hit).
- pedestrian_ego_speed_2hz_rules_r2_024: left_road, policy at fault: unclear. The ego approached the intersection in the right-most lane at about 7 m/s, close to the right curb. As it reached the stop line it was flagged offroad on the right edge, while its planned path bent left (straight across) even though the route turned right. The ego was only 0.7 m from the human trajectory, so this looks like a marginal clip of the curb corner rather than a clear drift off the road.
- pedestrian_ego_speed_2hz_rules_r2_025: turned_into_actor, policy at fault: yes. The route command was RIGHT. The ego cut its right turn much tighter than the recorded path, ending about 7 m off it, and drove slowly (about 3.8 m/s) head-on into parked car 90 at the curb on the corner of the cross street. The camera stayed coherent up to the impact, and the parked cars were visible in the frames before it.

## Every setting

- S1: 048b974e at ego_speed_scale 1.0, actor_time_shift_s 0.0: 3/3 failed, rate 53%-100% (90%), 3 possibly the simulator's (pedestrian_ego_speed_2hz_rules_r2_005, pedestrian_ego_speed_2hz_rules_r2_011, pedestrian_ego_speed_2hz_rules_r2_021)
- S2: 07981e6a at ego_speed_scale 1.0, actor_time_shift_s 0.0: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_2hz_rules_r2_006, pedestrian_ego_speed_2hz_rules_r2_012, pedestrian_ego_speed_2hz_rules_r2_022)
- S3: 0b10bce8 at ego_speed_scale 0.6, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_r2_035)
- S4: 0b10bce8 at ego_speed_scale 0.6, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_r2_029)
- S5: 0b10bce8 at ego_speed_scale 0.8, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_r2_045)
- S6: 0b10bce8 at ego_speed_scale 0.8, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_r2_019)
- S7: 0b10bce8 at ego_speed_scale 1.0, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_r2_004)
- S8: 0caa8f1a at ego_speed_scale 0.8, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_r2_038)
- S9: 0caa8f1a at ego_speed_scale 1.0, actor_time_shift_s 0.0: 0/5 failed, rate 0%-35% (90%) (pedestrian_ego_speed_2hz_rules_r2_007, pedestrian_ego_speed_2hz_rules_r2_016, pedestrian_ego_speed_2hz_rules_r2_026, pedestrian_ego_speed_2hz_rules_r2_032, pedestrian_ego_speed_2hz_rules_r2_043)
- S10: 0caa8f1a at ego_speed_scale 1.2, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_r2_049)
- S11: 0d4893f5 at ego_speed_scale 1.0, actor_time_shift_s 0.0: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_2hz_rules_r2_008, pedestrian_ego_speed_2hz_rules_r2_013, pedestrian_ego_speed_2hz_rules_r2_023)
- S12: 0e002edd at ego_speed_scale 0.8, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_r2_037)
- S13: 0e002edd at ego_speed_scale 1.0, actor_time_shift_s 0.0: 1/5 failed, rate 5%-56% (90%), 1 possibly the simulator's (pedestrian_ego_speed_2hz_rules_r2_001, pedestrian_ego_speed_2hz_rules_r2_015, pedestrian_ego_speed_2hz_rules_r2_025, pedestrian_ego_speed_2hz_rules_r2_031, pedestrian_ego_speed_2hz_rules_r2_041)
- S14: 0e002edd at ego_speed_scale 1.2, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_r2_047)
- S15: 12a09194 at ego_speed_scale 0.6, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_r2_036)
- S16: 12a09194 at ego_speed_scale 0.6, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_r2_030)
- S17: 12a09194 at ego_speed_scale 0.8, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_r2_046)
- S18: 12a09194 at ego_speed_scale 0.8, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_r2_020)
- S19: 12a09194 at ego_speed_scale 1.0, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_r2_003)
- S20: 18d28973 at ego_speed_scale 0.6, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_r2_040)
- S21: 18d28973 at ego_speed_scale 0.8, actor_time_shift_s -0.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_r2_050)
- S22: 18d28973 at ego_speed_scale 0.8, actor_time_shift_s 0.0: 0/3 failed, rate 0%-47% (90%) (pedestrian_ego_speed_2hz_rules_r2_028, pedestrian_ego_speed_2hz_rules_r2_034, pedestrian_ego_speed_2hz_rules_r2_044)
- S23: 18d28973 at ego_speed_scale 1.0, actor_time_shift_s 0.0: 0/2 failed, rate 0%-58% (90%) (pedestrian_ego_speed_2hz_rules_r2_009, pedestrian_ego_speed_2hz_rules_r2_018)
- S24: 18f8dbd6 at ego_speed_scale 0.6, actor_time_shift_s 0.0: 0/1 failed, rate 0%-73% (90%) (pedestrian_ego_speed_2hz_rules_r2_048)
- S25: 18f8dbd6 at ego_speed_scale 0.8, actor_time_shift_s 0.0: 0/2 failed, rate 0%-58% (90%) (pedestrian_ego_speed_2hz_rules_r2_039, pedestrian_ego_speed_2hz_rules_r2_042)
- S26: 18f8dbd6 at ego_speed_scale 1.0, actor_time_shift_s 0.0: 0/4 failed, rate 0%-40% (90%) (pedestrian_ego_speed_2hz_rules_r2_002, pedestrian_ego_speed_2hz_rules_r2_017, pedestrian_ego_speed_2hz_rules_r2_027, pedestrian_ego_speed_2hz_rules_r2_033)
- S27: 1bbe02fc at ego_speed_scale 1.0, actor_time_shift_s 0.0: 3/3 failed, rate 53%-100% (90%) (pedestrian_ego_speed_2hz_rules_r2_010, pedestrian_ego_speed_2hz_rules_r2_014, pedestrian_ego_speed_2hz_rules_r2_024)

## Provenance

Plan: `plan.json` (rationale: Copied from studies/pedestrian_ego_speed/plan.json (10 Hz) with the policy planning every 500 ms, so the method comparison can be repeated at 2 Hz. Scenes: these are the 10 scenes tagged pedestrian_crossing that have a recorded pedestrian key actor. Each scene's pedestrian is set in retime_tracks, so actor_time_shift_s moves only that person. actor_speed_scale stays at 1.0, so the pedestrian walks at the recorded speed. Traffic is replay, which keeps the scenario scripted as in Euro NCAP pedestrian tests. There is no delay, bias or noise.

Two other tagged scenes are left out: 095cf563 and 13a9767e. Neither has a pedestrian key actor, so a person-class retime there might hit no actor or the wrong one.

Budget: 5 rounds of 10 runs gives 50 runs, as the brief asks. The goal is top_k with k=5, high_min=0.5 and distinct scenes. With 90% ranges, each confirmed case needs about 4–5 failures out of 5 repeats, so roughly 25 runs go to confirmation and about 25 to searching the 5×9 grid. That is tight, and with partial results the study may confirm fewer than 5 cases.

Caveats:
- 6 of the scenes (048b974e, 07981e6a, 0caa8f1a, 0d4893f5, 18d28973, 1bbe02fc) failed at 0 delay in an earlier CATK run. That run used reactive traffic, not replay, so it may not carry over. If one still fails at 1.0x / 0 s, its failures may not come from speed or timing, and it fills a top_k slot cheaply without answering the question.
- 0e002edd, 18f8dbd6, 12a09194 and 0b10bce8 are the cleaner tests. In 0b10bce8 the ego barely moved (8.9 m), and in 12a09194 the pedestrian stayed far away (11.5 m).
- The failure check counts any front or side collision or leaving the road. It cannot tell whether the ego hit the pedestrian or another actor. Near misses are reported as closest approach to any actor, not ranked as failures.
- With ego_speed_scale above 1, the first second or two of the warm-up starts off the recorded scene.). Report written by claude-opus-5-5 from `results` in 21 s; every count above is computed from the queue, not written by the model.

50 of 50 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
