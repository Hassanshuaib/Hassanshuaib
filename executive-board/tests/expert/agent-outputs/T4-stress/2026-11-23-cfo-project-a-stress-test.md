# CFO: Project A NPV stress test (2026-11-23)

**Decision:** whether Project A's 6-year capex project creates value, and how fragile that NPV is. Currency SAR. All figures are fictional and **illustrative**, and every input comes from the CEO (no changes made).
**Script:** `board/analyses/calc/2026-11-23-cfo-project-a-stress-test.py` (seed 20261123, re-runnable). It uses boardcalc `npv`, `irr` and `payback`.

## Inputs (all **Input**, from the CEO)
Capex 2,400,000 at t=0. Straight-line depreciation over 6 years (400,000 a year). Salvage 200,000 pre-tax, taxed at 20%, giving 160,000 after tax at t=6.
Year-1 volume 40,000 units, growing 5% a year. Year-1 price 95, growing 2% a year. Variable cost 58% of revenue. Fixed cost 650,000, growing 3% a year.
NWC is 12% of revenue. Tax 20%, with losses creating a tax saving. Discount rate 11%.

**Convention set by the brief (base): NWC beginning-of-year.** The year-t NWC balance is invested at t-1, so the year-1 balance (456,000) goes in at t=0. Increments are invested at each later year-start, and the full balance is recovered at t=6.
**Alternative convention (NWC change in the same year as revenue, recovered at t=6):** NPV 1,806,830, IRR 29.1%. That is +58,661 versus base, so the base convention is the more conservative one.

Formulas: Rev_t = V1·1.05^(t-1)·P1·1.02^(t-1). EBIT = Rev − vc·Rev − F1·1.03^(t-1) − Capex/6. OCF = EBIT·(1−0.2) + Dep. FCF = OCF − ΔNWC (+ salvage·0.8 at t=6). NPV = Σ FCF_t/1.11^t.

## Base case cash flows (SAR)
| t | Revenue | Var. cost | Fixed | EBIT | Tax | OCF | NWC flow | Capex/Salvage | FCF |
|---|---|---|---|---|---|---|---|---|---|
| 0 | | | | | | | -456,000 | -2,400,000 | -2,856,000 |
| 1 | 3,800,000 | 2,204,000 | 650,000 | 546,000 | 109,200 | 836,800 | -32,376 | | 804,424 |
| 2 | 4,069,800 | 2,360,484 | 669,500 | 639,816 | 127,963 | 911,853 | -34,675 | | 877,178 |
| 3 | 4,358,756 | 2,528,078 | 689,585 | 741,092 | 148,218 | 992,874 | -37,137 | | 955,737 |
| 4 | 4,668,227 | 2,707,572 | 710,273 | 850,383 | 170,077 | 1,080,306 | -39,773 | | 1,040,533 |
| 5 | 4,999,672 | 2,899,810 | 731,581 | 968,281 | 193,656 | 1,174,625 | -42,597 | | 1,132,028 |
| 6 | 5,354,648 | 3,105,696 | 753,528 | 1,095,424 | 219,085 | 1,276,339 | +642,558 | +160,000 | 2,078,897 |

**Base results:** NPV **1,748,169**. IRR **27.4%** (one sign change, so the IRR is unique). Simple payback **3.21 years**. Discounted payback **4.05 years**.
**Peak funding:** 2,856,000 at t=0 (capex plus initial NWC). Cumulative cash turns positive during year 4.
**NPV bridge (PV terms):** after-tax EBITDA 3,972,589 + depreciation tax shield 338,443 − NWC 248,406 + salvage 85,543 − capex 2,400,000 = 1,748,169.

## 1. Tornado (±10% relative, one input at a time)
| Rank | Driver | −10% input → NPV | +10% input → NPV | Swing |
|---|---|---|---|---|
| 1 | Variable cost % | 52.2% → 2,621,353 | 63.8% → 874,984 | 1,746,369 |
| 2= | Year-1 price | 85.5 → 1,140,703 | 104.5 → 2,355,634 | 1,214,931 |
| 2= | Year-1 volume | 36,000 → 1,140,703 | 44,000 → 2,355,634 | 1,214,931 |
| 4 | Year-1 fixed cost | 585,000 → 1,983,216 | 715,000 → 1,513,122 | 470,094 |
| 5 | Capex (with depreciation) | 2.16m → 1,954,324 | 2.64m → 1,542,013 | 412,311 |

