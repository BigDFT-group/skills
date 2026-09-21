---
name: bigdft-suite-integration-maintainer
description: Use this skill when synchronizing BigDFT-suite subtrees with their upstream library repositories, maintaining the suite-to-library CI cascade, or reconciling subrepo divergence. Do not use it for library-internal scientific implementation without repository synchronization work.
license: GPL-3.0-or-later
---
<!-- SPDX-License-Identifier: GPL-3.0-or-later -->

# BigDFT Suite Integration Maintainer

The suite checkout is the authoritative integration view for component-library
source and CI changes. Its `check_library` jobs validate a bundled library and
publish it with `git subrepo push`; that push starts the library’s upstream CI.

## Suite-first publication rule

For every change to a bundled library, including a one-test CI correction:

1. Make the change in the corresponding subtree of
   `luigigenovese/bigdft-suite:devel`.
2. Commit and push the suite branch. Do not first fix only the standalone
   upstream library repository.
3. Let the suite pipeline’s matching `check_library` job validate the library
   and publish the subtree to its configured upstream branch.
4. Once the fork pipeline is suitable, create the
   `luigigenovese/devel` to `l_sim/devel` merge request. The target pipeline
   verifies the same cascade under the shared project configuration.

The rule keeps the suite snapshot, subrepo metadata, and library branches
aligned. It also avoids a later suite CI failure caused by a non-fast-forward
library update.

## Upstream divergence

Direct upstream changes are exceptional: use them only to reconcile an
already-diverged branch, respond to an upstream-only administrative need, or
merge an accepted upstream contribution. Immediately bring that result back
into the suite before further library work:

```sh
# git-subrepo must be available on PATH; use the .gitrepo remote and branch.
git subrepo pull futile
git push genovese devel
```

Read `<library>/.gitrepo` rather than guessing the remote or branch. If the
main worktree has unrelated tracked edits, perform the subrepo pull in an
isolated worktree and cherry-pick its resulting pull commit; never stash,
discard, or overwrite the unrelated work merely to satisfy git-subrepo.

Resolve generated-file conflicts by retaining the version appropriate to the
current build tooling, then complete the subrepo merge and commit normally.
After a direct upstream merge, verify that any CI fast-forward guard is
satisfied with `git merge-base --is-ancestor` before relying on its pipeline.

## CI configuration ownership

Nested library CI files in the suite are source copies that the suite cascade
publishes upstream. Keep shared CI policy and component-specific checks
aligned in both views through the suite-first flow. A common CI base must not
contain a rendered-page assertion that names one particular library; keep
library-specific documentation contracts in that library’s local CI file.

## Boundaries

- Use component maintainer skills for scientific implementation details.
- Use this skill for repository topology, subrepo metadata, CI propagation,
  and merge-request sequencing.
- Do not force-push, rewrite branch history, or delete branches as a normal
  synchronization mechanism. The suite CI owns its configured subrepo push.
