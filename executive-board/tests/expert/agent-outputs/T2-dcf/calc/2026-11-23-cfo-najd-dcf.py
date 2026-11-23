"""Najd Logistics (FICTIONAL, illustrative) - FCFF DCF, SAR. All inputs are CEO-provided.
Re-run: python3 2026-11-23-cfo-najd-dcf.py
Formulas:
  Bu = BL/(1+(1-t)D/E); BL' = Bu*(1+(1-t)D/E'); Ke = rf + BL'*MRP + CRP
  WACC = E/V*Ke + D/V*Kd*(1-t)
  FCFF = EBIT(1-t) + D&A - Capex - dNWC; DF_t = (1+WACC)^-t (end-year)
  TV_gordon = FCFF5*(1+g)/(WACC-g); TV_exit = 9.0 * EBITDA5
  implied g (exit) = (TV*WACC - FCFF5)/(TV + FCFF5)
Manual model is cross-checked against boardcalc.dcf / capm / wacc / unlever_beta / relever_beta.
"""
import sys
sys.path.insert(0, "/home/user/Hassanshuaib/executive-board/scripts")
import boardcalc as bc

# ---- Inputs (CEO) ----
REV0 = 50_000_000.0
GROWTH = [0.12, 0.10, 0.08, 0.06, 0.05]
EBIT_M, TAX, DA_P, CAPEX_P, NWC_P = 0.18, 0.20, 0.04, 0.06, 0.15
RF, BETA_PEER, DE_PEER, DE_TGT, MRP, CRP = 0.05, 1.10, 0.30, 0.25, 0.055, 0.01
KD_PRE = 0.07
G, EXIT_MULT = 0.03, 9.0
NET_DEBT, SHARES = 20_000_000.0, 10_000_000.0

# ---- Cost of capital ----
bu = BETA_PEER / (1 + (1 - TAX) * DE_PEER)
bl = bu * (1 + (1 - TAX) * DE_TGT)
ke = RF + bl * MRP + CRP
dv = DE_TGT / (1 + DE_TGT); ev_w = 1 - dv
kd_at = KD_PRE * (1 - TAX)
wacc = ev_w * ke + dv * kd_at

# ---- Projections ----
def project(wacc_rate, ebit_m=EBIT_M):
    rows, rev_prev, nwc_prev = [], REV0, NWC_P * REV0
    for t, gr in enumerate(GROWTH, 1):
        rev = rev_prev * (1 + gr)
        ebit = ebit_m * rev; nopat = ebit * (1 - TAX)
        da = DA_P * rev; capex = CAPEX_P * rev
        nwc = NWC_P * rev; dnwc = nwc - nwc_prev
        fcff = nopat + da - capex - dnwc
        df = (1 + wacc_rate) ** -t
        rows.append(dict(t=t, rev=rev, ebit=ebit, nopat=nopat, da=da, capex=capex,
                         dnwc=dnwc, fcff=fcff, df=df, pv=fcff * df, ebitda=ebit + da))
        rev_prev, nwc_prev = rev, nwc
    return rows

def value(wacc_rate, g=G, mult=EXIT_MULT, ebit_m=EBIT_M):
    r = project(wacc_rate, ebit_m)
    pv_exp = sum(x["pv"] for x in r)
    f5, e5, df5 = r[-1]["fcff"], r[-1]["ebitda"], r[-1]["df"]
    out = {}
    for name, tv in (("Gordon", f5 * (1 + g) / (wacc_rate - g)), ("Exit 9.0x", mult * e5)):
        ev = pv_exp + tv * df5; eq = ev - NET_DEBT
        out[name] = dict(tv=tv, pv_tv=tv * df5, ev=ev, eq=eq, ps=eq / SHARES, tv_pct=tv * df5 / ev)
    return r, pv_exp, out

rows, pv_exp, res = value(wacc)
f5, e5 = rows[-1]["fcff"], rows[-1]["ebitda"]
tv_g, tv_x = res["Gordon"]["tv"], res["Exit 9.0x"]["tv"]
impl_mult = tv_g / e5
impl_g = (tv_x * wacc - f5) / (tv_x + f5)

# ---- Output ----
print(f"Bu={bu:.4f} BL={bl:.4f} Ke={ke:.4%} Kd_at={kd_at:.2%} D/V={dv:.2f} WACC={wacc:.4%}")
print("Yr | Revenue | EBIT | NOPAT | D&A | Capex | dNWC | FCFF | DF | PV  (SAR m)")
for x in rows:
    print(f"Y{x['t']} | " + " | ".join(f"{x[k]/1e6:,.3f}" for k in
          ("rev", "ebit", "nopat", "da", "capex", "dnwc", "fcff")) + f" | {x['df']:.4f} | {x['pv']/1e6:,.3f}")
