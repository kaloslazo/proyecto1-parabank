from __future__ import annotations

import json
import subprocess
from pathlib import Path

from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import KeepTogether, LongTable, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "Proyecto1_Caso1_KalosLazo_GianpierSegovia.pdf"
SOURCE = ROOT / "src" / "data.ts"

INK = colors.HexColor("#1D1D1F")
INK_SOFT = colors.HexColor("#3A3A3C")
MUTED = colors.HexColor("#6E6E73")
LINE = colors.HexColor("#D9D9DE")
CANVAS = colors.HexColor("#F5F5F7")
SURFACE = colors.white


def load_content() -> tuple[list[dict], list[dict]]:
    node_program = r"""
const fs = require('fs');
const ts = require('typescript');
const source = fs.readFileSync(process.argv[1], 'utf8');
const js = ts.transpileModule(source, {
  compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2020 }
}).outputText;
const exported = {};
new Function('exports', 'module', js)(exported, { exports: exported });
process.stdout.write(JSON.stringify({
  functionalities: exported.clientFunctionalities,
  requirements: exported.clientRequirements
}));
"""
    result = subprocess.run(
        ["node", "-e", node_program, str(SOURCE)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)
    return payload["functionalities"], payload["requirements"]


styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="CoverTitle", parent=styles["Title"], fontName="Helvetica-Bold",
    fontSize=31, leading=35, textColor=INK, alignment=TA_LEFT, spaceAfter=10,
))
styles.add(ParagraphStyle(
    name="CoverSubtitle", parent=styles["BodyText"], fontName="Helvetica",
    fontSize=15, leading=21, textColor=MUTED, spaceAfter=24,
))
styles.add(ParagraphStyle(
    name="SectionTitle", parent=styles["Heading1"], fontName="Helvetica-Bold",
    fontSize=20, leading=24, textColor=INK, spaceAfter=6,
))
styles.add(ParagraphStyle(
    name="SectionLead", parent=styles["BodyText"], fontName="Helvetica",
    fontSize=9.5, leading=14, textColor=MUTED, spaceAfter=13,
))
styles.add(ParagraphStyle(
    name="Cell", parent=styles["BodyText"], fontName="Helvetica",
    fontSize=8.2, leading=11.2, textColor=INK_SOFT, alignment=TA_LEFT,
))
styles.add(ParagraphStyle(name="CellStrong", parent=styles["Cell"], fontName="Helvetica-Bold", textColor=INK))
styles.add(ParagraphStyle(name="CellMuted", parent=styles["Cell"], textColor=MUTED))
styles.add(ParagraphStyle(
    name="HeaderCell", parent=styles["Cell"], fontName="Helvetica-Bold",
    fontSize=7.8, leading=9.8, textColor=colors.white,
))
styles.add(ParagraphStyle(name="MetaLabel", parent=styles["BodyText"], fontName="Helvetica", fontSize=8, leading=11, textColor=MUTED))
styles.add(ParagraphStyle(name="MetaValue", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=INK))
styles.add(ParagraphStyle(name="MetricValue", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=19, leading=22, textColor=INK, alignment=TA_CENTER))
styles.add(ParagraphStyle(name="MetricLabel", parent=styles["BodyText"], fontName="Helvetica", fontSize=7.7, leading=10, textColor=MUTED, alignment=TA_CENTER))


def p(value: str, style: str = "Cell") -> Paragraph:
    safe = value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return Paragraph(safe, styles[style])


def page_chrome(canvas, doc) -> None:
    canvas.saveState()
    width, _ = landscape(A4)
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.5)
    canvas.line(18 * mm, 14 * mm, width - 18 * mm, 14 * mm)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(18 * mm, 9 * mm, "CS5383 - Proyecto 1 - Caso 1: ParaBank")
    page_text = f"Página {doc.page}"
    canvas.drawString(width - 18 * mm - stringWidth(page_text, "Helvetica", 7.5), 9 * mm, page_text)
    canvas.restoreState()


def table_style(header: bool = True) -> TableStyle:
    commands = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("GRID", (0, 0), (-1, -1), 0.45, LINE),
        ("BACKGROUND", (0, 1 if header else 0), (-1, -1), SURFACE),
    ]
    if header:
        commands.extend([
            ("BACKGROUND", (0, 0), (-1, 0), INK),
            ("LINEBELOW", (0, 0), (-1, 0), 0.8, INK),
        ])
    return TableStyle(commands)


