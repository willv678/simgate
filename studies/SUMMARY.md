# Studies

Every proposer that ran each study's plan, scored by code from the kept
runs (`summarize_studies.py`). Runs to goal: kept runs until the goal
was met, or not reached within the budget. Hardest: mean criticality
(1 a crash, 0.9 contact, 0 at 5 m) of the hardest setting found on each
of the k most challenging scenes, unconfirmed (`compare_proposers.hardest`).

| study | proposer | kept | failures | runs to goal | found | hardest | model s |
|---|---|---|---|---|---|---|---|
| controller_tuning_pedestrian | hybrid | 20/50 | 10 | 16 | 1 | 0.559 | 21.7 |
| cut_in_merge | rules | 27/54 | 7 | not reached | 2 | 0.909 | 0.0 |
| cut_in_merge | rules_r2 | 54/54 | 9 | not reached | 2 | 0.948 | 0.0 |
| cut_in_merge | rules_r3 | 39/54 | 9 | not reached | 2 | 0.929 | 0.0 |
| cut_in_merge | hybrid | 27/54 | 6 | not reached | 2 | 0.934 | 36.7 |
| cut_in_merge | hybrid_r2 | 36/54 | 17 | 32 | 5 | 1.0 | 51.7 |
| cut_in_merge | hybrid_r3 | 14/54 | 7 | not reached | 2 | 0.886 | 23.6 |
| cut_in_merge | llm | 27/54 | 6 | not reached | 2 | 0.933 | 56.5 |
| cut_in_merge | llm_r2 | 54/54 | 18 | not reached | 4 | 0.983 | 101.3 |
| cut_in_merge | random_confirm | 54/54 | 18 | not reached | 3 | 0.952 | 0.0 |
| cut_in_merge | random_confirm_r2 | 54/54 | 18 | not reached | 3 | 0.949 | 0.0 |
| ego_speed_smoke | grid | 5/5 | 1 | not reached | 0 | 0.2 | 0.0 |
| intersection | rules | 49/49 | 0 | not reached | 0 | 0.435 | 0.0 |
| intersection | hybrid | 49/49 | 6 | not reached | 1 | 0.541 | 91.4 |
| intersection | llm | 49/49 | 0 | not reached | 0 | 0.462 | 116.2 |
| intersection_ego_speed | rules | 49/49 | 9 | not reached | 2 | 0.617 | 0.0 |
| intersection_ego_speed | hybrid | 49/49 | 9 | not reached | 2 | 0.626 | 123.1 |
| intersection_ego_speed | llm | 49/49 | 8 | not reached | 2 | 0.599 | 117.7 |
| intersection_ego_speed | random_confirm | 49/49 | 12 | not reached | 2 | 0.606 | 0.0 |
| lead_vehicle | rules | 49/49 | 0 | not reached | 0 | 0.846 | 0.0 |
| lead_vehicle | rules_r2 | 49/49 | 0 | not reached | 0 | 0.851 | 0.0 |
| lead_vehicle | rules_r3 | 49/49 | 0 | not reached | 0 | 0.854 | 0.0 |
| lead_vehicle | rules_corners | 49/49 | 0 | not reached | 0 | 0.853 | 0.0 |
| lead_vehicle | rules_v2 | 49/49 | 1 | not reached | 0 | 0.891 | 0.0 |
| lead_vehicle | hybrid | 49/49 | 7 | not reached | 2 | 0.92 | 110.8 |
| lead_vehicle | hybrid_r2 | 49/49 | 10 | not reached | 3 | 0.952 | 100.4 |
| lead_vehicle | hybrid_r3 | 49/49 | 9 | not reached | 3 | 0.955 | 101.3 |
| lead_vehicle | llm | 21/49 | 13 | not reached | 3 | 0.918 | 40.7 |
| lead_vehicle | llm_r2 | 28/49 | 21 | 23 | 5 | 1.0 | 59.8 |
| lead_vehicle | llm_r3 | 35/49 | 23 | 30 | 5 | 1.0 | 75.8 |
| lead_vehicle | random_confirm | 49/49 | 17 | 43 | 5 | 1.0 | 0.0 |
| lead_vehicle | random_confirm_r2 | 49/49 | 17 | not reached | 4 | 0.978 | 0.0 |
| lead_vehicle | random_confirm_r3 | 49/49 | 11 | not reached | 3 | 0.953 | 0.0 |
| pedestrian_crossing | rules | 49/49 | 0 | not reached | 0 | 0.643 | 0.0 |
| pedestrian_crossing | hybrid | 49/49 | 0 | not reached | 0 | 0.636 | 90.1 |
| pedestrian_crossing | llm | 49/49 | 5 | not reached | 1 | 0.691 | 112.3 |
| pedestrian_crossing | random | 49/49 | 0 | not reached | 0 | 0.673 | 0.0 |
| pedestrian_crossing | optuna | 49/49 | 3 | not reached | 1 | 0.699 | 0.0 |
| pedestrian_ego_speed | rules | 30/50 | 17 | 25 | 5 | 1.0 | 0.0 |
| pedestrian_ego_speed | rules_r2 | 30/50 | 18 | 25 | 5 | 1.0 | 0.0 |
| pedestrian_ego_speed | rules_r3 | 30/50 | 18 | 25 | 5 | 1.0 | 0.0 |
| pedestrian_ego_speed | hybrid | 30/50 | 18 | 24 | 5 | 1.0 | 46.0 |
| pedestrian_ego_speed | hybrid_r2 | 30/50 | 19 | 28 | 5 | 1.0 | 45.6 |
| pedestrian_ego_speed | hybrid_r3 | 30/50 | 19 | 24 | 5 | 1.0 | 42.3 |
| pedestrian_ego_speed | llm | 30/50 | 18 | 28 | 5 | 1.0 | 52.5 |
| pedestrian_ego_speed | llm_r2 | 49/50 | 30 | 40 | 5 | 1.0 | 88.1 |
| pedestrian_ego_speed | llm_r3 | 39/50 | 25 | 37 | 5 | 1.0 | 78.2 |
| pedestrian_ego_speed | random | 48/50 | 31 | not reached | 0 | 1.0 | 0.0 |
| pedestrian_ego_speed | random_confirm | 39/50 | 28 | 31 | 5 | 1.0 | 0.0 |
| pedestrian_ego_speed | random_confirm_r2 | 39/50 | 29 | 32 | 5 | 1.0 | 0.0 |
| pedestrian_ego_speed | random_confirm_r3 | 40/50 | 31 | 32 | 5 | 1.0 | 0.0 |

