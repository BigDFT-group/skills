# Agent Instructions for This Repository

This repository contains portable, independently installable skill files.

The primary installable units are:

```text
skills/<skill-name>/SKILL.md
```

Each skill directory name should match the `name` field in the `SKILL.md` YAML frontmatter.

## Core Rules

When working in this repository:

1. Preserve the one-directory-per-skill structure.
2. Use lowercase hyphenated skill names.
3. Use the naming pattern `<project>-<role>`.
4. Keep each skill independently installable.
5. Embed essential context directly in the skill file.
6. Embed essential snippets directly in the skill file.
7. Use `examples/` only for optional extended examples.
8. Do not create `api-user.SKILL.md`, `maintainer.SKILL.md`, or similar multi-skill files inside one project directory.
9. Do not merge unrelated roles into one large skill unless explicitly requested.
10. Preserve GPL-3.0-or-later SPDX headers.
11. Preserve attribution for adapted snippets.
12. Do not include confidential, proprietary, unclear-license, or incompatible-license material.

## Skill Naming

Use:

```text
skills/<project>-<role>/SKILL.md
```

Good examples:

```text
skills/psolver-api-user/SKILL.md
skills/psolver-maintainer/SKILL.md
skills/psolver-ci-debugging/SKILL.md
skills/futile-api-user/SKILL.md
skills/bigdft-workflows/SKILL.md
```

Avoid:

```text
skills/psolver/api-user.SKILL.md
skills/psolver/maintainer.SKILL.md
skills/PSolver_API_User/SKILL.md
```

## Skill Frontmatter

Every `SKILL.md` should start with:

```markdown
---
name: skill-name
description: Use this skill when ...
license: GPL-3.0-or-later
---
```

Then include:

```markdown
<!--
SPDX-License-Identifier: GPL-3.0-or-later
-->
```

## Scope Control

Do not assume that one project has only one skill.

A project may have separate skills for:

- API usage;
- source maintenance;
- CI debugging;
- performance;
- documentation;
- packaging;
- release workflows;
- HPC workflows.

If a new task does not fit an existing role, propose a new role-specific skill rather than overloading an unrelated one.

## Portability Requirement

Each skill file must be useful if copied alone.

This means:

- include minimal project context inside the skill;
- include essential snippets inside the skill;
- do not require access to `examples/`;
- do not require access to other skill files;
- external links may supplement but must not be required.

## Examples

The `examples/` directory contains optional extended examples only.

Do not move essential operational knowledge from a skill into `examples/`.

## Licensing

The repository default is GPL-3.0-or-later.

A skill file does not relicense the upstream project it describes.

When adding snippets:

- prefer original examples;
- use short snippets;
- attribute adapted upstream snippets;
- check GPL-3.0-or-later compatibility;
- avoid GPL-2.0-only, AGPL, proprietary, confidential, or unclear-license material unless explicitly reviewed.

## When Updating the Repository

Before finishing a change, check:

- Does each new skill have its own directory?
- Does each skill directory contain exactly one `SKILL.md` as the main skill?
- Does the frontmatter `name` match the directory name?
- Is the skill self-contained?
- Is the skill role-specific?
- Is `skills/README.md` updated?
- Is `NOTICE.md` updated if needed?
