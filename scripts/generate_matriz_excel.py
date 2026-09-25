"""Genera la Matriz de Casos de Prueba (ParaBank) sobre la plantilla oficial.

Rellena las hojas 'Casos de Prueba', 'Ejecución' y 'Hallazgos' con el diseño
del Caso 1 (ParaBank), mapeado a los 22 RF del primer avance. Conserva la hoja
'Instrucciones' y el estilo visual de la plantilla.

Los veredictos de ejecución y los hallazgos observados se cargan desde
execution_results.json cuando existe (se completa tras la corrida real en
ParaBank); si no existe, la hoja 'Ejecución' queda con veredicto 'Pendiente'.
"""
from __future__ import annotations

import json
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = Path("/Users/gianpier/Downloads/Plantilla_Matriz_Casos_de_Prueba-1.xlsx")
OUTPUT = ROOT / "output" / "matriz" / "Proyecto1_Caso1_Matriz_Casos_de_Prueba.xlsx"
RESULTS = ROOT / "output" / "matriz" / "execution_results.json"

HEADER_FILL = PatternFill("solid", fgColor="1F4E78")
WHITE_FILL = PatternFill("solid", fgColor="FFFFFF")
ZEBRA_FILL = PatternFill("solid", fgColor="F7F9FC")
HEADER_FONT = Font(name="Arial", size=11, bold=True, color="FFFFFF")
CELL_FONT = Font(name="Arial", size=10, color="1D1D1F")
ID_FONT = Font(name="Arial", size=10, bold=True, color="1D1D1F")
THIN = Side(style="thin", color="D9D9DE")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
TOP_WRAP = Alignment(vertical="top", wrap_text=True)
CENTER_WRAP = Alignment(vertical="center", wrap_text=True)

