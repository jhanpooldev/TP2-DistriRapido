[← Volver al README Principal](../../README.md)

# 06 Reporte Final del Proyecto (Final Project Report)

**Proyecto:** EcoLogística Lima – Optimizador de Rutas Sostenibles para DistriRápido S.A.C.  
**Fecha de Cierre:** 19/11/2026 (fecha de corte de la evidencia verificable; **no se registró
acta de aceptación formal ni reunión de cierre con stakeholders**)  
**Versión:** 1.0.0

> Serie de cierre: [01 Estado](01%20Reporte%20de%20Estado%20V_1_0_0.md) ·
> [02 Variación](02%20Reporte%20de%20Variación%20V_1_0_0.md) ·
> [03 EVM](03%20Reporte%20de%20Análisis%20de%20Valor%20Ganado%20-%20EVM%20V_1_0_0.md) ·
> [04 Tableros](04%20Tableros%20de%20Control%20-%20Híbridos%20V_1_0_0.md) ·
> [05 Radiadores](05%20Radiadores%20de%20Información%20V_1_0_0.md) ·
> [06 Reporte Final](06%20Reporte%20Final%20del%20Proyecto%20V_1_0_0.md) ·
> [07 Lecciones](07%20Reporte%20Final%20de%20Lecciones%20Aprendidas%20V_1_0_0.md).

## 1. Descripción General del Proyecto

DistriRápido S.A.C. planificaba sus rutas de forma manual o con herramientas genéricas
que no consideraban criterios de sostenibilidad ni la optimización conjunta de múltiples
paradas, con sobrecostos de combustible, entregas prolongadas y huella de carbono
innecesaria. El proyecto construyó un sistema web para empresas de logística urbana en
Lima que calcula rutas considerando distancia, tiempo y emisiones estimadas de CO₂. El PMV
cubre los pasos 1, 2, 4, 5 y 8 del proceso logístico; quedan fuera la gestión detallada de
conductores, el seguimiento en tiempo real y el monitoreo GPS. La solución usa una
heurística propia (Haversine + Vecino Más Cercano + 2-opt), mapa Leaflet con trazado OSRM,
exportación CSV, JWT con expiración de 8 horas, bcrypt y control por roles. Fuente:
[Acta de Constitución](../01%20Inicio/02%20Acta%20de%20constitución%20V_1_0_0.md) y
[README principal](../../README.md).

## 2. Resumen de Desempeño

### 2.1 Alcance (Predictivo y Adaptativo)

- **Objetivos y criterios de éxito:** nueve KPIs publicados en el README. Cinco están
  verificados (tiempo de generación ≤ 5 s —máximo medido 20.2 ms—, distancia geodésica,
  rechazo de rutas con menos de dos puntos, aislamiento por operador y emisiones según
  factor del vehículo). Cuatro están pendientes o parciales: reducción de distancia ≥ 15 %,
  reducción de emisiones ≥ 10 %, flujo principal ≤ 3 pasos y ≤ 3 minutos, y cobertura
  global ≥ 70 %.
- **Evidencia de cumplimiento:** 36 de 49 SP cerrados; US-001 a US-008 y EN-01
  terminados; JWT de EN-02 terminado; CI de EN-03 implementada y ejecutada; seis entregables
  internos del Sprint 4, cuatro completados. La demostración verificada es la ejecución
  local documentada en la revisión del Sprint 4, con siete capturas reales de pantalla.
- **Variaciones, causas y su impacto:** 13 SP no cerrados por dependencias de HTTPS y de
  entorno de despliegue; Sprint 0 y Sprint 4 reorientados; RN-002, MFA, Staging y
  Producción fuera de lo entregado; sin re-baselining formal de los 49 SP. Impacto:
  SPI 0.7347 y SV -$2,647.25 (26.53 % del BAC), con cierre técnico parcial.

### 2.2 Calidad

- **Requisitos y criterios de aceptación:** US-001 a US-008 y EN-01 a EN-03, reglas
  RN-001 a RN-018 según corresponda, estándares W3C/WCAG, OWASP Top 10, ISO/IEC 25010 y
  Green Software, y DoD de [Transformando a ágil](../02%20Planificación/01%20Transformando%20a%20ágil%20V_1_0_0.md).
