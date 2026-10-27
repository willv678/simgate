# In cut-in and lead-vehicle scenes that pass as recorded, which combinations of the car's timing, the car's speed and the ego's speed at hand-off make the policy collide or leave the road? The aim is the 5 most challenging cases, each on a different scene, confirmed by repeats.

Study `rules_r6`: 60 kept runs on 10 scenes, varying actor_time_shift_s, actor_speed_scale, ego_speed_scale; 2 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** 0 of 5 challenging settings confirmed, after 6 rounds.

## Answer

The study did not find any combination that reliably makes the policy collide or leave the road, and none of the 5 cases it was asked for were confirmed. Most of the budget went into one setting, the car on its recorded timing at 1.25x speed with the ego at its recorded speed, repeated on 9 scenes. That setting failed only once, on 19f339ba. The upper end of the 90% ranges still leaves room for a real failure rate of up to about a third at that setting on each scene. The one failure is weak evidence: the policy braked hard for no reason on a clear road, and a car behind it, which doesn't react, ran into its rear quarter. That is a phantom-braking fault rather than the collision type the brief targets, and it is close to the rear-end hits the plan said to ignore.

## Findings

- With the car on its recorded timing at 1.25x speed and the ego at its recorded speed, the policy did not fail on any of 8 scenes across repeated runs. At this setting it does not fail often on these scenes, though the ranges cannot rule out a failure rate of up to about a third.
  - S1: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r6_001, car_conflicts_3knobs_2hz_rules_r6_017, car_conflicts_3knobs_2hz_rules_r6_028, car_conflicts_3knobs_2hz_rules_r6_038, car_conflicts_3knobs_2hz_rules_r6_048, car_conflicts_3knobs_2hz_rules_r6_058)
  - S2: 096988dd at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r6_002, car_conflicts_3knobs_2hz_rules_r6_013, car_conflicts_3knobs_2hz_rules_r6_023, car_conflicts_3knobs_2hz_rules_r6_033, car_conflicts_3knobs_2hz_rules_r6_043, car_conflicts_3knobs_2hz_rules_r6_051)
  - S3: 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r6_008, car_conflicts_3knobs_2hz_rules_r6_015, car_conflicts_3knobs_2hz_rules_r6_026, car_conflicts_3knobs_2hz_rules_r6_035, car_conflicts_3knobs_2hz_rules_r6_045, car_conflicts_3knobs_2hz_rules_r6_054)
  - S4: 0cf6368d at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r6_007, car_conflicts_3knobs_2hz_rules_r6_018, car_conflicts_3knobs_2hz_rules_r6_027, car_conflicts_3knobs_2hz_rules_r6_037, car_conflicts_3knobs_2hz_rules_r6_047, car_conflicts_3knobs_2hz_rules_r6_057)
  - S11: 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r6_009, car_conflicts_3knobs_2hz_rules_r6_016, car_conflicts_3knobs_2hz_rules_r6_024, car_conflicts_3knobs_2hz_rules_r6_034, car_conflicts_3knobs_2hz_rules_r6_044, car_conflicts_3knobs_2hz_rules_r6_055)
  - S12: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r6_003, car_conflicts_3knobs_2hz_rules_r6_014, car_conflicts_3knobs_2hz_rules_r6_025, car_conflicts_3knobs_2hz_rules_r6_036, car_conflicts_3knobs_2hz_rules_r6_046, car_conflicts_3knobs_2hz_rules_r6_056)
  - S13: 187e6244 at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r6_005, car_conflicts_3knobs_2hz_rules_r6_019, car_conflicts_3knobs_2hz_rules_r6_029, car_conflicts_3knobs_2hz_rules_r6_039, car_conflicts_3knobs_2hz_rules_r6_049, car_conflicts_3knobs_2hz_rules_r6_059)
  - S15: 1c45ce3a at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r6_010_a2, car_conflicts_3knobs_2hz_rules_r6_012, car_conflicts_3knobs_2hz_rules_r6_022, car_conflicts_3knobs_2hz_rules_r6_032, car_conflicts_3knobs_2hz_rules_r6_041, car_conflicts_3knobs_2hz_rules_r6_053)
