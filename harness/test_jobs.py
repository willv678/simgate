"""jobs.py: what the worker starts, and how a job's state is read."""

import jobs
import pytest


@pytest.fixture
def folders(tmp_path, monkeypatch):
    monkeypatch.setattr(jobs, "JOBS", tmp_path / "jobs")
    monkeypatch.setattr(jobs, "BRIEFS", tmp_path / "briefs")
    (tmp_path / "briefs" / "categories").mkdir(parents=True)
    (tmp_path / "briefs" / "categories" / "lead.md").write_text("# lead\n")
    return tmp_path


def _job(study, proposer, state, kind="study", replicate=1):
    return {"id": f"{study}_{proposer}", "study": study, "proposer": proposer,
            "replicate": replicate, "kind": kind, "state": state}  # fmt: skip


def test_counts_studies_and_loops_outside_studies_not_plans():
    commands = [
        "/x/.venv/bin/python3 research/harness/study.py research/briefs/a.md --proposer rules --yes",
        "uv run python research/harness/study.py research/briefs/a.md --proposer rules --yes",
        "/x/.venv/bin/python3 research/harness/study.py research/briefs/b.md --plan-only",
        "/x/.venv/bin/python3 /r/research/harness/loop.py /r/research/studies/a/rules/queue --audit",
        "/x/.venv/bin/python3 research/harness/loop.py research/harness/rp1_queue --policy agent",
        "bash research/harness/run_pool4.sh",
    ]
    assert jobs.simulations_running(commands) == 2
    assert jobs.pool_running(commands)
    assert not jobs.pool_running(commands[:-1])


def test_next_job_waits_for_a_slot_and_for_the_pool():
    found = [_job("a", "rules", "running"), _job("b", "llm", "queued")]
    assert jobs.next_job(found, running=1, pool=False)["id"] == "b_llm"
    assert jobs.next_job(found, running=2, pool=False) is None
    assert jobs.next_job(found, running=0, pool=True) is None


def test_next_job_never_starts_an_arm_already_running_or_a_plan():
    found = [
        _job("a", "rules", "running"),
        {**_job("a", "rules", "queued"), "id": "a_rules_2"},
        _job("c", "llm", "queued", kind="plan"),
        _job("d", "random", "queued"),
    ]
    assert jobs.next_job(found, running=1, pool=False)["id"] == "d_random"


def test_add_cancel_and_state(folders):
    job = jobs.add("categories/lead", "rules")
    assert job["study"] == "lead" and jobs.state(job) == "queued"
    jobs.cancel(job["id"])
    assert jobs.jobs()[0]["state"] == "cancelled"
    with pytest.raises(ValueError):
        jobs.cancel(job["id"])  # only a queued job can be cancelled
    (jobs.JOBS / f"{job['id']}.exit").write_text("0\n")
    assert jobs.jobs()[0]["state"] == "done"


def test_a_brief_outside_briefs_or_an_unknown_proposer_is_refused(folders):
    with pytest.raises(ValueError):
        jobs.add("../../etc/passwd", "rules")
    with pytest.raises(ValueError):
        jobs.add("categories/lead", "gradient_descent")


def test_a_launcher_from_another_boot_is_never_running(folders, monkeypatch):
    monkeypatch.setattr(jobs, "boot_id", lambda: "this-boot")
    monkeypatch.setattr(jobs, "_alive", lambda pid: True)
    job = {**jobs.add("categories/lead", "rules"), "pid": 123}
    assert jobs.state({**job, "boot_id": "this-boot"}) == "running"
    assert jobs.state({**job, "boot_id": "last-boot"}) == "failed"


def test_another_replicate_of_a_running_arm_may_start():
    found = [
        _job("a", "rules", "running"),
        {**_job("a", "rules", "queued", replicate=2), "id": "a_rules_r2"},
    ]
    assert jobs.next_job(found, running=1, pool=False)["id"] == "a_rules_r2"


def test_a_replicate_job_runs_its_own_arm(folders):
    job = jobs.add("categories/lead", "rules", replicate=2)
    assert job["id"].endswith("_lead_rules_r2")
    assert jobs.command(job)[-3:] == ["--replicate", "2", "--yes"]
