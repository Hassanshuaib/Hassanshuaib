# COO analysis: operational stress test of the CFO's SAR 300k Option B plan

Date: 2026-11-23 · Author: COO · Currency: SAR ex-VAT · Stage: idea, nothing validated
Reviewed: board/context.md, board/assumptions.md (A0–A20), board/analyses/2026-11-23-cfo-investment-300k.md
Calculations: board/analyses/calc/2026-11-23-coo-ops-challenge.py (re-runnable; every number below comes from it unless it is marked as a source)

## 0. Bottom line
The CFO's staging (Tranche 0, then lean build, then gated reserve) holds up on operational grounds, and I support it. Four of the operating assumptions underneath it don't hold as written.
1. **"Batch brew" cannot be delivered twice a week.** Only cold product, meaning cold brew RTD or concentrate plus milk, works on a 2-drops-a-week stock model. Hot coffee would need in-office brewing, which is Option C territory.
2. **Delivery is a step-fixed cost, not SAR 35 per drop.** A dedicated driver costs about SAR 89 per drop at 11 offices and about SAR 196 at 5 offices. SAR 35 is only reached at roughly 28–30 offices on dense routes.
3. **Capex leaves out the kit that has to sit in each office**: a fridge or dispenser and a float of returnable containers, about SAR 2.5k per office (estimate).
4. **The owner is the bottleneck.** At 160 seats the owner carries about 34 h/week of sales, delivery and account work on top of management. Owner plus one staff member breaks at about 220–250 seats, which is exactly the Lean Downside break-even (251 seats).

## 1. Operating model map

| Element | Design (COO view) | Constraint / note |
|---|---|---|
| Product | Cold brew RTD in 250 ml bottles, or concentrate in bulk dispensers, plus milk. Optional beans for an office's own brewer | Shelf life (§3) drives the drop frequency and the waste |
| Production | Grind, steep 12–24 h, filter, fill, cap, label with date, chill to ≤5°C | Steep time sets the calendar: produce on Sat/Sun and Tue/Wed |
| Storage | Walk-in or 2–3 upright commercial fridges at the kitchen; a fridge in each office | Office fridge space is often shared, so a dedicated unit is usually needed |
| Delivery | Route-based restock: swap containers, rotate stock, check temperature | Needs a trained person, not an on-demand courier |
| Sales / accounts | Founder-led, 2 new accounts a month (A8) | Owner time is the bottleneck |
| Suppliers | Roasted beans, bottles/caps/labels, milk, cleaning chemicals | Bean supply is a single point of failure; packaging MOQs |
| Riyadh work week | Sun–Thu. Thursday's drop must last until Sunday | Weekend gap means 4–5 days in the office |

## 2. Assumption-by-assumption verdict

