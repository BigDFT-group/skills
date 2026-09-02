---
name: wise-container-maintainer
description: Use this skill when the user wants to maintain WISE container images, IDE integration, nested/sidecar container support, display forwarding, host-open integration, agent setup, Git/SSH credential boundaries, CI smoke tests, or reproducible development environments. Do not use it for scientific usage of BigDFT, PSolver, or Futile APIs unless those tasks are part of WISE integration.
license: GPL-3.0-or-later
---

<!--
SPDX-License-Identifier: GPL-3.0-or-later
-->

# Skill: WISE Container Maintainer

## Purpose

Use this skill for maintenance of WISE, a Docker Compose based workstation environment for sandboxed AI-agent and IDE sessions. WISE generates per-session env files, starts an IDE container, optionally attaches a Docker-in-Docker sidecar, and provides host integration for display, ports, temporary files, and controlled host file/browser opening.

## Scope

This skill is for:

- WISE scripts under `scripts/`, Compose files under `compose/`, image files under `docker/`, CI smoke tests, and WISE user/developer docs;
- session env generation, launch/down/check workflows, named sessions, workspace/session-home/tmp path mapping, and Compose override selection;
- OpenVSCode, Zed, X11/Wayland, GPU/DRI/Vulkan diagnostics, and host opener behavior;
- sidecar Docker behavior, nested container workflows, port publishing, and Docker data volume lifecycle;
- WISE-specific credential isolation design such as SSH/Git mounts or future agent forwarding;
- creating or updating WISE-oriented Codex skills after behavior has stabilized.

This skill is not for ordinary scientific use of BigDFT, PSolver, Futile, or RemoteManager unless the work is about integrating those tools into WISE.

## Project Workflow

When working in the WISE repo:

- Inspect existing scripts and docs before editing. Prefer `rg` and focused `sed -n` reads.
- Keep changes aligned across CLI help, generated docs, user docs, and CI smoke tests.
- Regenerate CLI docs after changing helper `--help` output:

```bash
./scripts/generate-cli-docs
```

- Run lightweight validation before reporting success:

```bash
bash -n scripts/wise-env scripts/wise-up scripts/wise-check
./scripts/ci/static-checks
```

- For Docker behavior changes, run the relevant smoke when available:

```bash
./scripts/ci/sidecar-smoke
./scripts/ci/sidecar-wise-up-smoke
./scripts/ci/sidecar-nvidia-smoke  # NVIDIA driver/toolkit host only
./scripts/ci/bridge-startup-smoke
./scripts/ci/host-open-smoke
```

- Do not stage unrelated untracked files. Preserve user changes in the worktree.

## Core Commands

Normal session flow:

```bash
./scripts/wise-env
./scripts/wise-check
./scripts/wise-up
./scripts/wise-shell
./scripts/wise-down
```

Named sessions live under `~/.config/wise/sessions/NAME.env` by default:

```bash
./scripts/wise-env --name NAME --workdir /path/to/work
./scripts/wise-up --name NAME
./scripts/wise-shell --name NAME
./scripts/wise-sessions
```

`wise-up` runs `wise-check` by default. `wise-up --extra-compose FILE` records override provenance in the env file so later helper commands reuse it.

## Execution Context

Before proposing a WISE administration command, establish whether the agent is on the launcher host or inside the WISE workstation. Treat a shell as inside WISE when `/.dockerenv` exists or WISE container variables such as `WISE_CONTAINER_MODE` are present. State the required context next to commands.

- **Launcher host only:** `wise-env`, `wise-up`, `wise-down`, `wise-check`, `wise-sessions`, `wise-shell`, and `wise-sudo`; host Docker/NVIDIA runtime configuration; `xhost`; host network diagnostics. `wise-sudo` is launched on the host and runs its requested command as root *inside the existing WISE workstation*. Do not tell an agent already inside WISE to invoke it there.
- **Inside WISE:** normal development commands, editors, and `docker run` task containers through `DOCKER_HOST`. When a host-only action is needed, give the user a short labelled host-terminal recipe instead of attempting it from the session.
- **Nested task container:** only paths mirrored into the sidecar (workspace, session home, or `/tmp`) can be bind-mounted. It cannot perform WISE lifecycle operations.

