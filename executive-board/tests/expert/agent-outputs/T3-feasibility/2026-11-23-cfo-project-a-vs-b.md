# CFO analysis: Project A vs Project B (mutually exclusive, repeatable)
Date: 2026-11-23 | Currency: SAR | Case: fictional and illustrative | Script: `board/analyses/calc/2026-11-23-cfo-project-a-vs-b.py`

## 1. Decision and question
Choose one of two mutually exclusive, repeatable projects: A (new line, 6 years) or B (smaller line, 4 years). Which one creates more value at an 11% discount rate, given the different scale and lives?

## 2. Inputs and assumptions
**Inputs (CEO):** all A drivers (capex 2.4m, 6-year straight-line depreciation, 200k pre-tax salvage, 40,000 units +5%, price 95 +2%, variable cost 58%, fixed 650k +3%, NWC 12% of revenue), B's after-tax flows, r = 11%, tax 20%, tax-loss offset, repeatability on the same terms.
- A1 NWC convention (base): each year's balance is invested in that year (year-1 balance at t1) and fully recovered at t6. This is the CEO's stated interpretation. The alternative (balance in place at the start of each year, so the year-1 balance goes in at t0) is shown as a sensitivity. Basis: brief.
- A2 Year-end cash flows, nominal, with r = 11% nominal for both projects. Same risk class, so the same rate. Basis: brief and judgement.
- A3 Repetition "on the same terms" means identical nominal cash flows each cycle, with no inflation in capex or price. For A this is mildly conservative (cycle 2 restarts at price 95). Basis: brief.
- A4 B's flows are already after tax and include its own NWC and salvage. Basis: brief. **Unverified, so it should be confirmed.**
- A5 The tax-loss offset is not triggered: A's EBIT is positive every year. Zakat is ignored, which needs professional confirmation for a KSA entity.

## 3. Project A cash flow table (SAR, NWC convention A1)
| t | Revenue | Variable cost | Fixed cost | Depreciation | EBIT | Tax 20% | NOPAT | + Dep | ΔNWC | Capex | AT salvage | NWC recovery | **FCF** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | – | – | – | – | – | – | – | – | 0 | (2,400,000) | – | – | **(2,400,000)** |
| 1 | 3,800,000 | (2,204,000) | (650,000) | (400,000) | 546,000 | (109,200) | 436,800 | 400,000 | (456,000) | – | – | – | **380,800** |
| 2 | 4,069,800 | (2,360,484) | (669,500) | (400,000) | 639,816 | (127,963) | 511,853 | 400,000 | (32,376) | – | – | – | **879,477** |
| 3 | 4,358,756 | (2,528,078) | (689,585) | (400,000) | 741,092 | (148,218) | 592,874 | 400,000 | (34,675) | – | – | – | **958,199** |
| 4 | 4,668,227 | (2,707,572) | (710,273) | (400,000) | 850,383 | (170,077) | 680,306 | 400,000 | (37,137) | – | – | – | **1,043,170** |
| 5 | 4,999,672 | (2,899,810) | (731,581) | (400,000) | 968,281 | (193,656) | 774,625 | 400,000 | (39,773) | – | – | – | **1,134,852** |
| 6 | 5,354,648 | (3,105,696) | (753,528) | (400,000) | 1,095,424 | (219,085) | 876,339 | 400,000 | (42,597) | – | 160,000 | 642,558 | **2,036,300** |

Formulas: Rev_t = 40,000·1.05^(t−1) × 95·1.02^(t−1); FCF = NOPAT + Dep − ΔNWC − Capex + AT salvage + NWC recovery; AT salvage = 200,000 − 20%·(200,000 − 0).
Cash vs profit: total NOPAT is 3,872,798 and total FCF is 4,032,798. The difference is the 160,000 after-tax salvage, because depreciation reverses capex and NWC nets to zero over the life. The year-1 FCF is low (380,800) because the year-1 NWC build (456,000) absorbs most of the operating cash. Peak funding is 2.40m at t0 (2.86m under the t0 NWC convention). The cumulative position turns positive in year 4.

## 4. Metrics at 11% (MIRR finance and reinvestment rate = 11%)
| Metric | A | B | Favours |
|---|---|---|---|
| NPV (one cycle) | 1,806,830 | 124,409 | A |
| IRR | 29.10% | 16.17% | A |
| MIRR | 21.88% | 14.01% | A |
| Simple payback (yrs) | 3.17 | 2.76 | **B** |
| Discounted payback (yrs) | 3.94 | 3.50 | **B** |
| PI | 1.753 | 1.113 | A |
| EAA | 427,092 | 40,100 | A |
| 12-year replacement chain NPV | 2,772,835 (A×2) | 260,346 (B×3) | A |
| Chain EAA (check) | 427,092 | 40,100 | ties to EAA |

Incremental view (one cycle): A − B costs 1.3m more at t0 and adds 1.68m of NPV. The crossover rate on the 12-year chains is 35.87%, which is the same rate at which EAA_A = EAA_B, so the check is consistent. A wins at any discount rate below about 36%.

