---
name: bigdft-installation
description: Use this skill when the user wants to compile or install BigDFT from source, choose compilers and libraries, create an rcfile, or diagnose build-environment choices. Do not use it for BigDFT input generation, scientific workflow design, or source-code maintenance unrelated to installation.
license: GPL-3.0-or-later
---

<!--
SPDX-License-Identifier: GPL-3.0-or-later

Portions adapted from william-dawson/bigdft-skills at commit 3ee7e78b2443da258e37c8e7b18b79c4b1af9b4a.
Source file: skills/install/SKILL.md
Upstream plugin metadata declares license: MIT.
Adapted for the BigDFT-group/skills portable skill layout and relicensed here
under GPL-3.0-or-later with attribution preserved in NOTICE.md.
-->

# Skill: Bigdft Installation

Help the user build BigDFT from source using the `Installer.py` wrapper around jhbuild. **Ask each question one at a time.** Auto-detect what you can by running shell commands before asking the user.

## Pre-flight: Gather System Information

Before asking any questions, silently run these commands and record the results:

```bash
ls ./Installer.py ../Installer.py ../bigdft-suite/Installer.py ./bigdft-suite/Installer.py ~/bigdft-suite/Installer.py 2>/dev/null  # find source
pwd                  # current directory
uname -s -m          # OS and architecture
hostname             # for matching existing rcfiles
whoami               # if root, every Installer.py call must go through runuser (see below)
which mpifort mpif90 mpicc gfortran gcc ifort ifx icx 2>/dev/null
mpifort --version 2>/dev/null || mpif90 --version 2>/dev/null
gfortran --version 2>/dev/null
gcc --version 2>/dev/null
ifort --version 2>/dev/null || ifx --version 2>/dev/null
python3 --version 2>/dev/null
pkg-config --libs lapack blas 2>/dev/null
echo $MKLROOT
ls /opt/homebrew/opt/openblas 2>/dev/null   # macOS Homebrew
ls /usr/lib/x86_64-linux-gnu/liblapack* 2>/dev/null  # Debian/Ubuntu
```

Fill in this checklist (do not show it to the user):

```
Platform:        ___  (linux-x86_64 / linux-aarch64 / darwin-arm64 / darwin-x86_64)
Hostname:        ___
Fortran MPI:     ___  (mpifort / mpif90 / mpiifort / ftn / none)
Fortran serial:  ___  (gfortran / ifort / ifx / frt / none)
C compiler:      ___  (gcc / icc / icx / clang / fcc / none)
C++ compiler:    ___  (g++ / icpc / icpx / clang++ / FCC / none)
GCC version:     ___  (needed to decide -fallow-argument-mismatch)
BLAS/LAPACK:     ___  (mkl / openblas / accelerate / system / none)
MKLROOT:         ___  (path or empty)
Python 3:        ___  (version or none)
CUDA available:  ___  (yes / no; check nvcc or nvidia-smi)
OpenCL avail:    ___  (yes / no)
```

**Build user — decide this BEFORE running any `Installer.py`/jhbuild command.** jhbuild refuses
to run as root and then silently returns an empty module list (`List of modules to be treated:
['']`) that looks like a broken rcfile — do not chase it. If `whoami` is `root` (e.g. a
container), run **every** `Installer.py` call (autogen, build, clean, …) through
`runuser -u "$owner" --` from the start:
- existing/partial build → `owner=$(stat -c %U <build-dir>)` — it already has access;
- fresh build → create a user and build under a path it owns and can traverse, e.g. its own home
  (`useradd -m builder`). Never `chown` someone else's `0700` home.

Pick the build path once and never move it afterward — jhbuild bakes absolute paths into
`install/bin/*vars.sh`.

## Prerequisites: install missing system packages

BigDFT needs a full build toolchain plus a few libraries. Using the pre-flight results,
install **only what is missing** (do not reinstall what is already present). On Debian/Ubuntu:

