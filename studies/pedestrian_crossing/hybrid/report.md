# Which pedestrian step-out timings (±2 s) and walking speeds (0.5x to 2x) make VaVAM hit the pedestrian or leave the road in pedestrian-crossing scenes, with the other traffic replayed as recorded? Find the 5 hardest cases, each on a different scene.

Study `hybrid`: 49 kept runs on 6 scenes, varying actor_time_shift_s, actor_speed_scale; 2 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 0 of 5 challenging settings confirmed, after 7 rounds.

## Answer

No timing or speed tried made VaVAM hit a pedestrian or leave the road. Every kept run on all six scenes passed, so none of the five cases was confirmed and the goal was not met. The two settings repeated most, 0e002edd at 0 s / 1.25x and 13a9767e at +0.5 s / 1.25x, are the strongest evidence. Their 90% ranges rule out failing more often than not at those settings. Every other setting has only one or two runs. That is a hint that the policy copes, not a measured rate. Large parts of the range were barely tested: half speed, double speed, and shifts beyond ±1 s on most scenes. So the study cannot say that VaVAM handles every timing in scope. If near misses are ranked instead, 13a9767e had the highest criticality across its settings, followed by 0e002edd.

## Findings

- No kept run at any setting ended in a collision or in leaving the road, so the triage has no failures to explain and no challenging case was confirmed.
  - S1: 095cf563 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_011)
  - S2: 095cf563 at actor_time_shift_s 0, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_047)
  - S3: 095cf563 at actor_time_shift_s 0, actor_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (pedestrian_crossing_hybrid_040, pedestrian_crossing_hybrid_048)
  - S4: 095cf563 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/3 failed, rate 0%-47% (90%) (pedestrian_crossing_hybrid_005, pedestrian_crossing_hybrid_026, pedestrian_crossing_hybrid_032)
  - S5: 095cf563 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_010)
  - S6: 095cf563 at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_018)
  - S7: 0b10bce8 at actor_time_shift_s -1, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_042)
  - S8: 0b10bce8 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_028)
  - S9: 0b10bce8 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_003)
  - S10: 0b10bce8 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_014)
  - S11: 0b10bce8 at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_021)
  - S12: 0e002edd at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_016)
  - S13: 0e002edd at actor_time_shift_s 0, actor_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_034)
  - S14: 0e002edd at actor_time_shift_s 0, actor_speed_scale 1.25: 0/6 failed, rate 0%-31% (90%) (pedestrian_crossing_hybrid_007, pedestrian_crossing_hybrid_001_a2, pedestrian_crossing_hybrid_025, pedestrian_crossing_hybrid_031_a2, pedestrian_crossing_hybrid_041, pedestrian_crossing_hybrid_049)
  - S15: 0e002edd at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_012)
  - S16: 0e002edd at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_015)
  - S17: 12a09194 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_004)
  - S18: 13a9767e at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_009)
  - S19: 13a9767e at actor_time_shift_s 0, actor_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_046)
  - S20: 13a9767e at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_006)
  - S21: 13a9767e at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_008)
  - S22: 13a9767e at actor_time_shift_s 0.5, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_045)
  - S23: 13a9767e at actor_time_shift_s 0.5, actor_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (pedestrian_crossing_hybrid_033, pedestrian_crossing_hybrid_043)
  - S24: 13a9767e at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/6 failed, rate 0%-31% (90%) (pedestrian_crossing_hybrid_017, pedestrian_crossing_hybrid_022, pedestrian_crossing_hybrid_029, pedestrian_crossing_hybrid_030, pedestrian_crossing_hybrid_036, pedestrian_crossing_hybrid_037)
  - S25: 13a9767e at actor_time_shift_s 0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_024)
  - S26: 13a9767e at actor_time_shift_s 1, actor_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_044)
  - S27: 13a9767e at actor_time_shift_s 1, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_023)
  - S28: 18f8dbd6 at actor_time_shift_s -2, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_038)
  - S29: 18f8dbd6 at actor_time_shift_s -1.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_035)
  - S30: 18f8dbd6 at actor_time_shift_s -1.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_039)
  - S31: 18f8dbd6 at actor_time_shift_s -1, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_027)
  - S32: 18f8dbd6 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_020)
  - S33: 18f8dbd6 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_002)
  - S34: 18f8dbd6 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_013)
  - S35: 18f8dbd6 at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_019)
- On 0e002edd (recorded closest approach 0.15 m), stepping out on time at 1.25x speed was repeated and never failed. Its range rules out a failure rate above one half there. Neighbouring shifts of ±0.5 s and speeds of 1x and 1.5x also passed, each in a single run.
  - S12: 0e002edd at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_016)
  - S13: 0e002edd at actor_time_shift_s 0, actor_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_034)
  - S14: 0e002edd at actor_time_shift_s 0, actor_speed_scale 1.25: 0/6 failed, rate 0%-31% (90%) (pedestrian_crossing_hybrid_007, pedestrian_crossing_hybrid_001_a2, pedestrian_crossing_hybrid_025, pedestrian_crossing_hybrid_031_a2, pedestrian_crossing_hybrid_041, pedestrian_crossing_hybrid_049)
  - S15: 0e002edd at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_012)
  - S16: 0e002edd at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_015)
