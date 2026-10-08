"""What the outer loop may propose: each knob typed, with its legal values.

A knob is either a scenario variable (what a study varies and measures) or an
execution setting (how a run executes, fixed here and changed only by a
recovery in the inner loop). A study varies some scenario knobs; every
proposed run is checked here before it is queued, as the inner loop's
validator checks a recovery.

Only knobs the inner loop can apply and verify from the log are listed:

- planner_delay_us: postflight checks the resolved config and the age of the
  plan the controller got (physics.py);
- lateral_bias_m: a sideways shift of the plan (left positive), as from a
  perception or localisation error; postflight checks the resolved config and
  the plan's measured offset from the driver's;
- waypoint_noise_std: random jitter of each planned waypoint; postflight checks
  the resolved config and the plan's measured scatter (0.3 m requested
  measured 0.295 to 0.306 m on g3);
- actor_time_shift_s, actor_speed_scale: retime the recorded actors of the
  study's retime_class (AlpaSim's actor_retiming hook), with traffic replayed;
  postflight checks the rule landed and that the runtime retimed at least one
  actor of that class.

The controller that tracks the plan is the system under test, not a knob: a
study runs the linear MPC, or, in an A/B study (fixed setting `compare`),
every proposed setting once on each of two controllers.
"""

SCENE_FILE = "data/scenes/sim_scenes.csv"
DELAYS_US = tuple(range(0, 400_001, 50_000))
BIASES_M = (-0.5, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.5)
NOISES_M = (0.0, 0.1, 0.2, 0.3)
SHIFTS_S = (-2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0)
SPEED_SCALES = (0.5, 0.75, 1.0, 1.25, 1.5, 2.0)
SCENARIO = {
    "planner_delay_us": DELAYS_US,
    "lateral_bias_m": BIASES_M,
    "waypoint_noise_std": NOISES_M,
    "actor_time_shift_s": SHIFTS_S,
    "actor_speed_scale": SPEED_SCALES,
}
TYPES = {
    "planner_delay_us": (int,),
    "lateral_bias_m": (int, float),
    "waypoint_noise_std": (int, float),
    "actor_time_shift_s": (int, float),
    "actor_speed_scale": (int, float),
}
ACTOR_KNOBS = ("actor_time_shift_s", "actor_speed_scale")
# A study's fixed settings: how other actors move, and which recorded actors
# the actor knobs retime (AlpaSim label classes: person = pedestrian, rider =
# cyclist).
TRAFFIC_MODES = ("catk", "replay")
RETIME_CLASSES = ("person", "rider", "automobile", "heavy_truck")
DESCRIPTIONS = {
    "planner_delay_us": "planner delay in microseconds (camera frame to the "
    "controller receiving the plan made from it)",
    "lateral_bias_m": "sideways shift of the plan in metres, left positive, as "
    "from a perception or localisation error",
    "waypoint_noise_std": "random jitter of each planned waypoint, standard "
    "deviation in metres, as from noisy perception",
    "actor_time_shift_s": "seconds by which the study's actor class moves later "
    "than recorded (negative: earlier), e.g. a pedestrian stepping out sooner",
    "actor_speed_scale": "speed of the study's actor class relative to its "
    "recording (2.0: twice as fast along the same path)",
}
# The controller configs a run may use (AlpaSim's src/wizard/configs/controller/),
# each with what it is and the values that identify it in the resolved
# `controller` block of wizard-config.yaml, which postflight compares with the
# request (read_state.config_not_landed).
CONTROLLERS = {
    "linear": {
        "meaning": "linear MPC, stage terminal cost: the controller every study "
        "used before A/B studies",
        "resolved": {"mpc_implementation": "linear", "terminal_cost": "stage"},
    },
    "nonlinear": {
        "meaning": "nonlinear MPC, 2 s horizon",
        "resolved": {"mpc_implementation": "nonlinear", "n_horizon": 20},
    },
    "short_horizon": {
        "meaning": "nonlinear MPC with a 1.5 s horizon",
        "resolved": {"mpc_implementation": "nonlinear", "n_horizon": 15},
    },
    "feasible_best": {
        "meaning": "linear MPC with Riccati terminal cost and high position "
        "gains: the best tracking real vehicle physics allows",
        "resolved": {"mpc_implementation": "linear", "terminal_cost": "riccati"},
    },
    "kinematic_ideal": {
        "meaning": "no controller: the car is moved along the plan exactly, "
        "an upper bound on tracking",
        "resolved": {"mpc_implementation": "kinematic_ideal"},
    },
}
DEFAULT_CONTROLLER = "linear"
SIDES = ("a", "b")
EXECUTION = {"context_length": 8, "scene_file": SCENE_FILE, "trafficsim_device": "cpu"}
UNVARIED = {
    "planner_delay_us": 0,
    "lateral_bias_m": 0.0,
    "waypoint_noise_std": 0.0,
    "actor_time_shift_s": 0.0,
    "actor_speed_scale": 1.0,
}


