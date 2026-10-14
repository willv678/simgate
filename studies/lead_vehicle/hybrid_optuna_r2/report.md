# In lead-vehicle scenes, which timing shifts and speed scalings of the recorded lead car (with up to 200 ms planner delay if needed) make VaVAM run into it? Find the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `hybrid_optuna_r2`: 49 kept runs on 8 scenes, varying actor_time_shift_s, actor_speed_scale, planner_delay_us; 1 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 2 of 5 challenging settings confirmed, after 7 rounds.

## Answer

The goal was not met. Only two of the five cases were confirmed, and only one of them is a rear-end of the lead car. On 0e899dd3, moving the lead pickup 1 s earlier and slowing it to 0.5x, with 100 ms planner delay, made the ego hit its rear in every run (S16). But the ego took over only about 0.5 s before contact, with roughly 6 m of gap, so triage could not say whether the policy was at fault. On 19f339ba, a 1 s earlier shift at the recorded speed with 100 ms delay also failed every run (S22), but the lead car was not involved: the policy braked hard for no reason and drifted left into a car in the next lane. The only other failures were on 096988dd (S5) and 19f339ba at zero delay (S23). Both are the same kind of left drift into a passing car, and with only one to three runs at each setting they are hints, not confirmed rates. Five scenes never failed at any setting tried. No failure was flagged as a possible simulator artifact.

## Findings

- 0e899dd3 with the lead pickup 1 s earlier at 0.5x speed and 100 ms planner delay is a confirmed rear-end case: every run hit the pickup's rear. But the policy took over with only about 6 m of gap and 0.5 s before contact while closing on a much slower car, so triage could not say whether the policy was at fault.
  - S16: 0e899dd3 at actor_time_shift_s -1, actor_speed_scale 0.5, planner_delay_us 100000: 3/3 failed, rate 53%-100% (90%) (lead_vehicle_hybrid_optuna_r2_040, lead_vehicle_hybrid_optuna_r2_045, lead_vehicle_hybrid_optuna_r2_046)
- On 0e899dd3, other settings did not cause failures: the recorded speed with a 1.5 s earlier shift at 0 delay, and faster lead cars (1.25x, 2x) with up to 150 ms delay. The slowed lead car together with the planner delay seems to be what made it fail.
  - S15: 0e899dd3 at actor_time_shift_s -1.5, actor_speed_scale 1, planner_delay_us 0: 0/4 failed, rate 0%-40% (90%) (lead_vehicle_hybrid_optuna_r2_013, lead_vehicle_hybrid_optuna_r2_017, lead_vehicle_hybrid_optuna_r2_018, lead_vehicle_hybrid_optuna_r2_039)
  - S17: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.25, planner_delay_us 150000: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_hybrid_optuna_r2_026)
  - S18: 0e899dd3 at actor_time_shift_s 0.5, actor_speed_scale 2, planner_delay_us 100000: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_hybrid_optuna_r2_030)
  - S16: 0e899dd3 at actor_time_shift_s -1, actor_speed_scale 0.5, planner_delay_us 100000: 3/3 failed, rate 53%-100% (90%) (lead_vehicle_hybrid_optuna_r2_040, lead_vehicle_hybrid_optuna_r2_045, lead_vehicle_hybrid_optuna_r2_046)
- 19f339ba with the lead car 1 s earlier at recorded speed and 100 ms delay failed in every run, but none of these was a rear-end. Each time the policy braked hard with a clear lane ahead, drifted left, and hit a car in the adjacent left lane. This is a policy fault, but not a lead-vehicle braking case.
  - S22: 19f339ba at actor_time_shift_s -1, actor_speed_scale 1, planner_delay_us 100000: 3/3 failed, rate 53%-100% (90%) (lead_vehicle_hybrid_optuna_r2_005, lead_vehicle_hybrid_optuna_r2_015, lead_vehicle_hybrid_optuna_r2_016)
