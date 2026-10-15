# In merge and cut-in scenes, which timings and speeds of the other cars make the VaVAM policy collide or leave the road? Find the 5 most challenging settings, each on a different scene and confirmed by repeats.

Study `hybrid_optuna_r4`: 54 kept runs on 9 scenes, varying actor_time_shift_s, actor_speed_scale; 1 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 1 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The study confirmed one of the five challenging cases it was looking for, so the goal was not met. Scene 023b7fcc with cars 0.5 s earlier and at 2x speed made the policy collide in every repeat, and its range sits above one half (S1). The policy is to blame and none of the failures look like simulator artifacts. In those runs the ego follows lead car 66 too closely and hits it instead of braking. It then steers left into the next lane and hits car 61. That is a following-and-swerve failure, and it's not clear a cut-in caused it. No other setting on the other eight scenes failed even once. Settings repeated three times stayed below one half. Settings run only once or twice are a hint, not a rate, so the study can't say whether the other scenes have a challenging case.

## Findings

- Scene 023b7fcc with cars 0.5 s earlier and at 2x speed is a confirmed challenging case: the ego failed in every repeat, and the failure rate is surely above one half.
  - S1: 023b7fcc at actor_time_shift_s -0.5, actor_speed_scale 2: 4/4 failed, rate 60%-100% (90%) (cut_in_merge_hybrid_optuna_r4_006, cut_in_merge_hybrid_optuna_r4_010, cut_in_merge_hybrid_optuna_r4_011, cut_in_merge_hybrid_optuna_r4_012)
- The 023b7fcc failures are the policy's fault and are not simulator artifacts. The ego follows lead car 66 too closely and hits it instead of braking (the triage records the first run as no braking for the lead). Then it leaves its path to the left and hits car 61 in the next lane.
  - S1: 023b7fcc at actor_time_shift_s -0.5, actor_speed_scale 2: 4/4 failed, rate 60%-100% (90%) (cut_in_merge_hybrid_optuna_r4_006, cut_in_merge_hybrid_optuna_r4_010, cut_in_merge_hybrid_optuna_r4_011, cut_in_merge_hybrid_optuna_r4_012)
- The setting that broke 023b7fcc (0.5 s earlier, 2x speed) caused no failures on five other scenes (054b5901, 096988dd, 09a95ffa, 0e899dd3, 1c45ce3a). The failure comes from that scene, not from the retiming alone. On 096988dd this was checked with repeats; on the other four it was tried only once.
  - S1: 023b7fcc at actor_time_shift_s -0.5, actor_speed_scale 2: 4/4 failed, rate 60%-100% (90%) (cut_in_merge_hybrid_optuna_r4_006, cut_in_merge_hybrid_optuna_r4_010, cut_in_merge_hybrid_optuna_r4_011, cut_in_merge_hybrid_optuna_r4_012)
  - S2: 054b5901 at actor_time_shift_s -0.5, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_026)
  - S6: 096988dd at actor_time_shift_s -0.5, actor_speed_scale 2: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_hybrid_optuna_r4_032, cut_in_merge_hybrid_optuna_r4_041, cut_in_merge_hybrid_optuna_r4_052)
  - S9: 09a95ffa at actor_time_shift_s -0.5, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_042)
  - S17: 0e899dd3 at actor_time_shift_s -0.5, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_023)
  - S32: 1c45ce3a at actor_time_shift_s -0.5, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_043)
- Settings repeated three times without a failure are unlikely to be challenging cases: their ranges stay below one half. These cover 096988dd (0.5 s earlier, 2x), 09a95ffa (nominal timing at 1.5x, and 0.5 s later at 2x), 0e899dd3 (1.5 s later, 0.5x), 12855a41 (1.5 s earlier, 2x), 19f339ba (0.5 s earlier, 1.25x) and 1c45ce3a (2 s earlier, 2x).
  - S6: 096988dd at actor_time_shift_s -0.5, actor_speed_scale 2: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_hybrid_optuna_r4_032, cut_in_merge_hybrid_optuna_r4_041, cut_in_merge_hybrid_optuna_r4_052)
  - S10: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.5: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_hybrid_optuna_r4_033, cut_in_merge_hybrid_optuna_r4_037, cut_in_merge_hybrid_optuna_r4_038)
  - S11: 09a95ffa at actor_time_shift_s 0.5, actor_speed_scale 2: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_hybrid_optuna_r4_024, cut_in_merge_hybrid_optuna_r4_028, cut_in_merge_hybrid_optuna_r4_029)
  - S20: 0e899dd3 at actor_time_shift_s 1.5, actor_speed_scale 0.5: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_hybrid_optuna_r4_005, cut_in_merge_hybrid_optuna_r4_013, cut_in_merge_hybrid_optuna_r4_014)
  - S23: 12855a41 at actor_time_shift_s -1.5, actor_speed_scale 2: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_hybrid_optuna_r4_002, cut_in_merge_hybrid_optuna_r4_015, cut_in_merge_hybrid_optuna_r4_020)
  - S27: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_hybrid_optuna_r4_034, cut_in_merge_hybrid_optuna_r4_039, cut_in_merge_hybrid_optuna_r4_040)
  - S30: 1c45ce3a at actor_time_shift_s -2, actor_speed_scale 2: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_hybrid_optuna_r4_004_a2, cut_in_merge_hybrid_optuna_r4_016, cut_in_merge_hybrid_optuna_r4_019)
