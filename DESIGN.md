# Design direction · ParaBank QA Lab

## Idea

Una mesa de trabajo de pruebas para un sistema bancario real. La interfaz debe parecer una herramienta que un equipo de QA usa para revisar evidencia, no una landing page ni un dashboard genérico.

## Material y color

- Modo claro: lienzo gris Apple `#f5f5f7`, superficies blancas y tinta `#1d1d1f`.
- Modo oscuro: lienzo `#111113`, superficies `#1c1c1e` y tinta `#f5f5f7`.
- Señales y estados: grises medios, sin color decorativo.
- Profundidad plana: sin sombras, gradientes ni desenfoques.
- Cada bloque de contenido se contiene en una superficie con borde fino.
- Encabezados: Avenir Next, con peso moderado y tracking natural.
- Texto e interfaz: SF Pro Text o el sistema nativo como respaldo.

## Composición

- Navegación lateral sobria en escritorio y navegación inferior táctil en móvil.
- Sin logotipo decorativo; el contexto se comunica con texto directo.
- Encabezados directos, sin slogans ni micro-eyebrow como decoración.
- Etiquetas en estilo oración, nunca en mayúsculas espaciadas.
- Ritmo amplio entre grupos y una escala tipográfica estable; densidad contenida dentro de las tablas.
- Las tablas y listas son la estructura principal.
- Tarjetas solo cuando agrupan una acción o una unidad de evidencia.
- Cada tarjeta móvil sigue el orden identificador, título, contexto y resultado.
- Radios contenidos entre 10 y 16px; separación únicamente mediante fondo, borde y espacio.
- Sidebar fija durante el recorrido en escritorio; navegación inferior plana en móvil.

## Voz

Directa y específica: “Casos de prueba”, “Ejecución crítica”, “Matriz de trazabilidad”. Evitar frases de marketing, claims no verificables y estados de ejecución inventados.

## Interacción

- Navegación por secciones sin cambiar de ruta para mantener el ritmo de revisión.
- Filtros por prioridad y funcionalidad.
- Detalle de caso visible al seleccionarlo.
- Veredictos y evidencia persistidos localmente para que el dashboard sirva durante la ejecución manual.
