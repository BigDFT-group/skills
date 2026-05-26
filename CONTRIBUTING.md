# Contributing

Thank you for contributing to this project skills repository.

## Main Convention

Each skill is an independently installable directory:

```text
skills/<skill-name>/SKILL.md
```

Do not create multiple differently named skill files inside one project directory.

## Naming

Use:

```text
<project>-<role>
```

Examples:

```text
psolver-api-user
psolver-maintainer
futile-api-user
wise-container-maintainer
```

## Required Skill Header

Each `SKILL.md` must begin with YAML frontmatter:

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

## Self-Contained Skill Rule

Each skill must be useful when copied alone.

Essential context and essential snippets must be embedded directly in the skill.

Optional extended examples may be placed under `examples/`.

## Snippet Rules

Contributors should:

1. Write original snippets whenever possible.
2. Prefer short snippets.
3. Attribute adapted snippets.
4. Preserve required upstream notices.
5. Include only GPL-3.0-or-later-compatible material.
6. Avoid confidential, proprietary, unclear-license, or GPL-2.0-only material unless explicitly reviewed.

## Pull Request Checklist

Before submitting:

- [ ] New skill names are lowercase and hyphenated.
- [ ] Each new skill has its own directory.
- [ ] Each skill directory contains `SKILL.md`.
- [ ] The frontmatter `name` matches the directory name.
- [ ] The skill has a clear role and scope.
- [ ] The skill is independently installable.
- [ ] Essential examples are embedded.
- [ ] Optional examples are under `examples/`.
- [ ] SPDX headers are present.
- [ ] `skills/README.md` has been updated.
- [ ] `NOTICE.md` has been updated if snippets are adapted.

## Local Validation

Before opening a pull request, run:

```bash
python scripts/validate_skills.py
python scripts/build_docs.py
```

The first command checks the repository conventions. The second command builds
the static documentation site under `site/`, which is the same site published by
the GitHub Pages workflow on pushes to `main`.