- **Resultados de verificación y validación:** 66/66 pytest; 24/24 Vitest (93.22 %
  de sentencias sobre `src/logica/**`); 79 E2E aprobadas, 2 omitidas, 0 fallidas y 0
  flaky sobre 81 ejecuciones; build Vite de 85 módulos; 0 bugs, 0 vulnerabilidades,
  0 smells y 0 hotspots en SonarQube con 1.4 % de duplicación; Tests, CI, CodeQL y Green
  Audit en verde el 19/11/2026 sobre `85eac48`. Rendimiento del motor entre 17.9 y 20.2 ms
  con 20 puntos. Medición Lighthouse de la pantalla de login: transferencia de 130,946 B
  a 72,564 B (-44.58 %).
- **Requisitos eximidos o variaciones:** cobertura backend 61 % (63 % en otro informe)
  frente al objetivo de 70 %; Quality Gate con `ignoredConditions: true` y
  `new_coverage = 0.0`; SUS preparado pero no aplicado; Mood Chart sin datos; RN-002,
  HTTPS, MFA y rate limiting pendientes; Staging y Producción omitidos; Lighthouse solo
  sobre login; limitación IMP-10 con exactamente tres puntos.

#### Anexo A — Cobertura de estándares, áreas de gestión y competencias

| Estándar / marco | Evidencia verificable | Brecha declarada |
|:---|:---|:---|
| W3C / WCAG | Skip link, foco visible, `role="tablist"`, `aria-selected`, `aria-live`, tablas con `caption.sr-only` y `prefers-reduced-motion`. | `MapPicker` fija coordenadas solo con puntero; no hay equivalente de teclado (WCAG 2.1.1). |
| ISO/IEC 25010 | Funcionalidad del PMV verificada por pruebas; rendimiento medido; seguridad con JWT/bcrypt/roles; mantenibilidad por capas y módulos. | Sin despliegue real, sin medición de fiabilidad operativa ni SUS aplicado. |
| OWASP Top 10 | ORM, validación Pydantic, CORS explícito, cabeceras de endurecimiento, CSV neutralizado y popups con `textContent`. | Sin rate limiting en login, secreto JWT inseguro en desarrollo, credenciales demo sembradas, RN-002 y MFA pendientes. |
| Green Software | Lazy loading, `manualChunks`, paginación, caché, compresión, Lighthouse CI y reducción de transferencia medida. | Auditoría limitada al login, presupuestos en modo `warn`, sin JSON de Lighthouse conservado localmente. |
| Cinco áreas de gestión | Inicio (5 documentos), Planificación (12 documentos + imágenes), Ejecución (sprints 0–4), Seguimiento y Control (revisiones, impedimentos, EVM y tableros), Cierre (estos 7 documentos). | Cierre administrativo y aceptación formal pendientes. |

| Competencia (consigna general) | Evidencia en el proyecto |
|:---|:---|
| A — Aprendizaje Experiencial y Colaborativo | Cuatro retrospectivas con aprendizajes y ocho acciones de mejora con responsables. |
| B — Ciudadanía Glocal | Problema logístico contextualizado en Lima con impacto ambiental medido y límites declarados. |
| C — Comunicación Efectiva | README, CHANGELOG, cinco fases documentadas, enlaces bidireccionales y este cierre; video pendiente. |
| D — Medio Ambiente y Sostenibilidad | Informe de reducción de impacto ambiental con SWDM, -44.58 % de transferencia y supuestos explícitos. |
| E — Diseño y Desarrollo de Soluciones | PMV funcional, arquitectura por capas, heurística propia, API REST y suite E2E multi-navegador. |

### 2.3 Cronograma

| Hito / Entrega | Enfoque | Fecha Planificada | Fecha Real | Variación / Impacto |
|:---|:---:|:---:|:---:|:---|
| H1 — Inicio | Predictivo | 30/08/2026 | 27/08/2026 (documentación de Inicio) | Sin desfase declarado; fecha real es la de los documentos, no un acta de aprobación. |
| H2 — Planificación | Predictivo | 13/09/2026 | 10/09/2026 (presupuesto y artefactos) | Sin desfase declarado. |
| H3 — PMV Sprint 1 (base) | Adaptativo | 04/10/2026 | 04/10/2026 (Sprint 0) | Cumplido como base del proyecto. |
| H4 — PMV Sprint 2 | Adaptativo | 25/10/2026 | 01/11/2026 | 7 días de desfase; 16/16 SP cerrados. |
| H5 — PMV Completo | Híbrido | 08/11/2026 | 08/11/2026 (Sprint 3) | 4 de 12 SP cerrados; EN-03 parcial por falta de entorno. |
| H6 — Cierre | Predictivo | 15/11/2026 | 17/11/2026 (verificación local) y 19/11/2026 (GitHub) | 4 días de desfase y sin aceptación formal; cierre técnico parcial. |

