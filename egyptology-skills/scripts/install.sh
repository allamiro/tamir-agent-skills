#!/usr/bin/env bash
# Install the Egyptology skills into an agent's skills directory.
#
# Usage:
#   scripts/install.sh --claude --project /path/to/repo      # -> /path/to/repo/.claude/skills/
#   scripts/install.sh --agents --project /path/to/repo      # -> /path/to/repo/.agents/skills/
#   scripts/install.sh --claude --agents --user              # -> ~/.claude/skills and ~/.agents/skills
#   scripts/install.sh --claude --project . --symlink        # link instead of copy (tracks this checkout)
#   scripts/install.sh --claude --project . --dry-run
#
# Options:
#   --claude        install for Claude Code (.claude/skills)
#   --agents        install to the cross-tool .agents/skills location used by Codex-style agents
#   --project DIR   target project root (default: current directory)
#   --user          target the home directory instead of a project
#   --symlink       symlink each skill instead of copying
#   --force         replace skills that already exist at the destination
#   --dry-run       print what would happen
#   -h, --help      show this help
#
# Install ALL skills together: they refer to each other (transliteration uses
# gardiner-sign-lookup).
# Paths: Claude Code reads .claude/skills; Codex reads .agents/skills in the repo (and parent
# folders up to the repo root), $HOME/.agents/skills and /etc/codex/skills (OpenAI Codex skills
# documentation, read 2026-10-14). Tool versions change: confirm in your tool's docs.
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
src="$here/skills"
targets=()
base="$(pwd)"
mode="copy"
force=0
dry=0

usage() { sed -n '2,25p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; }

while [ $# -gt 0 ]; do
  case "$1" in
    --claude) targets+=(".claude/skills") ;;
    --agents) targets+=(".agents/skills") ;;
    --project) [ $# -ge 2 ] || { echo "error: --project needs a directory" >&2; exit 2; }; base="$(cd "$2" && pwd)"; shift ;;
    --user) base="$HOME" ;;
    --symlink) mode="symlink" ;;
    --force) force=1 ;;
    --dry-run) dry=1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "error: unknown option $1" >&2; usage >&2; exit 2 ;;
  esac
  shift
done

if [ ${#targets[@]} -eq 0 ]; then
  echo "error: choose at least one of --claude or --agents" >&2
  exit 2
fi
if [ ! -d "$src" ]; then
  echo "error: skills directory not found at $src" >&2
  exit 1
fi

run() { if [ "$dry" -eq 1 ]; then echo "[dry-run] $*"; else "$@"; fi; }

for t in "${targets[@]}"; do
  dest="$base/$t"
  run mkdir -p "$dest"
  for d in "$src"/*/; do
    name="$(basename "$d")"
    [ -f "$d/SKILL.md" ] || continue
    target="$dest/$name"
    if [ -e "$target" ] || [ -L "$target" ]; then
      if [ "$force" -eq 1 ]; then
        run rm -rf "$target"
      else
        echo "skip (exists, use --force to replace): $target"
        continue
      fi
    fi
    if [ "$mode" = "symlink" ]; then
      run ln -s "$d" "$target"
    else
      run cp -R "$d" "$target"
    fi
    echo "installed: $target"
  done
done
