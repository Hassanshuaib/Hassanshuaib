# COO analysis: Cloud kitchen operations check (packing, cups, oven OEE)
Date: 2026-11-23 | Role: COO | Status: fictional case, all inputs illustrative (CEO-provided) | Currency: SAR
Calc script: `board/analyses/calc/2026-11-23-coo-cloud-kitchen-ops.py` (uses boardcalc `erlang_c`, `staff_for_service_level`, `capacity`, `safety_stock`, `eoq`, `oee`)

## Bottom line
12 packing stations will not work. At 180 orders/hr and 15/hr per station, utilisation is exactly 100% and the queue grows without limit. **14 is the minimum** that meets the target (89.3% of orders wait 3 min or less). Run 14 at the peak and keep a 15th station ready to flex in. Cups: safety stock about 2,261, reorder point about 8,261, EOQ about 56,900 cups. Oven OEE is 75%, and the biggest loss is performance (speed), not downtime.

## Facts / user inputs (CEO, fictional)
- Packing: λ = 180 orders/hr at peak; μ = 15 orders/hr per station; M/M/c; target is 80% or more of orders waiting 3 min (0.05 hr) or less before packing starts; plan is c = 12.
- Cups: demand 1,200/day (sd 300, independent days); lead time 5 days (sd 1); 95% service level; D = 432,000/yr; S = SAR 450/order; H = SAR 0.12/cup/yr.
- Oven: planned 600 min, run 540 min, ideal cycle 0.5 min/unit, 950 units made, 900 good.

## Assumptions
- A1: Peak λ = 180/hr holds for the whole peak hour (stationary). Basis: CEO input. **Critical.** Real peaks surge within the hour.
- A2: Exponential service (CV = 1). Basis: M/M/c as given. A conservative assumption if packing is standardised.
- A3: Every station has a packer for the whole peak (no breaks or absences). Basis: estimate. **Critical.**
- A4: 360-day year for the EOQ cycle. Basis: CEO's D = 1,200 × 360.
- A5: Cup demand and lead time are independent and roughly normal. Basis: standard formula.

## (a) Packing stations: M/M/c (Erlang C)
Offered load a = λ/μ = 12 Erlangs. ρ = a/c. Wq = P(wait)/(cμ − λ). SL = 1 − P(wait)·e^(−(cμ−λ)·t).

| c | Utilisation ρ | P(wait) | Avg Wq | Lq (orders) | P(Wq ≤ 3 min) | Meets 80%? |
|---|---|---|---|---|---|---|
| 12 | 100.0% | n/a | infinite | infinite | 0% (unstable) | No |
| 13 | 92.3% | 70.4% | 2.82 min | 8.45 | 66.7% | No |
| **14** | **85.7%** | **48.2%** | **0.96 min** | **2.89** | **89.3%** | **Yes (minimum)** |
| 15 | 80.0% | 31.9% | 0.43 min | 1.28 | 96.6% | Yes |

- **Verdict on 12:** reject. With ρ = 1, packing capacity equals demand exactly, so any variability builds a backlog that never clears during the peak, and orders go cold.
- **14 is fragile.** Sensitivity: +10% arrivals (198/hr) requires 15; packers 10% slower (13.5/hr) requires 15; both together require 17.
- Planning rule (85% utilisation cap, `capacity`): 15 stations at 80% utilisation.
- The 3-min target covers only the wait before packing starts. Total time in system at c = 14 is about 4.96 min (wait plus 4 min of packing).

### Is M/M/c realistic?
- Service: packing is fairly standardised, so its CV is probably below 1, and M/M/c then overstates the wait (conservative).
- Arrivals: aggregator dispatch and lunch/dinner spikes are burstier than Poisson and change within the hour. Here M/M/c understates the wait. Size to the **peak 15-minute rate**, not the hourly average.
- Net: treat 14 as the floor. Validate with a time study (service time mean and CV) and 15-minute arrival data. Kingman/Allen-Cunneen or a simulation would then fine-tune the number.

