# Provenance and license notice

The skills in `skills/` are copied **unmodified** from Anthropic's
[financial-services-plugins](https://github.com/anthropics/financial-services-plugins), commit `3e32c22` (2026-11-12). They are licensed under the Apache License 2.0 (see `LICENSE`).

| Skill | Original path |
|---|---|
| audit-xls | plugins/vertical-plugins/financial-analysis/skills/audit-xls |
| 3-statement-model | plugins/vertical-plugins/financial-analysis/skills/3-statement-model |
| lbo-model | plugins/vertical-plugins/financial-analysis/skills/lbo-model |
| competitive-analysis | plugins/vertical-plugins/financial-analysis/skills/competitive-analysis |
| returns-analysis | plugins/vertical-plugins/private-equity/skills/returns-analysis |
| dd-checklist | plugins/vertical-plugins/private-equity/skills/dd-checklist |
| merger-model | plugins/vertical-plugins/investment-banking/skills/merger-model |

## Security review (2026-11-23)

- The skills are Markdown only, with one `references/` folder in 3-statement-model and in competitive-analysis.
- No scripts, hooks or MCP servers are included.
- The original `financial-analysis` plugin's `.mcp.json`, which pointed at 12 data-vendor servers, was deliberately **not** copied.
- Some skills mention Excel and PowerPoint add-in (Office JS) environments. In Claude Code they fall back to Python with openpyxl.

**To update:** re-copy the folders from a newer upstream commit, bump `version` in `.claude-plugin/plugin.json`, and update the commit above.
