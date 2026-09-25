"""Informe final consolidado - Proyecto 1 - Caso 1 ParaBank.

Un solo informe con secciones diferenciadas, alineado a la Guía de Entrega:
  1. Planificación de pruebas (resumen + estrategia justificada + niveles)
  2. Análisis de pruebas (priorización de los 22 RF por riesgo)
  3. Diseño de pruebas (18 casos + justificación de técnicas)
  4. Ejecución de casos críticos y hallazgos (desde execution_results.json)

Los casos se leen de generate_matriz_excel.CASES para mantener una sola fuente
de verdad con la matriz Excel. Los veredictos/hallazgos se leen del JSON que se
completa tras la ejecución manual en ParaBank.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import (LongTable, PageBreak, Paragraph, SimpleDocTemplate,
                                Spacer, Table, TableStyle)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "Proyecto1_Caso1_InformeFinal.pdf"
RESULTS = ROOT / "output" / "matriz" / "execution_results.json"

# Reusar la definición de casos de la matriz (fuente única de verdad).
_spec = importlib.util.spec_from_file_location("matriz", ROOT / "scripts" / "generate_matriz_excel.py")
_matriz = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_matriz)
CASES = _matriz.CASES
HIGH_CASES = _matriz.HIGH_CASES

INK = colors.HexColor("#1D1D1F")
INK_SOFT = colors.HexColor("#3A3A3C")
MUTED = colors.HexColor("#6E6E73")
LINE = colors.HexColor("#D9D9DE")
SURFACE = colors.HexColor("#F5F5F7")
GOOD = colors.HexColor("#1B7F4B")
BAD = colors.HexColor("#B3261E")
WARN = colors.HexColor("#8A6D00")
WHITE = colors.white

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="H0", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=28, leading=32, textColor=INK, spaceAfter=6))
styles.add(ParagraphStyle(name="Sub", parent=styles["BodyText"], fontName="Helvetica", fontSize=13, leading=18, textColor=MUTED, spaceAfter=18))
styles.add(ParagraphStyle(name="H1", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=16, leading=20, textColor=INK, spaceBefore=4, spaceAfter=7))
styles.add(ParagraphStyle(name="H2", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=11.5, leading=15, textColor=INK, spaceBefore=9, spaceAfter=4))
styles.add(ParagraphStyle(name="Body", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.3, leading=13.5, textColor=INK_SOFT, spaceAfter=6))
styles.add(ParagraphStyle(name="Bull", parent=styles["Body"], leftIndent=10, firstLineIndent=-7, spaceAfter=3))
styles.add(ParagraphStyle(name="TC", parent=styles["BodyText"], fontName="Helvetica", fontSize=7.4, leading=9.8, textColor=INK_SOFT))
styles.add(ParagraphStyle(name="TCS", parent=styles["TC"], fontName="Helvetica-Bold", textColor=INK))
styles.add(ParagraphStyle(name="TH", parent=styles["TC"], fontName="Helvetica-Bold", fontSize=7.3, leading=9.3, textColor=WHITE))
styles.add(ParagraphStyle(name="ML", parent=styles["BodyText"], fontName="Helvetica", fontSize=8, leading=11, textColor=MUTED))
styles.add(ParagraphStyle(name="MV", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=INK))


def esc(v: str) -> str:
    return str(v).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def P(v, s="Body"):
    return Paragraph(esc(v).replace("\n", "<br/>"), styles[s])


def bullets(items):
    return [Paragraph(f"- {esc(x)}", styles["Bull"]) for x in items]


def table(rows, widths, repeat=1):
    t = LongTable(rows, colWidths=widths, repeatRows=repeat)
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4.5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4.5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE),
        ("BACKGROUND", (0, 0), (-1, 0), INK),
    ]))
    return t


def verdict_color(v):
    return {"Pasó": GOOD, "Falló": BAD, "Bloqueado": WARN}.get(v, MUTED)


# --- Contenido: priorización de los 22 RF (según el primer avance) ----------
RF_PRIORITY = [
    ("RF-01", "F-01", "Registrar cliente con datos válidos y usuario único", "Media"),
    ("RF-02", "F-01", "Rechazar registro con usuario ya existente", "Alta"),
    ("RF-03", "F-01", "Rechazar acceso con credenciales inválidas", "Alta"),
    ("RF-04", "F-01", "Permitir acceso con credenciales válidas", "Media"),
    ("RF-05", "F-02", "Abrir cuenta con tipo y cuenta de fondeo válidos", "Alta"),
    ("RF-06", "F-02", "Rechazar apertura sin tipo o sin cuenta de fondeo", "Alta"),
    ("RF-07", "F-02", "Mostrar la cuenta creada con número y saldo", "Media"),
    ("RF-08", "F-03", "Transferir con débito y crédito por el mismo monto", "Alta"),
    ("RF-09", "F-03", "Rechazar transferencia mayor al saldo disponible", "Alta"),
    ("RF-10", "F-03", "Rechazar monto 0, negativo o misma cuenta", "Media"),
    ("RF-11", "F-04", "Procesar bill pay con datos y saldo válidos", "Alta"),
    ("RF-12", "F-04", "Rechazar bill pay con campos faltantes o inválidos", "Alta"),
    ("RF-13", "F-04", "Rechazar bill pay mayor al saldo de la cuenta", "Alta"),
    ("RF-14", "F-05", "Buscar transacciones por fecha o rango válido", "Media"),
    ("RF-15", "F-05", "Localizar transacción por monto o ID", "Media"),
    ("RF-16", "F-06", "Guardar datos de contacto válidos", "Media"),
    ("RF-17", "F-06", "No guardar datos de contacto inválidos", "Baja"),
    ("RF-18", "F-07", "Aprobar préstamo si cumple la regla de enganche", "Media"),
    ("RF-19", "F-07", "Rechazar préstamo si el enganche no cumple", "Media"),
    ("RF-20", "F-08", "Inicializar o limpiar la base de datos", "Media"),
    ("RF-21", "F-08", "Configurar parámetros numéricos del banco", "Media"),
    ("RF-22", "F-08", "Seleccionar proveedor y procesador de préstamos", "Baja"),
]

HIGH_JUSTIFY = [
    ("RF-02", "Un usuario duplicado corrompe la identidad del cliente y habilita cuentas ambiguas durante la captación masiva; es un control de integridad de acceso."),
    ("RF-03", "Es la primera barrera de control de acceso: una autenticación laxa expone cuentas y dinero de terceros."),
    ("RF-05", "La apertura correcta habilita todas las operaciones monetarias posteriores; sin cuentas bien creadas no existe flujo financiero válido."),
    ("RF-06", "Evita cuentas mal formadas (sin tipo o sin fondeo) que luego comprometen transferencias y pagos."),
    ("RF-08", "Es el riesgo financiero central del caso: un débito sin crédito (o viceversa) produce pérdida directa de dinero y reclamos."),
    ("RF-09", "Previene sobregiros y saldos inconsistentes al mover más dinero del disponible."),
    ("RF-11", "Mueve dinero hacia terceros; un pago procesado con datos incorrectos causa pérdida directa y reclamos difíciles de revertir."),
    ("RF-12", "La validación de campos evita pagos a beneficiarios mal definidos o por montos inválidos."),
    ("RF-13", "Protege la integridad del saldo impidiendo pagos que exceden los fondos de la cuenta."),
]

TECHNIQUE_JUSTIFY = [
    ("Partición de equivalencia", "CP-01, CP-02, CP-03, CP-12, CP-15, CP-16",
     "Los formularios (registro, credenciales, bill pay, filtros, perfil) tienen clases de entrada válidas e inválidas; probar un representante de cada clase reduce casos redundantes sin perder cobertura."),
    ("Análisis de valores límite", "CP-09, CP-10, CP-13, CP-14, CP-18",
     "Las reglas de dinero se definen sobre umbrales (saldo, saldo + 0.01, monto cero/negativo, umbral de enganche); los defectos se concentran en los bordes, por eso se prueban exactamente el límite y su vecino."),
    ("Tabla de decisión", "CP-05, CP-06, CP-08, CP-11, CP-17",
     "Las operaciones combinan varias condiciones (tipo x cuenta de fondeo; origen x destino x monto x saldo; beneficiario x cuenta x monto); la tabla de decisión asegura cubrir las combinaciones relevantes de reglas de negocio."),
    ("Transición de estados", "CP-04, CP-07",
     "La sesión y las cuentas cambian de estado (no autenticado -> autenticado; cuenta inexistente -> creada y persistente); se verifica que cada transición y su efecto observable ocurran correctamente."),
]


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    results, findings = {}, []
    if RESULTS.exists():
        payload = json.loads(RESULTS.read_text(encoding="utf-8"))
        results = payload.get("execution", {})
        findings = payload.get("findings", [])

    doc = SimpleDocTemplate(
        str(OUTPUT), pagesize=A4,
        leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm, bottomMargin=20 * mm,
        title="Informe Final - Proyecto 1 - ParaBank",
        author="Kalos Lazo y Gianpier Segovia",
    )
    S = [Spacer(1, 8 * mm), P("Informe de pruebas", "H0"),
         P("Proyecto 1 - Caso 1: banca digital con ParaBank", "Sub")]

    meta = Table([
        [P("Curso", "ML"), P("CS5383 - Verificación y Pruebas de Software", "MV")],
        [P("Sistema real", "ML"), P("ParaBank - https://parabank.parasoft.com/parabank/index.htm", "MV")],
        [P("Integrantes", "ML"), P("Kalos Lazo y Gianpier Segovia", "MV")],
        [P("Identificador del plan", "ML"), P("PP-PB-01 - Versión 1.0", "MV")],
        [P("Fecha", "ML"), P("Septiembre de 2026", "MV")],
    ], colWidths=[43 * mm, 124 * mm])
    meta.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7), ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6), ("BACKGROUND", (0, 0), (-1, -1), SURFACE),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE),
    ]))
    S += [meta, Spacer(1, 6 * mm)]
    S.append(P("Este informe consolida las cuatro actividades del proceso de pruebas sobre el sistema real ParaBank: planificación, análisis, diseño y ejecución. El plan de pruebas completo (11 secciones, ISO/IEC/IEEE 29119-3:2021) se entrega como documento acompañante PP-PB-01 y aquí se resume su estrategia. La matriz de casos se entrega en el archivo Excel adjunto.", "Body"))
    S.append(PageBreak())

    # ---- 1. Planificación (resumen) ----
    S.append(P("1. Planificación de pruebas", "H1"))
    S.append(P("Objetivo: comprobar que los flujos bancarios críticos preserven la integridad del dinero, controlen el acceso y produzcan resultados observables antes de la campaña de captación de clientes.", "Body"))
    S.append(P("Estrategia de pruebas (justificación)", "H2"))
    S.append(P("Se adopta una estrategia analítica basada en riesgo. El contexto es banca digital: el activo en juego es el dinero y la confianza del cliente, los datos son críticos y las operaciones monetarias son las de mayor impacto. Por eso el esfuerzo se concentra donde el riesgo de negocio es mayor (transferencias, pagos, apertura de cuentas y acceso) y se prueba con evidencia de estado antes/después. Al no disponer del código fuente de ParaBank, el trabajo es esencialmente de caja negra sobre el comportamiento observable.", "Body"))
    S.append(P("Niveles de prueba a aplicar", "H2"))
    levels = [
        ("Componente", "Fuera de alcance", "No hay acceso al código fuente ni al pipeline de ParaBank."),
        ("Integración", "Profundidad alta", "Consistencia entre formularios, cuentas, saldos e historial en transferencias y bill pay."),
        ("Sistema", "Cobertura completa", "Las 8 funcionalidades y los 22 RF se validan sobre el sistema desplegado."),
        ("Aceptación", "Flujos críticos", "Registro, apertura, transferencia y pago con resultados comprensibles para el cliente."),
    ]
    rows = [[P("Nivel", "TH"), P("Profundidad", "TH"), P("Aplicación", "TH")]]
    rows += [[P(a, "TCS"), P(b, "TC"), P(c, "TC")] for a, b, c in levels]
    S.append(table(rows, [30 * mm, 34 * mm, 103 * mm]))
    S.append(Spacer(1, 3 * mm))
    S.append(P("La estrategia, riesgos (R-01 a R-08), criterios de entrada/salida, estimación (36 h), entorno, responsabilidades y cronograma se detallan en el plan PP-PB-01.", "Body"))
    S.append(PageBreak())

    # ---- 2. Análisis de pruebas ----
    S.append(P("2. Análisis de pruebas", "H1"))
    n_alta = sum(1 for r in RF_PRIORITY if r[3] == "Alta")
    n_media = sum(1 for r in RF_PRIORITY if r[3] == "Media")
    n_baja = sum(1 for r in RF_PRIORITY if r[3] == "Baja")
    S.append(P(f"Se priorizan por riesgo los 22 requisitos funcionales del primer avance: {n_alta} de prioridad alta, {n_media} media y {n_baja} baja. El criterio es el impacto en el negocio bancario: mueven o comprometen dinero, o controlan el acceso -> alta; soportan la operación o la trazabilidad -> media; validaciones secundarias o configuración -> baja.", "Body"))
    rows = [[P("RF", "TH"), P("Func.", "TH"), P("Requisito", "TH"), P("Prioridad", "TH")]]
    for rid, fid, desc, pr in RF_PRIORITY:
        pr_style = "TCS"
        rows.append([P(rid, "TCS"), P(fid, "TC"), P(desc, "TC"), P(pr, pr_style)])
    S.append(table(rows, [16 * mm, 15 * mm, 116 * mm, 20 * mm]))
    S.append(P("Justificación de las prioridades altas", "H2"))
    jrows = [[P("RF", "TH"), P("Por qué es riesgo alto", "TH")]]
    jrows += [[P(rid, "TCS"), P(txt, "TC")] for rid, txt in HIGH_JUSTIFY]
    S.append(table(jrows, [16 * mm, 151 * mm]))
    S.append(PageBreak())

    # ---- 3. Diseño de pruebas ----
    S.append(P("3. Diseño de pruebas", "H1"))
    S.append(P(f"Se derivan {len(CASES)} casos de prueba de los RF priorizados, cubriendo 6 funcionalidades. Los {len(HIGH_CASES)} casos de prioridad alta corresponden a los 9 RF de riesgo alto y son los que se ejecutan sobre el sistema real (sección 4). Cada caso indica su RF, prioridad, técnica de diseño, precondiciones, pasos, datos y resultado esperado (detalle completo en la matriz Excel).", "Body"))
    S.append(P("Técnicas de diseño aplicadas (caja negra) y su justificación", "H2"))
    trows = [[P("Técnica", "TH"), P("Casos", "TH"), P("Por qué se aplica", "TH")]]
    trows += [[P(a, "TCS"), P(b, "TC"), P(c, "TC")] for a, b, c in TECHNIQUE_JUSTIFY]
    S.append(table(trows, [38 * mm, 38 * mm, 91 * mm]))
    S.append(P("Casos de prueba diseñados", "H2"))
    crows = [[P("ID", "TH"), P("Funcionalidad", "TH"), P("RF", "TH"), P("Prio.", "TH"), P("Técnica", "TH"), P("Resultado esperado", "TH")]]
    for c in CASES:
        crows.append([P(c[0], "TCS"), P(c[1], "TC"), P(c[2], "TC"), P(c[3], "TC"), P(c[4], "TC"), P(c[8], "TC")])
    S.append(table(crows, [15 * mm, 33 * mm, 14 * mm, 14 * mm, 33 * mm, 58 * mm]))
    S.append(PageBreak())

    # ---- 4. Ejecución y hallazgos ----
    S.append(P("4. Ejecución de casos críticos y hallazgos", "H1"))
    executed = [c for c in HIGH_CASES if c[0] in results]
    if executed:
        passed = sum(1 for c in executed if results[c[0]].get("verdict") == "Pasó")
        failed = sum(1 for c in executed if results[c[0]].get("verdict") == "Falló")
        blocked = sum(1 for c in executed if results[c[0]].get("verdict") == "Bloqueado")
        S.append(P(f"Se ejecutaron manualmente sobre ParaBank los {len(executed)} casos de prioridad alta. Resultado: {passed} pasaron, {failed} fallaron y {blocked} quedaron bloqueados. Cada caso registra resultado esperado, resultado obtenido, veredicto y evidencia.", "Body"))
    else:
        S.append(P("Pendiente de ejecución. Los 9 casos de prioridad alta se ejecutarán manualmente sobre ParaBank registrando resultado obtenido, veredicto (pasó / falló / bloqueado) y evidencia. Al completar la corrida, esta sección se regenera automáticamente desde execution_results.json.", "Body"))

    erows = [[P("ID", "TH"), P("Resultado esperado", "TH"), P("Resultado obtenido", "TH"), P("Veredicto", "TH"), P("Evidencia", "TH")]]
    for c in HIGH_CASES:
        cid = c[0]
        r = results.get(cid, {})
        verdict = r.get("verdict", "Pendiente")
        vp = Paragraph(esc(verdict), ParagraphStyle("v", parent=styles["TCS"], textColor=verdict_color(verdict)))
        erows.append([P(cid, "TCS"), P(c[8], "TC"), P(r.get("obtained", "Pendiente de ejecución."), "TC"), vp, P(r.get("evidence", "-"), "TC")])
    S.append(table(erows, [15 * mm, 52 * mm, 55 * mm, 20 * mm, 25 * mm]))

    S.append(P("Hallazgos", "H2"))
    if findings:
        frows = [[P("ID", "TH"), P("Título", "TH"), P("Esperado vs. obtenido", "TH"), P("Sev.", "TH"), P("Evidencia", "TH")]]
        for f in findings:
            frows.append([P(f.get("id", ""), "TCS"), P(f.get("title", ""), "TC"),
                          P(f"Esperado: {f.get('expected','')}  |  Obtenido: {f.get('obtained','')}", "TC"),
                          P(f.get("severity", ""), "TCS"), P(f.get("evidence", "-"), "TC")])
        S.append(table(frows, [15 * mm, 40 * mm, 72 * mm, 15 * mm, 25 * mm]))
    else:
        S.append(P("Los hallazgos (defectos, comportamientos inesperados o validaciones ausentes) se registrarán durante la ejecución, cada uno con ID, título, resumen, pasos para reproducir, esperado vs. obtenido, severidad y evidencia.", "Body"))

    doc.build(S, onFirstPage=_footer, onLaterPages=_footer)
    print(json.dumps({"output": str(OUTPUT), "cases": len(CASES),
                      "high": len(HIGH_CASES), "executed": len(results),
                      "findings": len(findings)}, ensure_ascii=False))


def _footer(canvas, doc):
    canvas.saveState()
    width, _ = A4
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.5)
    canvas.line(18 * mm, 14 * mm, width - 18 * mm, 14 * mm)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7.4)
    canvas.drawString(18 * mm, 9 * mm, "Informe de pruebas - ParaBank - Proyecto 1 - Caso 1")
    page = f"Página {doc.page}"
    canvas.drawString(width - 18 * mm - stringWidth(page, "Helvetica", 7.4), 9 * mm, page)
    canvas.restoreState()


if __name__ == "__main__":
    build()