Price and volume are identical because revenue = V × P and every revenue-linked line (variable cost, NWC) scales the same way. The variable-cost ±10% swing (±5.8 pts of a 42% contribution margin, about ±13.8% of contribution) is larger than ±10% of revenue. The NPV stays positive at every tornado end-point.

## 2. Reverse stress test (NPV = 0, everything else at base)
- **Break-even year-1 price: 67.66**, giving **28.8% headroom** below 95.
- **Break-even year-1 volume: 28,489 units**, giving **28.8% headroom** below 40,000.
- The headroom is identical for the same V × P reason. NPV is linear in each driver, so solving by bisection is exact (residual about 1e-10).

## 3. Combined downside (applied together)
Volume 30,000, price 87.4, variable cost 62% and fixed cost 715,000:
- NPV **−785,536**. IRR **2.1%** (unique). Simple payback **5.78 years**. **No discounted payback** within the 6-year life.
- FCF runs from 282,749 in year 1 to 1,143,451 in year 6. Peak funding is 2,714,640 at t=0 (NWC is lower because revenue is lower).
- This case breaches the volume break-even (30,000 is only 5% above 28,489 on its own). Adding the price, variable-cost and fixed-cost hits together pushes it well below zero.

## 4. Monte Carlo (20,000 runs, seed 20261123)
Distributions: price triangular(85, 95, 100); volume normal(40,000, 6,000); variable cost % triangular(0.55, 0.58, 0.64). All independent, everything else at base.
| Statistic | NPV (SAR) |
|---|---|
| NPV at base inputs | 1,748,169 |
| Mean | 1,496,873 |
| Median | 1,469,264 |
| Standard deviation | 942,480 |
| P5 / P95 | −13,005 / 3,087,557 |
| **P(NPV < 0)** | **5.1%** |

The volume truncation at 0 was **never triggered**: 0 of 20,000 draws, because 0 is 6.7 standard deviations below the mean.
**Why the mean is below the base NPV:** both triangular distributions are skewed against the project. The price mean is (85+95+100)/3 = 93.33, below the mode of 95. The variable-cost mean is (0.55+0.58+0.64)/3 = 59.0%, above the mode of 58%. The base case uses the modes, not the means. NPV at the input means is 1,493,688, which is almost exactly the MC mean of 1,496,873. The small residual comes from sampling noise and the price × variable-cost interaction. Volume is symmetric, so it contributes no bias.

## Interpretation (Opinion)
- On the CEO's inputs, the project clears 11% comfortably: IRR 27%, NPV of about 1.75m, and only about 5% probability of a loss under the stated uncertainty.
- The main fragility is **contribution margin**, not capex. Variable-cost % is the biggest driver. Price or volume headroom is about 29% each. However, a moderate *simultaneous* deterioration (the combined downside) wipes out the value: NPV −0.79m, IRR 2%.
- The MC understates tail risk because the inputs are drawn independently. In reality, price and volume cuts often move together (a weak market), so P(NPV < 0) is likely above 5%.
- **Verdict:** invest only if conditions are met.
  - **Conditions:** (1) evidence that the variable cost can be held at 60% or below (supplier quotes or contracts); (2) a demand signal supporting at least about 34,000 units in year 1 (roughly 15% above break-even).
  - **Kill criteria:** committed variable cost above 62%, or validated year-1 volume below about 30,000 at a price below 90.

## Limitations
- Annual end-of-year discounting, with no mid-year convention.
- Deterministic growth rates. No inflation split; inputs are treated as nominal.
- A 20% tax on all profit is the CEO's simplification. The real zakat/CIT treatment and VAT need professional confirmation.
- No correlation in the MC.
- The figures are illustrative.

**Checks:**
- Base NPV agrees exactly (difference 0.00) across three methods: boardcalc `npv`, manual discounting, and a PV decomposition bridge.
- boardcalc `irr` reports a single sign change, so the IRR is unique.
- Payback was hand-traced: cumulative −218,661 after year 3, then 218,661/1,040,533 = 0.21 of year 4.
- Break-even residuals are about 1e-10.
- NWC flows sum to zero across the life.
- No truncation in the MC. The MC mean reconciles to NPV at the input means.
- Gates 1, 2, 3, 6 and 7 applied.
- The project is material, so I recommend a CRO independent review before commitment.
