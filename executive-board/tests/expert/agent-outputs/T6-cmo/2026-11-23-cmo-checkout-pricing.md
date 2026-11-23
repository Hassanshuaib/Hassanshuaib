# CMO analysis: checkout A/B test, unit economics, price 79 -> 89 SAR (fictional)
Date: 2026-11-23 · Calc: `board/analyses/calc/2026-11-23-cmo-checkout-pricing.py` (imports boardcalc)

## Bottom line
The checkout result is not significant (p = 0.20, power about 25%). Do not roll it out as a "win". Keep testing to a
pre-computed sample size. The price rise looks attractive on paper because it breaks even even if churn
rises to about 5.4%. It has not been tested, though, so run it as a controlled test on new signups first.

## Inputs (all from the user, illustrative and fictional)
Control 213/5,200, variant 235/5,100. ARPU 79, GM 65%, churn 4.5%/mo, discount rate 1%/mo, fully loaded CAC 310. Proposed price 89.

## (a) Checkout A/B test (two-proportion z-test, pooled SE, two-sided)
| Metric | Value |
|---|---|
| Conversion: control / variant | 4.096% / 4.608% |
| Relative lift (point estimate) | +12.5% |
| z / p-value | 1.273 / 0.203 |
| 95% CI, absolute diff (unpooled Wald) | -0.28 pp to +1.30 pp |
| 95% CI, relative lift (log risk-ratio method) | -6.2% to +34.9% |
| n per arm for a 10% relative lift (alpha 0.05, power 0.8) | 38,508 (about 77k in total) |
| n per arm to detect the observed +12.5% | 24,956 |
| Power of the current test for the observed lift | 24.6% |
| Power of the current test for a true +10% lift | 17.5% |

Sample-size formula: n = [z(1-a/2)*sqrt(2*pbar*(1-pbar)) + z(1-b)*sqrt(p1(1-p1)+p2(1-p2))]^2 / (p2-p1)^2,
with p1 = 0.04096, p2 = 1.10*p1 and pbar = (p1+p2)/2.
Reading: the CI includes zero and a -6% lift. At about 25% power, a "+12%" point estimate is likely to be inflated (winner's curse).
The current test has about 1/7 of the traffic it needs.

## (b) Unit economics (GM basis, fully loaded CAC)
| Metric | Value |
|---|---|
| Monthly GP per sub | 51.35 |
| LTV undiscounted (GM*ARPU/churn) | 1,141 |
| LTV discounted, end-of-month cash: GM*ARPU/(churn+d) **[used]** | 934 |
| LTV discounted, start-of-month: GM*ARPU*(1+d)/(churn+d) (reference) | 943 |
| LTV:CAC undiscounted / discounted | 3.68x / 3.01x |
| CAC payback on GM | 6.04 months |
| Expected lifetime | 22.2 months |
Convention: revenue is collected at the end of each month, with survival (1-c)^(t-1) discounted by (1+d)^t. A 600-month numeric sum gives the same 933.64.
Reading: the economics are healthy but not generous. Discounted LTV:CAC is about 3.0x. Payback of about 6 months is good.

## (c) Price 79 -> 89 (+12.7%)
| Metric | Value |
|---|---|
| Immediate subscriber loss that keeps MRR unchanged | 11.24% (= 1 - 79/89) |
| GP-neutral churn, fixed COGS 27.65 (GP 51.35 -> 61.35) **[recommended]** | 5.38%/mo (+0.88 pp, +19.5% rel.) |
| GP-neutral churn, margin held at 65% of price (GP 51.35 -> 57.85) | 5.07%/mo (+0.57 pp, +12.7% rel.) |
| Volume-loss break-even, fixed COGS (classic rule) | -16.3% |
| At 89 with churn unchanged (fixed COGS): discounted LTV / LTV:CAC / payback | 1,115 / 3.60x / 5.05 mo |
Steady state subs = new/churn, so GP_ss = new*GP/c and the break-even is c_new = c_old*GP_new/GP_old. A simulation
with 45 new/mo (illustrative) confirms that steady-state GP is equal (51,350 both ways).
**Which rule to use:** fixed COGS, because coffee beans, roasting, packaging and shipping per bag do not rise with the price
we charge (A3). The 65% rule wrongly adds 3.50 SAR of COGS per sub, and so understates the headroom. The 65% figure
(5.07%) can still serve as a conservative guardrail while the COGS facts are confirmed.
Caveat: this break-even assumes the same number of new subs a month. A higher price on the paywall will probably lower
checkout conversion and so raise effective CAC. That needs its own guardrail.

## Assumptions
- A1 (critical): the test was randomised correctly, with no sample-ratio mismatch (5,200 vs 5,100 gives chi-sq 0.97, p 0.32, OK), no peeking, and one primary metric. Basis: not stated.
- A2: discount rate of 1%/mo, end-of-month cash convention. Basis: user input plus convention.
- A3 (critical for c): COGS per sub is fixed in SAR (27.65). Basis: the product is physical, so cost does not scale with price. Needs CFO confirmation.
- A4 (critical for c): new subs per month are unchanged at 89. Basis: given by the user. This is likely optimistic.
- A5: churn is constant (geometric). Real churn usually falls with tenure, so cohort curves would change LTV.

## Missing inputs that would change the conclusion
Pre-registered test plan and daily traffic (sets how long the test runs). Whether the checkout conversion leads to paid
subs or only trials. Current sub base and price elasticity or WTP data. COGS breakdown. Churn by tenure cohort. Competitor price points.

## Recommendations
1. **Checkout variant: do not roll out on this evidence.** Continue the test to 38.5k per arm (about 77k visitors in total),
   with a fixed stopping rule, no peeking (or a sequential/alpha-spending design), and the primary metric of paid conversion.
   Guardrails are refund rate and month-1 churn. Exception: if the variant is cheap, reversible and has no plausible downside, a
   "ship to learn" can be defended, but it must not be reported as a +12% gain.
2. **Price 89: test before rollout.** (i) Randomised price test on new signups only (79 vs 89). Primary metric is GP per visitor
   (conversion x GP/sub). Guardrails are checkout conversion drop under 16% relative and month-1/2 churn under 5.07% (strict) or 5.38%.
   (ii) Run it separately from the checkout test, or as a 2x2 factorial, so the two effects are not confounded. (iii) Only then
   migrate existing subs: grandfather them for 2–3 months with advance notice, and roll out to a 10–20% holdout cell first while watching cancellations.
   (iv) Cheap WTP check: Van Westendorp / Gabor-Granger survey, treated as stated intent with a haircut. Behaviour from test (i) decides.
Confidence: High on (1) (it is statistics). Medium on (2): it depends on A3, A4 and observed churn and conversion at 89.

Checks: all figures from boardcalc (ab_test, ab_sample_size, ltv, subscription_price_change, price_change_breakeven,
norm_cdf/ppf). ab_test CLI and module outputs match. Closed-form LTV equals a 600-month sum. Break-even churn confirmed by
steady-state simulation (GP equal). Relative-lift CI cross-checked (log-RR vs diff/p1). Gates: GM LTV, fully loaded CAC, payback shown, no underpowered winner called.
