[← Volver al README Principal](../../README.md)

# 02 Reporte de Variación (Variance Report)

**Proyecto:** EcoLogística Lima – Optimizador de Rutas Sostenibles para DistriRápido S.A.C.  
**Periodo Reportado:** Sprint 4 (09/11/2026 – 17/11/2026), con acumulado hasta el cierre del proyecto  
**Fecha de Corte:** 19/11/2026  
**Versión:** 1.0.0

> El periodo se define conforme a la
> [Revisión del Sprint 4](../03%20Implementación/Sprint%2004/01%20Revisión%20del%20Sprint%20V_1_0_0.md):
> verificación local el 17/11/2026 y verificación en GitHub el 19/11/2026. No se declara
> aceptación formal del cliente. Serie de cierre:
> [01 Estado](01%20Reporte%20de%20Estado%20V_1_0_0.md) ·
> [02 Variación](02%20Reporte%20de%20Variación%20V_1_0_0.md) ·
> [03 EVM](03%20Reporte%20de%20Análisis%20de%20Valor%20Ganado%20-%20EVM%20V_1_0_0.md) ·
> [04 Tableros](04%20Tableros%20de%20Control%20-%20Híbridos%20V_1_0_0.md) ·
> [05 Radiadores](05%20Radiadores%20de%20Información%20V_1_0_0.md) ·
> [06 Reporte Final](06%20Reporte%20Final%20del%20Proyecto%20V_1_0_0.md) ·
> [07 Lecciones](07%20Reporte%20Final%20de%20Lecciones%20Aprendidas%20V_1_0_0.md).

## 1. Variación de Cronograma

| Métrica / Aspecto | Detalle |
|:---|:---|
| **Resultados Planificados** | Línea base de 49 SP distribuidos en Sprint 1 (21), Sprint 2 (16) y Sprint 3 (12), más hitos H1 (30/08), H2 (13/09), H3 (04/10), H4 (25/10), H5 (08/11) y H6 (15/11/2026), según el [Acta de Constitución](../01%20Inicio/02%20Acta%20de%20constitución%20V_1_0_0.md) y [Transformando a ágil](../02%20Planificación/01%20Transformando%20a%20ágil%20V_1_0_0.md). |
| **Resultados Reales** | 36 de 49 SP cerrados (16 + 16 + 4); 13 SP parciales (EN-02: 5, EN-03: 8). Sprint 4 sin SP del backlog: seis entregables `ET-S4-xx`, cuatro completados, uno con despliegue omitido y uno parcial. Verificación local 17/11/2026 y en GitHub 19/11/2026. SPI acumulado **0.7347**; SV acumulado **-$2,647.25**. |
| **Variación Obtenida** | **-13 SP** respecto a la línea base (26.53 % del BAC en términos de valor). H4 se cerró el 01/11/2026, **7 días** después de lo previsto. H6 no se completó en la fecha planificada: al 19/11/2026 hay 4 días de desfase y, sobre todo, falta el cierre formal. En el Sprint 4 el PV y el EV del periodo son $0.00 porque no había SP planificados ni nuevos SP cerrados. |
| **Causa Raíz** | La porción HTTPS de EN-02 dependía del ambiente de despliegue; la porción de Staging de EN-03 exigía host, URL, proveedor y secretos que no fueron provistos. El Sprint 0 no estaba en el cronograma original. El Sprint 4 se extendió para ejecutar la suite E2E, la auditoría de calidad y la documentación. No se realizó sesión de revisión con stakeholders, por lo que no existe fecha de aceptación. |
| **Respuesta Planificada** | Mantener la línea base de 49 SP sin re-baselining no aprobado; ejecutar ACT-S4-02 y ACT-S4-03 para activar despliegue y enlazar corridas; conservar la fecha real de cada hito en el [Reporte Final](06%20Reporte%20Final%20del%20Proyecto%20V_1_0_0.md); no declarar terminado lo que no fue verificado. |

## 2. Variación de Costo

