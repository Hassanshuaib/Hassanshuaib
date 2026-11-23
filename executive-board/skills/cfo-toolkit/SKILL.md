---
name: cfo-toolkit
description: CFO toolkit: corporate finance, valuation, capital budgeting, 3-statement models, FSA, risk modelling, unit economics, FP&A, LBO/M&A - methods, verified calculator, quality gates.
---

# CFO Toolkit (index — read only the reference you need)

**Calculator** (stdlib Python; verified against LibreOffice formulas and closed forms by 36 tests):
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/boardcalc.py" <function> '<json>'`. Run `... boardcalc.py list` to see all functions, or add `--doc` after the JSON for one function's documentation. In a manual install, the path is `~/.claude/executive-board/scripts/boardcalc.py`. In Python: `sys.path.insert(0, "<that scripts dir>"); import boardcalc as bc`.

References live in `${CLAUDE_PLUGIN_ROOT}/skills/cfo-toolkit/references/`. If an optional skill below isn't installed, follow the reference alone.

| Task | Read | boardcalc functions | Optional skills (if installed) |
|---|---|---|---|
| Cost of capital, capital structure, ROIC/EVA, capital allocation, risk-adjusted returns | `corporate-finance.md` | `capm`, `unlever_beta`, `relever_beta`, `wacc`, `roic_eva`, `value_driver` | — |
| DCF, terminal value, comparable companies, precedents, valuation cross-checks | `valuation.md` | `dcf`, `dcf_grid`, `fcff_from`, `multiples_valuation` | `board-finance-pack:competitive-analysis` |
| NPV/IRR/MIRR/payback, mutually exclusive projects, investment feasibility | `capital-budgeting.md` | `npv`, `irr`, `mirr`, `payback`, `compare_projects`, `eaa`, `project` | — |
| Three-statement model, forecasting, reconciliation, ratio analysis, CCC, liquidity/solvency | `three-statement-fsa.md` | `three_statement`, `three_statement_xlsx`, `recalc_compare`, `ratios`, `altman_z` | `board-finance-pack:3-statement-model` (to fill an existing template), `finance:reconciliation`, `finance:financial-statements` |
| Sensitivity, scenarios, Monte Carlo, stress and reverse stress tests | `risk-modeling.md` | `tornado`, `grid`, `scenarios`, `montecarlo`, `breakeven_input`, `stress`, `covenant_headroom` | — |
| Unit economics, pricing maths, contribution margin, break-even, FP&A, budgets, variance analysis, dashboards | `unit-economics-fpa.md` | `breakeven`, `ltv`, `cohort_ltv`, `price_change_breakeven`, `subscription_price_change`, `variance_analysis`, `cagr` | `finance:variance-analysis` |
| LBO, M&A accretion/dilution, PE returns, due diligence | `pe-ma.md` | `lbo`, `accretion_dilution` | `board-finance-pack:lbo-model`, `:merger-model`, `:returns-analysis`, `:dd-checklist` |
| Auditing a model (yours or someone else's); independent review | `model-review.md` | `recalc_compare` | `board-finance-pack:audit-xls` |
| Sources to cite when research is required | `sources.md` | — | — |
| Excel deliverable with live formulas | `three-statement-fsa.md` §Excel | `three_statement_xlsx` | `anthropic-skills:xlsx` or `xlsx` |

## Quality gates (apply to every deliverable; state which ones you ran)

1. **No invented data.** Every number is tagged **Fact** (with source), **Input** (from the CEO), **Estimate** (yours, with basis) or **Opinion**. Missing inputs are listed explicitly.
2. **Verified arithmetic.** Every figure you present comes from executed code (boardcalc or a saved script in `board/analyses/calc/`) or from spreadsheet formulas. For models, state the check results: BS balances, cash ties out, RE rolls forward.
3. **Cash ≠ profit.** Always show cash flow (FCF, peak funding, runway) next to accounting profit, and explain any gap: D&A, working capital, capex, tax timing.
4. **Reality check.** Benchmark growth, margins and multiples against the base rate. Flag, for example, revenue CAGR above 30%, terminal growth above about 3–4% nominal, margins above peer best-in-class, ROIC far above WACC forever, or a TV share above 75%.
5. **Triangulate.** Value with at least two methods (for example DCF plus multiples, or Gordon plus exit multiple), reconcile any gap above 20%, and give a range, not a point.
6. **Downside first.** Give Base, Downside and Upside cases, a tornado of the top drivers, the break-even value of the critical driver (reverse stress) and, for material decisions, a Monte Carlo with P(NPV < 0).
7. **Model hygiene.** Check sign conventions, nominal versus real consistency, timing (mid-year?), units (thousands versus units), tax on losses, double-counting of working capital, and circularity.
8. **Economic reasoning.** Explain *why* value is created (ROIC versus WACC, competitive advantage, operating leverage), not just the output.
9. **Alternative interpretations.** Say what else could explain the numbers, and what evidence would change your recommendation.
10. **Independent review.** For material decisions, recommend that the Chief of Staff obtain an independent review: the CRO, using `cro-toolkit` `independent-review.md`.
