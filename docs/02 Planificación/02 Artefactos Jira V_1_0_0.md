[← Volver al README Principal](../../README.md)

# Artefactos Jira

**Proyecto:** EcoLogística Lima – Optimizador de Rutas Sostenibles para DistriRápido S.A.C.
**Versión:** 1.1.0 | **Fecha:** 19/11/2026

**Proyecto Jira:** *Mi equipo de software* (clave `KAN`, espacio de software gestionado por el equipo) — tablero `KAN board`.

> ⚠️ **Capturas pendientes.** Los datos de cada sección se tomaron del proyecto Jira real el 19/11/2026. Falta insertar las capturas de pantalla tomadas directamente de Jira. Ninguna captura puede ser generada artificialmente: la consigna exige evidencia funcional de una configuración real.
>
> **Política estricta de recorte:** cada imagen debe estar recortada exclusivamente al panel/contenedor del elemento de Jira a demostrar — sin escritorio, sin barra de tareas del sistema operativo, sin pestañas del navegador ni espacio sobrante. El incumplimiento resta el 50% del puntaje de la sección.
>
> Guarda las imágenes en la carpeta `docs/02 Planificación/img/` (créala al tomar la primera captura) y reemplaza cada marcador `[INSERTAR CAPTURA AQUÍ]` por `![descripción](img/nombre-archivo.png)`.

## Control de Versiones del Documento

| Versión | Fecha | Descripción del Cambio |
|:---:|:---:|:---|
| 1.0.0 | 05/10/2026 | Plantilla inicial y Sprint Goal del Sprint 1. |
| 1.1.0 | 19/11/2026 | Descripciones completadas con los datos reales de Jira tras el cierre del Sprint 3 y el inicio del Sprint 4. |

## Evidencia 1: Roadmap del Proyecto

*Mapeo de las Épicas (EP-01 a EP-04) en la línea de tiempo del proyecto (vista **Cronograma** de Jira).*

`[INSERTAR CAPTURA AQUÍ — vista Cronograma de Jira, recortada]`

**Descripción:** El cronograma cubre del **05/10/2026 al 17/11/2026** (Sprints 1 a 4). Las cuatro épicas se distribuyen así:

| Clave | Épica | Inicio | Fin | Estado |
|---|---|:---:|:---:|---|
| KAN-4 | [EP-01] Gestión de Puntos de Entrega y Rutas | 05/10/2026 | 01/11/2026 | Finalizado |
| KAN-5 | [EP-02] Motor de Optimización de Rutas | 05/10/2026 | 17/11/2026 | En curso (EN-02 en revisión) |
| KAN-6 | [EP-03] Visualización en Mapa | 19/10/2026 | 17/11/2026 | Finalizado |
| KAN-7 | [EP-04] Panel de Gestión del Operador | 19/10/2026 | 17/11/2026 | En curso (EN-03 en revisión) |

EP-01 y EP-02 arrancan en el Sprint 1; EP-03 y EP-04 en el Sprint 2. EP-02, EP-03 y EP-04 se extienden hasta el Sprint 4 porque contienen trabajo de consolidación de ese sprint.

## Evidencia 2: Backlog Priorizado

*Vista general del backlog con Story Points estimados (secuencia de Fibonacci) y épica asignada, según la tabla de la sección 2 de [01 Transformando a ágil](01%20Transformando%20a%20ágil%20V_1_0_0.md).*

`[INSERTAR CAPTURA AQUÍ — panel de Backlog de Jira, recortado]`

**Descripción:** El backlog del PMV contiene **11 historias y 49 Story Points**, ordenadas por prioridad (High → Medium → Low):

| Clave | Ítem | Épica | SP | Prioridad | Sprint |
|---|---|---|:---:|---|---|
| KAN-8 | US-001 Registrar puntos de entrega | EP-01 | 3 | High | Sprint 1 |
| KAN-9 | US-003 Generar ruta optimizada | EP-02 | 8 | High | Sprint 1 |
| KAN-10 | EN-01 Optimizar rendimiento del ruteo | EP-02 | 5 | High | Sprint 1 |
| KAN-11 | EN-02 Autenticación segura (JWT + HTTPS) | EP-02 | 5 | High | Sprint 1 → 2 → 4 |
| KAN-12 | US-004 Impacto ambiental (CO₂) | EP-02 | 5 | High | Sprint 2 |
| KAN-13 | US-005 Ruta en mapa interactivo | EP-03 | 5 | High | Sprint 2 |
| KAN-14 | US-002 Editar o eliminar una ruta | EP-01 | 3 | Medium | Sprint 2 |
| KAN-15 | US-007 Listar y buscar rutas | EP-04 | 3 | Medium | Sprint 2 |
| KAN-16 | US-006 Detalle de cada parada | EP-03 | 2 | Medium | Sprint 3 |
| KAN-17 | EN-03 Pipeline CI/CD a Staging | EP-04 | 8 | Medium | Sprint 3 → 4 |
| KAN-18 | US-008 Exportar resumen de ruta | EP-04 | 2 | Low | Sprint 3 |