```bash
pkgs="gfortran cmake pkg-config autoconf automake libtool libtool-bin \
  libopenmpi-dev openmpi-bin libopenblas-dev liblapack-dev \
  python3-dev libyaml-dev python3-yaml"
missing=""
for p in $pkgs; do dpkg -s "$p" >/dev/null 2>&1 || missing="$missing $p"; done
if [ -n "$missing" ]; then
  apt-get update && apt-get install -y $missing
else
  echo "All build dependencies already present — nothing to install."
fi
```

- `gfortran`, an MPI implementation (e.g. OpenMPI) and BLAS/LAPACK are **mandatory**.
- `libyaml-dev` is required by the **futile** module (configure fails with `yaml.h: No such file`).
- `cmake` is required by the **CheSS** module (the other modules use autotools).
- Without root access, ask the user to provide these via the system's module manager instead.

## Questions

### 1 -- Source location

Before asking, check whether the current working directory (or a nearby directory) already contains `Installer.py`. Also check common locations like `../bigdft-suite`, `./bigdft-suite`, and `$HOME/bigdft-suite`. If you find it, confirm with the user rather than asking from scratch:

```
I see bigdft-suite at <path>. Is that the one you want to build?
```

Only if nothing is found, offer to clone the official repository:

```
I couldn't find bigdft-suite nearby. I can clone it for you:

  git clone https://gitlab.com/l_sim/bigdft-suite.git

Where should I clone it?  (Default: ./bigdft-suite)
Or provide an existing path if you already have a copy elsewhere.
```

After cloning, verify the path contains `Installer.py`. Because the clone produces a git checkout, `Installer.py autogen -y` must be run before the first build.

### 2 -- Build directory

