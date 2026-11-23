#!/usr/bin/env python3
"""boardcalc: an audited calculation engine for the AI Executive Board.

Pure Python (stdlib only). openpyxl is needed only for the Excel exports,
and LibreOffice only for recalculation checks. Every function is
deterministic (Monte Carlo takes a seed) and returns plain dicts/lists, so
results can be pasted into analyses and re-run by anyone.

CLI usage:
    python3 boardcalc.py list                      # list functions
    python3 boardcalc.py doc npv irr               # full docs of named functions
    python3 boardcalc.py <function> '<json kwargs>'
    python3 boardcalc.py <function> @inputs.json  # kwargs read from a file
    python3 boardcalc.py npv '{"rate":0.1,"cashflows":[-100,30,40,50,20]}'

Conventions:
    * Rates are decimals (0.10 = 10%).
    * cashflows[0] occurs at t = 0 (today); cashflows[t] at the end of year t.
    * Money is in whatever currency the inputs use; no FX conversion is done.

Tested by tests/test_boardcalc.py against closed-form results and against
LibreOffice spreadsheet formulas (NPV, IRR, MIRR, PMT, ...).
"""
import json
import math
import random
import sys

# ======================================================================
# helpers
# ======================================================================


def _f(x):
    return float(x)


def norm_cdf(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def norm_ppf(p):
    """Inverse standard normal CDF (Acklam's algorithm, |error| < 1.2e-9)."""
    if not 0.0 < p < 1.0:
        raise ValueError("p must be in (0,1)")
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00]
    pl, ph = 0.02425, 1 - 0.02425
    if p < pl:
        q = math.sqrt(-2 * math.log(p))
        return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    if p > ph:
        q = math.sqrt(-2 * math.log(1 - p))
        return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    q = p - 0.5
    r = q * q
    return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)


def _bisect(fn, lo, hi, tol=1e-12, it=300):
    flo, fhi = fn(lo), fn(hi)
    if flo == 0:
        return lo
    if fhi == 0:
        return hi
    if flo * fhi > 0:
        return None
    for _ in range(it):
        mid = (lo + hi) / 2
        fm = fn(mid)
        if abs(fm) < tol or (hi - lo) / 2 < tol:
            return mid
        if flo * fm < 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    return (lo + hi) / 2


def _series(v, n):
    """Scalar -> list of length n; list is padded with its last value."""
    if isinstance(v, (list, tuple)):
        v = list(v)
        if not v:
            raise ValueError("empty list")
        return [float(x) for x in (v + [v[-1]] * (n - len(v)))[:n]]
    return [float(v)] * n


# ======================================================================
# 1. Time value, capital budgeting
# ======================================================================


def npv(rate, cashflows):
    """NPV with cashflows[0] at t=0. (Excel: =CF0 + NPV(rate, CF1:CFn))"""
    r = _f(rate)
    return sum(_f(c) / (1 + r) ** t for t, c in enumerate(cashflows))


def irr(cashflows, lo=-0.99, hi=10.0, grid=2000):
    """All IRRs in [lo, hi] found by grid scan + bisection.

    Returns {irr: primary (the root closest to 0, or null), all_irrs, sign_changes, warning}.
    If there are multiple sign changes there can be multiple IRRs; then use NPV or MIRR.
    """
    cfs = [_f(c) for c in cashflows]
    signs = [c for c in cfs if c != 0]
    changes = sum(1 for a, b in zip(signs, signs[1:]) if (a > 0) != (b > 0))
    f = lambda r: npv(r, cfs)
    roots, prev_r, prev_v = [], lo, f(lo)
    for i in range(1, grid + 1):
        r = lo + (hi - lo) * i / grid
        v = f(r)
        if prev_v == 0:
            roots.append(prev_r)
        elif prev_v * v < 0:
            root = _bisect(f, prev_r, r)
            if root is not None:
                roots.append(root)
        prev_r, prev_v = r, v
    roots = sorted(set(round(x, 12) for x in roots))
    primary = min(roots, key=abs) if roots else None
    warn = None
    if changes == 0:
        warn = "No sign change: IRR undefined."
    elif changes > 1:
        warn = "%d sign changes: multiple or no IRR possible; decide on NPV/MIRR." % changes
    if len(roots) > 1:
        warn = "Multiple IRRs %s: IRR is not a valid decision rule here; use NPV/MIRR." % [round(x, 6) for x in roots]
    return {"irr": primary, "all_irrs": roots, "sign_changes": changes, "warning": warn}


def mirr(cashflows, finance_rate, reinvest_rate):
    """Modified IRR, identical to Excel MIRR(values, finance_rate, reinvest_rate)."""
    cfs = [_f(c) for c in cashflows]
    n = len(cfs) - 1
    pv_neg = sum(c / (1 + finance_rate) ** t for t, c in enumerate(cfs) if c < 0)
    fv_pos = sum(c * (1 + reinvest_rate) ** (n - t) for t, c in enumerate(cfs) if c > 0)
    if pv_neg == 0 or fv_pos == 0:
        return None
    return (fv_pos / -pv_neg) ** (1.0 / n) - 1


def payback(cashflows, rate=None):
    """Simple payback (rate=None) or discounted payback in years (linear interpolation within the year)."""
    cum, prev = 0.0, 0.0
    for t, c in enumerate(cashflows):
        v = _f(c) if rate is None else _f(c) / (1 + rate) ** t
        prev, cum = cum, cum + v
        if t > 0 and prev < 0 <= cum:
            return t - 1 + (-prev / v if v else 0)
    return None


def profitability_index(rate, cashflows):
    """PI = PV(future flows) / |initial outlay|."""
    return sum(_f(c) / (1 + rate) ** t for t, c in enumerate(cashflows) if t > 0) / abs(_f(cashflows[0]))


def annuity_factor(rate, n):
    return n if rate == 0 else (1 - (1 + rate) ** -n) / rate


def pmt(rate, n, pv, fv=0.0, when=0):
    """Payment per period, sign convention of Excel PMT (returns negative for a positive loan pv)."""
    if rate == 0:
        return -(pv + fv) / n
    f = (1 + rate) ** n
    return -(rate * (pv * f + fv)) / ((1 + rate * when) * (f - 1))


def eaa(rate, cashflows):
    """Equivalent annual annuity: compare projects with unequal lives."""
    n = len(cashflows) - 1
    return npv(rate, cashflows) / annuity_factor(rate, n)


def compare_projects(rate, projects, finance_rate=None, reinvest_rate=None):
    """Mutually exclusive projects: {name: cashflows}. Ranks by NPV and shows IRR/MIRR/PI/EAA,
    the crossover rate for each pair, and flags NPV-vs-IRR ranking conflicts and unequal lives."""
    fr = rate if finance_rate is None else finance_rate
    rr = rate if reinvest_rate is None else reinvest_rate
    rows = {}
    for name, cfs in projects.items():
        rows[name] = {"npv": npv(rate, cfs), "irr": irr(cfs)["irr"], "mirr": mirr(cfs, fr, rr),
                      "pi": profitability_index(rate, cfs), "eaa": eaa(rate, cfs),
                      "life": len(cfs) - 1, "payback": payback(cfs), "disc_payback": payback(cfs, rate)}
    names = list(projects)
    cross = {}
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = projects[names[i]], projects[names[j]]
            n = max(len(a), len(b))
            diff = [(a[t] if t < len(a) else 0) - (b[t] if t < len(b) else 0) for t in range(n)]
            cross["%s vs %s" % (names[i], names[j])] = irr(diff)["all_irrs"]
    by_npv = sorted(names, key=lambda k: -rows[k]["npv"])
    by_irr = sorted(names, key=lambda k: -(rows[k]["irr"] if rows[k]["irr"] is not None else -9))
    lives = {rows[k]["life"] for k in names}
    notes = []
    if by_npv[0] != by_irr[0]:
        notes.append("NPV and IRR rank differently (scale/timing). For mutually exclusive projects follow NPV.")
    if len(lives) > 1:
        notes.append("Unequal lives: compare EAA (if projects are repeatable) rather than raw NPV.")
    return {"projects": rows, "rank_by_npv": by_npv, "rank_by_irr": by_irr, "crossover_rates": cross, "notes": notes}


# ======================================================================
# 2. Cost of capital, value creation
# ======================================================================


def capm(rf, beta, mrp, size_premium=0.0, country_risk_premium=0.0, specific_risk=0.0):
    """Cost of equity = rf + beta*MRP + size + country + specific premia (premia are judgement inputs)."""
    return rf + beta * mrp + size_premium + country_risk_premium + specific_risk