- The only failure came on 19f339ba at the same setting. The policy braked hard on an open highway with the lead car far ahead, and a following car that doesn't react overlapped its right rear. The policy was at fault for braking for nothing, but the collision is effectively a rear hit. It happened in only one of six repeats, so it is not a confirmed challenging case.
  - S14: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 1/6 failed, rate 4%-50% (90%) (car_conflicts_3knobs_2hz_rules_r6_004, car_conflicts_3knobs_2hz_rules_r6_011, car_conflicts_3knobs_2hz_rules_r6_021, car_conflicts_3knobs_2hz_rules_r6_031, car_conflicts_3knobs_2hz_rules_r6_042, car_conflicts_3knobs_2hz_rules_r6_052)
- By closest approach (criticality), the strongest near misses at the 1.25x setting were on 096988dd and 19f339ba, followed by 09a95ffa, 0e899dd3 and 12855a41. Under the brief's ranking these are the next-best candidates.
  - S2: 096988dd at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r6_002, car_conflicts_3knobs_2hz_rules_r6_013, car_conflicts_3knobs_2hz_rules_r6_023, car_conflicts_3knobs_2hz_rules_r6_033, car_conflicts_3knobs_2hz_rules_r6_043, car_conflicts_3knobs_2hz_rules_r6_051)
  - S14: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 1/6 failed, rate 4%-50% (90%) (car_conflicts_3knobs_2hz_rules_r6_004, car_conflicts_3knobs_2hz_rules_r6_011, car_conflicts_3knobs_2hz_rules_r6_021, car_conflicts_3knobs_2hz_rules_r6_031, car_conflicts_3knobs_2hz_rules_r6_042, car_conflicts_3knobs_2hz_rules_r6_052)
  - S3: 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r6_008, car_conflicts_3knobs_2hz_rules_r6_015, car_conflicts_3knobs_2hz_rules_r6_026, car_conflicts_3knobs_2hz_rules_r6_035, car_conflicts_3knobs_2hz_rules_r6_045, car_conflicts_3knobs_2hz_rules_r6_054)
  - S11: 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r6_009, car_conflicts_3knobs_2hz_rules_r6_016, car_conflicts_3knobs_2hz_rules_r6_024, car_conflicts_3knobs_2hz_rules_r6_034, car_conflicts_3knobs_2hz_rules_r6_044, car_conflicts_3knobs_2hz_rules_r6_055)
  - S12: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r6_003, car_conflicts_3knobs_2hz_rules_r6_014, car_conflicts_3knobs_2hz_rules_r6_025, car_conflicts_3knobs_2hz_rules_r6_036, car_conflicts_3knobs_2hz_rules_r6_046, car_conflicts_3knobs_2hz_rules_r6_056)
- On 0dbb91dd, moving the car 0 to 2 s earlier at 1.25x speed, and once at its recorded speed with a 2 s earlier start, caused no failure in single runs. One run per setting is only a hint. These runs also report zero criticality, which may mean no close approach was recorded at all.
  - S5: 0dbb91dd at actor_time_shift_s -2.0, actor_speed_scale 1.0, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_rules_r6_060)
  - S6: 0dbb91dd at actor_time_shift_s -2.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_rules_r6_050)
  - S7: 0dbb91dd at actor_time_shift_s -1.5, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_rules_r6_040)
  - S8: 0dbb91dd at actor_time_shift_s -1.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_rules_r6_030_a2)
  - S9: 0dbb91dd at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_rules_r6_020)
  - S10: 0dbb91dd at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_rules_r6_006)
