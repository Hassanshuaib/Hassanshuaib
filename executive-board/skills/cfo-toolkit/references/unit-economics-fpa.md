# Unit economics, pricing, break-even, FP&A

## Unit economics

- **Contribution margin** = price − variable cost per unit (include payment fees, delivery, packaging, commissions, refunds). Treat semi-variable costs explicitly.
- **Break-even** (`breakeven`): units = fixed / CM. Also report the margin of safety and the degree of operating leverage. Use cash break-even (excluding D&A) when funding is the question.
- **Subscription and customer economics** (`ltv`, `cohort_ltv`):
  - LTV on a **gross-margin** basis, discounted, with a horizon cap for young businesses. Prefer observed cohort retention over the constant-churn formula.
  - Report LTV:CAC (≥ 3 is a common heuristic, not a law) and **CAC payback** in months.
  - Fully loaded CAC includes salaries, tools and agency costs, not just ad spend.
- **Pricing maths:**
  - A price change of x% needs a volume change of `CM/(CM') − 1` to keep contribution flat (`price_change_breakeven`).
  - For subscription repricing, use `subscription_price_change`: the break-even immediate loss and the break-even churn.
  - Elasticity estimates need evidence (tests, history).

## FP&A

- **Budget:** driver-based (volume × price, headcount × cost per FTE, capacity-driven opex). Tie it to the three-statement model so that the cash budget follows the P&L budget.
- **Rolling forecast:** 12–18 months, updated monthly or quarterly. Track forecast accuracy (MAPE) to calibrate.
- **Variance analysis** (`variance_analysis`; for narrative and waterfalls, `finance:variance-analysis`): split into price, volume/mix and cost rate/efficiency. The components must sum to the total variance. Explain root causes, not just labels.
- **Dashboard KPIs (a small set):**
  - revenue versus budget and growth
  - gross margin
  - EBITDA
  - cash and runway
  - CCC
  - unit-economics KPIs (CAC, LTV:CAC, churn)
  - capex versus plan
  - covenant headroom
  Each KPI has an owner, a target, a threshold and a data source. Use the `dataviz` skill for charts.
