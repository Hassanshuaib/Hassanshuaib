# Expert Upgrade: Test Report (2026-11-23)

**Method:**
- Real headless Claude Code sessions, run as the CEO would: `claude -p --agent executive-board:chief-of-staff`. Each case ran in a fresh project.
- Fully specified fictional cases are in `tests/expert/cases/`.
- Expected answers were computed **independently** (`tests/expert/expected.py`). That script doesn't import boardcalc; it uses numpy polynomial roots for IRR, `statistics.NormalDist`, explicit closed forms and a separately written three-statement loop.
- The evidence is in `tests/expert/transcripts/`: every tool call, file read, calculator call and skill invocation, plus the final answers. The agents' own files are in `tests/expert/agent-outputs/`.

**The calculation engine:** `tests/test_boardcalc.py`, 36 of 36 passing. It is checked against LibreOffice's own NPV, IRR, MIRR and PMT, a live-formula Excel version of the three-statement model (match to 1e-9), closed forms and textbook cases. Two failures during development were errors **in my test expectations**, not in the engine, and were corrected.

## Results

| Case | Agent(s) | Result | Compared with the independent answer |
|---|---|---|---|
| T1 three-statement model (3 years, revolver, Excel with live formulas) | CFO | **PASS** | Revenue, EBITDA, NI, CFO, cash, revolver (1.23/1.70/1.23m), debt and equity all exact. Balance and cash checks are 0. 214 live formulas, recalculated. It also found an unplanted issue: the opening DIO of 46.6 days against the 55-day driver |
| T2 DCF (CAPM with relevered beta, dual terminal value) | CFO | **PASS** | β 1.0645, Ke 11.855%, WACC 10.604%, EV 98.06m/115.82m, per share 7.81/9.58, TV share 72.2%/76.5%, implied 7.20x and 4.44%, and all 9 sensitivity cells exact. The two methods were reconciled through the implied RONIC |
| T3 feasibility with a mutually exclusive alternative and unequal lives | CFO | **PASS** | All A cash flows, NPV 1,806,830 / 124,409, IRR 29.10%/16.17%, MIRR, payback, PI and EAA exact. Correct EAA and replacement-chain reasoning |
| T4 stress test (tornado, reverse stress, combined, Monte Carlo) | CFO | **PASS**, with a note | The Chief of Staff chose start-of-year working-capital timing, which the case didn't specify, and **disclosed** it with the alternative figure. Under that convention the base NPV 1,748,169, break-even price 67.66 and volume 28,489, and the combined case −0.79m are exact. The Monte Carlo mean (1.50m vs 1.49m) and P(NPV<0) (5.1% vs 5.3%) are within simulation error. It flagged that independent draws understate the tail risk |
| T5 operations: queueing, inventory, OEE | COO | **PASS** | It detected that the CEO's 12 stations are unstable (ρ = 1). The 14-station minimum, 85.7% utilisation, P(wait) 48.2%, 0.96-min average wait, 89.3% service level, safety stock 2,261, reorder point 8,261, EOQ about 56.9k and OEE 75.0% are all exact |
| T6 marketing: A/B test, LTV, price change | CMO | **PASS** | p = 0.20 (not significant), power about 25%, n about 38.5k per arm, LTV 934, LTV:CAC 3.0, payback 6.0 months, break-even loss 11.2%, churn 5.07%. It also gave the economically better 5.38% figure (fixed cost per subscriber) |
| T7 strategy: TAM, HHI, option robustness | CSO | **PASS** | TAM 231.55m by segment, SAM and SOM, HHI 1,972 (noting the 2010 versus 2023 band difference), scores and rank robustness all exact. The Chief of Staff challenged the SAR 10 per cup price |
| T8 independent review of a flawed CFO analysis (10 planted errors) | CRO | **PASS, 10 of 10 found** | FCFE/WACC mismatch, 8% terminal growth, NWC, the misstated NPV (recomputed 70.2m), the IRR claim, 45% growth, 0% tax, the NPV formula discounting t0, the SUM omitting Y5, and the hard-coded EBITDA. It also found that the forecast years alone have negative NPV (TV is 101% of value). One judgement is debatable: it rated NWC "minor" |
| R1 concept question | Chief of Staff | **PASS** | No sub-agent; answered in 2 sentences ($0.19) |
| R2 simple VAT arithmetic | Chief of Staff | **PASS** | No sub-agent; computed with code; covered both inclusive and exclusive readings ($0.24) |
| R3 complex purchase decision (Arabic) | CFO | **PASS** | Delegated automatically. It challenged the CEO's implied 120%+ return as suspicious and analysed cash first |
| Re-test: automatic review for a material decision (T3, SAR 2.4m) | CFO → CRO | **PASS** (after the fix) | The CRO ran **automatically** after the CFO, recomputed from inputs before reading the CFO's work, and matched 10 of 10 metrics |
| Re-test: invocation of a vendored third-party skill | CFO | **PASS** | `SKILL board-finance-pack:audit-xls` was invoked. It found all 3 planted spreadsheet errors plus 9 genuine issues, and recalculated the file in LibreOffice |

**Skill access verified for every agent:**
- The toolkit preload was confirmed by a probe: the CFO quoted its toolkit heading and the real path without reading any file.
- Every specialist called `boardcalc` in its tests.
- Reference files read on demand: `three-statement-fsa.md` (T1), `capital-budgeting.md` (T3 re-test), `independent-review.md` and `model-review.md` (CRO).

**Cost:** the 11 main runs cost **$8.31** at API list-price equivalent, about $0.70–1.20 per expert analysis. The automatic CFO plus CRO review cost $1.69.

## Weaknesses found and fixed during testing

1. The independent-review rule was contradictory, so the Chief of Staff only offered the review. **Fixed:** the review is automatic at SAR 250k or more, or for hard-to-reverse decisions, and was re-tested.
2. Agents read the 900-line calculator source, wasting tokens. **Fixed** with a `doc <fn>` command and an explicit instruction not to read the source. Partly effective: one agent still inspected the source through Python.
3. Vendored skills were never chosen spontaneously; agents preferred their own code. **Verified** that the skills work when invoked. Spontaneous use remains low.

## Remaining weaknesses (not fixed)

- **Fully specified cases.** These cases test calculation correctness and judgement on given inputs. They do **not** test real-world estimation from messy or missing data, which is where expert judgement matters most.
- **Convention choices** made by the Chief of Staff (T4) can shift results by about 3%. They are disclosed, but the CEO should confirm conventions for important models.
- **Same model.** The CFO and the CRO are the same model, so a shared blind spot would not be caught. This was not tested.
- **No live data:** no betas, multiples or precedents from data vendors. Every regulatory or tax statement must be confirmed by a professional.
- **Small sample:** 13 runs, one per case. Run-to-run variability was not measured.

**Conclusion:** on these cases the board produced **correct, verified numbers and sound financial reasoning**, and it found planted errors reliably. That is evidence of strong *calculation and review discipline*. It is **not proof of expert-level reliability** on real, ambiguous decisions. Material decisions should still get the automatic CRO review and, where the stakes justify it, a human professional.
