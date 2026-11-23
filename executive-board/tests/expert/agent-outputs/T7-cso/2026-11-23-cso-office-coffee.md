# CSO analysis: Riyadh office-coffee entry (FICTIONAL / ILLUSTRATIVE)
Date: 2026-11-23 | Currency: SAR, annual | Calc: `board/analyses/calc/2026-11-23-cso-office-coffee.py`

## 0. Framing
Stated question: "which entry mode?" Real question: **is a SAR ~3.2M/yr revenue ceiling worth a new business line, and what is the cheapest, most reversible way to find out?** Entry mode follows from that answer.

## 1. Inputs
**User inputs (U):** office counts and headcounts by segment; 60% drinkers; 16 cups/month; SAR 10/cup; SAM = 35% of TAM; SOM = 4% of SAM; market shares; option scores and weights. All are fictional.
**Facts:** US DOJ/FTC Horizontal Merger Guidelines. The 2010 version uses these bands: <1,500 unconcentrated, 1,500–2,500 moderately concentrated, >2,500 highly concentrated. The 2023 version uses: <1,000 unconcentrated, 1,000–1,800 moderately concentrated, >1,800 highly concentrated. These bands are from general knowledge. I did not run a web search.
**Assumptions (mine):**
- A1: SAR 10 is the net price per cup that the supplier earns. It is not a café retail price. (Basis: the brief. **Critical**, because B2B office-coffee service usually prices well below café level.)
- A2: 16 cups/month holds in every segment. That is about 0.75 cups per workday on a 21–22 day month. (Basis: the brief. **Critical**.)
- A3: A 4% SOM is reachable within about 3 years. (Basis: the brief. **Critical**.)
- A4: Market shares refer to actual spend, and actual spend is roughly equal to TAM. On that reading, a 1% firm has about SAR 2.3M of revenue. (Illustrative.)
- A5: Co-working members are mostly small and medium offices. (Basis: the typical co-working tenant profile. Needs validating.)

## 2. Market size (bottom-up)
Per employee: 0.60 × 16 × 12 × SAR 10 = **SAR 1,152 per employee per year**

| Segment | Offices | Employees | TAM (SAR) | % of TAM | TAM per office |
|---|---|---|---|---|---|
| Small (8) | 9,000 | 72,000 | 82,944,000 | 35.8% | 9,216 |
| Medium (45) | 1,400 | 63,000 | 72,576,000 | 31.3% | 51,840 |
| Large (300) | 220 | 66,000 | 76,032,000 | 32.8% | 345,600 |
| **Total** | 10,620 | 201,000 | **231,552,000** | 100% | |

- **SAM** (35%) = **SAR 81,043,200**
- **SOM** (4% of SAM) = **SAR 3,241,728/yr**, which is about 324k cups/yr. That equals 1.4% of TAM.
- Cross-check: SOM is about the size of 1.4 of the 1% firms (A4). So "winning SOM" means becoming a top-10 player, not a market leader.
- Top-down check: not possible, because the scenario is fictional and has no external benchmark. TAM is a ceiling, not a forecast.

## 3. Concentration
- HHI = 32² + 24² + 14² + 10² + 8² + 12×1² = 1,024 + 576 + 196 + 100 + 64 + 12 = **1,972**. CR4 = 80%.
- **The two guideline versions disagree.** Under 2010 it is *moderately* concentrated (1,500–2,500). Under 2023 it is *highly* concentrated (>1,800).
- Strategic read: two leaders hold 56% and there is a long tail of 1% firms. The leaders probably hold the large-office contracts, which are the most valuable at SAR 346k per office. The tail is fragmented and could be rolled up.
- Antitrust: buying one 1% firm adds only 2 points to the HHI (2×1×1), so it is a non-issue. Any combination involving the top two would be scrutinised.

## 4. Options (weighted score, renormalised weights)
| Option | Value .35 | Risk .25 | Capital .20 | Speed .20 | Score |
|---|---|---|---|---|---|
| **Partnership (co-working chain)** | 7 | 6 | 7 | 8 | **6.95** |
| Organic | 6 | 7 | 8 | 4 | 6.25 |
| Acquire small competitor | 9 | 4 | 3 | 7 | 6.15 |

