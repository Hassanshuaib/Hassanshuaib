# CFO Analysis: DCF valuation of Najd Logistics (FICTIONAL, illustrative), SAR
Date: 2026-11-23 | Author: CFO | Model: `board/analyses/calc/2026-11-23-cfo-najd-dcf.py` (re-runnable)

## 1. Decision and question
What is Najd Logistics worth per share on an FCFF DCF basis, and how do the Gordon and exit-multiple terminal methods compare? Currency is SAR. This is an illustrative exercise on a fictional company.

## 2. Inputs and assumptions
**User inputs (CEO), all of them; no market data was looked up or substituted.** Y0 revenue 50.0m; growth 12/10/8/6/5%; EBIT margin 18%; tax 20%; D&A 4% and capex 6% of revenue; NWC 15% of same-year revenue; rf 5.0%; peer βL 1.10 at D/E 0.30; target D/E 0.25; MRP 5.5%; CRP 1.0%; pre-tax Kd 7.0%; g 3%; exit 9.0x Y5 EBITDA; end-year discounting; net debt 20.0m; 10.0m shares.
**My assumptions:**
- A1: Net debt is taken at book value and assumed equal to its market value as at the valuation date. There are no minorities, leases or other debt-like items. Basis: none were provided.
- A2: The 20% tax rate is the marginal rate on all EBIT. Zakat versus CIT is not modelled and needs confirmation from a tax adviser.
- A3: Y5 reinvestment carries into Y6 unchanged, because FCFF6 = FCFF5 × (1+g) per the brief.

## 3. Cost of capital
| Item | Formula | Value |
|---|---|---|
| Unlevered β | 1.10 / (1 + 0.8 × 0.30) | **0.8871** |
| Relevered β | 0.8871 × (1 + 0.8 × 0.25) | **1.0645** |
| Ke | 5.0% + 1.0645 × 5.5% + 1.0% | **11.855%** |
| Kd after tax | 7.0% × (1 − 20%) | 5.60% |
| WACC | 0.80 × 11.855% + 0.20 × 5.60% | **10.604%** |

## 4. Explicit forecast (SAR m; FCFF = NOPAT + D&A − Capex − ΔNWC; DF = 1.10604^−t)
| Year | Revenue | EBIT | NOPAT | D&A | Capex | ΔNWC | FCFF | DF | PV |
|---|---|---|---|---|---|---|---|---|---|
| Y1 | 56.000 | 10.080 | 8.064 | 2.240 | 3.360 | 0.900 | 6.044 | 0.9041 | 5.465 |
| Y2 | 61.600 | 11.088 | 8.870 | 2.464 | 3.696 | 0.840 | 6.798 | 0.8174 | 5.557 |
| Y3 | 66.528 | 11.975 | 9.580 | 2.661 | 3.992 | 0.739 | 7.510 | 0.7391 | 5.551 |
| Y4 | 70.520 | 12.694 | 10.155 | 2.821 | 4.231 | 0.599 | 8.146 | 0.6682 | 5.443 |
| Y5 | 74.046 | 13.328 | 10.663 | 2.962 | 4.443 | 0.529 | 8.653 | 0.6042 | 5.228 |
PV of explicit FCFF = **27.243m**. Y5 EBITDA = 16.290m. FCFF6 = 8.912m.
Cash versus profit: FCFF runs at 75–81% of NOPAT. The gap is net capex (2% of revenue) plus working capital (15% of incremental revenue). FCFF is positive every year, so there is no funding need inside the model.

## 5. Terminal value and valuation (SAR m, except per share)
| Method | TV | PV of TV | EV | Equity (EV − 20.0) | Per share | TV % EV |
|---|---|---|---|---|---|---|
| (a) Gordon, g = 3% | 117.208 | 70.812 | **98.055** | 78.055 | **SAR 7.81** | 72.2% |
| (b) Exit, 9.0x EBITDA | 146.610 | 88.575 | **115.819** | 95.819 | **SAR 9.58** | 76.5% |

**Cross-implied figures:**
- The Gordon TV implies an exit multiple of 117.208 / 16.290 = **7.20x** Y5 EBITDA.
- The exit TV implies a perpetual growth rate of (146.610 × 10.604% − 8.653) / (146.610 + 8.653) = **4.44%**.

The EV gap is +18.1% on a Gordon base (16.6% on a midpoint base), so it sits inside the 20% reconciliation threshold. The equity gap is wider, at +22.8%, because the 20m of net debt magnifies it.

