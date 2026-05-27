# Project Skills Repository

This repository is a public library of **portable, independently installable skill files** for AI-assisted project usage, software maintenance, documentation, CI debugging, and scientific workflow support.

The repository is designed for environments such as WISE, AI-enabled IDEs, coding agents, MCP/ACP-based tooling, and other agentic development workflows.

The main design principle is:

```text
Each skill is an independently installable unit.
```

A skill should remain useful when copied alone into another project, IDE, or execution environment.

---

## Repository Goals

This repository provides:

- reusable skill files for project-specific AI agents;
- clear conventions for naming and structuring skills;
- role-specific skills for different usage modes;
- GPL-3.0-or-later licensing for the skill files;
- conservative rules for including real code snippets;
- adapter files for agents that consume repository-level instructions rather than skill bundles;
- templates for adding future skills consistently.

---

## License

Unless otherwise stated, the skill files and repository documentation are licensed under:

```text
GPL-3.0-or-later
```

Each skill file should include:

```markdown
<!--
SPDX-License-Identifier: GPL-3.0-or-later
-->
```

The GPL-3.0-or-later license applies to the contents of this repository.

It does **not** relicense the upstream projects described by the skills.

For example:

```text
skills/psolver-api-user/SKILL.md       GPL-3.0-or-later
PSolver source code                    governed by the PSolver upstream license

skills/futile-maintainer/SKILL.md      GPL-3.0-or-later
Futile source code                     governed by the Futile upstream license
```

---

## Why GPL-3.0-or-later?

The skills may contain short code snippets, command examples, configuration fragments, or usage patterns adapted from real open-source projects.

GPL-3.0-or-later is used because:

- redistributed modifications of skill files remain under the same license;
- snippets from GPL-compatible upstream projects can be included more safely than under a permissive-only license;
- Apache-2.0, MIT, BSD, and similar permissive snippets can generally be included in GPL-3.0-or-later material, while the reverse is not generally true for GPL snippets inside Apache-2.0 files;
- the repository is intended as a shared open knowledge base for agentic maintenance.

This repository does not remove the need to respect upstream licenses. Contributors must not include proprietary, confidential, unclear-license, or GPL-2.0-only material unless the compatibility situation has been explicitly reviewed.

---

## Skill Granularity Policy

Skills are organized by both **project** and **role**.

A project may need multiple skills because agent behavior differs depending on the task.

For example, for a subproject such as `PSolver` or `Futile`, the following are different use cases:

```text
API usage
source maintenance
CI debugging
performance analysis
documentation
packaging and release
```

These use cases should not be mixed into one large ambiguous skill file unless there is a strong reason.

The preferred naming pattern is:

```text
skills/<project>-<role>/SKILL.md
```

Examples:

```text
skills/psolver-api-user/SKILL.md
skills/psolver-maintainer/SKILL.md
skills/psolver-ci-debugging/SKILL.md
skills/futile-api-user/SKILL.md
skills/futile-maintainer/SKILL.md
skills/bigdft-workflows/SKILL.md
skills/remotemanager-hpc-workflows/SKILL.md
skills/wise-container-maintainer/SKILL.md
```

The skill directory name should match the `name` field in the YAML frontmatter of `SKILL.md`.

---

## Naming Rules

Use lowercase ASCII letters, digits, and hyphens.

Recommended format:

```text
<project>-<role>
```

Examples:

```text
psolver-api-user
psolver-maintainer
psolver-ci-debugging
psolver-performance
futile-api-user
futile-maintainer
bigdft-workflows
remotemanager-hpc-workflows
wise-container-maintainer
```

Avoid:

```text
PSolver_API_User
psolver/api-user.SKILL.md
psolver.api.user
api-user.SKILL.md
```

Rationale:

- one directory corresponds to one installable skill;
- the literal file name `SKILL.md` is easy for skill-compatible agents to discover;
- lowercase hyphenated names are robust across filesystems, shells, URLs, and packaging tools;
- the project and role are visible from the directory name.

---

## Skill Bundle Format

Each installable skill is a directory containing one required file:

```text
skills/<skill-name>/SKILL.md
```

The `SKILL.md` file should begin with YAML frontmatter:

```markdown
---
name: psolver-api-user
description: Use this skill when the user wants to call the PSolver API, understand public interfaces, prepare input data, or integrate PSolver as a library. Do not use it for source maintenance, CI debugging, or internal refactoring.
license: GPL-3.0-or-later
---
```

Then include the SPDX header:

```markdown
<!--
SPDX-License-Identifier: GPL-3.0-or-later
-->
```

The `description` should be written so that an agent can decide whether to load the skill.

---

## Self-Contained Skills

Each `SKILL.md` file must be useful when copied alone.

Therefore:

- essential context must be embedded directly in the skill file;
- essential snippets must be embedded directly in the skill file;
- optional examples may live under `examples/`, but the skill must not depend on them;
- external links may be provided, but the skill must not require internet access;
- the skill should clearly state what it is for and what it is not for.

Good pattern:

```text
skills/psolver-api-user/SKILL.md
```

contains the minimal project context, scope, boundaries, and essential examples needed for API usage.

Optional extended material may exist at:

```text
examples/psolver/
```

but the skill must still function without it.

---

## Examples Directory

The `examples/` directory contains optional extended examples.

These files are useful for testing, demonstration, and deeper documentation, but they are not required for installing or using an individual skill.

When a code pattern is essential for the agent's behavior, include it directly in the corresponding `SKILL.md`.

Use `examples/` for:

- longer executable examples;
- complete scripts;
- demonstration configurations;
- files that are too long to embed directly in a skill;
- examples intended for human testing or CI.