- No failures came up on scenes 054b5901, 0cf6368d, 096988dd, 09a95ffa, 0e899dd3, 12855a41, 19f339ba or 1c45ce3a anywhere in the timing (-2 s to +2 s) and speed (0.5x to 2x) range that was searched. But most settings ran only once or twice, so this is a hint, not evidence that these scenes are safe.
  - S2: 054b5901 at actor_time_shift_s -0.5, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_026)
  - S3: 054b5901 at actor_time_shift_s 0.5, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_007)
  - S4: 054b5901 at actor_time_shift_s 1.5, actor_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_053)
  - S5: 096988dd at actor_time_shift_s -2, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_051)
  - S7: 096988dd at actor_time_shift_s 1.5, actor_speed_scale 2: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_hybrid_optuna_r4_027, cut_in_merge_hybrid_optuna_r4_031)
  - S8: 096988dd at actor_time_shift_s 2, actor_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_hybrid_optuna_r4_009, cut_in_merge_hybrid_optuna_r4_018)
  - S9: 09a95ffa at actor_time_shift_s -0.5, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_042)
  - S12: 09a95ffa at actor_time_shift_s 1.5, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_hybrid_optuna_r4_001, cut_in_merge_hybrid_optuna_r4_017)
  - S13: 0cf6368d at actor_time_shift_s -1.5, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_054)
  - S14: 0cf6368d at actor_time_shift_s -0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_036)
  - S15: 0cf6368d at actor_time_shift_s 2, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_008)
  - S16: 0e899dd3 at actor_time_shift_s -1, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_044)
  - S17: 0e899dd3 at actor_time_shift_s -0.5, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_023)
  - S18: 0e899dd3 at actor_time_shift_s 0.5, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_047)
  - S19: 0e899dd3 at actor_time_shift_s 1, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_035)
  - S21: 0e899dd3 at actor_time_shift_s 2, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_046)
  - S22: 12855a41 at actor_time_shift_s -2, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_045)
  - S24: 12855a41 at actor_time_shift_s -1, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_049)
  - S25: 12855a41 at actor_time_shift_s 1, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_022)
  - S26: 19f339ba at actor_time_shift_s -1, actor_speed_scale 2: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_hybrid_optuna_r4_025, cut_in_merge_hybrid_optuna_r4_030)
  - S28: 19f339ba at actor_time_shift_s 1, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_003)
  - S29: 19f339ba at actor_time_shift_s 1.5, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_048)
  - S31: 1c45ce3a at actor_time_shift_s -1.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_021)
  - S32: 1c45ce3a at actor_time_shift_s -0.5, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_043)
  - S33: 1c45ce3a at actor_time_shift_s 1, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_050)
- The settings that came closest to failing without failing were on scene 0e899dd3 with cars late and slow (1.5 s to 2 s later at 0.5x, and 0.5 s later at 0.5x), on 09a95ffa with cars fast, and on 1c45ce3a with cars 1 s later at 0.5x. By the brief's rule they rank next as near misses, but the stopping rule did not check them.
  - S20: 0e899dd3 at actor_time_shift_s 1.5, actor_speed_scale 0.5: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_hybrid_optuna_r4_005, cut_in_merge_hybrid_optuna_r4_013, cut_in_merge_hybrid_optuna_r4_014)
  - S21: 0e899dd3 at actor_time_shift_s 2, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_046)
  - S18: 0e899dd3 at actor_time_shift_s 0.5, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_047)
  - S10: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.5: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_hybrid_optuna_r4_033, cut_in_merge_hybrid_optuna_r4_037, cut_in_merge_hybrid_optuna_r4_038)
  - S11: 09a95ffa at actor_time_shift_s 0.5, actor_speed_scale 2: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_hybrid_optuna_r4_024, cut_in_merge_hybrid_optuna_r4_028, cut_in_merge_hybrid_optuna_r4_029)
  - S33: 1c45ce3a at actor_time_shift_s 1, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_050)

## Open

