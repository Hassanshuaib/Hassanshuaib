"""CMO calc: checkout A/B test, unit economics, price 79->89. All inputs are user-supplied, fictional (SAR).
Run: python3 2026-11-23-cmo-checkout-pricing.py   (imports the verified boardcalc module)"""
import json, math, sys
sys.path.insert(0, "/home/user/Hassanshuaib/executive-board/scripts")
import boardcalc as bc

R = {}
# ---- (a) A/B test ----
ca, na, cb, nb = 213, 5200, 235, 5100
t = bc.ab_test(ca, na, cb, nb)                       # pooled z, two-sided p, unpooled Wald CI on diff
R["ab_test"] = t
pa, pb = t["rate_a"], t["rate_b"]
z975 = bc.norm_ppf(0.975)
# Relative-lift CI: log risk-ratio (Katz) method -- not in boardcalc, uses bc.norm_ppf
se_log = math.sqrt((1 - pa) / ca + (1 - pb) / cb)
rr = pb / pa
R["rel_lift_ci95_logRR"] = [rr * math.exp(-z975 * se_log) - 1, rr * math.exp(z975 * se_log) - 1]
# Cross-check: delta method on the difference divided by pa
R["rel_lift_ci95_simple"] = [t["ci95_diff"][0] / pa, t["ci95_diff"][1] / pa]
# Sample size for 10% relative lift from control rate
R["sample_size_10pct"] = bc.ab_sample_size(pa, 0.10, 0.05, 0.8, True)
R["sample_size_observed_lift"] = bc.ab_sample_size(pa, t["lift"], 0.05, 0.8, True)
# Power of the current test to detect the observed lift (normal approx, unpooled SE, both tails)
se_u = math.sqrt(pa * (1 - pa) / na + pb * (1 - pb) / nb)
d = pb - pa
R["power_observed_lift"] = bc.norm_cdf(d / se_u - z975) + bc.norm_cdf(-d / se_u - z975)
# Sample-ratio mismatch check (expected 50/50)
exp = (na + nb) / 2
srm = (na - exp) ** 2 / exp + (nb - exp) ** 2 / exp
R["srm_chisq_p"] = [srm, 2 * (1 - bc.norm_cdf(math.sqrt(srm)))]
# Power for a true 10% relative lift at current n
p2 = pa * 1.10
se10 = math.sqrt(pa * (1 - pa) / na + p2 * (1 - p2) / nb)
R["power_10pct_lift_current_n"] = bc.norm_cdf((p2 - pa) / se10 - z975)

# ---- (b) Unit economics ----
arpu, gm, churn, disc, cac = 79, 0.65, 0.045, 0.01, 310
R["ltv_undiscounted"] = bc.ltv(arpu, gm, churn, 0.0, cac)          # GM*ARPU/churn
R["ltv_discounted_end"] = bc.ltv(arpu, gm, churn, disc, cac)        # = GM*ARPU/(churn+d), end-of-month cash
m = arpu * gm
R["ltv_discounted_start"] = m * (1 + disc) / (churn + disc)          # start-of-month convention, for reference
R["ltv_discounted_start_ltv_cac"] = R["ltv_discounted_start"] / cac
# Cross-check closed form vs long-horizon sum in boardcalc
R["ltv_discounted_sum_600m"] = bc.ltv(arpu, gm, churn, disc, cac, max_months=600)["ltv"]

# ---- (c) Price 79 -> 89 ----
# Immediate MRR-neutral subscriber loss (any base size; 1000 used as scale)
sp = bc.subscription_price_change(1000, 79, 89, churn, churn, gross_margin=1.0)
R["mrr_breakeven_loss_pct"] = sp["breakeven_immediate_loss_pct"]
# Steady state subs = new/churn. GP-neutral churn: c_new = c_old * GP_new / GP_old
# Rule 1 (recommended): COGS fixed at 27.65/sub -> GP/sub 51.35 -> 61.35 (pass GP/sub as "price", gm=1)
cogs = 0.35 * 79
r1 = bc.subscription_price_change(1000, 79 - cogs, 89 - cogs, churn, churn, new_subs_per_month=45, gross_margin=1.0)
R["fixed_cogs_gp_per_sub"] = [79 - cogs, 89 - cogs]
R["fixed_cogs_breakeven_churn"] = r1["breakeven_churn_for_steady_state"]
R["fixed_cogs_volume_rule"] = bc.price_change_breakeven(79, cogs, 10 / 79)
# Rule 2: margin held at 65% of price -> GP/sub 51.35 -> 57.85
r2 = bc.subscription_price_change(1000, 79, 89, churn, churn, new_subs_per_month=45, gross_margin=gm)
R["pct_margin_breakeven_churn"] = r2["breakeven_churn_for_steady_state"]
# Verify: steady-state GP equal at breakeven churn (45 new/month illustrative)
v1 = bc.subscription_price_change(1000, 79 - cogs, 89 - cogs, churn, R["fixed_cogs_breakeven_churn"], new_subs_per_month=45)
v2 = bc.subscription_price_change(1000, 79, 89, churn, R["pct_margin_breakeven_churn"], new_subs_per_month=45, gross_margin=gm)
R["verify_ss_gp_fixed"] = [v1["steady_state_gm_old"], v1["steady_state_gm_new"]]
R["verify_ss_gp_pct"] = [v2["steady_state_gm_old"], v2["steady_state_gm_new"]]
# Unit economics at 89 (fixed COGS), current churn and at breakeven churn
R["ltv_89_fixed_cogs_disc"] = bc.ltv(89, (89 - cogs) / 89, churn, disc, cac)
print(json.dumps(bc._clean(R), indent=2))
