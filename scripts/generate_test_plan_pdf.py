from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import LongTable, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src" / "data.ts"
OUTPUT = ROOT / "output" / "pdf" / "Proyecto1_Caso1_PlanDePruebas.pdf"

INK = colors.HexColor("#1D1D1F")
INK_SOFT = colors.HexColor("#3A3A3C")
MUTED = colors.HexColor("#6E6E73")
LINE = colors.HexColor("#D9D9DE")
SURFACE = colors.HexColor("#F5F5F7")
WHITE = colors.white


def load_project_data() -> tuple[list[dict], list[dict]]:
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
    name="PlanTitle", parent=styles["Title"], fontName="Helvetica-Bold",
    fontSize=28, leading=32, textColor=INK, spaceAfter=8,
))
styles.add(ParagraphStyle(
    name="PlanSubtitle", parent=styles["BodyText"], fontName="Helvetica",
    fontSize=13, leading=18, textColor=MUTED, spaceAfter=20,
))
styles.add(ParagraphStyle(
    name="Section", parent=styles["Heading1"], fontName="Helvetica-Bold",
    fontSize=17, leading=21, textColor=INK, spaceBefore=3, spaceAfter=8,
))
styles.add(ParagraphStyle(
    name="Subsection", parent=styles["Heading2"], fontName="Helvetica-Bold",
    fontSize=11.5, leading=15, textColor=INK, spaceBefore=10, spaceAfter=5,
))
styles.add(ParagraphStyle(
    name="BodyPlan", parent=styles["BodyText"], fontName="Helvetica",
    fontSize=9.3, leading=13.5, textColor=INK_SOFT, spaceAfter=6,
))
styles.add(ParagraphStyle(
    name="BulletPlan", parent=styles["BodyPlan"], leftIndent=10,
    firstLineIndent=-7, spaceAfter=3,
))
styles.add(ParagraphStyle(
    name="TableCell", parent=styles["BodyText"], fontName="Helvetica",
    fontSize=7.7, leading=10.2, textColor=INK_SOFT,
))
styles.add(ParagraphStyle(
    name="TableCellStrong", parent=styles["TableCell"], fontName="Helvetica-Bold", textColor=INK,
))
styles.add(ParagraphStyle(
    name="TableHeader", parent=styles["TableCell"], fontName="Helvetica-Bold",
    fontSize=7.5, leading=9.5, textColor=WHITE,
))
styles.add(ParagraphStyle(
    name="MetaLabel", parent=styles["BodyText"], fontName="Helvetica",
    fontSize=8, leading=11, textColor=MUTED,
))
styles.add(ParagraphStyle(
    name="MetaValue", parent=styles["BodyText"], fontName="Helvetica-Bold",
    fontSize=9, leading=12, textColor=INK,
))
styles.add(ParagraphStyle(
    name="Callout", parent=styles["BodyPlan"], fontName="Helvetica-Bold",
    fontSize=10, leading=14, textColor=INK, leftIndent=5, rightIndent=5,
))


def escape(value: str) -> str:
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def paragraph(value: str, style: str = "BodyPlan") -> Paragraph:
    return Paragraph(escape(value), styles[style])


def bullets(items: list[str]) -> list[Paragraph]:
    return [Paragraph(f"- {escape(item)}", styles["BulletPlan"]) for item in items]


def styled_table(rows: list[list], widths: list[float], repeat_rows: int = 1) -> LongTable:
    table = LongTable(rows, colWidths=widths, repeatRows=repeat_rows)
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE),
        ("BACKGROUND", (0, 0), (-1, 0), INK),
        ("BACKGROUND", (0, 1), (-1, -1), WHITE),
    ]))
    return table


