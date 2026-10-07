# Revisión del sprint

[← Volver al README principal](../../../README.md)

---

**Nombre del Proyecto:** EcoLogística Lima – Optimizador de Rutas Sostenibles para DistriRápido S.A.C.

**Líder del Proyecto:** Jhunior Harold Cosme Tenorio

**Sprint:** 2

---

## Control de Versiones del Documento

| Versión | Fecha | Autor | Descripción del Cambio |
|:---:|:---:|:---|:---|
| 1.0.0 | 01/10/2026 | Jhunior Harold Cosme Tenorio / Equipo EcoLogística | Acta de Revisión del Sprint 1. |
| 2.0.0 | 05/10/2026 | Jhunior Harold Cosme Tenorio / Equipo EcoLogística | Acta de Revisión del Sprint 2. |
| 2.1.0 | 05/10/2026 | Jhunior Harold Cosme Tenorio / Equipo EcoLogística | Corregida para alinearse con el Informe de Estado del Sprint 2: se retiraron métricas no verificables y el endpoint `GET /api/rutas/demo-lima`, que no existe en `src/backend`. Las historias se identifican con los códigos del backlog oficial. |

> Este documento está archivado en `sprint 2/` porque la consigna académica reserva
> las cuatro rutas de `docs/03 Implementación/` para los entregables del Sprint 1.

---

## Historias de Usuario completadas en este Sprint

| ID | Título | Épica | SP | Estado |
|---|---|---|:---:|---|
| US-002 | Editar o eliminar una ruta existente | EP-01 | 3 | Completada |
| US-004 | Visualizar el impacto ambiental estimado de la ruta | EP-02 | 5 | Completada |
| US-005 | Ver la ruta calculada en un mapa interactivo | EP-03 | 5 | Completada |
| US-007 | Listar y buscar mis rutas guardadas | EP-04 | 3 | Completada |

**Total: 16 Story Points completados de 16 comprometidos.**

Qué se implementó en cada una:

- **US-002** — `PUT` y `DELETE` de rutas con recálculo de la ruta optimizada,
  eliminación explícita de los registros de `ruta_puntos` y respeto de **RN-009**,
  **RN-013** y **RN-014**. En la interfaz, edición y borrado con confirmación.
- **US-004** — Cálculo de ahorro de CO₂ a partir del factor de emisión del vehículo,
  con comparación optimizada frente a no optimizada (**RN-018**) y el indicador
  `sin_reduccion_significativa` (**RN-019**).
- **US-005** — Renderizado de la ruta sobre Leaflet con OpenStreetMap, marcadores
  numerados en el orden calculado, aviso controlado ante falla del proveedor de tiles
  y botón **Reintentar**.
- **US-007** — Filtros `desde`, `hasta` y `estado` con rango inclusivo y respuesta
  `400` ante formatos inválidos.

---

## Demostración del trabajo completado

El incremento del Sprint 2 es reproducible sobre la aplicación en ejecución. No se
afirma que una sesión de demostración ante stakeholders se haya realizado, porque el
repositorio no registra evidencia de ese evento.

Recorrido de verificación:

1. Iniciar sesión como operador y abrir `http://localhost:5173`.
2. Pestaña **Rutas**: editar una ruta quitando y agregando puntos; se comprueba que
   conserva su identificador y recalcula las métricas. Se intenta eliminar una ruta
   con entregas en curso para verificar el bloqueo por **RN-013**.
3. Pestaña **Mapa**: se visualiza el recorrido con los puntos en el orden optimizado.
4. Pestaña **Impacto**: se contrasta la ruta optimizada con la no optimizada.
5. En el listado, aplicar un filtro por estado y un rango de fechas sin resultados.

En el backend, la verificación se apoya en dos herramientas versionadas:

- `pytest` — 51 pruebas aprobadas en verde.
- `src/backend/smoke_sprint2.py` y `src/backend/auditoria_api.py` — verificación de
  extremo a extremo sobre la API en ejecución, que terminan sin anomalías.

---

## Pendientes

1. **Pruebas automatizadas del frontend.** `src/frontend` no incluye pruebas; la
   verificación de esa capa se limita a `npm run build`.
2. **RN-002** — Bloqueo por tres intentos fallidos durante 15 minutos: no implementado
   en `src/backend`.
3. **HTTPS** — El cifrado en tránsito no está implementado en el código de
   aplicación; queda a cargo del ambiente de despliegue.
4. **Elementos del Sprint 3** — US-006, EN-03 y US-008.

Estos mismos pendientes figuran en el Informe de Estado del Sprint 2, por lo que ambos
documentos son coherentes entre sí.

---

[← Volver al README principal](../../../README.md)