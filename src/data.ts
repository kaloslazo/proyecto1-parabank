export type Priority = 'Alta' | 'Media' | 'Baja'
export type TestStatus = 'Pendiente' | 'Pasó' | 'Falló' | 'Bloqueado'
export type NavKey = 'overview' | 'plan' | 'traceability' | 'cases' | 'execution' | 'findings'

export type Requirement = {
  id: string
  title: string
  type: 'Funcional' | 'No funcional'
  risk: Priority
  rationale: string
  coveredBy: string[]
}

export type TestCase = {
  id: string
  requirement: string
  feature: string
  condition: string
  priority: Priority
  technique: string
  preconditions: string
  data: string
  steps: string[]
  expected: string
  status: TestStatus
  evidence: boolean
}

export type Finding = {
  id: string
  summary: string
  detail: string
  severity: Priority
  status: 'Por ejecutar' | 'Registrado'
}

export const requirements: Requirement[] = [
  { id: 'RF-01', title: 'Registro con campos obligatorios y usuario único', type: 'Funcional', risk: 'Media', rationale: 'Evita cuentas incompletas y duplicadas durante la captación.', coveredBy: ['CP-REG-01', 'CP-REG-02', 'CP-REG-03'] },
  { id: 'RF-02', title: 'Login con rechazo claro de credenciales inválidas', type: 'Funcional', risk: 'Alta', rationale: 'Protege el acceso y evita estados ambiguos de autenticación.', coveredBy: ['CP-LOG-01', 'CP-LOG-02'] },
  { id: 'RF-03', title: 'Apertura con tipo y cuenta de fondeo', type: 'Funcional', risk: 'Alta', rationale: 'Una cuenta creada con datos incompletos compromete el flujo financiero.', coveredBy: ['CP-ACC-01', 'CP-ACC-02'] },
  { id: 'RF-04', title: 'Transferencia: débito y crédito por el mismo monto', type: 'Funcional', risk: 'Alta', rationale: 'Es el riesgo financiero principal del caso.', coveredBy: ['CP-TRF-01', 'CP-TRF-02', 'CP-TRF-03'] },
  { id: 'RF-05', title: 'Bill pay con datos completos y débito correcto', type: 'Funcional', risk: 'Alta', rationale: 'Un pago inconsistente puede causar pérdida directa y reclamos.', coveredBy: ['CP-BP-01', 'CP-BP-02', 'CP-BP-03'] },
  { id: 'RF-06', title: 'Búsqueda de transacciones por filtros', type: 'Funcional', risk: 'Media', rationale: 'Permite comprobar la trazabilidad de operaciones financieras.', coveredBy: ['CP-HIS-01', 'CP-HIS-02'] },
  { id: 'RF-07', title: 'Evaluación de préstamo según monto y enganche', type: 'Funcional', risk: 'Media', rationale: 'Una decisión errónea expone al banco a riesgo crediticio.', coveredBy: ['CP-LOAN-01', 'CP-LOAN-02'] },
  { id: 'RF-08', title: 'Persistencia de datos de contacto', type: 'Funcional', risk: 'Media', rationale: 'El perfil debe reflejar la información que usará atención al cliente.', coveredBy: ['CP-PROF-01'] },
  { id: 'RNF-01', title: 'Respuesta menor a 3 segundos por transacción', type: 'No funcional', risk: 'Media', rationale: 'La lentitud en flujos financieros aumenta abandono y doble envío.', coveredBy: ['CP-NFR-01'] },
  { id: 'RNF-02', title: 'Cierre automático por inactividad', type: 'No funcional', risk: 'Media', rationale: 'Reduce exposición de sesiones abiertas en equipos compartidos.', coveredBy: ['CP-NFR-02'] },
]

