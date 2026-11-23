"""Al-Waha Foods (fictional, illustrative) - integrated 3-statement model, SAR.

1. Builds an .xlsx with LIVE formulas: Inputs (blue), IS, BS, CF, Debt, Checks.
2. Recalculates it with LibreOffice headless and scans for errors.
3. Recomputes the model independently in plain Python (and cross-checks with boardcalc.three_statement).
4. Compares every key Excel value with the Python values.

Conventions: EBITDA = GP - Opex; D&A below EBITDA. Interest on OPENING balances (no circularity).
Tax = 20% x MAX(0, EBT), no loss carry-forward. Dividends = 25% x MAX(0, NI), paid in-year.
Working capital on ENDING balances, 365-day year. Revolver = MAX(min_cash - cash_pre_revolver, -opening_revolver).
"""
import json, os, shutil, subprocess, sys, tempfile
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill

OUT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XLSX = os.path.join(OUT_DIR, "2026-11-23-cfo-alwaha-3statement.xlsx")

# ---------------- Inputs (all CEO inputs) ----------------
INP = dict(rev0=24_000_000, growth=[0.18, 0.12, 0.08], gm=[0.38] * 3, opex=[0.22] * 3, da=[0.04] * 3,
           capex=[0.09, 0.07, 0.05], dso=[40] * 3, dio=[55] * 3, dpo=[35] * 3, days=365, tax=[0.20] * 3,
           r_term=[0.08] * 3, r_rev=[0.10] * 3, min_cash=[1_500_000] * 3, repay=[1_000_000] * 3, payout=[0.25] * 3,
           open=dict(cash=2_000_000, ar=2_600_000, inv=1_900_000, ppe=9_000_000, ap=1_500_000,
                     term=6_000_000, rev=0, eq=8_000_000))
Y = ["C", "D", "E"]  # Y1..Y3 columns; B = Y0

# ---------------- 1. Build workbook ----------------
BLUE = Font(color="0000FF"); BOLD = Font(bold=True); HDR = PatternFill("solid", fgColor="DDEBF7")
wb = Workbook()
inp = wb.active; inp.title = "Inputs"
inp["A1"] = "Al-Waha Foods - Inputs (SAR; fictional/illustrative). Blue = input."; inp["A1"].font = BOLD
for c, h in zip("ABCDEF", ["Driver", "Y0 / scalar", "Y1", "Y2", "Y3", "Note"]):
    inp[f"{c}3"] = h; inp[f"{c}3"].font = BOLD; inp[f"{c}3"].fill = HDR
rows = [("Revenue Y0 (actual)", "rev0", None, "SAR"), ("Revenue growth", None, "growth", "%"),
        ("Gross margin", None, "gm", "% rev"), ("Opex", None, "opex", "% rev; EBITDA = GP - Opex"),
        ("D&A", None, "da", "% rev; below EBITDA"), ("Capex", None, "capex", "% rev"),
        ("DSO", None, "dso", "days on revenue, ending AR"), ("DIO", None, "dio", "days on COGS, ending inventory"),
        ("DPO", None, "dpo", "days on COGS, ending AP"), ("Days in year", "days", None, ""),
        ("Tax rate", None, "tax", "on MAX(0,EBT); no loss c/f"), ("Term-debt interest", None, "r_term", "on opening balance"),
        ("Revolver interest", None, "r_rev", "on opening balance"), ("Minimum cash", None, "min_cash", "SAR"),
        ("Term-debt repayment", None, "repay", "SAR/yr (capped at balance)"), ("Dividend payout", None, "payout", "on MAX(0,NI), paid in-year")]
R = {}
for i, (lab, sk, vk, note) in enumerate(rows, start=4):
    inp[f"A{i}"] = lab; inp[f"F{i}"] = note; R[sk or vk] = i
    if sk: inp[f"B{i}"] = INP[sk]; inp[f"B{i}"].font = BLUE
    if vk:
        for c, v in zip(Y, INP[vk]): inp[f"{c}{i}"] = v; inp[f"{c}{i}"].font = BLUE
inp["A21"] = "Opening balance sheet (end Y0)"; inp["A21"].font = BOLD
ob = [("Cash", "cash"), ("Accounts receivable", "ar"), ("Inventory", "inv"), ("Net PP&E", "ppe"),
      ("Accounts payable", "ap"), ("Term debt", "term"), ("Revolver", "rev"), ("Equity", "eq")]
