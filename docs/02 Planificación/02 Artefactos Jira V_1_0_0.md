[← Volver al README Principal](../../README.md)

# Artefactos Jira

**Proyecto:** EcoLogística Lima – Optimizador de Rutas Sostenibles para DistriRápido S.A.C.
**Versión:** 1.0.0 | **Fecha:** 12/11/2026
**Proyecto Jira:** `KAN` (tablero Scrum con Sprints, Estimación en Story Points, Backlog y Lanzamientos activados)

> ⚠️ **Capturas pendientes.** Las descripciones de este documento ya reflejan la configuración real del proyecto Jira. Las capturas deben tomarse directamente de Jira: la consigna exige evidencia funcional de una configuración real, por lo que ninguna puede generarse artificialmente.
>
> **Política estricta de recorte:** cada imagen debe estar recortada exclusivamente al panel/contenedor del elemento de Jira a demostrar — sin escritorio, sin barra de tareas del sistema operativo, sin pestañas del navegador ni espacio sobrante. El incumplimiento resta el 50% del puntaje de la sección.
>
> Guarda las imágenes en la carpeta `img/` junto a este documento (`docs/02 Planificación/img/`) con el nombre indicado en cada sección, y reemplaza el marcador `[INSERTAR CAPTURA AQUÍ …]` por `![descripción](img/nombre-archivo.png)`.

## Mapeo de elementos en Jira

| ID documento | Clave Jira | Tipo | Épica | SP | Sprint | Estado en Jira |
|---|---|---|---|:---:|---|---|
| EP-01 | KAN-4 | Épica | — | — | — | En curso |
| EP-02 | KAN-5 | Épica | — | — | — | Finalizado |
| EP-03 | KAN-6 | Épica | — | — | — | Finalizado |
| EP-04 | KAN-7 | Épica | — | — | — | En curso |
| US-001 | KAN-8 | Historia | EP-01 | 3 | Sprint 1 | Finalizado |
| US-003 | KAN-9 | Historia | EP-02 | 8 | Sprint 1 | Finalizado |
| EN-01 | KAN-10 | Historia (`Enabler`) | EP-02 | 5 | Sprint 1 | Finalizado |
| EN-02 | KAN-11 | Historia (`Enabler`) | EP-01 | 5 | Sprint 1 → 2 → 3 | En revisión |
| US-004 | KAN-12 | Historia | EP-02 | 5 | Sprint 2 | Finalizado |
| US-005 | KAN-13 | Historia | EP-03 | 5 | Sprint 2 | Finalizado |
| US-002 | KAN-14 | Historia | EP-01 | 3 | Sprint 2 | Finalizado |
| US-007 | KAN-15 | Historia | EP-04 | 3 | Sprint 2 | Finalizado |
| US-006 | KAN-16 | Historia | EP-03 | 2 | Sprint 3 | Finalizado |
| EN-03 | KAN-17 | Historia (`Enabler`) | EP-04 | 8 | Sprint 3 | En revisión |
| US-008 | KAN-18 | Historia | EP-04 | 2 | Sprint 3 | Finalizado |

Cada historia incluye en Jira su redacción ("Como… quiero… para…"), los criterios de aceptación en Gherkin, la prioridad, la épica principal y la etiqueta `Historia-de-Usuario` o `Enabler`, tal como están definidos en [01 Transformando a ágil](01%20Transformando%20a%20ágil%20V_1_0_0.md).

## Evidencia 1: Roadmap del Proyecto

*Mapeo de las Épicas (EP-01 a EP-04) en la línea de tiempo del proyecto.*

`[INSERTAR CAPTURA AQUÍ — vista Cronograma de Jira, recortada — img/01-roadmap.png]`

**Descripción:** El cronograma cubre del **05/10/2026 al 08/11/2026**, es decir, los Sprints 1 a 3. Las 4 épicas se distribuyen así:

| Épica | Inicio | Fin | Sprints |
|---|---|---|---|
| EP-01 · Gestión de Puntos de Entrega y Rutas | 05/10/2026 | 01/11/2026 | 1 y 2 |
| EP-02 · Motor de Optimización de Rutas | 05/10/2026 | 01/11/2026 | 1 y 2 |
| EP-03 · Visualización en Mapa | 19/10/2026 | 08/11/2026 | 2 y 3 |
| EP-04 · Panel de Gestión del Operador | 19/10/2026 | 08/11/2026 | 2 y 3 |

EP-01 y EP-02 abren el proyecto porque contienen el flujo base: registrar puntos, calcular la ruta y autenticar. EP-03 y EP-04 se apoyan en ese flujo para la visualización y la gestión de rutas.

## Evidencia 2: Backlog Priorizado

*Vista general del backlog con Story Points estimados (secuencia de Fibonacci) y componentes asignados, según la tabla de la sección 2 de [01 Transformando a ágil](01%20Transformando%20a%20ágil%20V_1_0_0.md).*

