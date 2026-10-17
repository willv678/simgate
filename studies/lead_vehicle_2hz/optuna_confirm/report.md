# In lead-vehicle scenes, which timing shifts and speed scalings of the recorded lead car make VaVAM run into it? Find the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `optuna_confirm`: 49 kept runs on 8 scenes, varying actor_time_shift_s, actor_speed_scale; 2 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 0 of 5 challenging settings confirmed, after 7 rounds.

## Answer

No timing shift or speed scaling was confirmed to make VaVAM rear-end the lead car at 2 Hz planning. None of the 5 challenging cases was confirmed, so the goal was not met. Two settings failed: 12855a41 at +2 s, 1.0x (S20) and 19f339ba at +2 s, 0.75x (S26). Even these were not rear-ends. In every failure the policy drifted left out of its lane and hit a car in the next lane, and triage puts the fault on the policy, not on rendering. S20 failed in about half of its repeats, but its range runs from well below 0.5 to well above it, so it is not confirmed. S26 rests on a single run, which is a hint, not a rate. Most other settings got only one or two runs, so the study cannot say they are safe.

## Findings

- No setting was confirmed as failing in most runs, and no kept run on any scene rear-ended the retimed lead car.
  - S1: 023b7fcc at actor_time_shift_s -0.5, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_optuna_confirm_026)
  - S2: 023b7fcc at actor_time_shift_s 1.5, actor_speed_scale 1.0: 0/3 failed, rate 0%-47% (90%) (lead_vehicle_2hz_optuna_confirm_002, lead_vehicle_2hz_optuna_confirm_009, lead_vehicle_2hz_optuna_confirm_015_a2)
  - S3: 023b7fcc at actor_time_shift_s 2.0, actor_speed_scale 0.5: 0/6 failed, rate 0%-31% (90%) (lead_vehicle_2hz_optuna_confirm_020, lead_vehicle_2hz_optuna_confirm_022, lead_vehicle_2hz_optuna_confirm_025, lead_vehicle_2hz_optuna_confirm_030, lead_vehicle_2hz_optuna_confirm_038, lead_vehicle_2hz_optuna_confirm_045)
  - S4: 023b7fcc at actor_time_shift_s 2.0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_optuna_confirm_035)
  - S5: 096988dd at actor_time_shift_s -1.5, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_optuna_confirm_027)
  - S6: 096988dd at actor_time_shift_s 1.0, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (lead_vehicle_2hz_optuna_confirm_004_a2, lead_vehicle_2hz_optuna_confirm_017)
  - S7: 09a95ffa at actor_time_shift_s -0.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_optuna_confirm_014)
  - S8: 09a95ffa at actor_time_shift_s 1.5, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_optuna_confirm_021)
  - S9: 0cf6368d at actor_time_shift_s -0.5, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_optuna_confirm_005)
  - S10: 0cf6368d at actor_time_shift_s -0.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_optuna_confirm_012)
  - S11: 0cf6368d at actor_time_shift_s 2.0, actor_speed_scale 2.0: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_optuna_confirm_003)
  - S12: 0dbb91dd at actor_time_shift_s 0.0, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_optuna_confirm_013)
  - S13: 0dbb91dd at actor_time_shift_s 2.0, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_optuna_confirm_032)
  - S14: 0e899dd3 at actor_time_shift_s -2.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_optuna_confirm_001)
  - S15: 0e899dd3 at actor_time_shift_s 0.5, actor_speed_scale 2.0: 0/2 failed, rate 0%-58% (90%) (lead_vehicle_2hz_optuna_confirm_006, lead_vehicle_2hz_optuna_confirm_010)
  - S16: 12855a41 at actor_time_shift_s -1.0, actor_speed_scale 0.75: 0/2 failed, rate 0%-58% (90%) (lead_vehicle_2hz_optuna_confirm_018, lead_vehicle_2hz_optuna_confirm_024)
  - S17: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 0.5: 0/2 failed, rate 0%-58% (90%) (lead_vehicle_2hz_optuna_confirm_007, lead_vehicle_2hz_optuna_confirm_008)
  - S18: 12855a41 at actor_time_shift_s 0.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_optuna_confirm_042)
  - S19: 12855a41 at actor_time_shift_s 1.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_optuna_confirm_019)
  - S20: 12855a41 at actor_time_shift_s 2.0, actor_speed_scale 1.0: 3/6 failed, rate 22%-78% (90%) (lead_vehicle_2hz_optuna_confirm_028, lead_vehicle_2hz_optuna_confirm_029, lead_vehicle_2hz_optuna_confirm_033, lead_vehicle_2hz_optuna_confirm_036, lead_vehicle_2hz_optuna_confirm_039, lead_vehicle_2hz_optuna_confirm_043)
  - S21: 12855a41 at actor_time_shift_s 2.0, actor_speed_scale 2.0: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_optuna_confirm_040)
  - S22: 19f339ba at actor_time_shift_s -1.0, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_optuna_confirm_046)
  - S23: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.5: 0/4 failed, rate 0%-40% (90%) (lead_vehicle_2hz_optuna_confirm_011, lead_vehicle_2hz_optuna_confirm_016, lead_vehicle_2hz_optuna_confirm_023, lead_vehicle_2hz_optuna_confirm_031)
  - S24: 19f339ba at actor_time_shift_s 1.0, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_optuna_confirm_047)
  - S25: 19f339ba at actor_time_shift_s 2.0, actor_speed_scale 0.5: 0/4 failed, rate 0%-40% (90%) (lead_vehicle_2hz_optuna_confirm_034, lead_vehicle_2hz_optuna_confirm_037, lead_vehicle_2hz_optuna_confirm_044, lead_vehicle_2hz_optuna_confirm_048)
  - S26: 19f339ba at actor_time_shift_s 2.0, actor_speed_scale 0.75: 1/1 failed, rate 27%-100% (90%) (lead_vehicle_2hz_optuna_confirm_049)
  - S27: 19f339ba at actor_time_shift_s 2.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_optuna_confirm_041)
