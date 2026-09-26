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
  obtained?: string
  evidenceImage?: string
}

export type Finding = {
  id: string
  summary: string
  detail: string
  severity: Priority
  status: 'Por ejecutar' | 'Registrado'
  evidenceImage?: string
}

export type ClientRequirement = {
  id: string
  functionalityId: string
  requirement: string
  actor: string
  dataRules: string
  expected: string
  priority: Priority
}

export type ClientBlackBoxExample = {
  technique: string
  example: string
}

export type ClientFunctionality = {
  id: string
  name: string
  location: string
  actor: string
  requirementIds: string[]
}

export type ClientNonFunctionalRequirement = {
  id: string
  category: string
  requirement: string
  verification: string
  priority: Priority
}

export const clientFunctionalities: ClientFunctionality[] = [
  { id: 'F-01', name: 'Registro y login de clientes', location: 'Inicio y formulario de registro', actor: 'Cliente', requirementIds: ['RF-01', 'RF-02', 'RF-03', 'RF-04'] },
  { id: 'F-02', name: 'Apertura de nuevas cuentas', location: 'Menú de la cuenta: Abrir nueva cuenta', actor: 'Cliente', requirementIds: ['RF-05', 'RF-06', 'RF-07'] },
  { id: 'F-03', name: 'Transferencia entre cuentas propias', location: 'Menú de la cuenta: Transferir fondos', actor: 'Cliente', requirementIds: ['RF-08', 'RF-09', 'RF-10'] },
  { id: 'F-04', name: 'Pago de servicios a terceros (Bill Pay)', location: 'Menú de la cuenta: Pagar servicios', actor: 'Cliente', requirementIds: ['RF-11', 'RF-12', 'RF-13'] },
  { id: 'F-05', name: 'Búsqueda de transacciones', location: 'Menú de la cuenta: Buscar transacciones e historial', actor: 'Cliente', requirementIds: ['RF-14', 'RF-15'] },
  { id: 'F-06', name: 'Actualización de datos de contacto', location: 'Menú de la cuenta: Actualizar datos de contacto', actor: 'Cliente', requirementIds: ['RF-16', 'RF-17'] },
  { id: 'F-07', name: 'Solicitud de préstamos', location: 'Menú de la cuenta: Solicitar préstamo', actor: 'Cliente', requirementIds: ['RF-18', 'RF-19'] },
  { id: 'F-08', name: 'Panel de administración', location: 'Panel de administración del banco', actor: 'Administrador', requirementIds: ['RF-20', 'RF-21', 'RF-22'] },
]

