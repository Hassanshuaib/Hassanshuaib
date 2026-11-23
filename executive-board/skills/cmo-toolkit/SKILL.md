---
name: cmo-toolkit
description: CMO toolkit: market research, segmentation, pricing research, CAC/LTV, experiments, positioning - methods, verified calculator, quality gates.
---

# CMO Toolkit (index — read only what you need)

**Calculator:** `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/boardcalc.py" <function> '<json>'`. Run `list` for all functions, or add `--doc` for one. In a manual install, use `~/.claude/executive-board/scripts/boardcalc.py`. References are in `${CLAUDE_PLUGIN_ROOT}/skills/cmo-toolkit/references/`.

| Task | Read | boardcalc functions | Optional skills |
|---|---|---|---|
| Market research, segmentation, demand validation | `research-segmentation.md` | `ab_sample_size`, `market_sizing` | `anthropic-skills:deep-research` |
| Pricing strategy and research | `pricing.md` | `van_westendorp`, `gabor_granger`, `elasticity`, `price_change_breakeven`, `subscription_price_change` | — |
| Acquisition, retention, CAC/LTV, ROI, experiments | `growth-metrics.md` | `funnel`, `ltv`, `cohort_ltv`, `marketing_roi`, `ab_test`, `ab_sample_size` | `small-business:growth-pulse` (if connected) |
| Positioning, brand, competition | `positioning.md` | `decision_matrix` | `board-finance-pack:competitive-analysis` |

## Quality gates

1. Separate **observed behaviour** (sales, paid pilots, cohort data) from **stated intent** (surveys, interviews). Stated intent overstates demand. Apply a haircut, and say so.
2. Every benchmark (CAC, conversion, churn, CTR) is cited with its source and context, or marked "assumption". Never quote generic "industry averages" from memory as fact.
3. All funnel, LTV and test-statistics arithmetic is done in boardcalc.
4. Use fully loaded CAC and gross-margin LTV, and show CAC payback. Revenue LTV is not acceptable.
5. Experiments: state the hypothesis, the primary metric, the sample size (computed) and the stopping rule **before** running. Don't call winners on underpowered tests.
6. Attribution humility: last-click inflates the bottom-funnel channels. Use holdouts and incrementality tests when spend is material.
7. Hand the CFO the economics (price, volume ramp, CAC and churn ranges) as explicit, ranged assumptions.
