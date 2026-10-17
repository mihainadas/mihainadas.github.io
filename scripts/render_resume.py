"""Build the two-page, evidence-linked public resume from the website's profile data.

Install requirements-resume.txt before running. The generated PDF and integrity
record are committed, so ordinary Jekyll builds need no PDF toolchain.
"""

import hashlib
import io
import json
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

from fontTools.ttLib import TTFont as SourceFont
from fontTools.varLib.instancer import instantiateVariableFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether

ROOT = Path(__file__).resolve().parents[1]
INPUTS = ("_data/profile.json", "scripts/render_resume.py", "assets/media-sources/manrope.ttf")


def escape(value, entities=None):
    # Keep printable PDF punctuation portable while preserving the source data.
    return xml_escape(value.replace('\u2013', '-').replace('\u2011', '-'), entities or {})


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def absolute(url):
    return "https://mihainadas.github.io" + url if url.startswith("/") else url


def link(label, url):
    return f'<link href="{escape(absolute(url), {chr(34): "&quot;"})}" color="#963824">{escape(label)}</link>'


def main():
    data = json.loads((ROOT / INPUTS[0]).read_text(encoding="utf-8"))
    for name, weight in (("Manrope", 400), ("ManropeBold", 700)):
        font = SourceFont(ROOT / INPUTS[2])
        font = instantiateVariableFont(font, {"wght": weight}, inplace=True)
        # ReportLab deduplicates embedded faces by PostScript name. Give each
        # static instance its own name so bold is not silently mapped to regular.
        for record in font['name'].names:
            if record.nameID == 6:
                record.string = f'ManropePDF{weight}'.encode(record.getEncoding())
        buffer = io.BytesIO()
        font.save(buffer)
        buffer.seek(0)
        pdfmetrics.registerFont(TTFont(name, buffer))
    pdfmetrics.registerFontFamily("Manrope", normal="Manrope", bold="ManropeBold", italic="Manrope", boldItalic="ManropeBold")
    ink, muted, accent = (colors.HexColor(value) for value in ("#171b1c", "#48514f", "#963824"))
    styles = {
        "name": ParagraphStyle("Name", fontName="ManropeBold", fontSize=27, leading=34, textColor=ink, spaceAfter=8),
        "headline": ParagraphStyle("Headline", fontName="ManropeBold", fontSize=12, leading=18, textColor=accent, spaceAfter=12),
        "section": ParagraphStyle("Section", fontName="ManropeBold", fontSize=12, leading=17, textColor=ink, spaceBefore=14, spaceAfter=9, keepWithNext=True),
        "role": ParagraphStyle("Role", fontName="ManropeBold", fontSize=10, leading=15, textColor=ink, spaceAfter=3, keepWithNext=True),
        "body": ParagraphStyle("Body", fontName="Manrope", fontSize=9, leading=13, textColor=ink, spaceAfter=6, alignment=TA_LEFT),
        "small": ParagraphStyle("Small", fontName="Manrope", fontSize=7.5, leading=11.5, textColor=muted, spaceAfter=6),
    }
    story = []

    def add(text, style="body"):
        story.append(Paragraph(text, styles[style]))

    add(escape(data["name"]), "name")
    add(escape(data["headline"]), "headline")
    add(escape(data["summary"]))
    add(escape(data["location"]) + " · " + link("LinkedIn / contact", data["contact_url"]) + " · " + link("Online record", "/resume/"), "small")
    add("SELECTED LEADERSHIP EXPERIENCE", "section")
    for role in data["experience"]:
        items = [Paragraph(escape(role["title"] + " | " + role["organization"]), styles["role"]),
                 Paragraph(escape(role["period"]) + " · " + link("Role source", role["source"]), styles["small"]),
                 Paragraph(escape(role["detail"]), styles["body"])]
        for position in role.get('roles', []):
            items.append(Paragraph(escape(position['title'] + ' | ' + position['period']), styles['small']))
        story.append(KeepTogether(items))
    story.append(PageBreak())
    add("Public work and research", "name")
    add("Research, engineering, and decision support", "headline")
    for item in data["evidence"]:
        add(link(item["label"], item["url"]), "role")
        add(escape(item["detail"]))
    add("SELECTED PUBLICATIONS", "section")
    for paper in data["publications"]:
        story.append(KeepTogether([
            Paragraph(link(paper["title"], paper["url"]), styles["role"]),
            Paragraph(escape(paper["venue"] + " | " + paper["kind"]), styles["small"]),
        ]))
        story.append(Spacer(1, 5))
    add(link("Research context, data, code, and limitations", "/research/"))
    add("EDUCATION AND DEVELOPMENT", "section")
    for education in data["education"]:
        add(escape(education["qualification"]) + ' | ' + escape(education["institution"]), "role")
        add(escape(education['period'] + '. ' + education['status']) + ' · ' + link('Source', education['source']), 'small')
    add(escape(data['development']) + ' · ' + link('Source', data['development_source']), 'small')
    add("PROFESSIONAL CONTEXT", "section")
    add(escape(data["boundary"]), "small")
    add("Public sources reviewed " + escape(data["reviewed"]) + ". Publications also appear under " + escape(data["publishing_name"]) + ".", "small")
    add(" · ".join(link(item["label"], item["url"]) for item in data["identities"]), "small")
    output = ROOT / "assets/downloads/mihai-nadas-resume.pdf"
    output.parent.mkdir(parents=True, exist_ok=True)

    def frame(canvas, document):
        canvas.saveState()
        canvas.setStrokeColor(accent)
        canvas.setLineWidth(1.8)
        canvas.line(44, 805, 551, 805)
        canvas.setDateFormatter(lambda *args: 'D:' + data['reviewed'].replace('-', '') + '000000Z')
        canvas.setFont("Manrope", 7)
        canvas.setFillColor(muted)
        canvas.drawString(44, 28, "Mihai Dan Nadăș | mihainadas.github.io/resume/")
        canvas.drawRightString(551, 28, f"Reviewed {data['reviewed']} | {document.page}")
        canvas.restoreState()

    document = SimpleDocTemplate(str(output), pagesize=A4, rightMargin=44, leftMargin=44,
                                 topMargin=51, bottomMargin=48, title=data["name"] + " - Professional record",
                                 author=data["name"], subject="Selected leadership, research, and public evidence", invariant=1)
    document.build(story, onFirstPage=frame, onLaterPages=frame)
    if document.page != 2:
        raise ValueError('Resume must remain two pages; revise and visually review the layout before publishing.')
    record = {"reviewed": data["reviewed"], "inputs": {name: digest(ROOT / name) for name in INPUTS}, "pdf_sha256": digest(output)}
    (ROOT / "_data/resume_build.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print("Generated " + str(output.relative_to(ROOT)))


if __name__ == "__main__":
    main()