- The strongest candidate is 12855a41 with the lead car 2 s later at its recorded speed. About half of its repeats failed, and the range still includes rates below 0.5. Every failure there was the same side collision: with a RIGHT command, the ego drifted about 2 m left into the next lane and sideswiped actor 51 as it came up from behind. That is a lane-keeping failure, not a braking failure. No failure there was flagged as a possible rendering artifact.
  - S20: 12855a41 at actor_time_shift_s 2.0, actor_speed_scale 1.0: 3/6 failed, rate 22%-78% (90%) (lead_vehicle_2hz_optuna_confirm_028, lead_vehicle_2hz_optuna_confirm_029, lead_vehicle_2hz_optuna_confirm_033, lead_vehicle_2hz_optuna_confirm_036, lead_vehicle_2hz_optuna_confirm_039, lead_vehicle_2hz_optuna_confirm_043)
- On 19f339ba, the lead car 2 s later at 0.75x speed failed in its only run. After the handoff the policy braked hard for no clear reason, drifted left, and hit a car ahead in the left lane, and something hit the ego from behind. This is a single run, a hint only. Nearby settings on the same scene (+2 s at 0.5x, and 0 s at 1.5x) passed every repeat.
  - S26: 19f339ba at actor_time_shift_s 2.0, actor_speed_scale 0.75: 1/1 failed, rate 27%-100% (90%) (lead_vehicle_2hz_optuna_confirm_049)
  - S25: 19f339ba at actor_time_shift_s 2.0, actor_speed_scale 0.5: 0/4 failed, rate 0%-40% (90%) (lead_vehicle_2hz_optuna_confirm_034, lead_vehicle_2hz_optuna_confirm_037, lead_vehicle_2hz_optuna_confirm_044, lead_vehicle_2hz_optuna_confirm_048)
  - S23: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.5: 0/4 failed, rate 0%-40% (90%) (lead_vehicle_2hz_optuna_confirm_011, lead_vehicle_2hz_optuna_confirm_016, lead_vehicle_2hz_optuna_confirm_023, lead_vehicle_2hz_optuna_confirm_031)
- Some settings passed every repeat, enough to rule out a failure rate of 0.5 or more: 023b7fcc at +2 s and 0.5x, and at +1.5 s and 1.0x, and 19f339ba at +2 s and 0.5x, and at 0 s and 1.5x. This holds even though several of them scored as near misses.
  - S3: 023b7fcc at actor_time_shift_s 2.0, actor_speed_scale 0.5: 0/6 failed, rate 0%-31% (90%) (lead_vehicle_2hz_optuna_confirm_020, lead_vehicle_2hz_optuna_confirm_022, lead_vehicle_2hz_optuna_confirm_025, lead_vehicle_2hz_optuna_confirm_030, lead_vehicle_2hz_optuna_confirm_038, lead_vehicle_2hz_optuna_confirm_045)
  - S2: 023b7fcc at actor_time_shift_s 1.5, actor_speed_scale 1.0: 0/3 failed, rate 0%-47% (90%) (lead_vehicle_2hz_optuna_confirm_002, lead_vehicle_2hz_optuna_confirm_009, lead_vehicle_2hz_optuna_confirm_015_a2)
  - S25: 19f339ba at actor_time_shift_s 2.0, actor_speed_scale 0.5: 0/4 failed, rate 0%-40% (90%) (lead_vehicle_2hz_optuna_confirm_034, lead_vehicle_2hz_optuna_confirm_037, lead_vehicle_2hz_optuna_confirm_044, lead_vehicle_2hz_optuna_confirm_048)
  - S23: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.5: 0/4 failed, rate 0%-40% (90%) (lead_vehicle_2hz_optuna_confirm_011, lead_vehicle_2hz_optuna_confirm_016, lead_vehicle_2hz_optuna_confirm_023, lead_vehicle_2hz_optuna_confirm_031)
