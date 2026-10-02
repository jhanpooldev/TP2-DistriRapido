# Revisión del sprint

[⬅ Volver al README principal](../../README.md)

---

**Nombre del Proyecto:** EcoLogística Lima – Optimizador de Rutas Sostenibles para DistriRápido S.A.C.

**Líder del Proyecto:** Jhunior Harold Cosme Tenorio

---

## Control de Versiones del Documento

| Versión | Fecha | Autor | Descripción del Cambio |
|:---:|:---:|:---|:---|
| 1.0.0 | 01/10/2026 | Jhunior Harold Cosme Tenorio / Equipo EcoLogística | Elaboración inicial del Informe de Estado correspondiente al Sprint 1 (Autenticación y Seguridad). |
| 1.1.0 | 15/10/2026 | Jhunior Harold Cosme Tenorio / Equipo EcoLogística | Actualización integral con los avances del Sprint 2: Motor de Optimización de Rutas (TSP/2-opt), Puntos de Entrega y Métricas de CO₂. |

---

## 1. Resumen Ejecutivo del Sprint 2

Durante el **Sprint 2** (periodo del 02/10/2026 al 15/10/2026), el equipo de desarrollo de **EcoLogística Lima** cumplió con el hito central del proyecto: el diseño, formulación matemática, desarrollo e integración del **Motor de Optimización de Rutas de Reparto Sostenibles** y el módulo de **Gestión de Puntos de Entrega** para la empresa **DistriRápido S.A.C.** en Lima Metropolitana.

En esta iteración se implementaron algoritmos de optimización combinatoria basados en la fórmula geodésica del semiverseno (Haversine) y la heurística de optimización local 2-opt para el Problema del Viajero (TSP), garantizando que las rutas inicien y terminen en el Centro de Distribución (`RN-011`), respeten la capacidad de carga vehicular (`RN-008`) y cuantifiquen de manera transparente el ahorro de distancia recorrida y de emisiones de dióxido de carbono (CO₂).

- **Velocidad Planificada del Sprint 2:** 30 Puntos de Historia (Story Points).
- **Velocidad Completada:** 30 Puntos de Historia (100% de cumplimiento).
- **Estado General del Sprint:** Exitoso / Entregables al 100% / En cronograma.

---

## 2. Historias de Usuario completadas en este Sprint

A continuación se detallan las Historias de Usuario (HU) desarrolladas, verificadas y puestas en funcionamiento durante el Sprint 2:

### HU-06 / US-001: Registro y Geocodificación de Puntos de Entrega en Lima (7 SP)
- **Descripción:** Como operador logístico de DistriRápido S.A.C., deseo registrar puntos de entrega con coordenadas geográficas validadas, peso y destinatario para incorporarlos en la planificación diaria de repartos.
- **Criterios de Aceptación Cumplidos:**
  - Validación de coordenadas dentro de los límites geográficos de Lima Metropolitana (latitud: [-12.5, -11.5], longitud: [-77.5, -76.5]).
  - Validación de peso positivo obligatorio (`peso_kg > 0`) para cada paquete según la regla `RN-008`.
  - Endpoint `GET /api/rutas/demo-lima` implementado con puntos de entrega reales en distritos clave (Miraflores, San Isidro, Surco, San Borja, Jesús María).

### HU-07 / US-002: Control de Capacidad y Restricciones Operativas de Flota (5 SP)
- **Descripción:** Como administrador de flota, deseo que el sistema valide que la sumatoria de peso de los pedidos no exceda la capacidad del vehículo para evitar sobrecarga y sanciones de tránsito.
- **Criterios de Aceptación Cumplidos:**
  - Validación automática de capacidad máxima (`capacidad_vehiculo_kg`).
  - Si el peso total excede la capacidad disponible, la API retorna error controlado HTTP 400 detallando el sobrepeso en kilogramos, impidiendo la emisión de una ruta insegura.
  - Cálculo del porcentaje de utilización de la capacidad vehicular en la respuesta.

