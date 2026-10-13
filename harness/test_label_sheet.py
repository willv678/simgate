"""label_sheet.py: the sample is reproducible and the sheet is blind."""

import random
from pathlib import Path

import label_sheet


def _fake_studies(monkeypatch):
    runs = {s: [Path(f"/runs/{s}_{i:03d}") for i in range(40)] for s in label_sheet.STUDIES}

    def judged(run_dir):
        i = int(run_dir.name[-3:])
        if i % 4 == 3:
            return None
        return ("not_counted" if i % 4 == 2 else "counted", 1e6 * i, 0.0)

    monkeypatch.setattr(label_sheet, "kept_runs", lambda study: runs[study])
    monkeypatch.setattr(label_sheet, "contact_to_judge", judged)


def test_the_same_seed_draws_the_same_sample(monkeypatch):
    _fake_studies(monkeypatch)
    first = label_sheet.sample(random.Random(label_sheet.SEED))
    second = label_sheet.sample(random.Random(label_sheet.SEED))
    assert [c["run"] for c in first] == [c["run"] for c in second]


def test_each_study_gives_its_quota_from_each_group(monkeypatch):
    _fake_studies(monkeypatch)
    chosen = label_sheet.sample(random.Random(label_sheet.SEED))
    assert [c["id"] for c in chosen] == [f"L{i:02d}" for i in range(1, 61)]
    for study in label_sheet.STUDIES:
        groups = [c["group"] for c in chosen if c["study"] == study]
        assert groups.count("not_counted") == label_sheet.NOT_COUNTED
        assert len(groups) == label_sheet.PER_STUDY


def test_the_sheet_reveals_no_study_setting_or_verdict():
    leaks = ("study", "run", "group", "setting", "speed", "shift", "triage", "cause",
             "fault_rule", "counted", "actor_closed", "failed", "collision")
    for column in label_sheet.COLUMNS:
        assert not any(leak in column for leak in leaks), column


def test_the_video_hides_the_evaluators_metric_table():
    assert label_sheet.METRIC_TABLE.startswith("drawbox=") and "t=fill" in label_sheet.METRIC_TABLE


def test_kappa_is_one_for_full_agreement_and_zero_for_chance():
    same = [("policy", "policy"), ("not_policy", "not_policy")] * 5
    assert label_sheet.kappa(same) == 1.0
    chance = [("policy", "policy"), ("policy", "not_policy"),
              ("not_policy", "policy"), ("not_policy", "not_policy")]
    assert label_sheet.kappa(chance) == 0.0


def test_compare_leaves_out_unclear_labels():
    person = {"L01": "policy", "L02": "unclear", "L03": "not_policy"}
    other = {"L01": "policy", "L02": "policy", "L03": "policy"}
    found = label_sheet.compare(person, other)
    assert found["n"] == 2 and found["agree"] == 0.5
