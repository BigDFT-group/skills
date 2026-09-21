---
name: psolver-ci-debugging
description: Use this skill when the user wants to understand or fix PSolver build failures, test failures, compiler issues, or CI pipeline problems. Do not use it for general API usage, broad refactoring, or feature design.
license: GPL-3.0-or-later
---

<!--
SPDX-License-Identifier: GPL-3.0-or-later
-->

# Skill: PSolver CI Debugging

## Purpose

This role-specific skill guides an AI agent when working with **PSolver** in the context of **CI debugging**.

## Scope

This skill is for:

- understand or fix PSolver build failures, test failures, compiler issues, or CI pipeline problems;
- answering questions within the declared role;
- using real project conventions where known;
- avoiding behavior that belongs to a different skill.

This skill is not for:

- general API usage, broad refactoring, or feature design.

## Minimal Project Context

PSolver is an Autotools Fortran library in `psolver/`. Its optional Kokkos
backend is a nested CMake project in `psolver/kokkos/`, built as the
`psolverkokkos` moduleset module before PSolver. The backend can contain both
host and device specializations in one `libpsolverkokkos`; `KOKKOSCPU` and
`KOKKOSGPU` select them at runtime.

## Agent Responsibilities

- Reproduce failures with the exact image, rcfile, conditions, and module target.
- Separate configure, compile, install, link, and execution failures.
- Distinguish the standalone Kokkos CTest suite from full Fortran PSolver regressions.
- Inspect generated configuration and installed artifacts instead of assuming a successful build installed optional test files.
- Preserve public ABI and licensing metadata while fixing CI-specific problems.
- Route broad backend redesign to `psolver-maintainer` and public API questions to `psolver-api-user`.

## Common Tasks

- reproduce the Kokkos CI build with the exact SDK image and rcfile;
- diagnose missing test fixtures caused by optional Python dependencies;
- diagnose static-library compiler-runtime leakage into downstream modules;
- verify CPU/GPU execution-space selection and CUDA driver visibility;
- inspect GitLab pipeline/job traces with `glab api`.

## Suite-First Publication

For a PSolver source or CI correction in a BigDFT-suite checkout, use
`bigdft-suite-integration-maintainer`: push the suite `devel` change first and
let its `check_library` job publish PSolver upstream. Do not leave a fix only
in the standalone PSolver repository.

## Essential Workflows

### Reproduce the Kokkos CI contract

Follow `.gitlab-ci.yml` rather than inventing a parallel build. The Kokkos job
must cover both layers:

```sh
python3 ./Installer.py -y autogen psolver
mkdir -p tmp-kokkos
cd tmp-kokkos
python3 ../Installer.py -a no_upstream -f ../rcfiles/kokkos-ci.rc -y build psolver
source install/bin/bigdftvars.sh
pkg-config --modversion psolverkokkos
ctest --test-dir psolver-kokkos --output-on-failure
OMP_PROC_BIND=false make -C psolver/tests check-kokkos-cpu
```

`ctest` checks the public C++ ABI. `check-kokkos-cpu` crosses the full
Fortran/C dispatcher and runs `PS_Basics_ortho` for all four boundary
conditions. A passing CTest alone does not establish that the installed
Futile regression driver or Fortran integration works.

On a GPU-capable local SDK, run:

```sh
make -C tmp/psolver/tests check-kokkos-gpu
```

Do not run that target on a CPU-only CI runner. Confirm the image was started
with GPU access and that `nvidia-smi -L` works first.

### Regenerate Autotools from a writable source mount

Changes to `psolver/tests/Makefile.am` require `autoreconf -fi` or the
Installer's `autogen` action. A read-only source bind mount fails while
Automake updates `Makefile.in` or `autom4te.cache`. Use a disposable container
with the source mounted read-write and run it as the host UID/GID; keep build
outputs in a separate writable directory. Do not solve this by changing source
ownership from a root container.

Generated backend macros originate in the suite-level `m4/` directory.
Update the canonical macro there, then run `Installer.py autogen`; do not patch
only component copies under `*/config/m4/`.

### Futile test-driver availability

PSolver's Automake regression uses the path recorded as
`FUTILE_PYTHONDIR` in `futile.pc` and expects `f_regtest.py`,
`fldiff_yaml.py`, and `report.py`. Futile adds `tests/` to its install graph
only when its configure-time PyYAML probe succeeds. Therefore a successful
Futile build may still omit all regression scripts.