def unlever_beta(levered_beta, debt_to_equity, tax_rate):
    """Hamada: Bu = BL / (1 + (1-t) D/E)."""
    return levered_beta / (1 + (1 - tax_rate) * debt_to_equity)


def relever_beta(unlevered_beta, debt_to_equity, tax_rate):
    return unlevered_beta * (1 + (1 - tax_rate) * debt_to_equity)


def wacc(equity_value, debt_value, cost_of_equity, pre_tax_cost_of_debt, tax_rate):
    """WACC on market-value weights."""
    v = equity_value + debt_value
    return equity_value / v * cost_of_equity + debt_value / v * pre_tax_cost_of_debt * (1 - tax_rate)


def roic_eva(nopat, invested_capital, wacc_rate):
    """ROIC = NOPAT / invested capital; EVA = (ROIC - WACC) * invested capital."""
    r = nopat / invested_capital
    return {"roic": r, "spread": r - wacc_rate, "eva": (r - wacc_rate) * invested_capital}


def value_driver(nopat_next, growth, roic, wacc_rate):
    """McKinsey value-driver formula: V = NOPAT(1-g/ROIC)/(WACC-g). Shows growth only creates value if ROIC > WACC."""
    if growth >= wacc_rate:
        raise ValueError("growth must be < WACC")
    return nopat_next * (1 - growth / roic) / (wacc_rate - growth)


# ======================================================================
# 3. DCF valuation
# ======================================================================


def dcf(fcff, wacc_rate, terminal_growth=None, exit_multiple=None, terminal_metric=None,
        mid_year=False, net_debt=0.0, shares=None, long_run_growth_cap=0.04):
    """Enterprise DCF on explicit FCFF for years 1..N.

    Terminal value: Gordon growth (terminal_growth) and/or exit multiple (exit_multiple x terminal_metric,
    e.g. year-N EBITDA). If both are given, both are computed and cross-checked (implied multiple / implied g).
    mid_year discounts flows at t-0.5 (TV stays at N). Returns EV, equity, per-share, TV share and warnings.
    """
    f = [_f(x) for x in fcff]
    n = len(f)
    shift = 0.5 if mid_year else 0.0
    dfs = [(1 + wacc_rate) ** -(t + 1 - shift) for t in range(n)]
    pv_fcff = sum(a * b for a, b in zip(f, dfs))
    df_n = (1 + wacc_rate) ** -n
    out = {"pv_explicit": pv_fcff, "discount_factors": dfs, "warnings": []}
    methods = {}
    if terminal_growth is not None:
        if terminal_growth >= wacc_rate:
            raise ValueError("terminal_growth must be below WACC")
        tv = f[-1] * (1 + terminal_growth) / (wacc_rate - terminal_growth)
        methods["gordon"] = tv
        if terminal_growth > long_run_growth_cap:
            out["warnings"].append("Terminal growth %.2f%% exceeds long-run cap %.2f%% (nominal GDP-type ceiling)." % (terminal_growth * 100, long_run_growth_cap * 100))
        if terminal_metric:
            out["gordon_implied_exit_multiple"] = tv / terminal_metric
    if exit_multiple is not None:
        if not terminal_metric:
            raise ValueError("exit_multiple needs terminal_metric (e.g. year-N EBITDA)")
        tv = exit_multiple * terminal_metric
        methods["exit_multiple"] = tv
        out["exit_implied_growth"] = (tv * wacc_rate - f[-1]) / (tv + f[-1])
    if not methods:
        raise ValueError("give terminal_growth and/or exit_multiple")
    out["methods"] = {}
    for k, tv in methods.items():
        ev = pv_fcff + tv * df_n
        eq = ev - net_debt
        m = {"terminal_value": tv, "pv_terminal": tv * df_n, "enterprise_value": ev,
             "tv_share_of_ev": tv * df_n / ev if ev else None, "equity_value": eq}
        if shares:
            m["per_share"] = eq / shares
        if m["tv_share_of_ev"] and m["tv_share_of_ev"] > 0.75:
            out["warnings"].append("%s: terminal value is %.0f%% of EV - valuation rests on the terminal assumption." % (k, m["tv_share_of_ev"] * 100))
        out["methods"][k] = m
    if len(methods) == 2:
        a, b = (out["methods"][k]["enterprise_value"] for k in ("gordon", "exit_multiple"))
        gap = abs(a - b) / ((a + b) / 2)
        out["method_gap"] = gap
        if gap > 0.20:
            out["warnings"].append("Gordon and exit-multiple EVs differ by %.0f%%: reconcile growth vs multiple assumptions." % (gap * 100))
    return out


def dcf_grid(fcff, waccs, growths, net_debt=0.0, shares=None, mid_year=False):
    """Equity value (or per share) sensitivity: rows = WACC, cols = terminal growth (Gordon)."""
    grid = []
    for w in waccs:
        row = []
        for g in growths:
            if g >= w:
                row.append(None); continue
            m = dcf(fcff, w, terminal_growth=g, net_debt=net_debt, shares=shares, mid_year=mid_year, long_run_growth_cap=1)["methods"]["gordon"]
            row.append(m["per_share"] if shares else m["equity_value"])
        grid.append(row)
    return {"rows_wacc": waccs, "cols_growth": growths, "values": grid}


def fcff_from(ebit, tax_rate, da, capex, delta_nwc):
    """FCFF = EBIT(1-t) + D&A - capex - increase in NWC."""
    return ebit * (1 - tax_rate) + da - capex - delta_nwc


def multiples_valuation(metric_value, peer_multiples, net_debt=0.0):
    """Comparable-multiples valuation: EV range from peer multiples (min/25th/median/75th/max)."""
    m = sorted(_f(x) for x in peer_multiples)

    def q(p):
        k = (len(m) - 1) * p
        lo, hi = math.floor(k), math.ceil(k)
        return m[lo] + (m[hi] - m[lo]) * (k - lo)
    stats = {"min": m[0], "p25": q(.25), "median": q(.5), "p75": q(.75), "max": m[-1]}
    return {"multiples": stats, "ev": {k: v * metric_value for k, v in stats.items()},
            "equity": {k: v * metric_value - net_debt for k, v in stats.items()}}


# ======================================================================
# 4. Financial statement analysis
# ======================================================================


def ratios(revenue, cogs, ebit, net_income, interest, da, current_assets, current_liabilities,
           cash, inventory, receivables, payables, total_assets, total_debt, equity,
           cfo=None, capex=None, days=365):
    """Liquidity, efficiency (CCC), leverage, coverage, profitability and DuPont."""
    ebitda = ebit + da
    r = {
        "current_ratio": current_assets / current_liabilities,
        "quick_ratio": (current_assets - inventory) / current_liabilities,
        "cash_ratio": cash / current_liabilities,
        "dso": receivables / revenue * days, "dio": inventory / cogs * days, "dpo": payables / cogs * days,
        "gross_margin": (revenue - cogs) / revenue, "ebit_margin": ebit / revenue,
        "ebitda_margin": ebitda / revenue, "net_margin": net_income / revenue,
        "debt_to_equity": total_debt / equity, "net_debt_to_ebitda": (total_debt - cash) / ebitda,
        "interest_coverage": ebit / interest if interest else None,
        "roa": net_income / total_assets, "roe": net_income / equity,
        "asset_turnover": revenue / total_assets, "equity_multiplier": total_assets / equity,
    }
    r["ccc"] = r["dso"] + r["dio"] - r["dpo"]
    r["dupont_roe"] = r["net_margin"] * r["asset_turnover"] * r["equity_multiplier"]
    if cfo is not None:
        r["cash_conversion"] = cfo / net_income if net_income else None
        r["accruals_ratio"] = (net_income - cfo) / total_assets
        if capex is not None:
            r["fcf"] = cfo - capex
    return r


def altman_z(working_capital, retained_earnings, ebit, book_equity, total_liabilities, total_assets,
             sales=None, variant="private_nonmanufacturing"):
    """Altman Z'' (private / non-manufacturing, 4-factor) or Z' (private manufacturing, 5-factor)."""
    x1, x2, x3 = working_capital / total_assets, retained_earnings / total_assets, ebit / total_assets
    x4 = book_equity / total_liabilities
    if variant == "private_manufacturing":
        z = 0.717 * x1 + 0.847 * x2 + 3.107 * x3 + 0.420 * x4 + 0.998 * (sales / total_assets)
        zone = "safe" if z > 2.9 else "grey" if z > 1.23 else "distress"
    else:
        z = 6.56 * x1 + 3.26 * x2 + 6.72 * x3 + 1.05 * x4
        zone = "safe" if z > 2.6 else "grey" if z > 1.1 else "distress"
    return {"z": z, "zone": zone, "variant": variant}


