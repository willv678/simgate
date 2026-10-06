# Pedestrian crossing: the most challenging timings

## Question
In scenes where a pedestrian crosses or walks near the ego's path, which
pedestrian timings and speeds make the driving policy hit the pedestrian or
leave the road to avoid them? Find the 5 most challenging cases, each on a
different scene, confirmed by repeats.

## Scope
Scenes tagged pedestrian_crossing. Retime the recorded pedestrians (class
person): step out up to 2 s earlier or later, walk 0.5x to 2x their recorded
speed. Replay the other traffic as recorded so the scenario is scripted, as in
Euro NCAP pedestrian tests. No delay or perception error.

## Budget
About 50 runs.

## What counts
A front or side collision, or leaving the road. Near misses rank next.
