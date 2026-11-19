# Registro de impedimentos

[← Volver al README principal](../../../README.md)

---

**Nombre del Proyecto:** EcoLogística Lima – Optimizador de Rutas Sostenibles para DistriRápido S.A.C.

**Líder del Proyecto:** Jhunior Harold Cosme Tenorio

**Sprint:** 2

**Periodo:** 19/10/2026 – 01/11/2026

---

## Control de Versiones del Documento

| Versión | Fecha | Autor | Descripción del Cambio |
|:---:|:---:|:---|:---|
| 1.0.0 | 01/10/2026 | Andrew Steven Vega Reyes / Jhunior Harold Cosme Tenorio | Registro inicial de impedimentos del Sprint 1. |
| 2.0.0 | 05/10/2026 | Andrew Steven Vega Reyes / Jhunior Harold Cosme Tenorio | Registro de impedimentos del Sprint 2. |
| 2.1.0 | 05/10/2026 | Andrew Steven Vega Reyes / Jhunior Harold Cosme Tenorio | Corrección de trazabilidad: se retiraron los impedimentos referidos a MFA/TOTP, `pyotp`, `mfa_token`, `jti` y `/api/auth/mfa/verify`, porque esa implementación no forma parte del código entregable en `src/backend`. Se reclasificaron las referencias a reglas de negocio según `docs/inicio/09` (RN-014 es capacidad vehicular y RN-009 es protección de puntos en rutas confirmadas). |

> Este documento está archivado en `sprint 2/` porque la consigna académica reserva
> las cuatro rutas de `docs/03 Implementación/` para los entregables del Sprint 1.

---

## Matriz de Registro de Impedimentos

| Impedimento # | Fecha de Registro | Descripción del Impedimento así como el Impacto en el Proyecto | Prioridad | Reportado por | Fecha tope de Resolución | Estado | Fecha de Resolución | Resolución/Comentarios |
|:---:|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---|
| **IMP-S2-01** | 20/10/2026 | **La edición de una ruta se perdía al cerrar la sesión.** `PUT /api/v1/rutas/{id}` modificaba el objeto en memoria sin confirmar la transacción, por lo que los cambios no persistían. **Impacto:** US-02 quedaba incumplido: el operador corregía los pedidos y la ruta volvía a su estado anterior sin mensaje de error. | Crítica | Jhanpool Ernesto Flores Torres | 21/10/2026 | Resuelto | 21/10/2026 | Se añadió `commit()` explícito y se verificó que la edición conserva el mismo `id_ruta` y no crea una ruta duplicada. La verificación se incorpora en `src/backend/smoke_sprint2.py`. |
| **IMP-S2-02** | 21/10/2026 | **Huérfanos al eliminar una ruta.** `DELETE /api/v1/rutas/{id}` retiraba la ruta pero dejaba las filas asociadas en `ruta_puntos`. **Impacto:** inconsistencia referencial en la base de datos y puntos que quedaban listados sin ruta asociada. | Alta | Jhanpool Ernesto Flores Torres | 22/10/2026 | Resuelto | 22/10/2026 | El endpoint elimina explícitamente los registros de `ruta_puntos` antes de confirmar la transacción. La auditoría de API verifica que no quedan huérfanos. |
| **IMP-S2-03** | 22/10/2026 | **El botón Reintentar del mapa recargaba toda la aplicación.** Ante una falla del proveedor de tiles, `window.location.reload()` descartaba la sesión de trabajo del operador. **Impacto:** pérdida de contexto y riesgo de interpretar el cierre de sesión como una caída del sistema. | Media | Ricardo David Tucto Ubaldo | 24/10/2026 | Resuelto | 23/10/2026 | La acción recrea únicamente la capa de tiles. Además se corrigió el contador de errores, que se reiniciaba con cada tile correcto e impedía avisar cuando el proveedor respondía parcialmente. |
| **IMP-S2-04** | 23/10/2026 | **Las instancias de mapa de Leaflet no se destruían al desmontarse.** `MapView` y `MapPicker` liberaban marcadores pero no el mapa. **Impacto:** al alternar entre pestañas se acumulaban contenedores y escuchas de eventos, degradando el rendimiento de la interfaz. | Media | Ricardo David Tucto Ubaldo | 25/10/2026 | Resuelto | 24/10/2026 | Se añadió la limpieza del mapa en el cierre del efecto y se liberan capa, polilínea y marcadores. |
| **IMP-S2-05** | 25/10/2026 | **El cálculo de ahorro de CO₂ usaba un factor fijo.** La estimación no consideraba el factor de emisión del vehículo asignado a la ruta. **Impacto:** el indicador ambiental de US-04 podía sobreestimar o subestimar las emisiones según la motorización de la unidad. | Alta | Jhunior Harold Cosme Tenorio | 28/10/2026 | Resuelto | 27/10/2026 | El cálculo parte de `factor_emision_co2`, `consumo_litros_km` y `velocidad_promedio_kmh` del vehículo. Se añadió el indicador `sin_reduccion_significativa` para no presentar porcentajes engañosos. |
| **IMP-S2-06** | 26/10/2026 | **Los filtros de fecha excluían las rutas creadas el mismo día.** El límite superior se interpretaba como exclusivo. **Impacto:** el listado de US-07 ocultaba rutas creadas ese mismo día, confundiendo al operador. | Media | Andrew Steven Vega Reyes | 28/10/2026 | Resuelto | 27/10/2026 | El rango pasó a ser inclusivo y los formatos inválidos responden `400` con el formato esperado, en lugar de ignorarse. |

---

## Resumen

| Estado | Cantidad |
|:---:|:---:|
| Resueltos | 6 |
| Abiertos | 0 |
| **Total** | **6** |

Todos los impedimentos del Sprint 2 se resolvieron dentro de la propia iteración, y
cada resolución queda verificada por la auditoría de API (`src/backend/auditoria_api.py`)
o por el smoke test (`src/backend/smoke_sprint2.py`).

---

[← Volver al README principal](../../../README.md)