# ---------------------------------------------------------------------------
# Diseño de casos de prueba (18 casos, 6 funcionalidades, 9 de prioridad Alta)
# Columnas: ID, Funcionalidad, RF, Prioridad, Técnica, Precondiciones, Pasos,
#           Datos de Prueba, Resultado Esperado
# ---------------------------------------------------------------------------
CASES = [
    # --- F-01 Registro y login ---
    ["CP-01", "Registro de cliente", "RF-01", "Media", "Partición de equivalencia",
     "El nombre de usuario elegido no está registrado.",
     "1. Abrir Register.\n2. Completar todos los campos obligatorios con datos ficticios válidos.\n3. Enviar el formulario.",
     "Usuario: gsegovia.qa.<sufijo>; contraseña válida; datos ficticios coherentes.",
     "La cuenta se crea y el sistema muestra la confirmación de registro e inicia sesión."],
    ["CP-02", "Registro de cliente", "RF-02", "Alta", "Partición de equivalencia",
     "Ya existe una cuenta con el nombre de usuario a reutilizar.",
     "1. Abrir Register.\n2. Ingresar un nombre de usuario ya registrado.\n3. Completar el resto con datos válidos.\n4. Enviar.",
     "Usuario duplicado (ej. el creado en CP-01); resto de datos válidos.",
     "El registro es rechazado con un mensaje de 'usuario ya en uso' y no se crea una segunda cuenta."],
    ["CP-03", "Login de cliente", "RF-03", "Alta", "Partición de equivalencia",
     "Existe una cuenta de prueba registrada.",
     "1. Abrir la página de inicio.\n2. Probar usuario válido + contraseña incorrecta.\n3. Probar usuario inexistente.\n4. Enviar cada intento.",
     "Usuario válido + clave incorrecta; usuario inexistente + cualquier clave.",
     "La sesión no se inicia en ningún intento y se muestra un mensaje de error claro."],
    ["CP-04", "Login de cliente", "RF-04", "Media", "Transición de estados",
     "Cuenta de prueba activa; sesión cerrada (estado no autenticado).",
     "1. Ingresar usuario y contraseña válidos.\n2. Enviar.\n3. Observar el cambio de estado.",
     "Usuario y contraseña válidos de la cuenta de CP-01.",
     "El sistema transita a estado autenticado y muestra el Accounts Overview con las operaciones disponibles."],
    # --- F-02 Apertura de cuentas ---
    ["CP-05", "Apertura de nuevas cuentas", "RF-05", "Alta", "Tabla de decisión",
     "Cliente autenticado con al menos una cuenta de fondeo con saldo.",
     "1. Abrir Open New Account.\n2. Seleccionar tipo SAVINGS.\n3. Seleccionar una cuenta de fondeo válida.\n4. Enviar.",
     "Tipo: Savings; cuenta de fondeo existente del cliente.",
     "La nueva cuenta se crea, se muestra su número y aparece en el Accounts Overview."],
    ["CP-06", "Apertura de nuevas cuentas", "RF-06", "Alta", "Tabla de decisión",
     "Cliente autenticado.",
     "1. Abrir Open New Account.\n2. Dejar sin seleccionar tipo y/o cuenta de fondeo.\n3. Intentar enviar.",
     "Combinaciones: tipo vacío, fondeo vacío, ambos vacíos.",
     "La cuenta no se crea; el sistema impide continuar o solicita completar los datos faltantes."],
    ["CP-07", "Apertura de nuevas cuentas", "RF-07", "Media", "Transición de estados",
     "Se completó una apertura de cuenta (CP-05).",
     "1. Volver a Accounts Overview.\n2. Ubicar la cuenta recién creada.\n3. Verificar número, tipo y saldo inicial.",
     "Cuenta creada en CP-05.",
     "La cuenta aparece con su número, tipo y saldo inicial visibles y consistentes."],
    # --- F-03 Transferencias ---
    ["CP-08", "Transferencia entre cuentas propias", "RF-08", "Alta", "Tabla de decisión",
     "Dos cuentas propias con saldos conocidos y saldo suficiente en origen.",
     "1. Registrar saldos iniciales.\n2. Abrir Transfer Funds.\n3. Monto 100.00, origen y destino distintos.\n4. Enviar.\n5. Verificar saldos e historial.",
     "Monto: 100.00; origen y destino distintos.",
     "El origen se debita 100.00, el destino se acredita 100.00 y la operación queda en el historial."],
    ["CP-09", "Transferencia entre cuentas propias", "RF-09", "Alta", "Análisis de valores límite",
     "Cuenta de origen con saldo conocido.",
     "1. Registrar saldo de origen.\n2. Abrir Transfer Funds.\n3. Ingresar monto = saldo + 0.01.\n4. Enviar.\n5. Verificar saldos.",
     "Monto = saldo disponible + 0.01.",
     "La transferencia se rechaza y ningún saldo cambia."],
    ["CP-10", "Transferencia entre cuentas propias", "RF-10", "Media", "Análisis de valores límite",
     "Cliente autenticado con dos cuentas propias.",
     "1. Abrir Transfer Funds.\n2. Probar monto 0.00, luego -1.00.\n3. Probar origen = destino.\n4. Enviar cada caso.",
     "Montos 0.00 y -1.00; origen igual a destino.",
     "El sistema rechaza cada entrada inválida con una validación comprensible y sin alterar saldos."],
    # --- F-04 Bill Pay ---
    ["CP-11", "Pago de servicios (Bill Pay)", "RF-11", "Alta", "Tabla de decisión",
     "Cuenta con saldo suficiente.",
     "1. Registrar saldo.\n2. Abrir Bill Pay.\n3. Completar beneficiario, dirección, cuenta y monto 25.00 válidos.\n4. Enviar.\n5. Verificar saldo e historial.",
     "Beneficiario ficticio completo; cuenta propia; monto: 25.00.",
     "El pago se confirma, descuenta 25.00 de la cuenta y registra una operación consultable."],
    ["CP-12", "Pago de servicios (Bill Pay)", "RF-12", "Alta", "Partición de equivalencia",
     "Cliente autenticado.",
     "1. Abrir Bill Pay.\n2. Omitir por iteración nombre, dirección, cuenta o monto.\n3. Probar monto no numérico.\n4. Enviar cada caso.",
     "Un campo obligatorio vacío por iteración; monto no numérico ('abc').",
     "El pago no se procesa y el sistema identifica el dato faltante o inválido."],
    ["CP-13", "Pago de servicios (Bill Pay)", "RF-13", "Alta", "Análisis de valores límite",
     "Cuenta con saldo conocido.",
     "1. Registrar saldo.\n2. Abrir Bill Pay.\n3. Completar beneficiario válido.\n4. Ingresar monto = saldo + 0.01.\n5. Enviar.",
     "Monto = saldo disponible + 0.01.",
     "El pago se rechaza y el saldo de la cuenta permanece sin cambios."],
    # --- F-05 Búsqueda de transacciones ---
    ["CP-14", "Búsqueda de transacciones", "RF-14", "Media", "Análisis de valores límite",
     "Existen transacciones de prueba (generadas en CP-08/CP-11).",
     "1. Abrir Find Transactions.\n2. Buscar por fecha exacta de una operación.\n3. Buscar por rango con inicio <= fin.\n4. Probar rango con fin anterior al inicio.",
     "Fecha exacta conocida; rango válido; rango invertido.",
     "Se listan solo las transacciones que cumplen el filtro; el rango inválido no muestra resultados incoherentes."],
    ["CP-15", "Búsqueda de transacciones", "RF-15", "Media", "Partición de equivalencia",
     "Existe una transacción con monto e ID conocidos.",
     "1. Abrir Find Transactions.\n2. Buscar por monto exacto existente.\n3. Buscar por ID de transacción existente.\n4. Repetir con valores sin coincidencia.",
     "Monto e ID existentes; valores inexistentes.",
     "Se muestra la operación coincidente, o un mensaje de que no existen resultados."],
    # --- F-06 Actualización de perfil ---
    ["CP-16", "Actualización de datos de contacto", "RF-16", "Media", "Partición de equivalencia",
     "Cliente autenticado.",
     "1. Abrir Update Contact Info.\n2. Modificar teléfono y dirección con valores válidos.\n3. Guardar.\n4. Volver a abrir el perfil.",
     "Teléfono y dirección ficticios válidos.",
     "El sistema confirma la actualización y los datos persisten en el perfil."],
    # --- F-07 Préstamos ---
    ["CP-17", "Solicitud de préstamos", "RF-18", "Media", "Tabla de decisión",
     "Cliente autenticado con una cuenta de fondeo.",
     "1. Abrir Request Loan.\n2. Ingresar monto y down payment que cumplan la regla.\n3. Enviar.",
     "Monto de préstamo válido; down payment >= umbral.",
     "La solicitud muestra un resultado de aprobación explícito."],
    ["CP-18", "Solicitud de préstamos", "RF-19", "Media", "Análisis de valores límite",
     "Cliente autenticado.",
     "1. Abrir Request Loan.\n2. Ingresar down payment inmediatamente inferior al umbral.\n3. Enviar.",
     "Down payment = umbral - mínima unidad.",
     "La solicitud muestra un resultado de rechazo y no se presenta como aprobada."],
]