## controller_tuning_pedestrian

Does the tuned linear MPC (feasible_best: Riccati terminal cost, stiffer position tracking) fail less often than the default linear MPC when the key pedestrian steps out up to 2 s early and walks 1x to 2x their recorded speed?

- **hybrid**: linear fails less than feasible_best: the pooled 90% ranges separate

## cut_in_merge

In merge and cut-in scenes, which timings and speeds of the other cars make the VaVAM policy collide or leave the road? Find the 5 most challenging settings, each on a different scene and confirmed by repeats.

- **rules**: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 1.25; 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 1.25
- **rules_r2**: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 1.25; 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 1.25
- **rules_r3**: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 1.25; 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 1.25
- **hybrid**: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1.25; 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25
- **hybrid_r2**: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 2; 096988dd at actor_time_shift_s 0, actor_speed_scale 2; 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1.25; 054b5901 at actor_time_shift_s 0, actor_speed_scale 1.5; 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25
- **hybrid_r3**: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1.25; 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25
- **llm**: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1.25; 09a95ffa at actor_time_shift_s -1, actor_speed_scale 1.5
- **llm_r2**: 09a95ffa at actor_time_shift_s 0.5, actor_speed_scale 1; 023b7fcc at actor_time_shift_s -0.5, actor_speed_scale 1; 19f339ba at actor_time_shift_s 0.5, actor_speed_scale 1; 054b5901 at actor_time_shift_s -1, actor_speed_scale 1.25
- **random_confirm**: 096988dd at actor_time_shift_s 2.0, actor_speed_scale 1.25; 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 1.25; 023b7fcc at actor_time_shift_s -2.0, actor_speed_scale 1.5
- **random_confirm_r2**: 09a95ffa at actor_time_shift_s -1.5, actor_speed_scale 1.25; 023b7fcc at actor_time_shift_s 0.5, actor_speed_scale 2.0; 054b5901 at actor_time_shift_s -1.0, actor_speed_scale 1.25

