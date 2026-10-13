# Scenarios: coverage, definition, and what we can vary

Shao, 13 Oct: (1) are all three studies emergency braking (AEB)? cover the
car more widely; Level 2 is a starting point; (2) define scenarios in a
structured, standard way (OpenSCENARIO 1.4, esmini); (3) be clear which
parameters we change, and why those.

## 1. Coverage

**The study designs are AEB-shaped; the failures they found are not.**
Pedestrian, cut-in and car-ahead-braking are all "something appears in front
of the ego" tests. But Claude's triage of the 1,252 failed runs in those
studies (`figures/meeting/failure_types.png`,
`figures/cards/triage_causes.json`):

| failure | share |
|---|---|
| steered into another road user | 47% |
| left the road | 16% |
| another road user drove into the ego | 12% |
| did not brake for the car ahead (the AEB failure) | 10% |
| other (mostly contacts begun before the hand-off, problem 30) | 15% |

So about two thirds are lane-keeping failures (the left drift, `DRIFT.md`),
and only one in ten is the braking failure the studies were designed
around. (Triage ran on every run flagged failed at the time, including ones
the current scorer no longer counts.)

**Against Level 2 functions and the Euro NCAP tests behind them:**

| function | Euro NCAP test | study | status |
|---|---|---|---|
| adaptive cruise / emergency braking for a car ahead | AEB Car-to-Car rear (CCRs, CCRm, CCRb) | car ahead braking | done, 3 replicates x 2 rates |
| reacting to a cut-in | Assisted Driving (highway assist) cut-in and cut-out | car cutting in | done |
| emergency braking for a pedestrian | AEB VRU pedestrian (CPNA, CPFA) | pedestrian x ego speed | done |
| lane keeping, road edge, oncoming, overtaking | LSS: ELK, LKA | **lane keeping** (new) | queued 13 Oct, 6 methods |
| crossing traffic at a junction | AEB C2C crossing (CCCscp) | intersection | one replicate; 68 scenes tagged |
| turn across path | AEB C2C turn across path (CCFtap) | unprotected left | not possible: 2 of 250 scenes |
| lane change into an occupied lane | LSS overtaking | not designed | scenes exist (44 merge/cut-in) |

**Scene availability** (`harness/scene_tags.json`, 250 scenes): intersection
68, lead vehicle 58, merge/cut-in 44, pedestrian crossing 14, unprotected
left 2, 108 with none of the five.

## 2. A structured definition (OpenSCENARIO)

Each study is a **logical scenario** (Menzel et al., IV 2018: a scenario
with parameter ranges); each run is a **concrete scenario** (one value per
parameter). `harness/to_openscenario.py` writes both as ASAM OpenSCENARIO
XML 1.4 `ParameterValueDistribution` files in `scenarios/`:

- `scenarios/<study>.xosc`: the scene set and every varied knob's values;
- `scenarios/<study>_hardest.xosc`: the confirmed hardest settings, one
  parameter value set each.

All seven files validate against the 1.3 and 1.4 schemas (esmini's copies).
Parameter names: `SceneId`, `EgoSpeedScale`, `ActorTimeShift`,
`ActorSpeedScale`, `PlannerDelay`, `PlanLateralBias`, `PlanWaypointNoise`.

**esmini.** esmini plays OpenSCENARIO storyboards on OpenDRIVE maps. AlpaSim
scenes are neural reconstructions of recorded drives with their own map, no
OpenDRIVE, so esmini cannot replay them as is. The value is the shared
vocabulary: the same parameter files could drive an esmini or CARLA version
of a study given an OpenDRIVE map of the scene.

## 3. Which parameters, and why

AlpaSim replays real recorded scenes, so the parameters split three ways:

| | parameters | how |
|---|---|---|
| **vary per run** (knobs) | ego speed at hand-off (0.6-1.4x); a recorded actor's timing (-2 to +2 s) and speed (0.5-2x); planner delay (0-400 ms); plan sideways shift (-0.5 to +0.5 m) and waypoint noise (0-0.3 m) | `knobs.py`; each run proves from its log that the value took effect |
| **choose** (by picking scenes) | road type, number of lanes, curvature, junction, which actors are present, weather and light | the tagger's facts and tags (`scene_tags.json`); a study's scope picks scenes |
| **not possible** | add an actor that is not in the recording, change the road geometry, change the number of lanes | the scene is a reconstruction of one real drive |

Why these knobs: they are the Euro NCAP test parameters for each function
(test-vehicle speed, the other road user's timing and speed), plus the
policy's own inputs that a real stack gets wrong (latency, perception
error). Lanes, curvature and background vehicles are real factors too, but
in AlpaSim they are chosen through the scene, not dialled: a study that
needs curvature picks curved scenes.

Next candidates, in order: intersection crossing (68 scenes, CCCscp);
background-traffic density by choosing scenes; reactive traffic (AlpaSim's
CATK model) instead of replay, so other cars respond (`VALIDITY.md` section
4).