- 13a9767e was the most critical scene: every setting there scored higher criticality than any setting on the other scenes, and the peak was at +0.5 s, 1.25x. Even so, repeats at that setting never failed. It is the best near-miss candidate, but it is not a failure case.
  - S18: 13a9767e at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_009)
  - S19: 13a9767e at actor_time_shift_s 0, actor_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_046)
  - S20: 13a9767e at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_006)
  - S21: 13a9767e at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_008)
  - S22: 13a9767e at actor_time_shift_s 0.5, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_045)
  - S23: 13a9767e at actor_time_shift_s 0.5, actor_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (pedestrian_crossing_hybrid_033, pedestrian_crossing_hybrid_043)
  - S24: 13a9767e at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/6 failed, rate 0%-31% (90%) (pedestrian_crossing_hybrid_017, pedestrian_crossing_hybrid_022, pedestrian_crossing_hybrid_029, pedestrian_crossing_hybrid_030, pedestrian_crossing_hybrid_036, pedestrian_crossing_hybrid_037)
  - S25: 13a9767e at actor_time_shift_s 0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_024)
  - S26: 13a9767e at actor_time_shift_s 1, actor_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_044)
  - S27: 13a9767e at actor_time_shift_s 1, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_023)
- On 18f8dbd6, stepping out anywhere from 2 s early to 0.5 s late, at 1.25x or 1.5x, gave the same criticality and no failures. Retiming pedestrian track 97 does not seem to change how the ego and pedestrian interact here.
  - S28: 18f8dbd6 at actor_time_shift_s -2, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_038)
  - S29: 18f8dbd6 at actor_time_shift_s -1.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_035)
  - S30: 18f8dbd6 at actor_time_shift_s -1.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_039)
  - S31: 18f8dbd6 at actor_time_shift_s -1, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_027)
  - S32: 18f8dbd6 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_020)
  - S33: 18f8dbd6 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_002)
  - S34: 18f8dbd6 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_013)
  - S35: 18f8dbd6 at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_019)
- On 0b10bce8, criticality was also the same at every shift and speed tried, with no failures. This fits the plan's concern that the ego barely moves in this scene, so the pedestrian's timing does not matter.
  - S7: 0b10bce8 at actor_time_shift_s -1, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_042)
  - S8: 0b10bce8 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_028)
  - S9: 0b10bce8 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_003)
  - S10: 0b10bce8 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_014)
  - S11: 0b10bce8 at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_021)
- 12a09194 got a single run with zero criticality. The pedestrian never came into conflict with the ego at the recorded timing, so the scene was effectively not tested.
  - S17: 12a09194 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_004)
- On 095cf563, where every person-class actor was retimed together, shifts of ±0.5 s and speeds from 0.75x to 1.5x caused no failures. Criticality stayed in a narrow band, so no setting stood out.
  - S1: 095cf563 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_011)
  - S2: 095cf563 at actor_time_shift_s 0, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_047)
  - S3: 095cf563 at actor_time_shift_s 0, actor_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (pedestrian_crossing_hybrid_040, pedestrian_crossing_hybrid_048)
  - S4: 095cf563 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/3 failed, rate 0%-47% (90%) (pedestrian_crossing_hybrid_005, pedestrian_crossing_hybrid_026, pedestrian_crossing_hybrid_032)
  - S5: 095cf563 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_010)
  - S6: 095cf563 at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_018)

## Open

- Extreme speeds were not tested: no run used 0.5x or 2x, and 0.75x was tried only on 095cf563 and 13a9767e. A few runs at 0.5x and 2x on 13a9767e and 0e002edd, the two most critical scenes, would show whether the extremes of the speed range create conflict.
- Large time shifts were tested only on 18f8dbd6, the only scene with shifts beyond ±1 s. Running ±1.5 s and ±2 s on 13a9767e, 0e002edd and 095cf563 would cover the rest of the timing range.
- On 18f8dbd6 and 0b10bce8, criticality did not move with any retiming. It should be checked whether the retimed pedestrian actually reaches the ego's path, or whether another track is the relevant one.
- 12a09194 had only one run, with zero criticality. Larger shifts are needed to bring its pedestrian into conflict before calling the scene robust.
- Most settings have only one run, so their ranges cannot rule out a failure rate above one half. Repeats are needed before any single-run setting can be called safe.
- The six scenes that failed at baseline were left out on purpose. The study therefore says nothing about whether pedestrian retiming makes those scenes worse or better under replayed traffic.
- The two not-kept runs on 0e002edd (marked for re-run) are not evidence. Their re-runs are among the kept runs at S14.

## Every setting

