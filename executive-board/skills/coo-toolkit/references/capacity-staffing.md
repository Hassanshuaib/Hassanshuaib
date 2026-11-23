# Capacity, queueing, staffing

## Core relationships

- **Little's law:** WIP = throughput × lead time (`littles_law`). It holds for any stable system: use it to sanity-check claims.
- **Utilisation** ρ = demand / capacity. Waiting time grows non-linearly with ρ. Kingman's approximation: `Wq ≈ (ρ/(1−ρ)) × ((Ca²+Cs²)/2) × service time`. At ρ = 0.9, the wait is about 9× the service time when variability is moderate.
- **M/M/c (Erlang C):** use `erlang_c` and `staff_for_service_level` for counters, call centres, kitchens with orders and drivers, and clinics. Inputs are the arrival rate per hour, the service rate per server per hour, and the target (for example 80% served within 20 s). Erlang C assumes Poisson arrivals and exponential service. For peaky demand, staff by interval (hourly), not on daily averages.
- **Takt time** = available time / demand (`takt_time`). Each station's cycle time must be ≤ takt, or it is the bottleneck.

## Capacity planning steps

1. Forecast demand by interval, with peaks (for example Ramadan, seasonality, weekday versus weekend).
2. Convert it to workload (units × standard time). Add allowances: breaks, setup, rework, typically 10–20%.
3. Required resources at the target utilisation (`capacity`), and round up. Check the queue and service level for customer-facing work.
4. **Ramp:** apply a learning curve (`learning_curve`, typically 80–90% for manual work) and hiring and training lead times.
5. Identify the constraint (Theory of Constraints): exploit it, subordinate the rest to it, then elevate it.

## Workforce productivity

- Measure output per FTE-hour, with a quality adjustment. Compare against benchmarks, and cite their source.
- Absenteeism, attrition and training time reduce effective capacity. Include them (for example, effective FTE = headcount × 0.85).
- In KSA, plan around Saudisation (Nitaqat) quotas and visa lead times; verify the current rules with the HRSD ministry.
