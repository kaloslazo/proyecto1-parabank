import { FormEvent, ReactNode, useEffect, useMemo, useState } from 'react'
import { clientFunctionalities, clientNonFunctionalRequirements, clientRequirements, Finding, initialCases, initialFindings, navItems, NavKey, Priority, requirements, TestCase, TestStatus } from './data'

const priorityClass: Record<Priority, string> = { Alta: 'high', Media: 'medium', Baja: 'low' }
const statusClass: Record<TestStatus, string> = { Pendiente: 'pending', 'Pasó': 'passed', 'Falló': 'failed', Bloqueado: 'blocked' }

function Icon({ name, size = 18 }: { name: string; size?: number }) {
  const paths: Record<string, ReactNode> = {
    grid: <><rect x="3" y="3" width="7" height="7" rx="1.5" /><rect x="14" y="3" width="7" height="7" rx="1.5" /><rect x="3" y="14" width="7" height="7" rx="1.5" /><rect x="14" y="14" width="7" height="7" rx="1.5" /></>,
    clipboard: <><rect x="5" y="4" width="14" height="17" rx="2" /><path d="M9 4.5V3h6v1.5M8.5 10h7M8.5 14h7M8.5 18h4" /></>,
    route: <><circle cx="5" cy="5" r="2" /><circle cx="19" cy="19" r="2" /><path d="M7 5h6a4 4 0 0 1 4 4v2a4 4 0 0 1-4 4H9a4 4 0 0 0-4 4v0" /></>,
    check: <><circle cx="12" cy="12" r="9" /><path d="m8 12 2.5 2.5L16 9" /></>,
    play: <><circle cx="12" cy="12" r="9" /><path d="m10 8 5 4-5 4V8Z" /></>,
    spark: <><path d="m12 3 1.5 5.5L19 10l-5.5 1.5L12 17l-1.5-5.5L5 10l5.5-1.5L12 3Z" /><path d="m19 16 .6 2.4L22 19l-2.4.6L19 22l-.6-2.4L16 19l2.4-.6L19 16Z" /></>,
    external: <><path d="M14 4h6v6M20 4l-9 9" /><path d="M18 13v5a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h5" /></>,
    arrow: <><path d="M5 12h13M13 6l6 6-6 6" /></>,
    plus: <><path d="M12 5v14M5 12h14" /></>,
    clock: <><circle cx="12" cy="12" r="9" /><path d="M12 7v5l3 2" /></>,
    shield: <><path d="M12 3 20 6v5c0 5-3.3 8.2-8 10-4.7-1.8-8-5-8-10V6l8-3Z" /><path d="m8.5 12 2.2 2.2 4.8-5" /></>,
    filter: <><path d="M4 6h16M7 12h10M10 18h4" /></>,
    close: <><path d="m6 6 12 12M18 6 6 18" /></>,
    sun: <><circle cx="12" cy="12" r="3.5" /><path d="M12 2v2M12 20v2M4.93 4.93l1.42 1.42M17.65 17.65l1.42 1.42M2 12h2M20 12h2M4.93 19.07l1.42-1.42M17.65 6.35l1.42-1.42" /></>,
    moon: <path d="M20.5 14.5A8.5 8.5 0 0 1 9.5 3.5 8.5 8.5 0 1 0 20.5 14.5Z" />,
  }
  return <svg aria-hidden="true" width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">{paths[name] ?? paths.spark}</svg>
}

function Badge({ children, tone = 'neutral' }: { children: ReactNode; tone?: string }) {
  return <span className={`badge ${tone}`}>{children}</span>
}

function ProgressBar({ value, tone = 'plum' }: { value: number; tone?: string }) {
  return <div className="progress-track"><span className={`progress-fill ${tone}`} style={{ width: `${value}%` }} /></div>
}

