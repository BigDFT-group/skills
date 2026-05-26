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
| `bigdft-atlab-maintainer` | BigDFT/ATlab | Source maintenance | The user wants to maintain or debug BigDFT ATlab code involving simulation domains, grid cells, box iterators, multipoles, spherical harmonics, numerical utilities, or field I/O. |
| `bigdft-input-preparation` | BigDFT | Input preparation | The user wants to prepare BigDFT input files in YAML or Python, choose calculation settings, define systems, or configure DFT parameters. |
| `bigdft-input-variable-maintainer` | BigDFT/CheSS/PSolver | Input-variable maintenance | The user wants to add, modify, review, or debug input-variable definitions in BigDFT, CheSS, or PSolver, from YAML schema through generated strings, Fortran dictionaries, derived types, and runtime access. |
| `bigdft-installation` | BigDFT | Installation | The user wants to compile or install BigDFT from source, choose compilers and libraries, create an rcfile, or diagnose build-environment choices. |
| `bigdft-liborbs-maintainer` | BigDFT/liborbs | Source maintenance | The user wants to maintain or debug BigDFT liborbs code involving orbitals, localization regions, wavelet compression, operator application, views, MPI distribution, or GPU paths. |
| `bigdft-linear-scaling` | BigDFT | Linear-scaling workflows | The user wants to configure, explain, or extend BigDFT linear-scaling calculations, including lin_basis_params, ig_occupation, support functions, rloc, nbasis, and pseudopotential electron counts. |
| `bigdft-logfile-analysis` | BigDFT | Logfile analysis | The user wants to parse, inspect, compare, or analyze BigDFT logfile output, including energies, forces, eigenvalues, convergence data, and calculation metadata. |
| `bigdft-projectors-maintainer` | BigDFT | Projector maintenance | The user wants to implement, debug, or review BigDFT nonlocal pseudopotential projector code, including Kleinman-Bylander projectors, HGH/HGH-K radial functions, psppar layout, h_ij coupling matrices, and nonlocal matrix elements. |
| `bigdft-pseudopotentials` | BigDFT | Pseudopotential setup | The user wants to select, configure, or troubleshoot pseudopotentials for BigDFT calculations, including PSP formats, PyBigDFT pseudopotential APIs, command-line PSP files, and electron-count implications. |
| `bigdft-systems-api-user` | BigDFT/PyBigDFT | Systems API usage | The user wants to build, manipulate, read, write, or analyze atomic structures with PyBigDFT Atom, Fragment, and System classes. |
| `bigdft-workflows` | BigDFT | Workflow routing | The user wants to plan a BigDFT task at the workflow level, choose the right operational path, combine input preparation with execution and analysis, or decide which more specific BigDFT skill should be used. |
| `futile-api-user` | Futile | API usage | The user wants to call the Futile API, understand public interfaces, or integrate Futile utilities as a library. |
| `futile-maintainer` | Futile | Source maintenance | The user wants to write, modify, debug, or review BigDFT/Futile Fortran code using dictionaries, memory tracking, YAML I/O, error handling, timing, or MPI wrappers. |
| `psolver-api-user` | PSolver | API usage | The user wants to call the PSolver API, understand public interfaces, prepare input data, or integrate PSolver as a library. |
| `psolver-ci-debugging` | PSolver | CI debugging | The user wants to understand or fix PSolver build failures, test failures, compiler issues, or CI pipeline problems. |
| `psolver-maintainer` | PSolver | Source maintenance | The user wants to maintain, debug, or understand PSolver internals for electrostatics, Hartree potentials, FFT-based kernels, boundary conditions, implicit solvation, or GPU acceleration. |
| `remotemanager-hpc-workflows` | RemoteManager | HPC workflows | The user wants to configure RemoteManager connections, define remote HPC execution workflows, run Dataset computations, retrieve results, or debug remote workflow failures. |
| `wise-container-maintainer` | WISE | Container maintenance | The user wants to maintain WISE container images, IDE integration, agent setup, display forwarding, or reproducible development environments. |

## Adding a Skill

1. Create `skills/<project>-<role>/SKILL.md`.
2. Use the template from `templates/skill/SKILL.md`.
3. Make the skill self-contained.
4. Add the skill to this index.
5. Update `NOTICE.md` if snippets are adapted from upstream projects.
