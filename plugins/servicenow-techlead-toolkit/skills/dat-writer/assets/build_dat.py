# /// script
# dependencies = ["python-docx", "pillow"]
# ///
"""Markdown -> ELO-branded DAT (.docx) using ELO-DAT-Template.docx.

uv run build_dat.py dat.md out.docx --title "Portail RH" --client "ACME" --version 0.2 \
    --status Brouillon --author Maori [--date 2026-10-23] [--changes "Retours client"] \
    [--previous "0.1;2026-10-01;Maori;Relu;Première version"]...

Markdown subset: # ## ### headings (#### = bold paragraph), paragraphs, - bullets (indent 2
spaces = level 2), 1. lists, | tables | (escape a pipe as \\|), > callouts (consecutive lines
merge), ![caption](image.png), ```mermaid Figure N – caption``` diagrams (rendered to
figures/fig-N.png with the local Chrome), other ``` blocks as code, **bold** *italic* `code`
[text](url). Image paths resolve relative to the markdown file. A missing image or a diagram
that fails to render becomes a "Figure à insérer" callout and a warning, never a silent gap."""
import argparse
import html
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor
from PIL import Image, ImageChops

HERE = Path(__file__).parent
TEMPLATE = HERE / "ELO-DAT-Template.docx"
NAVY, PALE, TEXT = "003C7D", "EEF5FC", "1A2433"
BODY_MARKER = "{{BODY}}"
INLINE = re.compile(r"(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`|\[[^\]]+\]\([^)]+\))")
LINK = re.compile(r"^\[([^\]]+)\]\(([^)]+)\)$")
HEADING = re.compile(r"^(#{1,4})\s+(.*)$")
IMAGE = re.compile(r"^!\[(.*?)\]\((.*?)\)$")
NUMBERED = re.compile(r"^(\s*)(\d+)[.)]\s+(.*)$")
BULLET = re.compile(r"^(\s*)[-*]\s+(.*)$")
FENCE = re.compile(r"^```\s*(\w*)\s*(.*)$")
MAX_IMAGE_WIDTH = Cm(16.5)
CHROME = os.environ.get("CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
RENDER_SCALE = 2  # device pixels per CSS pixel; 96 CSS px = 1 inch
# One theme for every figure (ELO charter); diagrams carry no style of their own.
MERMAID_HTML = """<!doctype html><html><body style="margin:0;background:#fff">
<pre class="mermaid">%s</pre>
<script type="module">
import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
const NAVY="#003C7D", BLUE="#0068B3", PALE="#EEF5FC", GREY="#5E6B7F", TEXT="#1A2433",
      LINE="#C9D6E6", ZONE="#F7FAFD", WHITE="#FFFFFF";  // BLUE kept for the charter record
mermaid.initialize({
  startOnLoad: false, theme: "base",
  themeVariables: {
    fontFamily: "Century Gothic, Avenir, Helvetica, sans-serif", fontSize: "14px",
    primaryColor: PALE, primaryBorderColor: NAVY, primaryTextColor: TEXT,
    secondaryColor: WHITE, secondaryBorderColor: GREY, tertiaryColor: ZONE,
    lineColor: NAVY, textColor: TEXT,
    clusterBkg: ZONE, clusterBorder: LINE, edgeLabelBackground: WHITE,
    actorBkg: PALE, actorBorder: NAVY, actorTextColor: TEXT, signalColor: NAVY, signalTextColor: TEXT,
    noteBkgColor: "#FFF8E6", noteBorderColor: GREY,
    activationBkgColor: WHITE, activationBorderColor: BLUE,
    labelBoxBkgColor: WHITE, labelBoxBorderColor: GREY, altBackground: ZONE,
    attributeBackgroundColorOdd: WHITE, attributeBackgroundColorEven: PALE
  }
});
try { await mermaid.run(); } catch (e) { document.body.innerHTML = ""; }
</script></body></html>"""


def warn(message):
    print(f"WARNING: {message}", file=sys.stderr)


def add_inline(paragraph, text):
    for part in INLINE.split(text):
        if not part:
            continue
        if part.startswith("**"):
            paragraph.add_run(part[2:-2]).bold = True
        elif part.startswith("`"):
            paragraph.add_run(part[1:-1], style="Code Inline")
        elif part.startswith("*"):
            paragraph.add_run(part[1:-1]).italic = True
        elif m := LINK.match(part):
            paragraph.add_run(m.group(1))
            paragraph.add_run(f" ({m.group(2)})").font.color.rgb = RGBColor.from_string("5E6B7F")
        else:
            paragraph.add_run(part)


def render_mermaid(source, out_png):
    """Mermaid source -> trimmed PNG via the local Chrome. Returns False when nothing rendered."""
    page = out_png.with_suffix(".html")
    page.write_text(MERMAID_HTML % html.escape(source), encoding="utf-8")
    try:
        subprocess.run(
            [CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
             f"--force-device-scale-factor={RENDER_SCALE}", "--virtual-time-budget=15000",
             f"--screenshot={out_png}", "--window-size=1800,1400", page.as_uri()],
            check=True, capture_output=True, timeout=90)
    except (OSError, subprocess.SubprocessError) as error:
        warn(f"Chrome rendering failed: {error}")
        return False
    finally:
        page.unlink(missing_ok=True)
    image = Image.open(out_png).convert("RGB")
    box = ImageChops.difference(image, Image.new("RGB", image.size, "white")).getbbox()
    if box is None:  # blank page: Mermaid syntax error or network down
        out_png.unlink(missing_ok=True)
        return False
    pad = 8 * RENDER_SCALE
    image.crop((max(box[0] - pad, 0), max(box[1] - pad, 0),
                min(box[2] + pad, image.width), min(box[3] + pad, image.height))).save(out_png)
    return True


def cell_shade(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), fill)
    tcPr.append(shd)


