---
name: project-skills-maintainer
description: Use this skill when the user wants to update, synchronize, validate, install, commit, or push the BigDFT-group project-skills reference repository or the local Codex runtime copies in ~/.codex/skills. Do not use it for authoring unrelated project code or for ordinary use of an existing skill.
license: GPL-3.0-or-later
---

<!--
SPDX-License-Identifier: GPL-3.0-or-later
-->

# Skill: Project Skills Maintainer

## Purpose

Maintain the portable skill repository and keep it synchronized with the installed Codex runtime skills.

## Scope

This skill is for:

- updating `skills/<skill-name>/SKILL.md` in the reference repository;
- importing an intentional runtime edit from `~/.codex/skills` back into the repository;
- installing repository skill changes into the Codex runtime skills directory;
- validating skill repository invariants before commit or push;
- preparing a git commit or push for skill changes.

This skill is not for:

- modifying BigDFT, Futile, PSolver, or other project source code;
- general skill design guidance beyond this repository workflow;
- installing third-party Codex skills from another repository.

## Repository Context

The reference repository is normally a git checkout such as:

```text
/workspace/Sync/gitprojects/project-skills
```

The installed runtime copy is normally:

```text
~/.codex/skills
```

The repository copy is canonical. Runtime copies are used by Codex during work, but durable changes should be propagated back into the reference repository before committing or pushing.

## Core Workflow

When the user says a skill was updated in the runtime copy and should be saved to the reference repo, use the repository helper:

```bash
cd /workspace/Sync/gitprojects/project-skills
scripts/install-codex-skills.sh import-one <skill-name>
```

This copies:

```text
~/.codex/skills/<skill-name>/SKILL.md
```

into:

```text
skills/<skill-name>/SKILL.md
```

and validates the repository.

When the reference repository has the desired changes and they should be made available to Codex, install them back into the runtime directory:

```bash
cd /workspace/Sync/gitprojects/project-skills
scripts/install-codex-skills.sh install
```

To inspect differences between repository and runtime copies:

```bash
cd /workspace/Sync/gitprojects/project-skills
scripts/install-codex-skills.sh diff
scripts/install-codex-skills.sh diff <skill-name>
```

To list repository skills and runtime installation status:

```bash
cd /workspace/Sync/gitprojects/project-skills
scripts/install-codex-skills.sh list
```

## Validation

Before committing or pushing, run:

```bash
cd /workspace/Sync/gitprojects/project-skills
python3 scripts/validate_skills.py
```

The validator requires each skill directory to contain a `SKILL.md` with matching `name`, a `description` beginning with clear usage guidance, `license: GPL-3.0-or-later`, and the GPL SPDX header.

## Git Workflow

Before committing, inspect only relevant changes:

```bash
cd /workspace/Sync/gitprojects/project-skills
git status --short
git diff -- skills/<skill-name>/SKILL.md
```

Commit only intentional skill-repository changes:

```bash
git add skills/<skill-name>/SKILL.md
git commit -m "Update <skill-name> skill workflow"
```

Push only after validation succeeds and the user asks to push or clearly expects the repository update to be published:

```bash
git push
```

## Safety and Boundaries

- Preserve unrelated local changes in the repository and runtime skills directory.
- Treat `scripts/install-codex-skills.sh install` as repository-to-runtime propagation.
- Treat `scripts/install-codex-skills.sh import-one` as runtime-to-repository propagation for one reviewed skill.
- Do not use broad copy commands manually when the helper script can perform the synchronization and validation.
- Do not commit generated site files unless the user explicitly asks for documentation site updates.
