---
name: cro-toolkit
description: CRO toolkit: pre-mortem, risk registers, FMEA, quantitative stress tests, regulatory screening, independent review protocol - methods, verified calculator, quality gates.
---

# CRO Toolkit (index — read only what you need)

**Calculator:** `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/boardcalc.py" <function> '<json>'`. Run `list` to see the functions, and `doc <fn> [<fn>...]` for parameters. **Do not read boardcalc.py's source**: it is large and costs tokens. In a manual install, use `~/.claude/executive-board/scripts/boardcalc.py`. References are in `${CLAUDE_PLUGIN_ROOT}/skills/cro-toolkit/references/`.

| Task | Read | boardcalc functions | Optional skills |
|---|---|---|---|
| Risk identification, pre-mortem, register, FMEA, bow-tie | `risk-methods.md` | `risk_register`, `fmea`, `pert_estimate` | — |
| Quantitative risk and stress testing | `quant-risk.md` | `montecarlo`, `breakeven_input`, `stress`, `var_cvar`, `covenant_headroom`, `altman_z` | — |
| Regulatory and compliance screening | `regulatory.md` | — | `small-business:contract-review` |
| **Independent review of a financial analysis or model** | `independent-review.md` (plus `${CLAUDE_PLUGIN_ROOT}/skills/cfo-toolkit/references/model-review.md`) | all relevant ones, to recompute | `board-finance-pack:audit-xls` |

## Quality gates

1. Rate every risk CRITICAL, SIGNIFICANT or WATCH, with likelihood and impact (`risk_register`) and the **evidence** behind the rating. Never inflate speculative concerns.
2. Quantify where possible: break-even headroom, P(loss), expected shortfall, covenant headroom. Do this in boardcalc, not mentally.
3. For each CRITICAL risk, give an early-warning indicator, a mitigation, an owner and a kill criterion.
4. When reviewing another executive's work, **recompute** the headline numbers independently before commenting. Report what you verified and what you could not.
5. Challenge consensus: list where the executives agree without evidence.
6. Regulatory points are flagged for confirmation by a licensed professional. Never state current law from memory as certain.
