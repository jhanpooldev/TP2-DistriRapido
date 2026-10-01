# SPECS.md

Especificación técnica del sistema **EcoLogística Lima – Optimizador de Rutas Sostenibles para DistriRápido S.A.C.**

Este documento resume la especificación del sistema. Cuando un detalle normativo
requiere precisión (criterios de aceptación, fórmulas de cálculo, DDL), la fuente
de verdad es el documento correspondiente en `docs/inicio/`, referenciado en cada
sección.

| Documento de referencia | Contenido |
|---|---|
| `docs/inicio/06. Requisitos funcionales` | RF-001 a RF-014 con criterios BDD |
| `docs/inicio/07. Requisitos no funcionales` | RNF-001 a RNF-015 con métricas SMART |
| `docs/inicio/08. Usuarios` | Actores y matriz de control de acceso |
| `docs/inicio/09. Reglas de negocio` | RN-001 a RN-020 con matriz de trazabilidad |
| `docs/inicio/10. Stack tecnológico` | Evaluación y selección del stack |
| `docs/inicio/11. Base de datos` | Modelo conceptual, lógico y físico (DDL) |
| `docs/inicio/12. Modelo C4` | Arquitectura por niveles |
| `docs/inicio/13. Restricciones` | Restricciones multidimensionales del proyecto |

---

# Descripción del Proyecto

Desarrollar un sistema web inteligente para la planificación y optimización de rutas de distribución urbana para DistriRápido S.A.C., considerando distancia, tiempo estimado, capacidad de vehículos y criterios de sostenibilidad.
El sistema permitirá generar rutas optimizadas para las entregas, mejorar el uso de los vehículos y reducir distancias, tiempos de recorrido y emisiones de CO₂.

---

# Tecnologías
PostgreSQL (Base de datos)
FastAPI (Backend en Python)
React + Vite (Frontend)
SQLAlchemy (ORM)
Alembic (Migraciones)
Tailwind CSS (Interfaz)
Axios (Comunicación Frontend-Backend)
pytest + pytest-cov (Pruebas Backend)
Vitest (Pruebas Frontend)

---

# Objetivo del Sistema
Generar automáticamente rutas de distribución eficientes y sostenibles, considerando las restricciones operativas de la empresa y buscando reducir costos, tiempos de recorrido, distancia recorrida y emisiones de CO₂.

---
# Entradas del Sistema

Centro de distribución (ubicación de origen y retorno de toda ruta)
Direcciones o coordenadas de los puntos de entrega
Destinatario de cada punto de entrega
Cantidad y peso de los pedidos
Prioridad de las entregas
Vehículos disponibles y su capacidad
Perfil de cálculo del vehículo (consumo, factor de emisión, velocidad promedio)
Parámetros de sostenibilidad configurados
Límite de puntos admitidos por ruta

---

# Salidas del Sistema

Ruta optimizada
Secuencia de puntos de entrega (orden de visita)
Vehículo asignado
Distancia total recorrida
Tiempo estimado de recorrido
Distancia y tiempo del escenario no optimizado
Cantidad de entregas asignadas
Nivel de utilización del vehículo
Estimación de emisiones de CO₂
Ahorro estimado de distancia y de emisiones frente a la ruta no optimizada
Puntos pendientes por capacidad insuficiente
Estado de la ruta
Visualización de rutas en mapa (o formato tabular degradado)
Exportación de resultados (opcional, fuera del PMV)
---

# Actores del Sistema

Los tres actores Directos del PMV se describen en detalle en el documento
`docs/inicio/08. Usuarios`. Los actores Indirectos (docente, gerencia simulada y
API de mapas) no tienen credenciales de acceso al sistema.

## Administrador
Gestionar usuarios y roles
Configurar el centro de distribución
Configurar parámetros del sistema
Visualizar información general

## Operador Logístico
Registrar y gestionar puntos de entrega
Asignar prioridades
Ejecutar la generación de rutas
Visualizar rutas generadas
Consultar incidencias
Confirmar rutas

