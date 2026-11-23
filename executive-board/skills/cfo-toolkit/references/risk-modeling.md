# Sensitivity, scenarios, Monte Carlo, stress testing

| Tool | Answers | Function |
|---|---|---|
| Tornado (one at a time) | Which drivers matter most? | `tornado` (sorted by swing) |
| Two-way grid | How do two drivers interact? | `grid`; `dcf_grid` for WACC × g |
| Scenarios | Coherent stories (base/downside/upside) and expected value | `scenarios` with `probabilities` |
| Monte Carlo | Distribution of outcomes and P(failure) | `montecarlo` |
| Reverse stress | How bad must X get to break the plan? | `breakeven_input` |
| Combined stress | Several shocks at once (e.g. a recession) | `stress` |
| Covenant headroom | EBITDA decline before a breach | `covenant_headroom` |

## Rules

- **Scenarios must be internally coherent.** A downside with low volume also brings lower prices, slower collections and higher unit costs from fixed-cost absorption. Never flex only one variable and call it a scenario.
- **Ranges come from evidence:** historical volatility, peer dispersion, market data, or expert three-point estimates (PERT). State the basis for each range.
- **Monte Carlo:**
  - Pick distributions deliberately: triangular or PERT for expert estimates, lognormal for positive skewed quantities, normal only for symmetric quantities.
  - Model **correlations** (for example price and volume): ignoring them understates or overstates risk. `montecarlo` supports pairwise correlation for normal inputs. For others, simulate the dependency explicitly in a custom script.
  - Report the seed, n, mean, p5/p50/p95, P(NPV<0) and the expected shortfall. Check the MC standard error.
  - Monte Carlo doesn't add information; it **propagates** your assumptions. Garbage ranges produce garbage distributions.
- **Stress tests** should include at least:
  1. demand shock (−20 to −40% volume)
  2. price/margin squeeze
  3. cost inflation
  4. delay or ramp-up slip (6–12 months)
  5. financing stress (rate +300 bp, refinancing unavailable)
  6. key customer or supplier loss
  For each, report liquidity (minimum cash, revolver need), not just NPV.
- **Reverse stress:** report the break-even value of each critical driver and the **headroom** versus the base. Under 10–15% headroom on a driver with no evidence base means fragile.
