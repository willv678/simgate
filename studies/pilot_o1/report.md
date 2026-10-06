# How does the policy's failure rate on each candidate scene change with planner delay in microseconds (camera frame to the controller receiving the plan made from it)? Find the fragile scenes and roughly where each breaks.

Study `pilot_o1`: 15 kept runs on 4 scenes, varying planner_delay_us; 0 runs not kept by the gate. Counts are kept runs only.

## Answer

Only one scene shows a failure rate that rises with planner delay. On clipgt-02eadd92 the policy passed all 3 runs at 0–100 ms (0–100000 µs) and failed all 4 runs at 150 ms and above, so it seems to break somewhere between 100 and 150 ms. That rests on 1–2 runs per setting: the 90% ranges at the two settings either side of the break (0–0.58 at 100 ms, 0.42–1.0 at 150 ms) don't overlap, but only just, and one of the 150 ms failures may be a simulator artifact. Scene clipgt-01d503d4 failed every run, including at zero delay, so it fails no matter the delay rather than because of it. The rest is inconclusive: clipgt-023b7fcc gave mixed single-run results (failed only at 300 ms), clipgt-026d6a39 had one failure at zero delay that may be the simulator's, and four of the eight candidate scenes were never run.

## Findings

- clipgt-02eadd92 passes at 0 and 100 ms planner delay but fails at 150 ms and above, so it seems to break between 100 and 150 ms (100000–150000 µs). This rests on 1–2 runs per setting, and one of the two 150 ms failures may be a simulator artifact.
  - S8: 02eadd92 at planner_delay_us 0: 0/1 failed, rate 0%-73% (90%) (o1_009)
  - S9: 02eadd92 at planner_delay_us 100000: 0/2 failed, rate 0%-58% (90%) (o1_006, o1_013)
  - S10: 02eadd92 at planner_delay_us 150000: 2/2 failed, rate 42%-100% (90%), 1 possibly the simulator's (o1_011, o1_012)
  - S11: 02eadd92 at planner_delay_us 200000: 1/1 failed, rate 27%-100% (90%) (o1_003)
  - S12: 02eadd92 at planner_delay_us 400000: 1/1 failed, rate 27%-100% (90%) (o1_004)
- clipgt-01d503d4 failed at every delay tested, including 0 µs, so its failures can't be put down to planner delay. The scene fails even with no delay.
  - S1: 01d503d4 at planner_delay_us 0: 2/2 failed, rate 42%-100% (90%) (o1_010, o1_014)
  - S2: 01d503d4 at planner_delay_us 100000: 1/1 failed, rate 27%-100% (90%) (o1_007)
  - S3: 01d503d4 at planner_delay_us 200000: 1/1 failed, rate 27%-100% (90%) (o1_001)
- clipgt-023b7fcc shows no clear break point: it passed at 200 ms, failed at 300 ms and passed at 400 ms, one run each. That is consistent with run-to-run noise rather than a threshold.
  - S4: 023b7fcc at planner_delay_us 200000: 0/1 failed, rate 0%-73% (90%) (o1_002)
  - S5: 023b7fcc at planner_delay_us 300000: 1/1 failed, rate 27%-100% (90%) (o1_015)
  - S6: 023b7fcc at planner_delay_us 400000: 0/1 failed, rate 0%-73% (90%) (o1_008)
- clipgt-026d6a39 has one run, at 0 µs. It failed, but the failure is flagged as a possible simulator artifact, so it tells us nothing about delay sensitivity.
  - S7: 026d6a39 at planner_delay_us 0: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (o1_005)

## Open

- Where clipgt-02eadd92 breaks: run about 5 repeats each at 100, 125 and 150 ms to pin down the threshold. Also check run o1_011/o1_012 (the 150 ms failure flagged as a possible artifact) for rendering problems.
- Whether clipgt-01d503d4 fails at baseline in every run: more runs at 0 µs would tell us whether it just fails without any delay. If it does, delay can't be studied on this scene without first fixing the baseline failure.
- Whether clipgt-023b7fcc is sensitive to delay at all: repeat 200, 300 and 400 ms several times each to see if the 300 ms failure happens again.
- clipgt-026d6a39: rerun at 0 µs and then sweep delay, because its only run was a failure that may be an artifact.
- Scenes never run: clipgt-0245ff75, clipgt-02e075b9, clipgt-032b6f21 and clipgt-04394343. Each needs a delay sweep, e.g. 0, 100, 200 and 400 ms, before anyone can say whether it is fragile.

## Every setting

- S1: 01d503d4 at planner_delay_us 0: 2/2 failed, rate 42%-100% (90%) (o1_010, o1_014)
- S2: 01d503d4 at planner_delay_us 100000: 1/1 failed, rate 27%-100% (90%) (o1_007)
- S3: 01d503d4 at planner_delay_us 200000: 1/1 failed, rate 27%-100% (90%) (o1_001)
- S4: 023b7fcc at planner_delay_us 200000: 0/1 failed, rate 0%-73% (90%) (o1_002)
- S5: 023b7fcc at planner_delay_us 300000: 1/1 failed, rate 27%-100% (90%) (o1_015)
- S6: 023b7fcc at planner_delay_us 400000: 0/1 failed, rate 0%-73% (90%) (o1_008)
- S7: 026d6a39 at planner_delay_us 0: 1/1 failed, rate 27%-100% (90%), 1 possibly the simulator's (o1_005)
- S8: 02eadd92 at planner_delay_us 0: 0/1 failed, rate 0%-73% (90%) (o1_009)
- S9: 02eadd92 at planner_delay_us 100000: 0/2 failed, rate 0%-58% (90%) (o1_006, o1_013)
- S10: 02eadd92 at planner_delay_us 150000: 2/2 failed, rate 42%-100% (90%), 1 possibly the simulator's (o1_011, o1_012)
- S11: 02eadd92 at planner_delay_us 200000: 1/1 failed, rate 27%-100% (90%) (o1_003)
- S12: 02eadd92 at planner_delay_us 400000: 1/1 failed, rate 27%-100% (90%) (o1_004)

## Provenance

Plan: `plan.json` (rationale: fixed by the pilot script (run_pilot.sh), not planned from a brief). Report written by claude-opus-5-5 from `results` in 14 s; every count above is computed from the queue, not written by the model.
