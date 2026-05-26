# Claude Adapter Instructions

This file adapts the repository conventions for Claude-style coding agents.

The authoritative repository-wide instructions are in `AGENTS.md`.

When working in this repository, follow `AGENTS.md` first.

## Summary

This repository is a collection of portable skill bundles.

Each installable skill is:

```text
skills/<skill-name>/SKILL.md
```

Do not convert the repository to a structure where multiple skills are stored as differently named `*.SKILL.md` files inside one project directory.

Correct:

```text
skills/psolver-api-user/SKILL.md
skills/psolver-maintainer/SKILL.md
```

Incorrect:

```text
skills/psolver/api-user.SKILL.md
skills/psolver/maintainer.SKILL.md
```

## Editing Behavior

When asked to add or modify a skill:

1. Determine the project.
2. Determine the role.
3. Use `<project>-<role>` as the skill name.
4. Create or modify `skills/<skill-name>/SKILL.md`.
5. Keep the skill self-contained.
6. Update `skills/README.md`.
7. Preserve GPL-3.0-or-later licensing and attribution blocks.

## License Boundary

The skill files are GPL-3.0-or-later.

The upstream projects described by the skills keep their own licenses.