- 19f339ba also failed in its single run at 0 delay with the lead car 0.5 s later and faster (1.25x), and in the same way: needless braking and a left drift into the adjacent car. This scene's failures seem to come from the policy's own lateral behaviour rather than from the retiming.
  - S23: 19f339ba at actor_time_shift_s 0.5, actor_speed_scale 1.25, planner_delay_us 0: 1/1 failed, rate 27%-100% (90%) (lead_vehicle_hybrid_optuna_r2_002)
- 096988dd with the lead car 0.5 s later at 1.25x speed and no delay failed in most of its runs, but not enough for confirmation. Both failures were the ego veering left into a pickup passing in the left lane, not a rear-end. Slower or earlier lead cars on this scene, with up to 100 ms delay, did not fail.
  - S5: 096988dd at actor_time_shift_s 0.5, actor_speed_scale 1.25, planner_delay_us 0: 2/3 failed, rate 25%-92% (90%) (lead_vehicle_hybrid_optuna_r2_042, lead_vehicle_hybrid_optuna_r2_043, lead_vehicle_hybrid_optuna_r2_044)
  - S3: 096988dd at actor_time_shift_s -1.5, actor_speed_scale 0.5, planner_delay_us 50000: 0/3 failed, rate 0%-47% (90%) (lead_vehicle_hybrid_optuna_r2_003, lead_vehicle_hybrid_optuna_r2_008, lead_vehicle_hybrid_optuna_r2_009)
  - S4: 096988dd at actor_time_shift_s -1, actor_speed_scale 0.75, planner_delay_us 100000: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_hybrid_optuna_r2_027)
  - S6: 096988dd at actor_time_shift_s 2, actor_speed_scale 1, planner_delay_us 100000: 0/2 failed, rate 0%-58% (90%) (lead_vehicle_hybrid_optuna_r2_028, lead_vehicle_hybrid_optuna_r2_034)
- No setting tried on 023b7fcc, 09a95ffa, 0cf6368d, 0dbb91dd or 12855a41 caused a failure, even with planner delay up to 150–200 ms on some of them. Several of these settings have only one run, though, so they are not shown to be safe.
  - S1: 023b7fcc at actor_time_shift_s -0.5, actor_speed_scale 1.25, planner_delay_us 100000: 0/3 failed, rate 0%-47% (90%) (lead_vehicle_hybrid_optuna_r2_021, lead_vehicle_hybrid_optuna_r2_022, lead_vehicle_hybrid_optuna_r2_023)
  - S2: 023b7fcc at actor_time_shift_s 1.5, actor_speed_scale 1, planner_delay_us 100000: 0/3 failed, rate 0%-47% (90%) (lead_vehicle_hybrid_optuna_r2_032, lead_vehicle_hybrid_optuna_r2_036, lead_vehicle_hybrid_optuna_r2_049)
  - S7: 09a95ffa at actor_time_shift_s -1, actor_speed_scale 1, planner_delay_us 150000: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_hybrid_optuna_r2_029_a2)
  - S8: 09a95ffa at actor_time_shift_s 1.5, actor_speed_scale 0.75, planner_delay_us 50000: 0/4 failed, rate 0%-40% (90%) (lead_vehicle_hybrid_optuna_r2_014, lead_vehicle_hybrid_optuna_r2_019, lead_vehicle_hybrid_optuna_r2_024, lead_vehicle_hybrid_optuna_r2_038)
  - S9: 0cf6368d at actor_time_shift_s -1, actor_speed_scale 1.25, planner_delay_us 100000: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_hybrid_optuna_r2_033)
  - S10: 0cf6368d at actor_time_shift_s -0.5, actor_speed_scale 1, planner_delay_us 50000: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_hybrid_optuna_r2_004)
  - S11: 0cf6368d at actor_time_shift_s 1, actor_speed_scale 1.25, planner_delay_us 0: 0/3 failed, rate 0%-47% (90%) (lead_vehicle_hybrid_optuna_r2_001, lead_vehicle_hybrid_optuna_r2_010, lead_vehicle_hybrid_optuna_r2_011)
  - S12: 0dbb91dd at actor_time_shift_s -1, actor_speed_scale 1, planner_delay_us 200000: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_hybrid_optuna_r2_006)
  - S13: 0dbb91dd at actor_time_shift_s -1, actor_speed_scale 1.5, planner_delay_us 100000: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_hybrid_optuna_r2_007)
  - S14: 0dbb91dd at actor_time_shift_s 0.5, actor_speed_scale 0.5, planner_delay_us 0: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_hybrid_optuna_r2_035)
  - S19: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1, planner_delay_us 0: 0/3 failed, rate 0%-47% (90%) (lead_vehicle_hybrid_optuna_r2_012, lead_vehicle_hybrid_optuna_r2_020, lead_vehicle_hybrid_optuna_r2_025)
  - S20: 12855a41 at actor_time_shift_s 1, actor_speed_scale 1, planner_delay_us 100000: 0/2 failed, rate 0%-58% (90%) (lead_vehicle_hybrid_optuna_r2_031, lead_vehicle_hybrid_optuna_r2_037)
  - S21: 12855a41 at actor_time_shift_s 2, actor_speed_scale 1.25, planner_delay_us 200000: 0/3 failed, rate 0%-47% (90%) (lead_vehicle_hybrid_optuna_r2_041, lead_vehicle_hybrid_optuna_r2_047, lead_vehicle_hybrid_optuna_r2_048)