# ======================================================================
# 5. Three-statement model (no circularity: interest on opening balances)
# ======================================================================

TS_DEFAULTS = dict(years=5, growth=0.05, gross_margin=0.4, opex_pct=0.2, da_pct_rev=0.03,
                   capex_pct_rev=0.04, dso=45, dio=60, dpo=45, days=365, tax_rate=0.2,
                   interest_rate=0.07, revolver_rate=0.09, cash_interest_rate=0.0, min_cash=0.0,
                   debt_repayment=0.0, new_debt=0.0, payout_ratio=0.0)


def three_statement(revenue0, opening, **kw):
    """Integrated IS/BS/CF forecast.

    opening = {cash, ar, inventory, ppe, ap, debt, equity[, revolver, other_assets, other_liabilities]}
    (must balance). Drivers (scalar or per-year list): growth, gross_margin, opex_pct, da_pct_rev,
    capex_pct_rev, dso, dio (on COGS), dpo (on COGS), tax_rate, interest_rate (on opening debt),
    revolver_rate, cash_interest_rate (on opening cash), min_cash, debt_repayment, new_debt, payout_ratio.
    Tax is max(0, EBT) x rate with loss carry-forward. A revolver funds any shortfall below min_cash
    and is repaid from excess cash. Returns per-year statements plus integrity checks.
    """
    p = dict(TS_DEFAULTS); p.update(kw)
    n = int(p["years"])
    S = {k: _series(p[k], n) for k in ("growth", "gross_margin", "opex_pct", "da_pct_rev", "capex_pct_rev", "dso", "dio", "dpo",
                                     "tax_rate", "interest_rate", "revolver_rate", "cash_interest_rate", "min_cash",
                                     "debt_repayment", "new_debt", "payout_ratio")}
    o = {k: _f(opening.get(k, 0.0)) for k in ("cash", "ar", "inventory", "ppe", "other_assets", "ap", "other_liabilities", "debt", "revolver", "equity")}
    a0 = o["cash"] + o["ar"] + o["inventory"] + o["ppe"] + o["other_assets"]
    l0 = o["ap"] + o["other_liabilities"] + o["debt"] + o["revolver"] + o["equity"]
    if abs(a0 - l0) > 1e-6 * max(1, abs(a0)):
        raise ValueError("Opening balance sheet does not balance: assets %.2f vs L+E %.2f" % (a0, l0))
    days = p["days"]
    prev = dict(o); rev_prev = _f(revenue0); nol = 0.0
    years, checks = [], []
    for t in range(n):
        rev = rev_prev * (1 + S["growth"][t])
        cogs = rev * (1 - S["gross_margin"][t]); gp = rev - cogs
        opex = rev * S["opex_pct"][t]; ebitda = gp - opex
        da = rev * S["da_pct_rev"][t]; ebit = ebitda - da
        int_exp = prev["debt"] * S["interest_rate"][t] + prev["revolver"] * S["revolver_rate"][t]
        int_inc = prev["cash"] * S["cash_interest_rate"][t]
        ebt = ebit - int_exp + int_inc
        taxable = ebt - nol if ebt > 0 else 0.0
        if ebt > 0:
            used = min(nol, ebt); nol -= used
        else:
            nol += -ebt
        tax = max(0.0, taxable) * S["tax_rate"][t]
        ni = ebt - tax
        ar = rev * S["dso"][t] / days; inv = cogs * S["dio"][t] / days; ap = cogs * S["dpo"][t] / days
        capex = rev * S["capex_pct_rev"][t]
        ppe = prev["ppe"] + capex - da
        cfo = ni + da - (ar - prev["ar"]) - (inv - prev["inventory"]) + (ap - prev["ap"])
        cfi = -capex
        repay = min(S["debt_repayment"][t], prev["debt"] + S["new_debt"][t])
        debt = prev["debt"] + S["new_debt"][t] - repay
        div = max(0.0, ni) * S["payout_ratio"][t]
        pre_cash = prev["cash"] + cfo + cfi + S["new_debt"][t] - repay - div
        rev_draw = max(0.0, S["min_cash"][t] - pre_cash) if pre_cash < S["min_cash"][t] else -min(prev["revolver"], pre_cash - S["min_cash"][t])
        revolver = prev["revolver"] + rev_draw
        cff = S["new_debt"][t] - repay - div + rev_draw
        cash = prev["cash"] + cfo + cfi + cff
        equity = prev["equity"] + ni - div
        assets = cash + ar + inv + ppe + prev["other_assets"]
        le = ap + prev["other_liabilities"] + debt + revolver + equity
        y = {"year": t + 1, "revenue": rev, "cogs": cogs, "gross_profit": gp, "opex": opex, "ebitda": ebitda,
             "da": da, "ebit": ebit, "interest_expense": int_exp, "interest_income": int_inc, "ebt": ebt,
             "tax": tax, "net_income": ni,
             "cash": cash, "ar": ar, "inventory": inv, "ppe": ppe, "other_assets": prev["other_assets"],
             "total_assets": assets, "ap": ap, "other_liabilities": prev["other_liabilities"], "debt": debt,
             "revolver": revolver, "equity": equity, "total_liabilities_equity": le,
             "cfo": cfo, "capex": capex, "cfi": cfi, "debt_issued": S["new_debt"][t], "debt_repaid": repay,
             "revolver_change": rev_draw, "dividends": div, "cff": cff, "net_change_cash": cfo + cfi + cff,
             "nwc_change": (ar - prev["ar"]) + (inv - prev["inventory"]) - (ap - prev["ap"]),
             "fcff": ebit * (1 - S["tax_rate"][t]) + da - capex - ((ar - prev["ar"]) + (inv - prev["inventory"]) - (ap - prev["ap"])),
             "nol_carryforward": nol}
        checks.append({"year": t + 1, "balance_diff": assets - le,
                       "cash_tieout_diff": (prev["cash"] + y["net_change_cash"]) - cash,
                       "re_rollforward_diff": (prev["equity"] + ni - div) - equity})
        years.append(y)
        prev = {"cash": cash, "ar": ar, "inventory": inv, "ppe": ppe, "other_assets": prev["other_assets"], "ap": ap,
                "other_liabilities": prev["other_liabilities"], "debt": debt, "revolver": revolver, "equity": equity}
        rev_prev = rev
    ok = all(abs(c["balance_diff"]) < 1e-6 * max(1, abs(years[i]["total_assets"])) for i, c in enumerate(checks))
    warnings = []
    for y in years:
        if y["ppe"] < 0:
            warnings.append("Year %d: negative PP&E - D&A exceeds asset base; check da_pct_rev/capex." % y["year"])
        if y["revolver"] > 0:
            warnings.append("Year %d: revolver drawn %.0f - funding gap." % (y["year"], y["revolver"]))
    g = S["growth"]
    if max(g) > 0.30:
        warnings.append("Growth above 30%/yr assumed - requires strong evidence (capacity, demand, funding).")
    return {"years": years, "checks": checks, "balanced": ok, "warnings": warnings, "inputs": {"revenue0": revenue0, "opening": opening, **p}}