## Gerente
Visualizar indicadores logísticos
Consultar rutas generadas
Visualizar costos y tiempos
Consultar indicadores de sostenibilidad
Visualizar reportes

## Fuera del alcance del PMV

Las siguientes entidades quedan para versiones posteriores, según la nota NOT-05
del documento `docs/inicio/11. Base de datos`:

- **Conductor:** gestión de conductores y asignación conductor–vehículo.
- **Zona de distribución:** agrupación geográfica de puntos de entrega.
- **Pedido y Entrega:** trazabilidad comercial del pedido hasta su entrega.

Las reglas de negocio que sí se aplican en el PMV están consolidadas en el
documento `docs/inicio/09. Reglas de negocio` (RN-001 a RN-020) y son la fuente
de verdad para el cálculo de distancias, tiempos y emisiones.

---
# Reglas de Negocio

La especificación completa y trazable de las reglas de negocio se encuentra en el
documento `docs/inicio/09. Reglas de negocio` (RN-001 a RN-020). Resumen:

## Seguridad y control de acceso (RN-001 a RN-006)
Un usuario solo ingresa si su correo existe y la contraseña coincide tras el hash (RN-001).
Tres intentos fallidos consecutivos bloquean la cuenta por 15 minutos (RN-002).
Cada usuario accede solo a los módulos permitidos por su rol (RN-003).
Las contraseñas se almacenan únicamente como hash bcrypt irreversible (RN-004).
La sesión expira a las 8 horas de iniciarse (RN-005).
Las credenciales y claves de API se manejan por variables de entorno y no se exponen en los mensajes de error (RN-006).

## Operación y validaciones (RN-007 a RN-013)
Un punto de entrega solo se registra con dirección o coordenada válida (RN-007).
El peso de un punto de entrega debe ser mayor que cero (RN-008).
Un punto que ya pertenece a una ruta confirmada no puede modificarse ni eliminarse (RN-009).
Se requieren al menos 2 puntos de entrega válidos, además del centro de distribución, para generar una ruta (RN-010).
Toda ruta inicia y termina en el centro de distribución (RN-011).
Una ruta solo se conserva si el operador la confirma explícitamente (RN-012).
Una ruta con entregas completadas no puede eliminarse (RN-013).

## Cálculo y sostenibilidad (RN-014 a RN-020)
La carga total asignada a una ruta no puede superar la capacidad del vehículo; los puntos excedentes quedan pendientes por capacidad insuficiente (RN-014).
La distancia total es la suma de las distancias entre el centro de distribución, cada punto visitado en orden y el retorno al centro (RN-015).
El tiempo estimado se obtiene de la distancia total dividida por la velocidad promedio del vehículo (RN-016).
Las emisiones de CO₂ equivalen al consumo estimado de combustible multiplicado por el factor de emisión del vehículo (RN-017).
El ahorro se calcula contrastando la ruta optimizada frente a la ruta no optimizada (mismos puntos en orden de ingreso) (RN-018).
Los indicadores de sostenibilidad se calculan a partir del conjunto de rutas confirmadas (RN-019).
El panel del gerente muestra cantidad de rutas, distancia total y emisiones estimadas; si no hay rutas, todos los valores muestran cero (RN-020).

---

# Restricciones del Sistema

## Restricciones Duras (verificadas con pruebas automatizadas)
No superar la capacidad máxima del vehículo (RN-014).
No duplicar la asignación de un vehículo.
No duplicar un punto de entrega dentro de una misma planificación.
Todo punto asignado debe estar asociado a un vehículo cuando la ruta se confirma.
La ruta debe iniciar y terminar en el centro de distribución (RN-011).
Se requieren al menos 2 puntos de entrega válidos para generar una ruta (RN-010).
Los puntos no pueden quedar fuera de la planificación sin generar una incidencia.
Las ubicaciones deben ser válidas para generar una ruta (RN-007).

