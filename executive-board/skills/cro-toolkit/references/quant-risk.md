# Quantitative risk

- **Reverse stress** (`breakeven_input`): for each critical driver, find the value that makes NPV = 0 or cash < 0. Headroom below about 15% on an unvalidated driver means fragile.
- **Monte Carlo** (`montecarlo`): use the CFO's model inputs with *your own* ranges. Report P(NPV<0), p5 and the expected shortfall. Model correlation where drivers move together.
- **Combined stress** (`stress`): a recession package (volume −30%, price −10%, DSO +30 days, rate +300 bp). Track liquidity (minimum cash, funding gap), not just NPV.
- **Tail metrics** (`var_cvar`): VaR and CVaR of simulated P&L, for portfolios or recurring exposures.
- **Leverage risk** (`covenant_headroom`, `altman_z`): EBITDA decline to breach, and distress zone screening.
- **Liquidity is the killer:** most small-business failures are cash failures. Always compute the peak funding need and the months of runway in the downside case.
