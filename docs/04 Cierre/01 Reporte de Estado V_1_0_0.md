[← Volver al README Principal](../../README.md)

# 01 Reporte de Estado del Proyecto (Status Report)

**Proyecto:** EcoLogística Lima – Optimizador de Rutas Sostenibles para DistriRápido S.A.C.  
**Fecha de Corte:** 19/11/2026  
**Versión:** 1.0.0

> **Nota metodológica:** este reporte consolida solo evidencia verificable en el
> repositorio al 19/11/2026. Cuando un dato no existe se declara expresamente como
> "no disponible" o "no evaluable"; no se sustituye por estimaciones. Serie de cierre:
> [01 Estado](01%20Reporte%20de%20Estado%20V_1_0_0.md) ·
> [02 Variación](02%20Reporte%20de%20Variación%20V_1_0_0.md) ·
> [03 EVM](03%20Reporte%20de%20Análisis%20de%20Valor%20Ganado%20-%20EVM%20V_1_0_0.md) ·
> [04 Tableros](04%20Tableros%20de%20Control%20-%20Híbridos%20V_1_0_0.md) ·
> [05 Radiadores](05%20Radiadores%20de%20Información%20V_1_0_0.md) ·
> [06 Reporte Final](06%20Reporte%20Final%20del%20Proyecto%20V_1_0_0.md) ·
> [07 Lecciones](07%20Reporte%20Final%20de%20Lecciones%20Aprendidas%20V_1_0_0.md).

## 1. Información de Alcance

- **Logros completados:** el PMV quedó funcional en ejecución local con US-001 a US-008
  y EN-01; la autenticación JWT de EN-02 está terminada (HTTPS pendiente) y la CI de
  EN-03 está implementada y ejecutada (Staging y despliegue automático pendientes). Se
  cerraron **36 de 49 Story Points** del backlog (16 en Sprint 1, 16 en Sprint 2 y 4 en
  Sprint 3). El Sprint 4 entregó seis ítems técnicos internos: cuatro completados, uno
  ejecutado con despliegue omitido y uno parcial. La verificación automatizada registró
  **66/66 pruebas pytest**, **24/24 pruebas Vitest**, **79 aprobadas / 2 omitidas / 0
  fallidas** sobre 81 ejecuciones E2E en tres navegadores, y build de Vite exitoso sobre
  85 módulos. El 19/11/2026, sobre el commit `85eac48`, los workflows Tests, CI, CodeQL y
  Green Audit terminaron en verde. Fuentes:
  [Revisión Sprint 4](../03%20Implementación/Sprint%2004/01%20Revisión%20del%20Sprint%20V_1_0_0.md)
  y [Evidencias](../Evidencias/README.md).
- **Cambios al alcance (adiciones, eliminaciones o modificaciones):** se incorporó un
  Sprint 0 de base (01/10–04/10/2026, sin Story Points) no previsto en el cronograma
  inicial; el Sprint 4 se recondujo a consolidación de calidad sin historias nuevas
  (ítems `ET-S4-01` a `ET-S4-06`, que no deben interpretarse como US-009). Quedaron fuera
  del PMV, y así están documentados, el bloqueo por intentos fallidos (RN-002), HTTPS en
  la aplicación, la MFA con TOTP, el despliegue a Staging/Producción, Cypress y OR-Tools.
  Se corrigieron documentación y stacking (endpoint inexistente, cifras no verificables,
  Tailwind/Alembic/Vitest/GitHub Actions según correspondió) conforme al
  [CHANGELOG](../../CHANGELOG.md). **No se registró un re-baselining formal:** la línea
  base de 49 SP se mantuvo; los cambios se hicieron trazables en el historial de cambios.