function App() {
  const [activeNav, setActiveNav] = useState<NavKey>('overview')
  const [theme, setTheme] = useState<'light' | 'dark'>(() => {
    const saved = localStorage.getItem('parabank-theme')
    if (saved === 'light' || saved === 'dark') return saved
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
  })
  const [cases, setCases] = useState<TestCase[]>(() => loadLocal('parabank-cases', initialCases))
  const [findings, setFindings] = useState<Finding[]>(() => loadLocal('parabank-findings', initialFindings))
  const [selectedCase, setSelectedCase] = useState<TestCase | null>(null)
  const [caseFilter, setCaseFilter] = useState('Todos')
  const [showFindingForm, setShowFindingForm] = useState(false)
  const [notice, setNotice] = useState('')

  const highCases = cases.filter((item) => item.priority === 'Alta')

  useEffect(() => { localStorage.setItem('parabank-cases', JSON.stringify(cases)) }, [cases])
  useEffect(() => { localStorage.setItem('parabank-findings', JSON.stringify(findings)) }, [findings])
  useEffect(() => {
    document.documentElement.dataset.theme = theme
    document.documentElement.style.colorScheme = theme
    document.querySelector('meta[name="theme-color"]')?.setAttribute('content', theme === 'dark' ? '#111113' : '#f5f5f7')
    localStorage.setItem('parabank-theme', theme)
  }, [theme])

  const filteredCases = useMemo(() => {
    if (caseFilter === 'Todos') return cases
    if (['Alta', 'Media', 'Baja'].includes(caseFilter)) return cases.filter((item) => item.priority === caseFilter)
    return cases.filter((item) => item.feature === caseFilter)
  }, [caseFilter, cases])

  function navigateTo(key: NavKey) {
    setActiveNav(key)
    window.requestAnimationFrame(() => window.scrollTo({ top: 0, behavior: 'auto' }))
  }

  function updateStatus(id: string, status: TestStatus) {
    setCases((current) => current.map((item) => item.id === id ? { ...item, status } : item))
    setNotice(`Resultado guardado para ${id}.`)
    window.setTimeout(() => setNotice(''), 2600)
  }

  function toggleEvidence(id: string) {
    setCases((current) => current.map((item) => item.id === id ? { ...item, evidence: !item.evidence } : item))
    setNotice(`Evidencia actualizada para ${id}.`)
    window.setTimeout(() => setNotice(''), 2600)
  }

  function addFinding(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const form = new FormData(event.currentTarget)
    const summary = String(form.get('summary') || '').trim()
    const detail = String(form.get('detail') || '').trim()
    if (!summary || !detail) return
    setFindings((current) => [...current, { id: `OBS-${String(current.length + 1).padStart(2, '0')}`, summary, detail, severity: String(form.get('severity')) as Priority, status: 'Registrado' }])
    setShowFindingForm(false)
    setNotice('Hallazgo añadido a la bitácora.')
    window.setTimeout(() => setNotice(''), 2600)
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="project-label"><strong>Proyecto 1</strong><small>Pruebas de software</small></div>
        <div className="sidebar-section-label">Primer avance</div>
        <nav className="main-nav" aria-label="Navegación principal">
          {navItems.slice(0, 3).map((item) => <button key={item.key} aria-label={item.label} title={item.label} className={activeNav === item.key ? 'nav-item active' : 'nav-item'} onClick={() => navigateTo(item.key)}><Icon name={item.icon} /><span>{item.label}</span></button>)}
        </nav>
        <div className="sidebar-section-label later-label">Proyecto completo</div>
        <nav className="main-nav secondary-nav" aria-label="Etapas posteriores">
          {navItems.slice(3).map((item) => <button key={item.key} aria-label={item.label} title={item.label} className={activeNav === item.key ? 'nav-item active' : 'nav-item'} onClick={() => navigateTo(item.key)}><Icon name={item.icon} /><span>{item.label}</span></button>)}
        </nav>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div className="breadcrumbs"><span>CS5383</span><b>/</b><span>Proyecto 1</span><b>/</b><strong>Caso 1</strong></div>
          <div className="topbar-actions">
            <span className="topbar-label">Primer avance</span>
            <button
              className="theme-toggle"
              type="button"
              aria-label={theme === 'light' ? 'Activar modo oscuro' : 'Activar modo claro'}
              title={theme === 'light' ? 'Activar modo oscuro' : 'Activar modo claro'}
              onClick={() => setTheme((current) => current === 'light' ? 'dark' : 'light')}
            >
              <Icon name={theme === 'light' ? 'moon' : 'sun'} size={17} />
              <span>{theme === 'light' ? 'Oscuro' : 'Claro'}</span>
            </button>
          </div>
        </header>
        {notice && <div className="toast" role="status"><Icon name="check" size={16} />{notice}</div>}
        {activeNav === 'overview' && <Overview onNavigate={navigateTo} />}
        {activeNav === 'plan' && <Functionalities />}
        {activeNav === 'traceability' && <ClientRequirements />}
        {activeNav === 'cases' && <Cases cases={filteredCases} filter={caseFilter} setFilter={setCaseFilter} selectedCase={selectedCase} setSelectedCase={setSelectedCase} />}
        {activeNav === 'execution' && <Execution cases={highCases} updateStatus={updateStatus} toggleEvidence={toggleEvidence} />}
        {activeNav === 'findings' && <Findings findings={findings} showForm={showFindingForm} setShowForm={setShowFindingForm} onSubmit={addFinding} />}
      </main>
    </div>
  )
}

