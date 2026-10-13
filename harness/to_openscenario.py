"""Each study's parameter space as an ASAM OpenSCENARIO XML parameter
distribution, so the scenarios are stated in the field's standard terms.

A study is a logical scenario (Menzel et al., IV 2018): a scenario with
parameter ranges. Here, per study:

- `scenarios/<study>.xosc`: a ParameterValueDistribution whose
  deterministic distributions are the study's scene set and the legal
  values of every knob it varies (the logical scenario);
- `scenarios/<study>_hardest.xosc`: the confirmed hardest settings as
  parameter value sets (concrete scenarios).

The referenced scenario file names the AlpaSim scene rather than an
OpenSCENARIO storyboard: AlpaSim replays recorded scenes, so the road,
actors and their recorded tracks come from the scene, and the parameters
retime them. Written with scenariogeneration as OpenSCENARIO XML 1.4; the
files validate against the 1.3 and 1.4 schemas (esmini's copies).

    uv run --with scenariogeneration python research/harness/to_openscenario.py
"""

import json
import sys
from pathlib import Path

from scenariogeneration import xosc

sys.path.insert(0, str(Path(__file__).resolve().parent))

from case_card import hardest
from knobs import SCENARIO
from read_state import ROOT

STUDIES = ("pedestrian_ego_speed", "cut_in_merge", "lead_vehicle", "lane_keeping")
OUT = ROOT / "research" / "scenarios"
OSC_MINOR = 4
# OpenSCENARIO parameter names for the study knobs.
NAME = {
    "scene_id": "SceneId",
    "ego_speed_scale": "EgoSpeedScale",
    "actor_time_shift_s": "ActorTimeShift",
    "actor_speed_scale": "ActorSpeedScale",
    "planner_delay_us": "PlannerDelay",
    "lateral_bias_m": "PlanLateralBias",
    "waypoint_noise_std": "PlanWaypointNoise",
}


def _set(values) -> xosc.DistributionSet:
    found = xosc.DistributionSet()
    for value in values:
        found.add_value(str(value))
    return found


def logical(study: str, plan: dict) -> xosc.ParameterValueDistribution:
    space = xosc.Deterministic()
    space.add_single_distribution(NAME["scene_id"], _set(plan["scenes"]))
    for knob in plan["vary"]:
        space.add_single_distribution(NAME[knob], _set(SCENARIO[knob]))
    return xosc.ParameterValueDistribution(
        f"SimGate study {study}: {plan['question']}",
        "SimGate",
        f"alpasim://{study}/{{SceneId}}",
        space,
        osc_minor_version=OSC_MINOR,
    )


def concrete(study: str, plan: dict) -> xosc.ParameterValueDistribution | None:
    runs = hardest(study)
    if not runs:
        return None
    sets = xosc.DeterministicMultiParameterDistribution()
    for run in runs:
        values = xosc.ParameterValueSet()
        values.add_parameter(NAME["scene_id"], run["scene_id"])
        for knob in plan["vary"]:
            values.add_parameter(NAME[knob], str(run[knob]))
        sets.add_value_set(values)
    space = xosc.Deterministic()
    space.add_multi_distribution(sets)
    return xosc.ParameterValueDistribution(
        f"SimGate study {study}: confirmed hardest settings",
        "SimGate",
        f"alpasim://{study}/{{SceneId}}",
        space,
        osc_minor_version=OSC_MINOR,
    )


def main() -> int:
    OUT.mkdir(exist_ok=True)
    for study in STUDIES:
        path = ROOT / "research" / "studies" / study / "plan.json"
        if not path.exists():
            continue
        plan = json.loads(path.read_text())["plan"]
        logical(study, plan).write_xml(str(OUT / f"{study}.xosc"))
        found = concrete(study, plan)
        if found:
            found.write_xml(str(OUT / f"{study}_hardest.xosc"))
        print(study, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