- **Información de calidad (defectos o incidentes detectados):** se corrigieron la
  transacción sin `commit()` de `PUT /rutas/{id}`, la inyección de fórmulas en la
  exportación CSV, 5 bugs y 2 code smells del primer análisis de SonarQube y el
  `ReferenceError` que dejaba el panel en blanco. Persisten: IMP-10 (con exactamente tres
  puntos, 2-opt no se ejecuta y el ahorro se acota en cero), RN-002 sin implementar,
  HTTPS y MFA pendientes, cobertura backend del 61 % (el informe ambiental reporta 63 %)
  frente al objetivo de 70 %, y un Quality Gate "OK" con `ignoredConditions: true` y
  `new_coverage = 0.0`. **No hay incidentes de producción registrados**, coherente con la
  ausencia de despliegue real. Fuentes:
  [Impedimentos Sprint 1](../03%20Implementación/Sprint%2001/02%20Registro%20de%20Impedimentos%20V_1_0_0.md),
  [Calidad de código](../03%20Implementación/Sprint%2003/03%20Calidad%20de%20código%20V_1_0_0.md)
  y [mediciones Sonar](../Evidencias/sonar-sprint3/measures.json).

## 2. Información de Cronograma

- **Actividades/Hitos planificados pero no completados:** H4 (PMV Sprint 2, previsto
  25/10/2026; Sprint 2 cerrado el 01/11/2026), H6 (Cierre, previsto 15/11/2026; al
  19/11/2026 solo hay verificación en GitHub y esta documentación de cierre), la porción
  HTTPS de EN-02, la porción de Staging/despliegue de EN-03, la aplicación del SUS, la
  evidencia MP4 y la transición operativa a un entorno desplegado.
- **Causa raíz de las desviaciones:** dependencia de recursos externos no provistos
  (host, URL, proveedor y secretos) para Staging/Producción; alcance de seguridad más
  amplio que el implementado inicialmente; extensión del Sprint 4 para verificación E2E,
  calidad y documentación; y ausencia de participantes reclutados para el SUS. No hubo una
  sesión formal de revisión con stakeholders, por lo que no se registra fecha de
  aceptación del cliente.
- **Impacto en próximos hitos o en la ruta crítica:** el PMV es operativo en local y la
  integración frontend-backend quedó verificada, pero el cierre administrativo no puede
  declararse completo sin video, sin aceptación formal y sin despliegue. En términos de
  la línea base, quedan **13 SP no cerrados** (EN-02: 5, EN-03: 8), equivalentes a
  **$2,647.25** del BAC según la valorización por SP explicada en el
  [reporte EVM](03%20Reporte%20de%20Análisis%20de%20Valor%20Ganado%20-%20EVM%20V_1_0_0.md).
- **Acciones correctivas o preventivas planificadas:** las ocho acciones `ACT-S4-01` a
  `ACT-S4-08` de la
  [Retrospectiva del Sprint 4](../03%20Implementación/Sprint%2004/02%20Retrospectiva%20del%20Sprint%20V_1_0_0.md),
  con responsables y fechas entre el 24/11/2026 y el 08/12/2026. Al 19/11/2026 solo
  ACT-S4-02 se cumplió parcialmente (CI en verde, deploys omitidos); las demás siguen
  abiertas.

## 3. Información de Costos

- **Fondos ejecutados en este periodo:** **no hay registros de desembolsos reales,
  facturas, pagos ni horas ejecutadas**. El único referente es el presupuesto estimado en
  USD, **BAC = $9,978.08**, compuesto por $8,890.00 de recursos humanos (480 horas
  estimadas), $0.00 de licenciamiento, $19.00 de infraestructura y $1,069.08 de
  contingencia del 12 %. El Acta de Constitución expresó además un referencial de
  **S/ 13,200.00**. Ambos son costos de oportunidad, no desembolsos. Fuente:
  [Presupuesto](../02%20Planificación/04%20Presupuesto%20del%20proyecto%20V_1_0_0.md).
- **Causa raíz de la variación (mano de obra, materiales o estimaciones):** no es
  cuantificable. La ausencia de variación no significa desviación cero: significa que no
  existe Costo Real (AC) con el cual comparar el valor ganado. La Estimación a la
  Conclusión no puede calcularse sin ese dato.