function loadLocal<T>(key: string, fallback: T): T {
  try {
    const saved = localStorage.getItem(key)
    return saved ? JSON.parse(saved) as T : fallback
  } catch {
    return fallback
  }
}

function PageIntro({ title, description, action }: { eyebrow?: string; title: string; description: string; action?: ReactNode }) {
  return <div className="page-intro"><div><h1>{title}</h1><p>{description}</p></div>{action && <div className="intro-action">{action}</div>}</div>
}

function Overview({ onNavigate }: { onNavigate: (key: NavKey) => void }) {
  return <>
    <PageIntro title="Primer avance" description="Requisitos del cliente detallados para el Caso 1 de ParaBank." action={<a className="button primary" href="https://parabank.parasoft.com/parabank/index.htm" target="_blank" rel="noreferrer">Abrir ParaBank <Icon name="external" size={16} /></a>} />
    <section className="case-sheet">
      <div className="sheet-intro"><div><h2>Requisitos del cliente</h2><p>El alcance se organiza en ocho funcionalidades, con requisitos funcionales verificables y tres condiciones no funcionales de calidad.</p></div><dl className="sheet-meta"><div><dt>Equipo</dt><dd>Kalos Lazo y Gianpier Segovia</dd></div><div><dt>Formato</dt><dd>Requisito funcional (RF)</dd></div><div><dt>Uso</dt><dd>Apoyo para la exposición</dd></div></dl></div>
      <div className="sheet-stats"><div><span>Funcionalidades</span><strong>8/8</strong></div><div><span>Requisitos funcionales</span><strong>{clientRequirements.length}</strong></div><div><span>Requisitos no funcionales</span><strong>{clientNonFunctionalRequirements.length}</strong></div><div><span>Prioridad alta</span><strong>{clientRequirements.filter((item) => item.priority === 'Alta').length}</strong></div></div>
      <div className="sheet-workspace"><div className="risk-table"><div className="sheet-section-head"><div><span className="micro-label">Mapa de funcionalidades</span><h3>Todo el alcance está cubierto</h3></div><button className="text-button" onClick={() => onNavigate('plan')}>Ver tabla completa <Icon name="arrow" size={16} /></button></div><div className="risk-column-head functionality-column-head"><span>ID</span><span>Funcionalidad y ubicación</span><span>RF</span></div>{clientFunctionalities.map((item) => <div className="risk-table-row functionality-summary-row" key={item.id}><span className="risk-id">{item.id}</span><div><strong>{item.name}</strong><small>{item.location}</small></div><span className="rf-count">{item.requirementIds.length}</span></div>)}</div><aside className="presentation-guide"><section className="guide-panel"><span className="guide-index">1</span><div><span className="micro-label">Formato de entrega</span><h3>Requisitos funcionales</h3><p>Cada requisito incluye actor, datos y reglas, resultado esperado y prioridad.</p><button className="text-button" onClick={() => onNavigate('traceability')}>Revisar los requisitos <Icon name="arrow" size={15} /></button></div></section><section className="guide-panel"><span className="guide-index">2</span><div><span className="micro-label">Durante la exposición</span><h3>Recorrido recomendado</h3><div className="compact-actions"><button onClick={() => onNavigate('plan')}><span>1</span>Mostrar las funcionalidades <Icon name="arrow" size={14} /></button><button onClick={() => onNavigate('traceability')}><span>2</span>Explicar los requisitos <Icon name="arrow" size={14} /></button><a href="https://parabank.parasoft.com/parabank/index.htm" target="_blank" rel="noreferrer"><span>3</span>Abrir el sistema real <Icon name="external" size={14} /></a></div></div></section></aside></div>
    </section>
  </>
}