## (b) Cup inventory
- σ_LTD = √(L·σd² + d²·σL²) = √(5·300² + 1,200²·1²) = √(450,000 + 1,440,000) = **1,374.8 cups**. Lead-time variability is 76% of the variance, so the supplier, not demand, is the main driver.
- Safety stock = z·σ_LTD = 1.645 × 1,374.8 = **2,261 cups** (2,261.3 with the exact z = 1.64485).
- Reorder point = d·L + SS = 6,000 + 2,261 = **8,261 cups** (6.9 days of cover).
- EOQ = √(2DS/H) = √(2·432,000·450/0.12) = **56,921 cups**.
- Orders/yr = 432,000/56,921 = **7.59**. Cycle = 360/7.59 = **47.4 days**.
- Ordering cost = 7.59 × 450 = **SAR 3,415**. Cycle holding = Q/2·H = **SAR 3,415** (equal at the EOQ, as expected). **Total relevant = SAR 6,831/yr.** Adding safety-stock holding (2,261 × 0.12 = SAR 271) gives **SAR 7,102/yr**.
- Caveats: an average stock of about 30,700 cups (Q/2 + SS) needs storage space. Check it, along with any branding or format changes that would leave stock obsolete. The cost curve is flat near the EOQ, so rounding to supplier pallet sizes costs little.
- Lever: cutting the lead-time sd from 1 day to 0.5 day gives σ_LTD = √(450,000 + 360,000) = 900, so SS ≈ 1,480 (−35%). The supplier SLA is the lever.

## (c) Oven OEE
| Factor | Formula | Value | Loss (min of 600) |
|---|---|---|---|
| Availability | 540/600 | **90.0%** | 60 (downtime) |
| Performance | 0.5×950/540 | **88.0%** | **65 (speed loss, minor stops): biggest** |
| Quality | 900/950 | **94.7%** | 25 (50 rejects × 0.5 min) |
| **OEE** | A×P×Q | **75.0%** | 450 fully productive min of 600 |

- The biggest loss is performance (65 min), only just ahead of availability (60 min). Next steps: (1) find out why cycles run slower than 0.5 min (loading, door-open time, preheat); (2) run SMED on changeovers; (3) do root-cause work on the 5.3% scrap, because rejects also waste food cost.

## Execution risks and single points of failure
| Risk | Mitigation |
|---|---|
| Peak surges above 180/hr (A1) | Size to the 15-min peak, keep a 15th flex station, and stagger aggregator acceptance |
| Packer absence (A3): 14 staffed means a 13-station day, with SL of 66.7% | Cross-train kitchen staff, set an on-call rule, and add 1 roster buffer |
| Cup supplier lead-time variance (76% of risk) | Use a second supplier, put lead time into the SLA, and review the ROP monthly |
| Single oven (if only one): OEE 75% and no redundancy | Preventive maintenance plan and a backup cooking method for the menu |

## 30/60/90 plan
- **30 days:** Staff 14 stations at the peak, with a 15th on flex. Time-study packing (n ≥ 50) and log 15-minute arrivals. Set the cup ROP at 8,261 and the order quantity at about 57,000 (rounded to the supplier's pack size). Start an OEE loss log.
- **60 days:** Recompute c from real arrival and service data (Allen-Cunneen or simulation). Negotiate the cup supplier's lead-time SLA. Run a kaizen on oven performance loss.
- **90 days:** Target OEE of 80% or more. Introduce dynamic staffing by 15-minute slot. Review the SS against the actual fill rate.

## KPIs
1. P(wait ≤ 3 min) at the peak: ≥ 80% (target 85%).
2. Packing utilisation at the peak: 80–86%.
3. Cup stockouts: 0 per quarter; fill rate ≥ 95%.
4. Supplier lead time: mean ≤ 5 days, sd ≤ 1 day.
5. Oven OEE: 75% now, target 80% at 90 days (Performance ≥ 92%, Quality ≥ 97%).

## CFO hand-off (cash / P&L)
- Packing: +2 stations vs the plan (14 vs 12) means +2 packer-shifts per peak hour, plus fit-out capex if stations do not exist. Missing input: hourly wage and the cost per station.
- Cups: ordering plus holding is SAR 7,102/yr. The NWC tied up is about 30,700 cups × unit cost (missing input).
- Oven: each +1 pt of OEE adds about 6 productive min/day, about 12 units/day at 0.5 min (illustrative). This only becomes cash if the oven is the bottleneck and there is demand to fill the extra capacity.

## Missing inputs (would change the conclusion)
Real 15-minute peak arrival data; service-time CV; packer wage and station capex; cup unit cost and storage capacity; supplier MOQ and pack size; number of ovens and whether the oven is the bottleneck.

Checks: all figures from boardcalc (`erlang_c`, `staff_for_service_level`, `capacity`, `safety_stock`, `eoq`, `oee`). Erlang C cross-checked with an independent factorial-sum formula (identical to 10 dp at c = 13 and 14). σ_LTD, SS and ROP recomputed by hand with z = 1.645 (2,261.5 vs 2,261.3). EOQ ordering = holding (SAR 3,415 each) confirms the optimum. OEE A×P×Q = 450/600 = 0.75 ties out. Quality gates: utilisation shown alongside service level; 85% utilisation cap applied; SPOFs and mitigations listed; cash effects handed to the CFO.
