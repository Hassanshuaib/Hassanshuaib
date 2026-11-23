"""CRO independent recompute of the CFO Jeddah expansion analysis (2026-11-20).
Uses the verified boardcalc functions (npv, irr, mirr, payback, breakeven_input, tornado, stress,
montecarlo, recalc_compare) with a custom model registered for this project's cash-flow shape.
Run: python3 -I <this file>
"""
import json
import os
import sys

sys.path.insert(0, "/home/user/Hassanshuaib/executive-board/scripts")
import boardcalc as bc  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
XLSX = os.path.join(HERE, "..", "expansion-model.xlsx")

# Base = CFO memo inputs (user/CFO inputs, not CRO assumptions)
BASE = dict(rev1=3_000_000, growth=0.45, margin=0.25, tax=0.0, capex0=5_000_000, refit=2_500_000,
            refit_year=3, rate=0.11, g_tv=0.08, tv_maint=0.0, nwc_pct=0.0, dep_years=10,
            y5_ebitda=None, excel_shift=False, years=5)


def jeddah(**kw):
    p = dict(BASE); p.update(kw)
    n = int(p["years"]); dep = p["capex0"] / p["dep_years"]
    cfs, ebitdas, nwc_prev = [-p["capex0"]], [], 0.0
    for t in range(1, n + 1):
        rev = p["rev1"] * (1 + p["growth"]) ** (t - 1)
        e = rev * p["margin"]
        if t == n and p["y5_ebitda"] is not None:
            e = p["y5_ebitda"]                      # spreadsheet hardcode in G5
        tax = max(0.0, e - dep) * p["tax"]           # illustrative tax on EBIT (EBITDA less SL dep)
        nwc = rev * p["nwc_pct"]; dnwc = nwc - nwc_prev; nwc_prev = nwc
        cf = e - tax - dnwc - (p["refit"] if t == p["refit_year"] else 0.0)
        ebitdas.append(e); cfs.append(cf)
    tv_base = cfs[-1] - p["tv_maint"]                # normalised: deduct recurring refit/maintenance
    tv = tv_base * (1 + p["g_tv"]) / (p["rate"] - p["g_tv"])
    flows = cfs[:-1] + [cfs[-1] + tv]
    if p["excel_shift"]:                             # Excel =NPV(r, B9:G9): t=0 flow discounted one period
        v = bc.npv(p["rate"], [0.0] + flows)
    else:
        v = bc.npv(p["rate"], flows)
    pv_tv = tv / (1 + p["rate"]) ** n
    return {"cashflows": cfs, "tv": tv, "flows_with_tv": flows, "npv": v, "pv_tv": pv_tv,
            "tv_share_of_npv": pv_tv / v if v else None, "npv_ex_tv": v - pv_tv * (1 if not p["excel_shift"] else 1 / (1 + p["rate"]))}


bc._MODELS["jeddah"] = jeddah
out = {}

# 1. Memo replication
m = jeddah()
out["memo_replication"] = {
    "cashflows": m["cashflows"], "tv": m["tv"], "npv_correct_t0": m["npv"],
    "npv_excel_shift_error": jeddah(excel_shift=True)["npv"],
    "pv_tv": m["pv_tv"], "tv_share_of_npv": m["tv_share_of_npv"], "npv_ex_tv": m["npv_ex_tv"],
    "irr_with_tv": bc.irr(m["flows_with_tv"]), "irr_ex_tv": bc.irr(m["cashflows"]),
    "mirr_with_tv_11": bc.mirr(m["flows_with_tv"], 0.11, 0.11),
    "payback_ex_tv": bc.payback(m["cashflows"]),
    "tv_implied_ev_ebitda_y5": m["tv"] / (3_000_000 * 1.45 ** 4 * 0.25)}