export const clientRequirements: ClientRequirement[] = [
  { id: 'RF-01', functionalityId: 'F-01', requirement: 'El sistema debe permitir registrar un cliente cuando se completen todos los campos obligatorios y el nombre de usuario no esté registrado.', actor: 'Cliente', dataRules: 'Nombre, apellido, dirección, ciudad, estado, código postal, teléfono, SSN, usuario, contraseña y confirmación; todos obligatorios y usuario único.', expected: 'La cuenta se crea y se muestra una confirmación de registro.', priority: 'Alta' },
  { id: 'RF-02', functionalityId: 'F-01', requirement: 'El sistema debe rechazar el registro cuando el nombre de usuario ya exista.', actor: 'Cliente', dataRules: 'Usuario previamente registrado; el resto de datos puede ser válido.', expected: 'El registro no se crea y se muestra un mensaje indicando que el usuario ya está en uso.', priority: 'Alta' },
  { id: 'RF-03', functionalityId: 'F-01', requirement: 'El sistema debe rechazar el acceso cuando el usuario o la contraseña sean inválidos.', actor: 'Cliente', dataRules: 'Usuario inexistente, contraseña incorrecta o ambos datos inválidos.', expected: 'La sesión no se inicia y se muestra un mensaje de error claro.', priority: 'Alta' },
  { id: 'RF-04', functionalityId: 'F-01', requirement: 'El sistema debe permitir el acceso cuando las credenciales correspondan a un cliente registrado.', actor: 'Cliente', dataRules: 'Usuario y contraseña válidos de una cuenta existente.', expected: 'El cliente ingresa al resumen de cuentas y puede ver las operaciones disponibles.', priority: 'Alta' },
  { id: 'RF-05', functionalityId: 'F-02', requirement: 'El sistema debe permitir abrir una cuenta corriente o de ahorro cuando se seleccione el tipo y una cuenta de fondeo válida.', actor: 'Cliente', dataRules: 'Tipo: Checking o Savings; cuenta de fondeo existente y perteneciente al cliente.', expected: 'La nueva cuenta se crea y aparece en el resumen del cliente.', priority: 'Alta' },
  { id: 'RF-06', functionalityId: 'F-02', requirement: 'El sistema debe rechazar la apertura cuando no se seleccione el tipo de cuenta o la cuenta de fondeo.', actor: 'Cliente', dataRules: 'Tipo vacío, cuenta de fondeo vacía o ambos datos ausentes.', expected: 'La cuenta no se crea y el formulario solicita completar los datos faltantes.', priority: 'Alta' },
  { id: 'RF-07', functionalityId: 'F-02', requirement: 'El sistema debe mostrar la cuenta recién creada con su número y saldo en el resumen del cliente.', actor: 'Cliente', dataRules: 'Apertura completada correctamente.', expected: 'El número de cuenta, tipo y saldo inicial quedan visibles al volver al resumen.', priority: 'Alta' },
  { id: 'RF-08', functionalityId: 'F-03', requirement: 'El sistema debe transferir fondos entre dos cuentas propias cuando el monto sea positivo y exista saldo suficiente.', actor: 'Cliente', dataRules: 'Origen y destino distintos; monto mayor que cero y menor o igual al saldo de origen.', expected: 'El origen se debita y el destino se acredita por el mismo monto.', priority: 'Alta' },
  { id: 'RF-09', functionalityId: 'F-03', requirement: 'El sistema debe rechazar una transferencia cuyo monto supere el saldo disponible.', actor: 'Cliente', dataRules: 'Monto igual al saldo más 0.01 o cualquier monto mayor al saldo de origen.', expected: 'La transferencia no se procesa y ningún saldo cambia.', priority: 'Alta' },
  { id: 'RF-10', functionalityId: 'F-03', requirement: 'El sistema debe rechazar montos cero, negativos o una transferencia hacia la misma cuenta de origen.', actor: 'Cliente', dataRules: 'Monto 0.00, monto negativo, origen igual a destino.', expected: 'La operación no se procesa y el sistema muestra una validación comprensible.', priority: 'Alta' },
  { id: 'RF-11', functionalityId: 'F-04', requirement: 'El sistema debe procesar un pago de servicio cuando beneficiario, dirección, cuenta y monto sean válidos.', actor: 'Cliente', dataRules: 'Datos del beneficiario completos; cuenta propia seleccionada; monto positivo y dentro del saldo disponible.', expected: 'El pago se confirma y el monto se descuenta de la cuenta seleccionada.', priority: 'Alta' },
  { id: 'RF-12', functionalityId: 'F-04', requirement: 'El sistema debe rechazar un pago de servicio cuando falte el nombre, dirección, cuenta o monto requerido.', actor: 'Cliente', dataRules: 'Omitir cada campo obligatorio al menos una vez; probar monto vacío y no numérico.', expected: 'El pago no se procesa y se identifica el dato faltante o inválido.', priority: 'Alta' },
  { id: 'RF-13', functionalityId: 'F-04', requirement: 'El sistema debe rechazar un pago de servicio cuyo monto supere el saldo de la cuenta seleccionada.', actor: 'Cliente', dataRules: 'Monto igual al saldo más 0.01 o superior.', expected: 'El pago no se procesa y el saldo de la cuenta permanece sin cambios.', priority: 'Alta' },
  { id: 'RF-14', functionalityId: 'F-05', requirement: 'El sistema debe mostrar las transacciones que correspondan a una fecha exacta o a un rango de fechas válido.', actor: 'Cliente', dataRules: 'Fecha exacta y rango con fecha inicial menor o igual a fecha final.', expected: 'La lista muestra únicamente las transacciones que cumplen el filtro.', priority: 'Alta' },
  { id: 'RF-15', functionalityId: 'F-05', requirement: 'El sistema debe permitir localizar una transacción por monto o por ID de transacción.', actor: 'Cliente', dataRules: 'Monto exacto de una operación existente e ID de una operación existente; probar valores sin coincidencia.', expected: 'Se muestra la operación coincidente o un mensaje de que no existen resultados.', priority: 'Alta' },
  { id: 'RF-16', functionalityId: 'F-06', requirement: 'El sistema debe guardar los nuevos datos de contacto cuando el cliente complete la actualización y la confirme.', actor: 'Cliente', dataRules: 'Teléfono, dirección, ciudad, estado y código postal con valores válidos.', expected: 'El sistema confirma la actualización y los datos quedan asociados al perfil.', priority: 'Alta' },
  { id: 'RF-17', functionalityId: 'F-06', requirement: 'El sistema no debe guardar datos de contacto incompletos o inválidos.', actor: 'Cliente', dataRules: 'Campo obligatorio vacío, código postal inválido o formato de teléfono inválido.', expected: 'La actualización se rechaza y se informa qué dato debe corregirse.', priority: 'Baja' },
  { id: 'RF-18', functionalityId: 'F-07', requirement: 'El sistema debe aprobar una solicitud de préstamo cuando el monto solicitado y el enganche cumplan la regla configurada.', actor: 'Cliente', dataRules: 'Monto de préstamo válido y down payment igual o superior al umbral configurado.', expected: 'La solicitud muestra un resultado de aprobación.', priority: 'Alta' },
  { id: 'RF-19', functionalityId: 'F-07', requirement: 'El sistema debe rechazar una solicitud de préstamo cuando el enganche no cumpla la regla configurada.', actor: 'Cliente', dataRules: 'Down payment inferior al umbral o datos de solicitud inválidos.', expected: 'La solicitud muestra un resultado de rechazo y no se presenta como aprobada.', priority: 'Alta' },
  { id: 'RF-20', functionalityId: 'F-08', requirement: 'El panel debe permitir inicializar o limpiar la base de datos mediante las acciones administrativas disponibles.', actor: 'Administrador', dataRules: 'Acción Initialize o Clean seleccionada en la pantalla Administration.', expected: 'La acción se ejecuta y el panel informa su resultado.', priority: 'Alta' },
  { id: 'RF-21', functionalityId: 'F-08', requirement: 'El panel debe permitir configurar los valores numéricos de saldo inicial, saldo mínimo y umbral del banco.', actor: 'Administrador', dataRules: 'Valores numéricos válidos; probar también campos vacíos, negativos o no numéricos.', expected: 'Los parámetros se pueden enviar y el sistema muestra una confirmación o validación.', priority: 'Alta' },
  { id: 'RF-22', functionalityId: 'F-08', requirement: 'El panel debe permitir seleccionar el proveedor y procesador de préstamos disponibles.', actor: 'Administrador', dataRules: 'Opciones válidas de Loan Provider y Loan Processor.', expected: 'La selección queda disponible para la configuración del banco.', priority: 'Alta' },
]