def footer(canvas, doc) -> None:
    canvas.saveState()
    width, _ = A4
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.5)
    canvas.line(18 * mm, 14 * mm, width - 18 * mm, 14 * mm)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7.4)
    canvas.drawString(18 * mm, 9 * mm, "Plan de pruebas - ParaBank - PP-PB-01")
    page = f"Página {doc.page}"
    canvas.drawString(width - 18 * mm - stringWidth(page, "Helvetica", 7.4), 9 * mm, page)
    canvas.restoreState()


def build(functionalities: list[dict], requirements: list[dict]) -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUTPUT), pagesize=A4,
        leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm, bottomMargin=20 * mm,
        title="Plan de Pruebas - Proyecto 1 - ParaBank",
        author="Kalos Lazo y Gianpier Segovia",
        subject="Plan de pruebas basado en ISO/IEC/IEEE 29119-3:2021",
    )
    story = [
        Spacer(1, 10 * mm),
        Paragraph("Plan de pruebas", styles["PlanTitle"]),
        Paragraph("Proyecto 1 - Caso 1: banca digital con ParaBank", styles["PlanSubtitle"]),
    ]

    metadata = Table([
        [paragraph("Proyecto / aplicativo", "MetaLabel"), paragraph("ParaBank", "MetaValue")],
        [paragraph("Identificador", "MetaLabel"), paragraph("PP-PB-01", "MetaValue")],
        [paragraph("Versión", "MetaLabel"), paragraph("1.0", "MetaValue")],
        [paragraph("Fecha", "MetaLabel"), paragraph("18 de septiembre de 2026", "MetaValue")],
        [paragraph("Elaborado por", "MetaLabel"), paragraph("Kalos Lazo y Gianpier Segovia", "MetaValue")],
        [paragraph("Estado de aprobación", "MetaLabel"), paragraph("Pendiente de revisión docente", "MetaValue")],
    ], colWidths=[43 * mm, 124 * mm])
    metadata.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("BACKGROUND", (0, 0), (-1, -1), SURFACE),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE),
    ]))
    story.extend([metadata, Spacer(1, 8 * mm)])

    callout = Table([[Paragraph(
        "Objetivo: comprobar que los flujos bancarios críticos preserven la integridad del dinero, controlen el acceso y produzcan resultados observables antes de la campaña de captación de clientes.",
        styles["Callout"],
    )]], colWidths=[167 * mm])
    callout.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), SURFACE),
        ("BOX", (0, 0), (-1, -1), 0.6, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    story.extend([callout, Spacer(1, 8 * mm), Paragraph("1. Identificación del documento", styles["Section"])])
    story.append(paragraph(
        "Este plan identifica el enfoque para planificar, analizar, diseñar y ejecutar pruebas manuales sobre el sistema real ParaBank. Se basa en la plantilla académica alineada con ISO/IEC/IEEE 29119-3:2021 y en los requisitos funcionales detallados del primer avance.",
    ))
    story.append(Paragraph("2. Contexto", styles["Section"]))
    story.append(paragraph(
        "ParaBank representa un banco digital con registro de clientes, cuentas, transferencias, pago de servicios, historial, perfil, préstamos y administración. El negocio necesita reducir fallas financieras, decisiones crediticias incorrectas y pérdida de sesión durante operaciones críticas.",
    ))
    story.extend(bullets([
        "Sistema real: https://parabank.parasoft.com/parabank/index.htm",
        "Base de pruebas: 8 funcionalidades y 22 requisitos funcionales del primer avance.",
        "Equipo: 2 integrantes; las pruebas se ejecutarán con datos ficticios.",
        "Enfoque principal: pruebas basadas en riesgo y diseño de caja negra.",
    ]))
    story.append(PageBreak())

    story.append(Paragraph("3. Ítems de prueba y alcance", styles["Section"]))
    story.append(paragraph("Se incluyen todas las funcionalidades definidas para el Caso 1."))
    scope_rows = [[
        paragraph("ID", "TableHeader"), paragraph("Funcionalidad", "TableHeader"),
        paragraph("Cobertura prevista", "TableHeader"), paragraph("Prioridad base", "TableHeader"),
    ]]
    critical_ids = {"F-02", "F-03", "F-04"}
    for item in functionalities:
        priority = "Alta" if item["id"] in critical_ids else "Media"
        coverage = f'{item["location"]}. {len(item["requirementIds"])} RF asociados.'
        scope_rows.append([
            paragraph(item["id"], "TableCellStrong"), paragraph(item["name"], "TableCellStrong"),
            paragraph(coverage, "TableCell"), paragraph(priority, "TableCellStrong"),
        ])
    story.append(styled_table(scope_rows, [16 * mm, 48 * mm, 83 * mm, 20 * mm]))
    story.append(Paragraph("Fuera de alcance", styles["Subsection"]))
    story.extend(bullets([
        "Pruebas unitarias o de componente, porque no se dispone del código fuente ni del pipeline de ParaBank.",
        "Uso de datos bancarios reales, información personal real o transacciones con dinero real.",
        "Pruebas de infraestructura, recuperación ante desastres y disponibilidad continua del proveedor.",
        "Automatización del conjunto de pruebas; se evaluará como recomendación para el Proyecto 2.",
    ]))
    story.append(Paragraph("Criterios de alcance", styles["Subsection"]))
    story.extend(bullets([
        "Cobertura trazable de los 22 RF y de las 8 funcionalidades.",
        "Diseño mínimo de 15 casos sobre al menos 4 funcionalidades, priorizando riesgo alto y medio.",
        "Ejecución manual de todos los casos clasificados como prioridad alta.",
    ]))
    story.append(PageBreak())

    story.append(Paragraph("4. Supuestos y restricciones", styles["Section"]))
    assumptions = [
        ["Supuesto", "El entorno público de ParaBank estará disponible durante las sesiones de prueba.", "Validar URL al inicio y registrar bloqueos."],
        ["Supuesto", "Se podrán crear clientes y al menos dos cuentas propias con saldos conocidos.", "Preparar datos antes de ejecutar transferencias."],
        ["Supuesto", "Las reglas visibles del sistema representan la versión objeto de prueba.", "Registrar fecha, navegador y evidencia por sesión."],
        ["Restricción", "No existe acceso al código fuente, base de datos ni logs del servidor.", "Aplicar caja negra y observar interfaz, saldos e historial."],
        ["Restricción", "El entorno es compartido y sus datos pueden cambiar entre sesiones.", "Usar identificadores únicos y no depender de datos ajenos."],
        ["Restricción", "Tiempo y personal limitados a dos integrantes.", "Ejecutar primero casos de riesgo alto."],
    ]
    assumption_rows = [[paragraph("Tipo", "TableHeader"), paragraph("Condición", "TableHeader"), paragraph("Tratamiento", "TableHeader")]]
    assumption_rows += [[paragraph(a), paragraph(b), paragraph(c)] for a, b, c in assumptions]
    story.append(styled_table(assumption_rows, [23 * mm, 79 * mm, 65 * mm]))

    story.append(Paragraph("5. Riesgos", styles["Section"]))
    risks = [
        ["R-01", "Producto", "Débito sin crédito o crédito incorrecto en transferencias.", "Media", "Muy alto", "Casos de saldo antes/después e historial; prioridad alta."],
        ["R-02", "Producto", "Pago procesado con datos inválidos o saldo insuficiente.", "Media", "Muy alto", "Particiones válidas/inválidas y límite saldo + 0.01."],
        ["R-03", "Producto", "Préstamo aprobado o rechazado de forma incorrecta.", "Media", "Alto", "Tabla de decisión y valores cercanos al umbral."],
        ["R-04", "Producto", "Pérdida de sesión durante una operación.", "Media", "Alto", "Transición de estados y verificación posterior del saldo."],
        ["R-05", "Producto", "Acciones administrativas alteran datos sin confirmación clara.", "Baja", "Alto", "Usar datos recuperables y ejecutar al final de la sesión."],
        ["R-06", "Producto", "Respuesta superior a 3 segundos en transacciones.", "Media", "Medio", "Medir varias operaciones y registrar tiempos observados."],
        ["R-07", "Proceso", "Entorno público caído o inestable.", "Alta", "Alto", "Reintentar en otra franja; registrar caso como bloqueado."],
        ["R-08", "Proceso", "Datos de prueba contaminados por otros usuarios.", "Media", "Medio", "Usuarios únicos, saldos base y evidencia fechada."],
    ]
    risk_rows = [[
        paragraph("ID", "TableHeader"), paragraph("Tipo", "TableHeader"), paragraph("Riesgo", "TableHeader"),
        paragraph("Prob.", "TableHeader"), paragraph("Impacto", "TableHeader"), paragraph("Tratamiento", "TableHeader"),
    ]]
    risk_rows += [[paragraph(cell, "TableCellStrong" if index in {0, 3, 4} else "TableCell") for index, cell in enumerate(row)] for row in risks]
    story.append(styled_table(risk_rows, [12 * mm, 17 * mm, 48 * mm, 16 * mm, 18 * mm, 56 * mm]))
    story.append(PageBreak())

    story.append(Paragraph("6. Estrategia de pruebas", styles["Section"]))
    story.append(paragraph(
        "Se aplicará una estrategia analítica basada en riesgo. Las operaciones que modifican dinero se probarán con mayor profundidad y evidencia de estado antes y después. El trabajo será principalmente de caja negra sobre la interfaz web y el comportamiento observable.",
    ))
    story.append(Paragraph("Niveles de prueba", styles["Subsection"]))
    levels = [
        ["Componente", "No aplicable de forma directa", "Sin acceso al código fuente; se documenta como fuera de alcance."],
        ["Integración", "Profundidad alta", "Transferencia, bill pay e historial: consistencia entre formularios, cuentas y transacciones."],
        ["Sistema", "Cobertura completa", "Las 8 funcionalidades y los 22 RF se validan en el sistema desplegado."],
        ["Aceptación", "Flujos críticos", "Registro, apertura, transferencia y pago con resultados comprensibles para el cliente."],
    ]
    level_rows = [[paragraph("Nivel", "TableHeader"), paragraph("Cobertura", "TableHeader"), paragraph("Aplicación", "TableHeader")]]
    level_rows += [[paragraph(a, "TableCellStrong"), paragraph(b), paragraph(c)] for a, b, c in levels]
    story.append(styled_table(level_rows, [28 * mm, 39 * mm, 100 * mm]))
    story.append(Paragraph("Tipos de prueba", styles["Subsection"]))
    story.extend(bullets([
        "Funcionales: entradas, reglas, mensajes y persistencia para los 22 RF.",
        "Integridad de datos: débito, crédito, saldos e historial en operaciones monetarias.",
        "Sesión y acceso: autenticación inválida, autenticación válida e inactividad.",
        "Rendimiento básico: tiempo observable menor a 3 segundos en una operación válida.",
        "Usabilidad operativa: mensajes claros ante rechazo o validación.",
    ]))
    story.append(Paragraph("Técnicas de diseño", styles["Subsection"]))
    technique_rows = [[paragraph("Técnica", "TableHeader"), paragraph("Aplicación", "TableHeader")]]
    techniques = [
        ["Partición de equivalencia", "Campos obligatorios, credenciales, filtros, datos de perfil y beneficiario."],
        ["Valores límite", "Saldo disponible, saldo + 0.01, monto cero/negativo y umbral de enganche."],
        ["Tabla de decisión", "Apertura de cuenta, transferencias, bill pay y evaluación de préstamos."],
        ["Transición de estados", "Sesión autenticada/no autenticada, creación de cuenta y persistencia del perfil."],
        ["Basada en experiencia", "Exploración breve de mensajes, doble envío y consistencia visual del historial."],
    ]
    technique_rows += [[paragraph(a, "TableCellStrong"), paragraph(b)] for a, b in techniques]
    story.append(styled_table(technique_rows, [48 * mm, 119 * mm]))
    story.append(PageBreak())

    story.append(Paragraph("Criterios de entrada y salida", styles["Section"]))
    criteria_rows = [[paragraph("Entrada", "TableHeader"), paragraph("Salida", "TableHeader")]]
    entry = "URL disponible; RF revisados; cuenta de prueba creada; dos cuentas propias; saldos conocidos; navegador estable; datos ficticios preparados."
    exit_criteria = "22 RF trazados; mínimo 15 casos diseñados; todos los casos altos ejecutados; evidencias guardadas; hallazgos documentados; bloqueos justificados."
    criteria_rows.append([paragraph(entry), paragraph(exit_criteria)])
    story.append(styled_table(criteria_rows, [83.5 * mm, 83.5 * mm]))

    story.append(Paragraph("7. Entregables de prueba", styles["Section"]))
    story.extend(bullets([
        "Documento de funcionalidades y requisitos detallados del primer avance.",
        "Plan de pruebas aprobado por el equipo.",
        "Matriz de trazabilidad Requisito - Condición - Caso.",
        "Mínimo 15 casos de prueba con técnica y datos asociados.",
        "Registro de ejecución manual de casos de prioridad alta.",
        "Reporte de hallazgos con pasos, esperado, obtenido, severidad y evidencia.",
        "Reporte de cierre con recomendación de automatización para el Proyecto 2.",
    ]))

    story.append(Paragraph("8. Tareas de prueba y estimación", styles["Section"]))
    tasks = [
        ["Planificación", "Alcance, riesgos, estrategia y criterios.", "4 h"],
        ["Análisis", "Condiciones y trazabilidad de 22 RF.", "6 h"],
        ["Diseño", "Casos, técnicas y datos de prueba.", "10 h"],
        ["Preparación", "Usuarios, cuentas, saldos y entorno.", "3 h"],
        ["Ejecución", "Casos altos y captura de evidencia.", "8 h"],
        ["Cierre", "Hallazgos, conclusiones y revisión final.", "5 h"],
    ]
    task_rows = [[paragraph("Fase", "TableHeader"), paragraph("Actividad", "TableHeader"), paragraph("Esfuerzo del equipo", "TableHeader")]]
    task_rows += [[paragraph(a, "TableCellStrong"), paragraph(b), paragraph(c)] for a, b, c in tasks]
    story.append(styled_table(task_rows, [35 * mm, 92 * mm, 40 * mm]))
    story.append(paragraph("Estimación total: 36 horas de trabajo del equipo. Se ajustará según disponibilidad del entorno y número de hallazgos."))
    story.append(PageBreak())

    story.append(Paragraph("9. Necesidades de entorno y datos de prueba", styles["Section"]))
    environment_rows = [[paragraph("Categoría", "TableHeader"), paragraph("Necesidad", "TableHeader")]]
    environment = [
        ["Hardware", "Dos laptops con conexión estable a Internet."],
        ["Software", "Chrome actualizado; herramienta de captura; hoja de cálculo o documento para resultados."],
        ["Sistema", "ParaBank público y URL de administración disponible."],
        ["Datos", "Usuarios ficticios únicos; dos cuentas propias; saldos iniciales conocidos; beneficiarios ficticios."],
        ["Seguridad", "No usar nombres, SSN, teléfonos, direcciones ni credenciales reales."],
        ["Evidencia", "Captura antes, confirmación, captura después e historial para operaciones monetarias."],
    ]
    environment_rows += [[paragraph(a, "TableCellStrong"), paragraph(b)] for a, b in environment]
    story.append(styled_table(environment_rows, [37 * mm, 130 * mm]))

    story.append(Paragraph("10. Responsabilidades y comunicación", styles["Section"]))
    responsibility_rows = [[paragraph("Responsable", "TableHeader"), paragraph("Responsabilidad principal", "TableHeader")]]
    responsibilities = [
        ["Kalos Lazo", "Planificación, requisitos, trazabilidad y consolidación del informe."],
        ["Gianpier Segovia", "Diseño de casos, preparación de datos y coordinación de ejecución."],
        ["Ambos integrantes", "Revisión cruzada, ejecución de casos altos, análisis de hallazgos y exposición."],
        ["Docente", "Revisión académica, retroalimentación y aprobación de entregables."],
    ]
    responsibility_rows += [[paragraph(a, "TableCellStrong"), paragraph(b)] for a, b in responsibilities]
    story.append(styled_table(responsibility_rows, [46 * mm, 121 * mm]))
    story.extend(bullets([
        "Canal operativo: reunión breve del equipo y repositorio GitHub para versionar artefactos.",
        "Escalamiento: bloqueos del entorno o ambigüedades del alcance se consultan a la docente.",
        "Regla de revisión: ningún caso alto se considera cerrado sin evidencia revisada por ambos integrantes.",
    ]))

    story.append(Paragraph("11. Cronograma e hitos", styles["Section"]))
    schedule = [
        ["Hito 1", "18/09/2026", "Funcionalidades y requisitos detallados."],
        ["Hito 2", "Semana siguiente", "Plan, riesgos y matriz de trazabilidad."],
        ["Hito 3", "Semana posterior", "Diseño de casos y datos de prueba."],
        ["Hito 4", "Antes de la entrega final", "Ejecución manual de casos altos y hallazgos."],
        ["Hito 5", "Entrega final", "Informe consolidado, cierre y recomendación de automatización."],
    ]
    schedule_rows = [[paragraph("Hito", "TableHeader"), paragraph("Momento", "TableHeader"), paragraph("Resultado", "TableHeader")]]
    schedule_rows += [[paragraph(a, "TableCellStrong"), paragraph(b), paragraph(c)] for a, b, c in schedule]
    story.append(styled_table(schedule_rows, [25 * mm, 45 * mm, 97 * mm]))
    story.append(Spacer(1, 7 * mm))
    story.append(paragraph("Nota de control: las fechas posteriores al primer avance deben alinearse con el calendario oficial publicado en Canvas."))

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def validate(functionalities: list[dict], requirements: list[dict]) -> None:
    reader = PdfReader(str(OUTPUT))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    normalized_text = re.sub(r"\s+", " ", text)
    required_sections = [
        "1. Identificación del documento", "2. Contexto", "3. Ítems de prueba y alcance",
        "4. Supuestos y restricciones", "5. Riesgos", "6. Estrategia de pruebas",
        "7. Entregables de prueba", "8. Tareas de prueba y estimación",
        "9. Necesidades de entorno y datos de prueba", "10. Responsabilidades y comunicación",
        "11. Cronograma e hitos",
    ]
    missing = [section for section in required_sections if section not in text]
    if missing:
        raise RuntimeError(f"Secciones faltantes: {missing}")
    if len(functionalities) != 8 or len(requirements) != 22:
        raise RuntimeError("La fuente del proyecto no conserva la cobertura esperada.")
    if not all(item["name"] in normalized_text for item in functionalities):
        raise RuntimeError("Falta una funcionalidad en la tabla de alcance.")
    print(json.dumps({
        "output": str(OUTPUT), "pages": len(reader.pages),
        "sections": len(required_sections), "functionalities": len(functionalities),
        "requirements_reference": len(requirements),
    }, ensure_ascii=False))


if __name__ == "__main__":
    project_functionalities, project_requirements = load_project_data()
    build(project_functionalities, project_requirements)
    validate(project_functionalities, project_requirements)