Do not use `examples/` for information that the skill requires in order to work.

---

## Code Snippet Policy

Skill files may include short snippets when those snippets are necessary to describe real usage.

This is encouraged when artificial examples would mislead the agent.

However:

- prefer short snippets;
- attribute adapted snippets;
- preserve required upstream notices;
- include only GPL-3.0-or-later-compatible material;
- do not copy large portions of upstream documentation;
- do not include confidential or proprietary content.

Recommended attribution block:

```markdown
<!--
Snippet adapted from PROJECT_NAME.
Upstream license: LICENSE_NAME.
Source: path/to/upstream/file or documentation page, if known.
Included here under terms compatible with GPL-3.0-or-later.
-->
```

---

## Adapter Files

Not all agents discover `SKILL.md` bundles automatically.

For that reason, this repository includes adapter files:

```text
AGENTS.md
CLAUDE.md
CODE.md
.github/copilot-instructions.md
.zed/rules/skills.md
```

These files explain the repository conventions to agents that consume project-level instructions.

The adapters do not replace the skill files. They tell the agent how to select, preserve, and update the skills.

---

## Recommended Repository Layout

```text
.
├── README.md
├── LICENSE
├── NOTICE.md
├── CONTRIBUTING.md
├── AGENTS.md
├── CLAUDE.md
├── CODE.md
├── .github/
│   └── copilot-instructions.md
├── .zed/
│   └── rules/
│       └── skills.md
├── skills/
│   ├── README.md
│   ├── psolver-api-user/
│   │   └── SKILL.md
│   ├── psolver-maintainer/
│   │   └── SKILL.md
│   ├── psolver-ci-debugging/
│   │   └── SKILL.md
│   ├── futile-api-user/
│   │   └── SKILL.md
│   ├── futile-maintainer/
│   │   └── SKILL.md
│   ├── bigdft-workflows/
│   │   └── SKILL.md
│   ├── remotemanager-hpc-workflows/
│   │   └── SKILL.md
│   └── wise-container-maintainer/
│       └── SKILL.md
├── templates/
│   └── skill/
│       └── SKILL.md
└── examples/
    ├── bigdft/
    │   └── dry_run.py
    └── wise/
        └── compose-example.yaml
```

---

## Adding a New Skill

To add a skill:

1. Choose the project.
2. Choose the role.
3. Create a lowercase hyphenated skill name.
4. Create `skills/<skill-name>/SKILL.md`.
5. Add YAML frontmatter.
6. Add an SPDX header.
7. Make the skill self-contained.
8. Add essential snippets directly in the skill.
9. Put only optional extended examples under `examples/`.
10. Update `skills/README.md`.
11. Update `NOTICE.md` if snippets were adapted from upstream material.

Example:

```bash
mkdir -p skills/psolver-performance
cp templates/skill/SKILL.md skills/psolver-performance/SKILL.md
```

Then edit:

```yaml
name: psolver-performance
description: Use this skill when the user wants to analyze or improve PSolver performance, scaling, memory usage, accelerator behavior, or numerical kernels.
license: GPL-3.0-or-later
```

---

## Updating Existing Skills

When modifying an existing skill:

- preserve the directory name unless the skill identity truly changes;
- keep the `name` field identical to the directory name;
- update the `description` if the scope changes;
- avoid merging unrelated roles into one skill;
- keep the skill independently installable;
- preserve SPDX and attribution blocks;
- update `skills/README.md` if the role or scope changes.

---

## Installing Skills for Codex

Install the repository skills into Codex with:

```bash
scripts/install-codex-skills.sh install
```

By default, skills are copied to:

```text
${CODEX_SKILLS_DIR:-${CODEX_HOME:-$HOME/.codex}/skills}
```

Use `--dest DIR` for a project-local or test installation:

```bash
scripts/install-codex-skills.sh install --dest .codex/skills
```

The repository copy under `skills/<skill-name>/SKILL.md` is canonical. Installed copies under `~/.codex/skills` or `$CODEX_HOME/skills` are runtime deployment copies. Do not make unreviewed runtime edits the source of truth.

Useful commands:

```bash
scripts/install-codex-skills.sh list
scripts/install-codex-skills.sh diff
scripts/install-codex-skills.sh diff <skill-name>
scripts/install-codex-skills.sh import-one <skill-name>
```

Use `import-one` only after reviewing an intentional improvement made to an installed runtime copy. After importing or editing a canonical skill, run validation and reinstall:

```bash
python3 scripts/validate_skills.py
scripts/install-codex-skills.sh install
```

For Zed or another Codex frontend, keep the skills installed in the Codex skills directory and use a small project rule or `AGENTS.md` instruction to consider `bigdft-workflows` for BigDFT-related threads. This avoids loading every detailed skill body into unrelated conversations.

---

## Validation and Documentation CI

The repository includes a GitHub Actions workflow at:

```text
.github/workflows/docs.yml
```

The workflow validates the portable skill structure and builds a static
documentation site from the repository README, contributing guide, notice file,
and every `skills/<skill-name>/SKILL.md` file.

Run the same checks locally with:

```bash
python scripts/validate_skills.py
python scripts/build_docs.py
```

The generated site is written to:

```text
site/
```

On pull requests, CI validates and builds the site as an artifact. On pushes to
`main`, the workflow deploys the generated site to GitHub Pages.

---

## Status

This repository is intended to evolve as a shared skill library for project-specific AI agents.

The first goal is to provide clear, legally conservative, reusable skill files that can be used inside WISE, coding agents, IDEs, MCP/ACP workflows, and related environments.
