# Confirm the latency break on scene 02eadd92

## Question
Does scene clipgt-02eadd92-02f1-46d8-86fe-a9e338fed0b6 break between 100 ms
and 150 ms of planner delay? A pilot this morning saw it pass every run at 0
and 100 ms and fail every run from 150 ms up, but with only one or two runs per
delay.

## Win condition
Confirmed if the 90% range of the failure rate at 100 ms and at 150 ms no
longer overlap. Refuted if 100 ms fails or 150 ms passes often enough that
they clearly do.

## Scope
Only this scene. Delay only.

## Budget
8 runs, as 2 rounds of 4. It has to finish in about 40 minutes.
