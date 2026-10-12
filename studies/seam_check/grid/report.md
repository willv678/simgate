# With the warm-up seam fix applied, does every ego speed on 07981e6a pass the physics gate?

Study `grid`: 5 kept runs on 1 scenes, varying ego_speed_scale; 0 runs not kept by the gate. Counts are kept runs only.

**Goal:** none that code can check; the study ran its budget.

## Answer

Yes. Every ego speed from 0.6x to 1.4x on 07981e6a passed the physics gate. That includes 1.2x, the setting that halted before. Every run passed every validity check, and no run was dropped, so the warm-up seam fix held in simulation. This rests on one run per speed. It shows the seam stays within the physics bound for this scene, but it doesn't measure how often a later run might fail the gate. Apart from the gate, every run crashed. Triage blames the policy in each case, not the simulator: after handoff the ego drifted left into the parked cars even though the route command was RIGHT.

## Findings

- The warm-up seam fix held: the run at each speed (0.6x, 0.8x, 1.0x, 1.2x, 1.4x) passed every validity check, including the physics gate, and no run was dropped. That includes 1.2x, where the seam once reached 10.7 m/s^2 and halted both runs.
  - S1: 07981e6a at ego_speed_scale 0.6: 1/1 failed, rate 27%-100% (90%) (seam_check_grid_001)
  - S2: 07981e6a at ego_speed_scale 0.8: 1/1 failed, rate 27%-100% (90%) (seam_check_grid_002)
  - S3: 07981e6a at ego_speed_scale 1.0: 1/1 failed, rate 27%-100% (90%) (seam_check_grid_003)
  - S4: 07981e6a at ego_speed_scale 1.2: 1/1 failed, rate 27%-100% (90%) (seam_check_grid_004)
  - S5: 07981e6a at ego_speed_scale 1.4: 1/1 failed, rate 27%-100% (90%) (seam_check_grid_005)
- The run at every speed ended in a collision, and none of these failures is flagged as a possible simulator artifact. With one run per speed, this only hints at a failure rate. It does not measure one.
  - S1: 07981e6a at ego_speed_scale 0.6: 1/1 failed, rate 27%-100% (90%) (seam_check_grid_001)
  - S2: 07981e6a at ego_speed_scale 0.8: 1/1 failed, rate 27%-100% (90%) (seam_check_grid_002)
  - S3: 07981e6a at ego_speed_scale 1.0: 1/1 failed, rate 27%-100% (90%) (seam_check_grid_003)
  - S4: 07981e6a at ego_speed_scale 1.2: 1/1 failed, rate 27%-100% (90%) (seam_check_grid_004)
  - S5: 07981e6a at ego_speed_scale 1.4: 1/1 failed, rate 27%-100% (90%) (seam_check_grid_005)
- The policy caused the crashes, not the simulator or the warm-up. After handoff the ego drifted left into the parking lane along the left curb, even though the route command was RIGHT and the recorded path stayed right. It then hit the parked cars with little or no braking. At 0.6x it stayed at the left edge of its own lane and its planned path bent left into the parked cars. At 0.8x and above it left its lane completely.
  - S1: 07981e6a at ego_speed_scale 0.6: 1/1 failed, rate 27%-100% (90%) (seam_check_grid_001)
  - S2: 07981e6a at ego_speed_scale 0.8: 1/1 failed, rate 27%-100% (90%) (seam_check_grid_002)
  - S3: 07981e6a at ego_speed_scale 1.0: 1/1 failed, rate 27%-100% (90%) (seam_check_grid_003)
  - S4: 07981e6a at ego_speed_scale 1.2: 1/1 failed, rate 27%-100% (90%) (seam_check_grid_004)
  - S5: 07981e6a at ego_speed_scale 1.4: 1/1 failed, rate 27%-100% (90%) (seam_check_grid_005)

## Open

- How reliable the fix is: one run per speed shows the gate can pass at each speed, but not how often it does. Repeating several runs at 1.2x and its neighbours (1.0x, 1.4x) would show whether the seam ever comes near the physics bound again.
- Why the policy drifts left on 07981e6a at every speed when told to go RIGHT: more runs per speed, or a different controller on the same scene, would show whether this crash happens every time and whether it comes from this policy alone.

## Why the runs failed (triage from the video and log)

left_road 4, turned_into_actor 1

- seam_check_grid_001: turned_into_actor, policy at fault: yes. The route went straight and then right, along the right lane. Instead of following it, the ego stayed on the left edge of its lane and its planned path bent left toward the parked cars, with no braking (speed rose from 6.4 to 7.1 m/s). At 6.6 s its front hit the line of parked cars on the left (actors 15/31, gap to the car ahead closing to 2.7 m), while the logged trajectory stayed in the clear lane to the right.
- seam_check_grid_002: left_road, policy at fault: yes. After the 4.6 s handoff, the ego sped up from about 8.6 to 9.4 m/s on a narrow residential street. Its planned path (orange) hugged the left curb instead of following the lane. By 6.8 s the ego had drifted about 1.6 m off the recorded human path into the left parking lane and hit parked car 31 with its front. The route command was RIGHT.
- seam_check_grid_003: left_road, policy at fault: yes. After handoff, the ego drifted left out of its travel lane into the parking lane along the left curb. The recorded path stayed right and set up the upcoming right turn (command RIGHT). The ego kept going about 10–11 m/s toward the line of parked cars, the gap closing from 37.6 m to 4.1 m with barely any braking, and its front hit the parked car (id 6) at 7.5 s.
- seam_check_grid_004: left_road, policy at fault: yes. After handoff, the ego drifted left out of its travel lane into the parked-car lane at the curb. The route command was RIGHT, and the recorded path stays in the right lane before turning right. The ego kept going about 11–12 m/s along its planned path through the parking lane and hit parked car 6 head-on as the gap closed from 45 m to 4 m with almost no braking.
- seam_check_grid_005: left_road, policy at fault: yes. After handoff the ego (about 13–14 m/s) drifted left out of its travel lane into the parking lane on the left. That path ran straight into the row of parked cars (6, 3, 87), and the ego hit parked car 6 from behind, only slowing from about 14.6 to 12.2 m/s. Meanwhile the route command was RIGHT and the planned path turned right at the intersection ahead.

## Every setting

- S1: 07981e6a at ego_speed_scale 0.6: 1/1 failed, rate 27%-100% (90%) (seam_check_grid_001)
- S2: 07981e6a at ego_speed_scale 0.8: 1/1 failed, rate 27%-100% (90%) (seam_check_grid_002)
- S3: 07981e6a at ego_speed_scale 1.0: 1/1 failed, rate 27%-100% (90%) (seam_check_grid_003)
- S4: 07981e6a at ego_speed_scale 1.2: 1/1 failed, rate 27%-100% (90%) (seam_check_grid_004)
- S5: 07981e6a at ego_speed_scale 1.4: 1/1 failed, rate 27%-100% (90%) (seam_check_grid_005)

## Provenance

Plan: `plan.json` (rationale: Written by hand to re-check the warm-up seam fix (problem 24) in a simulation.). Report written by claude-opus-5-5 from `results` in 10 s; every count above is computed from the queue, not written by the model.

0 of 5 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
