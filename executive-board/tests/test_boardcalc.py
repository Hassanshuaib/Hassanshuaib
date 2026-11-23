#!/usr/bin/env python3
"""Independent verification of scripts/boardcalc.py.

Independent references used:
  * LibreOffice Calc built-in functions (NPV, IRR, MIRR, PMT) recalculated headless.
  * A live-formula Excel version of the three-statement model, recalculated by LibreOffice.
  * Closed-form identities (annuities, Gordon growth, EOQ, Little's law, Hamada).
  * Textbook cases with known answers (multiple-IRR polynomial, Erlang C by explicit formula).
Run:  python3 -I tests/test_boardcalc.py   (LibreOffice tests are skipped if soffice is absent)
"""
import math
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "scripts"))
import boardcalc as bc  # noqa: E402

SOFFICE = shutil.which("soffice") or shutil.which("libreoffice")


def close(a, b, rel=1e-9, abs_=1e-9):
    return abs(a - b) <= max(abs_, rel * max(abs(a), abs(b)))


class TestTimeValue(unittest.TestCase):
    def test_npv_annuity_closed_form(self):
        cfs = [-1000] + [300] * 5
        self.assertTrue(close(bc.npv(0.08, cfs), -1000 + 300 * (1 - 1.08 ** -5) / 0.08))

    def test_irr_simple_and_root(self):
        cfs = [-100, 30, 40, 50, 20]
        r = bc.irr(cfs)["irr"]
        self.assertTrue(abs(bc.npv(r, cfs)) < 1e-8)

    def test_multiple_irr_textbook(self):
        # -1 + 6x - 11x^2 + 6x^3, x = 1/(1+r): roots x = 1, 1/2, 1/3 -> r = 0%, 100%, 200%
        res = bc.irr([-1, 6, -11, 6])
        self.assertEqual(len(res["all_irrs"]), 3)
        for got, exp in zip(res["all_irrs"], [0.0, 1.0, 2.0]):
            self.assertAlmostEqual(got, exp, places=7)
        self.assertIn("Multiple IRRs", res["warning"])

    def test_payback(self):
        self.assertAlmostEqual(bc.payback([-100, 40, 40, 40]), 2.5)

    def test_crossover_and_conflict(self):
        out = bc.compare_projects(0.10, {"A": [-1000, 900, 300, 100], "B": [-1000, 0, 0, 1600]})
        x = out["crossover_rates"]["A vs B"][0]
        self.assertTrue(abs(bc.npv(x, [-1000, 900, 300, 100]) - bc.npv(x, [-1000, 0, 0, 1600])) < 1e-6)
        self.assertEqual(out["rank_by_npv"][0], "B")   # at 10%: NPV A=141, B=202
        self.assertAlmostEqual(out["projects"]["B"]["irr"], 1.6 ** (1 / 3) - 1, places=9)
        self.assertEqual(out["rank_by_irr"][0], "A")   # but A has higher IRR -> conflict flagged
        self.assertTrue(out["notes"])


class TestCostOfCapitalDCF(unittest.TestCase):
    def test_hamada_roundtrip(self):
        bu = bc.unlever_beta(1.3, 0.5, 0.2)
        self.assertTrue(close(bc.relever_beta(bu, 0.5, 0.2), 1.3))

    def test_wacc(self):
        self.assertTrue(close(bc.wacc(600, 400, 0.12, 0.07, 0.2), 0.6 * 0.12 + 0.4 * 0.07 * 0.8))

    def test_dcf_gordon_identity(self):
        # FCF growing at g from year 1 forever: EV must equal FCF1/(r-g) whatever the explicit horizon.
        r, g, f1 = 0.10, 0.03, 100.0
        fcff = [f1 * (1 + g) ** t for t in range(7)]
        ev = bc.dcf(fcff, r, terminal_growth=g)["methods"]["gordon"]["enterprise_value"]
        self.assertTrue(close(ev, f1 / (r - g), rel=1e-10))

    def test_dcf_cross_check_consistency(self):
        fcff = [100, 110, 120]
        out = bc.dcf(fcff, 0.1, terminal_growth=0.03, exit_multiple=10, terminal_metric=150)
        # the exit-implied growth must reproduce the exit TV under Gordon
        g = out["exit_implied_growth"]
        self.assertTrue(close(fcff[-1] * (1 + g) / (0.1 - g), 10 * 150, rel=1e-9))

    def test_value_driver_no_value_when_roic_eq_wacc(self):
        v1 = bc.value_driver(100, 0.0, 0.10, 0.10)
        v2 = bc.value_driver(100, 0.05, 0.10, 0.10)
        self.assertTrue(close(v1, v2))  # growth at ROIC = WACC creates no value