- The settings with the most repeats and no failures are on 09a95ffa (1.5 s later, 0.75x, 50 ms) and 0e899dd3 (1.5 s earlier, recorded speed, 0 delay). These are the settings most clearly shown not to be challenging.
  - S8: 09a95ffa at actor_time_shift_s 1.5, actor_speed_scale 0.75, planner_delay_us 50000: 0/4 failed, rate 0%-40% (90%) (lead_vehicle_hybrid_optuna_r2_014, lead_vehicle_hybrid_optuna_r2_019, lead_vehicle_hybrid_optuna_r2_024, lead_vehicle_hybrid_optuna_r2_038)
  - S15: 0e899dd3 at actor_time_shift_s -1.5, actor_speed_scale 1, planner_delay_us 0: 0/4 failed, rate 0%-40% (90%) (lead_vehicle_hybrid_optuna_r2_013, lead_vehicle_hybrid_optuna_r2_017, lead_vehicle_hybrid_optuna_r2_018, lead_vehicle_hybrid_optuna_r2_039)

## Open

- Whether S16 (0e899dd3) is a policy failure or set up to be unavoidable. The policy takes over only 0.5 s before contact, with about 6 m of gap. Re-running with an earlier handoff, or the same retiming at 0 delay, would show whether the policy can stop in time.
- Whether 096988dd at +0.5 s, 1.25x, 0 delay (S5) is reliably challenging. A few more repeats would confirm or reject it, but it would count as a lateral turn into another car, not a rear-end.
- Whether the left-drift failures on 19f339ba happen without any retiming. Runs at 0 s shift, 1.0x speed and 0 delay would show whether it is a baseline policy problem unrelated to the lead car.
- Whether a 0.5x lead car with 100 ms delay, the combination that failed on 0e899dd3, also causes rear-ends on the scenes that never failed (023b7fcc, 09a95ffa, 0cf6368d, 0dbb91dd, 12855a41). Most of those scenes were only probed with single runs at other settings.
- Three more confirmed cases on distinct scenes are still needed. The budget was spent mostly on screening, so the remaining candidates have one or no failures.

## Why the runs failed (triage from the video and log)

turned_into_actor 6, no_brake_for_lead 3