## Restricciones Blandas (objetivo de optimización, no bloquean la ejecución)
Minimizar la distancia total recorrida.
Minimizar el tiempo total de recorrido.
Reducir el consumo estimado de combustible.
Reducir las emisiones de CO₂.
Maximizar la utilización de la capacidad de los vehículos.
Priorizar entregas urgentes.
Reducir tiempos muertos.
Equilibrar la carga entre vehículos.

Las restricciones blandas se implementan como criterios de la función de puntuación
que evalúa el motor de ruteo (ver "Criterios de Optimización").

---
# Casos Límite

No existen vehículos disponibles → retornar error controlado.
La capacidad de los vehículos es insuficiente → generar incidencia y marcar los puntos excedentes como pendientes.
Existe una dirección o coordenada inválida → impedir el registro del punto (RN-007).
Existe menos de 2 puntos de entrega → responder que se requieren al menos 2 puntos (RN-010).
Existe una única solución razonable → la ruta se genera y queda disponible para su validación.
No existe solución óptima → generar la mejor solución disponible y registrar una advertencia.
Existen múltiples soluciones → seleccionar la solución con mejor puntuación.
Un punto no puede ser asignado → marcarlo como pendiente.
No existen puntos de entrega registrados → informar que no hay puntos suficientes para planificar una ruta.
Error durante la optimización → mantener los datos existentes y retornar error controlado, sin persistir registros parciales.

---

# Requisitos Funcionales

La especificación completa de los requisitos funcionales del PMV, con sus criterios
de aceptación en formato Gherkin/BDD, se encuentra en el documento
`docs/inicio/06. Requisitos funcionales` (RF-001 a RF-014). Resumen por rol:

## Administrador
RF-002: Registrar usuarios
RF-003: Control de acceso por rol
RF-005: Gestión de puntos de entrega
RF-010: Confirmación y gestión de rutas
RF-014: Cierre de sesión

## Operador Logístico
RF-003: Control de acceso por rol
RF-004: Registro de puntos de entrega
RF-005: Gestión de puntos de entrega
RF-006: Generación de ruta optimizada
RF-007: Estimación de restricciones de capacidad
RF-008: Comparación de impacto ambiental (CO₂)
RF-010: Confirmación y gestión de rutas
RF-011: Visualización de rutas históricas
RF-014: Cierre de sesión

## Gerente
RF-003: Control de acceso por rol
RF-011: Visualización de rutas históricas
RF-012: Visualización de indicadores de sostenibilidad
RF-013: Panel de indicadores (dashboard)
RF-014: Cierre de sesión

## Autenticación (todos los roles)
RF-001: Autenticación de usuarios
RF-014: Cierre de sesión

---
# Funcionalidades

Estado de cada funcionalidad del sistema respecto al alcance del Producto Mínimo Viable (PMV).

| Funcionalidad | Requisito | Estado en el PMV |
|--------------|-----------|------------------|
| Autenticación y autorización (JWT + RBAC) | RF-001, RF-003, EN-02 | Requerido |
| Gestión de usuarios y roles | RF-002 | Requerido |
| Registro de puntos de entrega | RF-004, US-001 | Requerido |
| Gestión de puntos de entrega | RF-005 | Requerido |
| Parámetros de vehículo (capacidad, emisión, consumo) | RF-007, RN-014 | Requerido |
| Optimización de rutas | RF-006, US-003 | Requerido |
| Cálculo de distancia, tiempo y CO₂ | RF-006, RF-008, RN-015..RN-017 | Requerido |
| Comparación de impacto ambiental (optimizada vs. no optimizada) | RF-008, US-004 | Requerido |
| Confirmación y gestión de rutas | RF-010, RN-012, RN-013 | Requerido |
| Visualización de rutas (mapa interactivo) | RF-009, US-005 | Requerido |
| Detalle de paradas en el mapa | RF-009, US-006 | Requerido |
| Panel de gestión del operador (listado y búsqueda) | RF-011, US-007 | Requerido |
| Indicadores logísticos del gerente | RF-013, RN-020 | Requerido |
| Indicadores de sostenibilidad | RF-012, RN-019 | Requerido |
| Cierre de sesión | RF-014 | Requerido |
| Gestión de conductores | — | Fuera del PMV |
| Gestión de zonas de distribución | — | Fuera del PMV |
| Gestión de pedidos y entregas | — | Fuera del PMV |
| Reporte de incidencias | — | Fuera del PMV |
| Seguimiento GPS en tiempo real | — | Fuera del PMV |
| Exportación de reportes | — | Deseado (post-PMV) |
| Historial avanzado de rutas | — | Deseado (post-PMV) |