export const clientBlackBoxExamples: Record<string, ClientBlackBoxExample> = {
  'RF-01': { technique: 'Partición de equivalencia', example: 'Registrar un cliente con todos los campos válidos y repetir dejando vacío un campo obligatorio; comparar creación y rechazo.' },
  'RF-02': { technique: 'Partición de equivalencia', example: 'Enviar el formulario con un usuario nuevo y luego con un usuario ya registrado; el segundo intento debe rechazarse.' },
  'RF-03': { technique: 'Partición de equivalencia', example: 'Probar usuario válido con contraseña incorrecta, usuario inexistente y ambos datos inválidos; ninguna combinación debe iniciar sesión.' },
  'RF-04': { technique: 'Pruebas de caso de uso', example: 'Recorrer el caso de uso de inicio de sesión con credenciales válidas y comprobar el acceso al resumen de cuentas.' },
  'RF-05': { technique: 'Tablas de decisión y gráficos causa-efecto', example: 'Combinar tipo de cuenta seleccionado y cuenta de fondeo válida; solo la combinación completa debe crear la cuenta.' },
  'RF-06': { technique: 'Tablas de decisión y gráficos causa-efecto', example: 'Omitir el tipo, omitir la cuenta de fondeo y omitir ambos; en los tres casos la apertura debe bloquearse.' },
  'RF-07': { technique: 'Pruebas de caso de uso', example: 'Completar el caso de uso de apertura y verificar en el resumen el nuevo número, tipo y saldo.' },
  'RF-08': { technique: 'Tablas de decisión y gráficos causa-efecto', example: 'Usar cuentas distintas, monto positivo y saldo suficiente; verificar el mismo importe como débito en origen y crédito en destino.' },
  'RF-09': { technique: 'Análisis de valores límite', example: 'Con saldo conocido, probar exactamente el saldo disponible y luego saldo + 0.01; el segundo monto debe rechazarse.' },
  'RF-10': { technique: 'Análisis de valores límite', example: 'Intentar transferir 0.00 y -0.01; ninguno debe modificar los saldos ni generar una transacción.' },
  'RF-11': { technique: 'Tablas de decisión y gráficos causa-efecto', example: 'Completar beneficiario, dirección, cuenta y monto válido con saldo suficiente; el pago debe confirmarse y descontarse.' },
  'RF-12': { technique: 'Partición de equivalencia', example: 'Omitir por separado nombre, dirección, cuenta y monto, y probar un monto no numérico; cada entrada inválida debe rechazarse.' },
  'RF-13': { technique: 'Análisis de valores límite', example: 'Probar un pago igual al saldo y otro por saldo + 0.01; el segundo no debe procesarse ni alterar el saldo.' },
  'RF-14': { technique: 'Análisis de valores límite', example: 'Buscar con fecha inicial igual a la final y luego con la fecha final anterior; comparar los resultados y la validación.' },
  'RF-15': { technique: 'Partición de equivalencia', example: 'Buscar un monto y un ID existentes, y repetir con valores sin coincidencia; debe mostrarse la operación o un estado sin resultados.' },
  'RF-16': { technique: 'Pruebas de caso de uso', example: 'Recorrer la actualización de perfil: modificar teléfono y dirección, guardar y volver a consultar los datos.' },
  'RF-17': { technique: 'Partición de equivalencia', example: 'Probar un campo obligatorio vacío, teléfono con formato inválido y código postal inválido; ningún cambio debe guardarse.' },
  'RF-18': { technique: 'Tablas de decisión y gráficos causa-efecto', example: 'Combinar monto válido con enganche igual o superior al umbral; la solicitud debe mostrar aprobación.' },
  'RF-19': { technique: 'Análisis de valores límite', example: 'Probar un enganche exactamente en el umbral y otro inmediatamente inferior; el segundo debe producir rechazo.' },
  'RF-20': { technique: 'Tablas de decisión y gráficos causa-efecto', example: 'Relacionar cada acción con su efecto: Clean debe limpiar los datos e Initialize debe restaurar los datos base.' },
  'RF-21': { technique: 'Partición de equivalencia', example: 'Enviar valores numéricos válidos y repetir con campos vacíos, negativos y texto; observar confirmación o validación.' },
  'RF-22': { technique: 'Tablas de decisión y gráficos causa-efecto', example: 'Seleccionar combinaciones disponibles de proveedor y procesador, guardar y comprobar que la configuración elegida permanezca activa.' },
}

