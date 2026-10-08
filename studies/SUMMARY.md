# Studies

Every proposer that ran each study's plan, scored by code from the kept
runs (`summarize_studies.py`). Runs to goal: kept runs until the goal
was met, or not reached within the budget. Hardest: mean criticality
(1 a crash, 0.9 contact, 0 at 5 m) of the hardest setting found on each
of the k most challenging scenes, unconfirmed (`compare_proposers.hardest`).

| study | proposer | kept | failures | runs to goal | found | hardest | model s |
|---|---|---|---|---|---|---|---|
| controller_tuning_pedestrian | hybrid | 10/50 | 5 | 6 | 1 | 0.612 | 8.4 |
| cut_in_merge | rules | 27/54 | 16 | 23 | 5 | 1.0 | 0.0 |
| cut_in_merge | hybrid | 27/54 | 18 | 19 | 5 | 1.0 | 36.7 |
| cut_in_merge | llm | 27/54 | 17 | 19 | 5 | 1.0 | 56.5 |
| ego_speed_smoke | grid | 5/5 | 1 | not reached | 0 | 0.2 | 0.0 |
| intersection | rules | 49/49 | 0 | not reached | 0 | 0.65 | 0.0 |
| intersection | hybrid | 49/49 | 6 | not reached | 1 | 0.748 | 91.4 |
| intersection | llm | 49/49 | 0 | not reached | 0 | 0.669 | 116.2 |
| lead_vehicle | rules | 49/49 | 3 | not reached | 1 | 0.89 | 0.0 |
| lead_vehicle | hybrid | 49/49 | 15 | not reached | 4 | 0.977 | 110.8 |
| lead_vehicle | llm | 21/49 | 19 | 21 | 5 | 1.0 | 40.7 |
| pedestrian_crossing | rules | 49/49 | 0 | not reached | 0 | 0.747 | 0.0 |
| pedestrian_crossing | hybrid | 49/49 | 0 | not reached | 0 | 0.74 | 90.1 |
| pedestrian_crossing | llm | 49/49 | 5 | not reached | 1 | 0.795 | 112.3 |
| pedestrian_crossing | random | 49/49 | 0 | not reached | 0 | 0.777 | 0.0 |
| pedestrian_crossing | optuna | 49/49 | 3 | not reached | 1 | 0.803 | 0.0 |
| pedestrian_ego_speed | rules | 30/50 | 17 | 25 | 5 | 1.0 | 0.0 |
| pedestrian_ego_speed | hybrid | 30/50 | 18 | 24 | 5 | 1.0 | 46.0 |
| pedestrian_ego_speed | llm | 30/50 | 18 | 28 | 5 | 1.0 | 52.5 |
| pedestrian_ego_speed | random | 48/50 | 31 | not reached | 0 | 1.0 | 0.0 |

## controller_tuning_pedestrian

Does the tuned linear MPC (feasible_best: Riccati terminal cost, stiffer position tracking) fail less often than the default linear MPC when the key pedestrian steps out up to 2 s early and walks 1x to 2x their recorded speed?

- **hybrid**: linear fails less than feasible_best: the pooled 90% ranges separate

## cut_in_merge

In merge and cut-in scenes, which timings and speeds of the other cars make the VaVAM policy collide or leave the road? Find the 5 most challenging settings, each on a different scene and confirmed by repeats.

- **rules**: 023b7fcc at actor_time_shift_s 0.0, actor_speed_scale 1.25; 054b5901 at actor_time_shift_s 0.0, actor_speed_scale 1.25; 09a95ffa at actor_time_shift_s 0.0, actor_speed_scale 1.25; 0e899dd3 at actor_time_shift_s 0.0, actor_speed_scale 1.25; 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.25
- **hybrid**: 054b5901 at actor_time_shift_s 0, actor_speed_scale 1.25; 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1.25; 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25; 09a95ffa at actor_time_shift_s 0, actor_speed_scale 1.25; 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 1.25
- **llm**: 054b5901 at actor_time_shift_s -0.5, actor_speed_scale 1.25; 023b7fcc at actor_time_shift_s 0, actor_speed_scale 1.25; 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25; 09a95ffa at actor_time_shift_s -1, actor_speed_scale 1.5; 0e899dd3 at actor_time_shift_s -1, actor_speed_scale 1.5

## ego_speed_smoke

Does the ego speed knob land and pass the gate on a real run at each value?

- **grid**: nothing confirmed

## intersection

At intersections with crossing traffic, which arrival times and speeds of the recorded crossing car make the VaVAM policy collide or leave the road? Find the 5 most challenging settings, each on a different scene, confirmed by repeats.

- **rules**: nothing confirmed
- **hybrid**: 02eadd92 at actor_time_shift_s 1, actor_speed_scale 1.25
- **llm**: nothing confirmed

## lead_vehicle

In lead-vehicle scenes, which timing shifts and speed scalings of the recorded lead car (with up to 200 ms planner delay if needed) make VaVAM run into it? Find the 5 most challenging cases, each on a different scene, confirmed by repeats.

- **rules**: 19f339ba at actor_time_shift_s 0.0, actor_speed_scale 1.25, planner_delay_us 200000
- **hybrid**: 0e899dd3 at actor_time_shift_s 0, actor_speed_scale 0.75, planner_delay_us 200000; 12855a41 at actor_time_shift_s 0, actor_speed_scale 0.75, planner_delay_us 200000; 09a95ffa at actor_time_shift_s 0, actor_speed_scale 0.75, planner_delay_us 200000; 19f339ba at actor_time_shift_s 0, actor_speed_scale 1.25, planner_delay_us 200000
- **llm**: 023b7fcc at actor_time_shift_s 1, actor_speed_scale 0.5, planner_delay_us 0; 19f339ba at actor_time_shift_s 1, actor_speed_scale 0.5, planner_delay_us 0; 096988dd at actor_time_shift_s 1, actor_speed_scale 0.5, planner_delay_us 0; 09a95ffa at actor_time_shift_s 1, actor_speed_scale 0.5, planner_delay_us 0; 12855a41 at actor_time_shift_s 1, actor_speed_scale 0.5, planner_delay_us 0

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
- **hybrid**: 048b974e at ego_speed_scale 1, actor_time_shift_s 0; 18d28973 at ego_speed_scale 1, actor_time_shift_s 0; 1bbe02fc at ego_speed_scale 1, actor_time_shift_s 0; 07981e6a at ego_speed_scale 1, actor_time_shift_s 0; 0caa8f1a at ego_speed_scale 1, actor_time_shift_s 0
- **llm**: 048b974e at ego_speed_scale 1.2, actor_time_shift_s -0.5; 18d28973 at ego_speed_scale 1.2, actor_time_shift_s -0.5; 1bbe02fc at ego_speed_scale 1.2, actor_time_shift_s -1; 0d4893f5 at ego_speed_scale 1.2, actor_time_shift_s -0.5; 0e002edd at ego_speed_scale 1.4, actor_time_shift_s -0.5
- **random**: nothing confirmed
