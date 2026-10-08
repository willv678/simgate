"""web.py: the app writes only what the command line would, and refuses the rest."""

import json
import threading
import urllib.request
from http.server import ThreadingHTTPServer

import jobs
import pytest
import web


@pytest.fixture
def folders(tmp_path, monkeypatch):
    monkeypatch.setattr(jobs, "BRIEFS", tmp_path / "briefs")
    monkeypatch.setattr(web, "STUDIES", tmp_path / "studies")
    (tmp_path / "briefs").mkdir()
    (tmp_path / "studies").mkdir()
    return tmp_path


def test_save_brief_checks_the_name_and_freezes_a_planned_study(folders):
    web.save_brief("night_peds", "# Night\n")
    assert (folders / "briefs" / "night_peds.md").read_text() == "# Night\n"
    with pytest.raises(web.Refused):
        web.save_brief("../escape", "# x\n")
    with pytest.raises(web.Refused):
        web.save_brief("empty_one", "  \n")
    (folders / "studies" / "night_peds").mkdir()
    (folders / "studies" / "night_peds" / "plan.json").write_text("{}")
    with pytest.raises(web.Refused):
        web.save_brief("night_peds", "# changed\n")


def test_two_briefs_cannot_share_a_study_folder(folders):
    (folders / "briefs" / "categories").mkdir()
    (folders / "briefs" / "categories" / "lead.md").write_text("# lead\n")
    with pytest.raises(web.Refused):
        web.save_brief("lead", "# another lead\n")


def test_running_arms_reads_the_proposer_and_defaults_to_llm():
    commands = [
        "/v/bin/python3 research/harness/study.py research/briefs/categories/lead.md --proposer rules --yes",
        "/v/bin/python3 research/harness/study.py research/briefs/x.md --yes",
        "/v/bin/python3 research/harness/study.py research/briefs/y.md --plan-only",
    ]
    assert web.running_arms(commands) == {("lead", "rules"), ("x", "llm")}


@pytest.fixture
def server():
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), web.Handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{httpd.server_address[1]}"
    httpd.shutdown()


def _post(url, body, headers):
    request = urllib.request.Request(
        url, json.dumps(body).encode(), {"Content-Type": "application/json", **headers}
    )
    try:
        return urllib.request.urlopen(request).status
    except urllib.error.HTTPError as exc:
        return exc.code


def test_changes_need_the_header_and_a_local_host(server, folders):
    body = {"name": "from_page", "text": "# x\n"}
    assert _post(server + "/api/brief", body, {}) == 403
    assert (
        _post(server + "/api/brief", body, {"X-SimGate": "1", "Host": "evil.example"})
        == 403
    )
    assert _post(server + "/api/brief", body, {"X-SimGate": "1"}) == 200
    assert (folders / "briefs" / "from_page.md").exists()


def test_static_files_stay_inside_their_folder(server, folders):
    (folders / "studies" / "s").mkdir()
    (folders / "studies" / "s" / "index.html").write_text("<p>ok</p>")
    assert (
        urllib.request.urlopen(server + "/studies/s/index.html").read() == b"<p>ok</p>"
    )
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(server + "/studies/..%2F..%2Fetc/passwd")
