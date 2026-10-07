# Informe de estado del proyecto

[← Volver al README principal](../../../README.md)

---

**Nombre del Proyecto:** EcoLogística Lima – Optimizador de Rutas Sostenibles para DistriRápido S.A.C.

**Líder del Proyecto:** Jhunior Harold Cosme Tenorio

**Sprint:** 2 – Iteración de mayor valor sobre lo construido en el Sprint 1

**Periodo:** 19/10/2026 – 01/11/2026

---

## Control de Versiones del Documento

| Versión | Fecha | Autor | Descripción del Cambio |
|:---:|:---:|:---|:---|
| 1.0.0 | 01/10/2026 | Jhunior Harold Cosme Tenorio / Equipo EcoLogística | Elaboración inicial del informe correspondiente al Sprint 1. |
| 2.0.0 | 05/10/2026 | Jhunior Harold Cosme Tenorio / Equipo EcoLogística | Redactado el Sprint 2 (US-002, US-004, US-005, US-007) sobre los cuatro entregables de `docs/03 Implementación/`. |
| 2.1.0 | 05/10/2026 | Jhunior Harold Cosme Tenorio / Equipo EcoLogística | Corrección de trazabilidad: se eliminaron las métricas no verificables (distancias, porcentajes de ahorro, cobertura y totales de pruebas), se sustituyeron los identificadores `HU-06` a `HU-09` por los del backlog oficial (`US-002`, `US-004`, `US-005`, `US-007`), se corrigieron las referencias a reglas de negocio según `docs/inicio/09` y se retirer las afirmaciones sobre MFA/TOTP, presente únicamente en el backend heredado de la raíz del repositorio. |

> Este documento está archivado en `sprint 2/` porque la consigna académica reserva
> las cuatro rutas de `docs/03 Implementación/` para los entregables del Sprint 1.

---

## 1. Resumen del Sprint

El Sprint 2 cubre los elementos **US-002, US-004, US-005 y US-007** del backlog
priorizado (`docs/planificacion/01 Transformando a ágil V_1_0_0.md`, secciones 1.1 y
2). El Sprint 1 permanece documentado en los entregables vigentes de
`docs/03 Implementación/`.

El incremento se concentra en dar salida consultable y editable a las rutas ya
generables desde el Sprint 1: permitir corregirlas cuando cambian los pedidos,
mostrarlas sobre un mapa, quantificar el beneficio ambiental y localizarlas por fecha
y estado.

- **Story Points comprometidos:** 16 (US-004: 5, US-005: 5, US-002: 3, US-007: 3).
- **Story Points completados:** 16.
- **Estado:** los cuatro elementos del Sprint 2 están implementados y verificados.

---

## 2. Historias de Usuario completadas en este Sprint

### US-002 — Editar o eliminar una ruta existente (3 SP, Épica EP-01)

Permite corregir o retirar una ruta guardada cuando la configuración de pedidos
cambia, con las protecciones de las reglas de negocio **RN-009** (puntos de una ruta
confirmada), **RN-013** (rutas con entregas en curso o completadas) y **RN-014**
(capacidad vehicular).

Trabajo entregado y verificable:

- `PUT /api/v1/rutas/{id}` recalcula la ruta optimizada con la nueva lista de puntos y
  confirma la transacción; la edición no genera una ruta duplicada.
- `DELETE /api/v1/rutas/{id}` elimina explícitamente las filas de `ruta_puntos` de la
  ruta, sin dejar registros huérfanos.
- En la interfaz, `RutasTab` ofrece edición y eliminación con confirmación y mensajes
  de resultado.

### US-004 — Visualizar el impacto ambiental estimado de la ruta (5 SP, Épica EP-02)

Compara la ruta optimizada frente a la no optimizada aplicando el factor de emisión
del vehículo seleccionado, en lugar de un valor fijo (**RN-017**, **RN-018**,
**RN-019**).

Trabajo entregado y verificable:

- El cálculo parte de `factor_emision_co2`, `consumo_litros_km` y
  `velocidad_promedio_kmh` del vehículo asignado.
- La respuesta incluye `ahorro_co2_kg`, `ahorro_co2_pct` y `ahorro_distancia_pct`.
- Cuando la reducción no es significativa se expone `sin_reduccion_significativa`
  para no presentar porcentajes negativos o engañosos.
- La pestaña `ImpactoTab` muestra la comparación y el ahorro por ruta.

### US-005 — Ver la ruta calculada en un mapa interactivo (5 SP, Épica EP-03)

Trabajo entregado y verificable:

- `MapView` renderiza la ruta sobre Leaflet con OpenStreetMap, mostrando los puntos
  numerados en el orden optimizado y la polilínea del recorrido.
- Si el proveedor de tiles no responde, se informa con un aviso controlado y un botón
  **Reintentar** que recrea la capa de tiles sin recargar la aplicación.
- `MapPicker` permite elegir coordenadas y geocodificar la dirección.

### US-007 — Listar y buscar mis rutas guardadas (3 SP, Épica EP-04)

Trabajo entregado y verificable:

- `GET /api/v1/rutas` acepta los filtros `desde`, `hasta` y `estado`.
- El rango de fechas es inclusivo: las rutas creadas el mismo día que `hasta` se
  incluyen. Un formato de fecha inválido responde `400` explicando el formato
  esperado, en lugar de ignorarse.
- El listado muestra un aviso cuando el filtro no arroja resultados.

---

## 3. Demostración del trabajo completado

La demostración del Sprint 2 se apoya en el incremento efectivamente construido y es
reproducible sobre la aplicación en ejecución. **No se afirma que una sesión de
demostración ante stakeholders haya ocurrido**, porque el repositorio no registra
evidencia de ese evento.

Con el backend en ejecución y el frontend en `http://localhost:5173`:

1. **Autenticación.** Ingreso con `operador@distrirapido.com` / `operador123`.
   `GET /api/v1/auth/me` devuelve el rol del usuario.
2. **Edición y eliminación (US-002).** Desde la pestaña *Rutas*, se selecciona una
   ruta, se quitan o agregan puntos y se guarda; la ruta conserva su identificador y
   recalcula distancia, tiempo y emisiones. Se comprueba que una ruta con entregas en
   curso o completada no puede eliminarse.
3. **Mapa (US-005).** La pestaña *Mapa* muestra el recorrido con los puntos numerados
   en el orden calculado.
4. **Impacto ambiental (US-004).** La pestaña *Impacto* contrasta la distancia y el
   CO₂ de la ruta optimizada frente a la no optimizada, con el factor del vehículo
   asignado.
5. **Búsqueda (US-007).** Se filtra el listado por estado *Confirmada* y por un rango
   de fechas sin resultados, verificando el aviso correspondiente.

---

## 4. Pendientes

Estos puntos quedaron fuera del Sprint 2 y no se deben reportar como completados:

1. **Cobertura de pruebas del frontend.** No existen pruebas automatizadas en
   `src/frontend`; la verificación del frontend se limitó a `npm run build`. El
   README lo refleja en la sección de ejecución de pruebas.
2. **RN-002 — Bloqueo por intentos fallidos.** La regla de bloqueo tras tres intentos
   fallidos no está implementada en `src/backend`.
3. **Cifrado HTTPS.** El Sprint 1 lo dejó pendiente; la aplicación sirve HTTP local y
   el cifrado en tránsito sigue a cargo del ambiente de despliegue.
4. **US-006 y US-008** (detalle de paradas en el mapa y exportación de resumen),
   junto con **EN-03** (pipeline de CI/CD), correspondientes al Sprint 3.

---

[← Volver al README principal](../../../README.md)