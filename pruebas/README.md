# Estructura 3: Pruebas

Carpeta de la estructura requerida del PFA dedicada a las pruebas del sistema
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
| Selección de enfoque / trazabilidad | `docs/inicio/06`, `docs/inicio/09` |
| Registro de KPIs y su verificación | `README.md` (sección KPIs) |
| Impedimentos detectados al probar | `docs/03 Implementación/02 Registro de Impedimentos V_1_0_0.md` |

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