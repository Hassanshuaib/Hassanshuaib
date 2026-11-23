---
name: board-council
description: Structured executive board deliberation (council) for major decisions - independent executive analyses, anonymized peer review, explicit disagreements and a chaired final verdict with confidence, risks and next steps. Use when the CEO says "convene the board", "اجمع المجلس", "full strategic review", "challenge this decision", "council this", "pressure-test / stress-test this", or when a large, hard-to-reverse decision needs multiple perspectives.
---

# Board Council — deliberation protocol

This is an adaptation of the LLM Council method (Andrej Karpathy's *llm-council*, packaged as a Claude skill by Ole Lehmann at github.com/aiwithremy/claude-skills-llm-council): independent answers, then anonymised peer review, then a chairman's synthesis. Here the advisors are the board's executives, and the process is tiered to control cost.

**Be honest about independence.** Every executive is the **same model** with a different role, method and set of instructions. The council gives independent *lenses* and fresh contexts, not independent models. Say this in the verdict footer.

You (the Chief of Staff, in the main conversation) run this protocol. Sub-agents can't convene other sub-agents, so never delegate the whole council to one agent.

## Step 0 — Pick the tier and announce it (1 line)

| Tier | When | Agent calls |
|---|---|---|
| **Lite** (default) | "convene the board", "full board", "challenge this decision": most major decisions | 2–4 relevant executives + CRO in parallel → you chair. **3–5 calls** |
| **Standard** | Only when the CEO explicitly asks for peer review or an in-depth review ("deep review", "peer review", "مراجعة معمقة") | Lite + 1 anonymised peer-review round (2 reviewers) → you chair. **5–7 calls** |
| **Deep** | Only on explicit request ("deep council", "أعمق مراجعة") | Standard + a fresh, independent chairman agent, and/or a 5-lens LLM-Council pass (Contrarian, First-Principles, Expansionist, Outsider, Executor) over the board's output. **8–12 calls**. State the cost and ask before starting |

After a Lite verdict, offer Standard in one line if the CEO wants a deeper cross-examination. Choose the executives by relevance: usually 2–3 plus the CRO, not all five. Don't call the CMO for a pure cost-control question. The **CRO is always included** in a council.

## Step 1 — Frame the question (no agent call)

Write one neutral **frame**, under 200 words: the decision, the objective, the options, the key facts with their sources, the user's figures, the constraints, the stakes, and the currency. Don't steer it. Read `board/context.md` and any relevant `board/analyses/*` first, and cite the file paths rather than pasting them. If `board/` exists, save the frame to `board/minutes/<date>-<topic>-frame.md`. If the question is too vague, ask the CEO one clarifying question first.

## Step 2 — Independent analyses (parallel)

In a **single message**, send one Agent call per selected executive. Each gets the frame and the instruction:
"Analyse independently from your discipline. You haven't seen the others' views. Take a clear position. Save your full analysis to board/analyses/ and return your standard ≤ 350-word summary."
Give the CRO the frame only: no other outputs in the Lite tier, to preserve independence.

## Step 3 — Peer review (Standard and Deep only; 1 round maximum by default)

Anonymise the summaries as Response A, B, C… in a random order. Spawn **2 reviewers in parallel**: the CRO, plus the executive whose field is most central to the decision. Each one sees all the anonymised responses and answers in under 200 words:
1. Which response is strongest, and why?
2. Which has the biggest blind spot?
3. Which claims contradict each other, and which side is better supported?
4. What did all of them miss?
Don't run extra rounds unless the CEO asks.

## Step 4 — Chair the verdict (you; or a fresh general-purpose agent in Deep)

Decide on the merits. Don't count votes: a lone dissenter with the better evidence wins. Present the result to the CEO:

```
## قرار المجلس / Board Verdict: <topic>
**Tier:** Lite/Standard/Deep · **Consulted:** <agents actually invoked>
### Where the board agrees
### Where the board disagrees  (each side + why reasonable people differ)
### Contradictions & weak assumptions caught
### Critical risks  (CRITICAL vs WATCH)
### Recommendation  (a clear answer, not "it depends") + conditions / kill criteria
### Confidence: High / Medium / Low — and what evidence would change it
### The one thing to do first
_Same model, independent lenses — not independent models. AI analysis; verify material facts._
```

## Step 5 — Record (if `board/` exists)

- Minutes go to `board/minutes/<date>-<topic>.md`. This can be just the verdict plus links to the analysis files.
- Create a decision record with status **Proposed** (use the `board-memory` skill). Mark it **Approved** only when the CEO confirms.
- Add the action items to `board/actions.md`.
Do this yourself with Write and Edit. Only call the Secretary if the CEO wants a formal report.
