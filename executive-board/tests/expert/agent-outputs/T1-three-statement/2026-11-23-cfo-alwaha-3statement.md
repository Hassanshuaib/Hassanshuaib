# Al-Waha Foods: integrated three-statement model (CFO), 2026-11-23

**Fictional/illustrative company. All figures in SAR.** Y0 = actuals (opening BS); Y1–Y3 = forecast.
- Workbook (live formulas): `board/analyses/2026-11-23-cfo-alwaha-3statement.xlsx` (sheets Inputs, IS, BS, CF, Debt, Checks)
- Build, recalc and verification script: `board/analyses/calc/2026-11-23-cfo-alwaha-3statement.py`

## Decision question
Al-Waha's plan shows growing profit. Does it generate enough cash to fund growth capex, scheduled debt service and a 25% dividend while keeping SAR 1.5m minimum cash? How much revolver is needed?

## Inputs (all CEO inputs, not facts)
Rev Y0 24.0m; growth 18/12/8%; GM 38%; Opex 22%; D&A 4%; Capex 9/7/5% of revenue; DSO 40 (revenue), DIO 55 and DPO 35 (COGS), 365 days, ending balances; tax 20% x MAX(0,EBT), no loss c/f; term interest 8% and revolver 10%, both on opening balances; min cash 1.5m; term repayment 1.0m/yr; payout 25%.
Opening BS: Cash 2.0m, AR 2.6m, Inv 1.9m, PP&E 9.0m = 15.5m; AP 1.5m, Term debt 6.0m, Equity 8.0m = 15.5m.

## Conventions
- C1. EBITDA = GP − Opex. D&A sits below EBITDA (EBIT = EBITDA − D&A).
- C2. Dividends = 25% x MAX(0, NI), paid in the same year. No dividend is paid in a loss year; none occurs in any case modelled.
- C3. Revolver draw/(repay) = MAX(min cash − cash before revolver, −opening revolver). This is a full cash sweep above the minimum, and the revolver never goes below zero.
- C4. **No circularity, confirmed.** Interest is charged on opening balances, so CFO does not depend on the current-year draw. LibreOffice recalculated without Err:522 (circular reference).
- C5. Scheduled repayment = MIN(1.0m, opening term balance).

## Results (Base)
| SAR | Y1 | Y2 | Y3 |
|---|---:|---:|---:|
| Revenue | 28,320,000 | 31,718,400 | 34,255,872 |
| EBITDA (16.0%) | 4,531,200 | 5,074,944 | 5,480,940 |
| Interest (term + revolver) | 480,000 | 523,063 | 490,017 |
| Net income | 2,334,720 | 2,626,516 | 2,896,550 |
| Increase in NWC | 1,065,666 | 487,880 | 364,284 |
| CFO | 2,401,854 | 3,407,372 | 3,902,501 |
| Capex | 2,548,800 | 2,220,288 | 1,712,794 |
| FCF (CFO − capex) | −146,946 | 1,187,084 | 2,189,708 |
| Dividends | 583,680 | 656,629 | 724,138 |
| Revolver draw/(repay) | 1,230,626 | 469,545 | (465,570) |
| Ending cash | 1,500,000 | 1,500,000 | 1,500,000 |
| Revolver balance | 1,230,626 | 1,700,170 | 1,234,600 |
| Term debt | 5,000,000 | 4,000,000 | 3,000,000 |
| Equity | 9,751,040 | 11,720,927 | 13,893,340 |
| Assets − L&E | 0 | 0 | 0 |
| CF cash − BS cash | 0 | 0 | 0 |

## Profit and cash
- Cumulative NI is 7.86m, but cumulative FCF is only 3.23m. Debt service and dividends need 4.96m (3.0m term repayment plus 1.96m dividends). The shortfall of 1.73m is covered by running cash down by 0.5m and leaving a 1.23m revolver balance at Y3.
- **Working-capital drag is 1.92m over three years, 1.07m of it in Y1.** About half of the Y1 drag (0.53m) is not growth at all. The forecast days are tighter than the opening balance sheet implies: the implied Y0 figures are DIO 46.6 days (forecast 55) and DPO 36.8 days (forecast 35). NWC rises from 12.5% to 14.4% of revenue. This step-up should be confirmed with operations.
- **Capex exceeds D&A** by 1.42m, 0.95m and 0.34m. Growth reinvestment absorbs cash before it shows up in profit.
- **Debt service:** the 1.0m/yr scheduled amortisation is the single largest call on cash after capex.

