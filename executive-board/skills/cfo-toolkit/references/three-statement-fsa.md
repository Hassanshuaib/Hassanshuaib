# Three-statement modelling, forecasting, financial statement analysis

## Integrated model (`three_statement`, `three_statement_xlsx`)

- **Drivers:** revenue growth (built bottom-up where possible: volume × price), gross margin, opex %, D&A, capex, DSO/DIO/DPO, tax, interest on **opening** balances (avoids circularity), the debt schedule, payout, and a minimum cash level with a revolver plug.
- **Mandatory integrity checks**, reported by the function (all must be about 0):
  - balance sheet balances every year
  - the cash-flow ending cash equals the balance-sheet cash
  - equity roll-forward = opening + NI − dividends
  - PP&E roll-forward = opening + capex − D&A
- **Excel deliverable:** `three_statement_xlsx(path, ...)` writes live formulas (Inputs sheet in blue, Model sheet in black formulas). Verify it with `recalc_compare` (LibreOffice). Tests show it matches the Python model to 1e-9.
- **Templates:** to fill an existing company template, use `board-finance-pack:3-statement-model` if it is installed.

## Forecasting discipline

- Start from the **historical base**: normalise one-offs, and check that revenue × DSO reproduces historical AR.
- **Growth realism:** compare to market growth plus share gain. Cap share gains at what capacity and sales capacity allow. Revenue CAGR above 30% for more than 3 years needs specific evidence.
- **Margin realism:** converge toward peer ranges. Operating leverage is real, but fixed costs step up with scale.
- **Reinvestment:** growth needs capex and NWC. Check the capex/D&A ratio (>1 when growing) and the asset-turnover trend.

## Reconciliation and accounting

- **Profit to cash:** CFO = NI + D&A ± ΔNWC ± other non-cash items. Explain each bridge item.
- **Model to actuals:** tie the opening balances to audited statements, and reconcile any difference before forecasting. For GL-level work, use `finance:reconciliation`.
- **IFRS points to check:** IFRS 15 revenue timing, IFRS 16 leases (EBITDA is inflated and debt increased), IFRS 9 expected credit losses on receivables, capitalised development costs, and end-of-service provisions (KSA).

## Financial statement analysis (`ratios`, `altman_z`)

- **Liquidity:** current, quick and cash ratios; runway (months of cash ÷ net burn).
- **Efficiency:** DSO, DIO, DPO and the **cash conversion cycle** = DSO + DIO − DPO. Translate a CCC change into cash: `ΔCCC/365 × revenue` (roughly).
- **Solvency:** D/E, net debt/EBITDA, interest cover, DSCR, Altman Z'' (private non-manufacturers) as a screening tool only.
- **Profitability:** gross, EBITDA, EBIT and net margins; ROA, ROE with the DuPont split (margin × turnover × leverage), and ROIC.
- **Earnings quality:** CFO/NI well below 1 for a long time, a rising accruals ratio, DSO rising faster than revenue, capitalised costs, and related-party revenue are all red flags.
