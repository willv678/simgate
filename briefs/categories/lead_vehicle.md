# Lead vehicle braking: the most challenging cases

## Question
In scenes with a car ahead in the ego's lane that slows or stops, which
timings and speeds of the vehicles ahead make the policy rear-end them? Find
the 5 most challenging cases, each on a different scene, confirmed by repeats.

## Scope
Scenes tagged lead_vehicle. Retime the recorded cars (class automobile): up
to 2 s earlier or later, 0.5x to 2x their recorded speed (slower means a
harder stop for the ego). Replay traffic as recorded. Planner delay may be
added up to 200 ms if the cases at zero delay are not challenging enough.

## Budget
About 50 runs.

## What counts
A front or side collision, or leaving the road. Near misses rank next.
