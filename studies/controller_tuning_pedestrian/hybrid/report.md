# Does the tuned linear MPC (feasible_best: Riccati terminal cost, stiffer position tracking) fail less often than the default linear MPC when the key pedestrian steps out up to 2 s early and walks 1x to 2x their recorded speed?

Study `hybrid`: 10 kept runs on 4 scenes, varying actor_time_shift_s, actor_speed_scale, every setting on linear (a) and feasible_best (b); 1 runs not kept by the gate. Counts are kept runs only.

**Goal (checked by code, not the model):** linear fails less than feasible_best: the pooled 90% ranges separate. Pooled over paired runs: linear 0/5 failed, rate 0%-35% (90%); feasible_best 5/5 failed, rate 65%-100% (90%). Sign test over the pairs where one failed: only linear 0, only feasible_best 5, two-sided p = 0.062, after 1 rounds.

## Answer

No. The tuned MPC (feasible_best) was less safe than the default linear MPC. The pooled 90% ranges separate, so the study stopped after its first round: feasible_best failed on every pair and linear on none. The exact sign test lands just above 0.05, though, so the result is strong but rests on few pairs. Two caveats limit what this says about early pedestrians. First, every pair ran at a single timing: no time shift (0 s) and 1.25x walking speed. The early step-outs of up to 2 s were never tested. Second, none of the feasible_best failures involved the pedestrian. In each one the ego steered wrongly at a RIGHT command, either turning too sharply into parked cars or veering left off the road. Every one was flagged as a possible simulator artifact because the ego ended far from the recorded path, but triage of the videos and logs blames the policy, not the rendering. So feasible_best seems to fail on these scenes whatever the pedestrian does, not because the pedestrian steps out early.

## Findings

- At 0 s shift and 1.25x speed, feasible_best failed in all four scenes and the default linear MPC passed in all four. Every pair split the same way, with only feasible_best failing.
  - S1: 0b10bce8 at actor_time_shift_s 0, actor_speed_scale 1.25: linear 0/1 failed, rate 0%-73% (90%) (controller_tuning_pedestrian_hybrid_004_linear); feasible_best 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (controller_tuning_pedestrian_hybrid_004_feasible_best)
  - S2: 0e002edd at actor_time_shift_s 0, actor_speed_scale 1.25: linear 0/2 failed, rate 0%-58% (90%) (controller_tuning_pedestrian_hybrid_001_linear, controller_tuning_pedestrian_hybrid_005_linear_a2); feasible_best 2/2 failed, rate 42%-100% (90%), 2 possibly the simulator's (controller_tuning_pedestrian_hybrid_001_feasible_best, controller_tuning_pedestrian_hybrid_005_feasible_best)
  - S3: 12a09194 at actor_time_shift_s 0, actor_speed_scale 1.25: linear 0/1 failed, rate 0%-73% (90%) (controller_tuning_pedestrian_hybrid_003_linear); feasible_best 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (controller_tuning_pedestrian_hybrid_003_feasible_best)
  - S4: 18f8dbd6 at actor_time_shift_s 0, actor_speed_scale 1.25: linear 0/1 failed, rate 0%-73% (90%) (controller_tuning_pedestrian_hybrid_002_linear); feasible_best 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (controller_tuning_pedestrian_hybrid_002_feasible_best)
- feasible_best failed on scene 0e002edd in both pairs run there. Both times it took the right turn too sharply and drove into the parked cars at the far curb. The policy was at fault, and the pedestrian was not involved.
  - S2: 0e002edd at actor_time_shift_s 0, actor_speed_scale 1.25: linear 0/2 failed, rate 0%-58% (90%) (controller_tuning_pedestrian_hybrid_001_linear, controller_tuning_pedestrian_hybrid_005_linear_a2); feasible_best 2/2 failed, rate 42%-100% (90%), 2 possibly the simulator's (controller_tuning_pedestrian_hybrid_001_feasible_best, controller_tuning_pedestrian_hybrid_005_feasible_best)
- On scenes 0b10bce8, 12a09194 and 18f8dbd6, feasible_best left the road. Despite a RIGHT command it steered left across lanes or the crosswalk and onto the curb or sidewalk. Triage found the camera view clean before the drift in two of these runs and judged the smearing in the third (12a09194) to be a result of the drift, not its cause.
  - S1: 0b10bce8 at actor_time_shift_s 0, actor_speed_scale 1.25: linear 0/1 failed, rate 0%-73% (90%) (controller_tuning_pedestrian_hybrid_004_linear); feasible_best 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (controller_tuning_pedestrian_hybrid_004_feasible_best)
  - S3: 12a09194 at actor_time_shift_s 0, actor_speed_scale 1.25: linear 0/1 failed, rate 0%-73% (90%) (controller_tuning_pedestrian_hybrid_003_linear); feasible_best 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (controller_tuning_pedestrian_hybrid_003_feasible_best)
  - S4: 18f8dbd6 at actor_time_shift_s 0, actor_speed_scale 1.25: linear 0/1 failed, rate 0%-73% (90%) (controller_tuning_pedestrian_hybrid_002_linear); feasible_best 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (controller_tuning_pedestrian_hybrid_002_feasible_best)