| ID | CFO value | Verdict | COO value and reason |
|---|---|---|---|
| A6 | 2 drops/office/week (lean) | **Accept, with a condition** | Workable only for cold product with a date mark of ≤7 days (§3). Strike "batch brew delivered" from the product. With Sun/Wed or Mon/Thu drops, the longest product age at the office is about 4–5 days. |
| A7 | SAR 35/drop | **Adjust** | Treat delivery as **step-fixed**, not variable. Dedicated driver at SAR 8.5k/month (the CFO's own basis): 5 offices = SAR 196/drop, 11 = 89, 21 = 47, 30 = 33. Even the CFO's basis of "~9 drops/day" works out to SAR 43, not 35. COO base: **owner delivers in Tranche 0 and up to about 12 offices (fuel/parking about SAR 10/drop, est.)**, then a part-time driver-helper at about SAR 4.5k/month (est.), which equals about SAR 47/drop at 11 offices. On-demand aggregators (app couriers) may be cheaper per trip, but they can't restock fridges, rotate stock, collect containers or own the cold chain. Use them only for emergency top-ups. Route capacity is about 9 drops per 5-hour shift at about 30 min/drop (A21). |
| A5 | 15 seats/office | **Accept as a planning value, unvalidated** | Downside of 12 is reasonable. The operational point is that per-seat pricing has to cover the **whole office headcount**, not only the people who drink coffee, or seats will shrink to the drinkers. Validate this in the LOIs. |
| A2 | 20 cups/seat/month | **Accept for COGS (conservative). Adjust for production planning to about 15–16** | A cold-only product in an office, including the winter months, will likely see lower uptake (estimate). Lower uptake reduces COGS under a fixed seat price, but par levels set too high create waste because of the 7-day dating. Set par levels from pilot data. The CFO's gate of ≥15 cups/seat is the right one. |
| A3 | COGS SAR 4.9/cup | **Accept, conditional on a bean quote** | COO rebuild at 20 g/cup (cold brew uses slightly more coffee than the CFO's 18 g), beans SAR 120/kg, 50% of cups with 100 ml milk, cups/lids, 12% waste: bulk concentrate 3.95, PET bottles 4.73, bottles with 18% waste 4.99. So 4.9 is fair for bottles, and the downside of 5.4 covers beans at about SAR 150/kg. It breaks if beans cost more than about SAR 150/kg or if every cup is a latte (+~0.5). |
| A10 | Rent SAR 5k/month | **Open, at risk** | Operationally plausible for 60–80 m². The real issue is **zoning and licensability**: a food production activity in a residential district may need a commercial-street plot and SFDA or Balady approval (§5). A cheap unit that can't be licensed is worth nothing. |
| A12 | 1 prep staff × 6k (lean), +6k per 250 seats | **Adjust** | One prep person covers the kitchen up to about 250 seats (about 43 h/week of kitchen work, 48 h is the cap). **The first step comes earlier, and it is a driver-helper (about 4.5–6k) at about 12–15 offices, not a second barista.** At 300+ seats: owner + 2 production staff + 1 driver, so staff cost is about SAR 16–18k/month (est.). Lead time for an expat hire (visa, iqama) could be several months, which needs confirmation. Saudization (Nitaqat) rules may require a Saudi hire, which needs confirmation. |
| A13 | Owner unpaid (lean) | **Accept for the model only. Reject as sustainable beyond about 12–18 months** | At 160 seats the owner carries about 34 h/week of sales, delivery and account work, plus admin and QA (§4). It is a full-time job with no backup. Single point of failure #1. |
| A15 | Capex SAR 90k (lean) | **Adjust to about SAR 105–115k** | Add the office-side kit: fridge/dispenser about SAR 1.8k plus a container float of 3 sets × 6 × SAR 40 = 2.5k/office (est.). That is about 28k at 11 offices and 53k at 21 offices, phased with growth. Offset: drop the 2 batch brewers if the product is cold-only (about −10k, est.). A vehicle is not included, so the plan assumes the owner's car; flag this. Option: charge a refundable deposit or install fee per office. |
| A16 | Pre-launch SAR 25k incl. licensing 12k | **Open** | Licensing cost depends on the licence class: SFDA food factory or Balady kitchen (§5). It could be materially higher if an SFDA factory licence and technical requirements apply. Needs professional confirmation. |
| A8 | 2 new offices/month | **Accept, with a condition** | This is consistent with about 15 h/week of founder sales. It **only holds if delivery is not eating that time**. Above about 12 offices, the owner delivering will crowd out sales. |

## 3. Product feasibility: shelf life, packaging, office storage
- **Shelf life (analogous non-Saudi guidance, not Saudi rules):** US state and local food-safety guidance treats cold brew made without a heat step as a time/temperature-controlled food that has to be refrigerated at ≤41°F (5°C). One HACCP document allows a date mark of no more than 7 days. Kegged product or product packed with reduced oxygen needs a HACCP plan, because of the risk of *C. botulinum* growth. A July 2026 FDA-reported recall of bag-in-box concentrate cited ambient storage as the botulism risk. Sources: [Wisconsin DATCP cold brew fact sheet](https://datcp.wi.gov/Documents2/ColdBrewFactSheet.pdf); [Anchorage cold brew HACCP 2022](https://muni.org/Departments/health/Admin/environment/SiteAssets/Pages/Food-Safety-Resources/Cold%20Brew%20Coffee%20Safety%20HACCP%202022.pdf); [recall report](https://www.thehealthy.com/?p=1231988). **Implication:** plan for a 7-day use-by date, an unbroken cold chain (insulated boxes with ice packs, data loggers), and lab shelf-life validation before scaling. **The Saudi requirement must be confirmed with SFDA.**
- **Packaging choice:** single-use PET is simplest, needs no returns and gives about 4.7 COGS. Returnable glass is cheaper per cup (about 4.3) but adds wash labour, breakage and a reverse-logistics loop. Bulk dispensers are cheapest (about 4.0) but need dispenser capex and sanitation at each office. **Tranche 0: PET only.**
- **Office storage:** at 15 seats × 20 cups, each drop is about 35 bottles (about 9 L) plus milk. That will not fit reliably in a shared office fridge, so a dedicated under-counter unit is needed.
- **Milk:** fresh milk adds a second chilled SKU with its own dating. Supply it, or let offices buy their own (test both in Tranche 0).

## 4. Capacity and throughput (COO estimates, illustrative)
Formulas: cups/week = seats × 20 ÷ (52/12). Kitchen hours = batches(40 L) × 1.5 h + bottles × 0.5 min + drops × 0.5 h wash + 6 h QC/admin. Delivery hours = drops × 0.5 h + 1.5 h per route day for loading and travel. Sales = 15 h/week. Account management = 0.5 h/office/week.

| Seats | Offices | Cups/wk | L/wk | Kitchen h | Delivery h | Sales h | Acct h | Total h | FTE @48h |
|---|---|---|---|---|---|---|---|---|---|
| 75 | 5 | 346 | 87 | 17 | 8 | 15 | 2.5 | 43 | 0.9 |
| 160 | 10.7 | 738 | 185 | 30 | 14 | 15 | 5 | 64 | 1.3 |
| 250 | 16.7 | 1,154 | 288 | 43 | 20 | 15 | 8 | 86 | 1.8 |
| 320 | 21.3 | 1,477 | 369 | 54 | 24 | 15 | 11 | 104 | 2.2 |
| 450 | 30 | 2,077 | 519 | 73 | 33 | 15 | 15 | 136 | 2.8 |

- **At 160 seats:** owner (about 34 h of sales, delivery and accounts, plus admin) and 1 prep person (about 30 h). Feasible, with a cushion of roughly 15–20%. There is no cover for sickness or leave.
- **Capacity breaks at about 220–250 seats (15–17 offices).** Kitchen work reaches about 43 h and the owner's load passes 45 h/week. Add a driver-helper at that point.
- **At 300+ seats:** owner (sales and management) + 2 production staff + 1 driver. Equipment is fine: about 370 L/week is about 9–10 steeps of 40 L across 2 production days, so 2–3 steep tanks are needed (est.).
- **Revised break-even** (script §7): if delivery moves into fixed cost as a part-time driver (fixed cost 21.5k, variable delivery about SAR 10/drop) plus office-kit depreciation, break-even is **about 189 seats, or 12.6 offices**, versus the CFO's 160/11. If the owner delivers: 141 seats, 9.4 offices. Downside (12 seats, SAR 210, COGS 5.4): **266 seats, about 22 offices**, which is past the point where owner plus one staff breaks, so the downside needs more staff. **The downside is worse than the CFO's model shows.**
- **Early-month cash:** with a hired driver, the CFO's SAR 35/drop understates delivery cost in months 1–6 by a factor of 2–5. The owner must deliver until about 12 offices.

## 5. Tranche 0 via a partner kitchen: regulatory plausibility (needs professional confirmation)
- SFDA states that food factories and warehouses need prior SFDA licensing, with an Activity Practice License as the final step and technical requirements to meet. Its investor guide lists a Balady (MOMRAH) licence or an equivalent approval as an early step. Sources: [SFDA licensing guide for food manufacturers/warehouses](https://sfda.gov.sa/sites/default/files/2025-02/GuideObtainingLicenseOperateFoodFeedManufacturersWarehouses.pdf); [SFDA technical requirements, food manufacture](https://sfda.gov.sa/sites/default/files/2024-07/TechnicalRequirementsFoodWaterManufacture.pdf); [SFDA investor journey](https://www.sfda.gov.sa/sites/default/files/2021-04/InvestorJourneytoObtainaLicenseforFoodManufactureoraBottledWaterandIceManufacture.pdf).
- **Key open question:** is the planned activity (bottled, labelled cold brew sold to third-party businesses) a *food factory* (SFDA) activity, or can it run under a Balady-licensed central kitchen or café licence? This is not confirmed. It drives A10, A15 and A16, and it decides whether a "partner kitchen" can legally supply the product. **Do not assume a restaurant or cloud-kitchen licence covers packaged B2B distribution.**
- **Most plausible Tranche 0 route (COO view):** buy or white-label RTD cold brew from a Riyadh roaster or producer that **already holds the right licence for packaged beverages**, and resell it under a short supply agreement. Pilot margin will be thin or negative, which is acceptable because Tranche 0 tests demand, consumption and route operations, not COGS. A second option is a co-packer producing to the CEO's recipe. The fallback is bean supply plus a loaned brewer (Option C-style).
- Also confirm: CR and activity code for invoicing in Tranche 0, Arabic labelling with production and expiry dates, a vehicle for food transport, and food-handler health certificates for the people who handle product.

## 6. Ramp check: 6 months to 11 offices
- With 2 adds/month and 3% churn starting from zero, there are 11.1 offices at M6, which matches the CFO. **One month without adds gives 9.4, and two months gives 7.6.** Corporate vendor onboarding (vendor registration, CR/VAT documents, PO cycles) and fridge installation can easily take a month (estimate).
- **But** if the Tranche 1 gate (≥5 prepaid pilots) converts at opening, there are 15.3 offices at M6. **So the ramp is consistent only if pilots convert into day-one accounts.** Make pilot-to-contract conversion a gate in its own right.
- Onboarding per office (est.): site survey and fridge placement (1 h), a 2-week par-level calibration, a named contact, a 30-day review. One onboarding a fortnight is manageable for the owner. Three or more a month collides with delivery.

## 7. Top execution risks and single points of failure

| # | Risk | Mitigation |
|---|---|---|
| 1 | **Owner overload (sales + delivery + QA)**. No backup, so growth stalls or quality slips | Owner delivers only to about 12 offices. Pre-hire a part-time driver-helper. Write SOPs from week 1. Name a backup person |
| 2 | **Cold-chain or food-safety incident** (warm office fridges, 7-day dating, a botulism-class hazard in sealed low-acid product) | PET with ≤7-day use-by. Insulated boxes, ice packs and temperature loggers. Dedicated office fridges. Lab shelf-life test. HACCP plan before Tranche 1 |
| 3 | **Licence class mismatch** (SFDA factory vs Balady kitchen, residential zoning) after signing a lease | Written regulatory opinion before any lease. Choose a unit already licensed for the activity |
| 4 | Delivery cost at low density | Cluster accounts within about 3–5 km of one route. Minimum 10 seats per account. Fixed delivery days |
| 5 | Waste from over-par stock | Weekly par review per office. Track waste % per account |
| 6 | Single bean supplier, packaging MOQs | Second roaster qualified. 4 weeks of packaging stock |

## 8. Minimum viable Tranche 0 setup (8–12 weeks, ≤ SAR 30k, est.)
- **People:** the CEO/owner covers sales, delivery and account checks. No hires. Optionally a freelance helper on production days if a co-packer needs one.
- **Product source:** an already-licensed roaster or co-packer (RTD cold brew, 250 ml PET, dated). Milk supplied by the producer or the office (test both).
- **Equipment (est.):** 5–6 under-counter fridges placed at pilot offices (borrowed, rented or bought; about 9–11k), 4 insulated boxes, ice packs, 2 temperature loggers, labels, and a simple subscription and billing tool. The owner's car.
- **Delivery:** owner-run route on fixed days. **Weekly schedule:** Sat/Tue collect from the producer; **Sun + Wed** route (or Mon + Thu), 09:30–13:00. Thursday 30-minute calls for par reviews. Mon/Tue sales meetings and tastings. Log the minutes and kilometres of every drop.
- **Scope:** 5–8 pilot offices within one 5 km cluster.

## 9. Operational KPIs to add to the gates and kill criteria
| KPI | Tranche 0 gate / Tranche 1 gate | Kill or red flag |
|---|---|---|
| Measured route time per drop (incl. parking/security) | ≤ 30 min | > 45 min average |
| Fully loaded delivery cost per drop (owner time costed at a notional SAR 50/h) | ≤ SAR 45 at ≥10 offices | > SAR 60 at 15 offices |
| Product waste (expired or returned) | ≤ 10% of units | > 15% for 2 months |
| Cold-chain compliance (logger ≤5°C) | ≥ 98% of drops | Any food-safety complaint means stop and investigate |
| On-time, in-full drops | ≥ 95% | < 90% |
| Pilot-to-contract conversion | ≥ 5 of 8 pilots convert and prepay | < 3 |
| Owner hours/week on ops (delivery + production) | ≤ 20 h | > 30 h means hire the driver-helper before more sales |
| Regulatory | Written licensing route confirmed **before** any lease | No licensable route means no lease |

## 10. 30/60/90 (Tranche 0 and the Tranche 1 decision)
- **Days 0–30:** licensing opinion (SFDA vs Balady, zoning). Shortlist 2 licensed producers. Pilot packaging and dating. Recruit 5–8 pilot offices in one cluster. Install fridges.
- **Days 31–60:** run pilots twice a week. Measure cups/seat, waste, minutes per drop and temperature. Weekly par tuning.
- **Days 61–90:** convert pilots to prepaid contracts. Get kitchen unit and fit-out quotes. Decide on Tranche 1 against the gates above plus the CFO's gates.
- **Resources:** the owner full-time, about SAR 25–30k cash, a regulatory adviser (budget inside the 30k, est.).

## 11. New assumptions (COO estimates)
- A21: route time about 30 min per drop (12 min driving, 8 min parking and security, 10 min restock); about 9 drops per 5-hour shift.
- A22: office-side kit about SAR 2,520 per office (fridge 1.8k + container float 0.72k).
- A23: cold brew use-by ≤ 7 days refrigerated at ≤5°C (based on US guidance; Saudi rule unconfirmed).
- A24: labour time standards (§4 formulas).
- A25: part-time driver-helper about SAR 4.5k/month, needed from about 12–15 offices.

## 12. Recommendation
**Keep the CFO's staged recommendation**, with these operational changes:
(1) The product is cold-only. Tranche 0 sources from an already-licensed producer, and the owner delivers.
(2) Tranche 1 budget rises by about 15–25k for office kit (offset by dropping the batch brewers), or offices pay deposits.
(3) Model delivery as step-fixed. Base break-even becomes about 12–13 offices (about 190 seats), not 11.
(4) Add the operational and regulatory KPIs above as gates.
(5) The Lean Downside needs an extra hire before break-even, so it is worse than the CFO shows. That reinforces "validate before lease."

**Confidence: Medium** on the structure and the failure points. **Low** on all the numbers, which are estimates. What would change this view: a confirmed licence route and real cost, measured minutes per drop in the pilot, real cups per seat and waste, and the CEO's willingness to deliver personally for the first 6–9 months.

_Not legal or regulatory advice. Confirm SFDA, Balady, Civil Defense, zoning, labour and Saudization requirements with qualified professionals._