function Metric({ label, value, detail, tone }: { label: string; value: string; detail: string; tone: string }) {
  return <div className={`metric-card ${tone}`}><span>{label}</span><strong>{value}</strong><small>{detail}</small></div>
}

function Functionalities() {
  return <><PageIntro title="Funcionalidades identificadas" description="El mapa completo del alcance funcional de ParaBank, en el orden recomendado para exponer." action={<Badge tone="mint">{clientFunctionalities.length} de 8</Badge>} /><div className="functionality-note"><Icon name="clipboard" size={20} /><div><strong>Formato elegido: requisito funcional</strong><p>Las ocho funcionalidades usan la misma estructura RF indicada en la guía.</p></div></div><div className="functionality-table"><div className="functionality-head"><span>ID</span><span>Funcionalidad</span><span>Dónde se encuentra en el sistema real</span><span>Actor</span><span>RF</span></div>{clientFunctionalities.map((item) => <div className="functionality-row" key={item.id}><span className="functionality-id" data-label="ID">{item.id}</span><div className="functionality-title" data-label="Funcionalidad"><strong>{item.name}</strong></div><span className="functionality-location" data-label="Ubicación">{item.location}</span><span className="functionality-actor" data-label="Actor">{item.actor}</span><span className="rf-count" data-label="Requisitos">{item.requirementIds.length}</span></div>)}</div><div className="functionality-foot"><span>Alcance completo</span><strong>8 funcionalidades, {clientRequirements.length} requisitos verificables</strong><span>La exposición sigue este orden.</span></div></>
}

function ClientRequirements() {
  const [activeFunctionality, setActiveFunctionality] = useState(clientFunctionalities[0].id)
  const current = clientFunctionalities.find((item) => item.id === activeFunctionality) ?? clientFunctionalities[0]
  const currentRequirements = clientRequirements.filter((item) => item.functionalityId === current.id)
  return <><PageIntro title="Requisitos del cliente" description="Los RF describen lo que hace el sistema. Los RNF establecen las condiciones de calidad que también indica el caso." action={<Badge tone="plum">{clientRequirements.length} RF + {clientNonFunctionalRequirements.length} RNF</Badge>} /><div className="rf-layout"><aside className="rf-nav"><span className="micro-label">Funcionalidades</span>{clientFunctionalities.map((item) => <button key={item.id} className={activeFunctionality === item.id ? 'rf-nav-item active' : 'rf-nav-item'} onClick={() => setActiveFunctionality(item.id)}><span>{item.id}</span><strong>{item.name}</strong><small>{item.requirementIds.length} requisitos</small></button>)}</aside><section className="rf-panel" data-functionality={current.id}><div className="rf-panel-head"><div><span className="functionality-id">{current.id}</span><h2>{current.name}</h2><p><strong>Dónde se usa:</strong> {current.location}</p></div><Badge tone="mint">{currentRequirements.length} RF</Badge></div><div className="rf-table-wrap"><div className="rf-table"><div className="rf-head"><span>ID</span><span>Requisito verificable</span><span>Actor</span><span>Datos y reglas</span><span>Resultado esperado</span><span>Prioridad</span></div>{currentRequirements.map((item) => <div className="rf-row" key={item.id}><span className="rf-id" data-label="ID">{item.id}</span><p data-label="Requisito">{item.requirement}</p><span data-label="Actor">{item.actor}</span><p data-label="Datos y reglas">{item.dataRules}</p><p data-label="Resultado esperado">{item.expected}</p><span data-label="Prioridad"><Badge tone={priorityClass[item.priority]}>{item.priority}</Badge></span></div>)}</div></div></section></div><section className="nfr-section"><div className="nfr-section-head"><div><h2>Requisitos no funcionales</h2><p>Condiciones de calidad indicadas en el enunciado del Caso 1.</p></div><Badge tone="neutral">{clientNonFunctionalRequirements.length} RNF</Badge></div><div className="nfr-table"><div className="nfr-head"><span>ID</span><span>Condición</span><span>Requisito</span><span>Cómo se verifica</span><span>Prioridad</span></div>{clientNonFunctionalRequirements.map((item) => <div className="nfr-row" key={item.id}><span className="nfr-id">{item.id}</span><strong className="nfr-category">{item.category}</strong><p className="nfr-requirement">{item.requirement}</p><p className="nfr-verification">{item.verification}</p><span className="nfr-priority"><Badge tone={priorityClass[item.priority]}>{item.priority}</Badge></span></div>)}</div></section></>
}

