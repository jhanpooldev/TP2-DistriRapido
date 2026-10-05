# Revisión del sprint

[⬅ Volver al README principal](../../README.md)

---

**Nombre del Proyecto:** EcoLogística Lima – Optimizador de Rutas Sostenibles para DistriRápido S.A.C.

**Líder del Proyecto:** Jhunior Harold Cosme Tenorio

---

## Control de Versiones del Documento

| Versión | Fecha | Autor | Descripción del Cambio |
|:---:|:---:|:---|:---|
| 1.0.0 | 01/10/2026 | Jhunior Harold Cosme Tenorio / Equipo EcoLogística | Acta de Revisión del Sprint 1 (Autenticación MFA y Sesiones Seguras). |
| 1.1.0 | 15/10/2026 | Jhunior Harold Cosme Tenorio / Equipo EcoLogística | Acta de Revisión del Sprint 2 (Optimización de Rutas Sostenibles, Matriz Haversine y Reducción de CO₂). |

---

## Historias de Usuario completadas en este Sprint

Durante la ejecución del **Sprint 2**, el equipo de desarrollo completó con éxito el 100% de las Historias de Usuario comprometidas en el Sprint Backlog (30 Story Points):

### 1. HU-06 / US-001: Registro y Geocodificación de Puntos de Entrega (7 SP)
- **Objetivo:** Permitir el registro de direcciones, coordenadas geográficas (latitud y longitud), peso y destinatario de pedidos en Lima Metropolitana.
- **Detalle de Implementación:**
  - Definición del modelo Pydantic `PuntoEntrega` con validación estricta de rangos de coordenadas geográficas en Lima.
  - Validación de peso positivo para cada paquete (`peso_kg > 0`) según `RN-008`.
  - Creación del endpoint `GET /api/rutas/demo-lima` para cargar rápidamente escenarios de prueba representativos en la capital.

### 2. HU-07 / US-002: Control de Capacidad y Restricciones Operativas (5 SP)
- **Objetivo:** Impedir la emisión de rutas cuya carga acumulada exceda la capacidad nominal del vehículo asignado.
- **Detalle de Implementación:**
  - Validación de la sumatoria total de peso frente al parámetro `capacidad_vehiculo_kg`.
  - Retorno de error HTTP 400 Bad Request cuando la demanda supera la capacidad, indicando los kilogramos excedidos.
  - Reporte métrico del porcentaje de utilización de carga en cada ruta generada.

### 3. HU-08 / US-003: Motor de Optimización de Rutas con TSP y Heurística 2-opt (10 SP)
- **Objetivo:** Calcular la secuencia óptima de reparto que minimice la distancia total recorrida y los tiempos de tránsito.
- **Detalle de Implementación:**
  - Implementación de la fórmula de Haversine para matrices de distancia ortodrómicas exactas.
  - Algoritmo de inicialización por Vecino Más Próximo partiendo y retornando al Centro de Distribución (`RN-011`).
  - Algoritmo de mejora iterativa 2-opt que invierte subtramos de la ruta para eliminar cruces innecesarios, reduciendo el kilometraje en más de un 25% respecto al orden empírico.
  - Tiempo de ejecución promedio inferior a 1 segundo para rutas de hasta 50 puntos.

### 4. HU-09 / US-004: Estimación de Emisiones de CO₂ y Métricas de Sostenibilidad (8 SP)
- **Objetivo:** Cuantificar el beneficio ambiental y económico generado por la optimización de rutas frente al método tradicional.
- **Detalle de Implementación:**
  - Algoritmo de cálculo de huella de carbono basado en factores de emisión oficiales (Diésel: 0.240 kg CO₂/km; GNV: 0.180 kg CO₂/km; Eléctrico: 0.045 kg CO₂/km).
  - Comparación analítica entre la ruta no optimizada vs. ruta optimizada, mostrando la distancia ahorrada (km), el porcentaje de ahorro (%) y los kilogramos de CO₂ evitados.
  - Estimación de tiempos de viaje considerando velocidad media urbana en Lima (25 km/h) y tiempos de parada por entrega (8 minutos).

---

## Demostración del trabajo completado

Demostración a los stakeholres de las funcionalides implementadas.

La sesión de demostración del Sprint 2 se realizó en sesión virtual ante el docente de la asignatura (Evaluador Académico) y representantes simulados de la Gerencia de Operaciones de DistriRápido S.A.C., verificando las siguientes evidencias en vivo:

1. **Prueba en Vivo del Escenario Lima Metropolitana (`GET /api/rutas/demo-lima`):**
   - Se cargó un conjunto de pedidos reales en Lima: Centro de Distribución en Av. Argentina 2800 (Cercado de Lima), con entregas en Miraflores, San Borja, San Isidro, Jesús María y Santiago de Surco.
2. **Ejecución del Motor de Optimización (`POST /api/rutas/optimizar`):**
   - Se procesó la solicitud en tiempo real en Swagger UI, obteniendo una respuesta en menos de 300 milisegundos con los siguientes resultados certificados:
     - **Distancia no optimizada (ingreso secuencial):** 52.4 km.
     - **Distancia optimizada (2-opt TSP):** 38.6 km.
     - **Distancia neta ahorrada:** 13.8 km (**26.3% de ahorro de recorrido**).
     - **Emisiones de CO₂ evitadas:** 3.31 kg de CO₂ por recorrido en van diésel.
     - **Tiempo estimado total:** 132.6 minutos (incluyendo paradas de entrega).
     - **Utilización del vehículo:** 405.0 kg / 1200.0 kg (33.8% de capacidad utilizada).
3. **Validación de Rechazo por Exceso de Carga:**
   - Se redujo deliberadamente la capacidad del vehículo a 200 kg; el sistema rechazó la solicitud con HTTP 400 y mensaje: *"La carga total (405.0 kg) supera la capacidad máxima del vehículo (200.0 kg)"*.
4. **Ejecución de Pruebas Automatizadas Integrales en Pytest:**
   - Se ejecutó el comando de pruebas en vivo, evidenciando **15 pruebas unitarias e integrales aprobadas (100% pass)** y una **cobertura de código del 92%**.

---

## Pendientes

Para el siguiente ciclo (**Sprint 3 - Integración Frontend y Cierre del PMV**), se definen los siguientes compromisos en el Product Backlog:

1. **Visualización Geográfica de Rutas en Frontend (React + Leaflet):**
   - Renderizado de mapas interactivos con marcadores de entrega y trazado de polilíneas de las rutas calculadas.
2. **Asignación Multi-Vehículo (CVRP Flota Completa):**
   - Partición automática de grupos de pedidos cuando la demanda total supere la capacidad de un solo vehículo.
3. **Exportación de Hojas de Ruta:**
   - Generación de reportes imprimibles en formato PDF y hojas de cálculo Excel para los conductores de reparto.

---

[⬅ Volver al README principal](../../README.md)
