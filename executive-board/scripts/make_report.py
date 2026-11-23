#!/usr/bin/env python3
"""Executive Board report generator.

Turns a Markdown file into management-ready deliverables:
  * DOCX  (python-docx; Arabic paragraphs are set right-to-left)
  * PDF   (converted from the DOCX with LibreOffice if available,
           otherwise a basic reportlab rendering for non-Arabic text)
  * XLSX  (openpyxl; every Markdown table becomes a worksheet,
           numeric cells are stored as numbers)

Usage:
  python3 make_report.py --input board/reports/draft.md --out-dir board/reports \
      --name 2026-11-23-investment-report --formats docx,pdf,xlsx [--title "..."]

It prints a JSON summary listing ONLY files that really exist on disk,
plus any formats that were skipped and why. Exit code 1 if nothing was produced.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date

ARABIC = re.compile(r"[؀-ۿݐ-ݿﭐ-﷿ﹰ-﻿]")


def has_arabic(text):
    return bool(ARABIC.search(text or ""))


# ---------------------------------------------------------------- parsing
def parse_markdown(md):
    """Very small Markdown block parser -> list of (kind, payload)."""
    blocks, para = [], []
    lines = md.splitlines()
    i = 0

    def flush():
        if para:
            blocks.append(("p", " ".join(s.strip() for s in para)))
            para.clear()

    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if not s:
            flush(); i += 1; continue
        m = re.match(r"^(#{1,6})\s+(.*)$", s)
        if m:
            flush(); blocks.append(("h%d" % len(m.group(1)), m.group(2).strip())); i += 1; continue
        if re.match(r"^(-{3,}|\*{3,}|_{3,})$", s):
            flush(); blocks.append(("hr", "")); i += 1; continue
        if s.startswith("|"):
            flush()
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                r = lines[i].strip().strip("|")
                cells = [c.strip() for c in r.split("|")]
                if not all(re.match(r"^:?-{2,}:?$", c) for c in cells if c):
                    rows.append(cells)
                i += 1
            if rows:
                blocks.append(("table", rows))
            continue
        m = re.match(r"^[-*+]\s+(.*)$", s)
        if m:
            flush(); blocks.append(("ul", m.group(1))); i += 1; continue
        m = re.match(r"^\d+[.)]\s+(.*)$", s)
        if m:
            flush(); blocks.append(("ol", m.group(1))); i += 1; continue
        if s.startswith(">"):
            flush(); blocks.append(("quote", s.lstrip("> ").strip())); i += 1; continue
        if s.startswith("```"):
            flush(); i += 1; code = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code.append(lines[i]); i += 1
            i += 1
            blocks.append(("code", "\n".join(code))); continue
        para.append(s); i += 1
    flush()
    return blocks


def inline_runs(text):
    """Split **bold** and *italic* / `code` into (text, bold, italic)."""
    out = []
    for part in re.split(r"(\*\*[^*]+\*\*|`[^`]+`|\*[^*]+\*)", text):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            out.append((part[2:-2], True, False))
        elif part.startswith("`") and part.endswith("`"):
            out.append((part[1:-1], False, False))
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            out.append((part[1:-1], False, True))
        else:
            out.append((part, False, False))
    return out


def strip_inline(text):
    return "".join(t for t, _, _ in inline_runs(text))


# ---------------------------------------------------------------- DOCX
def build_docx(blocks, title, path):
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Pt, RGBColor

    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Arial"
    st.font.size = Pt(11)
    rpr = st.element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts"); rpr.append(rfonts)
    for k in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(k), "Arial")

    def set_rtl(par):
        ppr = par._p.get_or_add_pPr()
        b = OxmlElement("w:bidi"); b.set(qn("w:val"), "1"); ppr.append(b)
        par.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    def add_runs(par, text):
        rtl = has_arabic(text)
        for t, bold, ital in inline_runs(text):
            r = par.add_run(t)
            r.bold, r.italic = bold, ital
            if rtl:
                rp = r._r.get_or_add_rPr()
                e = OxmlElement("w:rtl"); e.set(qn("w:val"), "1"); rp.append(e)
                if bold:
                    cb = OxmlElement("w:bCs"); rp.append(cb)
        if rtl:
            set_rtl(par)
        return par

    if title:
        h = doc.add_heading(level=0)
        add_runs(h, title)
    meta = doc.add_paragraph()
    mr = meta.add_run("Generated %s — AI Executive Board (AI-assisted; verify before external use)" % date.today().isoformat())
    mr.italic = True; mr.font.size = Pt(8); mr.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

    ol_n = 0
    for kind, payload in blocks:
        if kind != "ol" and kind != "ul":
            ol_n = 0
        if kind.startswith("h"):
            lvl = min(int(kind[1:]), 4)
            if title and lvl == 1 and strip_inline(payload) == strip_inline(title):
                continue
            add_runs(doc.add_heading(level=lvl), payload)
        elif kind == "p":
            add_runs(doc.add_paragraph(), payload)
        elif kind in ("ul", "ol"):
            if kind == "ol":
                ol_n += 1
            else:
                ol_n = 0
            if has_arabic(payload):
                # Word/LibreOffice list numbering is placed on the left for RTL text;
                # use an inline marker so the bullet sits on the right.
                marker = ("%d. " % ol_n) if kind == "ol" else "• "
                p = doc.add_paragraph()
                p.paragraph_format.right_indent = Pt(12)
                add_runs(p, marker + payload)
            else:
                add_runs(doc.add_paragraph(style="List Bullet" if kind == "ul" else "List Number"), payload)
        elif kind == "quote":
            p = doc.add_paragraph(style="Intense Quote"); add_runs(p, payload)
        elif kind == "code":
            p = doc.add_paragraph(); r = p.add_run(payload); r.font.name = "Courier New"; r.font.size = Pt(9)
        elif kind == "hr":
            doc.add_paragraph("―" * 30)
        elif kind == "table":
            rows = payload
            ncol = max(len(r) for r in rows)
            t = doc.add_table(rows=len(rows), cols=ncol)
            t.style = "Light Grid Accent 1"
            if any(has_arabic(c) for r in rows for c in r):
                tblpr = t._tbl.tblPr
                b = OxmlElement("w:bidiVisual"); tblpr.append(b)
            for ri, r in enumerate(rows):
                for ci in range(ncol):
                    cell = t.cell(ri, ci)
                    cell.text = ""
                    par = cell.paragraphs[0]
                    add_runs(par, r[ci] if ci < len(r) else "")
                    if ri == 0:
                        for run in par.runs:
                            run.bold = True
            doc.add_paragraph()
    doc.save(path)


# ---------------------------------------------------------------- PDF
def build_pdf(docx_path, blocks, title, path):
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if soffice and docx_path and os.path.exists(docx_path):
        outdir = tempfile.mkdtemp()
        try:
            subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", outdir, docx_path],
                           check=True, capture_output=True, timeout=180)
            produced = os.path.join(outdir, os.path.splitext(os.path.basename(docx_path))[0] + ".pdf")
            if os.path.exists(produced):
                shutil.move(produced, path)
                return "libreoffice"
        except Exception as e:  # fall through to reportlab
            sys.stderr.write("LibreOffice conversion failed: %s\n" % e)
        finally:
            shutil.rmtree(outdir, ignore_errors=True)
    alltext = (title or "") + " ".join(str(p) for _, p in blocks)
    if has_arabic(alltext):
        raise RuntimeError("PDF skipped: Arabic text needs LibreOffice (not found). Open the DOCX and 'Save as PDF' instead.")
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    from reportlab.lib import colors
    from xml.sax.saxutils import escape
    ss = getSampleStyleSheet()
    story = []
    if title:
        story.append(Paragraph(escape(title), ss["Title"]))
    for kind, payload in blocks:
        if kind.startswith("h"):
            story.append(Paragraph(escape(strip_inline(payload)), ss["Heading%d" % min(int(kind[1:]) + 0, 4)]))
        elif kind in ("p", "quote", "code"):
            story.append(Paragraph(escape(strip_inline(payload)), ss["BodyText"]))
        elif kind in ("ul", "ol"):
            story.append(Paragraph("• " + escape(strip_inline(payload)), ss["BodyText"]))
        elif kind == "table":
            data = [[strip_inline(c) for c in r] for r in payload]
            t = Table(data, repeatRows=1)
            t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                                   ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey)]))
            story.append(t); story.append(Spacer(1, 8))
    SimpleDocTemplate(path, pagesize=A4).build(story)
    return "reportlab"


# ---------------------------------------------------------------- XLSX
NUM = re.compile(r"^\(?-?[\d,]*\.?\d+\)?%?$")


def to_number(v):
    s = strip_inline(v).replace("SAR", "").replace("USD", "").replace("ر.س", "").strip()
    if not s or not NUM.match(s):
        return v
    neg = s.startswith("(") and s.endswith(")")
    s = s.strip("()")
    pct = s.endswith("%")
    s = s.rstrip("%").replace(",", "")
    try:
        n = float(s)
    except ValueError:
        return v
    n = -n if neg else n
    if pct:
        return n / 100.0
    return int(n) if n.is_integer() else n


def build_xlsx(blocks, title, path):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter
    tables, heading = [], title or "Table"
    for kind, payload in blocks:
        if kind.startswith("h"):
            heading = strip_inline(payload)
        if kind == "table":
            tables.append((heading, payload))
    if not tables:
        raise RuntimeError("XLSX skipped: the report contains no Markdown tables.")
    wb = Workbook()
    wb.remove(wb.active)
    used = set()
    for idx, (name, rows) in enumerate(tables, 1):
        sheet = re.sub(r"[\[\]:*?/\\]", "", name)[:28] or "Table"
        base, n = sheet, 2
        while sheet in used:
            sheet = ("%s %d" % (base[:25], n)); n += 1
        used.add(sheet)
        ws = wb.create_sheet(sheet)
        rtl = any(has_arabic(c) for r in rows for c in r)
        if rtl:
            ws.sheet_view.rightToLeft = True
        for ri, r in enumerate(rows, 1):
            for ci, v in enumerate(r, 1):
                val = strip_inline(v) if ri == 1 else to_number(v)
                if isinstance(val, str):
                    val = strip_inline(val)
                c = ws.cell(row=ri, column=ci, value=val)
                if isinstance(val, float) and "%" in v:
                    c.number_format = "0.0%"
                elif isinstance(val, (int, float)):
                    c.number_format = "#,##0.##"
                if ri == 1:
                    c.font = Font(bold=True, color="FFFFFF")
                    c.fill = PatternFill("solid", fgColor="1F4E79")
                    c.alignment = Alignment(wrap_text=True)
        for ci in range(1, max(len(r) for r in rows) + 1):
            width = max(len(str(ws.cell(row=ri, column=ci).value or "")) for ri in range(1, len(rows) + 1))
            ws.column_dimensions[get_column_letter(ci)].width = min(max(10, width + 2), 60)
        ws.freeze_panes = "A2"
    wb.save(path)


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", required=True, help="Markdown source file")
    ap.add_argument("--out-dir", default="board/reports")
    ap.add_argument("--name", default=None, help="Base file name without extension")
    ap.add_argument("--formats", default="docx", help="Comma list of docx,pdf,xlsx")
    ap.add_argument("--title", default=None)
    a = ap.parse_args()

    with open(a.input, encoding="utf-8") as f:
        md = f.read()
    blocks = parse_markdown(md)
    title = a.title
    if not title:
        for k, p in blocks:
            if k == "h1":
                title = strip_inline(p); break
    name = a.name or (date.today().isoformat() + "-report")
    os.makedirs(a.out_dir, exist_ok=True)
    fmts = [x.strip().lower() for x in a.formats.split(",") if x.strip()]
    created, skipped = [], {}
    docx_path = os.path.join(a.out_dir, name + ".docx")

    if "docx" in fmts or "pdf" in fmts:
        try:
            build_docx(blocks, title, docx_path)
        except ImportError:
            skipped["docx"] = "python-docx not installed (pip install python-docx)"
            docx_path = None
    if "pdf" in fmts:
        pdf_path = os.path.join(a.out_dir, name + ".pdf")
        try:
            engine = build_pdf(docx_path, blocks, title, pdf_path)
            sys.stderr.write("PDF engine: %s\n" % engine)
        except Exception as e:
            skipped["pdf"] = str(e)
    if "xlsx" in fmts:
        try:
            build_xlsx(blocks, title, os.path.join(a.out_dir, name + ".xlsx"))
        except ImportError:
            skipped["xlsx"] = "openpyxl not installed (pip install openpyxl)"
        except Exception as e:
            skipped["xlsx"] = str(e)
    if "docx" not in fmts and docx_path and os.path.exists(docx_path):
        os.remove(docx_path)  # DOCX was only an intermediate for PDF

    for ext in ("docx", "pdf", "xlsx"):
        p = os.path.join(a.out_dir, name + "." + ext)
        if ext in fmts and os.path.exists(p) and os.path.getsize(p) > 0:
            created.append({"path": os.path.abspath(p), "bytes": os.path.getsize(p)})
    print(json.dumps({"created": created, "skipped": skipped}, ensure_ascii=False, indent=2))
    sys.exit(0 if created else 1)


if __name__ == "__main__":
    main()
