[← Volver al README Principal](../../README.md)

# Documento 12: Plan y Estrategia de Pruebas

Documento dedicado a la planificación y estrategia de pruebas del sistema
**EcoLogística Lima**.

## Control de Versiones del Documento

| Versión | Fecha | Autor | Descripción del Cambio |
|:---:|:---:|:---|:---|
| 1.0.0 | 01/11/2026 | Jhunior Harold Cosme Tenorio / Equipo EcoLogística | Plan y estrategia de pruebas inicial. |
| 1.1.0 | 26/10/2026 | Jhunior Harold Cosme Tenorio / Equipo EcoLogística | Se actualizan las cifras al Sprint 3 (65 pytest, 24 Vitest, 60.82 % backend) y se agrega la ejecución real de auditoría, smoke test y SonarQube. |

## Qué va aquí

- **Planes de prueba** y matriz de casos (unitarios, integración, e2e).
- **Evidencias de ejecución**: resultados, capturas y reportes de corridas.
- Referencia a las **suites automatizadas** del proyecto.

## Ubicación de las pruebas automatizadas

Las suites de pruebas viven junto al código que verifican (no se duplican):

| Artefacto | Ubicación |
| :--- | :--- |
| Suite pytest (65 pruebas) | `src/backend/tests` |
| Suite Vitest (24 pruebas de `src/logica/**`) | `src/frontend/src/**/*.test.js` |
| Cobertura backend (pytest-cov) | `src/backend/coverage.xml` |
| Cobertura frontend (@vitest/coverage-v8) | `src/frontend/coverage/` |
| Selección de enfoque / trazabilidad | [05 Requisitos funcionales](05%20Requisitos%20funcionales%20V_1_0_0.md), [08 Reglas de negocio](08%20Reglas%20de%20negocio%20V_1_0_0.md) |
| Registro de KPIs y su verificación | `README.md` (sección KPIs) |
| Impedimentos detectados al probar | [Registro de Impedimentos del Sprint 1](../03%20Implementación/Sprint%201/02%20Registro%20de%20Impedimentos%20V_1_0_0.md) |
| Resultados del Sprint 3 | [Revisión del Sprint 3](../03%20Implementación/Sprint%2003/01%20Revisión%20del%20Sprint%20V_1_0_0.md) |

## Herramientas de verificación de extremo a extremo

| Herramienta | Ubicación |
| :--- | :--- |
| Auditoría de la API (cada endpoint y aislamiento por usuario) | `src/backend/auditoria_api.py` |
| Smoke test del Sprint 2 (flujo completo) | `src/backend/smoke_sprint2.py` |

> Ejecución (con el backend levantado en un puerto libre):
>
> ```bash
> cd src/backend
> python auditoria_api.py 8099
> python smoke_sprint2.py 8099
> ```

## Estado

- `src/backend/tests`: **65 pruebas en verde** sobre la base `DB_NAME_TEST`.
- Cobertura backend: **60.82 %** global (883 sentencias, 346 sin cubrir); el módulo
  de exportación del Sprint 3 alcanza **100 %**.
- `src/frontend/src/**/*.test.js`: **24 pruebas en verde** con **93.22 %** de
  sentencias, **85.24 %** de ramas, **91.3 %** de funciones y **97.84 %** de líneas
  sobre `src/logica/**`. No hay pruebas de componentes React.
- Auditoría y smoke test: se reejecutaron el 26/10/2026 contra PostgreSQL 18 local,
  con resultado **SIN ANOMALÍAS** y **TODO OK** respectivamente, sin alterar los datos.
- SonarQube: análisis real con Quality Gate **OK**, 0 bugs, 0 vulnerabilidades,
  0 code smells y 0 hotspots; cobertura global 9.8 % (incluye componentes React sin
  pruebas). Evidencias en
  [`docs/05 Evidencias/sonar-sprint3/`](../05%20Evidencias/sonar-sprint3/).
- Pendientes registrados: cobertura global del backend ≥ 70 %, pruebas de
  componentes React, mediciones de reducción de distancia/emisiones y ejecución
  real de los workflows de CI/CD (ver `README.md`, sección KPIs, y la Revisión del
  Sprint 3).