- lead_vehicle_hybrid_optuna_r2_002: turned_into_actor, policy at fault: yes. After the 4.6 s handoff on the highway, the ego braked hard without a reason ahead (17→10 m/s with a 30–48 m gap). It also yawed left out of its lane, against the RIGHT/STRAIGHT command. Its front hit actor 1, which was in the adjacent left lane; the hard braking also got the ego rear-ended.
- lead_vehicle_hybrid_optuna_r2_005: turned_into_actor, policy at fault: yes. On a clear multi-lane highway with the lead car 37+ m ahead, the ego braked for no apparent reason, slowing from about 17 to 10 m/s while the recorded human drove on. It then steered left, and its front hit actor 1 in the adjacent left lane, which by then was just ahead of the ego. The ego was also rear-ended after its unneeded braking.
- lead_vehicle_hybrid_optuna_r2_015: turned_into_actor, policy at fault: yes. On a straight, clear highway, the policy braked for no reason, from 17 to 10 m/s, even though the closest vehicle ahead was 37 to 50 m away. That dropped the ego about 8 m behind its recorded position, and actor 1 in the lane to the left moved up alongside it. At the same time the ego drifted left toward the lane line, and its front-left corner hit the rear-right of actor 1 (the later rear contact on the ego probably came from the braking).
- lead_vehicle_hybrid_optuna_r2_016: turned_into_actor, policy at fault: yes. After handoff on a straight multi-lane highway, the ego braked hard for no clear reason (17 → 9.7 m/s with a clear lane ahead) and drifted left out of its lane. Its front-left corner hit actor 1, the car just ahead in the adjacent left lane, while the recorded human trajectory stayed in its lane and went on ahead.
- lead_vehicle_hybrid_optuna_r2_040: no_brake_for_lead, policy at fault: unclear. The ego was following the recorded human path in heavy, slow highway traffic. It closed steadily on the pickup ahead in its lane (actor 6): the gap fell from 15 m to 6.3 m at handoff (4.7 s). Only 0.5 s after taking over, the policy hit the pickup's rear at 5.2 s. In that time it braked from 6.5 to 4.9 m/s, which was not enough. The ego was also rear-ended at some point.
- lead_vehicle_hybrid_optuna_r2_042: turned_into_actor, policy at fault: yes. On a wet multi-lane highway with a STRAIGHT command, the policy's planned path bent left. The ego drifted out of its lane, away from the recorded trajectory, and its front hit pickup 41, which was passing it in the left lane. The pickup was already alongside at 6.3 s, and the ego kept moving left into it instead of holding its lane.
- lead_vehicle_hybrid_optuna_r2_044: turned_into_actor, policy at fault: yes. On a multi-lane highway with a STRAIGHT (later RIGHT) command, the policy's plan veered left toward the adjacent left lane. Pickup 41 was coming up alongside in that lane, and at 7.3s the ego's front clipped its rear quarter while the ego drifted over at about 4.4 m/s.
- lead_vehicle_hybrid_optuna_r2_045: no_brake_for_lead, policy at fault: unclear. Going straight on a highway, the ego closed on a slower pickup (actor 5) in its lane, from a 15 m gap to 6.3 m by handoff at 4.7 s, while holding about 6.8 m/s. The policy braked hard after taking over (6.5 to 4.9 m/s), but it had only 0.5 s and hit the pickup's rear at 5.2 s.
- lead_vehicle_hybrid_optuna_r2_046: no_brake_for_lead, policy at fault: unclear. The ego was going straight in a congested lane at about 6.8 m/s and closing on a slower blue pickup ahead (actor 5) at roughly 3.5 m/s. The policy took over at 4.7 s with only about 6 m of gap. It braked to 4.9 m/s, but its front hit the pickup 0.5 s later, at 5.2 s. The ego was still exactly on the recorded human path (0.0 m off), and the reported gap was 4.9 m even at contact, so the short takeover window and a possible mismatch between the pickup's recorded size or behaviour and the human drive make it unclear how much of this is the policy's fault.

## Every setting

