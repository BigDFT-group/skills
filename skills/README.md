# Skills Index

This directory contains independently installable skill bundles.

Each skill is stored as:

```text
skills/<skill-name>/SKILL.md
```

The skill name should match the `name` field in the YAML frontmatter.

## Available Skills

| Skill | Project | Role | Use when |
|---|---|---|---|
| `psolver-api-user` | PSolver | API usage | The user wants to call PSolver APIs, understand public interfaces, or integrate PSolver as a library. |
| `psolver-maintainer` | PSolver | Source maintenance | The user wants to modify, debug, refactor, test, or maintain PSolver source code. |
| `psolver-ci-debugging` | PSolver | CI debugging | The user wants to understand or fix PSolver build, test, or CI failures. |
| `futile-api-user` | Futile | API usage | The user wants to call Futile APIs or understand public interfaces. |
| `futile-maintainer` | Futile | Source maintenance | The user wants to modify, debug, refactor, test, or maintain Futile source code. |
| `bigdft-workflows` | BigDFT | Workflows | The user wants to design or run BigDFT workflows, including dry runs and RemoteManager-related patterns. |
| `remotemanager-hpc-workflows` | RemoteManager | HPC workflows | The user wants to define, submit, validate, or reason about remote HPC workflows. |
| `wise-container-maintainer` | WISE | Container maintenance | The user wants to maintain WISE container images, IDE integration, or agentic development environments. |

## Adding a Skill

1. Create `skills/<project>-<role>/SKILL.md`.
2. Use the template from `templates/skill/SKILL.md`.
3. Make the skill self-contained.
4. Add the skill to this index.
5. Update `NOTICE.md` if snippets are adapted from upstream projects.
