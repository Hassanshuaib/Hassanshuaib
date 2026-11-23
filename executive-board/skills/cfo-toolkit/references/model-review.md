# Model and analysis review checklist (self-review, or an independent reviewer)

Run it in this order and report findings as **Error** (wrong number), **Inconsistency** (assumptions conflict) or **Judgement** (debatable).

## 1. Mechanics

- **Recompute headline numbers independently** (`boardcalc`, or `recalc_compare` for Excel): NPV/IRR, EV and equity, break-even.
- **Statements:**
  - Balance sheet balances, cash ties out, the RE roll-forward works.
  - There are no hard-codes inside formula rows.
  - Signs are consistent (outflows negative).
  - Units are consistent (thousands versus units, months versus years).
- **Timing:** t=0 versus end of year 1, mid-year convention, and partial first year.
- For Excel files, use `board-finance-pack:audit-xls` if installed.

## 2. Consistency

- Nominal and real figures must not be mixed. The currency of the flows matches the rate. FCFF goes with WACC, FCFE with Re.
- Growth must be consistent with reinvestment (`g ≈ reinvestment × RONIC`). Terminal capex must be at least D&A when growing.
- Tax treatment: losses, NOLs, zakat versus CIT. WACC weights should be market or target, not book.
- Working capital must not be double-counted (for example, NWC in both FCF and the TV).

## 3. Realism

- Growth, margin, CAC, churn and multiple assumptions versus base rates or peers. Name the source, or mark them as unsupported.
- Terminal value share and implied multiple / implied g.
- The ramp-up and the capacity to deliver (ask the COO).

## 4. Robustness

- Is the conclusion still true in the downside case? What is the break-even headroom of the critical driver?
- What does the forecast assume that hasn't been observed yet (demand, price acceptance, permits)?

## 5. Interpretation

- Are there alternative explanations? Does the recommendation follow from the numbers? Is the confidence stated honestly?

## Output

A table of findings (ID, type, location, impact on the conclusion, fix), followed by a **verdict**: conclusion holds / holds with changes / does not hold.
