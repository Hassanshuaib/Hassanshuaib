#!/bin/bash
# usage: run.sh <label> <project_dir> <prompt> [resume_session_id] [extra args...]
label=$1; dir=$2; prompt=$3; resume=$4; shift 4
SP=${SP:-$(cd "$(dirname "$0")" && pwd)}
cd "$dir" || exit 1
args=(-p "$prompt" --output-format stream-json --verbose --agent executive-board:chief-of-staff
  --allowedTools "Read,Write,Edit,Glob,Grep,Agent,Skill,WebSearch,Bash(python3:*),Bash(ls:*),Bash(mkdir:*),Bash(cat:*)")
[ -n "$resume" ] && args+=(--resume "$resume")
claude "${args[@]}" "$@" > "$SP/$label.jsonl" 2> "$SP/$label.err"
python3 "$SP/summ.py" "$SP/$label.jsonl"
