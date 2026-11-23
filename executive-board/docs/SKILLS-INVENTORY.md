# Skills Inventory: AI Executive Board (v1.1, 2026-11-23)

Legend:
- 🆕 **created** (custom, in this repo)
- 📦 **installed third-party**: vendored unmodified, Apache-2.0, in the optional `board-finance-pack` plugin
- ♻️ **reused**: already on your Claude account; synced, loaded when available
- ⛔ **not used**, with the reason

## 1. Audit findings (before the upgrade)

| Finding | Impact | Fix |
|---|---|---|
| No executive had the `Skill` tool | Agents could not use **any** skill | `Skill` was added to all six specialists |
| No calculation engine; each agent wrote ad-hoc scripts | Unverified arithmetic, and scripts lost in scratch folders | 🆕 `scripts/boardcalc.py`, plus 36 independent tests |
| Methods lived only in short agent prompts | Generic analysis, no quality gates | 🆕 one toolkit skill per executive, preloaded into its agent |
| Account plugins (Daloopa, Finance, Small-Business, BlackRock) unused by the board | Some overlap and some fit | Reused where they fit (below). Daloopa ⛔: listed companies only, and its data connector failed to connect here |

## 2. Per-agent inventory

| Agent | Preloaded | Created for it 🆕 | Third-party 📦 / reused ♻️ (invoked on demand) | Calculator functions |
|---|---|---|---|---|
| **Chief of Staff** | the playbook (agent) | routing rules for financial and technical questions; independent-review trigger | `board`, `board-council`, `board-memory`, `board-report` | uses `boardcalc` for any arithmetic |
| **CFO** | `cfo-toolkit` | `cfo-toolkit` index + 9 references: corporate-finance, valuation, capital-budgeting, three-statement-fsa, risk-modeling, unit-economics-fpa, pe-ma, model-review, sources | 📦 3-statement-model, lbo-model, merger-model, returns-analysis, dd-checklist, audit-xls · ♻️ finance:variance-analysis, finance:reconciliation, finance:financial-statements, anthropic-skills:xlsx | npv, irr (multi-root), mirr, payback, compare_projects, eaa, capm, (un/re)lever_beta, wacc, roic_eva, value_driver, dcf (dual TV + cross-check), dcf_grid, multiples_valuation, ratios, altman_z, three_statement (+xlsx with live formulas + LibreOffice recalc check), project, tornado, grid, scenarios, montecarlo, breakeven_input, stress, breakeven, ltv, variance_analysis, lbo, accretion_dilution, covenant_headroom |
| **COO** | `coo-toolkit` | index + capacity-staffing, process-quality, supply-chain, execution-kpis | ♻️ small-business:inventory-planner (needs a store connector) | erlang_c, staff_for_service_level, littles_law, capacity, takt_time, learning_curve, oee, dpmo_sigma, control_limits, fmea, eoq, safety_stock, pert_estimate |
| **CMO** | `cmo-toolkit` | index + research-segmentation, pricing, growth-metrics, positioning | 📦 competitive-analysis · ♻️ anthropic-skills:deep-research | funnel, ltv, cohort_ltv, marketing_roi, ab_test, ab_sample_size, van_westendorp, gabor_granger, elasticity, price_change_breakeven, subscription_price_change |
| **CSO** | `cso-toolkit` | index + frameworks, market-sizing, options-entry | 📦 competitive-analysis · ♻️ anthropic-skills:deep-research | market_sizing, bass_diffusion, hhi, decision_matrix (rank-flip robustness), expected_value, scenarios, cagr |
| **CRO** | `cro-toolkit` | index + risk-methods, quant-risk, regulatory, **independent-review protocol** | 📦 audit-xls · ♻️ small-business:contract-review | risk_register, fmea, pert_estimate, montecarlo, breakeven_input, stress, var_cvar, covenant_headroom, altman_z |
| **Secretary** | — | — (`board-report` already existed) | ♻️ anthropic-skills:docx / xlsx / pdf / pptx (now reachable: `Skill` tool added) | — |

## 3. Third-party research and decisions

| Source | Inspected | Decision |
|---|---|---|
| anthropics/financial-services-plugins (Apache-2.0, commit 3e32c22) | Manifests, hooks (empty), `.mcp.json` (12 data-vendor servers in `financial-analysis`), scripts (no network or exec), skill quality | 📦 **7 skills vendored unmodified, with your approval**. The full plugins were **not** installed, to avoid 12 paid-data connectors and about 30 extra always-on skills |
| anthropics/knowledge-work-plugins: operations, marketing | Operations skills are 39–113 lines; the plugins add 19 connectors (Slack, Notion, …) | ⛔ Not installed. Thin coverage, and our toolkits are deeper. Install it yourself if you use those connectors |
| anthropics/skills (xlsx, docx, pdf, pptx) | Already on your account as `anthropic-skills:*` | ♻️ Reused, not duplicated |
| aiwithremy/claude-skills-llm-council | No license (reviewed in v1.0) | ⛔ Method re-implemented in `board-council` |
| Daloopa plugin (on your account) | Ticker-based, needs the Daloopa connector | ⛔ For listed companies only; the connector failed to connect in this environment |

## 4. Token budget (from `claude plugin details`)

| Component | Always-on (every session) | On invoke |
|---|---|---|
| executive-board v1.1 (7 agents, 9 skills) | ~1.7k tokens (v1.0: ~1.3k) | Toolkit index ~0.6–1.7k, preloaded only into its own agent; each reference 0.5–1.5k, read only when needed |
| board-finance-pack (optional) | ~1.1k tokens | 1–15k per vendored skill, only when invoked |

## 5. Still missing (honest gaps)

1. **Live financial and market data.** There are no data subscriptions (FactSet, S&P, Daloopa, Bloomberg). Betas, ERPs, multiples and precedents must be researched online and cited, or supplied by you.
2. **Professional verification.** Tax, zakat, legal and licensing points are flagged, never certified. There is no human-expert review.
3. **Advanced statistics.** There is no scipy or statsmodels, so no regression, econometrics or conjoint estimation. The A/B test, sample size and Monte Carlo functions are covered.
4. **Excel recalculation on your machine.** `recalc_compare` needs LibreOffice. Without it, the Excel files still work, but the automatic formula-versus-Python check is skipped.
5. **Model diversity.** All executives run on the same model, so the independent review is a fresh-context check, not an independent mind.
6. **Operations and CRM data connectors** (POS, inventory, ads) are not connected. The COO and CMO work from the numbers you give them.
