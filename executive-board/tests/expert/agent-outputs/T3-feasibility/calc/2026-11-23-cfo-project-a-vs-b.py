"""CFO: Project A vs B (mutually exclusive, repeatable). SAR. Illustrative case.
Re-run: python3 2026-11-23-cfo-project-a-vs-b.py
Formulas:
  Rev_t = 40,000*1.05^(t-1) * 95*1.02^(t-1); Var = 58% Rev; Fixed_t = 650,000*1.03^(t-1); Dep = 400,000
  EBIT = Rev - Var - Fixed - Dep; Tax = 20% EBIT (negative = tax saving); NOPAT = EBIT - Tax
  NWC balance = 12% Rev. Conv "Y1": dNWC_t = NWC_t - NWC_(t-1), NWC_0 = 0, full balance recovered at t6.
  Conv "t0": balance needed at START of year t (i.e. held at t-1): outflow at t-1, recovered at t6.
  FCF = NOPAT + Dep - dNWC - Capex + after-tax salvage + NWC recovery
  NPV = sum CF_t/(1+r)^t; IRR: NPV=0; MIRR = (FV+ @11% / PV- @11%)^(1/n) - 1; PI = PV(CF1..n)/|CF0|
  EAA = NPV / [(1-(1+r)^-n)/r]; Chain(12y) = NPV * sum_k (1+r)^(-k*n), k=0..12/n-1
"""
import sys
sys.path.insert(0, "<repo>/executive-board/scripts")
import boardcalc as bc

R, T = 0.11, 0.20
B = [-1_100_000, 380_000, 400_000, 420_000, 380_000]


def project_a(price=95.0, units=40_000, var=0.58, fixed=650_000, nwc_pct=0.12, conv="Y1", capex=2_400_000, salvage=200_000):
    n, dep = 6, capex / 6
    rows = []
    for t in range(1, n + 1):
        rev = units * 1.05 ** (t - 1) * price * 1.02 ** (t - 1)
        vc, fc = var * rev, fixed * 1.03 ** (t - 1)
        ebit = rev - vc - fc - dep
        tax = T * ebit
        rows.append(dict(t=t, rev=rev, vc=vc, fc=fc, dep=dep, ebit=ebit, tax=tax, nopat=ebit - tax, nwc=nwc_pct * rev))
    cf = [0.0] * (n + 1)
    dnwc = [0.0] * (n + 1)
    for r in rows:
        prev = rows[r["t"] - 2]["nwc"] if r["t"] > 1 else 0.0
        k = r["t"] if conv == "Y1" else r["t"] - 1          # timing of the investment
        dnwc[k] -= r["nwc"] - prev
    sal_at = salvage - T * (salvage - 0)                    # book value zero at t6
    rec = rows[-1]["nwc"]
    cf[0] = -capex + dnwc[0]
    for r in rows:
        t = r["t"]
        cf[t] = r["nopat"] + r["dep"] + dnwc[t] + (sal_at + rec if t == n else 0)
    return rows, dnwc, sal_at, rec, cf


def metrics(cf, r=R):
    return dict(npv=bc.npv(r, cf), irr=bc.irr(cf)["irr"], mirr=bc.mirr(cf, r, r), pb=bc.payback(cf),
                dpb=bc.payback(cf, r), pi=bc.profitability_index(r, cf), eaa=bc.eaa(r, cf), n=len(cf) - 1)