- The ego's speed at hand-off was never changed from its recorded value, and the car's speed was only tried at 1.0x and 1.25x. The search therefore did not cover the three-knob space the brief describes.
  - S1: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r6_001, car_conflicts_3knobs_2hz_rules_r6_017, car_conflicts_3knobs_2hz_rules_r6_028, car_conflicts_3knobs_2hz_rules_r6_038, car_conflicts_3knobs_2hz_rules_r6_048, car_conflicts_3knobs_2hz_rules_r6_058)
  - S2: 096988dd at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r6_002, car_conflicts_3knobs_2hz_rules_r6_013, car_conflicts_3knobs_2hz_rules_r6_023, car_conflicts_3knobs_2hz_rules_r6_033, car_conflicts_3knobs_2hz_rules_r6_043, car_conflicts_3knobs_2hz_rules_r6_051)
  - S3: 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r6_008, car_conflicts_3knobs_2hz_rules_r6_015, car_conflicts_3knobs_2hz_rules_r6_026, car_conflicts_3knobs_2hz_rules_r6_035, car_conflicts_3knobs_2hz_rules_r6_045, car_conflicts_3knobs_2hz_rules_r6_054)
  - S4: 0cf6368d at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r6_007, car_conflicts_3knobs_2hz_rules_r6_018, car_conflicts_3knobs_2hz_rules_r6_027, car_conflicts_3knobs_2hz_rules_r6_037, car_conflicts_3knobs_2hz_rules_r6_047, car_conflicts_3knobs_2hz_rules_r6_057)
  - S5: 0dbb91dd at actor_time_shift_s -2.0, actor_speed_scale 1.0, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_rules_r6_060)
  - S6: 0dbb91dd at actor_time_shift_s -2.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_rules_r6_050)
  - S7: 0dbb91dd at actor_time_shift_s -1.5, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_rules_r6_040)
  - S8: 0dbb91dd at actor_time_shift_s -1.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_rules_r6_030_a2)
  - S9: 0dbb91dd at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_rules_r6_020)
  - S10: 0dbb91dd at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_rules_r6_006)
  - S11: 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r6_009, car_conflicts_3knobs_2hz_rules_r6_016, car_conflicts_3knobs_2hz_rules_r6_024, car_conflicts_3knobs_2hz_rules_r6_034, car_conflicts_3knobs_2hz_rules_r6_044, car_conflicts_3knobs_2hz_rules_r6_055)
  - S12: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r6_003, car_conflicts_3knobs_2hz_rules_r6_014, car_conflicts_3knobs_2hz_rules_r6_025, car_conflicts_3knobs_2hz_rules_r6_036, car_conflicts_3knobs_2hz_rules_r6_046, car_conflicts_3knobs_2hz_rules_r6_056)
  - S13: 187e6244 at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r6_005, car_conflicts_3knobs_2hz_rules_r6_019, car_conflicts_3knobs_2hz_rules_r6_029, car_conflicts_3knobs_2hz_rules_r6_039, car_conflicts_3knobs_2hz_rules_r6_049, car_conflicts_3knobs_2hz_rules_r6_059)
  - S14: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 1/6 failed, rate 4%-50% (90%) (car_conflicts_3knobs_2hz_rules_r6_004, car_conflicts_3knobs_2hz_rules_r6_011, car_conflicts_3knobs_2hz_rules_r6_021, car_conflicts_3knobs_2hz_rules_r6_031, car_conflicts_3knobs_2hz_rules_r6_042, car_conflicts_3knobs_2hz_rules_r6_052)
  - S15: 1c45ce3a at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r6_010_a2, car_conflicts_3knobs_2hz_rules_r6_012, car_conflicts_3knobs_2hz_rules_r6_022, car_conflicts_3knobs_2hz_rules_r6_032, car_conflicts_3knobs_2hz_rules_r6_041, car_conflicts_3knobs_2hz_rules_r6_053)

## Open

