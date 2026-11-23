#!/usr/bin/env python3
"""Independent expected answers for the expert test cases.

Written separately from scripts/boardcalc.py and does NOT import it. It uses numpy polynomial roots
for IRR, statistics.NormalDist for normal quantiles, explicit closed forms and a fresh
three-statement loop. Output: expected.json
"""
import json
import math
from statistics import NormalDist

import numpy as np

N = NormalDist()
OUT = {}


def npv(r, cf):
    return sum(c / (1 + r) ** t for t, c in enumerate(cf))


def irr_np(cf):
    # NPV polynomial in x = 1/(1+r): sum c_t x^t = 0
    roots = np.roots(list(reversed(cf)))
    rs = sorted(1 / x.real - 1 for x in roots if abs(x.imag) < 1e-10 and x.real > 0)
    return [r for r in rs if -0.99 < r < 10]


def mirr(cf, fr, rr):
    n = len(cf) - 1
    pvn = sum(c / (1 + fr) ** t for t, c in enumerate(cf) if c < 0)
    fvp = sum(c * (1 + rr) ** (n - t) for t, c in enumerate(cf) if c > 0)
    return (fvp / -pvn) ** (1 / n) - 1


def payback(cf, r=None):
    cum = 0
    for t, c in enumerate(cf):
        v = c if r is None else c / (1 + r) ** t
        if t and cum < 0 <= cum + v:
            return t - 1 + (-cum) / v
        cum += v


# ---------------- T1 three-statement (fresh implementation)
rev0 = 24e6
cash, ar, inv, ppe, ap, debt, eq, rv = 2e6, 2.6e6, 1.9e6, 9e6, 1.5e6, 6e6, 8e6, 0.0
g, capexp = [.18, .12, .08], [.09, .07, .05]
t1 = []
r = rev0
for y in range(3):
    r = r * (1 + g[y]); cogs = r * .62; ebitda = r * .38 - r * .22; da = r * .04; ebit = ebitda - da
    intr = debt * .08 + rv * .10; ebt = ebit - intr; tax = max(0, ebt) * .2; ni = ebt - tax
    ar1, inv1, ap1 = r * 40 / 365, cogs * 55 / 365, cogs * 35 / 365
    cfo = ni + da - (ar1 - ar) - (inv1 - inv) + (ap1 - ap)
    capex = r * capexp[y]; rep = min(1e6, debt); div = .25 * max(ni, 0)
    pre = cash + cfo - capex - rep - div
    if pre < 1.5e6:
        draw = 1.5e6 - pre
    else:
        draw = -min(rv, pre - 1.5e6)
    cash = pre + draw; rv += draw; debt -= rep; eq += ni - div; ppe += capex - da
    ar, inv, ap = ar1, inv1, ap1
    bal = (cash + ar + inv + ppe) - (ap + debt + rv + eq)
    t1.append(dict(year=y + 1, revenue=r, ebitda=ebitda, net_income=ni, cfo=cfo, cash=cash, revolver=rv, debt=debt, equity=eq, balance=bal))
OUT["T1"] = t1

# ---------------- T2 DCF
bu = 1.10 / (1 + .8 * .30); bl = bu * (1 + .8 * .25)
ke = .05 + bl * .055 + .01
wd, we = .25 / 1.25, 1 / 1.25
w = we * ke + wd * .07 * .8
revs = [50e6]
for gg in [.12, .10, .08, .06, .05]:
    revs.append(revs[-1] * (1 + gg))
fcff = []
for t in range(1, 6):
    R = revs[t]
    fcff.append(R * .18 * .8 + R * .04 - R * .06 - .15 * (R - revs[t - 1]))
pv = sum(f / (1 + w) ** (t + 1) for t, f in enumerate(fcff))
tv_g = fcff[-1] * 1.03 / (w - .03)
ebitda5 = revs[5] * .22
tv_m = 9 * ebitda5
ev_g = pv + tv_g / (1 + w) ** 5; ev_m = pv + tv_m / (1 + w) ** 5
sens = {}
for dw in (-.01, 0, .01):
    for gg in (.02, .03, .04):
        ww = w + dw
        ev = sum(f / (1 + ww) ** (t + 1) for t, f in enumerate(fcff)) + fcff[-1] * (1 + gg) / (ww - gg) / (1 + ww) ** 5
        sens["wacc%+.0f%%_g%.0f%%" % (dw * 100, gg * 100)] = (ev - 20e6) / 10e6