def chain(cf, horizon=12):
    n = len(cf) - 1
    out = [0.0] * (horizon + 1)
    for k in range(horizon // n):
        for t, c in enumerate(cf):
            out[k * n + t] += c
    return out


f = lambda x: f"{x:>12,.0f}"
rows, dnwc, sal_at, rec, A = project_a()
print("== Project A cash flow table (NWC conv: Y1) ==")
print("t0: capex -2,400,000 | FCF", f(A[0]))
hdr = "t   Revenue     VarCost     Fixed       Dep         EBIT        Tax         NOPAT       +Dep        dNWC        Salv(AT)    NWCrec      FCF"
print(hdr)
for r in rows:
    t = r["t"]
    s, nr = (sal_at, rec) if t == 6 else (0, 0)
    print(t, *map(f, [r["rev"], -r["vc"], -r["fc"], -r["dep"], r["ebit"], -r["tax"], r["nopat"], r["dep"], dnwc[t], s, nr, A[t]]))

# Integrity checks
ref = bc.project(life=6, units=40_000, unit_growth=0.05, price=95, price_growth=0.02, var_cost_pct=0.58, fixed_cost=650_000,
                 fixed_cost_growth=0.03, capex=2_400_000, salvage=200_000, nwc_pct=0.12, tax_rate=T, discount_rate=R)
assert max(abs(a - b) for a, b in zip(ref["cashflows"], A)) < 1e-6, "mismatch vs boardcalc.project"
assert abs(sum(dnwc) + rec) < 1e-6, "NWC not fully recovered"
assert abs(sum(A) - (sum(r["nopat"] for r in rows) + 0 * 1 + sal_at)) < 1e-6, "cash total != NOPAT + after-tax salvage"
assert abs(bc.npv(R, A[:0] + [A[0]] + A[1:]) - bc.npv(R, A)) < 1e-9
for p in (A, B):
    m = metrics(p)
    assert abs(bc.npv(m["irr"], p)) < 1e-3
print("Checks: A FCF == boardcalc.project (diff<1e-6); sum(dNWC)+recovery=0; sum(FCF)=sum(NOPAT)+AT salvage; NPV(IRR)=0")
print("A FCF:", [round(x) for x in A], " sum NOPAT:", round(sum(r['nopat'] for r in rows)), " sum FCF:", round(sum(A)))

print("\n== Metrics @11% ==")
cmp = bc.compare_projects(R, {"A": A, "B": B})
for k, cfs in (("A", A), ("B", B)):
    m = metrics(cfs)
    ch = chain(cfs)
    print(k, {x: round(v, 4) for x, v in m.items()}, "| chain12 NPV:", round(bc.npv(R, ch)), "| chain EAA:", round(bc.eaa(R, ch)))
print("compare_projects notes:", cmp.get("notes"), "| crossover(A-B one cycle):", cmp.get("crossover"))
diff12 = [a - b for a, b in zip(chain(A), chain(B))]
print("12y chain A:", [round(x) for x in chain(A)])
print("12y chain B:", [round(x) for x in chain(B)])
print("Crossover rate (12y chains A-B):", bc.irr(diff12)["all_irrs"],
      "| one-cycle A-B diff IRRs:", bc.irr([a - b for a, b in zip(A, B + [0, 0])])["all_irrs"])
print("Incremental (A-B one cycle) NPV:", round(bc.npv(R, A) - bc.npv(R, B)), "| extra capex:", A[0] - B[0])

print("\n== Sensitivity: NWC timing ==")
for conv in ("Y1", "t0"):
    _, d, _, _, cf = project_a(conv=conv)
    m = metrics(cf)
    print(conv, [round(x) for x in cf], {x: round(v, 4) for x, v in m.items()}, "chain12", round(bc.npv(R, chain(cf))))

print("\n== Sensitivity: discount rate (NPV / EAA / chain12) ==")
for r in (0.08, 0.09, 0.10, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16):
    _, _, _, _, A0 = project_a(conv="t0")
    print(f"{r:.0%}", "A npv", f(bc.npv(r, A)), "eaa", f(bc.eaa(r, A)), "| A(t0) eaa", f(bc.eaa(r, A0)),
          "| B npv", f(bc.npv(r, B)), "eaa", f(bc.eaa(r, B)), "| chain A", f(bc.npv(r, chain(A))), "B", f(bc.npv(r, chain(B))))
eaa_gap = lambda r: bc.eaa(r, A) - bc.eaa(r, B)
lo, hi = 0.01, 0.40
for _ in range(200):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if eaa_gap(lo) * eaa_gap(mid) > 0 else (lo, mid)
print("Rate where EAA_A = EAA_B:", round(mid, 5))

print("\n== A operating scenarios (Y1 conv) ==")
sc = {"Base": {}, "Downside (price -5%, var 60%, vol -10%)": dict(price=95 * 0.95, var=0.60, units=36_000),
      "Upside (price +3%, var 57%, vol +5%)": dict(price=95 * 1.03, var=0.57, units=42_000)}
for name, kw in sc.items():
    cf = project_a(**kw)[4]
    m = metrics(cf)
    print(name, "NPV", f(m["npv"]), "IRR", round(m["irr"], 4), "EAA", f(m["eaa"]), "vs B EAA", f(bc.eaa(R, B)))
# break-even Y1 price where EAA_A = EAA_B, and where NPV_A = 0
for target, lab in ((bc.eaa(R, B), "EAA_A=EAA_B"), (0.0, "NPV_A=0")):
    lo, hi = 40.0, 95.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if bc.eaa(R, project_a(price=mid)[4]) < target: lo = mid
        else: hi = mid
    print("Break-even Y1 price for", lab, round(mid, 3), f"({mid/95-1:+.2%})")
    lo, hi = 0.50, 0.90
    for _ in range(200):
        mid = (lo + hi) / 2
        if bc.eaa(R, project_a(var=mid)[4]) > target: lo = mid
        else: hi = mid
    print("Break-even var-cost % for", lab, round(mid, 5))
# Combined stress: var 60% and volume -10%; Y1 price at which EAA_A = EAA_B (kill-criterion basis)
lo, hi = 40.0, 95.0
for _ in range(200):
    mid = (lo + hi) / 2
    if bc.eaa(R, project_a(price=mid, var=0.60, units=36_000)[4]) < bc.eaa(R, B): lo = mid
    else: hi = mid
print("Combined-stress price for EAA_A=EAA_B:", round(mid, 2), f"({mid/95-1:+.2%})")
