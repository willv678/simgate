# On scene clipgt-02eadd92-02f1-46d8-86fe-a9e338fed0b6, is the failure rate at 150 ms of planner delay clearly higher than at 100 ms, so that their 90% intervals do not overlap?

Study `confirm_break_02eadd92`: 8 kept runs on 1 scenes, varying planner_delay_us; 0 runs not kept by the gate. Counts are kept runs only.

## Answer

Not confirmed. Every run at 150 ms failed, but runs at 100 ms failed as well, so the 90% ranges at 100 ms and 150 ms still overlap (S1, S2). This goes against the pilot, which saw 100 ms pass every time, so a sharp break between 100 ms and 150 ms is in doubt. It is not clearly refuted either, because with so few runs both ranges are wide. Both 100 ms failures are flagged as possible simulator artifacts (the ego was over 3.5 m from the recorded trajectory), even though triage blames the policy. The case against a clean break therefore rests partly on runs the simulator may explain.

## Findings

- At 150 ms, every run failed, and each failure was the policy's fault. The ego was in the lane of car 22, which was slowing for a red light. It braked too gently and hit the car from behind (no_brake_for_lead). None of these failures is flagged as a possible artifact.
  - S2: 02eadd92 at planner_delay_us 150000: 4/4 failed, rate 60%-100% (90%) (confirm_break_02eadd92_003, confirm_break_02eadd92_004, confirm_break_02eadd92_007, confirm_break_02eadd92_008)
- At 100 ms, some runs failed, against the pilot's finding that every run passed. Both failures had the same cause: the ego ran about 5 m left of the recorded path with a RIGHT command, steered or drifted right, and clipped slow car 22 in the next lane (turned_into_actor). Triage blames the policy.
  - S1: 02eadd92 at planner_delay_us 100000: 2/4 failed, rate 18%-82% (90%), 2 possibly the simulator's (confirm_break_02eadd92_001, confirm_break_02eadd92_002, confirm_break_02eadd92_005, confirm_break_02eadd92_006)
- Both failures at 100 ms are flagged as possible artifacts because the ego was over 3.5 m from the recorded trajectory. This is where the simulator's rendering is less reliable, so these failures are weaker evidence than the ones at 150 ms.
  - S1: 02eadd92 at planner_delay_us 100000: 2/4 failed, rate 18%-82% (90%), 2 possibly the simulator's (confirm_break_02eadd92_001, confirm_break_02eadd92_002, confirm_break_02eadd92_005, confirm_break_02eadd92_006)
- The failure mode differs between the two delays: side contact while moving toward the right turn at 100 ms, rear-ending a braking lead car at 150 ms. This suggests the delay changes how the scene fails, not only whether it fails.
  - S1: 02eadd92 at planner_delay_us 100000: 2/4 failed, rate 18%-82% (90%), 2 possibly the simulator's (confirm_break_02eadd92_001, confirm_break_02eadd92_002, confirm_break_02eadd92_005, confirm_break_02eadd92_006)
  - S2: 02eadd92 at planner_delay_us 150000: 4/4 failed, rate 60%-100% (90%) (confirm_break_02eadd92_003, confirm_break_02eadd92_004, confirm_break_02eadd92_007, confirm_break_02eadd92_008)
- The 90% range of the failure rate at 100 ms overlaps the range at 150 ms, so the win condition is not met.
  - S1: 02eadd92 at planner_delay_us 100000: 2/4 failed, rate 18%-82% (90%), 2 possibly the simulator's (confirm_break_02eadd92_001, confirm_break_02eadd92_002, confirm_break_02eadd92_005, confirm_break_02eadd92_006)
  - S2: 02eadd92 at planner_delay_us 150000: 4/4 failed, rate 60%-100% (90%) (confirm_break_02eadd92_003, confirm_break_02eadd92_004, confirm_break_02eadd92_007, confirm_break_02eadd92_008)

## Open

- Is the failure rate at 100 ms really above zero, or are its failures caused by the ego drifting into a lane the simulator renders poorly? Repeating runs at 100 ms, and checking the video of confirm_break_02eadd92_005 and _006 for rendering quality in the left lane, would settle this.
- Why does the ego end up 3–5 m left of the recorded path at both delays? If it starts or drifts into the wrong lane regardless of delay, the scene may be testing lane choice rather than latency. Runs at 0 ms in this study's setup would show whether that drift happens with no delay.
- Pooling with the pilot's runs, as the plan suggested, is no longer appropriate for confirmation, because this study's runs at 100 ms disagree with the pilot. More runs at 100 ms would be needed to narrow its range enough to tell whether it overlaps 150 ms clearly.
- The study cannot place the break more precisely than between 100 ms and 150 ms, because the knob has no values in between.

