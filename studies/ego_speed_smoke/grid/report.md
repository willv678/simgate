# Does the ego speed knob land and pass the gate on a real run at each value?

Study `grid`: 5 kept runs on 1 scenes, varying ego_speed_scale; 0 runs not kept by the gate. Counts are kept runs only.

**Goal:** none that code can check; the study ran its budget.

## Answer

Partly. At every ego_speed_scale value from 0.6 to 1.4, the run on this pedestrian scene passed the gate and was kept, and the gate rejected no runs. The results do not show whether the knob actually changed the ego's speed, because they contain no measured speed to compare across values. The only hint is criticality: it was slightly higher at 0.6, identical at 0.8, 1.0 and 1.2, and highest at 1.4. The single failure, at 1.4, is flagged as a possible simulator artifact because the ego ended up more than 3.5 m from the recorded path. But triage of the video shows the policy itself left the path and turned into a parked car. With one run per value, this is a hint and not a failure rate.

## Findings

- Every ego_speed_scale value (0.6, 0.8, 1.0, 1.2, 1.4) produced a run that passed every validity check and was kept. The gate rejected no runs.
  - S1: 0e002edd at ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (ego_speed_smoke_grid_001)
  - S2: 0e002edd at ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (ego_speed_smoke_grid_002)
  - S3: 0e002edd at ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (ego_speed_smoke_grid_003)
  - S4: 0e002edd at ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (ego_speed_smoke_grid_004)
  - S5: 0e002edd at ego_speed_scale 1.4: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (ego_speed_smoke_grid_005)
- The runs at 0.6 through 1.2 did not fail. With only one run each, this rules out a very high failure rate but says little more.
  - S1: 0e002edd at ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (ego_speed_smoke_grid_001)
  - S2: 0e002edd at ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (ego_speed_smoke_grid_002)
  - S3: 0e002edd at ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (ego_speed_smoke_grid_003)
  - S4: 0e002edd at ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (ego_speed_smoke_grid_004)
- The run at 1.4 failed because the policy was at fault. At the intersection the ego left the recorded straight-through path, turned sharply into the lane of parked cars, hit a parked car and mounted the curb. It was flagged as a possible artifact only because it ended up about 7 m off the recorded path, and the video shows that deviation was the policy's own manoeuvre, not a rendering problem.
  - S5: 0e002edd at ego_speed_scale 1.4: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (ego_speed_smoke_grid_005)
- Criticality was identical at 0.8, 1.0 and 1.2 and differed only at 0.6 and 1.4. This hints that the knob may have had little effect across the middle of the range. It does not confirm that the knob changed the ego's speed.
  - S2: 0e002edd at ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (ego_speed_smoke_grid_002)
  - S3: 0e002edd at ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (ego_speed_smoke_grid_003)
  - S4: 0e002edd at ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (ego_speed_smoke_grid_004)
  - S1: 0e002edd at ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (ego_speed_smoke_grid_001)
  - S5: 0e002edd at ego_speed_scale 1.4: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (ego_speed_smoke_grid_005)

## Open

- Whether the knob actually changes the ego's speed: the results contain no measured ego speed. To settle it, check the logged ego speed (or its ratio to the recorded speed) in runs ego_speed_smoke_grid_001 to ego_speed_smoke_grid_005 against the target scale. The triaged run at 1.4 was turning at about 4 m/s, and that should be checked too.
- Whether 1.4 reliably causes this policy-at-fault turn into parked cars, or whether it was a one-off. Several more runs at 1.4 (and at 1.2) on this scene would show it.
- Whether runs at extreme speed values that leave the recorded path will routinely trip the possible-artifact flag (over 3.5 m off the path) even when the policy is at fault. If so, the artifact check may need calibrating before any study varies this knob.

## Why the runs failed (triage from the video and log)

turned_into_actor 1

- ego_speed_smoke_grid_005: turned_into_actor, policy at fault: yes. At the intersection, the ego left the recorded straight-through path (green line) and swung into a sharp turn across the intersection at about 4 m/s. It turned into the curbside lane of parked cars and hit parked car 90 with its front, mounting the curb toward the building, about 7 m off the recorded trajectory.

## Every setting

- S1: 0e002edd at ego_speed_scale 0.6: 0/1 failed, rate 0%-73% (90%) (ego_speed_smoke_grid_001)
- S2: 0e002edd at ego_speed_scale 0.8: 0/1 failed, rate 0%-73% (90%) (ego_speed_smoke_grid_002)
- S3: 0e002edd at ego_speed_scale 1.0: 0/1 failed, rate 0%-73% (90%) (ego_speed_smoke_grid_003)
- S4: 0e002edd at ego_speed_scale 1.2: 0/1 failed, rate 0%-73% (90%) (ego_speed_smoke_grid_004)
- S5: 0e002edd at ego_speed_scale 1.4: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (ego_speed_smoke_grid_005)

## Provenance

Plan: `plan.json` (rationale: Written by hand to calibrate the ego speed check on real runs before any study varies it.). Report written by claude-opus-5-5 from `results` in 13 s; every count above is computed from the queue, not written by the model.

0 of 5 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