export const clientNonFunctionalRequirements: ClientNonFunctionalRequirement[] = [
  {
    id: 'RNF-01',
    category: 'Disponibilidad',
    requirement: 'El sistema debe mantener una alta disponibilidad durante el horario bancario.',
    verification: 'Comprobar el acceso y una operación crítica en distintas franjas del horario bancario; registrar cualquier indisponibilidad.',
    priority: 'Alta',
  },
  {
    id: 'RNF-02',
    category: 'Rendimiento',
    requirement: 'El sistema debe responder en menos de 3 segundos por transacción.',
    verification: 'Medir el tiempo desde el envío de una transferencia o pago válido hasta que se muestre la confirmación.',
    priority: 'Alta',
  },
  {
    id: 'RNF-03',
    category: 'Sesión',
    requirement: 'El sistema debe cerrar automáticamente la sesión después de un periodo de inactividad.',
    verification: 'Dejar la sesión sin actividad e intentar acceder luego a una función protegida; el sistema debe solicitar autenticación.',
    priority: 'Alta',
  },
]

export const requirements: Requirement[] = [
  { id: 'RF-01', title: 'Registro con campos obligatorios y usuario único', type: 'Funcional', risk: 'Alta', rationale: 'Evita cuentas incompletas y duplicadas durante la captación.', coveredBy: ['CP-REG-01', 'CP-REG-02', 'CP-REG-03'] },
  { id: 'RF-02', title: 'Login con rechazo claro de credenciales inválidas', type: 'Funcional', risk: 'Alta', rationale: 'Protege el acceso y evita estados ambiguos de autenticación.', coveredBy: ['CP-LOG-01', 'CP-LOG-02'] },
  { id: 'RF-03', title: 'Apertura con tipo y cuenta de fondeo', type: 'Funcional', risk: 'Alta', rationale: 'Una cuenta creada con datos incompletos compromete el flujo financiero.', coveredBy: ['CP-ACC-01', 'CP-ACC-02'] },
  { id: 'RF-04', title: 'Transferencia: débito y crédito por el mismo monto', type: 'Funcional', risk: 'Alta', rationale: 'Es el riesgo financiero principal del caso.', coveredBy: ['CP-TRF-01', 'CP-TRF-02', 'CP-TRF-03'] },
  { id: 'RF-05', title: 'Bill pay con datos completos y débito correcto', type: 'Funcional', risk: 'Alta', rationale: 'Un pago inconsistente puede causar pérdida directa y reclamos.', coveredBy: ['CP-BP-01', 'CP-BP-02', 'CP-BP-03'] },
  { id: 'RF-06', title: 'Búsqueda de transacciones por filtros', type: 'Funcional', risk: 'Alta', rationale: 'Permite comprobar la trazabilidad de operaciones financieras.', coveredBy: ['CP-HIS-01', 'CP-HIS-02'] },
  { id: 'RF-07', title: 'Evaluación de préstamo según monto y enganche', type: 'Funcional', risk: 'Alta', rationale: 'Una decisión errónea expone al banco a riesgo crediticio.', coveredBy: ['CP-LOAN-01', 'CP-LOAN-02'] },
  { id: 'RF-08', title: 'Persistencia de datos de contacto', type: 'Funcional', risk: 'Alta', rationale: 'El perfil debe reflejar la información que usará atención al cliente.', coveredBy: ['CP-PROF-01'] },
  { id: 'RNF-01', title: 'Respuesta menor a 3 segundos por transacción', type: 'No funcional', risk: 'Alta', rationale: 'La lentitud en flujos financieros aumenta abandono y doble envío.', coveredBy: ['CP-NFR-01'] },
  { id: 'RNF-02', title: 'Cierre automático por inactividad', type: 'No funcional', risk: 'Alta', rationale: 'Reduce exposición de sesiones abiertas en equipos compartidos.', coveredBy: ['CP-NFR-02'] },
]