- Six scenes had no failure at any setting tried: 023b7fcc, 096988dd, 09a95ffa, 0cf6368d, 0dbb91dd and 0e899dd3. Apart from 023b7fcc, those scenes got only one or two runs per setting, which cannot rule out high failure rates.
  - S1: 023b7fcc at actor_time_shift_s -0.5, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_optuna_confirm_026)
  - S4: 023b7fcc at actor_time_shift_s 2.0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_optuna_confirm_035)
  - S5: 096988dd at actor_time_shift_s -1.5, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_optuna_confirm_027)
  - S6: 096988dd at actor_time_shift_s 1.0, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (lead_vehicle_2hz_optuna_confirm_004_a2, lead_vehicle_2hz_optuna_confirm_017)
  - S7: 09a95ffa at actor_time_shift_s -0.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_optuna_confirm_014)
  - S8: 09a95ffa at actor_time_shift_s 1.5, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_optuna_confirm_021)
  - S9: 0cf6368d at actor_time_shift_s -0.5, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_optuna_confirm_005)
  - S10: 0cf6368d at actor_time_shift_s -0.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_optuna_confirm_012)
  - S11: 0cf6368d at actor_time_shift_s 2.0, actor_speed_scale 2.0: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_optuna_confirm_003)
  - S12: 0dbb91dd at actor_time_shift_s 0.0, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_optuna_confirm_013)
  - S13: 0dbb91dd at actor_time_shift_s 2.0, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_optuna_confirm_032)
  - S14: 0e899dd3 at actor_time_shift_s -2.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_optuna_confirm_001)
  - S15: 0e899dd3 at actor_time_shift_s 0.5, actor_speed_scale 2.0: 0/2 failed, rate 0%-58% (90%) (lead_vehicle_2hz_optuna_confirm_006, lead_vehicle_2hz_optuna_confirm_010)
- Both failing settings delay the lead car by the full +2 s. That points to delayed lead timing as where the policy struggles, but the failures came from lateral drift, so the link to the lead car is indirect.
  - S20: 12855a41 at actor_time_shift_s 2.0, actor_speed_scale 1.0: 3/6 failed, rate 22%-78% (90%) (lead_vehicle_2hz_optuna_confirm_028, lead_vehicle_2hz_optuna_confirm_029, lead_vehicle_2hz_optuna_confirm_033, lead_vehicle_2hz_optuna_confirm_036, lead_vehicle_2hz_optuna_confirm_039, lead_vehicle_2hz_optuna_confirm_043)
  - S26: 19f339ba at actor_time_shift_s 2.0, actor_speed_scale 0.75: 1/1 failed, rate 27%-100% (90%) (lead_vehicle_2hz_optuna_confirm_049)

## Open

- Whether 12855a41 at +2 s, 1.0x (S20) fails more than half the time. About six more repeats would separate its range from 0.5.
- Whether 19f339ba at +2 s, 0.75x (S26) repeats. About four more runs would confirm or drop it. Also unclear is whether the unexplained hard braking and left drift come from the retiming or from the policy alone.
- Whether the S20 failures depend on the lead car's retiming at all. They come from left drift into actor 51's lane. A baseline run at 0 s, 1.0x, or a run retiming only actor 51, would show whether the lead car matters.
- Near misses that never got repeats: 19f339ba at +1 s, 0.5x (S24) and 023b7fcc at -0.5 s, 0.75x (S1). Each was run once and scored high on criticality.
- Scenes 0dbb91dd, 09a95ffa, 0cf6368d, 096988dd and 0e899dd3 were barely screened, and 0dbb91dd's runs scored zero criticality. These scenes cannot yet be called hard or easy.
- How these results compare with the 10 Hz lead_vehicle study. This study gives no 10 Hz data, so whether planning at 2 Hz changes how often or how the policy fails is not settled here.
- Two runs were re-run, not kept, and are not evidence: 096988dd at +1 s, 1.25x and 023b7fcc at +1.5 s, 1.0x.

