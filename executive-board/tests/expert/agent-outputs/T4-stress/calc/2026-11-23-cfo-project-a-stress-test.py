"""Project A stress test (fictional, SAR). Re-run: python3 <this file>
Formulas per year t=1..6:
  Rev_t = V1*1.05^(t-1) * P1*1.02^(t-1);  VC_t = vc*Rev_t;  FC_t = F1*1.03^(t-1)
  EBIT_t = Rev - VC - FC - Dep (Dep = Capex/6);  Tax = 20%*EBIT (negative = tax saving)
  OCF_t = EBIT*(1-T) + Dep
  NWC balance B_t = 12%*Rev_t.
  Base convention (BEG): B_1 invested at t=0; at t=1..5 invest B_{t+1}-B_t; recover B_6 at t=6.
  Alt convention (END): change B_t - B_{t-1} at t (B_0=0); recover B_6 at t=6 (net zero at t=6).
  After-tax salvage at t=6 = 200,000*(1-0.2) = 160,000 (book value 0). Salvage fixed when capex flexes.
  NPV = sum CF_t/1.11^t.
"""
import sys, json, random, statistics as st
sys.path.insert(0, "/home/user/Hassanshuaib/executive-board/scripts")
import boardcalc as bc

BASE = dict(V1=40000, P1=95.0, vc=0.58, F1=650000.0, capex=2400000.0)
T, R, N, gV, gP, gF, NWC, SALV = 0.20, 0.11, 6, 0.05, 0.02, 0.03, 0.12, 200000.0


def flows(V1, P1, vc, F1, capex, conv="BEG", detail=False):
    dep = capex / N
    rev = [V1 * (1 + gV) ** (t - 1) * P1 * (1 + gP) ** (t - 1) for t in range(1, N + 1)]
    B = [NWC * r for r in rev]
    cf = [-capex] + [0.0] * N
    rows = []
    for t in range(1, N + 1):
        r = rev[t - 1]; v = vc * r; f = F1 * (1 + gF) ** (t - 1)
        ebit = r - v - f - dep; tax = T * ebit; ocf = ebit - tax + dep
        cf[t] += ocf
        rows.append(dict(t=t, rev=r, vc=v, fc=f, dep=dep, ebit=ebit, tax=tax, ocf=ocf))
    nf = [0.0] * (N + 1)
    if conv == "BEG":
        nf[0] = -B[0]
        for t in range(1, N):
            nf[t] = -(B[t] - B[t - 1])
        nf[N] += B[N - 1]
    else:
        prev = 0.0
        for t in range(1, N + 1):
            nf[t] = -(B[t - 1] - prev); prev = B[t - 1]
        nf[N] += B[N - 1]
    cf = [c + n for c, n in zip(cf, nf)]
    cf[N] += SALV * (1 - T)
    return (cf, rows, nf) if detail else cf


def pv(cf):  # manual NPV, method 2
    return sum(c / (1 + R) ** t for t, c in enumerate(cf))


def bc_npv(cf):  # boardcalc NPV, method 1
    r = bc.npv(R, cf)
    return r["npv"] if isinstance(r, dict) else r


def npv(**kw):
    return pv(flows(**{**BASE, **kw}))


def metrics(cf):
    return dict(npv=bc_npv(cf), irr=bc.irr(cf), payback=bc.payback(cf), disc_payback=bc.payback(cf, R))


out = {}
cf, rows, nf = flows(**BASE, detail=True)
out["base_cf"] = cf; out["rows"] = rows; out["nwc_flow"] = nf
# Method 3: PV decomposition
pv_ebitda = sum((r["rev"] - r["vc"] - r["fc"]) * (1 - T) / (1 + R) ** r["t"] for r in rows)
pv_shield = sum(T * r["dep"] / (1 + R) ** r["t"] for r in rows)
pv_nwc = pv(nf); pv_salv = SALV * (1 - T) / (1 + R) ** N
out["base_npv_checks"] = dict(boardcalc=bc_npv(cf), manual=pv(cf),
                              decomposition=-BASE["capex"] + pv_ebitda + pv_shield + pv_nwc + pv_salv,
                              parts=dict(pv_aftertax_EBITDA=pv_ebitda, pv_dep_shield=pv_shield,
                                         pv_nwc=pv_nwc, pv_salvage=pv_salv))
out["base"] = metrics(cf)
cf_end = flows(**BASE, conv="END")
out["alt_conv"] = dict(cf=cf_end, npv=pv(cf_end), irr=bc.irr(cf_end))

# 1 Tornado (+/-10% relative)
torn = []
for k in ["V1", "P1", "vc", "F1", "capex"]:
    lo, hi = npv(**{k: BASE[k] * 0.9}), npv(**{k: BASE[k] * 1.1})
    torn.append(dict(driver=k, low_in=BASE[k] * 0.9, npv_low=lo, high_in=BASE[k] * 1.1, npv_high=hi, swing=abs(hi - lo)))
torn.sort(key=lambda x: -x["swing"]); out["tornado"] = torn


# 2 Reverse stress (bisection)
def bisect(k, lo, hi):
    for _ in range(200):
        m = (lo + hi) / 2
        if npv(**{k: m}) > 0: hi = m
        else: lo = m
    return (lo + hi) / 2


beP, beV = bisect("P1", 1, 95), bisect("V1", 1, 40000)
out["breakeven"] = dict(P1=beP, P1_headroom=1 - beP / 95, V1=beV, V1_headroom=1 - beV / 40000,
                        npv_at_beP=npv(P1=beP), npv_at_beV=npv(V1=beV))

# 3 Combined downside
cfd = flows(V1=30000, P1=87.4, vc=0.62, F1=715000, capex=2400000)
out["downside"] = dict(cf=cfd, **metrics(cfd))

# 4 Monte Carlo
SEED, M = 20261123, 20000
rng = random.Random(SEED); res = []; trunc = 0
for _ in range(M):
    p = rng.triangular(85, 100, 95)          # Python signature: (low, high, mode)
    v = rng.gauss(40000, 6000)
    if v < 0:
        v = 0.0; trunc += 1
    c = rng.triangular(0.55, 0.64, 0.58)
    res.append(pv(flows(V1=v, P1=p, vc=c, F1=650000, capex=2400000)))
res.sort()
q = lambda a: res[int(round(a * (M - 1)))]
mP, mC = (85 + 95 + 100) / 3, (0.55 + 0.58 + 0.64) / 3
out["mc"] = dict(n=M, seed=SEED, mean=st.mean(res), median=st.median(res), sd=st.pstdev(res),
                 p_neg=sum(r < 0 for r in res) / M, p5=q(0.05), p95=q(0.95), truncations=trunc,
                 npv_at_base=npv(), mean_price=mP, mean_vc=mC, npv_at_input_means=npv(P1=mP, vc=mC))
print(json.dumps(out, indent=1, default=str))