- feasible_best also failed on 12a09194, where linear's criticality was 0 and the pedestrian likely never reaches the ego's path. This supports the reading that feasible_best's failures come from its own path tracking, not from the pedestrian's timing.
  - S3: 12a09194 at actor_time_shift_s 0, actor_speed_scale 1.25: linear 0/1 failed, rate 0%-73% (90%) (controller_tuning_pedestrian_hybrid_003_linear); feasible_best 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (controller_tuning_pedestrian_hybrid_003_feasible_best)
- Every feasible_best failure was flagged as a possible artifact because the ego ended over 3.5 m from the recorded trajectory. Triage, however, attributes all of them to the policy.
  - S1: 0b10bce8 at actor_time_shift_s 0, actor_speed_scale 1.25: linear 0/1 failed, rate 0%-73% (90%) (controller_tuning_pedestrian_hybrid_004_linear); feasible_best 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (controller_tuning_pedestrian_hybrid_004_feasible_best)
  - S2: 0e002edd at actor_time_shift_s 0, actor_speed_scale 1.25: linear 0/2 failed, rate 0%-58% (90%) (controller_tuning_pedestrian_hybrid_001_linear, controller_tuning_pedestrian_hybrid_005_linear_a2); feasible_best 2/2 failed, rate 42%-100% (90%), 2 possibly the simulator's (controller_tuning_pedestrian_hybrid_001_feasible_best, controller_tuning_pedestrian_hybrid_005_feasible_best)
  - S3: 12a09194 at actor_time_shift_s 0, actor_speed_scale 1.25: linear 0/1 failed, rate 0%-73% (90%) (controller_tuning_pedestrian_hybrid_003_linear); feasible_best 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (controller_tuning_pedestrian_hybrid_003_feasible_best)
  - S4: 18f8dbd6 at actor_time_shift_s 0, actor_speed_scale 1.25: linear 0/1 failed, rate 0%-73% (90%) (controller_tuning_pedestrian_hybrid_002_linear); feasible_best 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (controller_tuning_pedestrian_hybrid_002_feasible_best)

## Open

- Pedestrians stepping out early were never tested. Every pair used a 0 s shift and 1.25x speed, so the study does not show how either controller handles shifts of -0.5 to -2.0 s or speeds up to 2.0x. Pairs at, say, -1.0 s and -2.0 s with 1.5x and 2.0x on 0e002edd and 18f8dbd6 would settle this.
- Does feasible_best fail on these scenes even with the pedestrian left as recorded (0 s shift, 1.0x speed)? If it does, its failures are a baseline steering problem at right turns and have nothing to do with the pedestrian. A paired baseline run on each of the four scenes would settle this.
- Repeat runs would show whether feasible_best's failures are consistent or occasional. So far each setting has only one or two pairs, which is a hint rather than a per-scene rate. Two or three more pairs per scene would settle this.
- One linear run on 0e002edd (hybrid_005_linear) was not kept and had to be re-run. Its replacement passed, but the reason the gate rejected the first run is not recorded here.

## Why the runs failed (triage from the video and log)

left_road 3, turned_into_actor 2

- controller_tuning_pedestrian_hybrid_001_feasible_best: turned_into_actor, policy at fault: yes. With a RIGHT command at the intersection, the ego turned right too sharply, accelerating from 3 to 4.4 m/s, and drove onto the curb lane. It hit the parked cars along the right side of the cross street (actors 16/90) at the curb. The recorded human path stayed wider, and the ego ended 6.7 m off it.
- controller_tuning_pedestrian_hybrid_002_feasible_best: left_road, policy at fault: yes. The route command was RIGHT and the planned path went straight or bore right. Instead, the ego (≈9–10 m/s) steered left across several lanes. It went through the row of parked cars (34/52/54) on the far left and onto the sidewalk/building frontage, ending 11 m from the human trajectory. The camera view was clean at 5.3 s, so the drift came from the policy, not from a broken render.
- controller_tuning_pedestrian_hybrid_003_feasible_best: left_road, policy at fault: yes. The route command was RIGHT, but the ego ended up on the far left edge of a multi-lane diagonal road, about 14 m from the recorded path, which runs several lanes to the right. Its planned path pointed up and left, across the road boundary toward a pedestrian on the sidewalk. The ego slowed from 9.7 to 2.5 m/s but still crossed the left boundary onto the curb and sidewalk at 9.5 s. The camera view was already smeared at 7.5 s, but by then the ego was far from the recorded path, so the smearing is more likely a result of the drift than its cause.
- controller_tuning_pedestrian_hybrid_004_feasible_best: left_road, policy at fault: yes. The ego started from near a stop at the intersection with a RIGHT command and a route going ahead and to the right, but it steered hard left instead. It crossed the crosswalk and sidewalk and ended off the road facing a roadside fence at 3.6 m/s, 5.2 m from the human trajectory. The camera view looked clean before the failure, so a rendering problem doesn't explain it.
- controller_tuning_pedestrian_hybrid_005_feasible_best: turned_into_actor, policy at fault: yes. The ego was following a RIGHT command through the intersection, though the human recording continued nearly straight. It turned far too sharply, crossed the whole cross street, and at about 4 m/s drove nose-first into the parked cars (ids 90/16) at the far curb, leaving the drivable area.

