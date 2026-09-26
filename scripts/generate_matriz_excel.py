"""Genera la Matriz de Casos de Prueba (ParaBank) sobre la plantilla oficial.

Rellena las hojas 'Casos de Prueba', 'Ejecución' y 'Hallazgos' con el diseño
del Caso 1 (ParaBank), mapeado a los 36 RF del primer avance. Conserva la hoja
'Instrucciones' y el estilo visual de la plantilla.

Los veredictos de ejecución y los hallazgos observados se cargan desde
execution_results.json cuando existe (se completa tras la corrida real en
ParaBank); si no existe, la hoja 'Ejecución' queda con veredicto 'Pendiente'.
"""
from __future__ import annotations

import json
from pathlib import Path

import openpyxl
from openpyxl.drawing.image import Image as XLImage
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = Path("/Users/gianpier/Downloads/Plantilla_Matriz_Casos_de_Prueba-1.xlsx")
OUTPUT = ROOT / "output" / "matriz" / "Proyecto1_Caso1_Matriz_Casos_de_Prueba.xlsx"
RESULTS = ROOT / "output" / "matriz" / "execution_results.json"
EVIDENCE_DIR = ROOT / "output" / "evidencia"

# Miniatura de evidencia incrustada (px). Los 2:1 de ParaBank -> 380x190.
THUMB_W, THUMB_H = 380, 190

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
# Diseño de casos de prueba (62 casos, 8 funcionalidades, múltiples casos por RF)
# Columnas: ID, Funcionalidad, RF, Prioridad, Técnica, Precondiciones, Pasos,
#           Datos de Prueba, Resultado Esperado
# ---------------------------------------------------------------------------
CASES = [
    # --- F-01 Registro y login de clientes ---
    ["CP-01", "Registro de cliente", "RF-01", "Media", "Partición de equivalencia",
     "El nombre de usuario elegido no está registrado.",
     "1. Abrir Register.\n2. Completar todos los campos obligatorios con datos ficticios válidos.\n3. Enviar el formulario.",
     "Usuario: gsegovia.qa.<sufijo>; contraseña válida; datos ficticios coherentes.",
     "La cuenta se crea y el sistema muestra la confirmación de registro e inicia sesión."],
    ["CP-19", "Registro de cliente", "RF-01", "Alta", "Partición de equivalencia",
     "Formulario de registro abierto sin sesión activa.",
     "1. Abrir Register.\n2. Completar nombre y apellido pero omitir SSN, nombre de usuario y contraseña.\n3. Enviar el formulario.",
     "First Name: Carlos, Last Name: Gómez; SSN, Username y Password vacíos.",
     "El registro es bloqueado, no se crea la cuenta y el sistema muestra alertas de campos obligatorios requeridos."],
    ["CP-20", "Registro de cliente", "RF-01", "Alta", "Tabla de decisión",
     "Formulario de registro disponible.",
     "1. Abrir Register.\n2. Completar campos personales con datos válidos.\n3. Ingresar contraseña 'Clave123' y en confirmación 'ClaveDistinta456'.\n4. Enviar.",
     "Password: 'Clave123', Confirm: 'ClaveDistinta456'.",
     "El registro se rechaza alertando que las contraseñas no coinciden ('Passwords did not match') y no crea el usuario."],
    ["CP-02", "Registro de cliente", "RF-02", "Alta", "Partición de equivalencia",
     "Ya existe una cuenta con el nombre de usuario a reutilizar.",
     "1. Abrir Register.\n2. Ingresar un nombre de usuario ya registrado.\n3. Completar el resto con datos válidos.\n4. Enviar.",
     "Usuario duplicado (ej. el creado en CP-01); resto de datos válidos.",
     "El registro es rechazado con un mensaje de 'usuario ya en uso' y no se crea una segunda cuenta."],
    ["CP-21", "Registro de cliente", "RF-02", "Media", "Partición de equivalencia",
     "Existe una cuenta registrada con el usuario en minúsculas.",
     "1. Abrir Register.\n2. Ingresar en usuario el mismo nombre existente pero todo en mayúsculas.\n3. Completar datos válidos y enviar.",
     "Username: versión en mayúsculas de cuenta existente; resto de campos válidos.",
     "El sistema rechaza el intento identificando colisión de identidad, manteniendo unicidad insensible a mayúsculas."],
    ["CP-03", "Login de cliente", "RF-03", "Alta", "Partición de equivalencia",
     "Existe una cuenta de prueba registrada.",
     "1. Abrir la página de inicio.\n2. Probar usuario válido + contraseña incorrecta.\n3. Probar usuario inexistente.\n4. Enviar cada intento.",
     "Usuario válido + clave incorrecta; usuario inexistente + cualquier clave.",
     "La sesión no se inicia en ningún intento y se muestra un mensaje de error claro."],
    ["CP-22", "Login de cliente", "RF-03", "Alta", "Partición de equivalencia",
     "Portal en estado no autenticado.",
     "1. Abrir página de inicio.\n2. Dejar campos de usuario y contraseña vacíos.\n3. Clic en Log In.\n4. Probar luego usuario con valor y contraseña vacía.\n5. Clic en Log In.",
     "Intento 1: usuario '', clave ''; Intento 2: usuario 'gsegovia_qa_5821', clave ''.",
     "El sistema bloquea el acceso en ambos casos y muestra mensaje de validación de credenciales requeridas."],
    ["CP-04", "Login de cliente", "RF-04", "Media", "Transición de estados",
     "Cuenta de prueba activa; sesión cerrada (estado no autenticado).",
     "1. Ingresar usuario y contraseña válidos.\n2. Enviar.\n3. Observar el cambio de estado.",
     "Usuario y contraseña válidos de la cuenta de CP-01.",
     "El sistema transita a estado autenticado y muestra el Accounts Overview con las operaciones disponibles."],
    ["CP-23", "Login de cliente", "RF-04", "Media", "Transición de estados",
     "Cliente con sesión activa en el portal.",
     "1. Navegar por 'Open New Account', 'Transfer Funds', 'Bill Pay' y volver a 'Accounts Overview'.\n2. Comprobar que en ninguna pantalla se pierda la sesión ni pida volver a autenticarse.",
     "Navegación interna entre pantallas privadas.",
     "La sesión permanece activa de manera continua y el menú superior conserva el saludo al usuario y la opción Log Out."],
    ["CP-24", "Registro y login de clientes", "RF-23", "Alta", "Transición de estados",
     "Cliente con sesión autenticada activa.",
     "1. Hacer clic en 'Log Out'.\n2. Verificar redirección a página de inicio pública.\n3. Intentar volver atrás con el botón 'Atrás' del navegador o ingresar por URL directa a /overview.htm.",
     "Sesión activa cerrada mediante Log Out.",
     "La sesión se destruye, la página principal muestra el formulario de login y cualquier intento de navegar atrás o acceder a URL interna solicita credenciales."],
    ["CP-25", "Registro y login de clientes", "RF-24", "Media", "Partición de equivalencia",
     "Cliente registrado previamente en el sistema.",
     "1. En la página de login, hacer clic en 'Forgot login info?'.\n2. Ingresar nombre, apellido, dirección, ciudad, estado, zip y SSN del cliente registrado.\n3. Clic en 'Find My Login Info'.",
     "Datos personales exactos del cliente registrado.",
     "El sistema valida la información personal y muestra en pantalla el Username y la Password correspondientes a la cuenta."],
    ["CP-26", "Registro y login de clientes", "RF-24", "Media", "Partición de equivalencia",
     "Pantalla Customer Lookup abierta.",
     "1. Ingresar datos personales ficticios o no registrados en el sistema.\n2. Clic en 'Find My Login Info'.",
     "First Name: 'Inexistente', SSN: '000-00-0000', resto datos ficticios.",
     "El sistema no revela credenciales y muestra un mensaje indicando que no se pudo encontrar un cliente con esos datos."],

    # --- F-02 Apertura de nuevas cuentas ---
    ["CP-05", "Apertura de nuevas cuentas", "RF-05", "Alta", "Tabla de decisión",
     "Cliente autenticado con al menos una cuenta de fondeo con saldo.",
     "1. Abrir Open New Account.\n2. Seleccionar tipo SAVINGS.\n3. Seleccionar una cuenta de fondeo válida.\n4. Enviar.",
     "Tipo: Savings; cuenta de fondeo existente del cliente.",
     "La nueva cuenta se crea, se muestra su número y aparece en el Accounts Overview."],
    ["CP-27", "Apertura de nuevas cuentas", "RF-05", "Alta", "Tabla de decisión",
     "Cliente autenticado con cuenta de fondeo con saldo disponible.",
     "1. Abrir Open New Account.\n2. Seleccionar tipo CHECKING.\n3. Seleccionar cuenta de fondeo con saldo disponible.\n4. Enviar formulario.",
     "Tipo: Checking; cuenta de fondeo válida con saldo.",
     "Se genera una nueva cuenta corriente (CHECKING) con nuevo número de cuenta y saldo inicial acreditado."],
    ["CP-06", "Apertura de nuevas cuentas", "RF-06", "Alta", "Tabla de decisión",
     "Cliente autenticado.",
     "1. Abrir Open New Account.\n2. Dejar sin seleccionar tipo y/o cuenta de fondeo.\n3. Intentar enviar.",
     "Combinaciones: tipo vacío, fondeo vacío, ambos vacíos.",
     "La cuenta no se crea; el sistema impide continuar o solicita completar los datos faltantes."],
    ["CP-07", "Apertura de nuevas cuentas", "RF-07", "Media", "Transición de estados",
     "Se completó una apertura de cuenta (CP-05 / CP-27).",
     "1. Volver a Accounts Overview.\n2. Ubicar la cuenta recién creada.\n3. Verificar número, tipo y saldo inicial.",
     "Cuenta creada en CP-05 / CP-27.",
     "La cuenta aparece con su número, tipo y saldo inicial visibles y consistentes con la confirmación."],
    ["CP-28", "Apertura de nuevas cuentas", "RF-25", "Alta", "Pruebas de caso de uso",
     "Cuenta de fondeo con saldo inicial conocido (ej. $500.00).",
     "1. Registrar saldo inicial de la cuenta de fondeo.\n2. Abrir Open New Account y crear una cuenta fondeada con dicha cuenta.\n3. Comprobar saldos finales en Accounts Overview.",
     "Saldo mínimo configurado para depósito inicial (ej. $100.00).",
     "La cuenta de fondeo se debita exactamente por el monto del saldo mínimo asignado a la nueva cuenta, preservando el balance total."],
    ["CP-29", "Apertura de nuevas cuentas", "RF-26", "Baja", "Partición de equivalencia",
     "Cliente posee al menos una cuenta Checking y una cuenta Savings.",
     "1. Abrir Accounts Overview.\n2. Comprobar la columna de tipo o descripción de cada cuenta.\n3. Abrir la vista de detalle de cada una.",
     "Cuentas existentes de tipo Checking y Savings.",
     "El sistema diferencia claramente el tipo de producto financiero de cada cuenta (CHECKING / SAVINGS) tanto en el listado como en su detalle."],

    # --- F-03 Transferencia entre cuentas propias ---
    ["CP-08", "Transferencia entre cuentas propias", "RF-08", "Alta", "Tabla de decisión",
     "Dos cuentas propias con saldos conocidos y saldo suficiente en origen.",
     "1. Registrar saldos iniciales.\n2. Abrir Transfer Funds.\n3. Monto 100.00, origen y destino distintos.\n4. Enviar.\n5. Verificar saldos e historial.",
     "Monto: 100.00; origen y destino distintos.",
     "El origen se debita 100.00, el destino se acredita 100.00 y la operación queda en el historial."],
    ["CP-30", "Transferencia entre cuentas propias", "RF-08", "Alta", "Análisis de valores límite",
     "Cuenta origen con saldo disponible exacto S (ej. $200.00) y destino distinta.",
     "1. Registrar saldo origen S ($200.00) y saldo destino D.\n2. Abrir Transfer Funds.\n3. Ingresar monto exactamente igual al saldo disponible S ($200.00).\n4. Enviar y verificar saldos.",
     "Monto = $200.00 (límite superior válido del 100% del saldo).",
     "La transferencia se completa con éxito; la cuenta origen queda con saldo exacto de $0.00 y la cuenta destino se incrementa en $200.00."],
    ["CP-31", "Transferencia entre cuentas propias", "RF-08", "Media", "Análisis de valores límite",
     "Cuenta origen con saldo suficiente y cuenta destino distinta.",
     "1. Abrir Transfer Funds.\n2. Ingresar monto de 0.01.\n3. Seleccionar cuentas origen y destino distintas.\n4. Enviar.\n5. Verificar saldos.",
     "Monto = 0.01 (límite inferior válido).",
     "La transferencia se procesa exitosamente debitando 0.01 del origen y acreditando 0.01 en destino."],
    ["CP-09", "Transferencia entre cuentas propias", "RF-09", "Alta", "Análisis de valores límite",
     "Cuenta de origen con saldo conocido.",
     "1. Registrar saldo de origen.\n2. Abrir Transfer Funds.\n3. Ingresar monto = saldo + 0.01.\n4. Enviar.\n5. Verificar saldos.",
     "Monto = saldo disponible + 0.01.",
     "La transferencia se rechaza y ningún saldo cambia."],
    ["CP-32", "Transferencia entre cuentas propias", "RF-09", "Alta", "Partición de equivalencia",
     "Cuenta origen con saldo disponible de $300.00.",
     "1. Abrir Transfer Funds.\n2. Ingresar monto sustancialmente superior ($50,000.00) sobre saldo de $300.00.\n3. Enviar formulario.",
     "Monto = $50,000.00.",
     "El sistema bloquea la transacción informando saldo insuficiente y previene cualquier sobregiro."],
    ["CP-10", "Transferencia entre cuentas propias", "RF-10", "Media", "Análisis de valores límite",
     "Cliente autenticado con dos cuentas propias.",
     "1. Abrir Transfer Funds.\n2. Probar monto 0.00, luego -1.00.\n3. Probar origen = destino.\n4. Enviar cada caso.",
     "Montos 0.00 y -1.00; origen igual a destino.",
     "El sistema rechaza cada entrada inválida con una validación comprensible y sin alterar saldos."],
    ["CP-33", "Transferencia entre cuentas propias", "RF-10", "Media", "Tabla de decisión",
     "Cliente autenticado con al menos una cuenta activa.",
     "1. Abrir Transfer Funds.\n2. Seleccionar la misma cuenta en 'From account' y en 'To account'.\n3. Ingresar monto válido ($50.00).\n4. Enviar.",
     "From: 28662, To: 28662, Monto: $50.00.",
     "El sistema impide la transferencia hacia la misma cuenta emitiendo una validación explícita o bloqueando la selección repetida."],
    ["CP-34", "Transferencia entre cuentas propias", "RF-10", "Media", "Partición de equivalencia",
     "Cliente autenticado con dos cuentas propias.",
     "1. Abrir Transfer Funds.\n2. Ingresar caracteres alfabéticos o símbolos ('cien_dolares', '#@%') en Amount.\n3. Enviar.",
     "Monto: 'cien_dolares'.",
     "El formulario rechaza el envío requiriendo un formato numérico válido y no ejecuta la transacción."],
    ["CP-35", "Transferencia entre cuentas propias", "RF-27", "Media", "Pruebas de caso de uso",
     "Transferencia válida procesada entre dos cuentas propias (CP-08).",
     "1. Abrir 'Account Activity' de la cuenta origen y verificar registro de débito.\n2. Abrir 'Account Activity' de la cuenta destino y verificar crédito.\n3. Comparar fechas y montos.",
     "Transferencia de $100.00 entre cuentas propias.",
     "La cuenta origen registra un débito de $100.00 y la destino un crédito de $100.00 con la misma fecha y descripción consistente."],
    ["CP-36", "Transferencia entre cuentas propias", "RF-28", "Media", "Pruebas de caso de uso",
     "Datos de transferencia válidos enviados.",
     "1. Enviar transferencia válida desde Transfer Funds.\n2. Inspeccionar la pantalla de confirmación resultante.",
     "Origen: 28662, Destino: 28773, Monto: $100.00.",
     "Se despliega 'Transfer Complete!' especificando de manera legible el monto transferido, el número de cuenta debitada y la cuenta acreditada."],

    # --- F-04 Pago de servicios (Bill Pay) ---
    ["CP-11", "Pago de servicios (Bill Pay)", "RF-11", "Alta", "Tabla de decisión",
     "Cuenta con saldo suficiente.",
     "1. Registrar saldo.\n2. Abrir Bill Pay.\n3. Completar beneficiario, dirección, cuenta y monto 25.00 válidos.\n4. Enviar.\n5. Verificar saldo e historial.",
     "Beneficiario ficticio completo; cuenta propia; monto: 25.00.",
     "El pago se confirma, descuenta 25.00 de la cuenta y registra una operación consultable."],
    ["CP-37", "Pago de servicios (Bill Pay)", "RF-11", "Alta", "Análisis de valores límite",
     "Cuenta con saldo conocido S ($150.00).",
     "1. Abrir Bill Pay.\n2. Completar beneficiario válido.\n3. Ingresar Amount igual al saldo disponible ($150.00).\n4. Enviar y comprobar saldo e historial.",
     "Monto = $150.00 sobre saldo $150.00.",
     "El pago se efectúa exitosamente, debita $150.00 dejando el saldo en $0.00 sin errores en el sistema."],
    ["CP-12", "Pago de servicios (Bill Pay)", "RF-12", "Alta", "Partición de equivalencia",
     "Cliente autenticado.",
     "1. Abrir Bill Pay.\n2. Omitir por iteración nombre, dirección, cuenta o monto.\n3. Probar monto no numérico.\n4. Enviar cada caso.",
     "Un campo obligatorio vacío por iteración; monto no numérico ('abc').",
     "El pago no se procesa y el sistema identifica el dato faltante o inválido."],
    ["CP-38", "Pago de servicios (Bill Pay)", "RF-12", "Alta", "Análisis de valores límite",
     "Cliente autenticado en pantalla Bill Pay.",
     "1. Abrir Bill Pay.\n2. Completar beneficiario y cuenta válidos.\n3. Ingresar monto 0.00 y enviar.\n4. Ingresar monto -20.00 y enviar.",
     "Montos 0.00 y -20.00.",
     "El sistema no procesa el pago y notifica que el importe a pagar debe ser mayor a cero."],
    ["CP-39", "Pago de servicios (Bill Pay)", "RF-12", "Media", "Partición de equivalencia",
     "Formulario Bill Pay abierto.",
     "1. Ingresar caracteres alfabéticos o símbolos en el campo Account y Verify Account.\n2. Completar resto con datos válidos.\n3. Enviar.",
     "Account: 'ABC-99', Verify: 'ABC-99'.",
     "El sistema valida que el número de cuenta sea numérico y no permite procesar datos alfanuméricos inconsistentes."],
    ["CP-13", "Pago de servicios (Bill Pay)", "RF-13", "Alta", "Análisis de valores límite",
     "Cuenta con saldo conocido.",
     "1. Registrar saldo.\n2. Abrir Bill Pay.\n3. Completar beneficiario válido.\n4. Ingresar monto = saldo + 0.01.\n5. Enviar.",
     "Monto = saldo disponible + 0.01.",
     "El pago se rechaza y el saldo de la cuenta permanece sin cambios."],
    ["CP-40", "Pago de servicios (Bill Pay)", "RF-13", "Alta", "Análisis de valores límite",
     "Cuenta con saldo disponible exacto S ($250.00).",
     "1. Abrir Bill Pay.\n2. Ingresar datos de beneficiario válidos.\n3. Ingresar monto S + 0.01 ($250.01).\n4. Enviar.",
     "Monto = $250.01 sobre saldo $250.00.",
     "El sistema rechaza la operación por insuficiencia de fondos de forma controlada sin fallos de servidor."],
    ["CP-41", "Pago de servicios (Bill Pay)", "RF-29", "Alta", "Tabla de decisión",
     "Formulario de Bill Pay abierto.",
     "1. Ingresar en Account el valor '13579'.\n2. Ingresar en Verify Account el valor '97531' (discrepancia deliberada).\n3. Completar beneficiario y monto válidos.\n4. Enviar.",
     "Account: '13579', Verify Account: '97531'.",
     "El pago no se envía y se muestra un mensaje de validación indicando que los números de cuenta no coinciden."],
    ["CP-42", "Pago de servicios (Bill Pay)", "RF-29", "Alta", "Tabla de decisión",
     "Formulario de Bill Pay abierto con saldo suficiente.",
     "1. Ingresar en Account '13579' y en Verify Account '13579'.\n2. Completar todos los datos válidos y monto $40.00.\n3. Enviar.",
     "Account: '13579', Verify Account: '13579'.",
     "La validación de confirmación de cuenta es superada y la orden de pago procede a ser tramitada."],
    ["CP-43", "Pago de servicios (Bill Pay)", "RF-30", "Media", "Pruebas de caso de uso",
     "Envío de un pago de servicios válido.",
     "1. Completar y enviar un pago de servicios válido.\n2. Revisar la pantalla 'Bill Payment Complete'.",
     "Beneficiario 'Luz del Sur', Monto $25.00, Cuenta origen 28773.",
     "La pantalla confirma el pago mostrando el nombre del beneficiario, el monto debitado y el número de cuenta de débito de forma legible."],

    # --- F-05 Búsqueda de transacciones ---
    ["CP-14", "Búsqueda de transacciones", "RF-14", "Media", "Análisis de valores límite",
     "Existen transacciones de prueba (generadas en CP-08/CP-11).",
     "1. Abrir Find Transactions.\n2. Buscar por fecha exacta de una operación.\n3. Buscar por rango con inicio <= fin.\n4. Probar rango con fin anterior al inicio.",
     "Fecha exacta conocida; rango válido; rango invertido.",
     "Se listan solo las transacciones que cumplen el filtro; el rango inválido no muestra resultados incoherentes."],
    ["CP-44", "Búsqueda de transacciones", "RF-14", "Media", "Análisis de valores límite",
     "Cuenta seleccionada en Find Transactions.",
     "1. Abrir Find Transactions.\n2. En 'Find by Date Range', seleccionar fecha inicial posterior a la final (ej. inicio 30/09/2026, fin 01/09/2026).\n3. Clic en Find Transactions.",
     "Desde: 30/09/2026, Hasta: 01/09/2026.",
     "El sistema valida que el rango de fechas sea coherente y no arroja resultados erróneos ni excepciones no controladas."],
    ["CP-45", "Búsqueda de transacciones", "RF-14", "Baja", "Partición de equivalencia",
     "Formulario Find Transactions abierto.",
     "1. Ingresar en el campo fecha el valor 'fecha_invalida' o '2026/99/99'.\n2. Enviar búsqueda.",
     "Fecha: 'fecha_invalida'.",
     "El sistema valida el formato de fecha requerido y solicita un valor válido sin fallar internamente."],
    ["CP-15", "Búsqueda de transacciones", "RF-15", "Media", "Partición de equivalencia",
     "Existe una transacción con monto e ID conocidos.",
     "1. Abrir Find Transactions.\n2. Buscar por monto exacto existente.\n3. Buscar por ID de transacción existente.\n4. Repetir con valores sin coincidencia.",
     "Monto e ID existentes; valores inexistentes.",
     "Se muestra la operación coincidente, o un mensaje de que no existen resultados."],
    ["CP-46", "Búsqueda de transacciones", "RF-15", "Media", "Partición de equivalencia",
     "Existe transacción por monto con centavos (ej. $325.51).",
     "1. Abrir Find Transactions.\n2. Ingresar en 'Find by Amount' el importe 325.51.\n3. Enviar.",
     "Monto: 325.51.",
     "La búsqueda ubica y lista con precisión la transacción que coincide con el importe exacto con decimales."],
    ["CP-47", "Búsqueda de transacciones", "RF-31", "Media", "Pruebas de caso de uso",
     "Lista de resultados de búsqueda con al menos una transacción visible.",
     "1. En la lista de resultados, hacer clic en el enlace del ID de la transacción.\n2. Verificar los datos de la vista Transaction Details.",
     "Transacción listada en resultados.",
     "Se despliega la página de detalle con ID, fecha, tipo de movimiento, descripción y monto correspondiente."],
    ["CP-48", "Búsqueda de transacciones", "RF-32", "Baja", "Partición de equivalencia",
     "Cuenta seleccionada en Find Transactions.",
     "1. Buscar por ID de transacción '88888888'.\n2. Observar la pantalla resultante.",
     "ID inexistente: 88888888.",
     "El sistema muestra de manera explícita que no se encontraron transacciones para ese criterio, sin mostrar tablas vacías ambiguas ni errores."],

    # --- F-06 Actualización de datos de contacto ---
    ["CP-16", "Actualización de datos de contacto", "RF-16", "Media", "Partición de equivalencia",
     "Cliente autenticado.",
     "1. Abrir Update Contact Info.\n2. Modificar teléfono y dirección con valores válidos.\n3. Guardar.\n4. Volver a abrir el perfil.",
     "Teléfono y dirección ficticios válidos.",
     "El sistema confirma la actualización y los datos persisten en el perfil."],
    ["CP-49", "Actualización de datos de contacto", "RF-16", "Media", "Pruebas de caso de uso",
     "Cliente autenticado en portal.",
     "1. Abrir Update Contact Info.\n2. Modificar simultáneamente nombre, apellido, dirección, ciudad, estado, código postal y teléfono con nuevos datos válidos.\n3. Guardar y recargar.",
     "Datos válidos completos actualizados.",
     "El sistema actualiza satisfactoriamente la totalidad de los datos y se reflejan en el saludo y en el perfil del cliente."],
    ["CP-50", "Actualización de datos de contacto", "RF-17", "Baja", "Partición de equivalencia",
     "Formulario Update Contact Info abierto.",
     "1. Borrar el contenido de First Name y Address dejando los campos vacíos.\n2. Clic en 'Update Profile'.\n3. Observar si permite guardar.",
     "First Name: '', Address: ''.",
     "El sistema rechaza la actualización solicitando ingresar los datos requeridos obligatorios."],
    ["CP-51", "Actualización de datos de contacto", "RF-17", "Baja", "Partición de equivalencia",
     "Formulario Update Contact Info abierto.",
     "1. Ingresar en Zip Code texto extenso o símbolos no permitidos ('ZIP_INVALIDO_#@!').\n2. Clic en 'Update Profile'.",
     "Zip Code: 'ZIP_INVALIDO_#@!'.",
     "El sistema valida la integridad de los campos postales/telefónicos impidiendo guardar datos anómalos."],
    ["CP-52", "Actualización de datos de contacto", "RF-33", "Baja", "Pruebas de caso de uso",
     "Cliente registrado con información de contacto completa.",
     "1. Iniciar sesión.\n2. Hacer clic en 'Update Contact Info'.\n3. Inspeccionar el contenido de cada caja de texto antes de editar.",
     "Datos previamente registrados del cliente.",
     "Todos los campos del formulario se encuentran precargados con la información real y vigente del cliente."],

    # --- F-07 Solicitud de préstamos ---
    ["CP-17", "Solicitud de préstamos", "RF-18", "Media", "Tabla de decisión",
     "Cliente autenticado con una cuenta de fondeo.",
     "1. Abrir Request Loan.\n2. Ingresar monto y down payment que cumplan la regla.\n3. Enviar.",
     "Monto de préstamo válido; down payment >= umbral.",
     "La solicitud muestra un resultado de aprobación explícito."],
    ["CP-53", "Solicitud de préstamos", "RF-18", "Alta", "Análisis de valores límite",
     "Cliente autenticado con cuenta de fondeo.",
     "1. Abrir Request Loan.\n2. Ingresar monto $500.00 y down payment exactamente en el límite mínimo exigido (ej. $100.00 al 20%).\n3. Enviar.",
     "Loan Amount: 500.00, Down Payment: 100.00.",
     "El préstamo se aprueba al cumplir de forma estricta con el valor límite inferior exigido por la política crediticia."],
    ["CP-18", "Solicitud de préstamos", "RF-19", "Media", "Análisis de valores límite",
     "Cliente autenticado.",
     "1. Abrir Request Loan.\n2. Ingresar down payment inmediatamente inferior al umbral.\n3. Enviar.",
     "Down payment = umbral - mínima unidad.",
     "La solicitud muestra un resultado de rechazo y no se presenta como aprobada."],
    ["CP-54", "Solicitud de préstamos", "RF-19", "Media", "Análisis de valores límite",
     "Cliente autenticado en Request Loan.",
     "1. Abrir Request Loan.\n2. Ingresar monto $2000.00 y down payment 0.00.\n3. Enviar formulario.",
     "Monto: 2000.00, Down payment: 0.00.",
     "La solicitud es denegada automáticamente por carecer del enganche obligatorio."],
    ["CP-55", "Solicitud de préstamos", "RF-34", "Alta", "Pruebas de caso de uso",
     "Solicitud de préstamo aprobada exitosamente (CP-17 / CP-53).",
     "1. Completar solicitud de préstamo aprobada por $1000.00 hacia una cuenta activa.\n2. Abrir Accounts Overview.\n3. Verificar creación de cuenta tipo Loan y acreditación de saldo.",
     "Préstamo aprobado por $1000.00.",
     "Se genera un nuevo número de cuenta de tipo Loan en el listado y la cuenta receptora recibe el abono del monto del préstamo."],
    ["CP-56", "Solicitud de préstamos", "RF-35", "Media", "Pruebas de caso de uso",
     "Envío de solicitud de préstamo.",
     "1. Enviar solicitud de préstamo (aprobada o denegada).\n2. Inspeccionar la información provista en la respuesta.",
     "Solicitud de préstamo procesada.",
     "La pantalla detalla el Loan Provider, status (Approved / Denied), fecha de la solicitud y nuevo número de cuenta cuando corresponde."],

    # --- F-08 Panel de administración ---
    ["CP-57", "Panel de administración", "RF-20", "Media", "Tabla de decisión",
     "Acceso a pantalla Administration.",
     "1. Abrir página Administration.\n2. Hacer clic en el botón 'Initialize'.\n3. Verificar mensaje de respuesta y estado de los datos.",
     "Acción administrativa: Initialize.",
     "El sistema ejecuta la reinicialización y muestra 'Database Initialized' restaurando las cuentas y clientes base."],
    ["CP-58", "Panel de administración", "RF-20", "Media", "Tabla de decisión",
     "Acceso a pantalla Administration.",
     "1. Abrir Administration.\n2. Hacer clic en el botón 'Clean'.\n3. Observar confirmación.",
     "Acción administrativa: Clean.",
     "El sistema vacía los registros transaccionales y muestra 'Database Cleaned'."],
    ["CP-59", "Panel de administración", "RF-21", "Media", "Partición de equivalencia",
     "Acceso al panel Administration.",
     "1. Modificar 'Initial Balance' a 1500.00 y 'Minimum Balance' a 150.00.\n2. Clic en Submit.\n3. Recargar la página y revisar los campos.",
     "Initial Balance: 1500.00, Minimum Balance: 150.00.",
     "Los parámetros se actualizan en el sistema y los nuevos valores se conservan tras recargar."],
    ["CP-60", "Panel de administración", "RF-21", "Baja", "Partición de equivalencia",
     "Acceso al panel Administration.",
     "1. Ingresar valor negativo (-500.00) o texto ('invalido') en Initial Balance.\n2. Enviar cambios con Submit.",
     "Initial Balance: -500.00.",
     "El sistema rechaza la configuración con valores incoherentes o no numéricos protegiendo las reglas financieras del banco."],
    ["CP-61", "Panel de administración", "RF-22", "Baja", "Tabla de decisión",
     "Acceso al panel Administration.",
     "1. Seleccionar 'Web Service' en Loan Provider y 'Local' en Loan Processor.\n2. Clic en Submit.\n3. Recargar y verificar la selección activa.",
     "Provider: Web Service, Processor: Local.",
     "La configuración elegida queda guardada y se mantiene activa como motor de préstamos."],
    ["CP-62", "Panel de administración", "RF-36", "Baja", "Partición de equivalencia",
     "Acceso al panel Administration.",
     "1. Modificar 'Threshold' a 25% y 'Loan Provider Days' a 30.\n2. Guardar mediante Submit.\n3. Recargar para confirmar persistencia.",
     "Threshold: 25, Days: 30.",
     "El sistema guarda los nuevos parámetros y los aplica en las evaluaciones subsiguientes de solicitudes de crédito."],
]

