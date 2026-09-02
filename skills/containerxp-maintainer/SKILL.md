---
name: containerxp-maintainer
description: "Use this skill when maintaining ContainerXP's BigDFT ground, SDK, runtime, CI-SDK, release-catalog, and trace-guided stripping workflows, including the rcfiles associated with each image flavor. Use for ContainerXP image build, validation, pruning, and publication work; not for general Docker questions or unrelated BigDFT source development."
license: GPL-3.0-or-later
---
<!--
SPDX-License-Identifier: GPL-3.0-or-later
-->


# ContainerXP Maintainer

ContainerXP is the image-construction layer for BigDFT Suite development, testing, and runtime environments. Its central contract is that a container codename selects both an upstream-build rcfile and a BigDFT Suite-build rcfile. Maintain the image and rcfile as one unit.

Read [architecture.txt](references/architecture.txt) before changing an image recipe, adding a flavor, or deciding what may be stripped. Read `Dockerfiles/container-catalog.yaml` before working on a catalogued image. Read [catalog-schema.txt](references/catalog-schema.txt) when creating or updating catalog entries.

## Invariants

- Keep ground, full SDK, compact CI-SDK, and runtime concerns separate. Ground images provide the platform toolchain and provider environment; the SDK selects upstream packages and conditions; runtime consumes an SDK via `FROM`.
- `CODENAME=<name>` must resolve to both `<name>-upstream.rc` and `<name>.rc`. Verify both files in the exact BigDFT Suite source branch that the image will use. Do not silently combine an rcfile from one branch with sources from another.
- The parameterized SDK Dockerfile must remain profile-free. Select core, client, suite, and optional capabilities through explicit build arguments: packages, conditions, APT/Python prerequisites, source reference, and codename. Check the moduleset rather than assuming package names.
- A CI-SDK is a deliberately curated payload, rebuilt on an ABI-compatible ground image. It is not a new upstream build flavor and it must retain the source tree, rcfiles, installed upstream prefix, compiler wrappers, and any explicitly validated build inputs.
- Cache upstream source archives in the project tarball/LFS repository during image construction. Final CI jobs must not need network access to fetch their sources.
- Never change generic or mutable tags such as `latest` as part of a flavor release. Publish a new immutable/revision tag and record its registry digest only after the push succeeds.
- Preserve existing worktree changes. Do not broadly commit, retag, delete images, or publish anything without the user's explicit authorization.

## Workflow

1. Inspect the actual Dockerfiles, source branch, modulesets, and paired rcfiles. Treat `Dockerfiles/release-matrix.yaml` as legacy/planning input; reconcile it with actual recipes rather than assuming it is current.
2. Build the dedicated ground flavor. Keep architecture, operating-system, oneAPI, CUDA, and provider-specific environment choices explicit there.
3. Build the full SDK from that ground image. Pass selected root packages and conditions explicitly. Confirm that `/opt/upstream/bin/bigdftvars.sh` exposes the resulting prefix and helper entrypoints source it.
4. Validate the full SDK's package-specific contracts. For Kokkos this includes installed CMake packages and an external consumer; for a Suite SDK, perform a clean Suite build with its paired rcfile.
5. Derive a compact CI-SDK only after the full image works. Start from compatible ground, copy the justified payload, and test a clean Suite rebuild. Use file tracing only as evidence; distinguish true file opens from shell/environment directory probes.
6. Build a generic runtime layer from the selected SDK/CI-SDK and run intended smoke or CI tests. For GPU-capable images, separately validate build-time stubs and runtime driver-injected libraries.
7. Before publication, update the catalog with exact inputs, source commit, selected conditions, validation result, tag, and digest. Mark the digest as pending while a push is in progress.

## Flavor policy

Core, client, and suite are release selections, not Dockerfile targets:

- Define root packages and conditions at invocation time.
- Record choices in the catalog and connect them to the rcfile codename.
- Add optional features such as `kokkos`, `sycl`, `simulation`, `sirius`, or Python explicitly as conditions. Their dependencies belong in modulesets; do not hide them in image-name conventions.
- Use dedicated ground Dockerfiles where operating system or accelerator provider differs. Put exceptional provider environment variables in that ground flavor, not a generic SDK recipe.

## Validation and stripping

Use the detailed procedures in [architecture.txt](references/architecture.txt). At minimum, validate rcfile resolution, installed prefix, and a clean Suite compilation for every CI-SDK candidate. A successful trace from one build does not prove every unobserved file is removable: compiler drivers, transitive shared objects, deferred test paths, and alternate conditions may be needed later.

When an upstream package, compiler, base image, accelerator toolkit, or rcfile changes, use the catalog's update triggers to select affected rebuilds. Do not claim a registry digest until `docker push` has completed and the registry manifest can be inspected.