## Why the runs failed (triage from the video and log)

no_brake_for_lead 4, turned_into_actor 2

- confirm_break_02eadd92_003: no_brake_for_lead, policy at fault: yes. The ego was about 3 m left of the recorded path, in the lane with car 22, which was slowing toward a red light at the intersection; the human had driven in the lane to its right. The camera showed the lead car clearly, but the ego braked too gently (8.7 to 4.8 m/s while the gap shrank from 27 m to under 5 m) and hit car 22 from behind.
- confirm_break_02eadd92_004: no_brake_for_lead, policy at fault: yes. The ego was about 3 m left of the recorded path, in the lane behind vehicle 22, which was slowing for a red light at the intersection. The ego only eased off gradually, from 8.8 to 3.7 m/s, while the gap shrank from 25 m to 4 m, and it hit 22 from behind.
- confirm_break_02eadd92_005: turned_into_actor, policy at fault: yes. With a RIGHT command, the ego was in a lane about 5 m left of the recorded path. Approaching the intersection, it steered right toward the turn and its front-right corner hit actor 22, a car that was slow or stopped in the lane to its right near the stop line. The ego had slowed from 8 to about 5 m/s but kept moving right into that car instead of yielding or waiting behind it.
- confirm_break_02eadd92_006: turned_into_actor, policy at fault: yes. The route says RIGHT and the recorded drive stays in the right lane, but the ego went straight about 5 m to the left of it. Slowing from 8.5 to 5.4 m/s, it drove up beside slow vehicle 22 in the next lane to the right and clipped it with its front-right side at 10.8 s. Vehicle 22 drifts slightly left in the frames, but the ego's lane choice and tight lateral clearance are what made the contact happen.
- confirm_break_02eadd92_007: no_brake_for_lead, policy at fault: yes. The ego was approaching a red light in the same lane as car 22, which was nearly stopped at the stop line. The recorded human path was one lane to the right. Over 3 s the gap closed from 26 m to 4.4 m, but the ego only eased from 8.7 to 4.6 m/s, and its planned path ran straight into the car, so it hit it from behind.
- confirm_break_02eadd92_008: no_brake_for_lead, policy at fault: yes. The ego was about 3 m left of the recorded path, sharing a lane with car 22, which was slowing for a red light. Its route command was RIGHT. It braked only gradually, from 8.5 to 3.8 m/s, while the gap to car 22 shrank from 24 m to near zero, and it rear-ended car 22 at about 3.8 m/s. The lead car was clearly visible in the camera the whole time.

## Every setting

- S1: 02eadd92 at planner_delay_us 100000: 2/4 failed, rate 18%-82% (90%), 2 possibly the simulator's (confirm_break_02eadd92_001, confirm_break_02eadd92_002, confirm_break_02eadd92_005, confirm_break_02eadd92_006)
- S2: 02eadd92 at planner_delay_us 150000: 4/4 failed, rate 60%-100% (90%) (confirm_break_02eadd92_003, confirm_break_02eadd92_004, confirm_break_02eadd92_007, confirm_break_02eadd92_008)

## Provenance

Plan: `plan.json` (rationale: The brief limits the study to one scene, one knob and 8 runs as 2 rounds of 4. The plan follows that exactly, well within the caps of 60 runs and 10 per round. The scene passed in the earlier run at 0 delay, with 1.4 m clearance and 0.92 progress, so a delay effect can show there. Putting every run at the two delays that bracket the break gives at most 4 runs each, which is the most this budget allows.

Limits the researcher should know:
1. Even in the best case (4 passes out of 4 at 100 ms, 4 failures out of 4 at 150 ms), whether the 90% ranges separate depends on how they are calculated. Wilson intervals separate (upper ~0.40 against lower ~0.60). Exact Clopper-Pearson intervals still overlap slightly (upper ~0.53 against lower ~0.47). To confirm under the stricter method, this study's runs must be pooled with the pilot's runs at 100 ms and 150 ms; with 6 consistent runs per side, Clopper-Pearson separates (~0.39 against ~0.61). The researcher should decide the interval method and whether to pool before reading the result.
2. A single run that goes against the pilot at either delay would almost certainly leave the intervals overlapping at this sample size. That is closer to "not confirmed" than to a clear refutation, because 8 runs cannot show that the rates overlap clearly either.
3. The study can only say the break lies between 100 ms and 150 ms, because the knob has no values in between.
4. The 40-minute limit cannot be checked from the inputs. It assumes roughly 5 minutes per run, and 2 rounds keep the number of proposer turns low.). Report written by claude-opus-5-5 from `results` in 14 s; every count above is computed from the queue, not written by the model.