- Four of the five challenging cases are still missing. Probing around the closest near misses could settle this, for example later and slower cars on 0e899dd3 (around S20/S21), fast cars on 09a95ffa (around S10/S11) and 1 s later at 0.5x on 1c45ce3a (S33), with about four repeats for any setting that fails.
- It's unknown whether the retiming causes the 023b7fcc failure. The scene was chosen from runs with learned traffic and already came close at baseline, so it may fail at nominal timing and speed with replayed traffic too. A few runs at 0 s and 1x on 023b7fcc, plus nearby settings (e.g. -1 s or 0 s at 1.5x to 2x), would show this.
- It's unclear whether the 023b7fcc case is a cut-in or merge failure at all. The triage describes following a lead car too closely and then swerving left. Every car in that scene was retimed, so the run videos need checking to see whether car 66 cut in.
- Most settings on the other eight scenes ran only once or twice. A single run with no failure cannot rule out a failure rate above one half there.
- One run at S30 (1c45ce3a, 2 s earlier, 2x) was not kept and was re-run. It is not evidence.

## Why the runs failed (triage from the video and log)

turned_into_actor 3, no_brake_for_lead 1

- cut_in_merge_hybrid_optuna_r4_006: no_brake_for_lead, policy at fault: yes. On a multi-lane highway, the ego took over 1.7 m behind lead vehicle 66 in its own lane. Instead of braking, it sped up from 4.2 to 5.4 m/s and drove into and through 66's box (front collision from about 5.3 s, gap 0.1 m at 6.3 s, which also triggered the rear-contact flag), then veered left toward vehicle 61's lane while still in contact at 7.3 s.
- cut_in_merge_hybrid_optuna_r4_010: turned_into_actor, policy at fault: yes. Right after handoff, the ego was tangled up with actor 66 directly ahead in its lane. The two first touched front-on (about 5.3s), then 66 ended up overlapping the ego's rear (6.3s). After that, at about 6 m/s, the ego veered left off its planned path and partway into the next lane, hitting actor 61 there with its front at 7.3s.
- cut_in_merge_hybrid_optuna_r4_011: turned_into_actor, policy at fault: yes. In dense, slow highway traffic the ego tailgated actor 66 and was tangled up with it by 5.3–6.3s, with both front and rear contact. It then steered left out of its lane, away from the recorded path toward the adjacent lane, and at 7.3s drove its front into actor 61 in that lane at about 5.8 m/s.
- cut_in_merge_hybrid_optuna_r4_012: turned_into_actor, policy at fault: yes. The ego was tailgating actor 66 in its lane at about 5 m/s, closing to almost no gap and making contact around 5.3–6.3 s. It then left its planned path and steered left into the adjacent lane, where at 7.3 s its front ran into actor 61 in that lane.

## Every setting