- Whether the other parts of the space produce failures: ego speed 0.6x or 1.4x, car speed 0.5x (a sharply slowing lead) or 2x, and the car moved later in time. None of these were run. A coarse sweep of these corners on the scenes with the closest approaches (096988dd, 19f339ba, 09a95ffa, 0e899dd3, 12855a41) would show whether they fail.
- Whether the phantom braking on 19f339ba repeats. More repeats at that setting (S14), plus nearby settings with the ego faster, would show whether it is a real failure mode or a one-off. Re-running with reactive traffic would also show whether the collision depends on the follower not reacting.
- Whether the timing sweep on 0dbb91dd really produced no close approach. The zero criticality there should be checked against the logs, because the search may have lost its near-miss signal on that scene.
- Whether the policy actually planned at 2 Hz (control timestep 500 ms is set in the plan, but nothing checked the policy's own rhythm).
- Two runs (r6_010 on 1c45ce3a and r6_030 on 0dbb91dd) were not kept and were re-run. They are not evidence.

## Why the runs failed (triage from the video and log)

other 1

- car_conflicts_3knobs_2hz_rules_r6_004: other, policy at fault: yes. On an open highway with the road ahead clear (the lead was 43–59 m away), the ego braked hard for no reason, from 15.7 to 6.6 m/s, and drifted slightly left of the recorded path. At 8.1 s, actor 28 came up from behind on the ego's right rear and overlapped it. The scenario flags this as an at-fault front collision, but it is really the result of a following actor that does not react hitting a car that braked for nothing.

## Every setting

- S1: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r6_001, car_conflicts_3knobs_2hz_rules_r6_017, car_conflicts_3knobs_2hz_rules_r6_028, car_conflicts_3knobs_2hz_rules_r6_038, car_conflicts_3knobs_2hz_rules_r6_048, car_conflicts_3knobs_2hz_rules_r6_058)
- S2: 096988dd at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r6_002, car_conflicts_3knobs_2hz_rules_r6_013, car_conflicts_3knobs_2hz_rules_r6_023, car_conflicts_3knobs_2hz_rules_r6_033, car_conflicts_3knobs_2hz_rules_r6_043, car_conflicts_3knobs_2hz_rules_r6_051)
- S3: 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r6_008, car_conflicts_3knobs_2hz_rules_r6_015, car_conflicts_3knobs_2hz_rules_r6_026, car_conflicts_3knobs_2hz_rules_r6_035, car_conflicts_3knobs_2hz_rules_r6_045, car_conflicts_3knobs_2hz_rules_r6_054)
- S4: 0cf6368d at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r6_007, car_conflicts_3knobs_2hz_rules_r6_018, car_conflicts_3knobs_2hz_rules_r6_027, car_conflicts_3knobs_2hz_rules_r6_037, car_conflicts_3knobs_2hz_rules_r6_047, car_conflicts_3knobs_2hz_rules_r6_057)
- S5: 0dbb91dd at actor_time_shift_s -2.0, actor_speed_scale 1.0, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_rules_r6_060)
- S6: 0dbb91dd at actor_time_shift_s -2.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_rules_r6_050)
- S7: 0dbb91dd at actor_time_shift_s -1.5, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_rules_r6_040)
- S8: 0dbb91dd at actor_time_shift_s -1.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_rules_r6_030_a2)
- S9: 0dbb91dd at actor_time_shift_s -0.5, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_rules_r6_020)
- S10: 0dbb91dd at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (car_conflicts_3knobs_2hz_rules_r6_006)
- S11: 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r6_009, car_conflicts_3knobs_2hz_rules_r6_016, car_conflicts_3knobs_2hz_rules_r6_024, car_conflicts_3knobs_2hz_rules_r6_034, car_conflicts_3knobs_2hz_rules_r6_044, car_conflicts_3knobs_2hz_rules_r6_055)
- S12: 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r6_003, car_conflicts_3knobs_2hz_rules_r6_014, car_conflicts_3knobs_2hz_rules_r6_025, car_conflicts_3knobs_2hz_rules_r6_036, car_conflicts_3knobs_2hz_rules_r6_046, car_conflicts_3knobs_2hz_rules_r6_056)
- S13: 187e6244 at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r6_005, car_conflicts_3knobs_2hz_rules_r6_019, car_conflicts_3knobs_2hz_rules_r6_029, car_conflicts_3knobs_2hz_rules_r6_039, car_conflicts_3knobs_2hz_rules_r6_049, car_conflicts_3knobs_2hz_rules_r6_059)
- S14: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 1/6 failed, rate 4%-50% (90%) (car_conflicts_3knobs_2hz_rules_r6_004, car_conflicts_3knobs_2hz_rules_r6_011, car_conflicts_3knobs_2hz_rules_r6_021, car_conflicts_3knobs_2hz_rules_r6_031, car_conflicts_3knobs_2hz_rules_r6_042, car_conflicts_3knobs_2hz_rules_r6_052)
- S15: 1c45ce3a at actor_time_shift_s 0.0, actor_speed_scale 1.25, ego_speed_scale 1.0: 0/6 failed, rate 0%-31% (90%) (car_conflicts_3knobs_2hz_rules_r6_010_a2, car_conflicts_3knobs_2hz_rules_r6_012, car_conflicts_3knobs_2hz_rules_r6_022, car_conflicts_3knobs_2hz_rules_r6_032, car_conflicts_3knobs_2hz_rules_r6_041, car_conflicts_3knobs_2hz_rules_r6_053)

## Not kept by the gate

- car_conflicts_3knobs_2hz_rules_r6_010: not kept: RE-RUN
- car_conflicts_3knobs_2hz_rules_r6_030: not kept: RE-RUN

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
- A scale above 1 starts the ego behind its recorded start, so for the first second or two of the warm-up it is off the recording.). Report written by claude-opus-5-5 from `results` in 19 s; every count above is computed from the queue, not written by the model.

0 of 62 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