class TestThreeStatement(unittest.TestCase):
    CASE = dict(revenue0=10_000_000,
                opening={"cash": 1_000_000, "ar": 1_200_000, "inventory": 900_000, "ppe": 5_000_000,
                         "ap": 700_000, "debt": 3_000_000, "equity": 4_400_000},
                years=5, growth=[0.15, 0.12, 0.10, 0.08, 0.06], gross_margin=0.42, opex_pct=0.25,
                da_pct_rev=0.05, capex_pct_rev=[0.12, 0.10, 0.08, 0.06, 0.06], dso=45, dio=60, dpo=40,
                tax_rate=0.20, interest_rate=0.07, revolver_rate=0.09, min_cash=800_000,
                debt_repayment=600_000, payout_ratio=0.3)

    def test_integrity(self):
        res = bc.three_statement(**self.CASE)
        self.assertTrue(res["balanced"])
        for c in res["checks"]:
            self.assertLess(abs(c["balance_diff"]), 1e-4)
            self.assertLess(abs(c["cash_tieout_diff"]), 1e-4)
            self.assertLess(abs(c["re_rollforward_diff"]), 1e-4)

    def test_loss_and_revolver_paths(self):
        case = dict(self.CASE); case.update(gross_margin=0.20, opex_pct=0.30)   # loss-making -> NOL + revolver
        res = bc.three_statement(**case)
        self.assertTrue(res["balanced"])
        self.assertTrue(all(y["tax"] == 0 for y in res["years"]))
        self.assertTrue(any(y["revolver"] > 0 for y in res["years"]))
        self.assertTrue(all(y["cash"] >= case["min_cash"] - 1e-6 for y in res["years"]))

    def test_unbalanced_opening_rejected(self):
        case = dict(self.CASE); case["opening"] = dict(case["opening"], equity=1)
        with self.assertRaises(ValueError):
            bc.three_statement(**case)

    @unittest.skipUnless(SOFFICE, "LibreOffice not installed")
    def test_excel_formulas_match_python(self):
        for variant in ({}, {"gross_margin": 0.20, "opex_pct": 0.30}):
            case = dict(self.CASE); case.update(variant)
            tmp = tempfile.mkdtemp(); path = os.path.join(tmp, "ts.xlsx")
            out = bc.three_statement_xlsx(path, **case)
            R, years = out["rows"], out["python_result"]["years"]
            expected = {}
            for t, y in enumerate(years):
                col = chr(ord("C") + t)
                for k in ("revenue", "ebitda", "net_income", "tax", "cash", "ar", "ppe", "debt", "revolver", "equity",
                          "total_assets", "total_liabilities_equity", "cfo"):
                    expected["%s%d" % (col, R[k])] = y[k]
                expected["%s%d" % (col, R["balance_check"])] = 0.0
            cmp_ = bc.recalc_compare(path, expected)
            self.assertTrue(cmp_["available"])
            self.assertEqual(cmp_["mismatches"], [], cmp_)
            self.assertLess(cmp_["max_rel_error"], 1e-9)
            shutil.rmtree(tmp, ignore_errors=True)


@unittest.skipUnless(SOFFICE, "LibreOffice not installed")
class TestAgainstSpreadsheetFunctions(unittest.TestCase):
    def test_npv_irr_mirr_pmt(self):
        from openpyxl import Workbook, load_workbook
        cases = [[-100, 30, 40, 50, 20], [-5000, 1200, 1500, 1800, 2100, 900], [-2500, 0, 0, 1200, 1800, 900]]
        wb = Workbook(); ws = wb.active
        for i, cfs in enumerate(cases):
            r = i + 1
            for j, v in enumerate(cfs):
                ws.cell(r, 1 + j, v)
            last = chr(ord("A") + len(cfs) - 1)
            ws["J%d" % r] = "=A%d+NPV(0.1,B%d:%s%d)" % (r, r, last, r)
            ws["K%d" % r] = "=IRR(A%d:%s%d)" % (r, last, r)
            ws["L%d" % r] = "=MIRR(A%d:%s%d,0.08,0.12)" % (r, last, r)
        ws["M1"] = "=PMT(0.05/12,60,100000)"
        tmp = tempfile.mkdtemp(); p = os.path.join(tmp, "f.xlsx"); wb.save(p)
        subprocess.run([SOFFICE, "--headless", "--convert-to", "xlsx", "--outdir", os.path.join(tmp, "o"), p],
                       check=True, capture_output=True, timeout=180)
        ws2 = load_workbook(os.path.join(tmp, "o", "f.xlsx"), data_only=True).active
        for i, cfs in enumerate(cases):
            r = i + 1
            self.assertTrue(close(bc.npv(0.1, cfs), ws2["J%d" % r].value, rel=1e-9))
            self.assertTrue(close(bc.irr(cfs)["irr"], ws2["K%d" % r].value, rel=1e-7))
            self.assertTrue(close(bc.mirr(cfs, 0.08, 0.12), ws2["L%d" % r].value, rel=1e-9))
        self.assertTrue(close(bc.pmt(0.05 / 12, 60, 100000), ws2["M1"].value, rel=1e-9))
        shutil.rmtree(tmp, ignore_errors=True)