OUT["T2"] = dict(beta_unlevered=bu, beta_relevered=bl, cost_of_equity=ke, wacc=w, fcff=fcff,
                 ev_gordon=ev_g, ev_exit=ev_m, per_share_gordon=(ev_g - 20e6) / 10e6, per_share_exit=(ev_m - 20e6) / 10e6,
                 tv_share_gordon=tv_g / (1 + w) ** 5 / ev_g, tv_share_exit=tv_m / (1 + w) ** 5 / ev_m,
                 implied_exit_multiple_gordon=tv_g / ebitda5, implied_g_exit=(tv_m * w - fcff[-1]) / (tv_m + fcff[-1]),
                 sensitivity_per_share=sens)


# ---------------- T3 feasibility (fresh build)
def projA(units1=40000, price1=95, vc=.58, fixed1=650000, capex=2.4e6):
    cf = [-capex]; nwc_prev = 0
    for t in range(1, 7):
        R = units1 * 1.05 ** (t - 1) * price1 * 1.02 ** (t - 1)
        dep = capex / 6
        ebit = R * (1 - vc) - fixed1 * 1.03 ** (t - 1) - dep
        nwc = .12 * R
        c = ebit * .8 + dep - (nwc - nwc_prev); nwc_prev = nwc
        if t == 6:
            c += 200000 * .8 + nwc
        cf.append(c)
    return cf


A = projA(); B = [-1.1e6, 380000, 400000, 420000, 380000]
af = lambda r, n: (1 - (1 + r) ** -n) / r
OUT["T3"] = {}
for name, cf in (("A", A), ("B", B)):
    n = len(cf) - 1; v = npv(.11, cf)
    OUT["T3"][name] = dict(cashflows=cf, npv=v, irr=irr_np(cf), mirr=mirr(cf, .11, .11), payback=payback(cf),
                           disc_payback=payback(cf, .11), pi=sum(c / 1.11 ** t for t, c in enumerate(cf) if t) / -cf[0],
                           eaa=v / af(.11, n))

# ---------------- T4 stress
base = npv(.11, A)
torn = {}
for k, lo, hi in (("units1", 36000, 44000), ("price1", 85.5, 104.5), ("vc", .522, .638), ("fixed1", 585000, 715000), ("capex", 2.16e6, 2.64e6)):
    torn[k] = (npv(.11, projA(**{k: lo})), npv(.11, projA(**{k: hi})))
# NPV is linear in price1 and in units1 -> exact break-even by linear interpolation
def be(k, a, b):
    fa, fb = npv(.11, projA(**{k: a})), npv(.11, projA(**{k: b}))
    return a - fa * (b - a) / (fb - fa)
be_p, be_u = be("price1", 80, 100), be("units1", 30000, 50000)
comb = npv(.11, projA(units1=30000, price1=87.4, vc=.62, fixed1=715000))
rng = np.random.default_rng(12345); n = 200000
p = rng.triangular(85, 95, 100, n); u = rng.normal(40000, 6000, n); vcs = rng.triangular(.55, .58, .64, n)
# vectorised projA
t = np.arange(1, 7)
Rm = (u[:, None] * 1.05 ** (t - 1)) * (p[:, None] * 1.02 ** (t - 1))
dep = 2.4e6 / 6
ebit = Rm * (1 - vcs[:, None]) - 650000 * 1.03 ** (t - 1) - dep
nwc = .12 * Rm; dn = np.diff(np.concatenate([np.zeros((n, 1)), nwc], axis=1), axis=1)
cfm = ebit * .8 + dep - dn
cfm[:, 5] += 200000 * .8 + nwc[:, 5]
npvs = -2.4e6 + (cfm / 1.11 ** t).sum(axis=1)
OUT["T4"] = dict(base_npv=base, tornado=torn, breakeven_price=be_p, price_headroom=be_p / 95 - 1, breakeven_units=be_u,
                 units_headroom=be_u / 40000 - 1, combined_downside_npv=comb, mc_mean=float(npvs.mean()),
                 mc_prob_negative=float((npvs < 0).mean()), mc_p5=float(np.percentile(npvs, 5)))


# ---------------- T5 COO
def erlang(lam, mu, c):
    a = lam / mu
    if a >= c:
        return None
    s = sum(a ** k / math.factorial(k) for k in range(c)); top = a ** c / math.factorial(c) * c / (c - a)
    pw = top / (s + top); wq = pw / (c * mu - lam)
    return dict(c=c, util=a / c, p_wait=pw, mean_wait_min=wq * 60, sl_3min=1 - pw * math.exp(-(c * mu - lam) * 0.05))
