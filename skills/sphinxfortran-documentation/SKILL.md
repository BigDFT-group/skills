---
name: sphinxfortran-documentation
description: Use this skill when the user wants to document a Fortran library with sphinx-fortran, add source-driven Fortran API pages, create CI-covered fortranliteral examples, validate public/private API rendering, or generate LLM-ready documentation. Do not use it for unrelated Sphinx projects that do not use Fortran autodoc.
license: GPL-3.0-or-later
---

<!--
SPDX-License-Identifier: GPL-3.0-or-later
-->

# Skill: Sphinx-Fortran Documentation

## Purpose

Use this workflow to document Fortran libraries with `sphinx-fortran` while keeping the documentation maintainable, source-driven, and validated by CI.

The target contract is:

- public API facts live next to the Fortran declarations;
- examples live in executable test sources;
- source comments include tested snippets with `fortranliteral`;
- Sphinx pages define layout and select modules with autodoc directives;
- CI verifies the rendered public API, hidden private implementation details, runnable examples, and LLM export when enabled.

## Source Documentation Policy

Put API documentation in the Fortran source whenever it describes the API object itself.

```fortran
module my_module
  ! Module-level purpose and public API overview.
  implicit none
  private

  public :: compute

  interface compute
    ! Public generic interface for computing a value.
    !
    ! .. fortranliteral:: tests/example_usage.f90
    !    :marker: compute
    !    :dedent: 2
    module procedure compute_real, compute_integer
  end interface compute

  private :: compute_real, compute_integer
contains
  real function compute_real(value)
    ! Real implementation kept private behind compute.
    real, intent(in) :: value ! Value to compute.
    compute_real = value
  end function compute_real
end module my_module
```

Rules:

- Prefer default-private modules plus explicit `public ::` exports.
- Document public generic interfaces at the interface block.
- Keep private implementations private unless the page is explicitly internal developer documentation.
- Put routine/type/interface descriptions immediately after the declaration line, including declarations with standard prefixes such as `elemental pure function`, `pure function`, `recursive subroutine`, or `module procedure`; do not rely on comments placed only before the declaration, because they are not attached to the rendered API object.
- Put argument, variable, and field comments on the declaration line.
- Keep one documented entity per declaration line.
- For CI-covered examples, source comments should use `.. fortranliteral::` to include the executable snippet.

## Source-Level API Groups

Use `f:autogroup` for group-level prose that applies to several public objects in a large module, especially parameter families. Keep individual object facts on declaration lines and put only the shared concept in the group prose.

```fortran
! .. f:autogroup:: preferred-kinds
!    :title: Preferred kind parameters
!    :members: f_integer, f_double, f_byte
!
!    These names define the public ABI kind policy for host codes.
integer, parameter :: f_integer = c_int32_t ! Canonical integer kind.
integer, parameter :: f_double = c_double   ! Canonical real kind.
integer, parameter :: f_byte = c_bool       ! C-compatible logical kind.
```

`f:automodule` renders the group title, prose, and explicit members. The `:members:` option may be repeated. Grouped members are omitted from the default module member sections to avoid duplicate API entries.

## Fortranliteral Directive

Use `fortranliteral` in Fortran comments when an example should be rendered with the API object. It resolves its path relative to `fortran_literal_root` and forwards common `literalinclude` options. Prefer `:marker:` for standard snippets. Keep this directive with the public object documentation when sphinx-fortran can render that object directly; for manually documented objects, keep the directive in the `.rst` page until the object can be parsed/rendered by autodoc.


```fortran
! .. fortranliteral:: tests/example_usage.f90
!    :marker: compute
!    :dedent: 2
```

`marker: compute` expands to `start-after: doc-example-start: compute` and `end-before: doc-example-end: compute`.

## Runnable Example Policy

Examples shown in user documentation should come from code that CI compiles and runs.

Use stable markers around the snippet that the page should render:

```fortran
! doc-example-start: compute
subroutine example_compute()
  real :: result

  result = compute(2.0)
  call require(abs(result - 2.0) < epsilon(result), 'compute failed')
end subroutine example_compute
! doc-example-end: compute
```

The test program should fail nonzero on incorrect behavior. Keep examples small and focused on the public API.

## Sphinx Page Policy

Keep page structure in `.rst` files. Use `f:automodule` for source-derived API. Tested examples should usually be included from Fortran source comments with `fortranliteral`, not duplicated in the page.

```rst
My module
=========

.. f:automodule:: my_module
```

Configure `fortran_literal_root` in `conf.py` so `fortranliteral` paths are stable and project-root-relative:

```python
fortran_literal_root = os.path.abspath("..")
```

Use `:members:` to render a selected subset, `:undoc-members:` as the extension's exclusion list, and `:include-private:` only for internal/debug pages.

## CI Contract

A robust documentation CI job should:

1. install the same `sphinx-fortran` and parser dependencies used by the project;
2. compile and run every example source used by `fortranliteral` snippets;
3. build Sphinx with warnings as errors for the contract fixture or project docs;
4. run a rendered-page checker that verifies:
   - expected public symbols are present;
   - private implementation routines are absent;
   - required explanatory topics are present;
   - required `fortranliteral` example snippets are rendered;
5. when `sphinx-llm` is enabled, verify the LLM export exists, usually `llms-full.txt`.

Example rendered-page checks can be simple Python scripts that inspect generated HTML IDs and required text snippets. They should fail loudly when a public symbol, topic, or example disappears. Parser/rendering contract fixtures should include common declaration variants, including prefixed procedures such as `elemental pure function`, so source comments remain attached to the rendered API.

## Generic Interface Guidance

For generic interfaces:

- document the public interface, not each private implementation routine;
- keep implementation routines private when they are not user API;
- use implementation argument declarations to provide types, intents, optional attributes, and argument descriptions;
- add parser/rendering contract tests before relying on unusual Fortran spellings.

The expected rendered behavior is that the public interface appears, private implementations do not appear as separate API entries, and merged argument information is visible on the interface entry.

## LLM Documentation Export

When using `sphinx-llm`, include a CI check that the generated Markdown context exists. If the project publishes GitLab Pages, expose both the HTML documentation and the full Markdown context, for example:

```bash
sphinx-build -W --keep-going -b html doc/source public
test -s public/llms-full.txt
cp public/llms-full.txt public/my-library-full.md
```

A project-specific Codex skill can then refer to the generated Markdown and to these documentation rules.

## Agent Checklist

When adding documentation for a Fortran module:

1. Identify the public compiler API from `public`/`private` declarations.
2. Move API descriptions immediately after the relevant declaration line in the Fortran source; merge any important pre-declaration prose into that rendered comment block.
3. Add or extend executable example tests for public helpers/interfaces.
4. Mark example regions with `doc-example-start:` and `doc-example-end:` comments.
5. Add `f:autogroup` blocks for parameter/object families that need shared prose.
6. Add `fortranliteral` directives next to the public API source comments.
7. Wire the example program into CI.
8. Add rendered-document checks for symbols, topics, private leaks, groups, and examples.
9. Render locally and run the checker before handing off.

## Safety and Boundaries

- Do not document private implementation routines as public API unless the user asks for internal documentation.
- Do not duplicate large examples in `.rst`; include them from test sources with `fortranliteral`.
- Do not weaken Sphinx warnings or coverage checks to make CI pass.
- Preserve existing project licensing and comment style.
- If parser behavior is uncertain, add a small contract fixture before changing large production docs.