| Métrica / Aspecto | Detalle |
|:---|:---|
| **Resultados Planificados** | BAC estimado **$9,978.08** (USD): $8,890.00 RRHH (480 h estimadas), $0.00 licenciamiento, $19.00 infraestructura y $1,069.08 de contingencia (12 %). Referencial alternativo en el Acta: **S/ 13,200.00**. Fuente: [Presupuesto del proyecto](../02%20Planificación/04%20Presupuesto%20del%20proyecto%20V_1_0_0.md). |
| **Resultados Reales** | **Costo Real (AC) no disponible.** No existen registros de desembolsos, facturas, pagos ni horas ejecutadas. En consecuencia, CV y CPI son **no evaluables** y no pueden calcularse las tres proyecciones EAC. |
| **Variación Obtenida** | **No cuantificable.** No se sustituye AC por cero ni por el presupuesto estimado: hacerlo produciría un CV igual al EV y un CPI infinito o indefinido, cifras que no representan la ejecución real. |
| **Causa Raíz** | Proyecto académico: los montos son estimaciones de costo de oportunidad del tiempo del equipo y de infraestructura en planes gratuitos, no transacciones financieras. No se implementó un registro de horas reales por sprint. |
| **Respuesta Planificada** | Registrar AC real y horas ejecutadas por sprint antes de reportar CV, CPI o EAC. Acción **pendiente**, declarada en el [Reporte de Estado](01%20Reporte%20de%20Estado%20V_1_0_0.md). Hasta entonces, el análisis de costo se limita a la comparación entre PV y EV. |

## 3. Variación de Calidad

| Métrica / Aspecto | Detalle |
|:---|:---|
| **Resultados Planificados (Métricas/Criterios)** | Cobertura global ≥ 70 % en SPECS y ≥ 80 % de código nuevo en la DoD; generación de ruta ≤ 5 s (RNF); 0 bugs, 0 vulnerabilidades y 0 code smells en SonarQube; criterios de aceptación de US-001 a US-008 y EN-01 a EN-03; accesibilidad WCAG y seguridad OWASP; SUS aplicado a participantes reales. |
| **Resultados Reales (Defectos/Pruebas)** | **66/66 pytest**, **24/24 Vitest**, **79 aprobadas / 2 omitidas / 0 fallidas / 0 flaky** sobre 81 ejecuciones E2E (Chromium, Firefox y WebKit; 105,145 s). Build Vite exitoso (85 módulos). Motor: 17.9–20.2 ms con 20 puntos. SonarQube: 0 bugs, 0 vulnerabilidades, 0 smells, 0 hotspots, duplicación 1.4 %, cobertura 9.8 %. Cobertura backend 61 % (el informe ambiental reporta 63 %); frontend 93.22 % de sentencias sobre `src/logica/**`. CI/Tests/CodeQL/Green Audit en verde el 19/11/2026 sobre `85eac48`. Fuentes: [Evidencias](../Evidencias/README.md) y [resultados E2E](../Evidencias/playwright-sprint4/resultados.json). |
| **Variación Obtenida** | Cumplido: tiempo de respuesta, pruebas funcionales y E2E, build y hallazgos estáticos cero. **No cumplido:** cobertura backend 61 %/63 % frente a 70 %; Quality Gate "OK" con `ignoredConditions: true` y `new_coverage = 0.0`, por lo que no acredita el 80 % de código nuevo; SUS sin aplicar; RN-002, HTTPS, MFA y rate limiting sin implementar; Staging/Producción omitidos; Mood Chart sin datos. |
| **Causa Raíz** | No se incorporaron pruebas de componentes React ni un umbral de cobertura en CI; SonarQube mide todos los componentes, incluidos los React sin pruebas, de ahí la diferencia entre 9.8 % y 61 %; el despliegue dependía de credenciales externas; el instrumento SUS quedó preparado pero sin participantes. Las cifras 61 % y 63 % provienen de mediciones distintas y no han sido reconciliadas con una salida cruda de `pytest-cov` versionada. |
| **Respuesta Planificada** | ACT-S4-04 (pruebas de componentes), ACT-S4-05 (cobertura ≥ 70 % con umbral en CI), ACT-S4-06 (`@axe-core/playwright`), ACT-S4-07 (evidencia Lighthouse) y ACT-S4-08 (ciclo de datos de prueba), todas con responsable y fecha en la [Retrospectiva del Sprint 4](../03%20Implementación/Sprint%2004/02%20Retrospectiva%20del%20Sprint%20V_1_0_0.md). Mantener la limitación IMP-10 y los pendientes de seguridad visibles en el README. |

---

[← Volver al README Principal](../../README.md)