## Every setting

- S1: 0b10bce8 at actor_time_shift_s 0, actor_speed_scale 1.25: linear 0/1 failed, rate 0%-73% (90%) (controller_tuning_pedestrian_hybrid_004_linear); feasible_best 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (controller_tuning_pedestrian_hybrid_004_feasible_best)
- S2: 0e002edd at actor_time_shift_s 0, actor_speed_scale 1.25: linear 0/2 failed, rate 0%-58% (90%) (controller_tuning_pedestrian_hybrid_001_linear, controller_tuning_pedestrian_hybrid_005_linear_a2); feasible_best 2/2 failed, rate 42%-100% (90%), 2 possibly the simulator's (controller_tuning_pedestrian_hybrid_001_feasible_best, controller_tuning_pedestrian_hybrid_005_feasible_best)
- S3: 12a09194 at actor_time_shift_s 0, actor_speed_scale 1.25: linear 0/1 failed, rate 0%-73% (90%) (controller_tuning_pedestrian_hybrid_003_linear); feasible_best 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (controller_tuning_pedestrian_hybrid_003_feasible_best)
- S4: 18f8dbd6 at actor_time_shift_s 0, actor_speed_scale 1.25: linear 0/1 failed, rate 0%-73% (90%) (controller_tuning_pedestrian_hybrid_002_linear); feasible_best 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (controller_tuning_pedestrian_hybrid_002_feasible_best)

## Not kept by the gate

- controller_tuning_pedestrian_hybrid_005_linear: not kept: RE-RUN

## Provenance

Plan: `plan.json` (rationale: This is an A/B study of linear (a) against feasible_best (b). Each setting runs once on each controller with the same scene and knob values, so only the tuning differs. Traffic is replayed so both controllers face the same scripted scenario. Only the key pedestrian is retimed: retime_class is person, and retime_tracks names one pedestrian per scene. The two varied knobs are actor_time_shift_s and actor_speed_scale. The brief's range is -2.0 to 0.0 s and 1.0x to 2.0x. The objective holds the proposer to that range, because the knobs' legal values go beyond it. Delay, lateral bias and waypoint noise stay at their defaults of 0, so there is no delay and no perception error.

Scenes: there are 12 scenes tagged pedestrian_crossing. Six already failed at 0 delay and are left out, as the brief asks: 048b974e, 07981e6a, 0caa8f1a, 0d4893f5, 18d28973 and 1bbe02fc. Two others list no pedestrian key actor, so there is no key pedestrian to retime: 095cf563 and 13a9767e. That leaves 4 scenes:
- 0e002edd (pedestrian 12): closest approach 0.15 m.
- 18f8dbd6 (pedestrian 97): closest approach 0.9 m.
- 12a09194 (pedestrian 123): closest approach to any actor was 11.5 m, so its pedestrian may never reach the ego's path even when retimed.
- 0b10bce8 (pedestrian 32): in the earlier run the ego drove only 8.9 m (progress 0.11), so it may never reach the crossing.

The last two scenes may never fail on either controller. Those runs say nothing about which controller is safer, and the proposer is told to move away from such settings.

Budget: 5 rounds × 5 settings × 2 controllers = 50 runs, the brief's figure and within the cap of 60. The goal is compare. The study stops early if the 90% ranges of the two pooled failure rates separate. Otherwise it reports that no difference was shown, along with the exact sign test over pairs where only one controller failed.

Limits:
- With 25 pairs and few scenes, only a large difference between the controllers is likely to show up.
- The result applies only to these 4 scenes and these pedestrians.
- A single earlier run is a weak basis for calling a scene "not failing at baseline": one sample can pass once and fail the next time.
- Retiming a pedestrian in replay cannot make the pedestrian react to the ego.). Report written by claude-opus-5-5 from `results` in 16 s; every count above is computed from the queue, not written by the model.

11 of 11 queued runs are seeded (`seed` in the run's queue config); `replay.py` queues a kept one again with it.
