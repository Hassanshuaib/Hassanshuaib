# CRO independent review: CFO Jeddah expansion analysis (2026-11-23)

**Reviewed:** `2026-11-20-cfo-expansion.md` (memo) and `expansion-model.xlsx` (formulas inspected with openpyxl and recalculated in LibreOffice). Fictional test project, SAR.
**Verdict: the analysis does NOT hold. It is not fit to base an approval on.** This is a verdict on the analysis, not on the project: the project may still be worth doing, but the numbers presented cannot show that. **Recommendation: do not proceed yet.** Re-decide once the CFO has fixed the items in section 7.

## 1. Recompute (boardcalc `npv`, `irr`, `mirr`, `payback`, `recalc_compare`)
| Figure | CFO memo | CRO recompute | Status |
|---|---|---|---|
| Year-5 cash flow (Y0–Y5 flows as memo) | 3,315,380 | 3,315,380 | Verified |
| Terminal value (Gordon, g 8%, r 11%) | 119,353,669 | 119,353,669 | Verified (formula) |
| NPV @11%, Y0 at t=0 | **80,715,753** | **70,187,612** | **Differs, by −10.5m (−13%)** |
| NPV as the spreadsheet computes it (B12) | n/a | 62,927,846 | **Differs from the memo by −17.8m** |
| IRR (with TV) | **34%** | **95.5%** (MIRR 86%) | **Differs** |
| IRR (without TV, 5-year life) | not given | **7.0% (< 11% hurdle)** | New |
| NPV without TV | not given | **−642,982** | New |
| PV of TV as % of NPV | not given | **101%** | New |
| TV / Y5 EBITDA (implied multiple) | not given | **36.0x** | New |
| Payback (no TV) | not given | 4.5 years | New |

- **Could not reproduce 80.7m or 34%.** I tested several variants: no refit gives 72.0m, TV discounted 4 years gives 78.0m, no t0 capex gives 75.2m, and discounting at 8% gives 81.1m. None matches. The memo's headline numbers have no traceable source.
- The flows have 3 sign changes (Y3 is negative). The calculator warns that IRR is not a reliable decision rule here. Use NPV/MIRR.
- The spreadsheet's B12 result, recalculated in LibreOffice, matches my independent replication of its formulas exactly (max rel. error 0.0). The workbook is internally as I describe it below.

## 2. Spreadsheet findings (formulas, not values)
| ID | Cell | Finding | Effect |
|---|---|---|---|
| X1 | B12 `=NPV(0.11,B9:G9)` | Excel NPV() discounts the t=0 capex by one period. It should be `=B9+NPV(0.11,C9:G9)` | NPV understated by about 6.9m (62.9m vs 69.8m) |
| X2 | G5 `3300000` | A hardcode inside a formula row. The formula would give 3,315,380 | Y5 cash flow −15k, TV −0.55m. The memo uses the formula value, so the memo and the model disagree |
| X3 | B11 `=SUM(C4:F4)` | Labelled "Total 5-yr revenue" but sums only Y1–Y4 | Shows 22.8m vs 36.1m |
| X4 | Rows 4–8 | Growth (1.45), margin (0.25), WACC (0.11) and g (0.08) are hardcoded in every formula. There is no inputs block | Sensitivities can't be run and errors are easy to make |
| X5 | Whole sheet | No tax, debt, interest, NWC or maintenance-capex rows | Contradicts the memo's "FCFE after debt service" |
| X6 | File | No cached values: the file has never been calculated and saved in Excel | The CFO's 80.7m cannot have come from this file as it stands |

**Three different NPVs exist:** memo 80.7m, workbook 62.9m, correct arithmetic on the memo's own flows 70.2m.

