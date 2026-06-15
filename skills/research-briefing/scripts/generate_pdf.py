#!/usr/bin/env python3
"""
Research Briefing PDF Generator
================================
Bundled script for the research-briefing Cowork skill.

Usage:
    python3 generate_pdf.py --output briefing_20260506.pdf --data papers.json

The JSON data file must have this structure:
{
  "date": "May 06, 2026",
  "section1": [   <- Cardiovascular Research papers
    {
      "title": "Paper Title",
      "journal_info": "Author A, Author B et al.  Journal, Month Year  |  Vol. X",
      "summary": "2-3 sentence summary.",
      "doi": "https://doi.org/10.XXXX/XXXXX"
    }, ...
  ],
  "section2": [   <- Methodology Developments papers
    { ... same fields ... }
  ]
}
"""

import argparse
import json
import sys
from datetime import date

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer,
        HRFlowable, KeepTogether, Table, TableStyle
    )
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
except ImportError:
    print("reportlab not installed. Run: pip install reportlab --break-system-packages")
    sys.exit(1)


# ── Colour palette ────────────────────────────────────────────────────────────
DARK_BLUE   = colors.HexColor("#1a3a5c")
MED_BLUE    = colors.HexColor("#2563a8")
ACCENT      = colors.HexColor("#0e7490")
RULE_COLOR  = colors.HexColor("#93c5fd")
BODY_GRAY   = colors.HexColor("#1f2937")
META_GRAY   = colors.HexColor("#6b7280")


def build_styles():
    styles = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "BriefingTitle", fontName="Helvetica-Bold",
            fontSize=22, leading=28, textColor=DARK_BLUE,
            alignment=TA_CENTER, spaceAfter=4,
        ),
        "subtitle": ParagraphStyle(
            "BriefingSubtitle", fontName="Helvetica",
            fontSize=11, leading=16, textColor=META_GRAY,
            alignment=TA_CENTER, spaceAfter=4,
        ),
        "section_header": ParagraphStyle(
            "SectionHeader", fontName="Helvetica-Bold",
            fontSize=14, leading=18, textColor=colors.white,
            spaceBefore=14, spaceAfter=10,
        ),
        "paper_title": ParagraphStyle(
            "PaperTitle", fontName="Helvetica-Bold",
            fontSize=10.5, leading=14, textColor=DARK_BLUE,
            spaceBefore=2, spaceAfter=2,
        ),
        "meta": ParagraphStyle(
            "PaperMeta", fontName="Helvetica-Oblique",
            fontSize=8.5, leading=12, textColor=ACCENT, spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "PaperBody", fontName="Helvetica",
            fontSize=9.5, leading=14, textColor=BODY_GRAY,
            alignment=TA_JUSTIFY, spaceAfter=4,
        ),
        "doi": ParagraphStyle(
            "DOI", fontName="Helvetica",
            fontSize=8, leading=11, textColor=META_GRAY, spaceAfter=8,
        ),
        "intro": ParagraphStyle(
            "Intro", fontName="Helvetica",
            fontSize=10, leading=15, textColor=BODY_GRAY,
            alignment=TA_JUSTIFY, spaceAfter=6,
        ),
        "footer": ParagraphStyle(
            "Footer", fontName="Helvetica-Oblique",
            fontSize=8, textColor=META_GRAY, leading=12, alignment=TA_CENTER,
        ),
    }


def section_banner(label, style, bg_color):
    tbl = Table([[Paragraph(label, style)]], colWidths=[6.3 * inch])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), bg_color),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return tbl


def paper_entry(paper, styles):
    title   = paper.get("title", "")
    jinfo   = paper.get("journal_info", "")
    summary = paper.get("summary", "")
    doi     = paper.get("doi", "")

    items = [
        Paragraph(title, styles["paper_title"]),
        Paragraph(jinfo, styles["meta"]),
        Paragraph(summary, styles["body"]),
        Paragraph(f"DOI: {doi}", styles["doi"]),
        HRFlowable(width="100%", thickness=0.4, color=RULE_COLOR, spaceAfter=6),
    ]
    return KeepTogether(items)