export const initialCases: TestCase[] = [
  { id: 'CP-REG-01', requirement: 'RF-01', feature: 'Registro', condition: 'Crear un cliente con todos los campos obligatorios válidos.', priority: 'Media', technique: 'Partición de equivalencia', preconditions: 'No existe el nombre de usuario elegido.', data: 'Datos ficticios coherentes; usuario: kalos.demo.01', steps: ['Abrir Registro', 'Completar los campos obligatorios', 'Enviar el formulario'], expected: 'La cuenta se crea y el sistema confirma el registro.', status: 'Pendiente', evidence: false },
  { id: 'CP-REG-02', requirement: 'RF-01', feature: 'Registro', condition: 'Intentar registrar un nombre de usuario ya existente.', priority: 'Alta', technique: 'Partición de equivalencia', preconditions: 'Existe una cuenta con el usuario usado.', data: 'Usuario duplicado; resto de datos válidos.', steps: ['Abrir Registro', 'Ingresar un usuario existente', 'Enviar el formulario'], expected: 'El registro es rechazado con un mensaje claro y no crea una segunda cuenta.', status: 'Pendiente', evidence: false },
  { id: 'CP-REG-03', requirement: 'RF-01', feature: 'Registro', condition: 'Enviar el registro con uno o más campos obligatorios vacíos.', priority: 'Media', technique: 'Partición de equivalencia', preconditions: 'Formulario de registro disponible.', data: 'Dejar vacío nombre de usuario o contraseña.', steps: ['Abrir Registro', 'Dejar un campo requerido vacío', 'Enviar el formulario'], expected: 'El sistema señala el campo faltante y no crea la cuenta.', status: 'Pendiente', evidence: false },
  { id: 'CP-LOG-01', requirement: 'RF-02', feature: 'Login', condition: 'Autenticar con contraseña incorrecta.', priority: 'Alta', technique: 'Partición de equivalencia', preconditions: 'Cuenta de prueba registrada.', data: 'Usuario válido + contraseña incorrecta.', steps: ['Abrir Login', 'Ingresar credenciales inválidas', 'Enviar'], expected: 'El acceso es rechazado con un mensaje comprensible y la sesión no se inicia.', status: 'Pendiente', evidence: false },
  { id: 'CP-LOG-02', requirement: 'RF-02', feature: 'Login', condition: 'Autenticar con credenciales válidas.', priority: 'Media', technique: 'Transición de estados', preconditions: 'Cuenta de prueba activa.', data: 'Usuario y contraseña válidos.', steps: ['Abrir Login', 'Ingresar credenciales válidas', 'Enviar'], expected: 'El usuario pasa a estado autenticado y ve su resumen de cuentas.', status: 'Pendiente', evidence: false },
  { id: 'CP-ACC-01', requirement: 'RF-03', feature: 'Apertura de cuenta', condition: 'Abrir una cuenta de ahorro fondeada desde una cuenta existente.', priority: 'Alta', technique: 'Tabla de decisión', preconditions: 'Cliente autenticado con cuenta de fondeo.', data: 'Tipo: ahorro; cuenta de fondeo válida.', steps: ['Abrir Open New Account', 'Seleccionar Savings', 'Seleccionar cuenta de fondeo', 'Enviar'], expected: 'Se crea la cuenta y aparece en el resumen del cliente.', status: 'Pendiente', evidence: false },
  { id: 'CP-ACC-02', requirement: 'RF-03', feature: 'Apertura de cuenta', condition: 'Intentar abrir una cuenta sin tipo o sin cuenta de fondeo.', priority: 'Alta', technique: 'Tabla de decisión', preconditions: 'Cliente autenticado.', data: 'Tipo o cuenta de fondeo sin seleccionar.', steps: ['Abrir Open New Account', 'Omitir un dato requerido', 'Enviar'], expected: 'El sistema impide el envío y comunica qué dato falta.', status: 'Pendiente', evidence: false },
  { id: 'CP-TRF-01', requirement: 'RF-04', feature: 'Transferencia', condition: 'Transferir un monto válido entre dos cuentas propias.', priority: 'Alta', technique: 'Tabla de decisión', preconditions: 'Dos cuentas propias y saldo suficiente.', data: 'Monto: 100.00; origen y destino distintos.', steps: ['Abrir Transfer Funds', 'Seleccionar origen y destino', 'Ingresar 100.00', 'Enviar', 'Consultar saldos'], expected: 'El origen disminuye 100.00, el destino aumenta 100.00 y la transacción aparece en el historial.', status: 'Pendiente', evidence: false },
  { id: 'CP-TRF-02', requirement: 'RF-04', feature: 'Transferencia', condition: 'Transferir un monto superior al saldo disponible.', priority: 'Alta', technique: 'Valores límite', preconditions: 'Cuenta de origen con saldo conocido.', data: 'Monto: saldo + 0.01.', steps: ['Abrir Transfer Funds', 'Seleccionar origen y destino', 'Ingresar saldo + 0.01', 'Enviar'], expected: 'La operación se rechaza y no se modifica ningún saldo.', status: 'Pendiente', evidence: false },
  { id: 'CP-TRF-03', requirement: 'RF-04', feature: 'Transferencia', condition: 'Transferir cero, un monto negativo o usar la misma cuenta como origen y destino.', priority: 'Media', technique: 'Valores límite', preconditions: 'Cliente autenticado.', data: 'Monto: 0.00 y -1.00; origen = destino.', steps: ['Abrir Transfer Funds', 'Probar cada dato inválido', 'Enviar'], expected: 'El sistema rechaza los datos inválidos sin alterar saldos.', status: 'Pendiente', evidence: false },
  { id: 'CP-BP-01', requirement: 'RF-05', feature: 'Bill pay', condition: 'Pagar un servicio con beneficiario, cuenta y monto válidos.', priority: 'Alta', technique: 'Tabla de decisión', preconditions: 'Cuenta con saldo suficiente.', data: 'Beneficiario ficticio; monto: 25.00.', steps: ['Abrir Bill Pay', 'Completar datos del beneficiario', 'Seleccionar cuenta', 'Ingresar 25.00', 'Enviar'], expected: 'El pago se confirma, descuenta 25.00 y registra una operación consultable.', status: 'Pendiente', evidence: false },
  { id: 'CP-BP-02', requirement: 'RF-05', feature: 'Bill pay', condition: 'Enviar un pago sin nombre, dirección, cuenta o monto.', priority: 'Media', technique: 'Partición de equivalencia', preconditions: 'Cliente autenticado.', data: 'Omitir un campo requerido por iteración.', steps: ['Abrir Bill Pay', 'Dejar un dato vacío', 'Enviar'], expected: 'El sistema identifica el dato faltante y no procesa el pago.', status: 'Pendiente', evidence: false },
  { id: 'CP-BP-03', requirement: 'RF-05', feature: 'Bill pay', condition: 'Pagar un monto mayor al saldo disponible.', priority: 'Alta', technique: 'Valores límite', preconditions: 'Cuenta con saldo conocido.', data: 'Monto: saldo + 0.01.', steps: ['Abrir Bill Pay', 'Completar beneficiario', 'Ingresar saldo + 0.01', 'Enviar'], expected: 'El pago se rechaza y el saldo permanece intacto.', status: 'Pendiente', evidence: false },
  { id: 'CP-HIS-01', requirement: 'RF-06', feature: 'Historial', condition: 'Buscar operaciones por fecha y rango de fechas.', priority: 'Media', technique: 'Partición de equivalencia', preconditions: 'Existen transacciones de prueba.', data: 'Fecha exacta y rango que incluya una operación conocida.', steps: ['Abrir Account History', 'Consultar una fecha', 'Consultar un rango'], expected: 'Solo se muestran las operaciones que corresponden al filtro.', status: 'Pendiente', evidence: false },
  { id: 'CP-HIS-02', requirement: 'RF-06', feature: 'Historial', condition: 'Buscar una operación por monto o ID de transacción.', priority: 'Media', technique: 'Partición de equivalencia', preconditions: 'Existe una transacción con datos conocidos.', data: 'Monto exacto e ID obtenido después de una operación.', steps: ['Abrir búsqueda de transacciones', 'Ingresar monto', 'Repetir con ID'], expected: 'El resultado identifica la operación correcta sin mezclar registros.', status: 'Pendiente', evidence: false },
  { id: 'CP-LOAN-01', requirement: 'RF-07', feature: 'Préstamos', condition: 'Solicitar un préstamo con enganche suficiente para aprobación.', priority: 'Media', technique: 'Tabla de decisión', preconditions: 'Cliente autenticado y formulario disponible.', data: 'Monto solicitado y down payment que cumpla el umbral configurado.', steps: ['Abrir Request Loan', 'Ingresar monto y enganche', 'Enviar'], expected: 'El sistema muestra una aprobación explícita.', status: 'Pendiente', evidence: false },
  { id: 'CP-LOAN-02', requirement: 'RF-07', feature: 'Préstamos', condition: 'Solicitar un préstamo con enganche insuficiente.', priority: 'Media', technique: 'Valores límite', preconditions: 'Cliente autenticado.', data: 'Down payment por debajo del umbral.', steps: ['Abrir Request Loan', 'Ingresar monto y enganche insuficiente', 'Enviar'], expected: 'El sistema muestra un rechazo explícito y no aprueba el préstamo.', status: 'Pendiente', evidence: false },
  { id: 'CP-PROF-01', requirement: 'RF-08', feature: 'Perfil', condition: 'Actualizar datos de contacto y comprobar persistencia.', priority: 'Media', technique: 'Transición de estados', preconditions: 'Cliente autenticado.', data: 'Teléfono y dirección ficticios válidos.', steps: ['Abrir Update Contact Info', 'Modificar los datos', 'Guardar', 'Salir y volver al perfil'], expected: 'Los datos actualizados permanecen visibles en el perfil.', status: 'Pendiente', evidence: false },
  { id: 'CP-NFR-01', requirement: 'RNF-01', feature: 'Rendimiento', condition: 'Medir el tiempo de respuesta de una transferencia o pago.', priority: 'Media', technique: 'Medición', preconditions: 'Cuenta de prueba y cronómetro disponibles.', data: 'Transacción válida de bajo monto.', steps: ['Iniciar cronómetro al enviar', 'Detener al recibir confirmación', 'Registrar el tiempo'], expected: 'La confirmación llega en menos de 3 segundos.', status: 'Pendiente', evidence: false },
  { id: 'CP-NFR-02', requirement: 'RNF-02', feature: 'Sesión', condition: 'Verificar el comportamiento después de inactividad.', priority: 'Media', technique: 'Transición de estados', preconditions: 'Sesión iniciada; ventana de inactividad definida por el entorno.', data: 'Sin interacción durante el intervalo observado.', steps: ['Iniciar sesión', 'No interactuar', 'Intentar abrir una función protegida'], expected: 'La sesión se cierra y el sistema exige autenticación nuevamente.', status: 'Pendiente', evidence: false },
]

export const initialFindings: Finding[] = [
  { id: 'OBS-01', summary: 'La evidencia manual todavía está pendiente', detail: 'Los casos críticos están diseñados, pero aún no se registra un veredicto sin una ejecución sobre ParaBank.', severity: 'Alta', status: 'Por ejecutar' },
  { id: 'OBS-02', summary: 'La integridad del saldo es el punto de control principal', detail: 'Las pruebas de transferencia y bill pay deben capturar el saldo antes y después, además del historial.', severity: 'Alta', status: 'Por ejecutar' },
]

export const navItems: { key: NavKey; label: string; icon: string }[] = [
  { key: 'overview', label: 'Resumen', icon: 'grid' },
  { key: 'plan', label: 'Plan', icon: 'clipboard' },
  { key: 'traceability', label: 'Trazabilidad', icon: 'route' },
  { key: 'cases', label: 'Casos', icon: 'check' },
  { key: 'execution', label: 'Ejecución', icon: 'play' },
  { key: 'findings', label: 'Hallazgos', icon: 'spark' },
]