## 3. Methodology review
- **Cash-flow definition vs discount rate (Inconsistency, Critical).** The memo calls the flows FCFE after interest and repayment of a SAR 3.0m loan. But each flow is just EBITDA − capex. That is a pre-tax, unlevered flow: there is no interest, no principal, and t0 shows the full 5.0m rather than 2.0m of equity. FCFE must be discounted at the cost of equity (Re > WACC), not WACC. Pick one consistent basis: FCFF at WACC with no debt flows, or true FCFE at Re.
- **Terminal value (Judgement, Critical).** g = 8% in perpetuity leaves only a 3-point spread to r. TV is 101% of NPV and implies 36x Y5 EBITDA. The explicit five years destroy value (NPV −0.64m), so the whole case is the perpetuity. A perpetual nominal growth rate above plausible long-run economy growth is unsupported. The CFO must justify it or use a long-run rate and cross-check it against an exit multiple.
- **Year-3 refit (Inconsistency, Major).** It is correctly deducted in Y3. But the TV capitalises Y5, a year with zero capex, forever. A kitchen that needs a 2.5m refit after 3 years will need another one. A normalised TV flow should deduct maintenance capex (CRO A2: 2.5m every 3 years ≈ 0.83m a year), which cuts NPV by 17.8m.
- **Tax (Major).** 0% with no basis. Zakat or corporate income tax may apply, depending on ownership. An illustrative 20% tax on EBIT cuts NPV by 12.9m. *Regulatory: zakat/CIT applicability and base must be confirmed by a licensed Saudi tax adviser (ZATCA rules).*
- **Working capital (Minor).** "Not material" is asserted without evidence. It is plausibly small for F&B, but untested. At an illustrative 5% of revenue it costs about 1.6m.
- **Operating profile (Major).** 25% EBITDA margin from day 1, with no ramp-up, pre-opening costs or start-up losses.
- **Debt (Major).** The loan appears in the text only. There is no debt schedule, no covenant check and no liquidity view. Y3 is cash-negative (−0.92m), and Y3 is exactly when debt service and the refit coincide.

## 4. Assumption review: evidence vs assertion
| Assumption (CFO) | Evidence offered | Assessment |
|---|---|---|
| Y1 revenue 3.0m | None | Unsupported. Needs a site-level build-up (covers × spend × days) |
| Growth 45% a year × 5 (4.4x in 4 years) | "Management is confident" | **Assertion.** No market, capacity or comparable-site data. A single site's capacity to deliver 13.3m is unchecked (COO) |
| EBITDA margin 25% flat from Y1 | None | Unsupported. No benchmark, ramp or cost build-up |
| Tax 0% | None | Unsupported. Regulatory flag |
| WACC 11% | None (no CAPM/WACC build-up) | Unsupported, and the wrong rate for FCFE |
| TV g 8% perpetual | None | Unsupported. Value-critical |
| NWC immaterial | Assertion | Low impact |
| "Very high confidence" | No sensitivity or downside shown | Not justified |

**CRO assumptions (illustrative, for stress only):** A1 TV g = 3% (long-run nominal proxy, judgement). A2 the refit recurs every 3 years, 0.83m a year in the TV. A3 Re = 13% if the flows are FCFE (judgement, no CAPM inputs available). A4 tax 20% on EBIT, with straight-line depreciation over 10 years (illustrative only, not a tax position). A5 Monte Carlo PERT ranges: growth 5/25/45%, margin 12/20/27%, g 1/3/5%, r 11/13/16%. A6 NWC 5% of revenue. **A1–A3 are critical.**

## 5. Sensitivity and stress (boardcalc `tornado`, `breakeven_input`, `stress`, `montecarlo`, custom model)
**Tornado on the CFO base (NPV 70.2m):** r 11→16%: 70.2 → 20.0m. g 8→2%: 70.2 → 21.7m. Margin 30→15%: 85.6 → 39.4m. Growth 45→15%: 70.2 → 24.8m. Refit recurring: −17.8m. Tax 20%: −12.9m.

**Reverse stress (NPV = 0):**
- *On the CFO base:* the break-evens look huge (growth −25% a year, margin 2.2%, r 35.6%). That is only because the 8% perpetuity dominates. This is a symptom of the TV problem, not real headroom.
- *Without TV:* NPV is already negative. Break-even needs growth of 50.7% a year, above the CFO's 45%.
- *CRO-adjusted case (A1 + A2 + A3; NPV +13.0m, still 107% from TV):* NPV = 0 at **growth 16.9% a year** (vs 45%) or **margin 11.7%** (vs 25%).

**Combined stresses (cumulative, illustrative):**
| Scenario | NPV (SAR) |
|---|---|
| CFO base, arithmetic corrected | 70.2m |
| A: g 3% + recurring refit | 18.3m |
| B: A + r 13% | 13.0m |
| C: B + tax 20% (A4) | 9.0m |
| D: B + growth 25%, margin 20% | 0.08m (≈ break-even) |
| E: B + growth 15%, margin 18%, tax 20% | **−4.3m** |
| F: B + NWC 5% | 11.4m |

**Monte Carlo** (10,000 runs, seed 42, A5 ranges, adjusted case): mean +0.2m, P50 −0.2m, **P(NPV < 0) = 53%**, 5% expected shortfall −4.8m. These are illustrative ranges. The point is that once growth and margin are uncertain, the outcome is roughly a coin-flip.