## ego_speed_smoke

Does the ego speed knob land and pass the gate on a real run at each value?

- **grid**: nothing confirmed

## intersection

At intersections with crossing traffic, which arrival times and speeds of the recorded crossing car make the VaVAM policy collide or leave the road? Find the 5 most challenging settings, each on a different scene, confirmed by repeats.

- **rules**: nothing confirmed
- **hybrid**: 02eadd92 at actor_time_shift_s 1, actor_speed_scale 1.25
- **llm**: nothing confirmed

## intersection_ego_speed

At intersections with a recorded crossing car, which combinations of the ego's speed at hand-off and the crossing car's arrival time make VaVAM with the linear MPC collide or leave the road? The goal is the 5 most challenging cases, each on a different scene, confirmed by repeats.

- **rules**: 02eadd92 at ego_speed_scale 1.0, actor_time_shift_s 0.0; 054b5901 at ego_speed_scale 1.2, actor_time_shift_s 0.0
- **hybrid**: 02eadd92 at ego_speed_scale 1, actor_time_shift_s 0; 054b5901 at ego_speed_scale 1.2, actor_time_shift_s 0
- **llm**: 02eadd92 at ego_speed_scale 1.2, actor_time_shift_s 0; 054b5901 at ego_speed_scale 1.2, actor_time_shift_s -0.5
- **random_confirm**: 054b5901 at ego_speed_scale 1.4, actor_time_shift_s -1.5; 02eadd92 at ego_speed_scale 1.2, actor_time_shift_s 1.0

## lead_vehicle

In lead-vehicle scenes, which timing shifts and speed scalings of the recorded lead car (with up to 200 ms planner delay if needed) make VaVAM run into it? Find the 5 most challenging cases, each on a different scene, confirmed by repeats.