def three_statement_xlsx(path, revenue0, opening, **kw):
    """Write the same three-statement model to Excel with LIVE formulas (Inputs + Model sheets).
    The Python result is returned too, so the workbook can be recalculated and compared (recalc_compare)."""
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill
    from openpyxl.utils import get_column_letter as L
    res = three_statement(revenue0, opening, **kw)
    p = res["inputs"]; n = int(p["years"])
    wb = Workbook(); wi = wb.active; wi.title = "Inputs"
    blue = Font(color="0000FF"); bold = Font(bold=True)
    wi["A1"] = "Three-statement model inputs (blue = input)"; wi["A1"].font = bold
    wi["A3"] = "Revenue (year 0)"; wi["B3"] = _f(revenue0); wi["B3"].font = blue
    wi["A4"] = "Days in year"; wi["B4"] = p["days"]; wi["B4"].font = blue
    okeys = ["cash", "ar", "inventory", "ppe", "other_assets", "ap", "other_liabilities", "debt", "revolver", "equity"]
    wi["A6"] = "Opening balance sheet"; wi["A6"].font = bold
    orow = {}
    for i, k in enumerate(okeys):
        r = 7 + i; wi.cell(r, 1, k); c = wi.cell(r, 2, _f(opening.get(k, 0))); c.font = blue; orow[k] = r
    dkeys = ["growth", "gross_margin", "opex_pct", "da_pct_rev", "capex_pct_rev", "dso", "dio", "dpo", "tax_rate",
             "interest_rate", "revolver_rate", "cash_interest_rate", "min_cash", "debt_repayment", "new_debt", "payout_ratio"]
    wi["A19"] = "Drivers by year"; wi["A19"].font = bold
    for t in range(n):
        wi.cell(19, 3 + t, "Y%d" % (t + 1)).font = bold
    drow = {}
    for i, k in enumerate(dkeys):
        r = 20 + i; wi.cell(r, 1, k); drow[k] = r
        for t, v in enumerate(_series(p[k], n)):
            c = wi.cell(r, 3 + t, v); c.font = blue
    wm = wb.create_sheet("Model")
    lines = ["revenue", "cogs", "gross_profit", "opex", "ebitda", "da", "ebit", "interest_expense", "interest_income", "ebt",
             "nol_open", "nol_used", "nol_close", "tax", "net_income", "",
             "ar", "inventory", "ap", "capex", "ppe", "", "cfo", "cfi", "debt_repaid", "debt", "dividends", "pre_cash",
             "revolver_change", "revolver", "cff", "net_change_cash", "cash", "equity", "", "total_assets",
             "total_liabilities_equity", "balance_check"]
    R = {k: 3 + i for i, k in enumerate(lines) if k}
    wm["A1"] = "Integrated model (formulas)"; wm["A1"].font = bold
    wm.cell(2, 2, "Y0").font = bold
    for k, r in R.items():
        wm.cell(r, 1, k)
    # year-0 column (B) from opening balances
    for k in ("ar", "inventory", "ap", "ppe", "debt", "revolver", "cash", "equity"):
        wm.cell(R[k], 2, "=Inputs!B%d" % orow[k])
    wm.cell(R["revenue"], 2, "=Inputs!B3"); wm.cell(R["nol_close"], 2, 0)
    I = lambda k, col: "Inputs!%s%d" % (col, drow[k])
    for t in range(n):
        c = L(3 + t); pcol = L(2 + t); ic = L(3 + t)
        wm.cell(2, 3 + t, "Y%d" % (t + 1)).font = bold
        f = lambda k: "%s%d" % (c, R[k]); pf = lambda k: "%s%d" % (pcol, R[k])
        F = {
            "revenue": "=%s*(1+%s)" % (pf("revenue"), I("growth", ic)),
            "cogs": "=%s*(1-%s)" % (f("revenue"), I("gross_margin", ic)),
            "gross_profit": "=%s-%s" % (f("revenue"), f("cogs")),
            "opex": "=%s*%s" % (f("revenue"), I("opex_pct", ic)),
            "ebitda": "=%s-%s" % (f("gross_profit"), f("opex")),
            "da": "=%s*%s" % (f("revenue"), I("da_pct_rev", ic)),
            "ebit": "=%s-%s" % (f("ebitda"), f("da")),
            "interest_expense": "=%s*%s+%s*%s" % (pf("debt"), I("interest_rate", ic), pf("revolver"), I("revolver_rate", ic)),
            "interest_income": "=%s*%s" % (pf("cash"), I("cash_interest_rate", ic)),
            "ebt": "=%s-%s+%s" % (f("ebit"), f("interest_expense"), f("interest_income")),
            "nol_open": "=%s" % pf("nol_close"),
            "nol_used": "=IF(%s>0,MIN(%s,%s),0)" % (f("ebt"), f("nol_open"), f("ebt")),
            "nol_close": "=IF(%s>0,%s-%s,%s-%s)" % (f("ebt"), f("nol_open"), f("nol_used"), f("nol_open"), f("ebt")),
            "tax": "=MAX(0,%s-%s)*%s" % (f("ebt"), f("nol_used"), I("tax_rate", ic)),
            "net_income": "=%s-%s" % (f("ebt"), f("tax")),
            "ar": "=%s*%s/Inputs!$B$4" % (f("revenue"), I("dso", ic)),
            "inventory": "=%s*%s/Inputs!$B$4" % (f("cogs"), I("dio", ic)),
            "ap": "=%s*%s/Inputs!$B$4" % (f("cogs"), I("dpo", ic)),
            "capex": "=%s*%s" % (f("revenue"), I("capex_pct_rev", ic)),
            "ppe": "=%s+%s-%s" % (pf("ppe"), f("capex"), f("da")),
            "cfo": "=%s+%s-(%s-%s)-(%s-%s)+(%s-%s)" % (f("net_income"), f("da"), f("ar"), pf("ar"), f("inventory"), pf("inventory"), f("ap"), pf("ap")),
            "cfi": "=-%s" % f("capex"),
            "debt_repaid": "=MIN(%s,%s+%s)" % (I("debt_repayment", ic), pf("debt"), I("new_debt", ic)),
            "debt": "=%s+%s-%s" % (pf("debt"), I("new_debt", ic), f("debt_repaid")),
            "dividends": "=MAX(0,%s)*%s" % (f("net_income"), I("payout_ratio", ic)),
            "pre_cash": "=%s+%s+%s+%s-%s-%s" % (pf("cash"), f("cfo"), f("cfi"), I("new_debt", ic), f("debt_repaid"), f("dividends")),
            "revolver_change": "=IF(%s<%s,%s-%s,-MIN(%s,%s-%s))" % (f("pre_cash"), I("min_cash", ic), I("min_cash", ic), f("pre_cash"), pf("revolver"), f("pre_cash"), I("min_cash", ic)),
            "revolver": "=%s+%s" % (pf("revolver"), f("revolver_change")),
            "cff": "=%s-%s-%s+%s" % (I("new_debt", ic), f("debt_repaid"), f("dividends"), f("revolver_change")),
            "net_change_cash": "=%s+%s+%s" % (f("cfo"), f("cfi"), f("cff")),
            "cash": "=%s+%s" % (pf("cash"), f("net_change_cash")),
            "equity": "=%s+%s-%s" % (pf("equity"), f("net_income"), f("dividends")),
            "total_assets": "=%s+%s+%s+%s+Inputs!$B$%d" % (f("cash"), f("ar"), f("inventory"), f("ppe"), orow["other_assets"]),
            "total_liabilities_equity": "=%s+Inputs!$B$%d+%s+%s+%s" % (f("ap"), orow["other_liabilities"], f("debt"), f("revolver"), f("equity")),
            "balance_check": "=ROUND(%s-%s,6)" % (f("total_assets"), f("total_liabilities_equity")),
        }
        for k, formula in F.items():
            wm.cell(R[k], 3 + t, formula).number_format = "#,##0.00"
    wm.column_dimensions["A"].width = 26
    wb.save(path)
    return {"path": path, "rows": R, "python_result": res}


def recalc_compare(xlsx_path, expected, sheet="Model", tol=1e-6):
    """Recalculate an .xlsx with LibreOffice (headless) and compare cells to expected values.
    expected = {"C5": 123.4, ...}. Returns max abs/rel error. Needs `soffice` on PATH."""
    import os
    import shutil
    import subprocess
    import tempfile
    from openpyxl import load_workbook
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice:
        return {"available": False, "reason": "LibreOffice not installed"}
    tmp = tempfile.mkdtemp()
    subprocess.run([soffice, "--headless", "--convert-to", "xlsx", "--outdir", tmp, xlsx_path], check=True,
                   capture_output=True, timeout=180)
    wb = load_workbook(os.path.join(tmp, os.path.basename(xlsx_path)), data_only=True)
    ws = wb[sheet]
    worst, bad = 0.0, []
    for ref, exp in expected.items():
        got = ws[ref].value
        if got is None:
            bad.append((ref, exp, None)); continue
        err = abs(got - exp) / max(1.0, abs(exp))
        worst = max(worst, err)
        if err > tol:
            bad.append((ref, exp, got))
    shutil.rmtree(tmp, ignore_errors=True)
    return {"available": True, "cells_checked": len(expected), "max_rel_error": worst, "mismatches": bad[:20]}


# ======================================================================
# 6. Project feasibility model + risk analytics (sensitivity, MC, stress)
# ======================================================================

PROJECT_DEFAULTS = dict(life=5, units=1000, unit_growth=0.0, price=100.0, price_growth=0.0, var_cost_pct=0.6,
                        fixed_cost=10000.0, fixed_cost_growth=0.0, capex=50000.0, salvage=0.0, nwc_pct=0.1,
                        tax_rate=0.2, discount_rate=0.12, depreciation_years=None, ramp=None)