- S1: 023b7fcc at actor_time_shift_s -0.5, actor_speed_scale 1.25, planner_delay_us 100000: 0/3 failed, rate 0%-47% (90%) (lead_vehicle_hybrid_optuna_r2_021, lead_vehicle_hybrid_optuna_r2_022, lead_vehicle_hybrid_optuna_r2_023)
- S2: 023b7fcc at actor_time_shift_s 1.5, actor_speed_scale 1, planner_delay_us 100000: 0/3 failed, rate 0%-47% (90%) (lead_vehicle_hybrid_optuna_r2_032, lead_vehicle_hybrid_optuna_r2_036, lead_vehicle_hybrid_optuna_r2_049)
- S3: 096988dd at actor_time_shift_s -1.5, actor_speed_scale 0.5, planner_delay_us 50000: 0/3 failed, rate 0%-47% (90%) (lead_vehicle_hybrid_optuna_r2_003, lead_vehicle_hybrid_optuna_r2_008, lead_vehicle_hybrid_optuna_r2_009)
- S4: 096988dd at actor_time_shift_s -1, actor_speed_scale 0.75, planner_delay_us 100000: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_hybrid_optuna_r2_027)
- S5: 096988dd at actor_time_shift_s 0.5, actor_speed_scale 1.25, planner_delay_us 0: 2/3 failed, rate 25%-92% (90%) (lead_vehicle_hybrid_optuna_r2_042, lead_vehicle_hybrid_optuna_r2_043, lead_vehicle_hybrid_optuna_r2_044)
- S6: 096988dd at actor_time_shift_s 2, actor_speed_scale 1, planner_delay_us 100000: 0/2 failed, rate 0%-58% (90%) (lead_vehicle_hybrid_optuna_r2_028, lead_vehicle_hybrid_optuna_r2_034)
- S7: 09a95ffa at actor_time_shift_s -1, actor_speed_scale 1, planner_delay_us 150000: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_hybrid_optuna_r2_029_a2)
- S8: 09a95ffa at actor_time_shift_s 1.5, actor_speed_scale 0.75, planner_delay_us 50000: 0/4 failed, rate 0%-40% (90%) (lead_vehicle_hybrid_optuna_r2_014, lead_vehicle_hybrid_optuna_r2_019, lead_vehicle_hybrid_optuna_r2_024, lead_vehicle_hybrid_optuna_r2_038)
- S9: 0cf6368d at actor_time_shift_s -1, actor_speed_scale 1.25, planner_delay_us 100000: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_hybrid_optuna_r2_033)
- S10: 0cf6368d at actor_time_shift_s -0.5, actor_speed_scale 1, planner_delay_us 50000: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_hybrid_optuna_r2_004)
- S11: 0cf6368d at actor_time_shift_s 1, actor_speed_scale 1.25, planner_delay_us 0: 0/3 failed, rate 0%-47% (90%) (lead_vehicle_hybrid_optuna_r2_001, lead_vehicle_hybrid_optuna_r2_010, lead_vehicle_hybrid_optuna_r2_011)
- S12: 0dbb91dd at actor_time_shift_s -1, actor_speed_scale 1, planner_delay_us 200000: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_hybrid_optuna_r2_006)
- S13: 0dbb91dd at actor_time_shift_s -1, actor_speed_scale 1.5, planner_delay_us 100000: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_hybrid_optuna_r2_007)
- S14: 0dbb91dd at actor_time_shift_s 0.5, actor_speed_scale 0.5, planner_delay_us 0: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_hybrid_optuna_r2_035)
- S15: 0e899dd3 at actor_time_shift_s -1.5, actor_speed_scale 1, planner_delay_us 0: 0/4 failed, rate 0%-40% (90%) (lead_vehicle_hybrid_optuna_r2_013, lead_vehicle_hybrid_optuna_r2_017, lead_vehicle_hybrid_optuna_r2_018, lead_vehicle_hybrid_optuna_r2_039)
- S16: 0e899dd3 at actor_time_shift_s -1, actor_speed_scale 0.5, planner_delay_us 100000: 3/3 failed, rate 53%-100% (90%) (lead_vehicle_hybrid_optuna_r2_040, lead_vehicle_hybrid_optuna_r2_045, lead_vehicle_hybrid_optuna_r2_046)
- S17: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.25, planner_delay_us 150000: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_hybrid_optuna_r2_026)
- S18: 0e899dd3 at actor_time_shift_s 0.5, actor_speed_scale 2, planner_delay_us 100000: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_hybrid_optuna_r2_030)
- S19: 12855a41 at actor_time_shift_s 0, actor_speed_scale 1, planner_delay_us 0: 0/3 failed, rate 0%-47% (90%) (lead_vehicle_hybrid_optuna_r2_012, lead_vehicle_hybrid_optuna_r2_020, lead_vehicle_hybrid_optuna_r2_025)
- S20: 12855a41 at actor_time_shift_s 1, actor_speed_scale 1, planner_delay_us 100000: 0/2 failed, rate 0%-58% (90%) (lead_vehicle_hybrid_optuna_r2_031, lead_vehicle_hybrid_optuna_r2_037)
- S21: 12855a41 at actor_time_shift_s 2, actor_speed_scale 1.25, planner_delay_us 200000: 0/3 failed, rate 0%-47% (90%) (lead_vehicle_hybrid_optuna_r2_041, lead_vehicle_hybrid_optuna_r2_047, lead_vehicle_hybrid_optuna_r2_048)
- S22: 19f339ba at actor_time_shift_s -1, actor_speed_scale 1, planner_delay_us 100000: 3/3 failed, rate 53%-100% (90%) (lead_vehicle_hybrid_optuna_r2_005, lead_vehicle_hybrid_optuna_r2_015, lead_vehicle_hybrid_optuna_r2_016)
- S23: 19f339ba at actor_time_shift_s 0.5, actor_speed_scale 1.25, planner_delay_us 0: 1/1 failed, rate 27%-100% (90%) (lead_vehicle_hybrid_optuna_r2_002)