## Why the runs failed (triage from the video and log)

turned_into_actor 4

- lead_vehicle_2hz_optuna_confirm_033: turned_into_actor, policy at fault: yes. In slow highway traffic with a RIGHT command, the ego drifted left out of the recorded lane, ending about 2.1 m left of the human's path, and into the adjacent left lane. Actor 51 was coming up from behind on the left, and the ego's side hit it at 10.7 s.
- lead_vehicle_2hz_optuna_confirm_039: turned_into_actor, policy at fault: yes. The route command was RIGHT, but in slow highway traffic the ego drifted left out of its recorded lane, about 2 m off the human path, into the next lane. There it sideswiped actor 51, which was coming up beside it from behind on the left. The metrics log this as a lateral collision.
- lead_vehicle_2hz_optuna_confirm_043: turned_into_actor, policy at fault: yes. In slow highway traffic with a RIGHT command, the ego drifted about 2 m left of the recorded path, which ran toward the lane on the right. It ended up straddling the lane line into the left lane. Actor 51 came up from behind in that left lane, and the ego's front-left corner clipped it as it drew alongside at about 3.6 m/s.
- lead_vehicle_2hz_optuna_confirm_049: turned_into_actor, policy at fault: yes. After the 4.6s handoff on a straight multi-lane highway, the policy braked hard (17 to 9.4 m/s) for no clear reason and drifted left, away from the recorded path, which stayed straight or bore slightly right. At 7.1s its front-left corner hit actor 1, a car just ahead of it in the left lane. Something also hit the ego's rear, probably because of the sudden braking.

## Every setting

- S1: 023b7fcc at actor_time_shift_s -0.5, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_optuna_confirm_026)
- S2: 023b7fcc at actor_time_shift_s 1.5, actor_speed_scale 1.0: 0/3 failed, rate 0%-47% (90%) (lead_vehicle_2hz_optuna_confirm_002, lead_vehicle_2hz_optuna_confirm_009, lead_vehicle_2hz_optuna_confirm_015_a2)
- S3: 023b7fcc at actor_time_shift_s 2.0, actor_speed_scale 0.5: 0/6 failed, rate 0%-31% (90%) (lead_vehicle_2hz_optuna_confirm_020, lead_vehicle_2hz_optuna_confirm_022, lead_vehicle_2hz_optuna_confirm_025, lead_vehicle_2hz_optuna_confirm_030, lead_vehicle_2hz_optuna_confirm_038, lead_vehicle_2hz_optuna_confirm_045)
- S4: 023b7fcc at actor_time_shift_s 2.0, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_optuna_confirm_035)
- S5: 096988dd at actor_time_shift_s -1.5, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_optuna_confirm_027)
- S6: 096988dd at actor_time_shift_s 1.0, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (lead_vehicle_2hz_optuna_confirm_004_a2, lead_vehicle_2hz_optuna_confirm_017)
- S7: 09a95ffa at actor_time_shift_s -0.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_optuna_confirm_014)
- S8: 09a95ffa at actor_time_shift_s 1.5, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_optuna_confirm_021)
- S9: 0cf6368d at actor_time_shift_s -0.5, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_optuna_confirm_005)
- S10: 0cf6368d at actor_time_shift_s -0.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_optuna_confirm_012)
- S11: 0cf6368d at actor_time_shift_s 2.0, actor_speed_scale 2.0: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_optuna_confirm_003)
- S12: 0dbb91dd at actor_time_shift_s 0.0, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_optuna_confirm_013)
- S13: 0dbb91dd at actor_time_shift_s 2.0, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_optuna_confirm_032)
- S14: 0e899dd3 at actor_time_shift_s -2.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_optuna_confirm_001)
- S15: 0e899dd3 at actor_time_shift_s 0.5, actor_speed_scale 2.0: 0/2 failed, rate 0%-58% (90%) (lead_vehicle_2hz_optuna_confirm_006, lead_vehicle_2hz_optuna_confirm_010)
- S16: 12855a41 at actor_time_shift_s -1.0, actor_speed_scale 0.75: 0/2 failed, rate 0%-58% (90%) (lead_vehicle_2hz_optuna_confirm_018, lead_vehicle_2hz_optuna_confirm_024)
- S17: 12855a41 at actor_time_shift_s -0.5, actor_speed_scale 0.5: 0/2 failed, rate 0%-58% (90%) (lead_vehicle_2hz_optuna_confirm_007, lead_vehicle_2hz_optuna_confirm_008)
- S18: 12855a41 at actor_time_shift_s 0.5, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_optuna_confirm_042)
- S19: 12855a41 at actor_time_shift_s 1.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_optuna_confirm_019)
- S20: 12855a41 at actor_time_shift_s 2.0, actor_speed_scale 1.0: 3/6 failed, rate 22%-78% (90%) (lead_vehicle_2hz_optuna_confirm_028, lead_vehicle_2hz_optuna_confirm_029, lead_vehicle_2hz_optuna_confirm_033, lead_vehicle_2hz_optuna_confirm_036, lead_vehicle_2hz_optuna_confirm_039, lead_vehicle_2hz_optuna_confirm_043)
- S21: 12855a41 at actor_time_shift_s 2.0, actor_speed_scale 2.0: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_optuna_confirm_040)
- S22: 19f339ba at actor_time_shift_s -1.0, actor_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_optuna_confirm_046)
- S23: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.5: 0/4 failed, rate 0%-40% (90%) (lead_vehicle_2hz_optuna_confirm_011, lead_vehicle_2hz_optuna_confirm_016, lead_vehicle_2hz_optuna_confirm_023, lead_vehicle_2hz_optuna_confirm_031)
- S24: 19f339ba at actor_time_shift_s 1.0, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_optuna_confirm_047)
- S25: 19f339ba at actor_time_shift_s 2.0, actor_speed_scale 0.5: 0/4 failed, rate 0%-40% (90%) (lead_vehicle_2hz_optuna_confirm_034, lead_vehicle_2hz_optuna_confirm_037, lead_vehicle_2hz_optuna_confirm_044, lead_vehicle_2hz_optuna_confirm_048)
- S26: 19f339ba at actor_time_shift_s 2.0, actor_speed_scale 0.75: 1/1 failed, rate 27%-100% (90%) (lead_vehicle_2hz_optuna_confirm_049)
- S27: 19f339ba at actor_time_shift_s 2.0, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (lead_vehicle_2hz_optuna_confirm_041)

