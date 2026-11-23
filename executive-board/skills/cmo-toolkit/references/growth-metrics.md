# Acquisition, retention and marketing ROI

- **Funnel** (`funnel`): impressions → visits → leads → trials → customers. Model each conversion with a range, and find the weakest stage: fixing it usually beats buying more traffic.
- **CAC:** fully loaded (media + salaries + tools + agency + promotions) ÷ new customers, by channel. Blended CAC hides failing channels.
- **LTV** (`ltv`, `cohort_ltv`): gross-margin basis, discounted. Use cohort retention curves when available. Constant churn overstates LTV when early churn is high.
- **Health:** LTV:CAC ≥ 3 (heuristic), CAC payback < 12 months for SMB subscriptions (heuristic; state that it is), net revenue retention, and a retention curve that flattens.
- **Marketing ROI** (`marketing_roi`): ROAS on revenue is not ROI. Use margin and incremental revenue.
- **Experiments** (`ab_sample_size`, `ab_test`):
  - Pre-register the metric, the MDE and the sample size.
  - Use two-sided tests at α = 0.05 and power 0.8 by default.
  - Peeking inflates false positives, so use a fixed horizon.
  - Report the confidence interval, not just the p-value.
- **Retention levers:** onboarding to the first value moment, habit loops, service recovery, loyalty programmes (watch the margin cost) and win-back offers.