st = {c: erlang(180, 15, c) for c in range(12, 18)}
need = min(c for c, v in st.items() if v and v["sl_3min"] >= .8)
z = N.inv_cdf(.95); ss = z * math.sqrt(5 * 300 ** 2 + (1200 * 1) ** 2)
OUT["T5"] = dict(stations_12=st[12], stations_needed=need, at_needed=st[need], safety_stock=ss, reorder_point=1200 * 5 + ss,
                 eoq=math.sqrt(2 * 1200 * 360 * 450 / .12), oee=(540 / 600) * (0.5 * 950 / 540) * (900 / 950))

# ---------------- T6 CMO
pa, pb = 213 / 5200, 235 / 5100; pp = (213 + 235) / (5200 + 5100)
zz = (pb - pa) / math.sqrt(pp * (1 - pp) * (1 / 5200 + 1 / 5100))
p1 = pa; p2 = pa * 1.1; pbar = (p1 + p2) / 2
nn = (N.inv_cdf(.975) * math.sqrt(2 * pbar * (1 - pbar)) + N.inv_cdf(.8) * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2 / (p2 - p1) ** 2
m = 79 * .65
OUT["T6"] = dict(rate_a=pa, rate_b=pb, relative_lift=pb / pa - 1, z=zz, p_value=2 * (1 - N.cdf(abs(zz))), n_per_arm=math.ceil(nn),
                 ltv=m / (0.01 + 0.045), ltv_cac=m / 0.055 / 310, cac_payback_months=310 / m,
                 breakeven_immediate_loss=1 - 79 / 89, breakeven_churn=0.045 * 89 / 79)

# ---------------- T7 CSO
seg = {"small": 9000 * 8, "medium": 1400 * 45, "large": 220 * 300}
tam = {k: v * .6 * 16 * 12 * 10 for k, v in seg.items()}
T = sum(tam.values())
h = sum(s * s for s in [32, 24, 14, 10, 8] + [1] * 12)
opts = {"organic": [6, 7, 8, 4], "partnership": [7, 6, 7, 8], "acquire": [9, 4, 3, 7]}
wts = [.35, .25, .20, .20]
def scores(ws):
    s = sum(ws); return {k: sum(a * b for a, b in zip(v, ws)) / s for k, v in opts.items()}
sc = scores(wts); win = max(sc, key=sc.get)
flips = []
for i in range(4):
    for d in (-.2, .2):
        w2 = list(wts); w2[i] *= 1 + d; s2 = scores(w2); w_ = max(s2, key=s2.get)
        if w_ != win:
            flips.append((i, d, w_))
OUT["T7"] = dict(tam_by_segment=tam, tam=T, sam=T * .35, som=T * .35 * .04, hhi=h, scores=sc, winner=win, rank_flips=flips)

# ---------------- T8 planted-errors truth
truth = json.load(open(__file__.replace("expected.py", "fixtures/planted_truth.json")))
OUT["T8"] = dict(planted_errors=[
    "E1 FCFE discounted at WACC (rate/cash-flow mismatch; should use cost of equity)",
    "E2 terminal growth 8% with WACC 11% (unrealistic; TV dominates value)",
    "E3 NWC omitted despite 45% growth",
    "E4 arithmetic: stated NPV %.0f vs %.0f computed with their own inputs" % (truth["npv_stated"], truth["npv_their_method_correct"]),
    "E5 IRR presented as decisive although cash flows change sign 3 times (refit in Y3) / IRR unverified",
    "E6 45%%/yr growth for 5 years without evidence",
    "E7 tax 0%% unjustified (zakat/CIT)",
    "X1 xlsx: NPV formula discounts t0 (=NPV(0.11,B9:G9))",
    "X2 xlsx: SUM(C4:F4) omits Y5 revenue",
    "X3 xlsx: G5 EBITDA hard-coded 3,300,000 instead of formula (3,315,380)"],
    npv_their_inputs=truth["npv_their_method_correct"], npv_stated=truth["npv_stated"],
    their_cashflows_irrs=irr_np(truth["cf"][:5] + [truth["cf"][5] + truth["tv"]]))

json.dump(OUT, open(__file__.replace(".py", ".json"), "w"), indent=1, default=float)
print(json.dumps(OUT, indent=1, default=float)[:6000])
