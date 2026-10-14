import re

from package_skills import ADVISOR, OUT, SKILLS, package


def test_package_on_disk_is_current():
    stale = [path for path, text in package().items()
             if not path.is_file() or path.read_text(encoding="utf-8") != text]
    assert stale == [], "run research/harness/package_skills.py"


def test_every_contract_is_packaged_once():
    contracts = {spec["contract"] for spec in SKILLS.values()}
    extras = {source for spec in SKILLS.values() for source in spec.get("extra", {})}
    assert contracts | extras == {path.name for path in ADVISOR.glob("*.md")}


def test_frontmatter_is_valid_agent_skill():
    for path, text in package().items():
        if path.name != "SKILL.md":
            continue
        name = re.search(r"^name: (.+)$", text, re.M).group(1)
        description = re.search(r"^description: (.+)$", text, re.M).group(1)
        assert text.startswith("---\n") and name == path.parent.name
        assert re.fullmatch(r"[a-z0-9-]{1,64}", name)
        assert 0 < len(description) <= 1024


def test_contract_text_is_unchanged_inside_the_skill():
    files = package()
    for name, spec in SKILLS.items():
        contract = (ADVISOR / spec["contract"]).read_text(encoding="utf-8")
        assert contract in files[OUT / name / "SKILL.md"]