## Evidencia 3: Sprint Planning & Sprint Goal

*Ítems seleccionados para cada sprint y la meta (Sprint Goal) registrada en la cabecera del sprint.*

`[INSERTAR CAPTURA AQUÍ — panel de Sprint Planning de Jira, recortado]`

**Sprint Goal propuesto (Sprint 1):**
> Contar con un flujo end-to-end mínimo funcional: el operador puede registrar puntos de entrega, el backend calcula una ruta optimizada básica, y ese acceso queda protegido por autenticación — sentando las bases de rendimiento y seguridad sobre las que se construirán la visualización en mapa y el resto del panel en los sprints siguientes.

**Ítems incluidos en Sprint 1:** US-001, US-003, EN-01, EN-02 (21 Story Points — ver sección 2 de [01 Transformando a ágil](01%20Transformando%20a%20ágil%20V_1_0_0.md)).

**Calendario de sprints registrado en Jira:**

| Sprint | Inicio | Fin | Estado en Jira | Sprint Goal |
|---|:---:|:---:|---|---|
| Sprint 1 | 05/10/2026 | 18/10/2026 | Cerrado | Flujo end-to-end mínimo (texto anterior). |
| Sprint 2 | 19/10/2026 | 01/11/2026 | Cerrado | Que el operador visualice la ruta optimizada en un mapa interactivo junto con su impacto ambiental estimado (CO₂), y pueda listar, buscar, editar y eliminar sus rutas guardadas. |
| Sprint 3 | 02/11/2026 | 08/11/2026 | Cerrado | Completar el PMV: detalle de cada parada en el mapa, exportación del resumen de la ruta y pipeline CI/CD con despliegue a Staging (hito H5). |
| Sprint 4 | 09/11/2026 | 17/11/2026 | Activo | Consolidar la calidad del PMV: suite E2E multinavegador (Playwright), métricas de rendimiento y resiliencia, instrumento SUS, workflows de CI/CD hacia Producción y documentación del sprint. |

El Sprint 0 — Base del proyecto (01/10/2026 – 04/10/2026) corresponde al hito H3 del Acta de Constitución y no se registra como sprint Scrum, por no contener historias del backlog.

Al cerrar el Sprint 3, **EN-02 (KAN-11)** y **EN-03 (KAN-17)** quedaron incompletos y se trasladaron al Sprint 4, con un comentario en cada tarjeta que explica lo pendiente. El Sprint 4 no incorpora historias nuevas: sus entregables técnicos se registraron como **Tareas** `ET-S4-01` a `ET-S4-06` (KAN-19 a KAN-24), con la etiqueta `sprint-4`, según la [Revisión del Sprint 4](../03%20Implementación/Sprint%2004/01%20Revisión%20del%20Sprint%20V_1_0_0.md).

## Evidencia 4: Tablero Scrum Activo

*Flujo de trabajo con tarjetas distribuidas en las columnas del tablero: Por hacer → En curso → En revisión → Finalizado.*

`[INSERTAR CAPTURA AQUÍ — tablero Scrum de Jira (Sprint 4), recortado]`

**Descripción:** Tablero del **Sprint 4** con 8 tarjetas al 19/11/2026:

| Columna | Tarjetas | Detalle |
|---|:---:|---|
| Por hacer | 0 | — |
| En curso | 1 | KAN-21 ET-S4-03 Instrumento SUS (preparado, falta aplicarlo a participantes reales). |
| En revisión | 3 | KAN-11 EN-02, KAN-17 EN-03, KAN-22 ET-S4-04 Workflows de CI/CD (sin ejecución en GitHub ni proveedor de despliegue). |
| Finalizado | 4 | KAN-19 ET-S4-01 Suite E2E, KAN-20 ET-S4-02 Rendimiento y resiliencia, KAN-23 ET-S4-05 Limpieza del repositorio, KAN-24 ET-S4-06 Documentación. |

## Evidencia 5: Gestión de Versiones / Release

*Vista del módulo de Publicaciones (Releases) mostrando la versión creada (`v1.0.0-MVP`) y sus historias asociadas.*

`[INSERTAR CAPTURA AQUÍ — panel de Publicaciones de Jira, recortado]`

**Descripción:** Versión **`v1.0.0-MVP`** — *PMV completo de EcoLogística Lima (hito H5): EP-01 a EP-04, 11 ítems, 49 Story Points.* Tiene **11 historias asociadas** (KAN-8 a KAN-18), con inicio el 05/10/2026 y fecha de publicación prevista el 08/11/2026. La versión sigue **sin publicar** porque dos ítems, EN-02 y EN-03 (13 SP), están en revisión; por eso Jira la marca como vencida. 9 de 11 ítems (36 de 49 SP) están finalizados.

---

[← Volver al README Principal](../../README.md)
