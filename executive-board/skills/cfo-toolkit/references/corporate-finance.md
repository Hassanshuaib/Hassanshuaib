# Corporate finance: cost of capital, capital structure, value creation

## Cost of equity (CAPM and build-up)

`Re = rf + β·MRP (+ size premium + country risk premium + company-specific premium)`
- **rf:** use a long-term government bond yield in the **same currency** as the cash flows. For SAR flows, use a KSA government sukuk/bond yield. Alternatively use the USD 10-year yield plus a country default spread (the SAR is pegged to the USD, but sovereign risk differs). Cite the date and source. Never mix a USD rf with SAR inflation assumptions.
- **β:** for a private firm, take peer betas, unlever them (Hamada `Bu = BL / (1 + (1−t)·D/E)`), take the median, then relever at the target D/E. Prefer 2–5 years of weekly or monthly betas, and Blume-adjust if needed (`0.67·β + 0.33`).
- **MRP:** a mature-market ERP of about 4–6% (Damodaran's implied ERP is updated monthly; cite the value and date). Add a CRP for emerging markets (Damodaran publishes CRPs by country).
- **Small or private premia** are judgement calls. Show them separately and run a sensitivity. They are often the largest single uncertainty.

## Cost of debt and WACC

- **Pre-tax Kd:** the marginal borrowing rate (the current offer, or rf plus a credit spread for the synthetic rating from interest coverage). The coupon on old debt is not the cost of debt. Post-tax: `Kd·(1−t)`, and only if there is taxable profit to shield.
- **WACC weights:** use **target market-value** weights, not book values. Leases count as debt under IFRS 16 if the cash flows exclude lease payments; be consistent.
- **Islamic financing (murabaha, ijara):** treat the profit rate as the cost of debt economically.
- **Consistency rule:** FCFF goes with WACC, FCFE with Re. Nominal flows go with a nominal rate, real with real. The currency of the flows must match the currency of the rate.

## Capital structure

- **Trade-off theory:** the tax shield versus expected distress costs. Plot WACC against D/E. Beyond the optimum, Kd and β rise faster.
- **Pecking order:** internal funds, then debt, then equity. Under asymmetric information, an equity issue signals overvaluation.
- **MM intuition:** in perfect markets, leverage doesn't change firm value. Value comes from taxes, distress costs, agency effects and signalling. Always ask which of these applies.
- **Practical tests:** net debt/EBITDA, interest cover (EBIT/interest), DSCR, covenant headroom (`covenant_headroom`), and refinancing walls.

## Value creation

- `ROIC = NOPAT / invested capital` (invested capital = operating NWC + net PP&E + other operating assets, excluding cash).
- `EVA = (ROIC − WACC) × IC` (`roic_eva`).
- **Value-driver formula:** `V = NOPAT₁·(1 − g/ROIC)/(WACC − g)` (`value_driver`). Growth creates value **only if ROIC > WACC**. At ROIC = WACC, growth is value-neutral; below it, growth destroys value.
- **Common errors:** using EBITDA as "return"; including excess cash in IC; mixing pre-tax and post-tax figures.

## Capital allocation and risk-adjusted returns

- Rank uses of cash by **risk-adjusted NPV per riyal of scarce capital** (profitability index under capital rationing). Uses include organic projects, M&A, debt paydown, buybacks/dividends and holding cash.
- **Adjust the discount rate for project risk, not company average risk.** Using the company WACC for a riskier project overinvests; using it for a safer one underinvests.
- **Risk-adjusted metrics:** use the expected NPV across scenarios rather than the base NPV. Report P(NPV<0) from Monte Carlo, and RAROC (`expected return / economic capital`) for financial businesses.
- **Hurdle rates:** state the WACC, plus any strategic or illiquidity premium explicitly. Beware hurdle rates set far above WACC; they kill good projects.
- **Real options:** the option to delay, expand, abandon or stage. Staging investment (tranches with gates) has option value. Value it qualitatively, or with a decision tree (`expected_value`).