## 5. Economic reasoning and ranking conflicts
- **No scale-vs-IRR conflict.** The textbook conflict (the large project has the higher NPV, the small one the higher IRR) does not occur: A dominates B on NPV, IRR, MIRR and PI. A's larger scale is not bought with a lower return. Every extra riyal earns about 34% (one-cycle incremental IRR), against 11% required.
- **Unequal lives.** Raw NPV compares 6 years against 4, so it overstates A's lead. EAA (427k vs 40k a year) and the 12-year chain (2.77m vs 0.26m) correct for this, and A still wins by about 10x. With equal-risk repeatable projects, EAA and the chain must give the same ranking, and they do.
- **PI.** A's PI is higher too (1.75 vs 1.11). PI only matters under capital rationing. If capital is rationed, A still wins unless the 1.3m saved by choosing B could be deployed elsewhere at an NPV above about 1.68m. That is an implausible PI of about 2.3 on the 1.3m.
- **The only conflict is payback.** B recovers its cash about 0.4 years sooner, because it is smaller and A's year-1 NWC build depresses its early FCF. Payback ignores the cash after the cutoff and the scale, so it is a liquidity signal, not a value signal. It matters only if the company faces a binding cash constraint over the next 3–4 years.
- **Why A creates value.** A's contribution margin is 42% on growing volume against fixed costs that grow only 3%, so operating leverage lifts the EBIT margin from 14.4% (Y1) to 20.5% (Y6). B is close to marginal: its PI is 1.11, and its NPV turns negative at a discount rate of about 16.2%.

## 6. Sensitivities
**NWC timing (A):**
| Convention | t0 FCF | NPV | IRR | MIRR | PB | DPB | PI | EAA | Chain NPV |
|---|---|---|---|---|---|---|---|---|---|
| Year-1 (base) | (2,400,000) | 1,806,830 | 29.10% | 21.88% | 3.17 | 3.94 | 1.753 | 427,092 | 2,772,835 |
| t0 (start-of-year) | (2,856,000) | 1,748,169 | 27.35% | 20.20% | 3.21 | 4.05 | 1.612 | 413,226 | 2,682,811 |
Moving NWC to t0 costs only about 59k of NPV (−3.2%). **The decision does not change.**

**Discount rate (EAA, SAR):**
| r | 8% | 10% | 11% | 12% | 14% | 16% |
|---|---|---|---|---|---|---|
| A EAA | 495,273 | 449,921 | 427,092 | 404,166 | 358,035 | 311,551 |
| A EAA (t0 NWC) | 485,604 | 437,488 | 413,226 | 388,832 | 339,661 | 290,000 |
| B EAA | 62,651 | 47,677 | 40,100 | 32,465 | 17,023 | 1,357 |
The ranking only flips at r of about 35.9%. **The decision does not change** at any plausible cost of capital.

**Operating scenarios (A, illustrative ranges; B's flows are given):**
| Case | Drivers | NPV | IRR | EAA | vs B EAA 40,100 |
|---|---|---|---|---|---|
| Downside | price −5%, var 60%, volume −10% | 660,060 | 18.0% | 156,023 | A still wins |
| Base | as given | 1,806,830 | 29.1% | 427,092 | A wins |
| Upside | price +3%, var 57%, volume +5% | 2,469,514 | 35.0% | 583,735 | A wins |
Reverse stress (one driver at a time): the Y1 price would have to fall to 69.64 (−26.7%) for A's EAA to equal B's, and to 67.01 (−29.5%) for A's NPV to reach zero. Variable cost would have to rise to 68.9% of revenue (+10.9 pp) to equal B, or 70.0% to reach NPV = 0. The margin of safety is wide.

## 7. Reality check (gate 4)
An IRR of 29% and a margin rising to 20% are strong for a production line. The result depends on the 42% contribution margin and on 5% a year volume growth for six years. These drivers are the CEO's inputs, not market facts, and they have not been benchmarked. Because volume and price compound, Y6 revenue is 41% above Y1 (a CAGR of about 7.1% nominal), which is plausible but should be demand-tested.

## 8. Verdict
**Invest in A, not B**, on the condition that:
1. the price and variable-cost assumptions are confirmed by quotes or contracts (the 58% variable cost especially), and
2. the company can fund about 2.4–2.9m at t0 plus the year-1 NWC without straining liquidity.

**Kill or rethink criteria:** the validated Y1 price falls below about 81 (computed: with variable cost at 60% and volume −10% at the same time, A's EAA equals B's at a price of 81.37, or −14.3%), the variable cost is above about 65%, or cash is so constrained that a 3–4 year payback horizon binds. In that last case, revisit B or a phased A.

Confidence: High on the ranking, because it holds across every metric except payback, across NWC timing, at rates up to about 36%, and in the downside case. Medium on the absolute NPV, because the drivers are unvalidated.

## 9. Limitations
B's flows are a black box (A4). The analysis uses no inflation on repetition, a single discount rate, year-end timing, and no Monte Carlo (the case is illustrative and the margin of safety is wide). Tax, zakat and depreciation rules need confirmation by a tax adviser. For a real commitment of this size, an independent CRO review is recommended.

Checks: (1) A's FCF reproduced by an independent build and by `boardcalc.project` (max diff < 1e-6); (2) ΣΔNWC + recovery = 0; (3) ΣFCF = ΣNOPAT + AT salvage; (4) NPV at IRR ≈ 0 for A and B; (5) chain EAA = single-cycle EAA for both; (6) chain crossover rate (35.87%) = bisection rate where EAA_A = EAA_B; (7) `compare_projects` flagged the unequal lives and no NPV/IRR conflict. Gates run: 1, 2, 3, 4, 6 (scenarios, reverse stress), 7, 8, 9; gate 5 (triangulation) is satisfied by NPV/EAA/chain/incremental; gate 10 is recommended.