def style_table(table, header_cells=True):
    table.style = "Table Grid"
    tblPr = table._tbl.tblPr
    width = tblPr.find(qn("w:tblW"))
    if width is None:
        width = OxmlElement("w:tblW")
        tblPr.append(width)
    width.set(qn("w:type"), "pct")
    width.set(qn("w:w"), "5000")
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        for k, v in (("val", "single"), ("sz", "4"), ("color", "C9D6E6")):
            el.set(qn(f"w:{k}"), v)
        borders.append(el)
    tblPr.append(borders)
    for r, row in enumerate(table.rows):
        for cell in row.cells:
            if r == 0 and header_cells:
                cell_shade(cell, NAVY)
            elif r % 2 == 0:
                cell_shade(cell, PALE)
            for p in cell.paragraphs:
                p.paragraph_format.space_after = Pt(2)
                for run in p.runs:
                    run.font.size = Pt(9)
                    if r == 0 and header_cells:
                        run.font.bold = True
                        run.font.color.rgb = RGBColor.from_string("FFFFFF")
    header = table.rows[0]._tr.get_or_add_trPr()
    flag = OxmlElement("w:tblHeader")
    header.append(flag)


def parse_row(line):
    cells = re.split(r"(?<!\\)\|", line.strip().strip("|"))
    return [c.strip().replace("\\|", "|") for c in cells]


class Writer:
    def __init__(self, doc, anchor, base_dir):
        self.doc, self.anchor, self.base_dir = doc, anchor, base_dir
        self.figure_count = 0

    def _place(self, element):
        self.anchor.addprevious(element)

    def paragraph(self, text="", style=None):
        p = self.doc.add_paragraph(style=style)
        add_inline(p, text)
        self._place(p._p)
        return p

    def heading(self, level, text):
        if level <= 3:
            return self.paragraph(text, style=f"Heading {level}")
        p = self.doc.add_paragraph()
        p.add_run(text).bold = True
        p.paragraph_format.keep_with_next = True
        self._place(p._p)

    def code_block(self, lines):
        for line in lines:
            p = self.doc.add_paragraph()
            p.add_run(line or " ", style="Code Inline")
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.left_indent = Cm(0.4)
            self._place(p._p)
        self.paragraph("")

    def missing_figure(self, caption, detail):
        warn(f"figure not inserted: {caption or detail}")
        self.callout(f"**Figure à insérer** : {caption or detail}")

    def diagram(self, caption, source):
        self.figure_count += 1
        out = self.base_dir / "figures" / f"fig-{self.figure_count}.png"
        out.parent.mkdir(exist_ok=True)
        if render_mermaid(source, out):
            self.image(caption, out, scale=RENDER_SCALE)
        else:
            self.missing_figure(caption, "diagramme Mermaid non rendu")
            self.code_block(source.splitlines())

    def table(self, rows):
        header, body = rows[0], rows[1:]
        table = self.doc.add_table(rows=1 + len(body), cols=len(header))
        for cell, text in zip(table.rows[0].cells, header):
            add_inline(cell.paragraphs[0], text)
        for r, row in enumerate(body, start=1):
            for cell, text in zip(table.rows[r].cells, row + [""] * (len(header) - len(row))):
                add_inline(cell.paragraphs[0], text)
        style_table(table)
        self._place(table._tbl)
        self.paragraph("")

    def image(self, caption, path, scale=1):
        file = (self.base_dir / path).resolve()
        if not file.is_file():
            self.missing_figure(caption, f"image introuvable {path}")
            return
        with Image.open(file) as img:
            natural_width = Cm(img.width / (scale * 96) * 2.54)
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(str(file), width=min(natural_width, MAX_IMAGE_WIDTH))
        self._place(p._p)
        if caption:
            self.paragraph(caption, style="Caption")

    def list_item(self, level, marker, text):
        style = "List Bullet" if marker is None else "Normal"
        p = self.doc.add_paragraph(style=style)
        if marker is not None:
            p.paragraph_format.left_indent = Cm(0.9 + 0.6 * (level - 1))
            p.paragraph_format.first_line_indent = Cm(-0.6)
            p.add_run(f"{marker}.\t")
        elif level > 1:
            p.style = self.doc.styles["List Bullet 2"]
        add_inline(p, text)
        self._place(p._p)

    def callout(self, text):
        p = self.paragraph(text, style="Callout")
        pPr = p._p.get_or_add_pPr()
        borders = OxmlElement("w:pBdr")  # schema order: pBdr before shd
        left = OxmlElement("w:left")
        for k, v in (("val", "single"), ("sz", "18"), ("space", "8"), ("color", NAVY)):
            left.set(qn(f"w:{k}"), v)
        borders.append(left)
        pPr.append(borders)
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear")
        shd.set(qn("w:fill"), PALE)
        pPr.append(shd)


