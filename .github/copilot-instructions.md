# GitHub Copilot Instructions

This repository is a public library of portable, independently installable
skill bundles for AI-assisted scientific software work.

## Repository Invariant

Each installable skill is stored as:

```text
skills/<skill-name>/SKILL.md
```

The skill directory name must match the `name` field in the YAML frontmatter.

Use lowercase ASCII letters, digits, and hyphens only. Prefer:

```text
<project>-<role>
```

Examples:

```text
skills/psolver-api-user/SKILL.md
skills/psolver-maintainer/SKILL.md
skills/psolver-ci-debugging/SKILL.md
skills/futile-api-user/SKILL.md
skills/bigdft-workflows/SKILL.md
skills/remotemanager-hpc-workflows/SKILL.md
skills/wise-container-maintainer/SKILL.md
```

Do not create structures such as:

```text
skills/psolver/api-user.SKILL.md
skills/psolver/maintainer.SKILL.md
```

## Skill Files

Every `SKILL.md` must start with YAML frontmatter:

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

Write descriptions so an agent can decide when to load the skill and when not
to load it.

## Portability

Each skill must remain useful if copied alone into another project, IDE, WISE
environment, or agentic execution environment.

Keep essential context, commands, and short snippets directly inside the
`SKILL.md` file. Use `examples/` only for optional extended material. Do not
make one skill depend on another skill file or on examples.

## Role Boundaries

Keep skills role-specific. Do not mix API usage, source maintenance, CI
debugging, performance work, documentation, packaging, and release workflows
unless the user explicitly asks for a combined skill and the scope is justified.

When adding information from another project, decide whether it belongs in an
existing skill, a new role-specific skill, an optional example, `NOTICE.md`,
`skills/README.md`, or nowhere.

## Licensing

The repository default is GPL-3.0-or-later. This does not relicense upstream
projects described by the skills.

Do not include proprietary, confidential, unclear-license, GPL-2.0-only, or
AGPL material unless explicitly reviewed. Prefer original summaries and short,
essential snippets with attribution.

Update `NOTICE.md` when snippets are adapted from upstream material.