## Session Renewal

A configuration change that affects Compose selection, mounts, network policy, or sidecar image requires recreation from the launcher host. Preserve an existing session by using its env file as both the input base and output file. For example, to enable the NVIDIA sidecar for an existing named session:

```bash
# Launcher host, outside WISE.
SESSION="$HOME/.config/wise/sessions/research.env"
./scripts/wise-down --env-file "$SESSION"
./scripts/wise-env --base-env "$SESSION" --env-file "$SESSION" --gpu
./scripts/wise-check --env-file "$SESSION"
./scripts/wise-up --env-file "$SESSION" --build
```

Before this GPU renewal, configure the launcher host NVIDIA runtime and verify it outside WISE:

```bash
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
nvidia-smi -L
docker run --rm --gpus all nvidia/cuda:12.8.1-base-ubuntu24.04 nvidia-smi -L
```

Then, inside the renewed WISE session, verify the nested path with `docker run --rm --gpus all nvidia/cuda:12.8.1-base-ubuntu24.04 nvidia-smi -L`. If the agent is currently inside WISE, it should ask the user to run the host block, then continue only after the renewed session is available.

## Session Model

Important generated/session variables:

- `WISE_NAME`: session selector; default project is `wise`, named projects are `wise-NAME`.
- `HOST_WORKDIR`: host workspace root.
- `CONTAINER_WORKSPACE_PATH`: in-container workspace path, selected by `--workspace-path`.
- `WISE_SESSION_HOME`: host directory mounted as `CONTAINER_HOME`.
- `HOST_TMP`: host directory mounted as container `/tmp`, defaulting to `/tmp/wise-<name>`.
- `CONTAINER_XDG_RUNTIME_DIR`: session-specific runtime dir inside `/tmp`.
- `DISPLAY`: written as literal `DISPLAY=$DISPLAY` so the launch shell supplies the live display.
- `WISE_EXTRA_COMPOSE_FILES`: recorded extra Compose overrides.

WISE sets container `PATH` in Compose so `${CONTAINER_HOME}/.local/bin` is visible to OpenVSCode, startup hooks, `wise-shell`, and `docker compose exec`. Do not put `PATH=...:$PATH` into generated env files; Compose env files are not shell init files.

## Sidecar Docker

Sidecar mode is the default for generated sessions. It uses `compose/compose.docker-sidecar.yaml` and sets inner Docker access through `DOCKER_HOST=tcp://127.0.0.1:2375` inside WISE. The sidecar daemon is privileged but does not mount the host Docker socket.

Key rules:

- Do not mount `/var/run/docker.sock` from the host; host Docker socket access is effectively host-root capability.
- `WISE_DOCKER_DATA_VOLUME` stores sidecar Docker images/layers and is preserved by `wise-down` by default.
- Do not use the same Docker data volume from multiple active WISE sessions. `wise-up` should refuse that case.
- Use `wise-down` prune options for sidecar cleanup when disk space is needed.
- Inside WISE, nested containers can mount WISE-visible paths, for example `/workspace/work`, but files created by root in the inner container will be root-owned from WISE unless user mapping is handled.
- `WISE_GPU=0` uses the ordinary sidecar. `WISE_GPU=1` selects `compose.docker-sidecar.gpu.yaml`, which builds an NVIDIA Container Toolkit-enabled nested daemon so inner `docker run --gpus all` can work. Require a working host NVIDIA driver and host Docker NVIDIA runtime before enabling it.

## Ports and Networking

In sidecar mode, published ports are explicit and generated into a per-session `*.ports.yaml` override. Use:

```bash
./scripts/wise-env --publish 8888
./scripts/wise-env --publish 9000:8000
./scripts/wise-env --publish 127.0.0.1:9000:8000
```

Rules:

