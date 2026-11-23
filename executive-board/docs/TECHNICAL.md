# AI Executive Board — Technical Guide

The user-facing guide (in Arabic) is `../README.md`. This document covers the architecture, the verified platform facts, the LLM Council evaluation, costs, extension, maintenance and uninstall.

## 1. Architecture (the smallest reliable design)

```
CEO ──► Chief of Staff (main thread: `claude --agent …chief-of-staff`, the `board` skill, or the project setting "agent")
           │  Mode 1: talks itself (0 sub-agents)
           │  Mode 2: Agent tool → 1–2 specialists (in parallel when independent, sequential for handoffs)
           │  Mode 3: board-council skill → parallel executives + CRO → (optional peer review) → verdict
           ▼
   cfo · coo · cmo · cso · cro · secretary   (sub-agents; no Agent tool → no nested delegation)
           │ write full analyses + calc scripts
           ▼
   <project>/board/   (per-project decision memory, plain Markdown, optionally git-ignored)
```

Everything ships as a single **Claude Code plugin** (`executive-board/`), published by the marketplace file at the repository root (`.claude-plugin/marketplace.json`, marketplace name `hassan-board`).

| Path | What |
|---|---|
| `agents/chief-of-staff.md` | The orchestration playbook: modes, honesty rules, handoff protocol, memory and safety rules. Used as the main-thread agent, or read by the `board` skill |
| `agents/{cfo,coo,cmo,cso,cro}.md` | The specialists: expertise, method, and the shared "Board standards" (fact/assumption separation, auditable python calculations, ≤ 350-word return, write only in `board/`) |
| `agents/secretary.md` | Reports, minutes, registers. No invented data; files are reported only after they are verified |
| `skills/board` | Entry point. Activates Chief of Staff mode in any session |
| `skills/board-council` | Tiered deliberation (Lite / Standard / Deep) |
| `skills/board-memory` | Creates `board/` and records decisions, assumptions and actions |
| `skills/board-report` | Report workflow that delegates to the Secretary |
| `scripts/init_board.py` | Creates `board/` from `templates/board/`. Never overwrites. Optional `--gitignore` and `--default-agent` |
| `scripts/make_report.py` | Markdown → DOCX (Arabic RTL), PDF (via LibreOffice; reportlab fallback for non-Arabic), XLSX (one sheet per table, numbers typed). Prints JSON of the files that really exist |
| `templates/board/` | Memory skeleton, including the decision-record template with every required field |
| `install-manual.sh` / `uninstall-manual.sh` | Non-plugin fallback into `~/.claude` (backs up, keeps a manifest, restores on uninstall) |

Skill frontmatter uses only `name` and `description`, because Cowork and claude.ai reject Claude-Code-only fields such as `argument-hint`.

## 2. Platform facts verified (official docs, Nov 2026)

Sources: code.claude.com/docs/en/sub-agents, /plugins, /plugins-reference, /plugin-marketplaces, /skills, and the support.claude.com Cowork and plugin articles.

- **Agent locations and precedence:** managed > `--agents` > `.claude/agents/` > `~/.claude/agents/` > plugin `agents/`. Plugin agents are namespaced (`executive-board:cfo`).
- **Main-thread agent:** `claude --agent <name>`, or `"agent": "<name>"` in a settings file. A main-thread agent *can* use the Agent tool to spawn sub-agents. This is why the Chief of Staff must be the main thread, not a sub-agent.
- **Automatic delegation** is driven by the `description` field. It is not guaranteed. Explicit requests ("ask the CFO") and `@agent-executive-board:cfo` are reliable.
- **Plugin sub-agents ignore** `hooks`, `mcpServers` and `permissionMode`. None are used here.
- **`memory:` frontmatter** (`user`/`project`/`local`) exists but was deliberately **not used**. `user` scope would mix companies across projects, and file-based `board/` memory is transparent and portable.
- **Cowork:** "the same plugin format also installs on claude.ai and in Cowork" (Customize → Plugins → Add → Add marketplace → `owner/repo`). Plugins and skills added on the Claude account sync **one-way** into Claude Code (v2.1.273+). Cowork does **not** read `~/.claude/skills/`. No documentation says Cowork and Claude Code share conversations, memory or project files, so assume they don't. **Not tested in Cowork.**
- **Private repository marketplaces** use the machine's own git credentials: an SSH key, or `gh auth login` followed by `gh auth setup-git`. With HTTPS and no SSH key, set `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1`.
- **Cloud sessions** (claude.ai/code) don't load plugins that are enabled only in user settings. To use the board in a cloud session, enable it in the repository's `.claude/settings.json` (`enabledPlugins`).

## 3. LLM Council evaluation and decision

The skill at github.com/aiwithremy/claude-skills-llm-council (commit `55ee36e`, 2026-04-26) was inspected.