HIGH_CASES = [c for c in CASES if c[3] == "Alta"]


def style_header(ws, ncols):
    for col in range(1, ncols + 1):
        cell = ws.cell(row=1, column=col)
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = CENTER_WRAP
        cell.border = BORDER


def clear_rows(ws, start=2):
    if ws.max_row >= start:
        ws.delete_rows(start, ws.max_row - start + 1)


def write_row(ws, r, values, fill):
    for c, val in enumerate(values, start=1):
        cell = ws.cell(row=r, column=c, value=val)
        cell.font = ID_FONT if c == 1 else CELL_FONT
        cell.fill = fill
        cell.alignment = TOP_WRAP
        cell.border = BORDER


def build_cases_sheet(ws):
    style_header(ws, 9)
    clear_rows(ws)
    for i, case in enumerate(CASES):
        r = i + 2
        write_row(ws, r, case, WHITE_FILL if i % 2 == 0 else ZEBRA_FILL)
        ws.row_dimensions[r].height = 74
    ws.freeze_panes = "A2"


def build_execution_sheet(ws, results):
    # Columnas: ID Caso, Resultado Esperado, Resultado Obtenido, Veredicto, Evidencia, Observaciones
    style_header(ws, 6)
    clear_rows(ws)
    for i, case in enumerate(HIGH_CASES):
        cid = case[0]
        expected = case[8]
        res = results.get(cid, {})
        row = [
            cid,
            expected,
            res.get("obtained", "Pendiente de ejecución en ParaBank."),
            res.get("verdict", "Pendiente"),
            res.get("evidence", ""),
            res.get("notes", ""),
        ]
        r = i + 2
        write_row(ws, r, row, WHITE_FILL if i % 2 == 0 else ZEBRA_FILL)
        ws.row_dimensions[r].height = 56
    ws.freeze_panes = "A2"


def build_findings_sheet(ws, findings):
    # Columnas: ID, Título, Resumen, Pasos para Reproducir, Resultado Esperado, Resultado Obtenido, Severidad / Prioridad, Evidencia
    style_header(ws, 8)
    clear_rows(ws)
    if not findings:
        ws.cell(row=2, column=1, value="Pendiente")
        ws.cell(row=2, column=2,
                value="Los hallazgos se registrarán tras la ejecución manual de los casos de prioridad alta en ParaBank.")
        for c in range(1, 9):
            cell = ws.cell(row=2, column=c)
            cell.font = CELL_FONT
            cell.fill = WHITE_FILL
            cell.alignment = TOP_WRAP
            cell.border = BORDER
        return
    for i, f in enumerate(findings):
        r = i + 2
        row = [f.get(k, "") for k in
               ("id", "title", "summary", "steps", "expected", "obtained", "severity", "evidence")]
        write_row(ws, r, row, WHITE_FILL if i % 2 == 0 else ZEBRA_FILL)
        ws.row_dimensions[r].height = 70
    ws.freeze_panes = "A2"


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    results, findings = {}, []
    if RESULTS.exists():
        payload = json.loads(RESULTS.read_text(encoding="utf-8"))
        results = payload.get("execution", {})
        findings = payload.get("findings", [])

    wb = openpyxl.load_workbook(TEMPLATE)
    build_cases_sheet(wb["Casos de Prueba"])
    build_execution_sheet(wb["Ejecución"], results)
    build_findings_sheet(wb["Hallazgos"], findings)
    wb.save(OUTPUT)

    print(json.dumps({
        "output": str(OUTPUT),
        "cases": len(CASES),
        "high_priority_cases": len(HIGH_CASES),
        "executed": len(results),
        "findings": len(findings),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