def project(**kw):
    """Investment feasibility model (annual). Returns yearly P&L-to-FCF, NPV, IRR, MIRR, payback, and
    the accounting-profit vs cash-flow comparison.
    Drivers: life, units, unit_growth, price, price_growth, var_cost_pct, fixed_cost, fixed_cost_growth,
    capex (t=0), salvage (pre-tax, end of life), nwc_pct (of revenue, recovered at end), tax_rate,
    discount_rate, depreciation_years (straight-line, default=life), ramp (list of utilisation factors).
    Losses create a tax shield (assumes other taxable profits); set tax_rate=0 if not.
    """
    p = dict(PROJECT_DEFAULTS); p.update(kw)
    n = int(p["life"]); dep_years = int(p["depreciation_years"] or n)
    dep = p["capex"] / dep_years
    ramp = _series(p["ramp"], n) if p["ramp"] is not None else [1.0] * n
    rows, cfs = [], [-p["capex"]]
    nwc_prev = 0.0
    for t in range(1, n + 1):
        units = p["units"] * (1 + p["unit_growth"]) ** (t - 1) * ramp[t - 1]
        price = p["price"] * (1 + p["price_growth"]) ** (t - 1)
        rev = units * price
        var = rev * p["var_cost_pct"]
        fixed = p["fixed_cost"] * (1 + p["fixed_cost_growth"]) ** (t - 1)
        d = dep if t <= dep_years else 0.0
        ebit = rev - var - fixed - d
        tax = ebit * p["tax_rate"]
        nopat = ebit - tax
        nwc = rev * p["nwc_pct"]
        dnwc = nwc - nwc_prev; nwc_prev = nwc
        fcf = nopat + d - dnwc
        if t == n:
            book = p["capex"] - d * min(n, dep_years)
            fcf += p["salvage"] - (p["salvage"] - book) * p["tax_rate"] + nwc  # after-tax salvage + NWC recovery
        rows.append({"year": t, "units": units, "price": price, "revenue": rev, "variable_cost": var, "fixed_cost": fixed,
                     "depreciation": d, "ebit": ebit, "tax": tax, "net_operating_profit": nopat, "delta_nwc": dnwc, "fcf": fcf})
        cfs.append(fcf)
    r = p["discount_rate"]
    i = irr(cfs)
    cm = 1 - p["var_cost_pct"]
    be_units = (p["fixed_cost"] + dep) / (p["price"] * cm) if cm > 0 else None
    return {"cashflows": cfs, "npv": npv(r, cfs), "irr": i["irr"], "irr_warning": i["warning"],
            "mirr": mirr(cfs, r, r), "payback": payback(cfs), "discounted_payback": payback(cfs, r),
            "profitability_index": profitability_index(r, cfs),
            "accounting_profit_total": sum(x["net_operating_profit"] for x in rows),
            "cash_flow_total": sum(cfs), "years": rows,
            "accounting_breakeven_units_y1": be_units}


_MODELS = {"project": project}


def _run(model, inputs, metric):
    out = _MODELS[model](**inputs)
    return out[metric]


def tornado(base, ranges, model="project", metric="npv"):
    """One-at-a-time sensitivity. ranges = {input: [low, high]}. Sorted by swing (largest first)."""
    b = _run(model, base, metric)
    rows = []
    for k, (lo, hi) in ranges.items():
        vlo = _run(model, {**base, k: lo}, metric); vhi = _run(model, {**base, k: hi}, metric)
        rows.append({"input": k, "low": lo, "high": hi, "metric_at_low": vlo, "metric_at_high": vhi, "swing": abs(vhi - vlo)})
    rows.sort(key=lambda r: -r["swing"])
    return {"base": b, "metric": metric, "rows": rows}


def grid(base, x, xs, y, ys, model="project", metric="npv"):
    """Two-way sensitivity table: rows = y values, cols = x values."""
    return {"x": x, "xs": xs, "y": y, "ys": ys,
            "values": [[_run(model, {**base, x: xv, y: yv}, metric) for xv in xs] for yv in ys]}


def scenarios(base, cases, model="project", metric="npv", probabilities=None):
    """Named scenarios {name: {overrides}}; optional probabilities -> expected value."""
    res = {name: _run(model, {**base, **ov}, metric) for name, ov in cases.items()}
    out = {"metric": metric, "results": res}
    if probabilities:
        if abs(sum(probabilities.values()) - 1) > 1e-9:
            raise ValueError("probabilities must sum to 1")
        out["expected"] = sum(res[k] * probabilities[k] for k in res)
    return out


def _draw(rng, spec):
    kind = spec[0]
    if kind == "normal":
        return rng.gauss(spec[1], spec[2])
    if kind == "triangular":   # (low, mode, high)
        return rng.triangular(spec[1], spec[3], spec[2])
    if kind == "uniform":
        return rng.uniform(spec[1], spec[2])
    if kind == "lognormal":    # (mean, sd) of the variable itself
        m, s = spec[1], spec[2]
        sig2 = math.log(1 + (s / m) ** 2)
        return rng.lognormvariate(math.log(m) - sig2 / 2, math.sqrt(sig2))
    if kind == "pert":         # (low, mode, high)
        a, mo, b = spec[1], spec[2], spec[3]
        alpha = 1 + 4 * (mo - a) / (b - a); beta = 1 + 4 * (b - mo) / (b - a)
        return a + rng.betavariate(alpha, beta) * (b - a)
    if kind == "discrete":     # (values, probabilities)
        return rng.choices(spec[1], weights=spec[2])[0]
    raise ValueError("unknown distribution %s" % kind)


def montecarlo(base, dists, n=10000, seed=42, model="project", metric="npv", threshold=0.0, correlations=None):
    """Monte Carlo over the model. dists = {input: ["triangular", low, mode, high] | ["normal", mu, sd] |
    ["uniform", lo, hi] | ["lognormal", mean, sd] | ["pert", lo, mode, hi] | ["discrete", values, probs]}.
    correlations = {"a|b": rho} for normal inputs only (Gaussian copula on pairs, applied via shared shocks).
    Returns mean, sd, percentiles, P(metric < threshold), expected shortfall (5%) and seed."""
    rng = random.Random(seed)
    vals = []
    corr = correlations or {}
    for _ in range(int(n)):
        draw = {}
        z_common = {}
        for k, spec in dists.items():
            draw[k] = _draw(rng, spec)
        for pair, rho in corr.items():
            a, b = pair.split("|")
            if dists[a][0] == "normal" and dists[b][0] == "normal":
                za = (draw[a] - dists[a][1]) / dists[a][2]
                zb_ind = rng.gauss(0, 1)
                zb = rho * za + math.sqrt(1 - rho ** 2) * zb_ind
                draw[b] = dists[b][1] + zb * dists[b][2]
        vals.append(_run(model, {**base, **draw}, metric))
    vals.sort()
    m = sum(vals) / len(vals)
    sd = math.sqrt(sum((v - m) ** 2 for v in vals) / (len(vals) - 1))
    pct = lambda q: vals[min(len(vals) - 1, max(0, int(round(q * (len(vals) - 1)))))]
    k5 = max(1, int(0.05 * len(vals)))
    return {"n": len(vals), "seed": seed, "metric": metric, "mean": m, "sd": sd,
            "p5": pct(.05), "p10": pct(.10), "p50": pct(.5), "p90": pct(.90), "p95": pct(.95),
            "prob_below_threshold": sum(1 for v in vals if v < threshold) / len(vals),
            "expected_shortfall_5pct": sum(vals[:k5]) / k5, "threshold": threshold,
            "mc_standard_error_of_mean": sd / math.sqrt(len(vals))}


def breakeven_input(base, input_name, lo, hi, model="project", metric="npv", target=0.0):
    """Reverse stress test: value of one input at which metric == target (bisection within [lo, hi])."""
    f = lambda v: _run(model, {**base, input_name: v}, metric) - target
    root = _bisect(f, lo, hi, tol=1e-9)
    b = base.get(input_name, PROJECT_DEFAULTS.get(input_name))
    return {"input": input_name, "breakeven_value": root, "base_value": b,
            "headroom_pct": (root - b) / b if (root is not None and b) else None,
            "note": None if root is not None else "No break-even inside [lo, hi]"}


