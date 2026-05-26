#!/usr/bin/env python3
"""Validate portable skill repository invariants."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REQUIRED_ADAPTERS = [
    ROOT / "AGENTS.md",
    ROOT / "CLAUDE.md",
    ROOT / "CODE.md",
    ROOT / ".github" / "copilot-instructions.md",
    ROOT / ".zed" / "rules" / "skills.md",
]


def parse_frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("missing opening YAML frontmatter delimiter")

    data: dict[str, str] = {}
    for index, line in enumerate(lines[1:], start=1):
        if line == "---":
            if index == 1:
                raise ValueError("empty YAML frontmatter")
            return data
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line: {line!r}")
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()

    raise ValueError("missing closing YAML frontmatter delimiter")


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_name = skill_dir.name
    skill_file = skill_dir / "SKILL.md"

    if not NAME_RE.fullmatch(skill_name):
        errors.append(f"{skill_dir}: skill directory name must be lowercase ASCII with hyphens")

    if not skill_file.exists():
        errors.append(f"{skill_dir}: missing SKILL.md")
        return errors

    try:
        frontmatter = parse_frontmatter(skill_file)
    except ValueError as exc:
        errors.append(f"{skill_file}: {exc}")
        return errors

    actual_name = frontmatter.get("name")
    if actual_name != skill_name:
        errors.append(f"{skill_file}: frontmatter name {actual_name!r} does not match {skill_name!r}")

    description = frontmatter.get("description", "")
    if not description:
        errors.append(f"{skill_file}: missing description")
    elif "Use this skill when" not in description:
        errors.append(f"{skill_file}: description should state when to use the skill")

    if frontmatter.get("license") != "GPL-3.0-or-later":
        errors.append(f"{skill_file}: license must be GPL-3.0-or-later")

    text = skill_file.read_text(encoding="utf-8")
    if "SPDX-License-Identifier: GPL-3.0-or-later" not in text:
        errors.append(f"{skill_file}: missing GPL-3.0-or-later SPDX header")

    nested_skill_files = [path for path in skill_dir.rglob("*.md") if path.name != "SKILL.md"]
    for nested in nested_skill_files:
        errors.append(f"{nested}: skill bundle should not contain extra Markdown skill files")

    return errors


def main() -> int:
    errors: list[str] = []

    for path in REQUIRED_ADAPTERS:
        if not path.exists():
            errors.append(f"{path.relative_to(ROOT)}: required adapter file is missing")

    if not SKILLS_DIR.exists():
        errors.append("skills/: directory is missing")
    else:
        skill_dirs = sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir())
        if not skill_dirs:
            errors.append("skills/: no skill bundles found")
        for skill_dir in skill_dirs:
            errors.extend(validate_skill(skill_dir))

    template = ROOT / "templates" / "skill" / "SKILL.md"
    if not template.exists():
        errors.append("templates/skill/SKILL.md: template is missing")
    elif "SPDX-License-Identifier: GPL-3.0-or-later" not in template.read_text(encoding="utf-8"):
        errors.append("templates/skill/SKILL.md: missing GPL-3.0-or-later SPDX header")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Skill repository validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