- **rules**: nothing confirmed
- **rules_r2**: nothing confirmed
- **rules_r3**: nothing confirmed
- **rules_corners**: nothing confirmed
- **rules_v2**: nothing confirmed
- **hybrid**: 12855a41 at actor_time_shift_s 0, actor_speed_scale 0.75, planner_delay_us 200000; 09a95ffa at actor_time_shift_s 0, actor_speed_scale 0.75, planner_delay_us 200000
- **hybrid_r2**: 12855a41 at actor_time_shift_s 0, actor_speed_scale 0.75, planner_delay_us 200000; 09a95ffa at actor_time_shift_s 0, actor_speed_scale 0.75, planner_delay_us 200000; 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 1.25, planner_delay_us 200000
- **hybrid_r3**: 023b7fcc at actor_time_shift_s 0, actor_speed_scale 0.75, planner_delay_us 200000; 12855a41 at actor_time_shift_s 0, actor_speed_scale 0.75, planner_delay_us 200000; 19f339ba at actor_time_shift_s -0.5, actor_speed_scale 1.25, planner_delay_us 200000
- **llm**: 19f339ba at actor_time_shift_s 1, actor_speed_scale 0.5, planner_delay_us 0; 096988dd at actor_time_shift_s 1, actor_speed_scale 0.5, planner_delay_us 0; 12855a41 at actor_time_shift_s 1, actor_speed_scale 0.5, planner_delay_us 0
- **llm_r2**: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 0.5, planner_delay_us 0; 12855a41 at actor_time_shift_s 0, actor_speed_scale 0.5, planner_delay_us 0; 19f339ba at actor_time_shift_s 0, actor_speed_scale 0.5, planner_delay_us 0; 023b7fcc at actor_time_shift_s 0, actor_speed_scale 0.5, planner_delay_us 0; 096988dd at actor_time_shift_s 0, actor_speed_scale 0.5, planner_delay_us 0
- **llm_r3**: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 0.5, planner_delay_us 0; 023b7fcc at actor_time_shift_s 0, actor_speed_scale 0.5, planner_delay_us 0; 12855a41 at actor_time_shift_s 1, actor_speed_scale 0.5, planner_delay_us 0; 19f339ba at actor_time_shift_s 1, actor_speed_scale 0.5, planner_delay_us 0; 096988dd at actor_time_shift_s 1, actor_speed_scale 0.5, planner_delay_us 0
- **random_confirm**: 023b7fcc at actor_time_shift_s -1.0, actor_speed_scale 0.5, planner_delay_us 200000; 09a95ffa at actor_time_shift_s 2.0, actor_speed_scale 1.25, planner_delay_us 400000; 0e899dd3 at actor_time_shift_s -1.0, actor_speed_scale 0.5, planner_delay_us 50000; 12855a41 at actor_time_shift_s 0.0, actor_speed_scale 0.5, planner_delay_us 50000; 096988dd at actor_time_shift_s -1.5, actor_speed_scale 1.25, planner_delay_us 0
- **random_confirm_r2**: 09a95ffa at actor_time_shift_s 1.5, actor_speed_scale 0.75, planner_delay_us 250000; 023b7fcc at actor_time_shift_s 1.5, actor_speed_scale 0.75, planner_delay_us 50000; 12855a41 at actor_time_shift_s 0.5, actor_speed_scale 0.5, planner_delay_us 400000; 096988dd at actor_time_shift_s -2.0, actor_speed_scale 1.5, planner_delay_us 350000
- **random_confirm_r3**: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.5, planner_delay_us 200000; 023b7fcc at actor_time_shift_s 1.5, actor_speed_scale 0.75, planner_delay_us 50000; 096988dd at actor_time_shift_s -2.0, actor_speed_scale 1.5, planner_delay_us 350000

## pedestrian_crossing

Which pedestrian step-out timings (±2 s) and walking speeds (0.5x to 2x) make VaVAM hit the pedestrian or leave the road in pedestrian-crossing scenes, with the other traffic replayed as recorded? Find the 5 hardest cases, each on a different scene.

- **rules**: nothing confirmed
- **hybrid**: nothing confirmed
- **llm**: 13a9767e at actor_time_shift_s 0.5, actor_speed_scale 0.5
- **random**: nothing confirmed
- **optuna**: 13a9767e at actor_time_shift_s 1.0, actor_speed_scale 0.5

## pedestrian_ego_speed

In pedestrian-crossing scenes, which combinations of ego speed at hand-off (0.6x–1.4x recorded) and pedestrian step-out time (±2 s) make the VaVAM policy with the linear MPC collide or leave the road? Find the 5 most challenging cases, each on a different scene, confirmed by repeats.

