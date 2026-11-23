# Capital budgeting and investment feasibility

## Decision rules

| Rule | Use | Pitfalls |
|---|---|---|
| **NPV** | The primary rule: accept if > 0. For mutually exclusive projects, choose the highest NPV | The discount rate must reflect the project's risk |
| **IRR** | A communication metric | Multiple IRRs when cash flows change sign more than once. Scale and timing conflicts between mutually exclusive projects. Implicitly assumes reinvestment at the IRR |
| **MIRR** | Fixes IRR's reinvestment assumption (finance at Kd, reinvest at WACC) | Still a rate, so it ignores scale |
| **Payback / discounted payback** | Liquidity and risk screen | Ignores cash flows after payback |
| **PI** | Capital rationing: rank by NPV per riyal invested | Not for mutually exclusive choices with no rationing |
| **EAA** | Unequal lives, when projects can be repeated | Assumes replacement at the same terms |

- `compare_projects` reports all of these, the **crossover rate** (the IRR of the incremental cash flows), and flags NPV/IRR ranking conflicts and unequal lives.
- `irr` returns **all** roots and warns when there are several sign changes.

## Building project cash flows (`project` model or a custom script)

- **Incremental and after-tax only:**
  - Include opportunity costs (for example, owned premises that could be rented out) and cannibalisation.
  - Exclude sunk costs and allocated overheads that don't change.
  - Exclude financing flows; the discount rate handles financing.
- **Working capital:** the build-up is an outflow and is recovered at the end. **Capex** goes at t=0 (or on its schedule). **Depreciation** matters only through the tax shield.
- **Terminal and salvage value:** after-tax salvage = `S − (S − book)·t`. For going concerns, use a terminal value with stated growth.
- **Ramp-up:** new ventures rarely reach steady state in year 1. Use `ramp=[0.4, 0.7, 0.9, 1, 1]`, and justify it.
- **Inflation:** keep flows and rate both nominal, or both real.
- **Tax on losses:** the `project` model assumes the losses shield other profits. For a stand-alone start-up, set the tax shield to zero (tax_rate=0 in loss years), or model NOLs with `three_statement`.

## Investment feasibility report structure (what the CEO needs)

1. Decision and options, including "don't invest" and "smaller or staged".
2. Required inputs (provided versus missing) and the assumption table.
3. Base-case NPV, IRR, MIRR, payback and peak funding need. Accounting profit versus cash flow.
4. Tornado of the top drivers, plus the break-even value of the critical driver and its headroom versus the base (`breakeven_input`).
5. Scenarios with probabilities and the expected NPV. Monte Carlo P(NPV<0) and p5/p95 when material.
6. Economic logic: where does the excess return come from, and is it defensible?
7. Recommendation: invest / don't / invest with conditions (staging, kill criteria, financing structure).
