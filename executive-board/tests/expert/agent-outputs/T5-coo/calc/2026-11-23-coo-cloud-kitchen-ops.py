"""COO cloud kitchen ops checks (fictional, CEO-provided illustrative inputs). Re-run: python3 this_file.py"""
import sys, math, json
sys.path.insert(0, "/home/user/Hassanshuaib/executive-board/scripts")
import boardcalc as bc

def show(label, d):
    print(label, json.dumps(bc._clean(d)))

# (a) Packing: M/M/c, units = hours. Target wait 3 min = 0.05 h, SL >= 80%
LAM, MU, T, SL = 180.0, 15.0, 3 / 60, 0.80
print("(a) offered load a = lam/mu =", LAM / MU)
for c in (12, 13, 14, 15):
    show(" c=%d" % c, bc.erlang_c(LAM, MU, c, T))
show(" min c:", bc.staff_for_service_level(LAM, MU, T, SL))

# Independent cross-check of Erlang C (factorial-sum form, not the Erlang-B recursion boardcalc uses)
def ec_direct(lam, mu, c, t):
    a = lam / mu; rho = a / c
    s = sum(a ** k / math.factorial(k) for k in range(c))
    top = a ** c / math.factorial(c) / (1 - rho)
    pw = top / (s + top); wq = pw / (c * mu - lam)
    return {"p_wait": pw, "wq_min": wq * 60, "sl": 1 - pw * math.exp(-(c * mu - lam) * t)}
for c in (13, 14):
    show(" cross-check c=%d" % c, ec_direct(LAM, MU, c, T))

# Sensitivity: +10% peak arrivals, -10% service rate, both
show(" sens lam=198:", bc.staff_for_service_level(198, MU, T, SL))
show(" sens mu=13.5:", bc.staff_for_service_level(LAM, 13.5, T, SL))
show(" sens both:", bc.staff_for_service_level(198, 13.5, T, SL))
show(" 85% util planning rule:", bc.capacity(LAM, MU, 0.85))

# (b) Cups
ss = bc.safety_stock(1200, 300, 5, 0.95, 1)
show("(b) safety stock (z from norm_ppf(0.95)):", ss)
sd_L = math.sqrt(5 * 300 ** 2 + (1200 * 1) ** 2)
print(" sigma_LTD =", sd_L, " SS@z=1.645 =", 1.645 * sd_L, " ROP =", 1200 * 5 + 1.645 * sd_L)
e = bc.eoq(432000, 450, 0.12); show(" EOQ:", e)
q = e["eoq"]
print(" cycle days (360-day yr) =", 360 / e["orders_per_year"],
      " ordering cost =", 432000 / q * 450, " cycle holding =", q / 2 * 0.12,
      " SS holding =", ss["safety_stock"] * 0.12,
      " total incl SS =", e["total_relevant_cost"] + ss["safety_stock"] * 0.12)
print(" avg inventory units (Q/2+SS) =", q / 2 + ss["safety_stock"], " ROP as days of cover =", ss["reorder_point"] / 1200)

# (c) Oven OEE
o = bc.oee(600, 540, 0.5, 950, 900); show("(c)", o)
print(" losses (min of planned 600): availability =", 600 - 540, " performance =", 540 - 0.5 * 950,
      " quality =", 0.5 * (950 - 900), " fully productive =", 0.5 * 900)
print(" check A*P*Q =", (540 / 600) * (475 / 540) * (900 / 950), " = 450/600 =", 450 / 600)