## Not kept by the gate

- lead_vehicle_hybrid_optuna_r2_029: not kept: RE-RUN

## Provenance

Plan: `plan.json` (rationale: Scene choice: all eight scenes are tagged lead_vehicle, have an identified lead car, did not fail in the earlier run at 0 delay, and the ego drove far enough (6 to 19 m/s, about 35 to 130 m) to actually close on the car ahead. Several already came very close (0dbb91dd 0.23 m, 19f339ba 0.03 m, 12855a41 0.08 m, 096988dd and 023b7fcc 0.0 m), so they are likely to tip into failure. I left out lead_vehicle scenes that already fail at baseline, because they cannot show that the retiming caused the failure. I also left out scenes where the ego barely moved (for example 0fa7060f, 15dd433e, 0ac02819, 10d64934) and tagged scenes with no identified lead car (166fe701, 1bccdc21, 0ce02937, 1a5da90a).

Retiming: traffic is replay, as the brief asks, so the lead car follows its recorded path while being retimed. Only the lead car is retimed in each scene (via retime_tracks), not every car. That keeps the failures about the car ahead rather than about crossing traffic being shifted. 0cf6368d's lead car is also its cut-in car, so a failure there may be a cut-in rather than a pure braking case.

Goal: top_k with k=5, one setting per scene, and each setting's failure rate surely above 0.5. This matches 'the 5 most challenging cases, each on a different scene, confirmed by repeats'. The plan is 7 rounds of 7 runs (49, close to the brief's 50 and within the 60 cap), so the proposer can screen broadly and then repeat.

Limits:
(1) Budget. Confirming a rate above 0.5 at 90% takes about 4 to 5 failures per setting, so 5 confirmed cases need roughly 25 runs or more. That leaves little room for screening, and the study may end with fewer than 5 confirmed.
(2) Failure is any front or side collision or leaving the road. The check cannot tell a rear-end from other contact, and near misses are only a soft ranking for the proposer, not part of the goal.
(3) The 200 ms delay cap is given to the proposer as an instruction. The knob itself allows up to 400 ms, so the code does not enforce the cap.
(4) Under replay the lead car never reacts to the ego, and changing its speed stretches its recorded braking profile rather than making a new braking event.). Report written by claude-opus-5-5 from `results` in 24 s; every count above is computed from the queue, not written by the model.

50 of 50 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
