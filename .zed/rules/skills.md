# Portable Skills Repository Rules

This repository is a library of independent skill bundles.

## Skill Layout

The only installable skill layout is:

```text
skills/<skill-name>/SKILL.md
```

The directory name must match the frontmatter `name` field. Use lowercase
ASCII letters, digits, and hyphens only. Prefer `<project>-<role>`.

Correct:

```text
skills/psolver-api-user/SKILL.md
skills/psolver-maintainer/SKILL.md
skills/futile-api-user/SKILL.md
```

Incorrect:

```text
skills/psolver/api-user.SKILL.md
skills/psolver/maintainer.SKILL.md
skills/PSolver_API_User/SKILL.md
```

## Required Skill Header

Every skill file must begin with:

```markdown
---
name: skill-name
description: Use this skill when ...
license: GPL-3.0-or-later
---

<!--
SPDX-License-Identifier: GPL-3.0-or-later
-->
```

The description must explain both the intended use and the adjacent roles that
should use a different skill.

## Maintenance Rules

- Keep each `SKILL.md` independently installable.
- Put essential context, commands, and snippets directly in the skill file.
- Use `examples/` only for optional extended examples.
- Do not make a skill depend on another skill file.
- Do not merge unrelated roles into one large skill.
- Update `skills/README.md` when adding, renaming, or changing a skill.
- Update `NOTICE.md` when adapted snippets or attribution details are added.
- Preserve GPL-3.0-or-later SPDX headers.
- Do not invent APIs, commands, project behavior, or upstream licensing facts.

When upstream project details are uncertain, leave a TODO or ask for
confirmation instead of adding unsupported operational instructions.