## 6. Pre-mortem and risk register (boardcalc `risk_register`)
Failure stories, each with its early-warning signal:
1. **Demand ramps at 15–20%, not 45%.** Signal: Y1 monthly covers/revenue below plan for 2 consecutive quarters.
2. **Margins sit below 20% through the ramp.** Signal: month-6 EBITDA margin below 18%.
3. **The Y3 cash squeeze.** Debt service, the refit and lower-than-plan EBITDA all hit at once. Signal: forecast Y3 cash flow below debt service.
4. **Tax/zakat assessment not budgeted.** Signal: adviser confirms a liability.

| Risk | L | I | Rating | Mitigation | Owner |
|---|---|---|---|---|---|
| Approval on non-reproducible NPV/IRR | H | H | CRITICAL | CFO rebuilds a traceable model; CRO re-verifies | CFO |
| Value rests on 8% perpetual TV (101% of NPV) | H | H | CRITICAL | g at long-run rate, exit-multiple cross-check, show NPV ex-TV | CFO |
| 45% growth not achieved | H | H | CRITICAL | Bottom-up demand and capacity evidence; staged commitment | CEO/COO/CMO |
| Tax/zakat omitted | H | M | SIGNIFICANT | Licensed adviser opinion; model it | CFO |
| Recurring refit omitted from TV | H | M | SIGNIFICANT | Maintenance-capex schedule | COO/CFO |
| Debt service not modelled (liquidity) | M | M | SIGNIFICANT | Debt schedule, covenant headroom, Y3 cash plan | CFO |
| NWC higher than assumed | L | L | WATCH | Monitor | CFO |

**Kill criteria (if approved later):** after month 9, run-rate revenue more than 25% below plan, or EBITDA margin below 15%. Either one means a halt or rework before any further capital.

## 7. Findings ranked, and what the CFO must fix before the CEO decides
**Critical:** C1 the headline NPV (80.7m) and IRR (34%) cannot be reproduced, and memo, workbook and arithmetic give three different NPVs. C2 the value is entirely terminal (101% of NPV, 8% perpetual, 36x EBITDA), and NPV without TV is negative (IRR ex-TV 7% < 11%). C3 the flows are labelled FCFE but no debt is modelled, and they are discounted at WACC. C4 the 45% a year growth is an assertion.
**Major:** M1 tax 0% (regulatory flag). M2 the refit is treated as a one-off, with no maintenance capex in the TV. M3 the NPV() t0 error (X1) and the G5 hardcode (X2). M4 a flat 25% margin from Y1. M5 IRR is quoted despite 3 sign changes. M6 no sensitivity, yet "very high confidence".
**Minor:** m1 B11 excludes Y5. m2 drivers are hardcoded and there is no inputs sheet or cached values. m3 NWC is asserted. m4 a TV rounding difference of 11 SAR (immaterial).

**The CFO must provide:**
1. A rebuilt model with an inputs sheet and a reconciliation of the memo to the model.
2. One consistent cash-flow basis: FCFF at a documented WACC, or FCFE at Re with a full loan schedule (rate, tenor, repayment, covenants).
3. A TV at long-run g with an exit-multiple cross-check, NPV shown with and without TV, and the TV share.
4. A bottom-up Y1 revenue and growth case with capacity limits and a margin ramp, including pre-opening costs.
5. A tax/zakat treatment confirmed by an adviser.
6. A maintenance/refit capex schedule.
7. Downside/base/upside cases with break-even growth and margin.
8. Peak funding and a Y3 liquidity view.

**I would support approval if:** the rebuilt model shows positive NPV in the base case under consistent definitions, and demand is evidenced well enough to keep break-even growth (about 17% on the adjusted case) comfortably below a credible base. Better still, commit in stages, with the kill criteria above.

Checks: NPV/IRR/MIRR/payback recomputed independently with boardcalc from the memo inputs (not the CFO's file). Workbook formulas read with openpyxl and recalculated with LibreOffice via `recalc_compare` (6 cells, 0.0 error vs my replication). Alternative reconstructions of 80.7m/34% tested and none reproduced. Tornado, reverse stress, 6 combined stresses and a 10k Monte Carlo run in boardcalc. Script: `board/analyses/calc/2026-11-23-cro-review-expansion.py`. Not verified: any input's real-world basis (none provided). The tax position needs a professional.
