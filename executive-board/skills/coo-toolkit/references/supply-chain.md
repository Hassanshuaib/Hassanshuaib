# Supply chain, inventory, procurement

- **EOQ** (`eoq`): `√(2DS/H)`. The total cost curve is flat near the optimum, so round to practical pack sizes.
- **Safety stock and reorder point** (`safety_stock`): `z·√(L·σd² + d²·σL²)`. The service-level choice drives cost non-linearly: going from 95% to 99% roughly increases the z-factor by 1.41×.
- **ABC/XYZ classification:** tight control for A items (by value) and X items (stable demand); different policies for the rest.
- **Working-capital link:** DIO = inventory / COGS × 365. Every DIO day is worth COGS/365 in cash. Give the CFO the cash effect.
- **Supplier risk:** single source, lead-time variability, quality history, financial health, geopolitical and shipping routes. Mitigate with dual sourcing, buffer stock or contracts (price, volume and SLA clauses, penalties).
- **Procurement:** total cost of ownership (price + logistics + quality + inventory + admin), should-cost models, and competitive tendering. Never compare quotes on unit price alone.
- **Make vs buy:** compare full incremental cost, capacity and control, and the strategic importance (an input to the CSO).