Check both facts:

```sh
pkg-config --variable=futile_pythondir futile
python3 -c 'import yaml; print(yaml.__file__)'
```

When using `-a no_upstream`, source the upstream environment before configure.
Also verify its Python path matches the actual installation scheme:
`lib/pythonX.Y/site-packages` and `local/lib/pythonX.Y/dist-packages` are not
interchangeable. A module with `yaml.__file__ == None` may be an unrelated
namespace package, not PyYAML. Pure-Python PyYAML without `CLoader` is accepted
by Futile and still enables test-script installation.

### CUDA driver stubs are link-time only

CUDA driver stubs may be used through `-L` or `-Wl,-rpath-link` during the
build, but their directory must not precede the real driver in
`LD_LIBRARY_PATH`. A runtime failure containing `cudaErrorStubLibrary` means
the stub `libcuda` was loaded. Remove only the stub-directory component after
sourcing generated environment files; preserve the rest of the SDK paths.

### Static FFTW and compiler runtimes

The Kokkos host specialization links FFTW and its threaded library. If static
FFTW was compiled with IntelLLVM but `libpsolverkokkos` is linked by
`nvcc_wrapper` with a GNU host compiler, downstream links can fail in an
apparently unrelated module such as liborbs with `__kmpc_*`,
`_intel_fast_memcpy`, or `__svml_*` undefined references.

Use `nm -u` on `libfftw3.a` and `libfftw3_omp.a`, then `readelf -d` on
`libpsolverkokkos.so`, to identify the producer and missing `DT_NEEDED`
entries. The durable oneAPI CUDA image rule is to build FFTW with `CC=gcc`,
matching `NVCC_WRAPPER_DEFAULT_COMPILER=/usr/bin/g++`. An rcfile may temporarily
link Intel runtimes (`svml`, `irng`, `imf`, `irc`, `iomp5`, `irc_s`) for an
older image. Keep that workaround scoped to the oneAPI rcfile and remove it
after rebuilding the image.

### Diagnose execution-space selection

Check the requested input and reported enumerator together:

```yaml
setup:
  accel: KOKKOSCPU
```

```yaml
setup:
  accel: KOKKOSGPU
```

If `KOKKOSCPU` initializes or launches CUDA, audit every Kokkos launch for an
implicit default policy. Typed backend kernels must use policies such as
`Kokkos::RangePolicy<ExecSpace>` rather than count-only `parallel_for` or
`parallel_reduce` overloads.

### Inspect current GitLab state

Resolve pipeline and job IDs before reading a trace:

```sh
glab api 'projects/luigigenovese%2Fbigdft-suite/pipelines?ref=kokkos&per_page=3'
glab api 'projects/luigigenovese%2Fbigdft-suite/pipelines/PIPELINE_ID/jobs?per_page=100'
glab api 'projects/luigigenovese%2Fbigdft-suite/jobs/JOB_ID/trace'
```

Compare the exact failing command with the previous successful job. A newly
added test can expose a dependency omission that was already present; a green
preceding build does not prove the unexecuted dependency was installed.

## Safety and Boundaries

- Do not run GPU tests on an unverified runner or treat absence of a GPU as a code regression.
- Do not put CUDA stub directories on the runtime library path.
- Do not hard-code compiler runtime libraries in portable PSolver code; confine temporary compatibility flags to the matching rcfile.
- Do not modify source ownership to work around a read-only container mount.
- Do not assume optional files from examples or test directories are installed.

## Licensing Notes

This skill file is licensed under GPL-3.0-or-later unless otherwise stated.
Any adapted snippets must be GPL-3.0-or-later compatible and attributed in
`NOTICE.md` when required.

## References

- `.gitlab-ci.yml`: authoritative job commands and image tags
- `rcfiles/kokkos-ci.rc`: CPU Kokkos CI configuration
- `rcfiles/oneapi-cuda-hpc.rc`: current oneAPI/CUDA build configuration
- `rcfiles/oneapi-cuda-hpc-upstream.rc`: upstream SDK dependency build rules
- `psolver/kokkos/README.md`: supported execution spaces and build contract
- `psolver/tests/Makefile.am`: full backend regression targets