for i, (lab, k) in enumerate(ob, start=22):
    inp[f"A{i}"] = lab; inp[f"B{i}"] = INP["open"][k]; inp[f"B{i}"].font = BLUE; R["o_" + k] = i
inp["A30"] = "Opening check: assets - (liabilities + equity)"
inp["B30"] = "=(B22+B23+B24+B25)-(B26+B27+B28+B29)"
inp.column_dimensions["A"].width = 44; inp.column_dimensions["F"].width = 36

def sheet(name, title):
    ws = wb.create_sheet(name); ws["A1"] = title; ws["A1"].font = BOLD
    for c, h in zip("ABCDE", ["SAR", "Y0A", "Y1F", "Y2F", "Y3F"]):
        ws[f"{c}3"] = h; ws[f"{c}3"].font = BOLD; ws[f"{c}3"].fill = HDR
    ws.column_dimensions["A"].width = 40
    for c in "BCDE": ws.column_dimensions[c].width = 15
    return ws

IS = sheet("IS", "Income statement"); BS = sheet("BS", "Balance sheet (end of year)")
CF = sheet("CF", "Cash flow statement (indirect)"); DB = sheet("Debt", "Debt & revolver schedule")
CK = sheet("Checks", "Integrity checks (all should be 0 / TRUE)")
def I(key, c): return f"Inputs!{c}{R[key]}"

def put(ws, row, label, b=None, f=None, bold=False):
    ws[f"A{row}"] = label
    if bold: ws[f"A{row}"].font = BOLD
    if b is not None: ws[f"B{row}"] = b
    if f:
        for k, c in enumerate(Y):
            p = "BCD"[k]; ws[f"{c}{row}"] = f(c, p)
    for c in "BCDE": ws[f"{c}{row}"].number_format = '#,##0;(#,##0);"-"'