def build_pdf(data: dict, output_path: str):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=0.85 * inch,
        leftMargin=0.85 * inch,
        topMargin=0.9 * inch,
        bottomMargin=0.9 * inch,
        title="Research Briefing",
        author="Automated Research Monitor",
    )

    styles = build_styles()
    story  = []

    briefing_date = data.get("date", date.today().strftime("%B %d, %Y"))
    s1_papers     = data.get("section1", [])
    s2_papers     = data.get("section2", [])

    # ── Header ────────────────────────────────────────────────────────────────
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("Research Briefing", styles["title"]))
    story.append(Paragraph("Cardiovascular &amp; Computational Biology Literature", styles["subtitle"]))
    story.append(Paragraph(f"Automated digest &bull; {briefing_date}", styles["subtitle"]))
    story.append(Spacer(1, 0.08 * inch))
    story.append(HRFlowable(width="100%", thickness=1.5, color=MED_BLUE, spaceAfter=10))

    # ── Intro ─────────────────────────────────────────────────────────────────
    story.append(Paragraph(
        "This briefing curates recent publications from <i>Circulation</i>, <i>JACC</i>, "
        "<i>JAHA</i>, <i>Nature</i>, <i>Nature Medicine</i>, <i>Nature Cardiovascular Research</i>, "
        "<i>Circulation Research</i>, <i>Cell</i>, <i>Science</i>, and related high-impact journals. "
        "Papers are organized into two thematic sections: <b>Cardiovascular Research</b> — covering "
        "translational, genomic, and multi-omic discoveries — and <b>Methodology Developments</b> — "
        "highlighting computational, single-cell, and AI/ML advances with direct relevance to "
        "computational biology and bioinformatics research in cardiovascular disease. "
        "Based on articles retrieved from PubMed.",
        styles["intro"],
    ))
    story.append(Spacer(1, 0.05 * inch))

    # ── Section I ─────────────────────────────────────────────────────────────
    story.append(section_banner("I.  Cardiovascular Research", styles["section_header"], DARK_BLUE))
    for paper in s1_papers:
        story.append(paper_entry(paper, styles))

    # ── Section II ────────────────────────────────────────────────────────────
    story.append(Spacer(1, 0.05 * inch))
    story.append(section_banner("II.  Methodology Developments", styles["section_header"], ACCENT))
    for paper in s2_papers:
        story.append(paper_entry(paper, styles))

    # ── Footer ────────────────────────────────────────────────────────────────
    story.append(Spacer(1, 0.1 * inch))
    story.append(HRFlowable(width="100%", thickness=1, color=MED_BLUE, spaceAfter=8))
    story.append(Paragraph(
        f"<i>Literature retrieved from PubMed. All DOIs link to original publications. "
        f"Generated automatically via scheduled research monitoring on {briefing_date}. "
        f"Focused on: Circulation, JACC, JAHA, Nature, Nature Medicine, Nat Cardiovasc Res, "
        f"Circ Res, Cell, Science, and related journals. Curated for relevance to cardiovascular "
        f"computational biology and bioinformatics research.</i>",
        styles["footer"],
    ))

    doc.build(story)
    print(f"PDF written to: {output_path}")
    print(f"  Section I  (Cardiovascular Research):   {len(s1_papers)} papers")
    print(f"  Section II (Methodology Developments):  {len(s2_papers)} papers")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Generate research briefing PDF")
    parser.add_argument("--output", required=True, help="Output PDF path")
    parser.add_argument("--data",   required=True, help="Path to papers JSON file")
    args = parser.parse_args()

    with open(args.data) as f:
        data = json.load(f)

    build_pdf(data, args.output)


if __name__ == "__main__":
    main()
