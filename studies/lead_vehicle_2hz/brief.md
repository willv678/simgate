# Lead vehicle braking: the most challenging cases (2 Hz planning)

## Question
In scenes with a car ahead in the ego's lane that slows or stops, which
timings and speeds of the vehicles ahead make the policy rear-end them? Find
the 5 most challenging cases, each on a different scene, confirmed by repeats.

## Scope
Scenes tagged lead_vehicle. Retime the recorded cars (class automobile): up
to 2 s earlier or later, 0.5x to 2x their recorded speed (slower means a
harder stop for the ego). Replay traffic as recorded. No planner delay
(it cannot be checked at a 500 ms step).

## Budget
About 50 runs.

## What counts
A front or side collision, or leaving the road. Near misses rank next.

## Planning rate
The policy plans every 500 ms (2 Hz, VaVAM's own rhythm), not every
100 ms; at 2 Hz its left drift halves (FACTS.md, harness/m2_queue). Same scenes,
knobs and budget as the 10 Hz study `lead_vehicle`, so the two compare.
