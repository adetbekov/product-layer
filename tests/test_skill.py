"""Structural checks for the product-layer skill: budgets, links, rule ids.

Run: python -m pytest tests/  (or python tests/test_skill.py)
Tokens are estimated as words x 1.3, the same method as the research doc.
"""

import re
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent / "skills" / "product-layer"
CORE = sorted((SKILL / "references" / "core").glob("*.md"))
MODULES = sorted((SKILL / "references" / "modules").glob("*.md"))
ALL = [SKILL / "SKILL.md", *CORE, *MODULES, SKILL / "references" / "handoff.md"]

RULE_HEADING = re.compile(r"^## ([A-Z]{2})-(\d+) · ", re.M)
RULE_REF = re.compile(r"\b(IA|FL|SR|ST|ON|GC|TG|AP|RL)-(\d+)\b")
PATH_REF = re.compile(r"`((?:references/)?(?:core|modules)/[\w-]+\.md|references/handoff\.md)`")
VISUAL = re.compile(r"\b(\d+\s?(px|rem|ms)|#[0-9a-fA-F]{3,6}\b|ease-in|ease-out|cubic-bezier)", re.I)


def tokens(path):
    return round(len(path.read_text(encoding="utf-8").split()) * 1.3)


def defined_rules():
    ids = []
    for f in [*CORE, *MODULES]:
        ids += [f"{p}-{n}" for p, n in RULE_HEADING.findall(f.read_text(encoding="utf-8"))]
    return ids


def test_budgets():
    assert tokens(SKILL / "SKILL.md") <= 1500
    assert sum(tokens(f) for f in CORE) <= 12000
    for f in MODULES:
        assert tokens(f) <= 2000, f.name


def test_frontmatter():
    head = (SKILL / "SKILL.md").read_text(encoding="utf-8").split("---")[1]
    assert "name: product-layer" in head
    assert "description:" in head


def test_rule_ids_unique():
    ids = defined_rules()
    assert len(ids) == len(set(ids)), sorted(i for i in ids if ids.count(i) > 1)


def test_rule_refs_resolve():
    ids = set(defined_rules())
    for f in ALL:
        for p, n in RULE_REF.findall(f.read_text(encoding="utf-8")):
            assert f"{p}-{n}" in ids, f"{f.name}: {p}-{n}"


def test_path_refs_resolve():
    for f in ALL:
        for ref in PATH_REF.findall(f.read_text(encoding="utf-8")):
            rel = ref if ref.startswith("references/") else f"references/{ref}"
            assert (SKILL / rel).exists(), f"{f.name}: {ref}"


def test_no_visual_values():
    for f in ALL:
        hits = VISUAL.findall(f.read_text(encoding="utf-8"))
        assert not hits, f"{f.name}: {hits}"


def test_rule_has_why_and_examples():
    for f in [*CORE, *MODULES]:
        parts = RULE_HEADING.split(f.read_text(encoding="utf-8"))[1:]
        for i in range(0, len(parts), 3):
            body = parts[i + 2].split("\n## ")[0]
            for field in ("**Rule.**", "**Why.**", "Bad:", "Good:"):
                assert field in body, f"{f.name}: {parts[i]}-{parts[i + 1]} lacks {field}"


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
    for f in ALL:
        print(f"{tokens(f):>6}  {f.relative_to(SKILL)}")
    print(f"{sum(tokens(f) for f in CORE):>6}  core total")
    print("ok")
