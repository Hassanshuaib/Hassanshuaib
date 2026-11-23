# Independent critical review protocol (material financial decisions)

**Purpose:** a fresh-context second opinion on another executive's analysis, usually the CFO's. You are the reviewer, not the author.

1. **Read the analysis file and its calculation script.** Don't read the author's conclusions first if you can avoid it. Form your own expectation from the inputs.
2. **Recompute independently.** Re-run the headline numbers with boardcalc from the stated inputs, without reusing the author's script. Compare: NPV/IRR, EV and equity, break-even, peak funding. Report each as **Verified**, **Differs** (by how much and why) or **Could not verify** (missing inputs).
3. **Run the model-review checklist** (`cfo-toolkit/references/model-review.md`): mechanics, consistency, realism, robustness, interpretation.
4. **Stress what the author didn't:** at least one reverse stress on the most critical driver, and one combined stress.
5. **Alternative interpretations:** what else could explain the data? What would a sceptical investor or lender say?
6. **Output (≤ 350 words, plus a findings table in the file):**
   - Verdict: conclusion holds / holds with changes / does not hold.
   - Errors, inconsistencies and judgement differences, ranked by impact on the decision.
   - The numbers you verified, and the ones you could not.
   - Conditions under which you would support the decision.

**Note:** reviewer and author are the same underlying model. This review reduces errors from context and anchoring, but it is not a substitute for a human expert or auditor on decisions of major consequence.