def run_config(scene_id: str, settings: dict, fixed: dict, controller: str) -> dict:
    """The queue config of a run: the scene, the controller, the study's fixed
    settings and knob values, and every other scenario knob at its unvaried
    value. With `retime_tracks` (scene -> the scene's key actor), the actor
    knobs retime that one actor instead of its whole class."""
    tracks = fixed.get("retime_tracks", {})
    shared = {k: v for k, v in fixed.items() if k not in ("retime_tracks", "compare")}
    key_actor = {"retime_track": tracks[scene_id]} if scene_id in tracks else {}
    return {
        **EXECUTION,
        "scene_id": scene_id,
        "controller": controller,
        **shared,
        **key_actor,
        **UNVARIED,
        **settings,
    }


def fixed_problems(fixed: dict, varied: tuple) -> list[str]:
    """Why a study's fixed settings cannot run with the knobs it varies. Actor
    knobs retime recorded tracks; with CATK only the history before the
    hand-over would follow them, so they need replayed traffic. `compare`
    names the two controllers of an A/B study, a and b."""
    problems = []
    if set(fixed) - {"traffic", "retime_class", "retime_tracks", "compare"}:
        problems.append("fixed settings: traffic, retime_class, retime_tracks, compare")
    if "compare" in fixed:
        compare = fixed["compare"]
        if set(compare) != set(SIDES) or set(compare.values()) - set(CONTROLLERS):
            problems.append(
                f"compare names a controller from {sorted(CONTROLLERS)} as a and as b"
            )
        elif compare["a"] == compare["b"]:
            problems.append("compare needs two different controllers")
    if fixed.get("traffic", "catk") not in TRAFFIC_MODES:
        problems.append(f"traffic must be one of {TRAFFIC_MODES}")
    if set(varied) & set(ACTOR_KNOBS):
        if fixed.get("traffic") != "replay":
            problems.append("actor knobs need traffic replay")
        if fixed.get("retime_class") not in RETIME_CLASSES and not fixed.get(
            "retime_tracks"
        ):
            problems.append(
                f"actor knobs need a retime_class from {RETIME_CLASSES} or retime_tracks"
            )
    return problems


def rejection(proposed: dict, scenes: set[str], varied: tuple[str, ...]) -> str | None:
    """Why a proposed run may not be queued, or None. `scenes` is the study's
    candidate set: scenes of the catalog that are downloaded locally; `varied`
    the scenario knobs the study varies."""
    expected = {"scene_id", "why", *varied}
    if set(proposed) != expected:
        return f"keys must be {sorted(expected)}, got {sorted(proposed)}"
    if proposed["scene_id"] not in scenes:
        return f"scene {proposed['scene_id']!r} is not a candidate of this study"
    for knob in varied:
        value = proposed[knob]
        if type(value) not in TYPES[knob] or value not in SCENARIO[knob]:
            return f"{knob} {value!r} is not one of {list(SCENARIO[knob])}"
    return None