def stress(base, shocks, model="project", metric="npv"):
    """Combined stress scenarios: {name: {input: new_value}} applied together; reports metric and change."""
    b = _run(model, base, metric)
    return {"base": b, "results": {k: {"value": _run(model, {**base, **v}, metric), "change": _run(model, {**base, **v}, metric) - b} for k, v in shocks.items()}}


# ======================================================================
# 7. Unit economics, pricing, FP&A
# ======================================================================


def breakeven(fixed_costs, price, variable_cost, target_profit=0.0, actual_units=None):
    """Break-even units/revenue, contribution margin, margin of safety, degree of operating leverage."""
    cm = price - variable_cost
    if cm <= 0:
        return {"contribution_margin": cm, "error": "price <= variable cost: no break-even"}
    u = (fixed_costs + target_profit) / cm
    out = {"contribution_margin": cm, "cm_ratio": cm / price, "breakeven_units": u, "breakeven_revenue": u * price}
    if actual_units:
        profit = actual_units * cm - fixed_costs
        out.update({"margin_of_safety": (actual_units - u) / actual_units, "profit": profit,
                    "operating_leverage": actual_units * cm / profit if profit else None})
    return out


def ltv(arpu_month, gross_margin, monthly_churn, monthly_discount_rate=0.0, cac=None, max_months=None):
    """Customer LTV (gross-margin basis). Geometric survival; optional discounting and horizon cap.
    Also LTV:CAC and CAC payback months when cac is given."""
    m = arpu_month * gross_margin
    if max_months:
        v = sum(m * (1 - monthly_churn) ** (t - 1) / (1 + monthly_discount_rate) ** t for t in range(1, int(max_months) + 1))
    else:
        v = m * (1 + monthly_discount_rate) / (monthly_discount_rate + monthly_churn) / (1 + monthly_discount_rate)
    out = {"monthly_margin": m, "ltv": v, "expected_lifetime_months": 1 / monthly_churn if monthly_churn else None}
    if cac:
        out["ltv_to_cac"] = v / cac
        out["cac_payback_months"] = cac / m if m else None
    return out


def cohort_ltv(retention_curve, arpu_month, gross_margin, monthly_discount_rate=0.0):
    """LTV from an observed retention curve (fraction active in month 1..n)."""
    return sum(r * arpu_month * gross_margin / (1 + monthly_discount_rate) ** (t + 1) for t, r in enumerate(retention_curve))


def price_change_breakeven(price, variable_cost, price_change_pct):
    """Volume change needed to keep total contribution constant after a price change (classic pricing rule)."""
    cm = price - variable_cost
    new_cm = price * (1 + price_change_pct) - variable_cost
    return {"required_volume_change": cm / new_cm - 1, "cm_old": cm, "cm_new": new_cm}


def subscription_price_change(subs, price_old, price_new, churn_old, churn_new, months=12, new_subs_per_month=0.0,
                              gross_margin=1.0, immediate_loss_pct=0.0):
    """Subscription repricing: simulate MRR/gross margin over `months` and steady state for old vs new price."""
    def sim(price, churn, s0):
        s, tot = s0, 0.0
        for _ in range(months):
            tot += s * price * gross_margin
            s = s * (1 - churn) + new_subs_per_month
        steady = new_subs_per_month / churn * price * gross_margin if churn else None
        return tot, steady
    a, sa = sim(price_old, churn_old, subs)
    b, sb = sim(price_new, churn_new, subs * (1 - immediate_loss_pct))
    mrr_old, mrr_new = subs * price_old, subs * (1 - immediate_loss_pct) * price_new
    be_loss = 1 - price_old / price_new
    return {"mrr_old": mrr_old, "mrr_new_month1": mrr_new, "breakeven_immediate_loss_pct": be_loss,
            "breakeven_immediate_loss_subs": be_loss * subs,
            "cumulative_gm_old": a, "cumulative_gm_new": b, "steady_state_gm_old": sa, "steady_state_gm_new": sb,
            "breakeven_churn_for_steady_state": churn_old * price_new / price_old}


def variance_analysis(budget_price, budget_volume, actual_price, actual_volume, budget_unit_cost=None, actual_unit_cost=None):
    """Revenue variance split into price and volume effects (and cost variance if unit costs given)."""
    bud = budget_price * budget_volume; act = actual_price * actual_volume
    out = {"budget_revenue": bud, "actual_revenue": act, "total_variance": act - bud,
           "price_variance": (actual_price - budget_price) * actual_volume,
           "volume_variance": (actual_volume - budget_volume) * budget_price}
    if budget_unit_cost is not None and actual_unit_cost is not None:
        out["cost_rate_variance"] = -(actual_unit_cost - budget_unit_cost) * actual_volume
        out["cost_volume_variance"] = -(actual_volume - budget_volume) * budget_unit_cost
    return out


def cagr(start, end, years):
    return (end / start) ** (1.0 / years) - 1


# ======================================================================
# 8. LBO and M&A
# ======================================================================


def lbo(entry_ebitda, entry_multiple, debt_multiple, years=5, ebitda_growth=0.05, exit_multiple=None,
        interest_rate=0.08, tax_rate=0.2, capex_pct_ebitda=0.2, nwc_pct_ebitda=0.0, da_pct_ebitda=0.15,
        fees_pct=0.02, cash_sweep=1.0, mandatory_amort_pct=0.0, min_cash=0.0):
    """Simplified LBO: one debt tranche, interest on opening balance, cash sweep of free cash flow.
    Returns sources & uses, debt schedule, exit equity, IRR and MOIC, plus value-creation bridge."""
    exit_multiple = entry_multiple if exit_multiple is None else exit_multiple
    ev = entry_ebitda * entry_multiple
    debt0 = entry_ebitda * debt_multiple
    fees = ev * fees_pct
    equity0 = ev + fees + min_cash - debt0
    g = _series(ebitda_growth, years)
    debt, ebitda, cash = debt0, entry_ebitda, min_cash
    sched = []
    for t in range(years):
        ebitda = ebitda * (1 + g[t])
        da = ebitda * da_pct_ebitda
        interest = debt * interest_rate
        tax = max(0.0, (ebitda - da - interest) * tax_rate)
        fcf = ebitda - interest - tax - ebitda * capex_pct_ebitda - ebitda * g[t] / (1 + g[t]) * nwc_pct_ebitda
        mand = min(debt, debt0 * mandatory_amort_pct)
        sweep = min(debt - mand, max(0.0, fcf - mand) * cash_sweep)
        repay = mand + sweep
        cash += fcf - repay
        debt -= repay
        sched.append({"year": t + 1, "ebitda": ebitda, "interest": interest, "tax": tax, "fcf": fcf,
                      "repayment": repay, "debt_end": debt, "cash_end": cash, "leverage": debt / ebitda})
    exit_ev = ebitda * exit_multiple
    exit_eq = exit_ev - debt + cash
    cfs = [-equity0] + [0.0] * (years - 1) + [exit_eq]
    bridge = {"ebitda_growth": (ebitda - entry_ebitda) * entry_multiple,
              "multiple_change": (exit_multiple - entry_multiple) * ebitda,
              "net_debt_paydown_and_cash": (debt0 - debt) + (cash - min_cash),
              "fees_leakage": -fees}
    return {"sources_uses": {"enterprise_value": ev, "fees": fees, "min_cash": min_cash, "debt": debt0, "sponsor_equity": equity0},
            "schedule": sched, "exit_ev": exit_ev, "exit_equity": exit_eq, "moic": exit_eq / equity0,
            "irr": irr(cfs)["irr"], "value_creation_bridge": bridge,
            "bridge_check": sum(bridge.values()) - (exit_eq - equity0)}


def accretion_dilution(acq_net_income, acq_shares, target_net_income, price_paid, pct_cash, pct_stock,
                       acq_share_price, cost_of_debt=0.06, interest_on_cash=0.0, tax_rate=0.2,
                       synergies_pre_tax=0.0, pct_cash_from_balance=0.0, new_da_pre_tax=0.0):
    """Pro forma EPS for an acquisition. Stock portion issues new shares at acq_share_price; cash portion
    is funded by balance-sheet cash (lost interest) and new debt (after-tax interest). Includes breakeven synergies."""
    if abs(pct_cash + pct_stock - 1) > 1e-9:
        raise ValueError("pct_cash + pct_stock must be 1")
    eps0 = acq_net_income / acq_shares
    cash = price_paid * pct_cash
    from_bs = cash * pct_cash_from_balance; from_debt = cash - from_bs
    new_shares = price_paid * pct_stock / acq_share_price
    cost = (from_debt * cost_of_debt + from_bs * interest_on_cash + new_da_pre_tax) * (1 - tax_rate)
    ni_pf = acq_net_income + target_net_income - cost + synergies_pre_tax * (1 - tax_rate)
    eps1 = ni_pf / (acq_shares + new_shares)
    need = (eps0 * (acq_shares + new_shares) - (acq_net_income + target_net_income - cost)) / (1 - tax_rate)
    return {"standalone_eps": eps0, "pro_forma_eps": eps1, "accretion_pct": eps1 / eps0 - 1,
            "new_shares": new_shares, "new_debt": from_debt, "after_tax_financing_cost": cost,
            "breakeven_synergies_pre_tax": max(0.0, need)}