function Plan() {
  return <><PageIntro eyebrow="01 · Planificación" title="Plan de pruebas" description="Alcance, estrategia y condiciones para probar el caso de banca digital." /><section className="plan-grid"><div className="plan-main"><div className="plan-callout"><Icon name="shield" size={24} /><div><span className="micro-label">Qué se protege</span><h3>Que ninguna operación crítica pierda consistencia.</h3><p>Validar registro, autenticación, apertura de cuentas, transferencias, bill pay, préstamos, historial y perfil en el sistema real.</p></div></div><div className="plan-section"><div className="section-heading"><div><span className="micro-label">Método</span><h3>Riesgo primero</h3></div><Badge tone="plum">Caja negra</Badge></div><div className="strategy-points"><div><span>01</span><strong>Profundidad en dinero</strong><p>Sistema e integración sobre débito, crédito, saldo e historial.</p></div><div><span>02</span><strong>Datos controlados</strong><p>Cuentas ficticias con saldos conocidos y operaciones identificables.</p></div><div><span>03</span><strong>Evidencia útil</strong><p>Capturas antes/después y registro de resultado para cada caso alto.</p></div></div></div></div><aside className="plan-side"><div className="side-block"><span className="micro-label">Entrada</span><ul><li>URL operativa y navegador estable</li><li>Cuenta de prueba registrada</li><li>Dos cuentas propias con saldo conocido</li><li>Datos ficticios para beneficiario</li></ul></div><div className="side-block"><span className="micro-label">Salida</span><ul><li>100% de requisitos trazados</li><li>Casos altos ejecutados</li><li>Hallazgos con evidencia</li><li>Recomendación para automatizar</li></ul></div><div className="timeline"><span className="micro-label">Ruta</span><div><b>Hoy</b><span>Análisis y diseño inicial</span></div><div><b>Próximo</b><span>Ejecución manual crítica</span></div><div><b>Después</b><span>Informe y Proyecto 2</span></div></div></aside></section></>
}