---

# API REST (Resumen)

Base de la API: `/api/v1`. Todas las rutas, salvo el login y el health check,
requieren cabecera `Authorization: Bearer <token>` (EN-02) y aplican control de
acceso por rol (RF-003).

## Salud
GET /api/v1/health

## Autenticación
POST /api/v1/auth/login
GET /api/v1/auth/me

## Usuarios (solo Administrador)
GET /api/v1/usuarios
POST /api/v1/usuarios
GET /api/v1/usuarios/{id}
PUT /api/v1/usuarios/{id}

## Puntos de entrega (Operador Logístico)
GET /api/v1/puntos-entrega
POST /api/v1/puntos-entrega
GET /api/v1/puntos-entrega/{id}
PUT /api/v1/puntos-entrega/{id}
DELETE /api/v1/puntos-entrega/{id}

## Rutas
POST /api/v1/rutas/optimizar
GET  /api/v1/rutas
POST /api/v1/rutas
GET  /api/v1/rutas/{id}
GET  /api/v1/rutas/{id}/puntos
PUT  /api/v1/rutas/{id}
DELETE /api/v1/rutas/{id}
GET  /api/v1/rutas/{id}/resumen

## Vehículos (solo lectura en el PMV)
GET /api/v1/vehiculos

## Indicadores
GET /api/v1/indicadores
GET /api/v1/indicadores/sostenibilidad

Nota: `POST /api/v1/rutas/optimizar` devuelve la ruta calculada **sin persistirla**
(cálculo stateless). `POST /api/v1/rutas` la confirma y la registra (RN-012).
`PUT /api/v1/rutas/{id}` reemplaza el conjunto de puntos de una ruta guardada y
recalcula la secuencia optimizada sobre esa nueva configuración (US-002), por lo
que requiere al menos dos puntos válidos (RN-010). Las operaciones de edición y
eliminación se rechazan si la ruta ya tiene entregas completadas (RN-009, RN-013).

`GET /api/v1/rutas/{id}/resumen` devuelve el resumen exportable de la ruta
(puntos, orden de visita e impacto ambiental estimado) con los mismos datos que
`GET /api/v1/rutas/{id}/puntos` más los indicadores de la ruta; el formateo a PDF
o CSV se resuelve en el cliente a partir de esa respuesta (US-008). El endpoint
responde `404` si la ruta aún no ha sido calculada ni confirmada.

---
# Modelo de Datos (Alto Nivel)

El esquema completo, con tipos, restricciones y DDL en SQL, se encuentra en el
documento `docs/inicio/11. Base de datos`. Las entidades del PMV son:

| Tabla | Descripción |
|---|---|
| roles | Catálogo de roles del sistema (Administrador, Operador Logístico, Gerente) |
| usuarios | Cuentas de acceso con correo, hash de contraseña y rol asignado |
| puntos_entrega | Puntos de entrega: dirección, coordenadas, peso y destinatario |
| parametros_vehiculo | Perfil de cálculo por vehículo: capacidad, emisión, consumo y velocidad |
| rutas | Ruta generada: métricas calculadas, escenario no optimizado y estado |
| ruta_puntos | Tabla intermedia que materializa el orden de visita de cada punto en una ruta |