# IS
put(IS, 4, "Revenue", f"={I('rev0','B')}", lambda c, p: f"={p}4*(1+{I('growth',c)})", True)
put(IS, 5, "COGS", None, lambda c, p: f"={c}4*(1-{I('gm',c)})")
put(IS, 6, "Gross profit", None, lambda c, p: f"={c}4-{c}5", True)
put(IS, 7, "Opex", None, lambda c, p: f"={c}4*{I('opex',c)}")
put(IS, 8, "EBITDA", None, lambda c, p: f"={c}6-{c}7", True)
put(IS, 9, "D&A", None, lambda c, p: f"={c}4*{I('da',c)}")
put(IS, 10, "EBIT", None, lambda c, p: f"={c}8-{c}9", True)
put(IS, 11, "Interest - term debt", None, lambda c, p: f"=Debt!{c}7")
put(IS, 12, "Interest - revolver", None, lambda c, p: f"=Debt!{c}19")
put(IS, 13, "EBT", None, lambda c, p: f"={c}10-{c}11-{c}12", True)
put(IS, 14, "Tax", None, lambda c, p: f"=MAX(0,{c}13)*{I('tax',c)}")
put(IS, 15, "Net income", None, lambda c, p: f"={c}13-{c}14", True)
put(IS, 16, "Dividends declared & paid", None, lambda c, p: f"=MAX(0,{c}15)*{I('payout',c)}")
put(IS, 17, "Capex (memo)", None, lambda c, p: f"={c}4*{I('capex',c)}")
put(IS, 18, "EBITDA margin (memo, %)", None, lambda c, p: f"={c}8/{c}4")
for c in Y: IS[f"{c}18"].number_format = "0.0%"
# BS
put(BS, 4, "Cash", f"={I('o_cash','B')}", lambda c, p: f"=CF!{c}21")
put(BS, 5, "Accounts receivable", f"={I('o_ar','B')}", lambda c, p: f"=IS!{c}4*{I('dso',c)}/Inputs!$B${R['days']}")
put(BS, 6, "Inventory", f"={I('o_inv','B')}", lambda c, p: f"=IS!{c}5*{I('dio',c)}/Inputs!$B${R['days']}")
put(BS, 7, "Net PP&E", f"={I('o_ppe','B')}", lambda c, p: f"={p}7+IS!{c}17-IS!{c}9")
put(BS, 8, "Total assets", "=SUM(B4:B7)", lambda c, p: f"=SUM({c}4:{c}7)", True)
put(BS, 10, "Accounts payable", f"={I('o_ap','B')}", lambda c, p: f"=IS!{c}5*{I('dpo',c)}/Inputs!$B${R['days']}")
put(BS, 11, "Term debt", f"={I('o_term','B')}", lambda c, p: f"=Debt!{c}6")
put(BS, 12, "Revolver", f"={I('o_rev','B')}", lambda c, p: f"=Debt!{c}18")
put(BS, 13, "Total liabilities", "=SUM(B10:B12)", lambda c, p: f"=SUM({c}10:{c}12)", True)
put(BS, 14, "Equity", f"={I('o_eq','B')}", lambda c, p: f"={p}14+IS!{c}15-IS!{c}16")
put(BS, 15, "Total liabilities & equity", "=B13+B14", lambda c, p: f"={c}13+{c}14", True)
put(BS, 17, "CHECK: Assets - L&E", "=B8-B15", lambda c, p: f"=ROUND({c}8-{c}15,4)", True)
put(BS, 18, "CHECK: CF ending cash - BS cash", None, lambda c, p: f"=ROUND(CF!{c}21-{c}4,4)", True)
# CF
put(CF, 4, "Net income", None, lambda c, p: f"=IS!{c}15")
put(CF, 5, "D&A", None, lambda c, p: f"=IS!{c}9")
put(CF, 6, "(Increase)/decrease in AR", None, lambda c, p: f"=BS!{p}5-BS!{c}5")
put(CF, 7, "(Increase)/decrease in inventory", None, lambda c, p: f"=BS!{p}6-BS!{c}6")
put(CF, 8, "Increase/(decrease) in AP", None, lambda c, p: f"=BS!{c}10-BS!{p}10")
put(CF, 9, "Cash flow from operations (CFO)", None, lambda c, p: f"=SUM({c}4:{c}8)", True)
put(CF, 11, "Capex", None, lambda c, p: f"=-IS!{c}17")
put(CF, 12, "Cash flow from investing (CFI)", None, lambda c, p: f"={c}11", True)
put(CF, 14, "Term-debt repayment", None, lambda c, p: f"=-Debt!{c}5")
put(CF, 15, "Revolver draw/(repayment)", None, lambda c, p: f"=Debt!{c}17")
put(CF, 16, "Dividends paid", None, lambda c, p: f"=-IS!{c}16")
put(CF, 17, "Cash flow from financing (CFF)", None, lambda c, p: f"=SUM({c}14:{c}16)", True)
put(CF, 19, "Net change in cash", None, lambda c, p: f"={c}9+{c}12+{c}17", True)
put(CF, 20, "Opening cash", None, lambda c, p: f"=BS!{p}4")
put(CF, 21, "Ending cash", None, lambda c, p: f"={c}20+{c}19", True)
put(CF, 23, "Free cash flow (CFO + capex, memo)", None, lambda c, p: f"={c}9+{c}11", True)
# Debt
put(DB, 4, "Term debt - opening", None, lambda c, p: f"={p}6")
put(DB, 5, "Scheduled repayment", None, lambda c, p: f"=MIN({I('repay',c)},{c}4)")
put(DB, 6, "Term debt - closing", f"={I('o_term','B')}", lambda c, p: f"={c}4-{c}5", True)
put(DB, 7, "Term interest (opening x rate)", None, lambda c, p: f"={c}4*{I('r_term',c)}")
put(DB, 9, "Opening cash", None, lambda c, p: f"=BS!{p}4")
put(DB, 10, "CFO", None, lambda c, p: f"=CF!{c}9")
put(DB, 11, "CFI", None, lambda c, p: f"=CF!{c}12")
put(DB, 12, "Term repayment", None, lambda c, p: f"=CF!{c}14")
put(DB, 13, "Dividends", None, lambda c, p: f"=CF!{c}16")
put(DB, 14, "Cash before revolver", None, lambda c, p: f"=SUM({c}9:{c}13)", True)
put(DB, 15, "Minimum cash", None, lambda c, p: f"={I('min_cash',c)}")
put(DB, 16, "Revolver - opening", None, lambda c, p: f"={p}18")
put(DB, 17, "Draw/(repayment) = MAX(min - pre-cash, -opening)", None, lambda c, p: f"=MAX({c}15-{c}14,-{c}16)")
put(DB, 18, "Revolver - closing", f"={I('o_rev','B')}", lambda c, p: f"={c}16+{c}17", True)
put(DB, 19, "Revolver interest (opening x rate)", None, lambda c, p: f"={c}16*{I('r_rev',c)}")
DB["A21"] = "No circularity: interest uses opening balances, so CFO does not depend on this year's revolver draw."
# Checks
put(CK, 4, "Assets - L&E", "=BS!B17", lambda c, p: f"=BS!{c}17")
put(CK, 5, "CF ending cash - BS cash", None, lambda c, p: f"=BS!{c}18")
put(CK, 6, "Equity roll-forward (open+NI-div-close)", None, lambda c, p: f"=ROUND(BS!{p}14+IS!{c}15-IS!{c}16-BS!{c}14,4)")
put(CK, 7, "PP&E roll-forward (open+capex-D&A-close)", None, lambda c, p: f"=ROUND(BS!{p}7+IS!{c}17-IS!{c}9-BS!{c}7,4)")
put(CK, 8, "Cash >= minimum (TRUE)", None, lambda c, p: f"=BS!{c}4>=Inputs!{c}{R['min_cash']}-0.001")
put(CK, 9, "Revolver >= 0 (TRUE)", None, lambda c, p: f"=Debt!{c}18>=-0.001")
put(CK, 10, "Opening BS check (Inputs)", "=Inputs!B30")
CK["A12"] = "ALL CHECKS PASS"; CK["A12"].font = BOLD
CK["B12"] = ('=AND(MAX(ABS(B4),ABS(C4),ABS(D4),ABS(E4))<0.01,MAX(ABS(C5),ABS(D5),ABS(E5))<0.01,'
             'MAX(ABS(C6),ABS(D6),ABS(E6))<0.01,MAX(ABS(C7),ABS(D7),ABS(E7))<0.01,AND(C8:E9),ABS(B10)<0.01)')
