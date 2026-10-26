[← Volver al README Principal](../../README.md)

# Documento 12: Plan y Estrategia de Pruebas

Documento dedicado a la planificación y estrategia de pruebas del sistema
**EcoLogística Lima**.

## Qué va aquí

- **Planes de prueba** y matriz de casos (unitarios, integración, e2e).
- **Evidencias de ejecución**: resultados, capturas y reportes de corridas.
- Referencia a las **suites automatizadas** del proyecto.

## Ubicación de las pruebas automatizadas

Las suites de pruebas viven junto al código que verifican (no se duplican):

| Artefacto | Ubicación |
| :--- | :--- |
| Suite pytest (51 pruebas) | `src/backend/tests` |
| Selección de enfoque / trazabilidad | [05 Requisitos funcionales](05%20Requisitos%20funcionales%20V_1_0_0.md), [08 Reglas de negocio](08%20Reglas%20de%20negocio%20V_1_0_0.md) |
| Registro de KPIs y su verificación | `README.md` (sección KPIs) |
| Impedimentos detectados al probar | [Registro de Impedimentos del Sprint 1](../03%20Implementación/Sprint%201/02%20Registro%20de%20Impedimentos%20V_1_0_0.md) |

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

- `src/backend/tests`: **51 pruebas en verde** sobre la base `DB_NAME_TEST`.
- Auditoría y smoke test: terminan **sin anomalías** y son repetibles (herméticos).
- Pendientes registrados: cobertura global ≥ 70 % (sin herramienta configurada),
  pruebas del frontend y mediciones de reducción de distancia/emisiones
  (ver `README.md`, sección KPIs, y la Retrospectiva del Sprint 1).