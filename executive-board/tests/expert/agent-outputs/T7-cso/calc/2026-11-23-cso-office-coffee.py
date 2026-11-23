"""Riyadh office-coffee (FICTIONAL, illustrative). Re-runnable audit script.
Uses boardcalc.py (cso-toolkit) and cross-checks every figure with independent arithmetic."""
import json, subprocess, itertools

CALC = "<repo>/executive-board/scripts/boardcalc.py"
def bc(fn, payload):
    return json.loads(subprocess.run(["python3", CALC, fn, json.dumps(payload)],
                                     capture_output=True, text=True, check=True).stdout)

# (a) Sizing - user inputs
DRINK, CUPS_M, PRICE = 0.60, 16, 10
per_emp = DRINK * CUPS_M * 12 * PRICE          # SAR per employee per year (blended)
segs = [("Small", 9000, 8), ("Medium", 1400, 45), ("Large", 220, 300)]
seg_in = [{"name": n, "units": o * e, "annual_value": per_emp, "offices": o} for n, o, e in segs]
ms = bc("market_sizing", {"segments": seg_in, "serviceable_share": 0.35, "obtainable_share": 0.04})
manual_tam = sum(o * e * DRINK * CUPS_M * 12 * PRICE for _, o, e in segs)
assert abs(ms["tam"] - manual_tam) < 1e-6
print("per employee/yr SAR", per_emp)
for r in ms["segments"]:
    print(f'{r["name"]:6} emp={r["units"]:>6} TAM={r["tam"]:>14,.0f} share={r["tam"]/ms["tam"]:.1%} per-office={r["tam"]/r["offices"]:,.0f}')
print(f'TAM={ms["tam"]:,.0f} SAM={ms["sam"]:,.0f} SOM={ms["som"]:,.0f} cups/yr SOM={ms["som"]/PRICE:,.0f}')

# (b) Concentration
shares = [32, 24, 14, 10, 8] + [1] * 12
assert sum(shares) == 100
h = bc("hhi", {"shares": shares}); manual_h = sum(s * s for s in shares); assert h["hhi"] == manual_h
band2010 = "highly" if manual_h > 2500 else "moderately" if manual_h >= 1500 else "un"
band2023 = "highly" if manual_h > 1800 else "moderately" if manual_h >= 1000 else "un"
print("HHI", h, "| 2010:", band2010 + "concentrated", "| 2023:", band2023 + "concentrated")
print("CR4 =", sum(shares[:4]))
# HHI delta if we acquire one 1% firm and later grow; and if top two merged (illustrative)
print("HHI delta from 1%+1% combination =", 2 * 1 * 1)

# (c) Decision matrix
opts = {"Organic": {"value": 6, "risk": 7, "capital": 8, "speed": 4},
        "Partnership": {"value": 7, "risk": 6, "capital": 7, "speed": 8},
        "Acquire": {"value": 9, "risk": 4, "capital": 3, "speed": 7}}
W = {"value": 0.35, "risk": 0.25, "capital": 0.20, "speed": 0.20}
dm = bc("decision_matrix", {"options": opts, "weights": W, "perturb": 0.2})
print("boardcalc decision_matrix:", json.dumps(dm, indent=None))

def scores(ws, renorm=True):
    t = sum(ws.values()) if renorm else 1.0
    return {o: sum(sc[c] * ws[c] for c in ws) / t for o, sc in opts.items()}
base = scores(W)
for o, v in base.items(): assert abs(v - dm["scores"][o]) < 1e-9
print("base", {k: round(v, 3) for k, v in base.items()})
min_margin = None
for c, d in itertools.product(W, (-0.2, 0.2)):
    w2 = dict(W); w2[c] *= 1 + d
    for renorm in (True, False):
        s = scores(w2, renorm); rk = sorted(s, key=s.get, reverse=True)
        m = s[rk[0]] - s[rk[1]]
        print(f'{c:7} {d:+.0%} renorm={renorm!s:5} ' + " ".join(f"{k}={s[k]:.3f}" for k in rk) + f' margin={m:.3f}')
        if renorm and (min_margin is None or m < min_margin[0]): min_margin = (m, c, d, rk[0], rk[1])
print("smallest renormalised top-2 margin:", min_margin)

# Break-even: how far must one weight move (others renormalised) for a challenger to beat Partnership?
for c in W:
    for ch in ("Organic", "Acquire"):
        for k in [x / 1000 for x in range(0, 5001)]:          # multiplier 0..5x on weight c
            w2 = dict(W); w2[c] = W[c] * k; s = scores(w2)
            if s[ch] > s["Partnership"]:
                print(f'flip: {ch} beats Partnership when {c} weight x{k:.3f} (raw {W[c]*k:.3f}, normalised {w2[c]/sum(w2.values()):.3f})')
                break