- S1: 095cf563 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_011)
- S2: 095cf563 at actor_time_shift_s 0, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_047)
- S3: 095cf563 at actor_time_shift_s 0, actor_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (pedestrian_crossing_hybrid_040, pedestrian_crossing_hybrid_048)
- S4: 095cf563 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/3 failed, rate 0%-47% (90%) (pedestrian_crossing_hybrid_005, pedestrian_crossing_hybrid_026, pedestrian_crossing_hybrid_032)
- S5: 095cf563 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_010)
- S6: 095cf563 at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_018)
- S7: 0b10bce8 at actor_time_shift_s -1, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_042)
- S8: 0b10bce8 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_028)
- S9: 0b10bce8 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_003)
- S10: 0b10bce8 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_014)
- S11: 0b10bce8 at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_021)
- S12: 0e002edd at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_016)
- S13: 0e002edd at actor_time_shift_s 0, actor_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_034)
- S14: 0e002edd at actor_time_shift_s 0, actor_speed_scale 1.25: 0/6 failed, rate 0%-31% (90%) (pedestrian_crossing_hybrid_007, pedestrian_crossing_hybrid_001_a2, pedestrian_crossing_hybrid_025, pedestrian_crossing_hybrid_031_a2, pedestrian_crossing_hybrid_041, pedestrian_crossing_hybrid_049)
- S15: 0e002edd at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_012)
- S16: 0e002edd at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_015)
- S17: 12a09194 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_004)
- S18: 13a9767e at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_009)
- S19: 13a9767e at actor_time_shift_s 0, actor_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_046)
- S20: 13a9767e at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_006)
- S21: 13a9767e at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_008)
- S22: 13a9767e at actor_time_shift_s 0.5, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_045)
- S23: 13a9767e at actor_time_shift_s 0.5, actor_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (pedestrian_crossing_hybrid_033, pedestrian_crossing_hybrid_043)
- S24: 13a9767e at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/6 failed, rate 0%-31% (90%) (pedestrian_crossing_hybrid_017, pedestrian_crossing_hybrid_022, pedestrian_crossing_hybrid_029, pedestrian_crossing_hybrid_030, pedestrian_crossing_hybrid_036, pedestrian_crossing_hybrid_037)
- S25: 13a9767e at actor_time_shift_s 0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_024)
- S26: 13a9767e at actor_time_shift_s 1, actor_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_044)
- S27: 13a9767e at actor_time_shift_s 1, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_023)
- S28: 18f8dbd6 at actor_time_shift_s -2, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_038)
- S29: 18f8dbd6 at actor_time_shift_s -1.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_035)
- S30: 18f8dbd6 at actor_time_shift_s -1.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_039)
- S31: 18f8dbd6 at actor_time_shift_s -1, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_027)
- S32: 18f8dbd6 at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_020)
- S33: 18f8dbd6 at actor_time_shift_s 0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_002)
- S34: 18f8dbd6 at actor_time_shift_s 0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_013)
- S35: 18f8dbd6 at actor_time_shift_s 0.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (pedestrian_crossing_hybrid_019)

## Not kept by the gate

- pedestrian_crossing_hybrid_001: not kept: RE-RUN
- pedestrian_crossing_hybrid_031: not kept: RE-RUN

## Provenance

Plan: `plan.json` (rationale: Scope: the brief asks for scenes tagged pedestrian_crossing, with recorded pedestrians retimed (class person), other traffic on replay (as in Euro NCAP-style scripted tests), and no delay or perception error.

Scene choice: I left out the six tagged scenes that already failed in the earlier run at 0 delay (048b974e, 07981e6a, 0caa8f1a, 0d4893f5, 18d28973, 1bbe02fc). A failure there would probably come from the scene itself, not from the pedestrian's timing, so it would rank as 'challenging' without answering the question. That leaves six candidates:
- Four have an identified pedestrian, and only that pedestrian is retimed:
  - 0e002edd: closest approach 0.15 m
  - 18f8dbd6: 0.9 m
  - 0b10bce8: 1.5 m, but the ego drove only 8.9 m, so it may sit nearly stopped
  - 12a09194: 11.5 m, so the pedestrian is far away and a shift may be needed to create conflict
- Two had near misses but no identified pedestrian, so their whole person class is retimed:
  - 095cf563: 0.17 m
  - 13a9767e: 0.12 m

Budget: 7 rounds of 7 runs (49 runs) gives the proposer room to adapt. With 90% ranges, confirming a rate above 0.5 takes about 4 to 5 failures per setting. Five confirmed cases therefore need about 25 runs, which leaves the rest for searching.

Limits:
- Six candidates for k=5 is tight. If two scenes turn out robust, or 095cf563 or 13a9767e turn out to have no person-class actor (their runs would then fail as invalid), the goal cannot be met. The study then runs its full budget and reports fewer than five confirmed cases, with near misses (closest approach) ranked next.
- The earlier baseline used CATK traffic, not replay, so baselines under replay may differ.
- The failure check does not say which actor was hit. A collision with a replayed vehicle counts the same as one with the pedestrian.
- Replayed traffic does not react to the ego, which differs from CATK.). Report written by claude-opus-5-5 from `results` in 21 s; every count above is computed from the queue, not written by the model.
