#!/usr/bin/env python3
"""
build_proposal_word.py
----------------------
Compiles the Markdown proposal into a clean, executive Word document (.docx)
using the custom Word_Document_Template.docx reference document, applying:
  - 100% Garamond typography
  - All black font (RGB 0,0,0) across headings, titles, links, and body
  - 1.15 line spacing throughout
  - 1.0 inch margins all around
  - Zero horizontal line borders
  - Justified body text
  - Proper scaling and centering of figures:
      * Figure 1: 50% text width (3.25 in)
      * Figure 2: 2x2 grid (Panels A-D), borderless, centered
      * Figure 3: 1x2 grid (Panels A & B side by side), borderless, centered
      * Figure notes: 9.0 pt italic Garamond
"""

import os
import sys
import subprocess
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MD_PATH = os.path.join(BASE_DIR, "OS-SI Proposal[10.28.26].md")
DOCX_PATH = os.path.join(BASE_DIR, "OS-SI Proposal[10.28.26].docx")
TEMPLATE_PATH = os.path.join(BASE_DIR, "Word_Document_Template.docx")
TEMP_MD_PATH = os.path.join(BASE_DIR, "temp_for_docx.md")

def build_docx():
    # 1. Read Markdown and filter out markdown-only TOC and horizontal rules
    with open(MD_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    filtered_lines = []
    skip_toc = False

    for line in lines:
        if line.strip().startswith("# OS-SI Proposal"):
            continue
        if "## Table of Contents for Main Proposal" in line:
            skip_toc = True
            continue
        if skip_toc:
            if line.strip().startswith("## 1. Introduction"):
                skip_toc = False
                filtered_lines.append(line)
            continue
        if line.strip() == "---":
            continue
        filtered_lines.append(line)

    with open(TEMP_MD_PATH, "w", encoding="utf-8") as f:
        f.writelines(filtered_lines)

    # 2. Compile via Pandoc using the reference template
    cmd = [
        "pandoc",
        TEMP_MD_PATH,
        "-o", DOCX_PATH,
        f"--reference-doc={TEMPLATE_PATH}",
        f"--resource-path={BASE_DIR}"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("Pandoc Error:", res.stderr, file=sys.stderr)
        return False

    if os.path.exists(TEMP_MD_PATH):
        os.remove(TEMP_MD_PATH)

    # 3. Post-process DOCX styles and layouts
    doc = docx.Document(DOCX_PATH)
    black = RGBColor(0, 0, 0)

    # Margins: 1.0 in
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)

    # Styles enforcement
    for s in doc.styles:
        if hasattr(s, "font") and s.font:
            s.font.name = "Garamond"
            s.font.color.rgb = black
        if hasattr(s, "paragraph_format") and s.paragraph_format:
            s.paragraph_format.line_spacing = 1.15

    # Inline shapes sizing
    if len(doc.inline_shapes) > 0:
        s0 = doc.inline_shapes[0]
        aspect0 = s0.height / s0.width
        s0.width = Inches(3.25)
        s0.height = int(Inches(3.25) * aspect0)

    for i in range(1, len(doc.inline_shapes)):
        s = doc.inline_shapes[i]
        aspect = s.height / s.width
        if s.width > Inches(4.5):
            s.width = Inches(6.20)
            s.height = int(Inches(6.20) * aspect)
        else:
            s.width = Inches(3.10)
            s.height = int(Inches(3.10) * aspect)

    # Tables layout (centered, borderless)
    for table in doc.tables:
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        for row in table.rows:
            for cell in row.cells:
                tcPr = cell._tc.get_or_add_tcPr()
                tcBorders = parse_xml(r"""
                    <w:tcBorders xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
                        <w:top w:val="none"/>
                        <w:left w:val="none"/>
                        <w:bottom w:val="none"/>
                        <w:right w:val="none"/>
                    </w:tcBorders>
                """)
                tcPr.append(tcBorders)
                for p in cell.paragraphs:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    p.paragraph_format.line_spacing = 1.15
                    for run in p.runs:
                        run.font.name = "Garamond"
                        run.font.color.rgb = black

    # Paragraphs formatting
    for i, p in enumerate(doc.paragraphs):
        # Remove any paragraph borders (horizontal lines)
        pPr = p._p.get_or_add_pPr()
        pBdr = pPr.find("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pBdr")
        if pBdr is not None:
            pPr.remove(pBdr)

        p.paragraph_format.line_spacing = 1.15

        for run in p.runs:
            run.font.name = "Garamond"
            run.font.color.rgb = black

        p_text = p.text.strip()

        # Title block
        if i == 0 and "Overcoming Data Bottlenecks" in p_text:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(16)
            p.paragraph_format.space_after = Pt(8)
            for r in p.runs:
                r.font.size = Pt(16)
                r.font.bold = True
        elif i in [1, 2, 3, 4, 5] and any(k in p_text for k in ["Authors:", "University of Southern", "Proposal for Special Issue", "CFP / URL", "Repository:"]):
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(3)
            for r in p.runs:
                r.font.size = Pt(11)

        # Headings
        elif p.style.name.startswith("Heading 1"):
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(4)
            for r in p.runs:
                r.font.size = Pt(15)
                r.font.bold = True
        elif p.style.name.startswith("Heading 2"):
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(3)
            for r in p.runs:
                r.font.size = Pt(13.5)
                r.font.bold = True
        elif p.style.name.startswith("Heading 3"):
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(2)
            for r in p.runs:
                r.font.size = Pt(12.5)
                r.font.bold = True
        elif p.style.name.startswith("Heading 4"):
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(2)
            for r in p.runs:
                r.font.size = Pt(12)
                r.font.bold = True
                r.font.italic = True

        # Figures & Captions
        elif "graphic" in p._p.xml:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(4)
        elif any(p_text.startswith(f"Figure {num}.") for num in range(1, 10)):
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(4)
            for r in p.runs:
                r.font.size = Pt(11.5)
                r.font.bold = True
        elif p_text.startswith("Application of the LLM-powered topic extraction"):
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(6)
            for r in p.runs:
                r.font.size = Pt(10)
                r.font.italic = True
        elif p_text.startswith("Notes:") or p_text.startswith("*Notes:"):
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(14)
            for r in p.runs:
                r.font.size = Pt(9.0)
                r.font.italic = True
        else:
            if p.alignment != WD_ALIGN_PARAGRAPH.CENTER:
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(4)

    doc.save(DOCX_PATH)
    print("Build complete: OS-SI Proposal[10.28.26].docx updated successfully.")
    return True

if __name__ == "__main__":
    build_docx()
