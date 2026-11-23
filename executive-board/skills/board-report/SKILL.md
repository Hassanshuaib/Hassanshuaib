---
name: board-report
description: Produce real executive deliverables (Word DOCX, PDF, Excel XLSX) from board analyses, minutes and decisions via the Executive Secretary. Use when the CEO asks for an executive report, board pack, minutes document, decision memo, Excel table/model export, or "have the secretary prepare a report" (جهز تقرير، محضر اجتماع، ملف وورد/إكسل/PDF).
---

# Board report

1. Find the sources: the relevant `board/analyses/*`, `board/minutes/*`, `board/decisions/*`, `board/actions.md` and `board/assumptions.md` in the current project. If there are no sources, say so and offer to run the analysis first. Never create a report from invented data.
2. Delegate to the **Secretary** agent (`executive-board:secretary` or `secretary`) with a brief that contains:
   - the absolute project path and the list of source files
   - the formats: DOCX by default, PDF and/or XLSX if asked. XLSX is only meaningful if the report has tables.
   - the audience, language and length
   - the report script path: `${CLAUDE_PLUGIN_ROOT}/scripts/make_report.py`
3. When it returns, verify the files yourself with `ls -la <paths>`, then give the CEO the real absolute paths.
   - If a format was skipped (for example, PDF without LibreOffice), tell the CEO why and what to do instead: open the DOCX and use "Save as PDF".
4. In Claude Code, the CEO can open the files from the file explorer. Tell them which folder: `board/reports/`.