class TestProjectAndRisk(unittest.TestCase):
    BASE = dict(life=5, units=10000, price=50, var_cost_pct=0.55, fixed_cost=120000, capex=400000,
                nwc_pct=0.10, tax_rate=0.20, discount_rate=0.12, salvage=40000)

    def test_project_hand_calc(self):
        p = bc.project(**self.BASE)
        rev = 500000; dep = 80000
        ebit = rev * 0.45 - 120000 - dep
        fcf1 = ebit * 0.8 + dep - 50000
        self.assertTrue(close(p["cashflows"][1], fcf1))
        fcf5 = ebit * 0.8 + dep + 40000 - (40000 - 0) * 0.2 + 50000   # after-tax salvage + NWC recovery
        self.assertTrue(close(p["cashflows"][5], fcf5))
        self.assertTrue(close(p["npv"], bc.npv(0.12, p["cashflows"])))

    def test_breakeven_input_zeroes_npv(self):
        be = bc.breakeven_input(self.BASE, "price", 1, 200)
        self.assertLess(abs(bc.project(**{**self.BASE, "price": be["breakeven_value"]})["npv"]), 1e-4)

    def test_mc_degenerate_equals_base(self):
        mc = bc.montecarlo(self.BASE, {"price": ["uniform", 50, 50]}, n=200)
        self.assertTrue(close(mc["mean"], bc.project(**self.BASE)["npv"]))

    def test_mc_linear_mean(self):
        # NPV is linear in price -> E[NPV] = NPV(E[price]) within Monte Carlo error
        mc = bc.montecarlo(self.BASE, {"price": ["normal", 50, 5]}, n=20000, seed=7)
        self.assertLess(abs(mc["mean"] - bc.project(**self.BASE)["npv"]), 4 * mc["mc_standard_error_of_mean"])

    def test_tornado_sorted(self):
        t = bc.tornado(self.BASE, {"price": [45, 55], "fixed_cost": [100000, 140000], "tax_rate": [0.15, 0.25]})
        swings = [r["swing"] for r in t["rows"]]
        self.assertEqual(swings, sorted(swings, reverse=True))


class TestFinanceMisc(unittest.TestCase):
    def test_breakeven(self):
        b = bc.breakeven(100000, 50, 30, actual_units=8000)
        self.assertAlmostEqual(b["breakeven_units"], 5000)
        self.assertAlmostEqual(b["margin_of_safety"], 0.375)
        self.assertAlmostEqual(b["operating_leverage"], 160000 / 60000)

    def test_ltv_closed_form_vs_sum(self):
        a = bc.ltv(100, 0.7, 0.05, 0.01)["ltv"]
        b = bc.ltv(100, 0.7, 0.05, 0.01, max_months=5000)["ltv"]
        self.assertTrue(close(a, b, rel=1e-9) and close(a, 70 / 0.06))

    def test_lbo_bridge_and_no_debt(self):
        out = bc.lbo(100, 8, 4, years=5, ebitda_growth=0.06, exit_multiple=9)
        self.assertLess(abs(out["bridge_check"]), 1e-6)
        nod = bc.lbo(100, 8, 0, years=3, ebitda_growth=0.0, fees_pct=0, capex_pct_ebitda=1.0, tax_rate=0, da_pct_ebitda=0)
        self.assertTrue(close(nod["moic"], 1.0))     # no growth, no debt, all EBITDA reinvested -> MOIC 1.0

    def test_accretion_breakeven_synergies(self):
        k = dict(acq_net_income=500, acq_shares=100, target_net_income=60, price_paid=1200, pct_cash=0.5,
                 pct_stock=0.5, acq_share_price=60, cost_of_debt=0.07, tax_rate=0.2)
        s = bc.accretion_dilution(**k)["breakeven_synergies_pre_tax"]
        self.assertTrue(close(bc.accretion_dilution(**k, synergies_pre_tax=s)["accretion_pct"], 0.0, abs_=1e-12))

    def test_variance_decomposition_sums(self):
        v = bc.variance_analysis(10, 1000, 11, 900)
        self.assertTrue(close(v["price_variance"] + v["volume_variance"], v["total_variance"]))