### 2.4 Costo

- **Presupuesto aprobado (y rango de tolerancia):** $9,978.08 USD estimados, con
  contingencia del 12 % ($1,069.08). Referencial en soles: S/ 13,200.00, con 10 % de
  contingencia. No se definió un rango de tolerancia numérico adicional.
- **Costo final real del proyecto:** **no disponible**. No hay registros de desembolsos,
  facturas ni horas ejecutadas; los montos son costo de oportunidad académico.
- **Análisis de variaciones e impacto:** CV, CPI y las tres EAC son **no evaluables** por
  ausencia de AC. No se afirma sobrecoste ni ahorro. Detalle en el [reporte EVM](03%20Reporte%20de%20Análisis%20de%20Valor%20Ganado%20-%20EVM%20V_1_0_0.md).

## 3. Resumen de Riesgos, Incidentes e Impedimentos

| ID / Descripción | Tipo (Riesgo/Incidente/Impedimento) | Impacto Real | Respuesta Aplicada |
|:---|:---:|:---|:---|
| RSK-02 — Complejidad del algoritmo de optimización (severidad 15, Alta) | Riesgo | No se materializó como falla: la heurística respondió en 17.9–20.2 ms. | Mitigación prevista aplicada: Vecino Más Cercano + 2-opt en lugar de búsqueda exhaustiva. |
| IMP-01 — Falta de `email-validator` impedía arrancar la API | Impedimento | Bloqueo inicial resuelto el 06/10/2026. | Dependencia incorporada y verificación posterior. |
| IMP-03 — Búsqueda `O(n!)` inviable frente al SLA de 5 s | Impedimento | Riesgo de tiempo de respuesta eliminado. | Adopción de heurística; ver `test_optimizer.py`. |
| IMP-S2-01 — `PUT /rutas/{id}` perdía ediciones al cerrar sesión | Impedimento | Pérdida intermitente de cambios. | `commit()` explícito el 21/10/2026. |
| IMP-10 — 2-opt no se ejecuta con exactamente tres puntos | Impedimento | Abierto: la distancia optimizada puede ser levemente mayor; ahorro acotado en cero. | Documentado como limitación conocida en el README; pendiente de corrección. |
| EN-02 (HTTPS) y EN-03 (Staging/Producción) | Riesgo materializado / impedimento | 13 SP no acreditados, SPI 0.7347; despliegue no verificable. | CI ejecutada; acciones ACT-S4-02 y ACT-S4-03 abiertas/parciales. |
| Hallazgos de la auditoría de cierre (credenciales demo, JWT por defecto, `VITE_API_URL`, límite de 100 registros) | Riesgo | No hay incidente en producción; riesgo latente para un despliegue futuro. | Declarados en el Reporte de Estado; requieren registro en la matriz RSK y corrección. |

No se registraron incidentes de producción porque nunca hubo despliegue real.

## 4. Evaluación del Éxito y Cierre

- **Satisfacción de los interesados (Stakeholders):** **no medida**. No se realizó sesión
  de revisión ni de aceptación formal, y el cuestionario SUS quedó preparado pero sin
  aplicar. No se declara satisfacción ni puntaje alguno. La acción ACT-S4-01 (SUS a al
  menos cinco operadores) sigue abierta con fecha límite 01/12/2026.
- **Satisfacción y reconocimiento del equipo:** **no medida**. No existe Mood Chart ni
  registro de clima; las retrospectivas documentan aprendizajes, no percepciones
  individuales. No se declara un estado de ánimo ni un nivel de satisfacción.
- **Transición operativa y cierre administrativo:** parcial. El PMV opera en local con
  integración frontend-backend verificada; CI, pruebas, CodeQL y Green Audit están en
  verde sobre `85eac48`; los workflows de Staging y Producción quedaron omitidos. Se
  entregan los siete documentos de cierre y el índice bidireccional en el README; el video
  MP4 y el acta de aceptación permanecen pendientes, registrados sin evidencia ficticia.
  En consecuencia, el estado honesto es **cierre técnico parcial; cierre administrativo
  pendiente**.

---

[← Volver al README Principal](../../README.md)