Relaciones principales:

- rol → usuario (N:1)
- usuario → punto_entrega (1:N) — el operador que registra el punto
- usuario → ruta (1:N) — el operador que genera la ruta
- parametros_vehiculo → ruta (1:N) — el vehículo asignado
- ruta ↔ punto_entrega (N:M, a través de ruta_puntos, con el campo `orden`)

Las tablas de conductores, zonas, pedidos, entregas e incidencias quedan fuera del
alcance del PMV (nota NOT-05 de `docs/inicio/11. Base de datos`).

---
# Requisitos de Interfaz (UI)

Diseño responsive utilizando Tailwind CSS.
Panel principal según el rol del usuario autenticado.
Gestión mediante tablas y formularios.
Formulario de registro de puntos de entrega.
Formulario de inicio de sesión.
Vista de la ruta optimizada (secuencia de paradas, distancia, tiempo y CO₂).
Comparación lado a lado de la ruta optimizada y la no optimizada.
Visualización de rutas mediante mapa (con degradación a formato tabular si el servicio de mapas no responde).
Visualización de las paradas de una ruta.
Indicadores logísticos.
Indicadores de sostenibilidad.
Visualización de rutas históricas con filtros por fecha y estado.
Estados de carga y error visibles en todas las vistas.
Validación de formularios con mensajes en español.
Interfaz accesible conforme a WCAG 2.1 nivel AA (etiquetas asociadas y contraste ≥ 4.5:1).

---
# Requisitos No Funcionales

Detalle completo con escenarios de calidad y métricas SMART en `docs/inicio/07. Requisitos no funcionales` (RNF-001 a RNF-015).

## Rendimiento
Tiempo de generación de rutas ≤ 5 segundos (P95) para conjuntos de hasta 20 puntos de entrega.
Tiempo de generación de rutas ≤ 50 segundos (P95) para el escenario completo del PMV (50 puntos).
Latencia de consultas de lectura ≤ 1.5 segundos (P95).
Soporte inicial para al menos 50 puntos de entrega por ruta.

## Seguridad
Autenticación mediante JWT con expiración de 8 horas (EN-02).
Hashing seguro de contraseñas mediante bcrypt (RN-004).
Bloqueo de 3 intentos fallidos durante 15 minutos (RN-002).
Control de acceso basado en roles (RN-003).
Seguridad basada en OWASP Top 10.

## Calidad
Validación de datos mediante Pydantic.
Arquitectura modular.
Separación Frontend / Backend.
API RESTful.
Documentación automática mediante Swagger/OpenAPI.
Diseño responsive.
Cobertura de pruebas ≥ 70% (módulos de validación ≥ 80%).
Cobertura ≥ 80% sobre el código nuevo o modificado según el DoD global.

---

# Criterios de Optimización

La generación de rutas considera una función de optimización basada en criterios logísticos y ambientales.

Los principales criterios son:

Minimizar la distancia recorrida (criterio principal del PMV).
Minimizar el tiempo de recorrido.
Minimizar las emisiones estimadas de CO₂.
Maximizar la utilización de la capacidad vehicular.
Priorizar las entregas según su urgencia.

Implementación en el PMV:

- El motor de ruteo aplica la heurística del vecino más cercano sobre una matriz de distancias calculada con la fórmula de Haversine.
- La solución inicial se mejora iterativamente con la técnica 2-opt hasta alcanzar una solución localmente óptima o agotar el presupuesto de iteraciones definido.
- El tiempo de ejecución se acota para satisfacer el SLA de 5 segundos (P95) con hasta 20 puntos (EN-01, RNF-001).
- Cuando el conjunto de puntos supera el límite admitido, el sistema responde con un error controlado en lugar de bloquearse (EN-01).

La solución no optimizada se calcula con el mismo conjunto de puntos en el orden de ingreso, y sirve como línea base para el cálculo de ahorro (RN-018).