function Traceability() {
  return <><PageIntro eyebrow="02 · Análisis" title="Matriz de trazabilidad" description="Requisitos, condiciones derivadas y casos relacionados en una sola vista." action={<Badge tone="mint">Cobertura 100%</Badge>} /><div className="table-shell"><div className="table-toolbar"><div><strong>Matriz de trazabilidad</strong><span>10 requisitos · 20 casos relacionados</span></div><div className="toolbar-note"><span className="dot-key high-dot" /> Alto <span className="dot-key medium-dot" /> Medio</div></div><div className="trace-table"><div className="trace-head"><span>ID</span><span>Base de prueba</span><span>Condiciones derivadas</span><span>Riesgo</span><span>Casos</span></div>{requirements.map((item) => <div className="trace-row" key={item.id}><span className="trace-id">{item.id}</span><div><strong>{item.title}</strong><small>{item.type}</small></div><div className="condition-copy">{item.rationale}</div><Badge tone={priorityClass[item.risk]}>{item.risk}</Badge><div className="case-pills">{item.coveredBy.map((id) => <span key={id}>{id}</span>)}</div></div>)}</div></div><div className="analysis-note"><div className="note-icon"><Icon name="spark" size={20} /></div><div><strong>Decisión de análisis</strong><p>Las prioridades altas se concentran en operaciones que pueden modificar dinero o permitir acceso indebido. La búsqueda, perfil y préstamos mantienen cobertura porque sostienen trazabilidad y decisiones posteriores.</p></div></div></>
}

function Cases({ cases, filter, setFilter, selectedCase, setSelectedCase }: { cases: TestCase[]; filter: string; setFilter: (value: string) => void; selectedCase: TestCase | null; setSelectedCase: (value: TestCase | null) => void }) {
  const filterOptions = ['Todos', 'Alta', 'Media', 'Registro', 'Transferencia', 'Bill pay', 'Apertura de cuenta', 'Historial', 'Préstamos', 'Perfil', 'Rendimiento', 'Sesión']
  return <><PageIntro eyebrow="03 · Diseño" title="Casos de prueba" description="Cada caso conecta una condición, una técnica y un resultado esperado. Selecciona uno para revisar su ficha." action={<Badge tone="plum">{cases.length} visibles</Badge>} /><div className="case-toolbar"><div className="filter-label"><Icon name="filter" size={16} /><span>Filtrar por</span></div><div className="filter-scroll">{filterOptions.map((item) => <button key={item} className={filter === item ? 'filter-pill selected' : 'filter-pill'} onClick={() => setFilter(item)}>{item}</button>)}</div></div><section className="cases-layout"><div className="case-list">{cases.map((item) => <button className={selectedCase?.id === item.id ? 'case-row selected' : 'case-row'} key={item.id} onClick={() => setSelectedCase(item)}><div className="case-row-top"><span className="case-id">{item.id}</span><Badge tone={priorityClass[item.priority]}>{item.priority}</Badge></div><strong>{item.condition}</strong><div className="case-row-bottom"><span>{item.feature}</span><span>{item.technique}</span><span className={`status-dot ${statusClass[item.status]}`} />{item.status}</div></button>)}</div>{selectedCase ? <CaseDetail item={selectedCase} close={() => setSelectedCase(null)} /> : <div className="empty-detail"><div className="empty-blob"><Icon name="check" size={28} /></div><h3>Selecciona un caso</h3><p>Aquí verás precondiciones, datos, pasos y resultado esperado para exponerlo o ejecutarlo.</p></div>}</section></>
}

function CaseDetail({ item, close }: { item: TestCase; close: () => void }) {
  return <aside className="case-detail"><div className="detail-top"><div><span className="case-id">{item.id}</span><Badge tone={priorityClass[item.priority]}>{item.priority}</Badge></div><button className="icon-button" onClick={close} aria-label="Cerrar detalle"><Icon name="close" size={17} /></button></div><h2>{item.condition}</h2><div className="detail-meta"><span>{item.feature}</span><span>{item.technique}</span></div><DetailBlock label="Precondiciones" value={item.preconditions} /><DetailBlock label="Datos de prueba" value={item.data} /><div className="detail-block"><span className="micro-label">Pasos</span><ol>{item.steps.map((step, index) => <li key={step}><span>{index + 1}</span>{step}</li>)}</ol></div><div className="expected-box"><span className="micro-label">Resultado esperado</span><p>{item.expected}</p></div></aside>
}

function DetailBlock({ label, value }: { label: string; value: string }) { return <div className="detail-block"><span className="micro-label">{label}</span><p>{value}</p></div> }