- **Impacto en el presupuesto general o reserva de contingencia:** no hay registro de
  ejecución de la contingencia de $1,069.08 ni de la inversión estimada en infraestructura
  de $19.00. El presupuesto general estimado se mantiene como línea base documental.
- **Acciones correctivas o preventivas planificadas:** incorporar un registro de horas
  reales por sprint y de costos efectivamente incurridos, con responsable y periodicidad
  definidos, antes de intentar CV, CPI o EAC. Esta acción está **pendiente** y no se
  presenta como ejecutada.

## 4. Proyección (Look Ahead)

- **Logros/Entregables planificados para el próximo periodo:** cerrar las acciones
  registradas —SUS aplicado a al menos cinco operadores (ACT-S4-01, 01/12/2026), definir
  proveedor/URL/secretos de Producción (ACT-S4-03, 01/12/2026), pruebas de componentes
  React (ACT-S4-04, 01/12/2026), elevar la cobertura backend a ≥ 70 % (ACT-S4-05,
  08/12/2026), incorporar `@axe-core/playwright` (ACT-S4-06, 08/12/2026), conservar o
  justificar la exclusión de la evidencia Lighthouse (ACT-S4-07) y documentar el ciclo de
  vida de los datos de prueba (ACT-S4-08)—, además del video MP4 de ~5 minutos exigido
  en `docs/05 Video proyecto` (ver [estado del entregable](../05%20Video%20proyecto/README.md)).
- **Costos planificados para el próximo periodo:** no existe una línea base de costos
  ejecutados ni un plan de desembolsos por periodo. El presupuesto solo estima $19.00 de
  infraestructura y una contingencia de $1,069.08; por ello no se informa un monto
  planificado adicional para el próximo periodo.

## 5. Riesgos, Incidentes y Comentarios

- **Nuevos riesgos identificados:** la auditoría de cierre detectó credenciales de
  demostración sembradas automáticamente cuando la base está vacía
  (`admin/admin123`, `operador/operador123`), `JWT_SECRET` inseguro por defecto en
  `development`, `VITE_API_URL` documentada pero no efectiva en el cliente, el límite de
  100 registros en los selectores del panel, la coherencia del Quality Gate de SonarQube
  y la procedencia de `resultados.json` (ruta absoluta de otro workspace). Estos hallazgos
  se suman a la matriz RSK-01 a RSK-08 sin modificarla: requieren registro formal en una
  siguiente versión de la matriz.
- **Nuevos incidentes (Issues) surgidos:** no se registraron incidentes en producción.
  Las desviaciones abiertas se tratan como impedimentos y deuda de calidad documentada,
  no como incidentes operativos.
- **Comentarios relevantes:** el estado real es de **cierre técnico parcial**. No se
  declara satisfacción de interesados ni del equipo porque no hay medición (sin SUS
  aplicado, sin Mood Chart y sin sesión de aceptación). Este documento y sus seis
  acompañantes cierran la trazabilidad documental; el video y la aceptación formal
  permanecen pendientes y se listan sin estimaciones ficticias.

## 6. Actualización posterior al corte (25/11/2026)

Este reporte conserva íntegramente su fecha de corte del 19/11/2026. Con posterioridad se
ejecutó el cierre del feedback final de auditoría: el hallazgo de `JWT_SECRET` inseguro por
defecto en `development` quedó **resuelto** (clave aleatoria efímera en desarrollo, valores
de ejemplo y vacíos descartados, variable obligatoria ≥32 caracteres en Staging/Producción),
la cobertura backend pasó a **74 %** y la frontend a **87,03 % global** con componentes
React, y la latencia local de respuestas 401/403 quedó medida en `test_rnf004_latencia.py`.
Las cifras y estados vigentes se consolidan en el
[README principal](../../README.md) y en la
[matriz de trazabilidad](../02%20Planificación/11%20Matriz%20de%20Trazabilidad%20V_1_0_0.md).
El video, la aceptación formal, el SUS, el AC real y el despliegue siguen pendientes por
las mismas causas externas declaradas en este documento.

---

[← Volver al README Principal](../../README.md)