# 2. Spreadsheet replication (G5 hardcode 3.3m, Excel NPV shift) + LibreOffice recalculation check
s = jeddah(y5_ebitda=3_300_000, excel_shift=True)
s_fix_npv = jeddah(y5_ebitda=3_300_000)["npv"]
exp = {"G5": 3_300_000, "G7": 3_300_000, "G8": s["tv"], "G9": 3_300_000 + s["tv"],
       "B11": sum(3_000_000 * 1.45 ** k for k in range(4)), "B12": s["npv"]}
out["spreadsheet"] = {"expected_cells": exp, "npv_xlsx_as_built": s["npv"], "npv_xlsx_t0_fixed": s_fix_npv,
                      "rev_total_5y_correct": sum(3_000_000 * 1.45 ** k for k in range(5)),
                      "recalc": bc.recalc_compare(os.path.abspath(XLSX), exp, sheet="Model", tol=1e-6)}

# 3. Reverse stress (NPV = 0), memo base
out["reverse_stress"] = {
    "growth": bc.breakeven_input(BASE, "growth", -0.5, 0.45, model="jeddah"),
    "margin": bc.breakeven_input(BASE, "margin", 0.0, 0.25, model="jeddah"),
    "rev1": bc.breakeven_input(BASE, "rev1", 0.0, 3_000_000, model="jeddah"),
    "rate": bc.breakeven_input(BASE, "rate", 0.0801, 2.0, model="jeddah"),
    "g_tv": bc.breakeven_input(BASE, "g_tv", -0.9, 0.08, model="jeddah")}
# with no terminal value at all (5-yr life, no salvage)
noTV = dict(BASE, g_tv=-1.0)  # g=-100% -> TV = 0
out["npv_no_tv"] = jeddah(**noTV)["npv"]
out["growth_breakeven_no_tv"] = bc.breakeven_input(noTV, "growth", -0.5, 2.0, model="jeddah")

# 4. Tornado on memo base
out["tornado"] = bc.tornado(BASE, {"growth": [0.15, 0.45], "margin": [0.15, 0.30], "g_tv": [0.02, 0.08],
                                   "rate": [0.11, 0.16], "tv_maint": [833_333, 0.0], "tax": [0.20, 0.0]},
                            model="jeddah")

# 5. Combined stresses (illustrative; CRO assumptions A1-A6 in the review)
adj = dict(g_tv=0.03, tv_maint=2_500_000 / 3)              # A1, A2
out["stress"] = bc.stress(BASE, {
    "A_tv_g3_refit_recurring": adj,
    "B_plus_rate13": {**adj, "rate": 0.13},
    "C_plus_tax20_illustrative": {**adj, "rate": 0.13, "tax": 0.20},
    "D_growth25_margin20": {**adj, "rate": 0.13, "growth": 0.25, "margin": 0.20},
    "E_growth15_margin18_tax20": {**adj, "rate": 0.13, "growth": 0.15, "margin": 0.18, "tax": 0.20},
    "F_nwc5pct": {**adj, "rate": 0.13, "nwc_pct": 0.05}}, model="jeddah")
ADJ = dict(BASE, **adj, rate=0.13)
out["adj_case"] = {k: jeddah(**ADJ)[k] for k in ("npv", "tv", "pv_tv", "tv_share_of_npv", "npv_ex_tv")}
out["adj_reverse_growth"] = bc.breakeven_input(ADJ, "growth", -0.5, 0.45, model="jeddah")
out["adj_reverse_margin"] = bc.breakeven_input(ADJ, "margin", 0.0, 0.25, model="jeddah")

# 6. Monte Carlo (illustrative ranges, A5)
out["montecarlo"] = bc.montecarlo(ADJ, {"growth": ["pert", 0.05, 0.25, 0.45], "margin": ["pert", 0.12, 0.20, 0.27],
                                        "g_tv": ["pert", 0.01, 0.03, 0.05], "rate": ["pert", 0.11, 0.13, 0.16]},
                                  n=10000, seed=42, model="jeddah")
print(json.dumps(bc._clean(out), indent=1, default=str))
