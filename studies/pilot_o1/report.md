# How does the policy's failure rate on each candidate scene change with planner delay in microseconds (camera frame to the controller receiving the plan made from it)? Find the fragile scenes and roughly where each breaks.

Study `pilot_o1`: 15 kept runs on 4 scenes, varying planner_delay_us; 0 runs not kept by the gate. Counts are kept runs only.

## Answer

Of the eight candidate scenes, only clipgt-02eadd92 looks sensitive to planner delay. It passed all 3 kept runs at 0 and 100,000 µs, then failed all 4 kept runs at 150,000 µs or more. That puts its break somewhere between 100,000 and 150,000 µs (100–150 ms), though only 1–2 runs back each setting. Two scenes failed with no delay at all: clipgt-01d503d4 failed every run (4 of 4, from 0 to 200,000 µs), and clipgt-026d6a39 failed its one run at 0 µs. Delay can't explain their failures. clipgt-023b7fcc gave mixed results from single runs, and four scenes were never run, so the study can't say whether they are fragile.

## Findings

- clipgt-02eadd92 breaks somewhere between 100,000 and 150,000 µs of planner delay. It passed every kept run at 0 and 100,000 µs and failed every kept run at 150,000, 200,000 and 400,000 µs. Each setting has only 1–2 runs, so the break point is a rough estimate, not a measured rate.
  - S8: 02eadd92 at planner_delay_us 0: 0/1 failed (o1_009)
  - S9: 02eadd92 at planner_delay_us 100000: 0/2 failed (o1_006, o1_013)
  - S10: 02eadd92 at planner_delay_us 150000: 2/2 failed (o1_011, o1_012)
  - S11: 02eadd92 at planner_delay_us 200000: 1/1 failed (o1_003)
  - S12: 02eadd92 at planner_delay_us 400000: 1/1 failed (o1_004)
- clipgt-01d503d4 failed every run, including with no delay (2 of 2 at 0 µs, then failed at 100,000 and 200,000 µs). The scene fails without any delay, so this is not a delay break point.
  - S1: 01d503d4 at planner_delay_us 0: 2/2 failed (o1_010, o1_014)
  - S2: 01d503d4 at planner_delay_us 100000: 1/1 failed (o1_007)
  - S3: 01d503d4 at planner_delay_us 200000: 1/1 failed (o1_001)
- clipgt-026d6a39 failed its only run, which had no delay. So far it looks like it fails without delay, not because of it, but one run is only a hint.
  - S7: 026d6a39 at planner_delay_us 0: 1/1 failed (o1_005)
- clipgt-023b7fcc gave no clear pattern: it passed at 200,000 µs, failed at 300,000 µs and passed at 400,000 µs, one run each. That mix suggests the outcome varies from run to run, and there is no evidence of a delay threshold.
  - S4: 023b7fcc at planner_delay_us 200000: 0/1 failed (o1_002)
  - S5: 023b7fcc at planner_delay_us 300000: 1/1 failed (o1_015)
  - S6: 023b7fcc at planner_delay_us 400000: 0/1 failed (o1_008)

## Open

- Four candidate scenes have no runs at all: clipgt-0245ff75, clipgt-02e075b9, clipgt-032b6f21 and clipgt-04394343. To learn whether any of them is fragile, run each at 0 µs and at about 200,000 µs.
- clipgt-02eadd92's break point needs pinning down: run about 3 times each at 100,000, 125,000 and 150,000 µs to narrow the threshold and confirm that 100,000 µs passes reliably.
- clipgt-023b7fcc: repeat runs at 300,000 and 400,000 µs (about 3 each) would show whether the 300,000 µs failure means anything or is run-to-run variation. A 0 µs run would give a baseline.
- clipgt-01d503d4 and clipgt-026d6a39 fail with no delay, so a delay sweep can't show a break point for them. More 0 µs runs for clipgt-026d6a39 would confirm it fails without delay. Both scenes' failures need checking for a cause that isn't delay, or the scenes should be left out of the delay study.

## Every setting

- S1: 01d503d4 at planner_delay_us 0: 2/2 failed (o1_010, o1_014)
- S2: 01d503d4 at planner_delay_us 100000: 1/1 failed (o1_007)
- S3: 01d503d4 at planner_delay_us 200000: 1/1 failed (o1_001)
- S4: 023b7fcc at planner_delay_us 200000: 0/1 failed (o1_002)
- S5: 023b7fcc at planner_delay_us 300000: 1/1 failed (o1_015)
- S6: 023b7fcc at planner_delay_us 400000: 0/1 failed (o1_008)
- S7: 026d6a39 at planner_delay_us 0: 1/1 failed (o1_005)
- S8: 02eadd92 at planner_delay_us 0: 0/1 failed (o1_009)
- S9: 02eadd92 at planner_delay_us 100000: 0/2 failed (o1_006, o1_013)
- S10: 02eadd92 at planner_delay_us 150000: 2/2 failed (o1_011, o1_012)
- S11: 02eadd92 at planner_delay_us 200000: 1/1 failed (o1_003)
- S12: 02eadd92 at planner_delay_us 400000: 1/1 failed (o1_004)

## Provenance

Plan: `plan.json` (rationale: fixed by the pilot script (run_pilot.sh), not planned from a brief). Report written by claude-opus-5-5 from `results` in 14 s; every count above is computed from the queue, not written by the model.
