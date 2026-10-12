# Cut-in and merge: the most challenging cases (2 Hz planning)

## Question
In scenes where another car changes into the ego's lane or the ego merges,
which timings and speeds of the other cars make the policy collide? Find the
5 most challenging cases, each on a different scene, confirmed by repeats.

## Scope
Scenes tagged merge_cut_in. Retime the recorded cars (class automobile): up to
2 s earlier or later, 0.5x to 2x speed. Replay traffic as recorded.

## Budget
About 50 runs.

## What counts
A front or side collision, or leaving the road. Near misses rank next.

## Planning rate
The policy plans every 500 ms (2 Hz, VaVAM's own rhythm), not every
100 ms; at 2 Hz its left drift halves (FACTS.md, harness/m2_queue). Same scenes,
knobs and budget as the 10 Hz study `cut_in_merge`, so the two compare.