---

# Indicadores de Sostenibilidad

El sistema deberá permitir estimar indicadores como:
Distancia total recorrida.
Tiempo total estimado.
Consumo estimado de combustible.
Emisiones estimadas de CO₂.
Emisiones por entrega.
Utilización promedio de vehículos.
Ahorro estimado de distancia.
Ahorro estimado de emisiones.
Los valores ambientales deberán considerarse estimaciones calculadas a partir de los parámetros configurados del vehículo y la ruta.
Los indicadores se calculan a partir del conjunto de rutas confirmadas registradas en el sistema (RN-019).
Si no existen rutas registradas, el panel muestra los indicadores en cero (RN-020).

---

# Seguridad

El sistema deberá implementar:
Autenticación mediante JWT.
Control de acceso basado en roles.
Validación de entradas mediante Pydantic.
Hashing seguro de contraseñas mediante bcrypt.
Protección frente a SQL Injection mediante SQLAlchemy.
Rate limiting cuando corresponda.
Variables de entorno para información sensible.
HTTPS en producción.
Manejo seguro de errores.
No exposición de credenciales, tokens o información sensible.

---

# Criterios de Aceptación

El sistema se considera funcional para el PMV cuando:

Los usuarios pueden autenticarse correctamente y la sesión expira a las 8 horas (RF-001, EN-02).
Los roles tienen acceso únicamente a las funciones correspondientes (RF-003).
El administrador puede registrar usuarios con su rol asignado (RF-002).
Los puntos de entrega pueden registrarse con dirección o coordenadas válidas y no se aceptan ubicaciones inválidas (RF-004, RN-007).
Los puntos de entrega no pueden modificarse ni eliminarse si pertenecen a una ruta confirmada (RN-009).
El sistema genera una ruta optimizada a partir de 2 o más puntos válidos (RF-006, RN-010).
La ruta inicia y termina en el centro de distribución (RN-011).
La capacidad de los vehículos es respetada y los puntos excedentes quedan marcados como pendientes (RF-007, RN-014).
La distancia total, el tiempo estimado y las emisiones de CO₂ se calculan según RN-015, RN-016 y RN-017.
El sistema muestra la comparación entre la ruta optimizada y la no optimizada sin presentar porcentajes negativos (RF-008, RN-018).
Las rutas confirmadas se registran y pueden consultarse; las rutas con entregas completadas no pueden eliminarse (RF-010, RN-012, RN-013).
Las rutas generadas pueden visualizarse en un mapa o degradarse a formato tabular si el servicio externo no responde (RF-009).
Las entregas pueden consultarse por ruta en su orden de visita.
Los indicadores logísticos y de sostenibilidad pueden visualizarse (RF-012, RF-013).
Las pruebas automatizadas se ejecutan correctamente.
La cobertura global alcanza como mínimo el 70%.
El tiempo de generación de ruta para 20 puntos se cumple en el 95% de las ejecuciones (EN-01, RNF-001).

---

# Mejoras Futuras

Optimización multiobjetivo avanzada.
Integración con servicios de mapas.
Información de tráfico en tiempo real.
Geocodificación automática de direcciones.
Seguimiento GPS de vehículos.
Predicción de tiempos de llegada.
Predicción de demanda.
Optimización dinámica de rutas.
Integración con sistemas ERP.
Aplicación móvil para conductores.
Notificaciones a clientes.
Historial avanzado de emisiones.
Machine Learning para predicción de demanda y tiempos.

---

# Cumplimiento SDD

Este documento define las entradas, salidas, actores, reglas de negocio, restricciones, funcionalidades, API, modelo de datos, requisitos no funcionales y criterios de aceptación del sistema.

Su objetivo es reducir la ambigüedad durante el desarrollo y mantener coherencia entre los requisitos, el diseño, la implementación y las pruebas del proyecto EcoLogística Lima.