# Casos ejecutados en ParaBank (se mantienen exactamente los 9 ejecutados)
EXECUTED_IDS = {"CP-02", "CP-03", "CP-05", "CP-06", "CP-08", "CP-09", "CP-11", "CP-12", "CP-13"}
HIGH_CASES = [c for c in CASES if c[0] in EXECUTED_IDS]


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


def embed_evidence(ws, row, col, filename):
    """Incrusta la primera captura de `filename` (puede traer varias separadas
    por ';') anclada a la celda (row, col). Devuelve True si incrustó algo."""
    if not filename:
        return False
    first = filename.split(";")[0].strip()
    path = EVIDENCE_DIR / first
    if not path.exists():
        return False
    img = XLImage(str(path))
    img.width, img.height = THUMB_W, THUMB_H
    ws.add_image(img, f"{get_column_letter(col)}{row}")
    return True


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
        evidence_name = res.get("evidence", "")
        r = i + 2
        # La columna Evidencia (E) llevará la imagen incrustada; si no hay
        # imagen disponible, se deja el nombre del archivo como texto.
        has_img = (EVIDENCE_DIR / evidence_name.split(";")[0].strip()).exists() if evidence_name else False
        row = [
            cid,
            expected,
            res.get("obtained", "Pendiente de ejecución en ParaBank."),
            res.get("verdict", "Pendiente"),
            "" if has_img else evidence_name,
            res.get("notes", ""),
        ]
        write_row(ws, r, row, WHITE_FILL if i % 2 == 0 else ZEBRA_FILL)
        if embed_evidence(ws, r, 5, evidence_name):
            ws.row_dimensions[r].height = 150
        else:
            ws.row_dimensions[r].height = 56
    ws.column_dimensions["E"].width = 56
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
        evidence_name = f.get("evidence", "")
        has_img = (EVIDENCE_DIR / evidence_name.split(";")[0].strip()).exists() if evidence_name else False
        values = [f.get(k, "") for k in
                  ("id", "title", "summary", "steps", "expected", "obtained", "severity")]
        values.append("" if has_img else evidence_name)
        write_row(ws, r, values, WHITE_FILL if i % 2 == 0 else ZEBRA_FILL)
        if embed_evidence(ws, r, 8, evidence_name):
            ws.row_dimensions[r].height = 150
        else:
            ws.row_dimensions[r].height = 70
    ws.column_dimensions["H"].width = 56
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