## Not kept by the gate

- lead_vehicle_2hz_optuna_confirm_004: not kept: RE-RUN
- lead_vehicle_2hz_optuna_confirm_015: not kept: RE-RUN

## Provenance

Plan: `plan.json` (rationale: Copied from studies/lead_vehicle/plan.json (10 Hz) with the policy planning every 500 ms, so the method comparison can be repeated at 2 Hz. Scene choice: all eight scenes are tagged lead_vehicle, have an identified lead car, did not fail in the earlier run at 0 delay, and the ego drove far enough (6 to 19 m/s, about 35 to 130 m) to actually close on the car ahead. Several already came very close (0dbb91dd 0.23 m, 19f339ba 0.03 m, 12855a41 0.08 m, 096988dd and 023b7fcc 0.0 m), so they are likely to tip into failure. I left out lead_vehicle scenes that already fail at baseline, because they cannot show that the retiming caused the failure. I also left out scenes where the ego barely moved (for example 0fa7060f, 15dd433e, 0ac02819, 10d64934) and tagged scenes with no identified lead car (166fe701, 1bccdc21, 0ce02937, 1a5da90a).

Retiming: traffic is replay, as the brief asks, so the lead car follows its recorded path while being retimed. Only the lead car is retimed in each scene (via retime_tracks), not every car. That keeps the failures about the car ahead rather than about crossing traffic being shifted. 0cf6368d's lead car is also its cut-in car, so a failure there may be a cut-in rather than a pure braking case.

Goal: top_k with k=5, one setting per scene, and each setting's failure rate surely above 0.5. This matches 'the 5 most challenging cases, each on a different scene, confirmed by repeats'. The plan is 7 rounds of 7 runs (49, close to the brief's 50 and within the 60 cap), so the proposer can screen broadly and then repeat.

Limits:
(1) Budget. Confirming a rate above 0.5 at 90% takes about 4 to 5 failures per setting, so 5 confirmed cases need roughly 25 runs or more. That leaves little room for screening, and the study may end with fewer than 5 confirmed.
(2) Failure is any front or side collision or leaving the road. The check cannot tell a rear-end from other contact, and near misses are only a soft ranking for the proposer, not part of the goal.
(3) The 200 ms delay cap is given to the proposer as an instruction. The knob itself allows up to 400 ms, so the code does not enforce the cap.
(4) Under replay the lead car never reacts to the ego, and changing its speed stretches its recorded braking profile rather than making a new braking event.). Report written by claude-opus-5-5 from `results` in 22 s; every count above is computed from the queue, not written by the model.

51 of 51 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
