---
name: remotemanager-hpc-workflows
description: Use this skill when the user wants to define, validate, submit, inspect, or reason about remote HPC workflows. Do not use it for generic shell scripting, unrelated cluster administration, or low-level RemoteManager source maintenance.
license: GPL-3.0-or-later
---

<!--
SPDX-License-Identifier: GPL-3.0-or-later
-->

# Skill: RemoteManager HPC Workflows

## Purpose

This role-specific skill guides an AI agent when working with **RemoteManager** in the context of **HPC workflow orchestration**.

## Scope

This skill is for:

- define, validate, submit, inspect, or reason about remote HPC workflows;
- answering questions within the declared role;
- using real project conventions where known;
- avoiding behavior that belongs to a different skill.

This skill is not for:

- generic shell scripting, unrelated cluster administration, or low-level RemoteManager source maintenance.

## Minimal Project Context

TODO: Add a concise description of RemoteManager that is sufficient for this skill to be useful when copied alone.

## Agent Responsibilities

The agent should:

- stay within the role of this skill;
- prefer accurate, project-specific guidance over generic advice;
- distinguish public APIs from internal implementation details;
- preserve licensing and attribution metadata;
- suggest updates to this skill when recurring missing knowledge is identified.

The agent should not:

- invent APIs or commands;
- remove license headers;
- include confidential or unclear-license material;
- assume that optional files from `examples/` are installed;
- silently switch to a different role without stating why.

## Common Tasks

TODO: List common tasks for this role.

## Essential Commands and Workflows

TODO: Add short essential commands directly here.

## Essential Snippets

TODO: Add short essential snippets directly here if needed.

## Optional Extended Examples

Optional extended examples may exist in the repository under `examples/`, but this skill must remain operational without them.

## Safety and Boundaries

The agent must keep this skill role-specific. If the user asks for a different mode of work, such as source maintenance instead of API usage, the agent should suggest the corresponding skill.

## Licensing Notes

This skill file is licensed under GPL-3.0-or-later unless otherwise stated.

Any adapted snippets must be compatible with GPL-3.0-or-later and attributed either inline or in `NOTICE.md`.

## References

TODO: Add upstream project references.
