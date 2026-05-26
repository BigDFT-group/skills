# Notices and Attributions

This repository contains GPL-3.0-or-later skill files and examples for AI-assisted project usage, maintenance, and workflow support.

Some files may contain short snippets adapted from upstream open-source projects. Where applicable, attribution should be provided here.

## General Policy

When a skill includes an adapted snippet, record:

- upstream project name;
- upstream license;
- source file or documentation page, when known;
- repository file containing the snippet.

## BigDFT

Some examples may be adapted from BigDFT usage patterns or documentation.

Upstream project: BigDFT  
Upstream license: see the BigDFT upstream repository  
Relevant files:

```text
skills/bigdft-atlab-maintainer/SKILL.md
skills/bigdft-input-preparation/SKILL.md
skills/bigdft-input-variable-maintainer/SKILL.md
skills/bigdft-installation/SKILL.md
skills/bigdft-liborbs-maintainer/SKILL.md
skills/bigdft-linear-scaling/SKILL.md
skills/bigdft-logfile-analysis/SKILL.md
skills/bigdft-projectors-maintainer/SKILL.md
skills/bigdft-pseudopotentials/SKILL.md
skills/bigdft-systems-api-user/SKILL.md
skills/bigdft-workflows/SKILL.md
examples/bigdft/
```

## william-dawson/bigdft-skills

Several role-specific skill files were adapted from the public Claude Code
plugin repository `william-dawson/bigdft-skills`.

Source repository: `git@github.com:william-dawson/bigdft-skills.git`  
Source commit: `3ee7e78b2443da258e37c8e7b18b79c4b1af9b4a`  
Upstream plugin metadata license: MIT  
Upstream author metadata: William Dawson

The source skills were converted from topic-only Claude plugin skill names into
the portable `skills/<project>-<role>/SKILL.md` layout, given GPL-3.0-or-later
frontmatter for this repository, and annotated with source provenance comments.

Relevant source-to-repository mappings:

```text
skills/atlab/SKILL.md              -> skills/bigdft-atlab-maintainer/SKILL.md
skills/dataset/SKILL.md            -> skills/remotemanager-hpc-workflows/SKILL.md
skills/futile/SKILL.md             -> skills/futile-maintainer/SKILL.md
skills/input/SKILL.md              -> skills/bigdft-input-preparation/SKILL.md
skills/install/SKILL.md            -> skills/bigdft-installation/SKILL.md
skills/liborbs/SKILL.md            -> skills/bigdft-liborbs-maintainer/SKILL.md
skills/linear-scaling/SKILL.md     -> skills/bigdft-linear-scaling/SKILL.md
skills/logfile/SKILL.md            -> skills/bigdft-logfile-analysis/SKILL.md
skills/projectors/SKILL.md         -> skills/bigdft-projectors-maintainer/SKILL.md
skills/pseudopotentials/SKILL.md   -> skills/bigdft-pseudopotentials/SKILL.md
skills/psolver/SKILL.md            -> skills/psolver-maintainer/SKILL.md
skills/remote/SKILL.md             -> skills/remotemanager-hpc-workflows/SKILL.md
skills/systems/SKILL.md            -> skills/bigdft-systems-api-user/SKILL.md
skills/variables/SKILL.md          -> skills/bigdft-input-variable-maintainer/SKILL.md
```

## PSolver

Some examples may be adapted from PSolver usage patterns or documentation.

Upstream project: PSolver  
Upstream license: see the PSolver upstream repository  
Relevant files:

```text
skills/psolver-api-user/SKILL.md
skills/psolver-maintainer/SKILL.md
skills/psolver-ci-debugging/SKILL.md
```

## Futile

Some examples may be adapted from Futile usage patterns or documentation.

Upstream project: Futile  
Upstream license: see the Futile upstream repository  
Relevant files:

```text
skills/futile-api-user/SKILL.md
skills/futile-maintainer/SKILL.md
```

## RemoteManager

Some examples may be adapted from RemoteManager usage patterns or documentation.

Upstream project: RemoteManager  
Upstream license: see the RemoteManager upstream repository  
Relevant files:

```text
skills/remotemanager-hpc-workflows/SKILL.md
```

## WISE

Some examples may be adapted from WISE usage patterns or documentation.

Upstream project: WISE  
Upstream license: see the WISE upstream repository  
Relevant files:

```text
skills/wise-container-maintainer/SKILL.md
examples/wise/
```
