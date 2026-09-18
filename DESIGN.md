# Design direction · ParaBank QA Lab

## Idea

Una mesa de trabajo de pruebas para un sistema bancario real. La interfaz debe parecer una herramienta que un equipo de QA usa para revisar evidencia, no una landing page ni un dashboard genérico.

## Material y color

- Fondo: gris Apple `#f5f5f7`.
- Tinta principal: negro suave `#1d1d1f`.
- Señal de riesgo: gris medio `#636366`.
- Confirmación: gris medio `#515154`.
- Superficies: blanco y gris muy claro.
- Profundidad mínima; el contenido se separa con reglas, tipografía y espacio.
- Encabezados: Avenir Next, con peso moderado y tracking natural.
- Texto e interfaz: SF Pro Text o el sistema nativo como respaldo.

## Composición

- Navegación lateral sobria en escritorio y navegación inferior táctil en móvil.
- Sin logotipo decorativo; el contexto se comunica con texto directo.
- Encabezados directos, sin slogans ni micro-eyebrow como decoración.
- Etiquetas en estilo oración, nunca en mayúsculas espaciadas.
- Ritmo amplio entre grupos; densidad contenida dentro de las tablas.
- Las tablas y listas son la estructura principal.
- Tarjetas solo cuando agrupan una acción o una unidad de evidencia.
- Cada tarjeta móvil sigue el orden identificador, título, contexto y resultado.
- Radios contenidos entre 10 y 16px; sombras suaves y discretas.

## Voz

Directa y específica: “Casos de prueba”, “Ejecución crítica”, “Matriz de trazabilidad”. Evitar frases de marketing, claims no verificables y estados de ejecución inventados.

## Interacción

- Navegación por secciones sin cambiar de ruta para mantener el ritmo de revisión.
- Filtros por prioridad y funcionalidad.
- Detalle de caso visible al seleccionarlo.
- Veredictos y evidencia persistidos localmente para que el dashboard sirva durante la ejecución manual.