I also considered two options outside the matrix. "Do nothing" scores 0 on value with no capital and no risk. "Staged": the partnership pilot below is the staged option.

**Sensitivity (each weight ±20%, one at a time):**
- Partnership wins all 8 cases with renormalisation, and all 8 without it.
- The order of 2nd and 3rd place swaps between cases. Acquire comes 2nd when value is +20%, risk is −20%, capital is −20% or speed is +20%.
- Smallest top-two margin is **0.56**: speed −20%, Partnership 6.91 vs Organic 6.34. Without renormalising, the smallest margin is 0.54 in the same case.
- Break-even weights (single weight moved, others renormalised). Acquire wins only if the value weight rises above **0.75 raw (0.54 normalised)**, which is about 2.1× the current weight. Organic wins only if speed falls below 0.025, or risk rises above about 0.95, or capital rises above about 0.90.
- **No plausible ±20% change flips the winner.** Robust.

## 5. Competitive advantage (7 Powers)
- Organic: none. It relies on execution only.
- Partnership: possible **Cornered Resource**, but only if the co-working access is **exclusive** and multi-year. Without exclusivity it has no moat. There are also mild **switching costs**, from installed machines and service contracts.
- Acquire: none on its own. The tail of 1% firms could give roll-up **Scale Economies** in route density, but that is a different and larger strategy.

## 6. Recommendation
**Enter through the co-working partnership as a staged pilot. Focus on small and medium offices inside the co-working footprint. Do not acquire now.**
- Segment logic: co-working gives dense, low-cost access to small and medium tenants. Those tenants have high CAC when reached one by one, and they make up 67% of TAM. Large offices (SAR 346k each) are where the leaders compete, so defer them until we have references.
- What SOM implies: a revenue ceiling of about **SAR 3.2M/yr**. If gross margin is 35–50% (illustrative, not given), that leaves about SAR 1.1–1.6M of gross profit before route, staff and machine costs. It is **worth pursuing only as a low-capital adjacency, or as a beachhead that can later grow to the 1% firms' level.** It does not justify an acquisition premium or a heavy capex build.
- An acquisition becomes rational only if the strategy changes to a roll-up of the 1% tail. That would need a separate case.

**Gates / kill criteria**
- G1 (0–6 months, pilot at 3–5 sites). Continue only if three things hold: measured cups per employee per month is at least 12, the realised net price is at least SAR 8, and the partner grants exclusivity for at least 24 months. Kill if price is below SAR 6 or uptake is below 40% of employees.
- G2 (6–18 months). Continue only if the run-rate is at least SAR 1M and contribution margin is positive per site. Expand to direct small and medium sales near the hubs.
- G3 (18–36 months). Revisit the acquisition or roll-up option only if the run-rate approaches SOM and route density economics are proven.

## 7. Assumptions that matter most and how to validate them
1. **SAR 10/cup (A1).** Revenue scales 1:1 with price. Validate with quotes from 3–5 Riyadh office-coffee suppliers, competitor price lists and the pilot's realised price.
2. **16 cups/month and 60% drinkers (A2).** Volume is the product of these two. Validate with consumption logs or machine telemetry from pilot sites, plus an employee survey (n ≥ 200).
3. **4% SOM (A3).** Check it against how fast the 1% firms grew and against win rates in pilot sales. Also confirm the 35% radius figure by mapping offices against our delivery routes.

## 8. Missing inputs that could change the conclusion
Gross margin and cost to serve per site; partner terms and exclusivity; acquisition price and target revenue; whether shares are measured on spend or on TAM; segment-specific consumption and price (large offices likely negotiate lower prices).

## 9. Top risks
Price compression from the two leaders. A non-exclusive partner, or a partner that switches supplier. SAR 10 being a retail-level assumption, which would overstate everything. Low drink uptake in small offices.

Checks: TAM, SAM, SOM, HHI and the decision matrix were computed with cso-toolkit `boardcalc.py` (market_sizing, hhi, decision_matrix with ±20% perturbation). Each one was asserted equal to independent manual arithmetic in the calc script. Segment shares sum to 100%. Market shares sum to 100. Non-renormalised sensitivity and break-even weights were computed separately, and the speed break-even of 0.025 was checked analytically (P − O = 4w − 0.10).