- S1: 023b7fcc at actor_time_shift_s -0.5, actor_speed_scale 2: 4/4 failed, rate 60%-100% (90%) (cut_in_merge_hybrid_optuna_r4_006, cut_in_merge_hybrid_optuna_r4_010, cut_in_merge_hybrid_optuna_r4_011, cut_in_merge_hybrid_optuna_r4_012)
- S2: 054b5901 at actor_time_shift_s -0.5, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_026)
- S3: 054b5901 at actor_time_shift_s 0.5, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_007)
- S4: 054b5901 at actor_time_shift_s 1.5, actor_speed_scale 1: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_053)
- S5: 096988dd at actor_time_shift_s -2, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_051)
- S6: 096988dd at actor_time_shift_s -0.5, actor_speed_scale 2: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_hybrid_optuna_r4_032, cut_in_merge_hybrid_optuna_r4_041, cut_in_merge_hybrid_optuna_r4_052)
- S7: 096988dd at actor_time_shift_s 1.5, actor_speed_scale 2: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_hybrid_optuna_r4_027, cut_in_merge_hybrid_optuna_r4_031)
- S8: 096988dd at actor_time_shift_s 2, actor_speed_scale 1: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_hybrid_optuna_r4_009, cut_in_merge_hybrid_optuna_r4_018)
- S9: 09a95ffa at actor_time_shift_s -0.5, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_042)
- S10: 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.5: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_hybrid_optuna_r4_033, cut_in_merge_hybrid_optuna_r4_037, cut_in_merge_hybrid_optuna_r4_038)
- S11: 09a95ffa at actor_time_shift_s 0.5, actor_speed_scale 2: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_hybrid_optuna_r4_024, cut_in_merge_hybrid_optuna_r4_028, cut_in_merge_hybrid_optuna_r4_029)
- S12: 09a95ffa at actor_time_shift_s 1.5, actor_speed_scale 1.25: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_hybrid_optuna_r4_001, cut_in_merge_hybrid_optuna_r4_017)
- S13: 0cf6368d at actor_time_shift_s -1.5, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_054)
- S14: 0cf6368d at actor_time_shift_s -0.5, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_036)
- S15: 0cf6368d at actor_time_shift_s 2, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_008)
- S16: 0e899dd3 at actor_time_shift_s -1, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_044)
- S17: 0e899dd3 at actor_time_shift_s -0.5, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_023)
- S18: 0e899dd3 at actor_time_shift_s 0.5, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_047)
- S19: 0e899dd3 at actor_time_shift_s 1, actor_speed_scale 0.75: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_035)
- S20: 0e899dd3 at actor_time_shift_s 1.5, actor_speed_scale 0.5: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_hybrid_optuna_r4_005, cut_in_merge_hybrid_optuna_r4_013, cut_in_merge_hybrid_optuna_r4_014)
- S21: 0e899dd3 at actor_time_shift_s 2, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_046)
- S22: 12855a41 at actor_time_shift_s -2, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_045)
- S23: 12855a41 at actor_time_shift_s -1.5, actor_speed_scale 2: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_hybrid_optuna_r4_002, cut_in_merge_hybrid_optuna_r4_015, cut_in_merge_hybrid_optuna_r4_020)
- S24: 12855a41 at actor_time_shift_s -1, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_049)
- S25: 12855a41 at actor_time_shift_s 1, actor_speed_scale 1.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_022)
- S26: 19f339ba at actor_time_shift_s -1, actor_speed_scale 2: 0/2 failed, rate 0%-58% (90%) (cut_in_merge_hybrid_optuna_r4_025, cut_in_merge_hybrid_optuna_r4_030)
- S27: 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 1.25: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_hybrid_optuna_r4_034, cut_in_merge_hybrid_optuna_r4_039, cut_in_merge_hybrid_optuna_r4_040)
- S28: 19f339ba at actor_time_shift_s 1, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_003)
- S29: 19f339ba at actor_time_shift_s 1.5, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_048)
- S30: 1c45ce3a at actor_time_shift_s -2, actor_speed_scale 2: 0/3 failed, rate 0%-47% (90%) (cut_in_merge_hybrid_optuna_r4_004_a2, cut_in_merge_hybrid_optuna_r4_016, cut_in_merge_hybrid_optuna_r4_019)
- S31: 1c45ce3a at actor_time_shift_s -1.5, actor_speed_scale 1.25: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_021)
- S32: 1c45ce3a at actor_time_shift_s -0.5, actor_speed_scale 2: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_043)
- S33: 1c45ce3a at actor_time_shift_s 1, actor_speed_scale 0.5: 0/1 failed, rate 0%-73% (90%) (cut_in_merge_hybrid_optuna_r4_050)

## Not kept by the gate

- cut_in_merge_hybrid_optuna_r4_004: not kept: RE-RUN

## Provenance

Plan: `plan.json` (rationale: Scope and settings follow the brief. Traffic is replayed as recorded. Only recorded cars (class automobile) are retimed, using the knobs' full ranges: -2 s to +2 s and 0.5x to 2x speed.

Scene choice: 31 scenes carry the merge_cut_in tag. I kept 9 that passed at 0 delay and have a car identified as a key actor. Scenes that already fail with the recorded timing would fill the top 5 without showing what the retiming does, so I left them out. Three scenes have a car marked as cutting in (0cf6368d track 21, 12855a41 track 31, 1c45ce3a track 14). In those, only that car is retimed. The other six retime every car in the scene: with only a lead or crossing car identified, retiming that car alone could miss the car that actually changes lanes. Several picks already came close at baseline (023b7fcc and 096988dd at 0.0 m, 19f339ba at 0.03 m, 12855a41 at 0.08 m, 054b5901 at 0.26 m), so they are good places to look first.

Budget and stopping rule: 6 rounds of 9 runs gives 54 runs, close to the brief's ~50 and under the cap of 60. The goal is top_k with k=5, one case per scene, failure rate surely above 0.5. A setting needs about 4 failures in 4 runs to clear that bar, so confirming 5 cases costs about 20 to 25 runs. That leaves roughly 30 runs to search, and the study stops early once 5 cases are confirmed.

What this plan cannot do:
- If fewer than 5 scenes break reliably within the budget, the study will report fewer than 5 confirmed cases.
- Near misses can guide the search, but the stopping rule only counts failures, so they are not a checked ranking.
- The tags do not say whether the ego merges or another car cuts in, so the two cases cannot be told apart.
- The 0-delay results were recorded with learned (CATK) traffic, not replay, so the pass/fail used to pick scenes is only a guide.
- Retiming a whole class moves every car in the scene, not only the one changing lanes.
- Only the three scenes with a marked cut-in car can isolate it.). Report written by claude-opus-5-5 from `results` in 23 s; every count above is computed from the queue, not written by the model.

55 of 55 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