**First locate an existing build — do not guess its path.** A previous/partial install leaves a
build directory holding `custom.rc` and `install/_jhbuild/`. Search for it before assuming
anything (run, don't ask; the build dir name is arbitrary — `build`, `bigdft-build`, …):

```bash
find "$(dirname <source-dir>)" -maxdepth 2 -name custom.rc 2>/dev/null
```

If a match is found, its directory **is** the build dir to reuse — resume it (see below). Only if
nothing is found, create a new one:

```
Where should I create the build directory?
Default: a "build" directory beside the source.
```

The build directory **must** be a **sibling** of the source, never inside it — e.g. `/p/build`
next to `/p/bigdft-suite`, **not** `<source-dir>/build`. Create it if it doesn't exist.

**If a build directory already exists (any level of previous/partial install):** do not trust
the build log, and do not wipe it. The build is incremental — re-run
`Installer.py build -f <build-dir>/custom.rc -y` to finish only what is missing (works at any
level: empty, half, almost done). Then confirm success on the **real artifact**, not on a
"completed" message: `source <build-dir>/install/bin/bigdftvars.sh && bigdft --help`. If
`bigdft` is missing, it is not done. If the build is broken, use `clean` (then rebuild), or
`startover` (git checkout) for a full reset.

### 3 -- Compilers and MPI

If auto-detection found compilers, confirm with the user:

```
I detected:
  Fortran MPI compiler: <detected>
  C compiler: <detected>
  C++ compiler: <detected>

Are these correct, or would you like to use different compilers?
```

If nothing was detected, ask explicitly:

```
Which compilers should I use?
  - Fortran MPI compiler (e.g. mpifort, mpiifort, ftn)
  - C compiler (e.g. gcc, icc, icx, clang)
  - C++ compiler (e.g. g++, icpc, icpx, clang++)
```

### 4 -- BLAS/LAPACK

If auto-detection found a library, confirm. Otherwise ask:

```
Which BLAS/LAPACK implementation should I link against?
  1. Intel MKL (set MKLROOT if not already)
  2. OpenBLAS (-lopenblas)
  3. Apple Accelerate (-framework Accelerate)  [macOS only]
  4. System LAPACK (-llapack -lblas)
  5. Custom (provide linker flags)
```

### 5 -- Anything beyond the default?

By default, build `bigdft` with standard optimization (`-O2`). Do **not** ask about modules, optimization flags, or optional features unless the user brings them up. Instead, ask a single open-ended question:

```
I'll build bigdft with -O2 optimization. Any custom requirements?
(e.g. also build spred, enable GPU support, debug flags, etc.)
```

If they say no, proceed with defaults. If they mention specifics, handle accordingly:

- **Modules**: default is `['bigdft']`. Other options: `['spred']` (full suite), `['chess']` (CheSS only), or any subset of: futile, atlab, chess, liborbs, psolver, bigdft, spred, PyBigDFT, bigdft-client.
- **GPU**: add CUDA (`--enable-cuda-gpu`) and/or OpenCL (`--enable-opencl`) flags. Only mention if hardware was detected in pre-flight.
- **Optimization**: `-O2` is default. `-O3` for aggressive, `-O0 -g -fbounds-check -fbacktrace` for debug.
- **Optional features**: Python bindings (`conditions.add("python")`), testing (`conditions.add("testing")`), dynamic libraries (`--enable-dynamic-libraries`).

For GCC >= 10, always add `-fallow-argument-mismatch` to FCFLAGS regardless of what the user asks for.

## rcfile Generation

After collecting answers, generate a configuration file. Write it to `<build-dir>/custom.rc`.

### rcfile Template

```python
# BigDFT configuration file
# Generated for: FILL (hostname / platform)
# Date: FILL

import os

# Modules to build
modules = FILL  # e.g. ['bigdft'] or ['spred']
moduleset = 'suite'

# Skip system-provided packages
skip = FILL  # e.g. ["PyYAML", "libyaml"]

# Conditions -- leave ALL commented out unless the user explicitly requests them
# conditions.add("testing")     # only if user wants to run tests
# conditions.add("python")      # only if user explicitly asks for Python/PyGObject bindings
# conditions.add("no_upstream") # only if user wants to skip upstream dependencies

def env_configuration():
    '''Configure compilers and flags for autotools packages.'''
    conf = {}
    conf["FC"] = "FILL"        # e.g. "mpifort"
    conf["CC"] = "FILL"        # e.g. "gcc"
    conf["CXX"] = "FILL"       # e.g. "g++"
    conf["FCFLAGS"] = "FILL"   # e.g. "-O2 -fopenmp"
    conf["CFLAGS"] = "FILL"    # e.g. "-O2"
    conf["CXXFLAGS"] = "FILL"  # e.g. "-O2 -std=c++11"
    # FILL: BLAS/LAPACK linking
    conf["--with-ext-linalg"] = "FILL"
    return " ".join(['"' + k + '=' + v + '"' for k, v in conf.items()])

autogenargs = env_configuration()

# Module-specific overrides
module_autogenargs = {}
module_cmakeargs = {}
module_makeargs = {}

# FILL: Add module-specific settings if needed
# Example: module_autogenargs['bigdft'] = env_configuration() + ' --with-gobject=yes'
# Example: module_cmakeargs['ntpoly'] = '-DCMAKE_Fortran_COMPILER=FILL ...'
```

### BLAS/LAPACK Reference Configurations

Use the appropriate linking line based on the user's choice:

**Intel MKL (GNU compilers):**
```python
mkl = os.environ["MKLROOT"] + "/lib/intel64"
conf["FCFLAGS"] = "-I" + os.environ["MKLROOT"] + "/include -O2 -fopenmp"
conf["--with-ext-linalg"] = (
    "-L" + mkl + " -Wl,--start-group "
    "-lmkl_gf_lp64 -lmkl_gnu_thread -lmkl_core "
    "-Wl,--end-group -lgomp -lpthread -lm -ldl"
)
```

**Intel MKL (Intel compilers):**
```python
mkl = os.environ["MKLROOT"] + "/lib/intel64"
conf["FCFLAGS"] = "-I" + os.environ["MKLROOT"] + "/include -O2 -qopenmp"
conf["--with-ext-linalg"] = (
    "-L" + mkl + " "
    "-lmkl_intel_lp64 -lmkl_intel_thread -lmkl_core "
    "-liomp5 -lpthread -lm -ldl"
)
```

**Intel MKL with ScaLAPACK (Intel compilers + Intel MPI):**
```python
mkl = os.environ["MKLROOT"] + "/lib/intel64"
conf["--with-ext-linalg"] = (
    "-L" + mkl + " "
    "-lmkl_scalapack_lp64 -lmkl_intel_lp64 -lmkl_intel_thread -lmkl_core "
    "-lmkl_blacs_intelmpi_lp64 -liomp5 -lpthread -lm -ldl"
)
```

**OpenBLAS:**
```python
conf["--with-ext-linalg"] = "-lopenblas"
# or with explicit path:
conf["--with-ext-linalg"] = "-L/path/to/openblas/lib -lopenblas"
```

**Apple Accelerate (macOS):**
```python
conf["--with-ext-linalg"] = "-framework Accelerate"
```

**System LAPACK/BLAS:**
```python
conf["--with-ext-linalg"] = "-llapack -lblas"
```

### Compiler Flag Reference

**GCC (gfortran):**
```
FCFLAGS: -O2 -fopenmp -fPIC
         -fallow-argument-mismatch  (GCC >= 10, required)
CFLAGS:  -O2 -fPIC
LIBS:    -lstdc++  (sometimes needed)
```

**Intel classic (ifort/icc):**
```
FCFLAGS: -O2 -qopenmp -fPIC
CFLAGS:  -O2 -fPIC
```

**Intel oneAPI (ifx/icx):**
```
FCFLAGS: -O2 -qopenmp -fPIC
CFLAGS:  -O2 -fPIC
CXXFLAGS: -O2 -std=c++11
```

**Cray wrappers (ftn/cc):**
```
FC=ftn  (no explicit MPI flags needed)
BLAS/LAPACK: --with-blas=no --with-lapack=no  (Cray libsci is automatic)
```

**Fujitsu (frt/fcc on Fugaku):**
```
FC=mpifrt or mpifrtpx (cross-compile)
FCFLAGS: -SSL2BLAMP -Kfast,openmp,noautoobjstack
LIBS: -SSL2BLAMP -Kfast,openmp -Nlibomp --linkstl=libfjc++
--with-ext-linalg: -fjlapackex
```

**macOS with Clang + gfortran:**
```
FC=mpifort  CC=clang  CXX=clang++
FCFLAGS: -O2 -fopenmp -mtune=native
CFLAGS: -O2 -std=c99 -Wno-error=implicit-function-declaration
LIBS: -lc++
```

### GPU Configuration

**CUDA:**
```python
# Add to autogenargs:
conf["--enable-cuda-gpu"] = ""
conf["--with-cuda-path"] = "/usr/local/cuda"  # or $CUDA_HOME
conf["NVCC_FLAGS"] = "--compiler-options -fPIC"
# For specific architecture:
conf["NVCC_FLAGS"] = "-arch sm_80 -O3 --compiler-options -fPIC"
```

**OpenCL:**
```python
conf["--enable-opencl"] = ""
conf["--with-ocl-path"] = "/usr/local/cuda"  # NVIDIA OpenCL
# or for Intel:
conf["--with-ocl-path"] = "/opt/intel/oneapi/..."
```

**SYCL (Intel oneAPI):**
```python
conf["FCFLAGS"] += " -fsycl -fsycl-device-code-split=per_kernel"
conf["CXXFLAGS"] = "-O2 -fsycl -fsycl-device-code-split=per_kernel -fPIC"
# Add to linalg: -lmkl_sycl
```

### NTPoly Configuration

NTPoly uses CMake and often needs special handling:

```python
module_cmakeargs['ntpoly'] = (
    "-DCMAKE_Fortran_COMPILER=FILL "      # e.g. mpifort
    "-DCMAKE_C_COMPILER=FILL "            # e.g. gcc
    "-DCMAKE_CXX_COMPILER=FILL "          # e.g. g++
    "-DCMAKE_Fortran_FLAGS_RELEASE='-O2 -fopenmp -fPIC' "
    "-DBUILD_SHARED_LIBS=ON "
    "-DFORTRAN_ONLY=NO"
)
```

For Fujitsu compilers, add: `-DCMAKE_Fortran_MODDIR_FLAG=-M`

### Packages to Skip

Common packages to skip when already system-installed:

```python
# Conda environment
skip = ["spglib", "PyYAML", "libyaml", "ntpoly", "libxc"]

# HPC with module system (common)
skip = ["PyYAML", "libyaml"]

# Minimal build
skip = ["ntpoly"]
```

## Build Execution

> **Build as the user decided in pre-flight.** If root, prefix EVERY `Installer.py` call
> (autogen included) with `runuser -u "$owner" --` — use `runuser`, not `su -` (which can fail
> with "Authentication failure" in containers):
>
> ```bash
> runuser -u "$owner" -- bash -lc "cd <build-dir> && <source-dir>/Installer.py build -f <build-dir>/custom.rc -y"
> ```

After writing the rcfile, determine whether the source is a git checkout or a tarball. If the source directory contains a `.git` directory (or the individual packages like `futile/`, `bigdft/` contain `autogen.sh` but no `configure`), it is a developer build from git and needs autogen first.

**For git checkouts (developer builds):**
```bash
cd FILL  # build directory
FILL/Installer.py autogen -y
FILL/Installer.py build -f FILL/custom.rc -y
```

**For tarballs:**
```bash
cd FILL  # build directory
FILL/Installer.py build -f FILL/custom.rc -y
```

The `-y` flag auto-answers yes to prompts.

Tell the user:
- The build log is in `<build-dir>/_jhbuild/logs/` if something fails
- Build parallelism is auto-detected (CPU count + 1)
- After a successful build, source the environment: `source <build-dir>/install/bin/bigdftvars.sh`

## Troubleshooting

If the build fails, check the error and suggest fixes:

| Error | Likely cause | Fix |
|-------|-------------|-----|
| `Type mismatch` in Fortran | GCC >= 10 strictness | Add `-fallow-argument-mismatch` to FCFLAGS |
| `cannot find -llapack` | Missing LAPACK | Install or fix `--with-ext-linalg` path |
| `No rule to make target` | Stale build | Run `Installer.py clean` then rebuild |
| `libyaml.so not found` at runtime | Missing LD_LIBRARY_PATH | `export LD_LIBRARY_PATH=<build>/install/lib:$LD_LIBRARY_PATH` |
| `MPI_Init` errors | Wrong compiler wrapper | Ensure FC is an MPI wrapper (mpifort, not gfortran) |
| `configure: error: cannot run test program` | Cross-compilation mismatch | Add `--build=` and `--host=` flags |
| Build in source dir error | Must use separate build dir | Create and cd to a separate build directory |
| `autogen.sh: not found` | Developer build needs autogen | Run `Installer.py autogen` first |

## Installer.py Action Reference

After the initial build, the user may need these:

| Command | Purpose |
|---------|---------|
| `Installer.py build -f custom.rc` | Full build with dependencies |
| `Installer.py make` | Recompile without reconfigure (fast) |
| `Installer.py clean` | Clean all build artifacts |
| `Installer.py buildone <module>` | Build a single module |
| `Installer.py cleanone <module>` | Clean a single module |
| `Installer.py check` | Run test suite |
| `Installer.py autogen` | Regenerate configure scripts (developers) |
| `Installer.py dry_run` | Show build order (generates buildprocedure.png) |
| `Installer.py link` | Show linker flags for external codes |

Available modules: `futile`, `atlab`, `chess`, `liborbs`, `psolver`, `bigdft`, `PyBigDFT`, `spred`, `bigdft-client`.

## Existing rcfile Reference

If the user is on a known HPC system, suggest using an existing rcfile from the source tree instead of generating one. Known systems:

| System | rcfile | Compilers | Notes |
|--------|--------|-----------|-------|
| **macOS (Clang)** | `rcfiles/macos_clang.rc` | clang + gfortran | Accelerate framework |
| **macOS (GCC/Homebrew)** | `rcfiles/macos_gcc.rc` | Homebrew gcc + gfortran | Auto-detects GCC version |
| **Ubuntu/Debian** | `rcfiles/ubuntu_MPI.rc` | gcc + mpifort | OpenBLAS, debug flags |
| **Ubuntu OpenCL** | `rcfiles/ubuntu_OCL.rc` | gcc + mpif90 | OpenCL + OpenMP |
| **Ubuntu OpenMP only** | `rcfiles/ubuntu_OMP.rc` | gfortran (no MPI) | Minimal, serial+OpenMP |
| **Conda** | `rcfiles/conda.rc` | conda compilers | Skips conda packages |
| **Container** | `rcfiles/container.rc` | gcc + mpif90 | CUDA + OpenCL |
| **Container + MKL** | `rcfiles/container_mkl.rc` | gcc + mpif90 | MKL + CUDA |
| **ARCHER2** | `rcfiles/archer2.rc` | Cray ftn (GNU) | MKL, Cray wrappers |
| **Fugaku (native)** | `rcfiles/fugaku_node.rc` | Fujitsu frt | ARM A64FX |
| **Fugaku (cross)** | `rcfiles/fugaku_cross.rc` | Fujitsu frtpx | Cross-compile for A64FX |
| **IRENE (GNU)** | `rcfiles/irene-gnu.rc` | gcc + mpif90 | CEA, MKL |
| **IRENE (Intel)** | `rcfiles/irene.rc` | Intel + mpif90 | CEA, MKL + ScaLAPACK |
| **Leonardo** | `rcfiles/leonardo.rc` | gcc + mpif90 | A100 GPUs, CUDA + OpenCL |
| **Hokusai** | `rcfiles/hokusai.rc` | Intel + mpiifort | RIKEN, MKL |
| **Topaze** | `rcfiles/topaze.rc` | Intel + mpif90 | CUDA + OpenCL, bio support |
| **Vega (FOSS)** | `rcfiles/vega-foss-cuda.rc` | gcc + mpif90 | MKL + CUDA |
| **Vega (Intel)** | `rcfiles/vega-intel.rc` | Intel + mpif90 | MKL |
| **Adastra** | `rcfiles/adastra.rc` | Intel oneAPI (ifx) | AMD GPU, SYCL |
| **Manneback** | `rcfiles/mann_gnu.rc` | gcc (EasyBuild) | UCLouvain, MKL |

If a match is found, suggest:
```bash
cd <build-dir>
<src-dir>/Installer.py build -f <src-dir>/rcfiles/<match>.rc
```

## Notes

- Never build inside the source directory. Always create a separate build directory.
- The `buildrc` file is auto-generated in the build directory after the first build and can be reused for subsequent builds.
- After a successful build, a `Makefile` is generated in the build directory with convenience targets (`make build`, `make clean`, `make check`).
- For developer builds (from git, not tarball), run `Installer.py autogen` before the first build.
- `source install/bin/bigdftvars.sh` sets up PATH, LD_LIBRARY_PATH, PYTHONPATH, and PKG_CONFIG_PATH.
- The build system auto-detects CPU count and uses `jobs = cpu_count + 1` for parallel make.
- Conditions control optional features: `testing`, `python`, `no_upstream`, `bio`, `ase`, `vdw`, `sirius`, `sycl`, `dill`, `boost`, `spg`, `amber`, `devdoc`, `simulation`.