// Diseño (18 casos) y ejecución real sobre ParaBank (24-09-2026).
// Usuario de prueba gsegovia_qa_5821; cuentas 28662 / 28773. Los 9 casos de
// prioridad Alta se ejecutaron: 6 pasaron, 3 fallaron; cada uno con captura.
export const initialCases: TestCase[] = [
  { id: 'CP-01', requirement: 'RF-01', feature: 'Registro', condition: 'Registrar un cliente con todos los datos válidos.', priority: 'Media', technique: 'Partición de equivalencia', preconditions: 'El nombre de usuario elegido no está registrado.', data: 'Usuario gsegovia_qa_5821; datos ficticios coherentes.', steps: ['Abrir Register', 'Completar los campos obligatorios', 'Enviar el formulario'], expected: 'La cuenta se crea y el sistema muestra la confirmación de registro.', status: 'Pendiente', evidence: false },
  { id: 'CP-02', requirement: 'RF-02', feature: 'Registro', condition: 'Registrar un nombre de usuario ya existente.', priority: 'Alta', technique: 'Partición de equivalencia', preconditions: 'Ya existe una cuenta con ese usuario.', data: 'Usuario duplicado; resto de datos válidos.', steps: ['Abrir Register', 'Ingresar un usuario ya registrado', 'Enviar'], expected: 'El registro es rechazado con un mensaje de usuario en uso y no crea una segunda cuenta.', status: 'Pasó', evidence: true, obtained: "Sin sesión activa se rechaza con 'This username already exists.'", evidenceImage: 'CP-02_usuario_duplicado_rechazado.jpg' },
  { id: 'CP-03', requirement: 'RF-03', feature: 'Login', condition: 'Autenticar con credenciales inválidas.', priority: 'Alta', technique: 'Partición de equivalencia', preconditions: 'Existe una cuenta de prueba registrada.', data: 'Usuario válido + contraseña incorrecta; usuario inexistente.', steps: ['Abrir la página de inicio', 'Ingresar credenciales inválidas', 'Enviar'], expected: 'La sesión no se inicia y se muestra un mensaje de error claro.', status: 'Pasó', evidence: true, obtained: "'The username and password could not be verified.'; no inicia sesión.", evidenceImage: 'CP-03_login_invalido.jpg' },
  { id: 'CP-04', requirement: 'RF-04', feature: 'Login', condition: 'Autenticar con credenciales válidas.', priority: 'Media', technique: 'Transición de estados', preconditions: 'Cuenta de prueba activa; sesión cerrada.', data: 'Usuario y contraseña válidos.', steps: ['Ingresar credenciales válidas', 'Enviar', 'Observar el cambio de estado'], expected: 'El sistema transita a estado autenticado y muestra el Accounts Overview.', status: 'Pendiente', evidence: false },
  { id: 'CP-05', requirement: 'RF-05', feature: 'Apertura de cuenta', condition: 'Abrir una cuenta Savings fondeada desde una cuenta existente.', priority: 'Alta', technique: 'Tabla de decisión', preconditions: 'Cliente autenticado con cuenta de fondeo.', data: 'Tipo: Savings; cuenta de fondeo válida.', steps: ['Abrir Open New Account', 'Seleccionar SAVINGS', 'Seleccionar cuenta de fondeo', 'Enviar'], expected: 'La nueva cuenta se crea, muestra su número y aparece en el resumen.', status: 'Pasó', evidence: true, obtained: 'Se creó la cuenta SAVINGS 28773 y aparece en el resumen.', evidenceImage: 'CP-05_cuenta_savings_creada.jpg' },
  { id: 'CP-06', requirement: 'RF-06', feature: 'Apertura de cuenta', condition: 'Abrir una cuenta sin tipo o sin cuenta de fondeo.', priority: 'Alta', technique: 'Tabla de decisión', preconditions: 'Cliente autenticado.', data: 'Tipo vacío, fondeo vacío o ambos.', steps: ['Abrir Open New Account', 'Dejar sin seleccionar tipo y/o fondeo', 'Intentar enviar'], expected: 'La cuenta no se crea; el sistema solicita completar los datos faltantes.', status: 'Pasó', evidence: true, obtained: 'La UI no permite dejar campos vacíos (desplegables con valor por defecto): se cumple por prevención.', evidenceImage: 'CP-06_apertura_sin_opcion_vacia.jpg' },
  { id: 'CP-07', requirement: 'RF-07', feature: 'Apertura de cuenta', condition: 'Ver la cuenta recién creada en el resumen.', priority: 'Media', technique: 'Transición de estados', preconditions: 'Se completó una apertura de cuenta.', data: 'Cuenta creada en CP-05.', steps: ['Volver a Accounts Overview', 'Ubicar la cuenta creada', 'Verificar número, tipo y saldo'], expected: 'La cuenta aparece con su número, tipo y saldo inicial.', status: 'Pendiente', evidence: false },
  { id: 'CP-08', requirement: 'RF-08', feature: 'Transferencia', condition: 'Transferir un monto válido entre dos cuentas propias.', priority: 'Alta', technique: 'Tabla de decisión', preconditions: 'Dos cuentas propias con saldo suficiente.', data: 'Monto: 100.00; origen 28662, destino 28773.', steps: ['Registrar saldos iniciales', 'Abrir Transfer Funds', 'Transferir 100.00', 'Enviar', 'Verificar saldos e historial'], expected: 'El origen se debita 100.00, el destino se acredita 100.00 y queda en el historial.', status: 'Pasó', evidence: true, obtained: '28662 $425.50→$325.50 y 28773 $90.00→$190.00; débito y crédito correctos.', evidenceImage: 'CP-08_saldos_despues.jpg' },
  { id: 'CP-09', requirement: 'RF-09', feature: 'Transferencia', condition: 'Transferir un monto mayor al saldo disponible (saldo + 0.01).', priority: 'Alta', technique: 'Análisis de valores límite', preconditions: 'Cuenta de origen con saldo conocido.', data: 'Monto = saldo disponible + 0.01 (325.51 sobre 325.50).', steps: ['Registrar saldo de origen', 'Abrir Transfer Funds', 'Ingresar saldo + 0.01', 'Enviar', 'Verificar saldos'], expected: 'La transferencia se rechaza y ningún saldo cambia.', status: 'Falló', evidence: true, obtained: 'PERMITIÓ la transferencia: 28662 quedó en -$0.01. No valida saldo insuficiente (H-01).', evidenceImage: 'CP-09_H01_saldo_negativo.jpg' },
  { id: 'CP-10', requirement: 'RF-10', feature: 'Transferencia', condition: 'Transferir cero, negativo o a la misma cuenta.', priority: 'Media', technique: 'Análisis de valores límite', preconditions: 'Cliente autenticado con dos cuentas.', data: 'Montos 0.00 y -1.00; origen igual a destino.', steps: ['Abrir Transfer Funds', 'Probar cada dato inválido', 'Enviar'], expected: 'El sistema rechaza cada entrada inválida sin alterar saldos.', status: 'Pendiente', evidence: false },
  { id: 'CP-11', requirement: 'RF-11', feature: 'Bill pay', condition: 'Pagar un servicio con beneficiario, cuenta y monto válidos.', priority: 'Alta', technique: 'Tabla de decisión', preconditions: 'Cuenta con saldo suficiente.', data: 'Beneficiario ficticio; monto: 25.00 desde 28773.', steps: ['Registrar saldo', 'Abrir Bill Pay', 'Completar datos y monto 25.00', 'Enviar', 'Verificar saldo e historial'], expected: 'El pago se confirma, descuenta 25.00 y registra una operación consultable.', status: 'Falló', evidence: true, obtained: "'Bill Payment Complete', pero el saldo siguió en $515.51 y no se registró el débito (H-02).", evidenceImage: 'CP-11_H02_billpay_no_descuenta.jpg' },
  { id: 'CP-12', requirement: 'RF-12', feature: 'Bill pay', condition: 'Enviar un pago con campos obligatorios faltantes.', priority: 'Alta', technique: 'Partición de equivalencia', preconditions: 'Cliente autenticado.', data: 'Un campo obligatorio vacío por iteración; monto no numérico.', steps: ['Abrir Bill Pay', 'Omitir un dato requerido', 'Enviar'], expected: 'El pago no se procesa y el sistema identifica el dato faltante o inválido.', status: 'Pasó', evidence: true, obtained: "Valida cada campo ('Payee name is required.', 'The amount cannot be empty.', ...) y no procesa el pago.", evidenceImage: 'CP-12_billpay_validacion_campos.jpg' },
  { id: 'CP-13', requirement: 'RF-13', feature: 'Bill pay', condition: 'Pagar un monto mayor al saldo de la cuenta.', priority: 'Alta', technique: 'Análisis de valores límite', preconditions: 'Cuenta con saldo conocido.', data: 'Monto 1000.00 sobre saldo 515.51 desde 28773.', steps: ['Abrir Bill Pay', 'Completar beneficiario válido', 'Ingresar monto > saldo', 'Enviar'], expected: 'El pago se rechaza y el saldo permanece sin cambios.', status: 'Falló', evidence: true, obtained: "No validó saldo: mostró 'An internal error has occurred' y luego el Accounts Overview quedó roto (H-03).", evidenceImage: 'CP-13_H03_billpay_error_interno.jpg' },
  { id: 'CP-14', requirement: 'RF-14', feature: 'Historial', condition: 'Buscar transacciones por fecha exacta o rango.', priority: 'Media', technique: 'Análisis de valores límite', preconditions: 'Existen transacciones de prueba.', data: 'Fecha exacta; rango válido; rango invertido.', steps: ['Abrir Find Transactions', 'Buscar por fecha', 'Buscar por rango', 'Probar rango inválido'], expected: 'Se listan solo las transacciones que cumplen el filtro.', status: 'Pendiente', evidence: false },
  { id: 'CP-15', requirement: 'RF-15', feature: 'Historial', condition: 'Localizar una transacción por monto o ID.', priority: 'Media', technique: 'Partición de equivalencia', preconditions: 'Existe una transacción con monto e ID conocidos.', data: 'Monto e ID existentes; valores inexistentes.', steps: ['Abrir Find Transactions', 'Buscar por monto', 'Buscar por ID', 'Repetir sin coincidencia'], expected: 'Se muestra la operación coincidente o un mensaje de sin resultados.', status: 'Pendiente', evidence: false },
  { id: 'CP-16', requirement: 'RF-16', feature: 'Perfil', condition: 'Actualizar datos de contacto y verificar persistencia.', priority: 'Media', technique: 'Partición de equivalencia', preconditions: 'Cliente autenticado.', data: 'Teléfono y dirección ficticios válidos.', steps: ['Abrir Update Contact Info', 'Modificar datos', 'Guardar', 'Volver a abrir el perfil'], expected: 'El sistema confirma la actualización y los datos persisten.', status: 'Pendiente', evidence: false },
  { id: 'CP-17', requirement: 'RF-18', feature: 'Préstamos', condition: 'Solicitar un préstamo que cumple la regla de enganche.', priority: 'Media', technique: 'Tabla de decisión', preconditions: 'Cliente autenticado con cuenta de fondeo.', data: 'Monto válido; down payment >= umbral.', steps: ['Abrir Request Loan', 'Ingresar monto y enganche', 'Enviar'], expected: 'La solicitud muestra un resultado de aprobación explícito.', status: 'Pendiente', evidence: false },
  { id: 'CP-18', requirement: 'RF-19', feature: 'Préstamos', condition: 'Solicitar un préstamo con enganche insuficiente.', priority: 'Media', technique: 'Análisis de valores límite', preconditions: 'Cliente autenticado.', data: 'Down payment inmediatamente inferior al umbral.', steps: ['Abrir Request Loan', 'Ingresar enganche insuficiente', 'Enviar'], expected: 'La solicitud muestra un resultado de rechazo y no se aprueba.', status: 'Pendiente', evidence: false },
]