- OpenVSCode is published automatically from `OPENVSCODE_PORT`; use `wise-env --openvscode-port PORT` to change both the service and its automatic mapping without retaining stale `3123` mappings.
- Default bind address is `127.0.0.1`.
- Explicit non-loopback binds such as `0.0.0.0:PORT:PORT` expose the service beyond the host and require service-level authentication.
- Bridge mode is the default. Use `wise-env --sidecar-network host` only as an explicit VPN/debug fallback: the privileged sidecar then shares host networking and service listeners bypass generated `ports:` mappings.
- Bridge sidecar sessions enable IPv6 by default with a deterministic ULA `/64`; use `--network-ipv6-subnet` to override it or `--no-ipv6` only where the Docker host cannot support IPv6 bridges.
- In non-sidecar host-network mode, `OPENVSCODE_PORT` remains directly relevant for avoiding host port collisions.

## Display, X11, Zed, and GPU

Display checks happen after startup. Common X11 failure text includes `Authorization required`, `unable to open display`, or Zed `Failed to initialize X11 client`.

Preferred persistent X11 authorization workflow:

```bash
./scripts/wise-env --env-file ~/.config/wise/sessions/default.env --xhost-localuser
./scripts/wise-up --env-file ~/.config/wise/sessions/default.env
```

This writes `WISE_XHOST_LOCALUSER=1`; `wise-up` then runs `xhost +SI:localuser:$USER` on the launcher host before Compose starts. This is opt-in because X11 access lets GUI-capable processes running as the host user interact with the host desktop.

Temporary suppression and manual revocation:

```bash
./scripts/wise-up --no-xhost-auth
xhost -SI:localuser:$(id -un)
```

`--no-xhost-auth` only skips WISE adding authorization for that launch; it does not revoke host X server state already added.

GPU checks:

```bash
./scripts/wise-gpu-check --env-file ~/.config/wise/sessions/default.env
```

`llvmpipe` is acceptable as an extra fallback when Vulkan also reports integrated, discrete, or virtual hardware GPUs. It is a problem when it is the only Vulkan device. Linux GPU access depends on `/dev/dri` mounts and supplemental render-node GIDs from `wise-env`. Numeric GIDs in `id` output are valid when the container has no matching group name.

Use `ZED_ALLOW_EMULATED_GPU=1` only when software rendering is intentional; it hides the warning but does not restore hardware acceleration. Intel/Mesa GUI acceleration uses `/dev/dri` and is independent of `WISE_GPU`; `--gpus all` is the NVIDIA compute path.

## Host Opener

`wise-up --host-open` starts an opt-in Unix-socket bridge so processes inside WISE can open host browser/document targets through `xdg-open`/`sensible-browser`.

Security model:

- Accepted URL schemes: `http`, `https`, `mailto`.
- Accepted file opens: mapped `.pdf` and `.docx` under workspace, session home, or session tmp.
- The bridge rejects arbitrary local files and arbitrary commands.
- Socket path is inside `${HOST_TMP}` and appears in WISE as `/tmp/wise-host-open.sock`.
- `wise-down` stops managed bridges started through `wise-up`; manually managed bridges are left alone.

Validate with:

```bash
./scripts/ci/host-open-smoke
```

## CI and Documentation

CI includes static checks plus representative smoke tests for sessions, host-open, bridge startup, ordinary sidecar workflows, and a manually run NVIDIA sidecar workflow. When adding options:

- update CLI help;
- regenerate `docs/generated/cli-reference.md`;
- update `docs/user-guide/configuration.md` or `docs/user-guide/launch-modes.md` as appropriate;
- add or adjust smoke assertions, usually in `scripts/ci/session-smoke` for env generation and `scripts/ci/sidecar-wise-up-smoke` for user-facing launch behavior.

## Safety Boundaries

- Never replace the host Docker socket approach with a convenience mount.
- Do not silently relax host desktop or credential access. Prefer explicit env-file policy plus visible warnings.
- Treat SSH/Git credentials as sensitive. Prefer future agent-forwarding designs over mounting raw private keys when possible.
- Do not make sidecar port bindings public unless the user explicitly asks and the docs warn about exposure.
- Do not remove backward-facing safeguards such as project replacement checks or sidecar data-volume concurrency checks without a clear replacement.