def render(markdown, writer):
    lines, i = markdown.splitlines(), 0
    paragraph_buf = []

    def flush():
        if paragraph_buf:
            writer.paragraph(" ".join(paragraph_buf))
            paragraph_buf.clear()

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped or stripped == "---":
            flush()
        elif m := HEADING.match(stripped):
            flush()
            writer.heading(len(m.group(1)), m.group(2))
        elif m := IMAGE.match(stripped):
            flush()
            writer.image(m.group(1), m.group(2))
        elif m := FENCE.match(stripped):
            flush()
            language, caption = m.group(1).lower(), m.group(2).strip()
            block, i = [], i + 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                block.append(lines[i])
                i += 1
            if language == "mermaid":
                writer.diagram(caption, "\n".join(block))
            else:
                writer.code_block(block)
        elif stripped.startswith("|"):
            flush()
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                row = parse_row(lines[i])
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in row):
                    rows.append(row)
                i += 1
            writer.table(rows)
            continue
        elif stripped.startswith(">"):
            flush()
            quote = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip().lstrip("> ").strip())
                i += 1
            writer.callout(" ".join(q for q in quote if q))
            continue
        elif m := NUMBERED.match(line):
            flush()
            writer.list_item(1 + len(m.group(1)) // 2, m.group(2), m.group(3))
        elif m := BULLET.match(line):
            flush()
            writer.list_item(1 + len(m.group(1)) // 2, None, m.group(2))
        else:
            paragraph_buf.append(stripped)
        i += 1
    flush()


def replace_placeholders(doc, values):
    def in_paragraphs(paragraphs):
        for p in paragraphs:
            for run in p.runs:
                for key, val in values.items():
                    if key in run.text:
                        run.text = run.text.replace(key, val)

    def in_tables(tables):
        for t in tables:
            for row in t.rows:
                for cell in row.cells:
                    in_paragraphs(cell.paragraphs)

    in_paragraphs(doc.paragraphs)
    in_tables(doc.tables)
    for section in doc.sections:
        for part in (section.header, section.footer, section.first_page_header, section.first_page_footer):
            in_paragraphs(part.paragraphs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("markdown", type=Path)
    ap.add_argument("output", type=Path)
    ap.add_argument("--title", required=True)
    ap.add_argument("--client", required=True)
    ap.add_argument("--version", default="0.1")
    ap.add_argument("--status", default="Brouillon")
    ap.add_argument("--author", default="Maori")
    ap.add_argument("--date", default=date.today().isoformat())
    ap.add_argument("--changes", default="Première version")
    ap.add_argument("--previous", action="append", default=[], metavar="V;DATE;AUTEUR;STATUT;MODIFS",
                    help="earlier version rows for the document-control table, oldest first")
    args = ap.parse_args()

    doc = Document(str(TEMPLATE))
    anchor = next((p for p in doc.paragraphs if p.text == BODY_MARKER), None)
    if anchor is None:
        sys.exit(f"{BODY_MARKER} not found in template")
    render(args.markdown.read_text(encoding="utf-8"),
           Writer(doc, anchor._p, args.markdown.resolve().parent))
    anchor._p.getparent().remove(anchor._p)
    replace_placeholders(doc, {
        "{{TITLE}}": args.title, "{{CLIENT}}": args.client, "{{VERSION}}": args.version,
        "{{STATUS}}": args.status, "{{AUTHOR}}": args.author, "{{DATE}}": args.date,
        "{{CHANGES}}": args.changes,
    })
    add_previous_versions(doc.tables[0], args.previous)
    style_table(doc.tables[0])
    doc.save(args.output)
    print(args.output)


def add_previous_versions(table, previous):
    """Earlier versions go above the current row, which stays last."""
    current = table.rows[-1]._tr
    for spec in previous:
        cells = [c.strip() for c in spec.split(";")]
        if len(cells) != 5:
            sys.exit(f"--previous expects 5 fields separated by ';', got: {spec!r}")
        row = table.add_row()
        for cell, text in zip(row.cells, cells):
            cell.text = text
        current.addprevious(row._tr)


if __name__ == "__main__":
    main()