| Check | Finding |
|---|---|
| Contents | `SKILL.md` and `README.md` only. Pure instructions: no scripts, no dependencies, no network calls, no credentials |
| Security | Safe to read. There is nothing to execute |
| License | **No license file**, so redistribution rights are unclear. **Not vendored into this repo** |
| Method | 5 thinking-style advisors → 5 anonymised peer reviews → 1 chairman. About **11 sub-agent calls per run** |
| Fit | The advisors are generic lenses, not executive roles. Its broad triggers ("should I X or Y") would compete with the Chief of Staff. It also contradicts itself: "do NOT generate files" versus "the visual report matters" |

**Decision:** don't install it as-is. Its core method (independent answers → anonymised peer review → chaired synthesis that may side with a well-reasoned dissenter) is re-implemented, with credit, in `skills/board-council`. That version uses the board's executives and cost tiers:

- **Lite (default):** 2–4 relevant executives plus the CRO in parallel; the Chief of Staff chairs. 3–5 calls.
- **Standard (on request):** Lite plus one anonymised peer-review round with 2 reviewers. 5–7 calls.
- **Deep (explicit request, with the cost stated first):** Standard plus a fresh independent chairman agent and/or the original 5-lens pass. 8–12 calls.

If you still want the original skill, install it yourself from its repository. Its triggers may then overlap with `board-council`.

**On independence:** every executive is the same model with different instructions and a fresh context. This reduces anchoring, but it is *not* the multi-model diversity of Karpathy's original. The verdict footer says so. For real model diversity, set a different `model:` (for example `sonnet`) in `agents/cro.md`.

## 4. Token and cost trade-offs (measured)

The plugin's always-on overhead is about **1.3k tokens per session** (from `claude plugin details`), including sessions unrelated to business. On-invoke costs: Chief of Staff playbook about 3.3k tokens, each executive about 1.1–1.4k, council skill about 1.7k.

Measured on Opus, at API list-price equivalent. Subscription plans consume usage limits instead.

| Interaction | Sub-agents | Measured cost |
|---|---|---|
| Brainstorm (Test A) | 0 | $0.44 (first turn, including cache creation) |
| Continue from `board/` in a new session (Test G) | 0 | $0.26 |
| Ask CFO, SAR 300k, full model (Test B) | 1 | ≈ $1.02 |
| CFO → COO handoff (Test C) | 1 | ≈ $1.09 |
| Quick CFO question in a plain session (Test F2) | 1 | $0.28 |
| Council **Lite**, fresh project (Test D2) | 3 | $1.70 |
| Council **Standard** (Test D, before tuning) | 5 + 2 | ≈ $5.05 |
| Report DOCX/PDF/XLSX (Test E, before tuning) | 1 | ≈ $1.85 |

Levers already applied:
- Mode 1 is the default.
- "Full board" maps to Lite.
- File-path handoffs replace pasted context.
- Executives return ≤ 350 words and use ≤ 5 web searches.
- One review round maximum.
- The Secretary runs the generator once and does no visual QA unless asked.

Further optional levers:
- `model: sonnet` on specialists for routine work: much cheaper, somewhat less deep.
- `effort: low` on the Secretary.

## 5. Adding a new executive (for example a General Counsel or CHRO)

1. Copy `agents/cso.md` to `agents/clo.md`. Change `name`, `description` (say when to use it), `color`, the role paragraph and the Method. Keep the "Board standards" block.
2. Add a row to the table in section 1 of `agents/chief-of-staff.md`.
3. Bump `version` in `.claude-plugin/plugin.json`, commit and push, then run `/plugin marketplace update hassan-board`.
4. Check that `/agents` lists `executive-board:clo`.

## 6. Maintenance

- **Edit behaviour** in the agent and skill Markdown files. There is no code to change, except the two scripts.
- **Validate** with `claude plugin validate .` (from the repo root) and `claude plugin validate ./executive-board`.
- **Update** clients with `/plugin marketplace update hassan-board`. Plugins pin to `version`, so bump it on every release.
- **Re-run the acceptance tests:** `tests/run.sh` and `tests/summ.py` drive headless `claude -p --agent executive-board:chief-of-staff --output-format stream-json` and list every tool and Agent call as evidence. Use fictional projects only.

## 7. Uninstall and revert

| What | How |
|---|---|
| Plugin | `/plugin uninstall executive-board@hassan-board`, then optionally `/plugin marketplace remove hassan-board` |
| Manual install | `executive-board/uninstall-manual.sh`. Removes only the files listed in its manifest and restores the backups |
| Per-project default agent | Delete the `"agent"` line in `<project>/.claude/settings.json`. A `.bak` copy was written |
| Project memory | `board/` folders are never deleted by uninstall. Delete them yourself if wanted |

## 8. Security posture

- No hooks, no MCP servers, no credentials and no network integrations ship with the plugin.
- Executives are told: read-only public web research only, never contact external systems, write only inside `<project>/board/`, never store secrets.
- These are *instructions*, not a sandbox. Claude Code's permission prompts remain the enforcement layer, so keep your normal permission mode.
- Third-party code was inspected, not executed. LLM Council contains no code.
- Accounting, banking and CRM connectors that exist in your Claude account are not used by the board. Connecting them needs your explicit approval each time.
