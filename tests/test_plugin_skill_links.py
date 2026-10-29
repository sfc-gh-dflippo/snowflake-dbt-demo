"""Check plugin skill ids and links resolve to shipped SKILL.md files."""

import re
from pathlib import Path

PLUGINS = Path(__file__).resolve().parents[1] / ".claude" / "plugins"
ID = re.compile(r"\b(snowflake-dbt-migration|dbt-quality):([a-z0-9-]+)\b")
LINK = re.compile(
    r"`(\.\./[a-z0-9-]+(?:/[a-z0-9-]+)*)`|\]\((\.{1,2}/skills/[^)#\s]+|\.\./[^)#\s]+)\)"
)


def docs():
    for plugin in PLUGINS.iterdir():
        if (plugin / "skills").is_dir():
            yield from (plugin / "skills").glob("*/SKILL.md")
            yield from [plugin / "README.md"]


def test_no_commands_dir():
    for plugin in PLUGINS.iterdir():
        assert not (plugin / "commands").exists(), plugin


def test_qualified_ids_resolve():
    for doc in docs():
        for plugin, skill in ID.findall(doc.read_text(encoding="utf-8")):
            assert (PLUGINS / plugin / "skills" / skill / "SKILL.md").is_file(), (
                doc,
                plugin,
                skill,
            )


def test_relative_skill_links_resolve():
    for doc in docs():
        for m in LINK.finditer(doc.read_text(encoding="utf-8")):
            rel = m.group(1) or m.group(2)
            target = (doc.parent / rel).resolve()
            if "skills" in rel.split("/") or doc.name == "SKILL.md":
                if target.suffix:
                    continue  # file links are not skill links
                assert (target / "SKILL.md").is_file(), (doc, rel)


if __name__ == "__main__":
    test_no_commands_dir()
    test_qualified_ids_resolve()
    test_relative_skill_links_resolve()
    print("ok")