# ======================================================================
# 9. Operations (COO)
# ======================================================================


def erlang_c(arrival_rate, service_rate, servers, target_wait=None):
    """M/M/c queue. arrival_rate and service_rate per same time unit (service_rate = per server).
    Returns utilisation, P(wait), mean wait Wq, mean in queue Lq, and service level P(wait <= target_wait)."""
    a = arrival_rate / service_rate
    c = int(servers)
    rho = a / c
    if rho >= 1:
        return {"utilisation": rho, "stable": False, "note": "arrival >= capacity: queue grows without bound"}
    b = 1.0
    for k in range(1, c + 1):           # Erlang B recursion (numerically stable)
        b = a * b / (k + a * b)
    pw = b / (1 - rho * (1 - b))
    wq = pw / (c * service_rate - arrival_rate)
    out = {"offered_load_erlangs": a, "utilisation": rho, "stable": True, "p_wait": pw, "mean_wait": wq,
           "mean_queue_length": arrival_rate * wq, "mean_time_in_system": wq + 1 / service_rate}
    if target_wait is not None:
        out["service_level"] = 1 - pw * math.exp(-(c * service_rate - arrival_rate) * target_wait)
    return out


def staff_for_service_level(arrival_rate, service_rate, target_wait, target_service_level, max_servers=1000):
    """Smallest number of servers meeting P(wait <= target_wait) >= target_service_level."""
    c = max(1, int(math.floor(arrival_rate / service_rate)) + 1)
    while c <= max_servers:
        r = erlang_c(arrival_rate, service_rate, c, target_wait)
        if r.get("stable") and r["service_level"] >= target_service_level:
            return {"servers": c, **r}
        c += 1
    return {"servers": None, "note": "not reached within max_servers"}


def littles_law(wip=None, throughput=None, lead_time=None):
    """L = lambda x W. Give any two; returns the third."""
    if wip is None:
        return {"wip": throughput * lead_time}
    if throughput is None:
        return {"throughput": wip / lead_time}
    return {"lead_time": wip / throughput}


def oee(planned_time, run_time, ideal_cycle_time, total_count, good_count):
    """Overall equipment effectiveness = availability x performance x quality."""
    av = run_time / planned_time
    perf = ideal_cycle_time * total_count / run_time
    q = good_count / total_count
    return {"availability": av, "performance": perf, "quality": q, "oee": av * perf * q}


def eoq(annual_demand, order_cost, holding_cost_per_unit_year):
    """Economic order quantity, orders/year and total relevant cost."""
    q = math.sqrt(2 * annual_demand * order_cost / holding_cost_per_unit_year)
    return {"eoq": q, "orders_per_year": annual_demand / q,
            "total_relevant_cost": annual_demand / q * order_cost + q / 2 * holding_cost_per_unit_year}


def safety_stock(daily_demand_mean, daily_demand_sd, lead_time_days, service_level, lead_time_sd_days=0.0):
    """Safety stock & reorder point with demand and lead-time variability (normal approximation)."""
    z = norm_ppf(service_level)
    sd = math.sqrt(lead_time_days * daily_demand_sd ** 2 + (daily_demand_mean * lead_time_sd_days) ** 2)
    ss = z * sd
    return {"z": z, "safety_stock": ss, "reorder_point": daily_demand_mean * lead_time_days + ss}


def takt_time(available_time, demand):
    return available_time / demand


def learning_curve(first_unit_time, learning_rate, units):
    """Wright's curve: time of unit n = T1 * n^log2(rate); returns unit time and cumulative total."""
    b = math.log(learning_rate, 2)
    return {"unit_time": first_unit_time * units ** b,
            "cumulative_time": sum(first_unit_time * k ** b for k in range(1, int(units) + 1)),
            "exponent": b}


def capacity(demand_units, capacity_units_per_resource, target_utilisation=0.85):
    """Resources needed at a target utilisation, and actual utilisation after rounding up."""
    need = demand_units / (capacity_units_per_resource * target_utilisation)
    n = math.ceil(need - 1e-12)
    return {"resources_needed": n, "exact": need, "utilisation_at_n": demand_units / (n * capacity_units_per_resource)}


def dpmo_sigma(defects, units, opportunities_per_unit, shift=1.5):
    """Six Sigma: DPMO, yield and (short-term) sigma level with the conventional 1.5 sigma shift."""
    dpmo = defects / (units * opportunities_per_unit) * 1e6
    y = 1 - dpmo / 1e6
    return {"dpmo": dpmo, "yield": y, "sigma_level": (norm_ppf(y) + shift) if 0 < y < 1 else None}


def control_limits(values, chart="individuals", sample_sizes=None):
    """SPC limits. individuals: mean +/- 2.66 x average moving range (I-MR chart).
    p: proportion defective per sample (values = defect counts, sample_sizes = n per sample)."""
    if chart == "p":
        pbar = sum(values) / sum(sample_sizes)
        pts = []
        for d, n in zip(values, sample_sizes):
            s = math.sqrt(pbar * (1 - pbar) / n)
            p = d / n
            pts.append({"p": p, "ucl": pbar + 3 * s, "lcl": max(0.0, pbar - 3 * s), "out": p > pbar + 3 * s or p < max(0.0, pbar - 3 * s)})
        return {"center": pbar, "points": pts}
    m = sum(values) / len(values)
    mr = sum(abs(a - b) for a, b in zip(values[1:], values)) / (len(values) - 1)
    ucl, lcl = m + 2.66 * mr, m - 2.66 * mr
    return {"center": m, "ucl": ucl, "lcl": lcl, "out_of_control": [i for i, v in enumerate(values) if v > ucl or v < lcl]}


def fmea(items):
    """FMEA: items = [{failure_mode, severity 1-10, occurrence 1-10, detection 1-10}] -> RPN ranked; flags severity >= 9."""
    rows = [{**i, "rpn": i["severity"] * i["occurrence"] * i["detection"], "safety_critical": i["severity"] >= 9} for i in items]
    return sorted(rows, key=lambda r: (-r["safety_critical"], -r["rpn"]))


# ======================================================================
# 10. Marketing analytics (CMO)
# ======================================================================


def van_westendorp(too_cheap, cheap, expensive, too_expensive, grid_points=400):
    """Van Westendorp PSM from respondent price lists (same length, one price per respondent per question).
    Returns OPP (too cheap x too expensive), IPP (cheap x expensive) and the acceptable range
    (PMC: too cheap x 'not cheap'; PME: too expensive x 'not expensive')."""
    allp = too_cheap + cheap + expensive + too_expensive
    lo, hi = min(allp), max(allp)
    n = len(too_cheap)
    ge = lambda xs, p: sum(1 for x in xs if x >= p) / n   # share saying "too cheap/cheap" at price p (descending curves)
    le = lambda xs, p: sum(1 for x in xs if x <= p) / n   # share saying "expensive/too expensive" at p (ascending)
    pts = [lo + (hi - lo) * i / grid_points for i in range(grid_points + 1)]

    def cross(f, g):
        prev = None
        for p in pts:
            d = f(p) - g(p)
            if prev is not None and (d == 0 or (d > 0) != (prev[1] > 0)):
                return p
            prev = (p, d)
        return None
    return {"OPP": cross(lambda p: ge(too_cheap, p), lambda p: le(too_expensive, p)),
            "IPP": cross(lambda p: ge(cheap, p), lambda p: le(expensive, p)),
            "PMC": cross(lambda p: ge(too_cheap, p), lambda p: 1 - ge(cheap, p)),
            "PME": cross(lambda p: le(too_expensive, p), lambda p: 1 - le(expensive, p)),
            "n": n, "note": "Stated-preference survey: indicates an acceptable range, not true willingness to pay."}


