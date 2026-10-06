"""rules.py and promote.py: deterministic checks, and the gate they must pass."""

import json
from pathlib import Path

import pytest
from promote import admission
from read_state import State, read_state
from rules import rule_problem, violation

CONTEXT_8 = {
    "id": "context_length_is_8",
    "file": "driver-config.yaml",
    "path": "inference.context_length",
    "op": "eq",
    "value": 8,
    "reason": "VaVAM needs 8 frames",
}
DELAY_LANDED = {
    "id": "delay_matches_label",
    "file": "wizard-config.yaml",
    "path": "runtime.simulation_config.planner_delay_us",
    "op": "eq_label",
    "label_key": "planner_delay_us",
    "reason": "the delay the label records must be the one that ran",
}


def _run(make_run, name, **kwargs):
    entry = make_run(name, **kwargs)
    return Path(entry["run_dir"]), entry["config"]


@pytest.mark.parametrize(
    "rule,problem",
    [
        (CONTEXT_8, None),
        (DELAY_LANDED, None),
        ({**CONTEXT_8, "file": "secrets.env"}, "file must be one of"),
        ({**CONTEXT_8, "op": "matches"}, "op must be one of"),
        ({**CONTEXT_8, "id": "Has Spaces"}, "is not snake_case"),
        ({**DELAY_LANDED, "label_key": None}, "eq_label needs label_key"),
        ({**CONTEXT_8, "op": "le", "value": "8"}, "le needs a number"),
    ],
)
def test_rule_shape(rule, problem):
    found = rule_problem(rule)
    assert (found is None) if problem is None else problem in found


def test_violation_reads_the_resolved_config(make_run):
    path, label = _run(make_run, "ok")
    assert violation(CONTEXT_8, path, label) is None
    assert violation(DELAY_LANDED, path, label) is None
    path, label = _run(make_run, "late", planner_delay_us=100000, resolved_delay_us=0)
    assert "is 0, rule eq_label 100000" in violation(DELAY_LANDED, path, label)
    missing = {**CONTEXT_8, "path": "inference.not_there"}
    assert "missing" in violation(missing, path, label)


def test_promoted_rule_fails_a_run_the_other_checks_keep(make_run, no_promoted_rules):
    entry = make_run("r")
    assert read_state(entry).state is State.COMPLETE
    strict = {**CONTEXT_8, "id": "context_length_is_16", "value": 16}
    no_promoted_rules.write_text(json.dumps([strict]))
    result = read_state(entry)
    assert result.state is State.FAILED
    assert result.k_status.startswith("rule_violated: context_length_is_16")


def test_admission(make_run):
    clean = {f"g{index}": _run(make_run, f"g{index}") for index in range(3)}
    batch = {
        "swept": _run(make_run, "swept", planner_delay_us=100000, resolved_delay_us=0),
        "zero": _run(make_run, "zero"),
    }
    admitted = admission(DELAY_LANDED, batch, {"swept"}, clean)
    assert admitted["admitted"] and admitted["caught"] == ["swept"]
    # The batch varies the delay, so pinning it to a constant is refused.
    pinned = {
        **CONTEXT_8,
        "id": "no_delay",
        "file": "wizard-config.yaml",
        "path": "runtime.simulation_config.planner_delay_us",
        "value": 0,
    }
    assert admission(pinned, batch, {"swept"}, clean)["reason"].startswith("pins")
    # A rule that misses what it was proposed for is refused.
    assert not admission(CONTEXT_8, batch, {"swept"}, clean)["admitted"]
    # A rule that fires on a known-good run is refused.
    wrong = {**CONTEXT_8, "id": "context_length_is_16", "value": 16}
    assert (
        admission(wrong, batch, {"swept"}, clean)["reason"] == "fires on 3 clean runs"
    )


def test_ne_holds_where_the_value_is_absent(make_run):
    """A forbidden setting that is absent is not set; a typo never fires."""
    path, label = _run(make_run, "ok")
    no_fault = {
        **CONTEXT_8,
        "id": "no_fault_injection",
        "file": "wizard-config.yaml",
        "path": "runtime.simulation_config.fault_injection.enabled",
        "op": "ne",
        "value": True,
    }
    assert violation(no_fault, path, label) is None
    batch = {"ok": (path, label)}
    typo = {**no_fault, "path": "runtime.simulation_config.fault_injecton.enabled"}
    assert admission(typo, batch, {"ok"}, {})["reason"] == "fires on none of the flagged runs"