## Funding implications
- The revolver peaks at **1.70m in Y2** and starts to be repaid in Y3. Net debt/EBITDA in Y3 is 0.5x, so leverage stays modest.
- **The 25% payout is not covered by free cash flow until Y2.** In Y1, FCF is negative (−0.15m), so the dividend and the debt repayment are funded entirely by the revolver and cash on hand. Over Y1–Y3 the dividend is affordable only because the revolver funds it.

### Scenarios (Python; A1 and A2 are illustrative CFO assumptions)
| Case | Peak revolver | Y3 revolver | Cum FCF | Y3 ND/EBITDA |
|---|---:|---:|---:|---:|
| Base | 1,700,170 | 1,234,600 | 3,229,846 | 0.50x |
| Downside A1 (growth 10/6/3%, GM 35%, DSO 50) | 3,476,829 | 3,476,829 (still rising) | 171,819 | 1.33x |
| Upside A2 (growth 22/15/10%, GM 39%) | 1,476,797 | 720,295 | 4,086,828 | 0.35x |

### Sensitivity of peak revolver (one driver at a time; others at Base)
| Driver | Low | Base | High |
|---|---:|---:|---:|
| Payout 0 / 25 / 50% | 646,946 | 1,700,170 | 3,272,940 |
| DSO 30 / 40 / 50 days | 784,620 | 1,700,170 | 2,615,721 |
| Gross margin 41 / 38 / 35% | 674,312 | 1,700,170 | 3,091,560 |
| Y1 capex 7 / 9 / 11% | 1,099,786 | 1,700,170 | 2,300,554 |

Gross margin and payout are the largest levers. Each 10 days of DSO moves the peak revolver by about 0.9m.

## Recommendation
Proceed with the plan, **conditional on:**
1. Arranging a committed revolver of at least **SAR 3.5m**. This covers the A1 downside peak of 3.48m; the base case needs 1.7m.
2. **Deferring or cutting the Y1 dividend.** Set the dividend policy as payout of FCF after debt service rather than 25% of NI. With 0% payout, the peak revolver falls to 0.65m.
3. Validating the DIO 55 / DPO 35 days against operations. Holding Y0 days would release about 0.5m.
4. Phasing the Y1 capex (9%) against milestones.

**Kill or rethink criteria:**
- the revolver is still rising in Y3 (the downside pattern);
- gross margin falls below about 35%;
- DSO goes above 50 days;
- net debt/EBITDA goes above 2.0x.

Lender covenants are not yet known.

## Missing inputs that could change the conclusion
- Revolver facility size, covenants and fees.
- The capex split between maintenance and growth.
- Seasonality: within-year working-capital peaks are likely above the year-end figures.
- Zakat (KSA entities are typically assessed on the zakat base rather than 20% income tax) and VAT timing. **Confirm both with a tax adviser.**
- The lender's actual amortisation profile.

## Checks
- **Model integrity:** 214 live formulas, recalculated in LibreOffice headless, with 0 #REF/#VALUE/Err cells. Each year: Assets − L&E = 0; CF ending cash − BS cash = 0; equity and PP&E roll-forwards = 0; cash ≥ minimum; revolver ≥ 0; opening BS balances. Checks!B12 ALL CHECKS PASS = TRUE.
- **Independent recompute:** a plain-Python model matches Excel to a maximum absolute difference of 4.5e-8 SAR. The `boardcalc.three_statement` cross-check matches with 0.0 difference and a balanced BS.
- **Quality gates run:** gate 1 (inputs tagged), 2 (arithmetic verified), 3 (profit versus cash), 6 (downside first, partly: scenarios and sensitivities, no Monte Carlo) and 7 (circularity, tax on losses, sign conventions).
- **Not applicable:** gate 4 (no peers for a fictional firm) and gate 5 (no valuation requested).