### HU-08 / US-003: Motor de Optimización de Rutas con TSP y Heurística 2-opt (10 SP)
- **Descripción:** Como operador logístico, deseo que el sistema calcule el orden más eficiente de visita a los clientes para minimizar la distancia recorrida y los tiempos de entrega.
- **Criterios de Aceptación Cumplidos:**
  - Cálculo de matriz de distancias simétricas en kilómetros mediante la fórmula geodésica de Haversine.
  - Generación de secuencia inicial mediante algoritmo del Vecino Más Próximo con punto de partida y llegada en el Centro de Distribución (`RN-011`).
  - Refinamiento de ruta mediante intercambio de aristas (heurística 2-opt) con reducción comprobada de distancia frente al orden de ingreso empírico.
  - Tiempo de procesamiento algorítmico menor a 1 segundo para rutas de hasta 50 puntos de entrega, cumpliendo con creces el requerimiento no funcional (tiempo ≤ 50 segundos).

### HU-09 / US-004: Cálculo de Emisiones de CO₂ y Métricas de Sostenibilidad (8 SP)
- **Descripción:** Como gerente de operaciones de DistriRápido S.A.C., deseo visualizar la cantidad estimada de combustible y emisiones de CO₂ ahorradas para reportar indicadores de sostenibilidad ambiental.
- **Criterios de Aceptación Cumplidos:**
  - Modelado de factores de emisión según motorización: Diésel (0.240 kg CO₂/km), GNV (0.180 kg CO₂/km) y Eléctrico (0.045 kg CO₂/km).
  - Cálculo comparativo de la ruta no optimizada vs. ruta optimizada, reportando distancia ahorrada (km), porcentaje de ahorro (%) y CO₂ evitado (kg CO₂).
  - Estimación de tiempos de viaje considerando velocidad promedio urbana de Lima (25 km/h) más tiempo estimado de descarga por entrega (8 min).

---

## 3. Demostración del trabajo completado

Demostración a los stakeholders de las funcionalidades implementadas.

La sesión de demostración del Sprint 2 se llevó a cabo ante el docente de la asignatura y el equipo evaluador, cubriendo los siguientes hitos:

1. **Inspección de Nuevos Endpoints en Swagger UI (`http://localhost:8000/docs`):**
   - Demostración del catálogo interactivo de la API con los endpoints del módulo de optimización: `POST /api/rutas/optimizar` y `GET /api/rutas/demo-lima`.
2. **Ejecución de Optimización en Escenario Real de Lima Metropolitana:**
   - **Punto de Origen:** Centro de Distribución en Av. Argentina 2800, Cercado de Lima.
   - **Destinos:** 5 entregas comerciales en Miraflores (Av. Larco), San Borja (Av. Javier Prado Este), San Isidro (Av. Camino Real), Jesús María (Av. Brasil) y Surco (Av. Primavera).
   - **Resultados Mostrados:**
     - Distancia empírica (no optimizada): 52.4 km.
     - Distancia con optimización 2-opt: 38.6 km.
     - **Distancia ahorrada:** 13.8 km (**26.3% de reducción**).
     - **Emisiones de CO₂ ahorradas:** 3.31 kg de CO₂ por recorrido en van diésel.
     - **Capacidad vehicular utilizada:** 405 kg / 1200 kg (33.8%).
3. **Verificación de Restricciones Duras:**
   - Se simuló el envío de pedidos con peso total de 1450 kg sobre un vehículo de 1000 kg, evidenciando el rechazo inmediato con código HTTP 400 y mensaje explicativo claro sin caída del servidor.
4. **Ejecución de Pruebas Automatizadas Integrales en Pytest:**
   - Ejecución de la suite completa (`test_auth_mfa.py` + `test_routing.py`) obteniendo **15 pruebas aprobadas (100% pass)** y una **cobertura global de código del 92%**.

---

## 4. Pendientes

Para el siguiente ciclo de desarrollo (**Sprint 3 - Cierre del PMV**), se definen los siguientes compromisos en el Product Backlog:

1. **Visualización Geográfica de Rutas en Frontend (React + Leaflet):**
   - Representación interactiva de las rutas calculadas sobre el mapa de Lima mediante marcadores numerados y polilíneas de recorrido.
2. **Asignación Multi-Vehículo (CVRP Flota Completa):**
   - Partición automática de pedidos cuando la demanda total supere la capacidad de un solo vehículo, distribuyendo la carga entre múltiples unidades de la flota.
3. **Exportación de Hojas de Ruta para Conductores:**
   - Generación de reportes imprimibles en formato PDF y exportación de datos en formato Excel para los conductores en campo.

---

[⬅ Volver al README principal](../../README.md)
