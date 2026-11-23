# Valuation: DCF, multiples, precedents, terminal value

## DCF (enterprise approach)

1. **FCFF** = EBIT(1−t) + D&A − capex − ΔNWC (`fcff_from`). Forecast it from a driver-based model (revenue, margins, reinvestment), ideally the three-statement model.
2. **Reinvestment consistency:** `g = reinvestment rate × RONIC`. If you assume 8% growth with almost no capex or NWC, the forecast is internally inconsistent; flag it.
3. **Discount** at WACC (`dcf`). Use `mid_year=True` when cash arrives through the year; this raises value by about `(1+WACC)^0.5`.
4. **Terminal value.** Compute both methods and reconcile them:
   - **Gordon:** `TV = FCFF_{N+1}/(WACC−g)`. Long-run g ≤ nominal long-run GDP and inflation, typically 2–4%, and it must be < WACC. The steady-state reinvestment in the terminal year must equal `g/RONIC`.
   - **Exit multiple:** EV/EBITDA × terminal EBITDA. Use a mature-company multiple, not today's growth multiple.
   - Report the **implied exit multiple** from Gordon and the **implied g** from the exit multiple. `dcf` does this when both are given. A large gap means one assumption is wrong.
   - If the **TV share of EV is above 75%**, the valuation is mostly an assumption about the long run. Extend the explicit period, or present it as a range.
5. **EV → equity:** subtract net debt (debt + leases + preferred + minorities − cash, and excess cash only). Adjust for non-operating assets and debt-like items (provisions, end-of-service benefits, unfunded liabilities).
6. **Sensitivity:** a WACC × g grid (`dcf_grid`), and margin × growth via the model. Show the value range.

## Comparable companies (trading multiples)

- **Peer selection:** similar growth, margin, risk, size and business model. Document why each peer is included or excluded. Use 5–10 peers.
- **Multiple choice:** use EV/EBITDA or EV/EBIT for operating value, P/E for equity (consistent capital structures only), and EV/Revenue only for loss-makers (weak). Calendarise to the same fiscal period, and use LTM and NTM consistently.
- **Statistics:** use the median and interquartile range (`multiples_valuation`). Never the mean alone, because outliers distort it.
- **Private-company adjustment:** a discount for lack of marketability, about 15–35%, is a judgement call; show it separately. Adjust for size and the quality of earnings (normalised EBITDA).

## Precedent transactions

- Transaction multiples include a **control premium** (typically about 20–40%) and reflect market conditions at the time. Note the date and the cycle.
- Use them as a range check for M&A pricing, not as a stand-alone valuation. Data are often incomplete; cite the source of each deal.

## Cross-check discipline

- The football-field output shows ranges from the DCF (with sensitivity), comps (IQR) and precedents. Explain any method that sits outside the others.
- **Sanity checks:**
  - implied EV/EBITDA of your DCF versus peers
  - implied perpetual growth
  - ROIC in the terminal year versus WACC (it should fade toward WACC unless there is a durable moat)

## Typical errors to look for

- Discounting FCFE at WACC.
- Double-counting cash.
- Forgetting the NWC build in growth years.
- Terminal-year capex below D&A while still growing.
- Tax rates that ignore NOLs or zakat (in KSA, zakat applies to Saudi/GCC ownership, corporate income tax to foreign ownership; verify with a tax adviser).
- Valuing a loss-maker on a multiple of negative EBITDA.
- A nominal WACC paired with real cash flows.