- **rules**: 048b974e at ego_speed_scale 1.0, actor_time_shift_s 0.0; 18d28973 at ego_speed_scale 1.0, actor_time_shift_s 0.0; 1bbe02fc at ego_speed_scale 1.0, actor_time_shift_s 0.0; 07981e6a at ego_speed_scale 1.0, actor_time_shift_s 0.0; 0d4893f5 at ego_speed_scale 1.0, actor_time_shift_s 0.0
- **rules_r2**: 048b974e at ego_speed_scale 1.0, actor_time_shift_s 0.0; 18d28973 at ego_speed_scale 1.0, actor_time_shift_s 0.0; 1bbe02fc at ego_speed_scale 1.0, actor_time_shift_s 0.0; 07981e6a at ego_speed_scale 1.0, actor_time_shift_s 0.0; 0caa8f1a at ego_speed_scale 1.0, actor_time_shift_s 0.0
- **rules_r3**: 048b974e at ego_speed_scale 1.0, actor_time_shift_s 0.0; 18d28973 at ego_speed_scale 1.0, actor_time_shift_s 0.0; 1bbe02fc at ego_speed_scale 1.0, actor_time_shift_s 0.0; 07981e6a at ego_speed_scale 1.0, actor_time_shift_s 0.0; 0caa8f1a at ego_speed_scale 1.0, actor_time_shift_s 0.0
- **hybrid**: 048b974e at ego_speed_scale 1, actor_time_shift_s 0; 18d28973 at ego_speed_scale 1, actor_time_shift_s 0; 1bbe02fc at ego_speed_scale 1, actor_time_shift_s 0; 07981e6a at ego_speed_scale 1, actor_time_shift_s 0; 0caa8f1a at ego_speed_scale 1, actor_time_shift_s 0
- **hybrid_r2**: 048b974e at ego_speed_scale 1, actor_time_shift_s 0; 18d28973 at ego_speed_scale 1, actor_time_shift_s 0; 1bbe02fc at ego_speed_scale 1, actor_time_shift_s 0; 07981e6a at ego_speed_scale 1, actor_time_shift_s 0; 0caa8f1a at ego_speed_scale 1, actor_time_shift_s 0
- **hybrid_r3**: 048b974e at ego_speed_scale 1, actor_time_shift_s 0; 18d28973 at ego_speed_scale 1, actor_time_shift_s 0; 1bbe02fc at ego_speed_scale 1, actor_time_shift_s 0; 07981e6a at ego_speed_scale 1, actor_time_shift_s 0; 0caa8f1a at ego_speed_scale 1, actor_time_shift_s 0
- **llm**: 048b974e at ego_speed_scale 1.2, actor_time_shift_s -0.5; 18d28973 at ego_speed_scale 1.2, actor_time_shift_s -0.5; 1bbe02fc at ego_speed_scale 1.2, actor_time_shift_s -1; 0d4893f5 at ego_speed_scale 1.2, actor_time_shift_s -0.5; 0e002edd at ego_speed_scale 1.4, actor_time_shift_s -0.5
- **llm_r2**: 048b974e at ego_speed_scale 1.4, actor_time_shift_s -1; 0e002edd at ego_speed_scale 1.4, actor_time_shift_s 0; 18d28973 at ego_speed_scale 1.2, actor_time_shift_s -0.5; 1bbe02fc at ego_speed_scale 1.2, actor_time_shift_s -0.5; 0d4893f5 at ego_speed_scale 1.2, actor_time_shift_s -0.5
- **llm_r3**: 048b974e at ego_speed_scale 1.2, actor_time_shift_s 0; 0e002edd at ego_speed_scale 1.4, actor_time_shift_s 0; 18d28973 at ego_speed_scale 1, actor_time_shift_s 0; 1bbe02fc at ego_speed_scale 1.2, actor_time_shift_s 0; 0caa8f1a at ego_speed_scale 1.2, actor_time_shift_s 0
- **random**: nothing confirmed
- **random_confirm**: 048b974e at ego_speed_scale 0.6, actor_time_shift_s -1.5; 0caa8f1a at ego_speed_scale 1.0, actor_time_shift_s 1.5; 0d4893f5 at ego_speed_scale 1.2, actor_time_shift_s 1.0; 18d28973 at ego_speed_scale 0.8, actor_time_shift_s 0.0; 07981e6a at ego_speed_scale 1.4, actor_time_shift_s -0.5
- **random_confirm_r2**: 0d4893f5 at ego_speed_scale 0.8, actor_time_shift_s 2.0; 0e002edd at ego_speed_scale 1.4, actor_time_shift_s -1.5; 07981e6a at ego_speed_scale 0.6, actor_time_shift_s 1.5; 18d28973 at ego_speed_scale 1.2, actor_time_shift_s -1.0; 0caa8f1a at ego_speed_scale 0.6, actor_time_shift_s 1.0
- **random_confirm_r3**: 0caa8f1a at ego_speed_scale 0.8, actor_time_shift_s -1.0; 0d4893f5 at ego_speed_scale 0.6, actor_time_shift_s 1.5; 18d28973 at ego_speed_scale 1.4, actor_time_shift_s 0.5; 048b974e at ego_speed_scale 0.8, actor_time_shift_s -1.0; 07981e6a at ego_speed_scale 1.4, actor_time_shift_s 1.0