wb.save(XLSX)

# ---------------- 2. Recalculate in LibreOffice ----------------
tmp = tempfile.mkdtemp()
subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx", "--outdir", tmp, XLSX],
               check=True, capture_output=True, timeout=180)
rc = load_workbook(os.path.join(tmp, os.path.basename(XLSX)), data_only=True)
errors = [f"{ws.title}!{cell.coordinate}={cell.value}" for ws in rc for row in ws.iter_rows() for cell in row
          if isinstance(cell.value, str) and (cell.value.startswith("#") or cell.value.startswith("Err:"))]
formulas = sum(1 for ws in wb for row in ws.iter_rows() for cell in row
               if isinstance(cell.value, str) and cell.value.startswith("="))

# ---------------- 3. Independent Python recompute ----------------
def model(INP):
  o = INP["open"]; cash, ar, inv, ppe, ap, term, revo, eq = (o[k] for k in ["cash", "ar", "inv", "ppe", "ap", "term", "rev", "eq"])
  rev = INP["rev0"]; py = []
  for t in range(3):
    rev = rev * (1 + INP["growth"][t]); cogs = rev * (1 - INP["gm"][t]); gp = rev - cogs
    ebitda = gp - rev * INP["opex"][t]; da = rev * INP["da"][t]; ebit = ebitda - da
    i_term = term * INP["r_term"][t]; i_rev = revo * INP["r_rev"][t]; ebt = ebit - i_term - i_rev
    tax = max(0, ebt) * INP["tax"][t]; ni = ebt - tax; div = max(0, ni) * INP["payout"][t]
    capex = rev * INP["capex"][t]
    ar1, inv1, ap1 = rev * INP["dso"][t] / 365, cogs * INP["dio"][t] / 365, cogs * INP["dpo"][t] / 365
    dnwc = (ar1 - ar) + (inv1 - inv) - (ap1 - ap)
    cfo = ni + da - dnwc; rep = min(INP["repay"][t], term)
    pre = cash + cfo - capex - rep - div
    draw = max(INP["min_cash"][t] - pre, -revo)
    cash = pre + draw; revo += draw; term -= rep; ppe = ppe + capex - da; eq = eq + ni - div
    ar, inv, ap = ar1, inv1, ap1
    py.append(dict(rev=rev, ebitda=ebitda, ebit=ebit, interest=i_term + i_rev, ebt=ebt, ni=ni, div=div,
                   dnwc=dnwc, cfo=cfo, capex=capex, da=da, fcf=cfo - capex, pre=pre, draw=draw, cash=cash,
                   revolver=revo, term=term, equity=eq, ppe=ppe, ar=ar, inv=inv, ap=ap,
                   check=(cash + ar + inv + ppe) - (ap + term + revo + eq)))
  return py
py = model(INP)

