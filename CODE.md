# CODE.md

This file provides coding-agent maintenance rules for this repository.

It is intentionally generic and can be read by agents or humans that do not consume `AGENTS.md`, `CLAUDE.md`, or `SKILL.md` bundles directly.

## Repository Invariant

The repository is a library of independent skill bundles.

A skill bundle is:

```text
skills/<skill-name>/SKILL.md
```

The skill name must be lowercase and hyphenated.

The skill name should normally be:

```text
<project>-<role>
```

## Do Not Break These Conventions

Do not:

- rename `SKILL.md` to a role-specific filename;
- put many role-specific skill files inside one project directory;
- make a skill depend on `examples/`;
- remove YAML frontmatter;
- remove SPDX headers;
- merge API usage, source maintenance, and CI debugging into one vague skill;
- include copied upstream code without attribution and license compatibility review.

## Expected File Types

- `README.md`: human-facing repository explanation.
- `AGENTS.md`: generic agent adapter.
- `CLAUDE.md`: Claude-style adapter.
- `CODE.md`: generic coding-agent rules.
- `.github/copilot-instructions.md`: GitHub Copilot / VS Code adapter.
- `.zed/rules/skills.md`: Zed rule adapter.
- `skills/README.md`: skill index.
- `skills/<skill-name>/SKILL.md`: installable skill.
- `templates/skill/SKILL.md`: template for new skills.
- `examples/`: optional extended examples only.

## Review Checklist

Before committing:

- [ ] New skill names are lowercase and hyphenated.
- [ ] Each skill has `SKILL.md`.
- [ ] Frontmatter `name` equals directory name.
- [ ] `description` clearly states when to use and not use the skill.
- [ ] Each skill is self-contained.
- [ ] Essential snippets are embedded.
- [ ] Optional examples are under `examples/`.
- [ ] `skills/README.md` is updated.
- [ ] `NOTICE.md` is updated if snippets are adapted.
