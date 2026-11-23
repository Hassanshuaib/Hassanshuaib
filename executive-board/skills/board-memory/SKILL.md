---
name: board-memory
description: Per-project decision memory for the AI Executive Board - create the ./board/ folder (context, brainstorm, assumptions, decision register, minutes, actions, reports, lessons) and record decisions, assumptions and action items. Use when the CEO wants to save/record a decision, track assumptions or actions, set up board memory for a project, or review what was decided before.
---

# Board memory

All memory for a project lives in `./board/` inside **the current project directory**. Nothing goes in user-level folders. This keeps every company's data separate.

## Create the folder (once per project; ask the CEO first)
Run: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/init_board.py" --project-dir "<current project dir>" --name "<project name>"`
- If `${CLAUDE_PLUGIN_ROOT}` didn't resolve (manual install), use Glob to find `**/executive-board/scripts/init_board.py`.
- The script never overwrites files. If it prints a git **WARNING**, ask the CEO whether to protect the folder, then re-run with `--gitignore`.
- Optionally, if the CEO agrees, add `--default-agent executive-board:chief-of-staff` (or `chief-of-staff` for a manual install). After that, plain `claude` in this folder opens directly as the Chief of Staff. The script keeps the existing settings and writes a `.bak` copy.
- Then fill in `board/context.md` from the conversation, keeping it under 60 lines and marking facts versus assumptions.

## Record a decision
1. Read `board/decisions/register.md` and take the next number (DEC-001, DEC-002, …).
2. Copy `board/decisions/TEMPLATE.md` to `board/decisions/DEC-NNN-<slug>.md` and fill in every section from real sources: the conversation, files in `board/analyses/` and the minutes. Unknown fields get "TBD". Never invent anything.
3. Status stays **Proposed** until the CEO explicitly decides. Then set it to Approved, Rejected or Deferred, and record the CEO's words in section 11.
4. Add or update the row in `board/decisions/register.md`.

## Assumptions, actions, lessons, brainstorms
- Assumptions → add a row to `board/assumptions.md` (A-IDs). Update their status when an executive challenges or validates one. Never delete rows.
- Actions → `board/actions.md`. Every action needs an owner and a due date or trigger.
- Lessons → `board/lessons.md` after a decision is reviewed.
- Brainstorms → `board/brainstorm/<date>-<topic>.md`: the idea, open questions, options, and the next step.

## Rules
- Keep files concise. They are read again in later sessions, so brevity saves tokens.
- Never store passwords, API keys, bank or ID numbers.
- Never read or write another project's `board/` folder unless the CEO explicitly asks.
