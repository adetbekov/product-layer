"""Smoke test of the documented install: copy skills/product-layer into each agent's skills folder and use it there.

Run: python -m pytest tests/  (or python tests/test_install.py)
The copy must be self-contained: frontmatter readable, every file the skill points to present inside the copy, and
nothing pointing back into this repo (bench, tests, docs).
"""

import re
import shutil
import tempfile
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent / "skills" / "product-layer"
TARGETS = [".claude/skills", ".github/skills", ".agents/skills", ".cursor/skills"]  # README Quick start
PATH_REF = re.compile(r"`((?:references/)?(?:core|modules)/[\w-]+\.md|references/handoff\.md)`")
OUTSIDE = re.compile(r"\.\./|bench/|tests/|docs/|CREDITS\.md")


def install(root, target):
    dest = Path(root) / target / "product-layer"
    shutil.copytree(SKILL, dest)
    return dest


def frontmatter(skill_md):
    text = skill_md.read_text(encoding="utf-8")
    assert text.startswith("---\n"), "SKILL.md must open with frontmatter"
    head = dict(line.split(": ", 1) for line in text.split("---\n")[1].strip().splitlines())
    return head


def check_copy(dest):
    head = frontmatter(dest / "SKILL.md")
    assert head["name"] == "product-layer" and len(head["description"]) > 100
    files = sorted(dest.rglob("*.md"))
    assert len(files) == len(list(SKILL.rglob("*.md")))
    for f in files:
        text = f.read_text(encoding="utf-8")
        for ref in PATH_REF.findall(text):
            rel = ref if ref.startswith("references/") else f"references/{ref}"
            assert (dest / rel).is_file(), f"{f.name}: {ref} missing in the installed copy"
        assert not OUTSIDE.search(text), f"{f.name} points outside the skill folder"


def test_copy_install_works_for_every_agent():
    with tempfile.TemporaryDirectory() as tmp:
        for target in TARGETS:
            check_copy(install(tmp, target))


if __name__ == "__main__":
    test_copy_install_works_for_every_agent()
    print("ok")