function Execution({ cases, updateStatus, toggleEvidence }: { cases: TestCase[]; updateStatus: (id: string, status: TestStatus) => void; toggleEvidence: (id: string) => void }) {
  return <><PageIntro eyebrow="04 · Ejecución" title="Ejecución crítica" description="Solo se ejecutan primero los casos de prioridad alta. Cada veredicto necesita evidencia del sistema real." action={<Badge tone="high">{cases.filter((item) => item.status !== 'Pendiente').length}/{cases.length} listos</Badge>} /><div className="execution-banner"><div className="banner-icon"><Icon name="play" size={21} /></div><div><strong>Antes / operación / después</strong><span>Registra saldo inicial, confirmación, saldo final e historial.</span></div><a className="text-button" href="https://parabank.parasoft.com/parabank/index.htm" target="_blank" rel="noreferrer">Ir a ParaBank <Icon name="external" size={15} /></a></div><div className="execution-list">{cases.map((item) => <div className="execution-card" key={item.id}><div className="execution-head"><div><span className="case-id">{item.id}</span><h3>{item.condition}</h3></div><Badge tone={statusClass[item.status]}>{item.status}</Badge></div><div className="execution-info"><div><span className="micro-label">Resultado esperado</span><p>{item.expected}</p></div><div><span className="micro-label">Evidencia</span><p className={item.evidence ? 'evidence-ready' : 'evidence-pending'}>{item.evidence ? 'Captura registrada' : 'Pendiente de captura'}</p></div></div><div className="execution-actions"><button className="evidence-chip" onClick={() => toggleEvidence(item.id)}><Icon name={item.evidence ? 'check' : 'clock'} size={15} />{item.evidence ? 'Evidencia lista' : 'Marcar evidencia'}</button><label>Veredicto<select value={item.status} onChange={(event) => updateStatus(item.id, event.target.value as TestStatus)}><option>Pendiente</option><option>Pasó</option><option>Falló</option><option>Bloqueado</option></select></label></div></div>)}</div></>
}

function Findings({ findings, showForm, setShowForm, onSubmit }: { findings: Finding[]; showForm: boolean; setShowForm: (value: boolean) => void; onSubmit: (event: FormEvent<HTMLFormElement>) => void }) {
  return <><PageIntro eyebrow="05 · Hallazgos" title="Hallazgos y evidencia" description="Registra lo que ocurrió en el sistema: defecto, validación ausente o confirmación importante." action={<button className="button primary" onClick={() => setShowForm(!showForm)}><Icon name="plus" size={16} /> Registrar hallazgo</button>} />{showForm && <form className="finding-form" onSubmit={onSubmit}><div><label>Resumen<input name="summary" placeholder="Ej. El saldo no se actualiza después de la transferencia" required /></label><label>Severidad<select name="severity" defaultValue="Media"><option>Alta</option><option>Media</option><option>Baja</option></select></label></div><label>Detalle y evidencia esperada<textarea name="detail" placeholder="Pasos, esperado vs obtenido y captura que falta..." required /></label><div className="form-actions"><button type="button" className="button ghost" onClick={() => setShowForm(false)}>Cancelar</button><button type="submit" className="button primary">Guardar observación</button></div></form>}<div className="finding-grid">{findings.map((item) => <article className="finding-card" key={item.id}><div className="finding-top"><span className="case-id">{item.id}</span><Badge tone={priorityClass[item.severity]}>{item.severity}</Badge></div><h3>{item.summary}</h3><p>{item.detail}</p><div className="finding-foot"><span className={`status-dot ${item.status === 'Registrado' ? 'passed' : 'pending'}`} />{item.status}<span className="foot-separator" /><span>Sin captura aún</span></div></article>)}<article className="method-card"><div className="method-illustration"><span>01</span><span>02</span><span>03</span></div><span className="micro-label">Formato de reporte</span><h3>Resumen → reproducción → evidencia</h3><p>La severidad se decide por impacto y prioridad, no por intuición.</p></article></div></>
}

export default App
