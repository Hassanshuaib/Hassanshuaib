#!/usr/bin/env bash
# Removes ONLY the files recorded by install-manual.sh. Your project board/ folders are never touched.
set -euo pipefail
CL="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
HOMEDIR="$CL/executive-board"
MANIFEST="$HOMEDIR/.installed-files"
[ -f "$MANIFEST" ] || { echo "Nothing to uninstall (no manifest at $MANIFEST)."; exit 0; }
while read -r f; do [ -n "$f" ] && rm -f "$f" && rmdir "$(dirname "$f")" 2>/dev/null || true; done < "$MANIFEST"
rm -rf "$HOMEDIR"
# restore files that the installer had backed up (oldest backup = your original files)
OLDEST="$(ls -d "$CL"/executive-board-backup-* 2>/dev/null | sort | head -1 || true)"
if [ -n "$OLDEST" ]; then
  cp -a "$OLDEST"/. "$CL"/ && echo "Restored your original files from $OLDEST (backup folders kept; delete them when satisfied)."
fi
echo "Removed AI Executive Board files. Project board/ folders were not touched."