def build_pdf(functionalities: list[dict], requirements: list[dict]) -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUTPUT), pagesize=landscape(A4),
        rightMargin=18 * mm, leftMargin=18 * mm, topMargin=17 * mm, bottomMargin=20 * mm,
        title="Proyecto 1 - Primer avance - ParaBank",
        author="Kalos Lazo y Gianpier Segovia",
        subject="Funcionalidades identificadas y requisitos funcionales detallados",
    )
    story = [
        Spacer(1, 22 * mm),
        Paragraph("Proyecto 1 - Primer avance", styles["CoverTitle"]),
        Paragraph("Requisitos del cliente detallados para el Caso 1 de ParaBank", styles["CoverSubtitle"]),
    ]

    meta = Table([
        [p("Curso", "MetaLabel"), p("CS5383 - Verificación y Pruebas de Software", "MetaValue")],
        [p("Sistema real", "MetaLabel"), p("ParaBank, sitio web público de Parasoft", "MetaValue")],
        [p("Integrantes", "MetaLabel"), p("Kalos Lazo y Gianpier Segovia", "MetaValue")],
        [p("Formato elegido", "MetaLabel"), p("Requisito funcional (RF)", "MetaValue")],
        [p("Fecha", "MetaLabel"), p("18 de septiembre de 2026", "MetaValue")],
    ], colWidths=[42 * mm, 151 * mm])
    meta.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("BACKGROUND", (0, 0), (-1, -1), CANVAS),
        ("LINEBELOW", (0, 0), (-1, -2), 0.45, LINE),
        ("BOX", (0, 0), (-1, -1), 0.55, LINE),
    ]))
    story.extend([meta, Spacer(1, 14 * mm)])

    high_count = sum(1 for item in requirements if item["priority"] == "Alta")
    metrics = Table([
        [p(str(len(functionalities)), "MetricValue"), p(str(len(requirements)), "MetricValue"), p(str(high_count), "MetricValue")],
        [p("Funcionalidades cubiertas", "MetricLabel"), p("Requisitos funcionales", "MetricLabel"), p("Prioridad alta", "MetricLabel")],
    ], colWidths=[58 * mm, 58 * mm, 58 * mm])
    metrics.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("BACKGROUND", (0, 0), (-1, -1), SURFACE),
        ("BOX", (0, 0), (-1, -1), 0.55, LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.45, LINE),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.extend([metrics, PageBreak()])

    story.append(Paragraph("Funcionalidades identificadas", styles["SectionTitle"]))
    story.append(Paragraph(
        "Mapa completo del alcance funcional del sistema real. Las secciones siguientes mantienen este mismo orden.",
        styles["SectionLead"],
    ))
    function_rows = [[
        p("ID", "HeaderCell"), p("Funcionalidad", "HeaderCell"),
        p("Dónde se encuentra en el sistema real", "HeaderCell"), p("Actor", "HeaderCell"),
        p("RF", "HeaderCell"),
    ]]
    for item in functionalities:
        function_rows.append([
            p(item["id"], "CellStrong"), p(item["name"], "CellStrong"), p(item["location"]),
            p(item["actor"]), p(str(len(item["requirementIds"])), "CellStrong"),
        ])
    function_table = LongTable(
        function_rows, repeatRows=1,
        colWidths=[16 * mm, 67 * mm, 107 * mm, 40 * mm, 16 * mm],
    )
    function_table.setStyle(table_style())
    story.append(function_table)

    for item in functionalities:
        related = [r for r in requirements if r["functionalityId"] == item["id"]]
        story.append(PageBreak())
        title = f'{item["id"]} - {item["name"]}'
        location = f'<b>Dónde se usa:</b> {item["location"]}'
        story.append(KeepTogether([
            Paragraph(title, styles["SectionTitle"]),
            Paragraph(location, styles["SectionLead"]),
        ]))
        rows = [[
            p("ID", "HeaderCell"), p("Requisito verificable", "HeaderCell"), p("Actor", "HeaderCell"),
            p("Datos y reglas", "HeaderCell"), p("Resultado esperado", "HeaderCell"), p("Prioridad", "HeaderCell"),
        ]]
        for req in related:
            rows.append([
                p(req["id"], "CellStrong"), p(req["requirement"]), p(req["actor"]),
                p(req["dataRules"]), p(req["expected"]), p(req["priority"], "CellStrong"),
            ])
        req_table = LongTable(
            rows, repeatRows=1,
            colWidths=[16 * mm, 55 * mm, 24 * mm, 61 * mm, 68 * mm, 22 * mm],
        )
        req_table.setStyle(table_style())
        story.append(req_table)

    doc.build(story, onFirstPage=page_chrome, onLaterPages=page_chrome)


def validate_pdf(functionalities: list[dict], requirements: list[dict]) -> None:
    reader = PdfReader(str(OUTPUT))
    extracted = "\n".join(page.extract_text() or "" for page in reader.pages)
    expected_terms = [item["id"] for item in functionalities] + [item["id"] for item in requirements]
    missing = [term for term in expected_terms if term not in extracted]
    if missing:
        raise RuntimeError(f"Contenido faltante en el PDF: {missing}")
    if len(functionalities) != 8 or len(requirements) != 22:
        raise RuntimeError("La fuente no contiene las 8 funcionalidades y 22 requisitos esperados.")
    if len(reader.pages) != 10:
        raise RuntimeError(f"Se esperaban 10 páginas y se generaron {len(reader.pages)}.")
    print(json.dumps({
        "output": str(OUTPUT), "pages": len(reader.pages),
        "functionalities": len(functionalities), "requirements": len(requirements),
        "high_priority": sum(1 for item in requirements if item["priority"] == "Alta"),
    }, ensure_ascii=False))


if __name__ == "__main__":
    functionalities_data, requirements_data = load_content()
    build_pdf(functionalities_data, requirements_data)
    validate_pdf(functionalities_data, requirements_data)