## 6. Sensitivity: Gordon value per share (SAR)
| WACC \ g | 2% | 3% | 4% |
|---|---|---|---|
| 9.60% | 8.14 | 9.33 | 10.95 |
| **10.60%** | 6.92 | **7.81** | 8.96 |
| 11.60% | 5.96 | 6.64 | 7.49 |

Per share by exit multiple: 7x = 7.61; 8x = 8.60; 9x = 9.58; 10x = 10.57; 11x = 11.55.
Per share by EBIT margin (Gordon / Exit): 15% = 5.77 / 7.79; 18% = 7.81 / 9.58; 21% = 9.84 / 11.37.
The drivers that matter most are WACC, g or the exit multiple, and EBIT margin. Each ±1 point of WACC moves value by about 15–19%. Each ±3 points of margin moves it by about 26% (Gordon).

## 7. Reconciliation of the two methods
- **Why they differ.** A 9.0x multiple prices the business as if it grows at 4.44% forever. The Gordon case assumes 3%. Put the other way round, 3% growth at a 10.6% WACC is worth only 7.20x EBITDA. The remaining gap is the difference between those two growth rates, capitalised over a 6–7.6% spread to WACC.
- **Economic test.** Y5 reinvests 18.8% of NOPAT. At g = 3% that implies a return on new invested capital (RONIC) of 15.9%. At 4.44% it implies 23.6%, which is more than twice WACC in perpetuity. That is hard to justify for asset-heavy logistics without a durable moat.
- **Which is more defensible.** The Gordon case. It is built from the company's own cash flows and cost of capital, and 3% sits within the nominal long-run ceiling (gate: g ≤ 3–4%). The 9.0x multiple is a CEO input with no stated peer set or date. Multiples also embed current market sentiment and control or liquidity effects that may not apply here. Its implied 4.44% g breaches the gate.
- **What closes the gap.** Either use an exit multiple of **7.2x**, or a Gordon g of **4.44%**. A WACC reduction of roughly 1 point at g = 3% (per share 9.33 at 9.60% WACC) also gets close.
- **Conservatism note (A3).** FCFF6 = FCFF5 × 1.03 carries the reinvestment Y5 needed for 5% growth into a 3% world. That understates FCFF6 slightly, so the Gordon value is mildly conservative. A value-driver TV, NOPAT × (1 − g/RONIC), would lift it. This is a refinement and does not change the conclusion.
- **Range.** Use **SAR 7.8–9.6 per share**, with the Gordon value of 7.81 as the anchor. The plausible WACC/g band from the grid is 6.6–9.3.

## 8. Verdict
A fair-value anchor of **SAR 7.81 per share** (equity 78.1m), with 9.58 as the top of the range. Do not underwrite a price above about SAR 9.6 unless:
- (i) peer evidence supports 9x as a sustainable multiple, not a cyclical one, or
- (ii) management can show RONIC of about 20% or more alongside 4–4.5% long-run growth.

Kill criteria for any buy-side use: EBIT margin below 15% (value falls to SAR 5.8), or WACC above 11.6% (SAR 6.6).

## 9. Limitations
- TV is 72–77% of EV, so the valuation rests on the terminal assumption.
- The figures are illustrative, built on fictional inputs.
- The 9.0x multiple and the beta have no market source.
- Tax and zakat treatment needs professional confirmation.
- For a real transaction, the CRO should run an independent review.

**Checks:** 11 of 11 integrity checks passed in the script:
- The manual β, Ke, WACC and per-share values (both methods) match boardcalc's `unlever_beta`, `relever_beta`, `capm`, `wacc` and `dcf` to 1e-9.
- The implied g and implied multiple match boardcalc.
- Round trips pass: Gordon at 4.44% reproduces the exit TV, and the exit multiple at 7.20x reproduces the Gordon TV.
- Cumulative ΔNWC equals NWC5 − NWC0.

Quality gates run: 1 (tagging), 2 (verified arithmetic), 3 (cash versus profit), 4 (reality check: TV share 72–77% flagged, implied g 4.44% flagged), 5 (two methods reconciled), 7 (end-year timing, nominal consistency, sign conventions), 8 (RONIC test). Gate 6 was partial: a sensitivity grid only, with no Monte Carlo, which is not material for an illustrative exercise.
