# Unprotected left turn: the most challenging gaps

## Question
In scenes where the ego turns left across oncoming traffic, which arrival
timings and speeds of the oncoming cars make the policy collide during the
turn? Find the 5 most challenging cases, each on a different scene, confirmed
by repeats.

## Scope
Scenes tagged unprotected_left. Retime the recorded cars (class automobile):
up to 2 s earlier or later, 0.5x to 2x speed (Euro NCAP's turn-across-path
test varies the oncoming speed). Replay traffic as recorded.

## Budget
About 50 runs.

## What counts
A front or side collision, or leaving the road. Near misses rank next.