class TestOpsMarketingStrategy(unittest.TestCase):
    def test_erlang_c_explicit_formula(self):
        lam, mu, c = 100.0, 20.0, 6       # 5 Erlangs on 6 agents
        a = lam / mu
        s = sum(a ** k / math.factorial(k) for k in range(c))
        top = a ** c / math.factorial(c) * c / (c - a)
        self.assertTrue(close(bc.erlang_c(lam, mu, c)["p_wait"], top / (s + top), rel=1e-12))

    def test_staffing_monotone(self):
        r = bc.staff_for_service_level(100, 20, 20 / 3600, 0.8)
        self.assertGreaterEqual(r["service_level"], 0.8)
        self.assertLess(bc.erlang_c(100, 20, r["servers"] - 1, 20 / 3600).get("service_level", 0), 0.8)

    def test_eoq_littles(self):
        self.assertTrue(close(bc.eoq(12000, 50, 2.4)["eoq"], math.sqrt(2 * 12000 * 50 / 2.4)))
        self.assertTrue(close(bc.littles_law(throughput=20, lead_time=3)["wip"], 60))

    def test_norm_ppf(self):
        self.assertAlmostEqual(bc.norm_ppf(0.975), 1.959963985, places=8)
        self.assertAlmostEqual(bc.norm_cdf(bc.norm_ppf(0.123)), 0.123, places=9)

    def test_ab_sample_size_textbook(self):
        # 10% -> 12% (20% relative), alpha .05, power .8: ~3,841 per arm (standard tables give ~3,840)
        n = bc.ab_sample_size(0.10, 0.20)["per_arm"]
        self.assertTrue(3800 <= n <= 3900, n)

    def test_hhi_and_decision(self):
        self.assertEqual(bc.hhi([30, 30, 20, 20])["hhi"], 2600)
        d = bc.decision_matrix({"A": {"x": 9, "y": 2}, "B": {"x": 5, "y": 6}}, {"x": 0.5, "y": 0.5})
        self.assertEqual(d["winner"], "B" if d["scores"]["B"] > d["scores"]["A"] else "A")

    def test_bass_cumulative_bounded(self):
        out = bc.bass_diffusion(1000, 0.03, 0.38, 30)
        self.assertTrue(all(0 <= x["cumulative"] <= 1000 for x in out))

    def test_six_sigma_reference_point(self):
        # 3.4 DPMO is the textbook 6-sigma point (with 1.5 shift)
        self.assertAlmostEqual(bc.dpmo_sigma(34, 1_000_000, 10)["sigma_level"], 6.0, places=2)

    def test_van_westendorp_symmetric(self):
        tc = [5] * 50 + [7] * 50; ch = [8] * 50 + [10] * 50; ex = [14] * 50 + [16] * 50; te = [18] * 50 + [22] * 50
        r = bc.van_westendorp(tc, ch, ex, te)
        self.assertTrue(r["PMC"] <= r["OPP"] <= r["PME"] and r["PMC"] <= r["IPP"] <= r["PME"], r)

    def test_gabor_granger(self):
        g = bc.gabor_granger([10, 20, 30, 40], [0.9, 0.7, 0.4, 0.1], unit_cost=8)
        self.assertEqual(g["revenue_max_price"], 20)   # 9, 14, 12, 4
        self.assertEqual(g["profit_max_price"], 30)    # profits 1.8, 8.4, 8.8, 3.2
        self.assertEqual(max(g["rows"], key=lambda r: r["profit"])["price"], g["profit_max_price"])

    def test_covenant(self):
        c = bc.covenant_headroom(ebitda=100, net_debt=300, interest=20, max_leverage=4.0, min_coverage=3.0)
        self.assertTrue(close(c["max_ebitda_decline_pct"], 0.25))  # leverage binds at EBITDA 75


if __name__ == "__main__":
    unittest.main(verbosity=1)