print(f"PV explicit FCFF = {pv_exp/1e6:,.3f}m; EBITDA5 = {e5/1e6:,.3f}m; FCFF6 = {f5*(1+G)/1e6:,.3f}m")
for k, m in res.items():
    print(f"{k}: TV={m['tv']/1e6:,.3f}m PV_TV={m['pv_tv']/1e6:,.3f}m EV={m['ev']/1e6:,.3f}m "
          f"Equity={m['eq']/1e6:,.3f}m /share={m['ps']:.2f} TV%EV={m['tv_pct']:.1%}")
gap = (res["Exit 9.0x"]["ev"] - res["Gordon"]["ev"]) / res["Gordon"]["ev"]
print(f"Implied exit multiple (Gordon) = {impl_mult:.2f}x; implied g (exit) = {impl_g:.3%}; "
      f"EV gap exit vs Gordon = {gap:+.1%}")

# Economic consistency: implied RONIC in terminal = g / reinvestment rate (Y5 reinvestment carried forward)
nopat5 = rows[-1]["nopat"]; rr5 = 1 - f5 / nopat5
print(f"Y5 reinvestment rate = {rr5:.1%}; implied RONIC at g=3% = {G/rr5:.1%}; at implied g = {impl_g/rr5:.1%}")

# ---- Sensitivity: Gordon value per share, WACC +-1% x g ----
print("WACC \\ g | 2% | 3% | 4%")
for w in (wacc - 0.01, wacc, wacc + 0.01):
    print(f"{w:.2%} | " + " | ".join(f"{value(w, g)[2]['Gordon']['ps']:.2f}" for g in (0.02, 0.03, 0.04)))
print("Exit multiple per share: " + ", ".join(f"{m:.0f}x={value(wacc, mult=m)[2]['Exit 9.0x']['ps']:.2f}"
                                             for m in (7, 8, 9, 10, 11)))
print("EBIT margin (Gordon / Exit) per share: " + ", ".join(
    f"{em:.0%}={value(wacc, ebit_m=em)[2]['Gordon']['ps']:.2f}/{value(wacc, ebit_m=em)[2]['Exit 9.0x']['ps']:.2f}"
    for em in (0.15, 0.18, 0.21)))

# ---- Integrity checks ----
chk = []
chk.append(abs(bc.unlever_beta(BETA_PEER, DE_PEER, TAX) - bu) < 1e-12)
chk.append(abs(bc.relever_beta(bu, DE_TGT, TAX) - bl) < 1e-12)
chk.append(abs(bc.capm(RF, bl, MRP, country_risk_premium=CRP) - ke) < 1e-12)
chk.append(abs(bc.wacc(0.80, 0.20, ke, KD_PRE, TAX) - wacc) < 1e-12)
d = bc.dcf([x["fcff"] for x in rows], wacc, terminal_growth=G, exit_multiple=EXIT_MULT,
           terminal_metric=e5, net_debt=NET_DEBT, shares=SHARES)
chk.append(abs(d["methods"]["gordon"]["per_share"] - res["Gordon"]["ps"]) < 1e-9)
chk.append(abs(d["methods"]["exit_multiple"]["per_share"] - res["Exit 9.0x"]["ps"]) < 1e-9)
chk.append(abs(d["exit_implied_growth"] - impl_g) < 1e-12)
chk.append(abs(d["gordon_implied_exit_multiple"] - impl_mult) < 1e-12)
# Round trips: Gordon at implied g reproduces exit TV; exit at implied multiple reproduces Gordon TV
chk.append(abs(value(wacc, g=impl_g)[2]["Gordon"]["tv"] - tv_x) < 1e-3)
chk.append(abs(value(wacc, mult=impl_mult)[2]["Exit 9.0x"]["tv"] - tv_g) < 1e-3)
# Cumulative dNWC = NWC5 - NWC0
chk.append(abs(sum(x["dnwc"] for x in rows) - NWC_P * (rows[-1]["rev"] - REV0)) < 1e-6)
print(f"boardcalc method gap = {d['method_gap']:.1%}; warnings = {d['warnings']}")
print(f"Checks passed: {sum(chk)}/{len(chk)}")
