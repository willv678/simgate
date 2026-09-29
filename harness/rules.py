"""Checks the tier 2 auditor proposed and promote.py admitted into the gate.

A rule names one value in a run's resolved config and what it must be. It is
data, not code, so checking it is deterministic and cannot do anything else:

    {"id": "context_length_is_8", "file": "driver-config.yaml",
     "path": "inference.context_length", "op": "eq", "value": 8, "reason": "..."}
    {"id": "delay_matches_label", "file": "wizard-config.yaml",
     "path": "runtime.simulation_config.planner_delay_us", "op": "eq_label",
     "label_key": "planner_delay_us", "reason": "..."}

`eq_label` compares the value with the run's label, the config the experiment
recorded for it. A missing file, path, or label key is a violation: a run
whose config cannot show that it is right is not kept.

read_state.py applies the promoted rules to every finished run. They live in
rules/promoted.json, or in the file named by ALPASIM_RULES.
"""

import json
import os
import re
from pathlib import Path

import yaml

FILES = ("driver-config.yaml", "wizard-config.yaml")
OPS = ("eq", "ne", "le", "ge", "in", "eq_label")
PROMOTED = Path(__file__).resolve().parent / "rules" / "promoted.json"
_MISSING = object()


def rules_file() -> Path:
    return Path(os.environ.get("ALPASIM_RULES", PROMOTED))


def load_rules() -> list[dict]:
    return json.loads(rules_file().read_text(encoding="utf-8"))


def rule_problem(rule: dict) -> str | None:
    """Why this is not a well-formed rule, or None."""
    for key in ("id", "file", "path", "op", "reason"):
        if not isinstance(rule.get(key), str) or not rule[key]:
            return f"missing {key}"
    if not re.fullmatch(r"[a-z0-9_]+", rule["id"]):
        return f"id {rule['id']!r} is not snake_case"
    if rule["file"] not in FILES:
        return f"file must be one of {FILES}"
    if rule["op"] not in OPS:
        return f"op must be one of {OPS}"
    if rule["op"] == "eq_label":
        if not isinstance(rule.get("label_key"), str):
            return "eq_label needs label_key"
    elif "value" not in rule:
        return f"{rule['op']} needs value"
    if rule["op"] == "in" and not isinstance(rule["value"], list):
        return "in needs a list value"
    if rule["op"] in ("le", "ge") and not isinstance(rule["value"], int | float):
        return f"{rule['op']} needs a number"
    return None


def _lookup(config, path: str):
    for key in path.split("."):
        if not isinstance(config, dict) or key not in config:
            return _MISSING
        config = config[key]
    return config


def violation(rule: dict, run_path: Path, label: dict) -> str | None:
    """How this run breaks the rule, or None when it satisfies it."""
    source = run_path / rule["file"]
    if not source.is_file():
        return f"{rule['id']}: {rule['file']} missing"
    actual = _lookup(yaml.safe_load(source.read_text(encoding="utf-8")), rule["path"])
    if actual is _MISSING:
        return f"{rule['id']}: {rule['path']} missing from {rule['file']}"
    op = rule["op"]
    if op == "eq_label":
        if rule["label_key"] not in label:
            return f"{rule['id']}: label has no {rule['label_key']}"
        expected = label[rule["label_key"]]
        ok = actual == expected
    else:
        expected = rule["value"]
        ok = {
            "eq": lambda: actual == expected,
            "ne": lambda: actual != expected,
            "le": lambda: isinstance(actual, int | float) and actual <= expected,
            "ge": lambda: isinstance(actual, int | float) and actual >= expected,
            "in": lambda: actual in expected,
        }[op]()
    if ok:
        return None
    return f"{rule['id']}: {rule['path']} is {actual!r}, rule {op} {expected!r}"


def violations(rules: list[dict], run_path: Path, label: dict) -> list[str]:
    return [
        found
        for rule in rules
        if (found := violation(rule, run_path, label)) is not None
    ]
