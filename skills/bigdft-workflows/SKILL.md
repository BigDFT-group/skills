---
name: bigdft-workflows
description: Use this skill when the user wants to plan a BigDFT task at the workflow level, choose the right operational path, combine input preparation with execution and analysis, or decide which more specific BigDFT skill should be used. Do not use it for detailed source maintenance of a specific library when a more specific maintainer skill applies.
license: GPL-3.0-or-later
---

<!--
SPDX-License-Identifier: GPL-3.0-or-later

This file summarizes workflow boundaries derived from the portable BigDFT skill
set. Some role descriptions were adapted from william-dawson/bigdft-skills at
commit 3ee7e78b2443da258e37c8e7b18b79c4b1af9b4a; upstream plugin metadata declares license: MIT.
-->

# Skill: BigDFT Workflows

## Purpose

Use this skill to orient a BigDFT task before selecting a more specific operational path. BigDFT is a wavelet-based electronic-structure code with Python workflow tools, Fortran libraries, RemoteManager integration, and several specialized components.

## Scope

This skill is for:

- planning a BigDFT calculation workflow from input preparation through result analysis;
- identifying whether the user needs input generation, system construction, pseudopotentials, installation, logfile analysis, RemoteManager execution, or source maintenance;
- keeping BigDFT user workflows distinct from low-level library maintenance.

This skill is not for:

- detailed maintenance of PSolver, Futile, liborbs, ATlab, projectors, or input-variable plumbing;
- CI-only failure triage;
- WISE container maintenance.

## Workflow Decision Guide

Use the user's intent to choose the work mode:

| User intent | Work mode |
|---|---|
| Prepare `input.yaml` or PyBigDFT input dictionaries | BigDFT input preparation |
| Build or edit atomic structures with PyBigDFT | BigDFT systems API usage |
| Select PSP files or reason about valence electron counts | BigDFT pseudopotential setup |
| Configure support functions, `lin_basis_params`, or `ig_occupation` | BigDFT linear-scaling setup |
| Parse energies, forces, eigenvalues, or convergence from logfiles | BigDFT logfile analysis |
| Compile BigDFT from source | BigDFT installation |
| Run Python functions or BigDFT jobs remotely | RemoteManager HPC workflows |
| Add or modify input variables in BigDFT, CheSS, or PSolver | BigDFT input-variable maintenance |
| Work on Futile dictionaries, memory, YAML I/O, or error handling | Futile maintenance |
| Work on PSolver electrostatics or Poisson kernels | PSolver maintenance |
| Work on orbital descriptors, wavelet compression, or views | BigDFT liborbs maintenance |
| Work on domains, grids, multipoles, or field I/O | BigDFT ATlab maintenance |
| Work on nonlocal pseudopotential projector math or kernels | BigDFT projector maintenance |

## Minimal Project Context

BigDFT workflows commonly combine:

1. system construction with PyBigDFT `Atom`, `Fragment`, and `System` classes;
2. input preparation through YAML dictionaries or PyBigDFT input helpers;
3. pseudopotential selection, which controls valence electron counts and can affect linear-scaling basis choices;
4. local or remote execution;
5. logfile parsing for energies, forces, eigenvalues, convergence, and metadata.

For source-level tasks, BigDFT includes several specialized libraries. Do not give generic advice when a component-specific maintenance skill is more appropriate.

## Agent Responsibilities

The agent should:

- identify the user's role before giving detailed instructions;
- keep user-facing calculation setup separate from source-maintenance guidance;
- preserve license and attribution metadata when moving snippets between skills;
- mark uncertain BigDFT behavior as TODO rather than inventing APIs or defaults;
- prefer project-specific BigDFT patterns over generic DFT or generic HPC advice;
- when a BigDFT-related thread validates reusable operational knowledge, ask whether the corresponding canonical skill file in the project-skills repository should be updated.

The agent should not:

- merge unrelated roles into this broad workflow skill;
- assume RemoteManager, PyBigDFT, or BigDFT executables are installed without checking;
- depend on optional examples outside this file for essential behavior;
- treat installed runtime copies under `~/.codex/skills` as the canonical source for skill maintenance.

## Skill Maintenance Feedback

If a thread reveals that a BigDFT, PSolver, Futile, RemoteManager, or WISE skill is missing important reusable guidance, update the canonical repository copy first:

```text
/workspace/Sync/gitprojects/project-skills/skills/<skill-name>/SKILL.md
```

Preserve the GPL-3.0-or-later frontmatter, SPDX header, role-specific scope, and attribution notes. Update `skills/README.md` if the skill scope or description changes, and update `NOTICE.md` if new adapted snippets or attribution details are added.

After editing a canonical skill, validate and reinstall:

```bash
python3 scripts/validate_skills.py
scripts/install-codex-skills.sh install
```

If a runtime copy under `~/.codex/skills` was edited during experimentation, compare it against the canonical skill and import only reviewed changes:

```bash
scripts/install-codex-skills.sh diff <skill-name>
scripts/install-codex-skills.sh import-one <skill-name>
scripts/install-codex-skills.sh install
```

## Essential Checks

For a user workflow, establish these facts early:

```bash
python3 -c "import BigDFT; print('PyBigDFT available')" 2>/dev/null
python3 -c "import remotemanager; print(remotemanager.__version__)" 2>/dev/null
command -v bigdft 2>/dev/null
```

If a check fails, do not fabricate an environment. Ask whether the user wants installation guidance, local Python-only preparation, or remote execution setup.

## Licensing Notes

This skill file is licensed under GPL-3.0-or-later. Adapted role descriptions from william-dawson/bigdft-skills are MIT-licensed upstream and attributed in `NOTICE.md`.
