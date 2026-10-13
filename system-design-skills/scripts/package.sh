#!/usr/bin/env bash
# Build zip archives of the skills for tools that import skills from an archive.
#
# Usage:
#   scripts/package.sh            # writes dist/system-design-skills.zip (all skills together)
#   scripts/package.sh --each     # also writes one zip per skill (dist/<skill>.zip)
#
# The combined archive keeps every skill as a top-level folder, so the cross-skill
# template references (../system-design/assets/templates/...) keep working. A per-skill
# zip does NOT include those shared templates; use it only for system-design on its own
# or add the templates to the target tool.
# For ChatGPT / OpenAI uploads use scripts/build_chatgpt.py instead: it builds one
# self-contained zip per skill that satisfies OpenAI's bundle rules.
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
out="$here/dist"
each=0
case "${1:-}" in
  --each) each=1 ;;
  -h|--help) sed -n '2,13p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit 0 ;;
  "") ;;
  *) echo "error: unknown option $1" >&2; exit 2 ;;
esac

command -v zip >/dev/null 2>&1 || { echo "error: 'zip' command not found" >&2; exit 1; }
mkdir -p "$out"
rm -f "$out/system-design-skills.zip"
(cd "$here/skills" && zip -qr "$out/system-design-skills.zip" . -x '*.DS_Store' -x '*__pycache__*')
echo "wrote $out/system-design-skills.zip"
if [ "$each" -eq 1 ]; then
  for d in "$here"/skills/*/; do
    n="$(basename "$d")"
    rm -f "$out/$n.zip"
    (cd "$here/skills" && zip -qr "$out/$n.zip" "$n" -x '*.DS_Store' -x '*__pycache__*')
    echo "wrote $out/$n.zip"
  done
fi
