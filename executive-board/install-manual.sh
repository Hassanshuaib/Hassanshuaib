#!/usr/bin/env bash
# Manual (non-plugin) install of the AI Executive Board into ~/.claude.
# Prefer the plugin install (see README). Use this only if plugins are unavailable.
# Safe: backs up any file it would replace, records what it installed, reversible
# with uninstall-manual.sh.
set -euo pipefail
SRC="$(cd "$(dirname "$0")" && pwd)"
CL="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
HOMEDIR="$CL/executive-board"
STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP="$CL/executive-board-backup-$STAMP"
MANIFEST="$HOMEDIR/.installed-files"
mkdir -p "$CL/agents" "$CL/skills" "$HOMEDIR"
: > "$MANIFEST.tmp"
put() { # src dst
  if [ -e "$2" ] && ! grep -qxF "$2" "$MANIFEST" 2>/dev/null; then
    mkdir -p "$BACKUP/$(dirname "${2#$CL/}")"; cp -a "$2" "$BACKUP/${2#$CL/}"
    echo "backed up existing $2"
  fi
  mkdir -p "$(dirname "$2")"
  sed "s#\${CLAUDE_PLUGIN_ROOT}#$HOMEDIR#g" "$1" > "$2"
  echo "$2" >> "$MANIFEST.tmp"
}
for f in "$SRC"/agents/*.md; do put "$f" "$CL/agents/$(basename "$f")"; done
for d in "$SRC"/skills/*/; do n=$(basename "$d"); put "$d/SKILL.md" "$CL/skills/$n/SKILL.md"; done
rm -rf "$HOMEDIR/scripts" "$HOMEDIR/templates" "$HOMEDIR/agents"
cp -a "$SRC/scripts" "$SRC/templates" "$SRC/agents" "$HOMEDIR/"
mv "$MANIFEST.tmp" "$MANIFEST"
echo "Installed AI Executive Board into $CL (agents: chief-of-staff cfo coo cmo cso cro secretary)."
[ -d "$BACKUP" ] && echo "Backups of replaced files: $BACKUP"
echo "Start with:  claude --agent chief-of-staff"
