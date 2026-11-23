#!/usr/bin/env python3
"""Create the per-project ./board/ decision-memory folder from templates.

Safe by design: it never overwrites existing files (it only adds missing ones)
and writes only inside the target project directory.

Usage: python3 init_board.py [--project-dir .] [--name "Project name"] [--gitignore]
"""
import argparse
import os
import shutil
import subprocess
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = os.path.join(os.path.dirname(HERE), "templates", "board")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-dir", default=".")
    ap.add_argument("--name", default=None)
    ap.add_argument("--gitignore", action="store_true", help="add board/ to the project's .gitignore if it is a git repo")
    ap.add_argument("--default-agent", default=None, metavar="AGENT",
                    help="also make AGENT (e.g. executive-board:chief-of-staff) the default main agent in this folder "
                         "by setting \"agent\" in <project>/.claude/settings.json (existing settings are kept; a backup is written)")
    a = ap.parse_args()
    proj = os.path.abspath(a.project_dir)
    name = a.name or os.path.basename(proj)
    target = os.path.join(proj, "board")
    created, kept = [], []
    for root, _dirs, files in os.walk(TEMPLATES):
        rel = os.path.relpath(root, TEMPLATES)
        dst_dir = os.path.normpath(os.path.join(target, rel))
        os.makedirs(dst_dir, exist_ok=True)
        for f in files:
            src, dst = os.path.join(root, f), os.path.join(dst_dir, f)
            if os.path.exists(dst):
                kept.append(dst); continue
            if f == ".gitkeep":
                open(dst, "w").close()
            else:
                with open(src, encoding="utf-8") as fh:
                    txt = fh.read().replace("{{PROJECT}}", name).replace("{{DATE}}", date.today().isoformat())
                with open(dst, "w", encoding="utf-8") as fh:
                    fh.write(txt)
            created.append(dst)
    is_git = subprocess.run(["git", "-C", proj, "rev-parse", "--is-inside-work-tree"],
                            capture_output=True, text=True).stdout.strip() == "true"
    gi_msg = ""
    if is_git:
        ignored = subprocess.run(["git", "-C", proj, "check-ignore", "-q", "board/context.md"]).returncode == 0
        if ignored:
            gi_msg = "board/ is already git-ignored."
        elif a.gitignore:
            with open(os.path.join(proj, ".gitignore"), "a", encoding="utf-8") as fh:
                fh.write("\n# AI Executive Board memory (confidential)\nboard/\n")
            gi_msg = "Added board/ to .gitignore."
        else:
            gi_msg = "WARNING: this is a git repository and board/ is NOT ignored; it could be committed. Re-run with --gitignore to protect it."
    agent_msg = ""
    if a.default_agent:
        import json
        sdir = os.path.join(proj, ".claude"); os.makedirs(sdir, exist_ok=True)
        sp = os.path.join(sdir, "settings.json")
        data = {}
        if os.path.exists(sp):
            with open(sp, encoding="utf-8") as fh:
                raw = fh.read()
            data = json.loads(raw or "{}")
            with open(sp + ".bak", "w", encoding="utf-8") as fh:
                fh.write(raw)
        data["agent"] = a.default_agent
        with open(sp, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, ensure_ascii=False)
        agent_msg = "Default agent in this folder set to %s (%s). Remove the \"agent\" line to undo." % (a.default_agent, sp)
    print("Board folder:", target)
    print("Created %d file(s); kept %d existing file(s) untouched." % (len([c for c in created if not c.endswith('.gitkeep')]), len(kept)))
    if gi_msg:
        print(gi_msg)
    if agent_msg:
        print(agent_msg)


if __name__ == "__main__":
    main()
