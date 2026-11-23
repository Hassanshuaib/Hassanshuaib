---
name: cso-toolkit
description: CSO toolkit: strategy frameworks, bottom-up market sizing, market entry, option scoring, scenarios - methods, verified calculator, quality gates.
---

# CSO Toolkit (index — read only what you need)

**Calculator:** `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/boardcalc.py" <function> '<json>'`. Run `list` for all functions, or add `--doc` for one. In a manual install, use `~/.claude/executive-board/scripts/boardcalc.py`. References are in `${CLAUDE_PLUGIN_ROOT}/skills/cso-toolkit/references/`.

| Task | Read | boardcalc functions | Optional skills |
|---|---|---|---|
| Frameworks, competitive advantage, industry analysis | `frameworks.md` | `hhi` | `board-finance-pack:competitive-analysis` |
| Market sizing and adoption | `market-sizing.md` | `market_sizing`, `bass_diffusion`, `cagr` | `anthropic-skills:deep-research` |
| Market entry, business model, options, trade-offs, scenarios | `options-entry.md` | `decision_matrix`, `expected_value`, `scenarios` | — |

## Quality gates

1. Market size is **bottom-up** (customers × frequency × value) and cross-checked top-down. Show the arithmetic and the sources. TAM is not a forecast.
2. Use frameworks only where they change the conclusion. Never fill a framework for decoration.
3. Always include the options "do nothing", "smaller or staged" and "partner/license" next to the big move.
4. Robustness: show whether the recommended option survives weight changes (`decision_matrix` rank-flip test) and different scenarios.
5. Name the competitive advantage mechanism (one of the 7 Powers, or none). "Better execution" alone is not durable.
6. Give milestones and kill criteria: what must be true at each gate to continue.