export const initialFindings: Finding[] = [
  { id: 'H-01', summary: 'Transferencia permite exceder el saldo disponible (sin validación de fondos)', detail: 'Con la cuenta 28662 en $325.50 se transfirió $325.51 (saldo + 0.01) a 28773. Esperado (RF-09): la transferencia se rechaza y ningún saldo cambia. Obtenido: "Transfer Complete!" y la cuenta 28662 quedó en -$0.01.', severity: 'Alta', status: 'Registrado', evidenceImage: 'CP-09_H01_transferencia_sobregiro.jpg' },
  { id: 'H-02', summary: 'Bill Pay confirma el pago pero no descuenta el saldo ni registra la transacción', detail: 'Pago de $25.00 desde 28773 ($515.51). Esperado (RF-11): el pago se descuenta y queda registrado. Obtenido: "Bill Payment Complete", pero el saldo siguió en $515.51 y no aparece el débito en la actividad de la cuenta.', severity: 'Media', status: 'Registrado', evidenceImage: 'CP-11_H02_billpay_no_descuenta.jpg' },
  { id: 'H-03', summary: 'Bill Pay con monto mayor al saldo produce error interno y deja el resumen inoperable', detail: 'Pago de $1000.00 (mayor al saldo) desde 28773. Esperado (RF-13): rechazo con validación comprensible y saldo sin cambios. Obtenido: "An internal error has occurred and has been logged." y el Accounts Overview quedó devolviendo el mismo error de forma persistente.', severity: 'Alta', status: 'Registrado', evidenceImage: 'CP-13_H03_overview_roto.jpg' },
]

export const navItems: { key: NavKey; label: string; icon: string }[] = [
  { key: 'overview', label: 'Resumen', icon: 'grid' },
  { key: 'plan', label: 'Funciones', icon: 'clipboard' },
  { key: 'traceability', label: 'Requisitos', icon: 'route' },
  { key: 'cases', label: 'Casos', icon: 'check' },
  { key: 'execution', label: 'Ejecución', icon: 'play' },
  { key: 'findings', label: 'Hallazgos', icon: 'clipboard' },
]