`[INSERTAR CAPTURA AQUÍ — vista Backlog de Jira, recortada — img/02-backlog.png]`

**Descripción:** El backlog contiene **11 elementos con un total de 49 Story Points**: 8 historias de usuario y 3 enablers, todos estimados con valores de Fibonacci (2, 3, 5 y 8). El orden aplica la priorización por valor de negocio y riesgo técnico de la sección 2:

- **Alta:** US-001, US-003, EN-01, EN-02, US-004 y US-005.
- **Media:** US-002, US-007, US-006 y EN-03.
- **Baja:** US-008.

Los elementos están repartidos en tres sprints: Sprint 1 con 21 SP, Sprint 2 con 16 SP y Sprint 3 con 12 SP.

## Evidencia 3: Sprint Planning & Sprint Goal

*Ítems seleccionados para el Sprint 1 y la meta (Sprint Goal) redactada en la cabecera del sprint.*

`[INSERTAR CAPTURA AQUÍ — cabecera del Sprint 1 en Jira con su objetivo, recortada — img/03-sprint-planning.png]`

**Sprint Goal (Sprint 1):**
> Contar con un flujo end-to-end mínimo funcional: el operador puede registrar puntos de entrega, el backend calcula una ruta optimizada básica, y ese acceso queda protegido por autenticación — sentando las bases de rendimiento y seguridad sobre las que se construirán la visualización en mapa y el resto del panel en los sprints siguientes.

**Ítems incluidos en Sprint 1:** US-001, US-003, EN-01, EN-02 (21 Story Points — ver sección 2 de [01 Transformando a ágil](01%20Transformando%20a%20ágil%20V_1_0_0.md)).

**Descripción:** Los sprints configurados en Jira son los siguientes:

| Sprint | Fechas | Ítems | SP | Sprint Goal | Estado |
|---|---|---|:---:|---|---|
| Sprint 1 | 05/10/2026 – 18/10/2026 | US-001, US-003, EN-01, EN-02 | 21 | El indicado arriba. | Cerrado |
| Sprint 2 | 19/10/2026 – 01/11/2026 | US-004, US-005, US-002, US-007 | 16 | Que el operador visualice la ruta optimizada en un mapa interactivo junto con su impacto ambiental estimado (CO₂), y pueda listar, buscar, editar y eliminar sus rutas guardadas. | Cerrado |
| Sprint 3 | 02/11/2026 – 08/11/2026 | US-006, EN-03, US-008 | 12 | Completar el PMV: detalle de cada parada en el mapa, exportación del resumen de la ruta y pipeline CI/CD con despliegue a Staging (hito H5). | Activo |

EN-02 quedó al 60 % al cierre del Sprint 1: la autenticación JWT está terminada, pero falta HTTPS. Por eso se trasladó como trabajo incompleto al Sprint 2 y después al Sprint 3, donde sigue abierta. El Sprint 0 — Base del proyecto (01/10/2026 – 04/10/2026) corresponde al hito H3 del Acta de Constitución y no se registra como sprint Scrum, por no contener historias del backlog.

## Evidencia 4: Tablero Scrum Activo

*Flujo de trabajo con tarjetas distribuidas en las columnas del tablero: Por hacer → En curso → En revisión → Finalizado (equivalentes a To Do → In Progress → In Review / QA → Done).*

`[INSERTAR CAPTURA AQUÍ — tablero del Sprint 3 en Jira, recortado — img/04-tablero.png]`

**Descripción:** El tablero muestra el Sprint 3, que está activo. Las 4 tarjetas se reparten así:

| Columna | Tarjetas |
|---|---|
| Por hacer | 0 |
| En curso | 0 |
| En revisión | 2: EN-02 (falta HTTPS) y EN-03 (falta un host de Staging) |
| Finalizado | 2: US-006 y US-008 |

Los dos enablers siguen en "En revisión" y no en "Finalizado" porque aún no cumplen la Definition of Done. Sus criterios exigen cifrado en tránsito y un despliegue automático verificado en Staging, y ninguno de los dos existe todavía (ver [Revisión del Sprint 3](../03%20Implementación/Sprint%2003/01%20Revisión%20del%20Sprint%20V_1_0_0.md)).

## Evidencia 5: Gestión de Versiones / Release

*Vista del módulo de Releases mostrando la versión creada (`v1.0.0-MVP`) y su asociación de historias.*

`[INSERTAR CAPTURA AQUÍ — vista Lanzamientos de Jira, recortada — img/05-release.png]`

**Descripción:** La versión **`v1.0.0-MVP`** va del 05/10/2026 al 08/11/2026 (fecha de lanzamiento planificada, hito H5) y agrupa las **11 historias del backlog** (49 SP). Está **sin publicar** porque EN-02 y EN-03 siguen en "En revisión". Las otras 9 historias ya están en "Finalizado" (36 SP).

---

[← Volver al README Principal](../../README.md)
