#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-3.0-or-later

set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
ROOT_DIR=$(cd "$SCRIPT_DIR/.." && pwd)
SRC_DIR="$ROOT_DIR/skills"
DEST_DIR="${CODEX_SKILLS_DIR:-${CODEX_HOME:-$HOME/.codex}/skills}"

usage() {
  cat <<'EOF'
Usage:
  scripts/install-codex-skills.sh install [--dest DIR]
  scripts/install-codex-skills.sh list [--dest DIR]
  scripts/install-codex-skills.sh diff [--dest DIR] [SKILL_NAME]
  scripts/install-codex-skills.sh import-one SKILL_NAME [--dest DIR]

Commands:
  install      Copy repository skills to the Codex skills directory.
  list         Show repository skills and whether each one is installed.
  diff         Compare installed runtime copies against repository skills.
  import-one   Copy one installed skill back into the repository.

Defaults:
  Destination is $CODEX_SKILLS_DIR, or $CODEX_HOME/skills, or ~/.codex/skills.

Notes:
  The repository copy is canonical. The install command is one-way by default:
  repository -> Codex runtime. Use import-one only after reviewing intentional
  improvements made to an installed runtime copy.
EOF
}

die() {
  printf 'ERROR: %s\n' "$*" >&2
  exit 1
}

require_skill_name() {
  local name=$1
  [[ "$name" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]] || die "invalid skill name: $name"
}

parse_dest() {
  while (($#)); do
    case "$1" in
      --dest)
        shift
        (($#)) || die "--dest requires a directory"
        DEST_DIR=$1
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      *)
        die "unexpected argument: $1"
        ;;
    esac
    shift
  done
}

skill_dirs() {
  find "$SRC_DIR" -mindepth 1 -maxdepth 1 -type d -printf '%f\n' | sort
}

validate_repo() {
  python3 "$ROOT_DIR/scripts/validate_skills.py" >/dev/null
}

install_skills() {
  parse_dest "$@"
  validate_repo
  mkdir -p "$DEST_DIR"

  local name src dest
  while IFS= read -r name; do
    src="$SRC_DIR/$name"
    dest="$DEST_DIR/$name"
    mkdir -p "$dest"
    cp -R "$src/." "$dest/"
    printf 'installed %s -> %s\n' "$name" "$dest"
  done < <(skill_dirs)
}

list_skills() {
  parse_dest "$@"
  printf 'Destination: %s\n\n' "$DEST_DIR"

  local name status
  while IFS= read -r name; do
    if [[ -f "$DEST_DIR/$name/SKILL.md" ]]; then
      status=installed
    else
      status=missing
    fi
    printf '%-36s %s\n' "$name" "$status"
  done < <(skill_dirs)
}

diff_one() {
  local name=$1
  require_skill_name "$name"
  [[ -f "$SRC_DIR/$name/SKILL.md" ]] || die "repository skill not found: $name"
  [[ -f "$DEST_DIR/$name/SKILL.md" ]] || die "installed skill not found: $name"
  diff -u "$SRC_DIR/$name/SKILL.md" "$DEST_DIR/$name/SKILL.md" || true
}

diff_skills() {
  local name=
  if (($#)) && [[ "$1" != "--dest" && "$1" != "-h" && "$1" != "--help" ]]; then
    name=$1
    shift
  fi
  parse_dest "$@"

  if [[ -n "$name" ]]; then
    diff_one "$name"
    return
  fi

  local skill
  while IFS= read -r skill; do
    if [[ -f "$DEST_DIR/$skill/SKILL.md" ]] && ! cmp -s "$SRC_DIR/$skill/SKILL.md" "$DEST_DIR/$skill/SKILL.md"; then
      printf '\n=== %s ===\n' "$skill"
      diff_one "$skill"
    fi
  done < <(skill_dirs)
}

import_one() {
  (($#)) || die "import-one requires a skill name"
  local name=$1
  shift
  require_skill_name "$name"
  parse_dest "$@"

  [[ -f "$SRC_DIR/$name/SKILL.md" ]] || die "repository skill not found: $name"
  [[ -f "$DEST_DIR/$name/SKILL.md" ]] || die "installed skill not found: $name"

  cp "$DEST_DIR/$name/SKILL.md" "$SRC_DIR/$name/SKILL.md"
  validate_repo
  printf 'imported %s from %s\n' "$name" "$DEST_DIR/$name/SKILL.md"
}

main() {
  (($#)) || {
    usage
    exit 0
  }

  local command=$1
  shift

  case "$command" in
    install) install_skills "$@" ;;
    list) list_skills "$@" ;;
    diff) diff_skills "$@" ;;
    import-one) import_one "$@" ;;
    -h|--help) usage ;;
    *) die "unknown command: $command" ;;
  esac
}

main "$@"
