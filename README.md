# Proyecto 1 · ParaBank

Dashboard de trabajo para el Proyecto 1 de **Pruebas y Verificación de Software (CS5383)**.

El producto convierte el caso de banca digital en un espacio operativo para el primer avance y las siguientes etapas:

- documentar las 8 funcionalidades del alcance de ParaBank;
- presentar 22 requisitos verificables en formato RF, organizados por funcionalidad;

- planificar la estrategia de pruebas;
- mantener la matriz de trazabilidad;
- diseñar y filtrar casos de prueba;
- ejecutar primero los casos de prioridad alta;
- registrar hallazgos y evidencias pendientes.

## Ejecutar localmente

```bash
npm install
npm run dev
```

Para validar el build de producción:

```bash
npm run build
```

## Primer avance · 18/09/2026

La entrega inmediata usa un solo formato: **Requisito (RF)**. La vista `Funcionalidades` cubre todo el alcance del caso y la vista `Requisitos RF` contiene, para cada funcionalidad, ID, requisito verificable, actor, datos y reglas, resultado esperado y prioridad. No se mezclan RF con HU.

Las vistas de casos, ejecución y hallazgos quedan preparadas para las etapas posteriores; cualquier resultado se mantiene como `Pendiente` hasta ejecutarlo en ParaBank.

## Dirección visual

La interfaz usa una dirección Apple minimalista y monocromática. El resto se comporta como una mesa de trabajo de QA: fondo gris claro, tinta negra, reglas finas, tablas densas y estados explícitos. La profundidad separa niveles de trabajo; no se usa para decorar información vacía.

## Fuente de verdad del contenido

El contenido inicial se deriva de `Proyecto1_Enunciado_v2.pdf` y del Caso 1: Banca digital (ParaBank). Los resultados de ejecución aparecen como `Pendiente` hasta que el equipo pruebe el sistema real y registre evidencia.

## Próximas iteraciones

1. Completar usuario, grupo y datos de prueba reales.
2. Añadir capturas en la bitácora de ejecución.
3. Convertir la matriz y los casos a informe Word/PDF.
4. Seleccionar los flujos estables para automatización del Proyecto 2.