# boardcalc cross-check (its loss carry-forward is irrelevant if EBT > 0 every year)
sys.path.insert(0, "<repo>/executive-board/scripts")
bcres = None
try:
    import boardcalc as bc
    o = INP["open"]
    bcres = bc.three_statement(opening=dict(cash=o["cash"], ar=o["ar"], inventory=o["inv"], ppe=o["ppe"], ap=o["ap"],
                               debt=o["term"], equity=o["eq"], revolver=0), revenue0=INP["rev0"], years=3,
                               growth=INP["growth"], gross_margin=0.38, opex_pct=0.22, da_pct_rev=0.04,
                               capex_pct_rev=INP["capex"], dso=40, dio=55, dpo=35, tax_rate=0.20, interest_rate=0.08,
                               revolver_rate=0.10, cash_interest_rate=0.0, min_cash=1_500_000,
                               debt_repayment=1_000_000, payout_ratio=0.25)
except Exception as e:  # signature mismatch etc. - reported, not fatal
    bcres = f"boardcalc cross-check not run: {e}"

# ---------------- 4. Compare Excel vs Python ----------------
MAP = {"rev": ("IS", 4), "ebitda": ("IS", 8), "ni": ("IS", 15), "div": ("IS", 16), "cfo": ("CF", 9),
       "fcf": ("CF", 23), "cash": ("BS", 4), "revolver": ("BS", 12), "term": ("BS", 11), "equity": ("BS", 14),
       "ppe": ("BS", 7), "draw": ("Debt", 17), "pre": ("Debt", 14), "check": ("BS", 17)}
maxdiff = 0.0
for t, c in enumerate(Y):
    for k, (s, r) in MAP.items():
        maxdiff = max(maxdiff, abs((rc[s][f"{c}{r}"].value or 0) - py[t][k]))
ck = rc["Checks"]
out = dict(xlsx=XLSX, formulas=formulas, errors=errors, max_abs_diff_excel_vs_python=maxdiff,
           all_checks_pass=ck["B12"].value,
           checks={ck[f"A{r}"].value: [ck[f"{c}{r}"].value for c in "BCDE"] for r in range(4, 11)},
           python=[{k: round(v, 2) for k, v in d.items()} for d in py],
           boardcalc=bcres if isinstance(bcres, str) else "ran (see compare)")
if not isinstance(bcres, str):
    bmap = {"rev": "revenue", "ebitda": "ebitda", "ni": "net_income", "cash": "cash", "revolver": "revolver", "equity": "equity"}
    bd = 0.0
    for t in range(3):
        yb = bcres["years"][t]
        for k, kb in bmap.items():
            if kb in yb: bd = max(bd, abs(yb[kb] - py[t][k]))
    out["boardcalc"] = dict(max_abs_diff_vs_python=bd, balanced=bcres["balanced"], warnings=bcres["warnings"])

# ---------------- 5. Scenarios & sensitivity (Python only; ILLUSTRATIVE assumptions A1-A3) ----------------
import copy
def run(**chg):
    d = copy.deepcopy(INP); d.update(chg); p = model(d)
    return dict(peak_revolver=round(max(x["revolver"] for x in p)), y3_revolver=round(p[2]["revolver"]),
                cum_fcf=round(sum(x["fcf"] for x in p)), cum_div=round(sum(x["div"] for x in p)),
                y3_ni=round(p[2]["ni"]), y3_net_debt=round(p[2]["term"] + p[2]["revolver"] - p[2]["cash"]),
                y3_nd_ebitda=round((p[2]["term"] + p[2]["revolver"] - p[2]["cash"]) / p[2]["ebitda"], 2))
out["scenarios"] = {
    "Base": run(),
    "Downside (A1: growth 10/6/3%, GM 35%, DSO 50)": run(growth=[0.10, 0.06, 0.03], gm=[0.35] * 3, dso=[50] * 3),
    "Upside (A2: growth 22/15/10%, GM 39%)": run(growth=[0.22, 0.15, 0.10], gm=[0.39] * 3)}
out["sens_payout"] = {f"{p:.0%}": run(payout=[p] * 3)["peak_revolver"] for p in (0, 0.25, 0.5)}
out["sens_dso"] = {d: run(dso=[d] * 3)["peak_revolver"] for d in (30, 40, 50)}
out["sens_gm"] = {f"{g:.0%}": run(gm=[g] * 3)["peak_revolver"] for g in (0.35, 0.38, 0.41)}
out["sens_capex_y1"] = {f"{c:.0%}": run(capex=[c, 0.07, 0.05])["peak_revolver"] for c in (0.07, 0.09, 0.11)}
out.pop("python_full", None)
print(json.dumps(out, indent=1, default=str))
shutil.rmtree(tmp, ignore_errors=True)
