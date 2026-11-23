---
name: coo-toolkit
description: COO toolkit: capacity/queueing, staffing, Lean Six Sigma, inventory, supply chain, execution KPIs - methods, verified calculator, quality gates.
---

# COO Toolkit (index — read only what you need)

**Calculator:** `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/boardcalc.py" <function> '<json>'`. Run `list` for all functions, or add `--doc` for one. In a manual install, use `~/.claude/executive-board/scripts/boardcalc.py`. References are in `${CLAUDE_PLUGIN_ROOT}/skills/coo-toolkit/references/`.

| Task | Read | boardcalc functions | Optional skills |
|---|---|---|---|
| Capacity, queues, staffing, service levels, ramp-up | `capacity-staffing.md` | `erlang_c`, `staff_for_service_level`, `littles_law`, `capacity`, `takt_time`, `learning_curve` | — |
| Process improvement, Lean, Six Sigma, quality | `process-quality.md` | `oee`, `dpmo_sigma`, `control_limits`, `fmea` | — |
| Inventory, procurement, supply chain, vendors | `supply-chain.md` | `eoq`, `safety_stock` | `small-business:inventory-planner` (if connected) |
| Execution plans, KPIs, operational review of others' assumptions | `execution-kpis.md` | `pert_estimate`, `project` (cost side) | — |

## Quality gates

1. Every operational claim is tagged with a number and a basis: time study, benchmark, vendor quote or estimate.
2. All capacity, queue and inventory arithmetic is done in boardcalc or a saved script. Show utilisation **and** service level, never utilisation alone.
3. Plan at **≤ 80–85% utilisation** for variable work, because queues explode as utilisation approaches 100% (Kingman). Justify anything higher.
4. Model ramp-up and learning curves. Day-1 productivity is not steady state.
5. Identify the bottleneck and the single points of failure (people, suppliers, licences) and give a mitigation for each.
6. Translate every operational change into money and pass it to the CFO: opex, capex, NWC (inventory, payables).
7. Accept, adjust or reject the other executives' operational assumptions explicitly, with the reason for each.