def gabor_granger(prices, purchase_shares, unit_cost=0.0, market_size=1.0):
    """Revenue- and profit-maximising price from a stated purchase-likelihood curve."""
    rows = [{"price": p, "share": s, "revenue": p * s * market_size, "profit": (p - unit_cost) * s * market_size}
            for p, s in zip(prices, purchase_shares)]
    return {"rows": rows, "revenue_max_price": max(rows, key=lambda r: r["revenue"])["price"],
            "profit_max_price": max(rows, key=lambda r: r["profit"])["price"]}


def funnel(top, rates):
    """Stage counts from top-of-funnel and stage conversion rates; overall conversion."""
    stages = [top]
    for r in rates:
        stages.append(stages[-1] * r)
    return {"stages": stages, "overall_conversion": stages[-1] / top}


def ab_sample_size(baseline_rate, min_detectable_effect, alpha=0.05, power=0.8, relative=True):
    """Per-arm sample size for a two-proportion z-test (two-sided)."""
    p1 = baseline_rate
    p2 = p1 * (1 + min_detectable_effect) if relative else p1 + min_detectable_effect
    za, zb = norm_ppf(1 - alpha / 2), norm_ppf(power)
    pbar = (p1 + p2) / 2
    n = (za * math.sqrt(2 * pbar * (1 - pbar)) + zb * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2 / (p2 - p1) ** 2
    return {"per_arm": math.ceil(n), "p1": p1, "p2": p2}


def ab_test(conversions_a, n_a, conversions_b, n_b):
    """Two-proportion z-test (pooled), two-sided p-value and 95% CI of the difference."""
    pa, pb = conversions_a / n_a, conversions_b / n_b
    pp = (conversions_a + conversions_b) / (n_a + n_b)
    se = math.sqrt(pp * (1 - pp) * (1 / n_a + 1 / n_b))
    z = (pb - pa) / se
    se_u = math.sqrt(pa * (1 - pa) / n_a + pb * (1 - pb) / n_b)
    return {"rate_a": pa, "rate_b": pb, "lift": pb / pa - 1, "z": z, "p_value": 2 * (1 - norm_cdf(abs(z))),
            "ci95_diff": [pb - pa - 1.959964 * se_u, pb - pa + 1.959964 * se_u]}


def marketing_roi(spend, revenue_attributed, gross_margin):
    """ROAS (revenue/spend) vs true marketing ROI on gross margin."""
    return {"roas": revenue_attributed / spend, "roi_on_margin": (revenue_attributed * gross_margin - spend) / spend}


def elasticity(p1, q1, p2, q2):
    """Arc (midpoint) price elasticity of demand."""
    return ((q2 - q1) / ((q1 + q2) / 2)) / ((p2 - p1) / ((p1 + p2) / 2))


# ======================================================================
# 11. Strategy (CSO)
# ======================================================================


def market_sizing(segments, serviceable_share=None, obtainable_share=None):
    """Bottom-up TAM: segments = [{name, units (customers), annual_value}]; optional SAM and SOM shares."""
    rows = [{**s, "tam": s["units"] * s["annual_value"]} for s in segments]
    tam = sum(r["tam"] for r in rows)
    out = {"segments": rows, "tam": tam}
    if serviceable_share is not None:
        out["sam"] = tam * serviceable_share
        if obtainable_share is not None:
            out["som"] = out["sam"] * obtainable_share
    return out


def hhi(shares):
    """Herfindahl-Hirschman index from market shares in % (e.g. [30, 20, 10]). US DOJ 2023 thresholds."""
    h = sum(s ** 2 for s in shares)
    band = "highly concentrated" if h > 1800 else "moderately concentrated" if h >= 1000 else "unconcentrated"
    return {"hhi": h, "band": band}


def bass_diffusion(market_potential, p, q, periods):
    """Bass adoption curve: new adopters per period and cumulative (discrete-time)."""
    cum, out = 0.0, []
    for t in range(1, int(periods) + 1):
        new = (p + q * cum / market_potential) * (market_potential - cum)
        cum += new
        out.append({"period": t, "new": new, "cumulative": cum, "penetration": cum / market_potential})
    return out


def decision_matrix(options, weights, perturb=0.2):
    """Weighted scoring. options = {name: {criterion: score}}, weights = {criterion: w}.
    Tests rank stability by perturbing each weight +/- perturb (relative)."""
    tw = sum(weights.values())
    def score(ws):
        t = sum(ws.values())
        return {o: sum(sc[c] * ws[c] / t for c in ws) for o, sc in options.items()}
    base = score(weights)
    winner = max(base, key=base.get)
    flips = []
    for c in weights:
        for d in (-perturb, perturb):
            w2 = dict(weights); w2[c] = max(0.0, w2[c] * (1 + d))
            s2 = score(w2); w = max(s2, key=s2.get)
            if w != winner:
                flips.append({"criterion": c, "change": d, "new_winner": w})
    return {"scores": base, "winner": winner, "robust": not flips, "rank_flips": flips, "weights_normalised": {k: v / tw for k, v in weights.items()}}


def expected_value(outcomes):
    """outcomes = [{name, probability, value}] -> EV, sd, downside probability."""
    if abs(sum(o["probability"] for o in outcomes) - 1) > 1e-9:
        raise ValueError("probabilities must sum to 1")
    ev = sum(o["probability"] * o["value"] for o in outcomes)
    sd = math.sqrt(sum(o["probability"] * (o["value"] - ev) ** 2 for o in outcomes))
    return {"expected_value": ev, "sd": sd, "prob_loss": sum(o["probability"] for o in outcomes if o["value"] < 0)}


# ======================================================================
# 12. Risk (CRO)
# ======================================================================


def risk_register(risks):
    """risks = [{name, likelihood 1-5, impact 1-5, [expected_loss]}] -> scored, ranked, rated."""
    rows = []
    for r in risks:
        s = r["likelihood"] * r["impact"]
        rating = "CRITICAL" if s >= 15 or r["impact"] == 5 and r["likelihood"] >= 3 else "SIGNIFICANT" if s >= 8 else "WATCH"
        rows.append({**r, "score": s, "rating": rating})
    rows.sort(key=lambda x: -x["score"])
    return rows


def pert_estimate(optimistic, most_likely, pessimistic):
    """Three-point (PERT) estimate: mean and sd."""
    return {"mean": (optimistic + 4 * most_likely + pessimistic) / 6, "sd": (pessimistic - optimistic) / 6}


def var_cvar(samples, confidence=0.95):
    """Historical/simulated VaR and CVaR (expected shortfall) of a P&L sample (losses negative)."""
    s = sorted(samples)
    k = max(1, int((1 - confidence) * len(s)))
    return {"var": -s[k - 1], "cvar": -sum(s[:k]) / k, "confidence": confidence}


def covenant_headroom(ebitda, net_debt, interest, max_leverage, min_coverage):
    """How far EBITDA can fall before breaching leverage or interest-cover covenants."""
    lev_break = net_debt / max_leverage
    cov_break = interest * min_coverage
    binding = max(lev_break, cov_break)
    return {"leverage": net_debt / ebitda, "coverage": ebitda / interest if interest else None,
            "ebitda_at_leverage_breach": lev_break, "ebitda_at_coverage_breach": cov_break,
            "max_ebitda_decline_pct": 1 - binding / ebitda}


# ======================================================================
# CLI
# ======================================================================

PUBLIC = {k: v for k, v in dict(globals()).items() if callable(v) and not k.startswith("_") and v.__module__ == __name__
          and k not in ("main",)}


def _clean(o):
    if isinstance(o, float):
        return round(o, 10) if math.isfinite(o) else str(o)
    if isinstance(o, dict):
        return {k: _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_clean(v) for v in o]
    return o


def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help", "list"):
        for k in sorted(PUBLIC):
            doc = (PUBLIC[k].__doc__ or "").strip().split("\n")[0]
            print("%-26s %s" % (k, doc))
        return 0
    if argv[1] == "doc":
        for name in argv[2:]:
            print("## %s\n%s\n" % (name, (PUBLIC[name].__doc__ or "").strip()) if name in PUBLIC else "unknown %s" % name)
        return 0
    fn = PUBLIC.get(argv[1])
    if not fn:
        print("unknown function %s (run: list)" % argv[1], file=sys.stderr); return 2
    if len(argv) > 2:
        raw = argv[2]
        if raw.startswith("@"):
            with open(raw[1:], encoding="utf-8") as fh:
                raw = fh.read()
        kwargs = json.loads(raw)
    else:
        kwargs = {}
    if len(argv) > 3 and argv[3] == "--doc":
        print(fn.__doc__); return 0
    print(json.dumps(_clean(fn(**kwargs)), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
