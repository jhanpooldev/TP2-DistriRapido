# SPECS.md

# Descripción del Proyecto

Desarrollar un sistema web inteligente para la planificación y optimización de rutas de distribución urbana para DistriRápido S.A.C., considerando distancia, tiempo, tráfico, capacidad de vehículos y criterios de sostenibilidad.
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
Direcciones o puntos de entrega
Ubicación del centro de distribución
Pedidos registrados
Cantidad y peso de los pedidos
Prioridad de las entregas
Vehículos disponibles
Capacidad de los vehículos
Ubicación actual de los vehículos
Disponibilidad de los vehículos
Distancia entre puntos
Tiempo estimado de recorrido
Información de tráfico disponible
Restricciones de circulación
Parámetros de sostenibilidad

---

# Salidas del Sistema
Ruta optimizada
Secuencia de puntos de entrega
Vehículo asignado
Distancia total recorrida
Tiempo estimado de recorrido
Cantidad de entregas asignadas
Nivel de utilización del vehículo
Estimación de emisiones de CO₂
Ahorro estimado frente a una ruta no optimizada
Estado de la ruta
Reporte de incidencias o conflictos
Visualización de rutas en mapa
Exportación de resultados (opcional)

---

# Actores del Sistema

## Administrador
Gestionar usuarios y roles
Gestionar vehículos
Gestionar conductores
Gestionar zonas de distribución
Gestionar parámetros del sistema
Visualizar información general

## Operador Logístico
Registrar y gestionar pedidos
Registrar puntos de entrega
Asignar prioridades
Ejecutar la generación de rutas
Visualizar rutas generadas
Consultar incidencias

## Conductor
Visualizar ruta asignada
Consultar secuencia de entregas
Consultar información de cada entrega
Actualizar estado de las entregas

## Gerente
Visualizar indicadores logísticos
Consultar rutas generadas
Visualizar costos y tiempos
Consultar indicadores de sostenibilidad
Visualizar reportes

---

# Reglas de Negocio
Un pedido debe contar con una dirección o ubicación válida.
Cada pedido debe tener una cantidad o peso registrado.
Un vehículo no puede superar su capacidad máxima.
Un vehículo no puede estar asignado a dos rutas simultáneamente.
Cada entrega debe pertenecer a una ruta.
Cada entrega debe tener un estado definido.
Las rutas deben iniciar desde el centro de distribución.
Las rutas deben respetar la disponibilidad de los vehículos.
Las rutas deben considerar las restricciones operativas configuradas.
La carga total asignada a un vehículo no debe superar su capacidad.
Los vehículos deben contar con información necesaria para estimar emisiones.
Las rutas generadas deben poder ser validadas antes de su ejecución.

---

# Restricciones del Sistema

## Restricciones Duras
No superar la capacidad máxima del vehículo.
No duplicar la asignación de un vehículo.
No duplicar una entrega dentro de una misma planificación.
Toda entrega debe estar asociada a un vehículo cuando la ruta sea confirmada.
La ruta debe iniciar desde el centro de distribución.
La ruta debe considerar la disponibilidad del vehículo.
Los pedidos no pueden quedar fuera de la planificación sin generar una incidencia.
Las ubicaciones deben ser válidas para generar una ruta.

## Restricciones Blandas
Minimizar la distancia total recorrida.
Minimizar el tiempo total de recorrido.
Reducir el consumo estimado de combustible.
Reducir las emisiones de CO₂.
Maximizar la utilización de la capacidad de los vehículos.
Priorizar entregas urgentes.
Reducir tiempos muertos.
Equilibrar la carga entre vehículos.

---

# Casos Límite
No existen vehículos disponibles → retornar error controlado.
La capacidad de los vehículos es insuficiente → generar incidencia.
Existe una dirección inválida → impedir la generación de la ruta correspondiente.
No existe solución óptima → generar la mejor solución disponible y registrar advertencia.
Existen múltiples soluciones → seleccionar la solución con mejor puntuación.
Un pedido no puede ser asignado → marcar pedido como pendiente.
Un vehículo no tiene capacidad suficiente → excluirlo de la asignación.
No existen pedidos pendientes → informar que no existen entregas por planificar.
Error durante la optimización → mantener los datos existentes y retornar error controlado.

---

# Requisitos Funcionales

## Administrador
Registrar usuarios.
Gestionar roles.
Registrar vehículos.
Actualizar vehículos.
Consultar vehículos.
Gestionar conductores.
Gestionar zonas de distribución.
Configurar parámetros del sistema.
Consultar información general.

## Operador Logístico
Registrar pedidos.
Actualizar pedidos.
Consultar pedidos.
Eliminar pedidos cuando corresponda.
Registrar puntos de entrega.
Asignar prioridades.
Consultar pedidos pendientes.
Generar rutas optimizadas.
Visualizar rutas generadas.
Consultar incidencias.
Confirmar rutas.

## Conductor
Consultar ruta asignada.
Visualizar secuencia de entregas.
Consultar información de cada entrega.
Actualizar estado de entrega.
Registrar incidencia de entrega.

## Gerente
Visualizar indicadores logísticos.
Consultar rutas.
Consultar distancia recorrida.
Consultar tiempos estimados.
Consultar utilización de vehículos.
Consultar emisiones estimadas.
Visualizar reportes.

---

# Funcionalidades
| Funcionalidad | Estado |
|--------------|--------|
| Autenticación y autorización | Requerido |
| Gestión de usuarios | Requerido |
| Gestión de vehículos | Requerido |
| Gestión de conductores | Requerido |
| Gestión de pedidos | Requerido |
| Gestión de entregas | Requerido |
| Gestión de zonas | Requerido |
| Optimización de rutas | Requerido |
| Asignación de vehículos | Requerido |
| Visualización de rutas | Requerido |
| Seguimiento de entregas | Requerido |
| Indicadores logísticos | Requerido |
| Indicadores de sostenibilidad | Requerido |
| Reporte de incidencias | Requerido |
| Exportación de reportes | Deseado |
| Historial de rutas | Deseado |

---

# API (Resumen)

## Autenticación
POST /api/auth/login
POST /api/auth/register
POST /api/auth/refresh

## Usuarios
GET /api/usuarios
POST /api/usuarios
PUT /api/usuarios/{id}
DELETE /api/usuarios/{id}

## Vehículos
GET /api/vehiculos
POST /api/vehiculos
GET /api/vehiculos/{id}
PUT /api/vehiculos/{id}
DELETE /api/vehiculos/{id}

## Conductores
GET /api/conductores
POST /api/conductores
GET /api/conductores/{id}
PUT /api/conductores/{id}
DELETE /api/conductores/{id}

## Pedidos
GET /api/pedidos
POST /api/pedidos
GET /api/pedidos/{id}
PUT /api/pedidos/{id}
DELETE /api/pedidos/{id}

## Entregas
GET /api/entregas
POST /api/entregas
GET /api/entregas/{id}
PUT /api/entregas/{id}

## Rutas
POST /api/rutas/optimizar
GET /api/rutas
GET /api/rutas/{id}
PUT /api/rutas/{id}/confirmar
GET /api/rutas/{id}/entregas

## Indicadores
GET /api/indicadores
GET /api/indicadores/sostenibilidad
GET /api/indicadores/logisticos

## Incidencias
GET /api/incidencias
POST /api/incidencias
PUT /api/incidencias/{id}

---

# Modelo de Datos (Alto Nivel)
Tablas principales:
usuarios
roles
vehiculos
conductores
pedidos
entregas
rutas
ruta_entregas
zonas
incidencias
indicadores
Relaciones principales:
usuario → rol
conductor → vehículo
pedido → entrega
ruta → vehículo
ruta → conductor
ruta → entregas
entrega → pedido
entrega → zona
ruta → incidencias
ruta → indicadores

---

# Requisitos de Interfaz (UI)
Diseño responsive utilizando Tailwind CSS.
Dashboard según rol.
Gestión mediante tablas y formularios.
Formulario de registro de pedidos.
Gestión de vehículos.
Vista de rutas optimizadas.
Visualización de rutas mediante mapa.
Visualización de entregas.
Indicadores logísticos.
Indicadores de sostenibilidad.
Visualización de incidencias.
Estados de carga y error.
Validación de formularios.

---

# Requisitos No Funcionales
Tiempo de generación de rutas ≤ 50 segundos para el escenario definido del PMV.
Soporte inicial para al menos:
- 50 pedidos.
- 10 vehículos.
- 10 conductores.
- 20 zonas de distribución.
Autenticación mediante JWT con expiración de 8 horas cuando se implemente.
Seguridad basada en OWASP Top 10.
Validación de datos mediante Pydantic.
Arquitectura modular.
Separación Frontend / Backend.
API RESTful.
Documentación automática mediante Swagger/OpenAPI.
Diseño responsive.
Cobertura de pruebas ≥ 70%.
Módulos críticos con cobertura ≥ 70%.
Módulos de validación con cobertura ≥ 80%.

---

# Criterios de Optimización

La generación de rutas deberá considerar una función de optimización basada en criterios logísticos y ambientales.
Los principales criterios serán:
Minimizar distancia recorrida.
Minimizar tiempo de recorrido.
Minimizar emisiones estimadas de CO₂.
Maximizar utilización de capacidad vehicular.
Priorizar entregas según prioridad.
Reducir tiempos muertos.
El sistema podrá utilizar una función de puntuación para comparar las soluciones generadas.

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
Los usuarios pueden autenticarse correctamente.
Los roles tienen acceso únicamente a las funciones correspondientes.
Los vehículos pueden registrarse y gestionarse.
Los pedidos pueden registrarse correctamente.
Las entregas pueden ser asociadas a pedidos.
El sistema puede generar una ruta optimizada.
La capacidad de los vehículos es respetada.
Las rutas generadas pueden visualizarse.
Las entregas pueden consultarse por ruta.
Los indicadores logísticos pueden visualizarse.
Los indicadores de sostenibilidad pueden visualizarse.
Los conflictos o incidencias son identificados.
Las pruebas automatizadas se ejecutan correctamente.
La cobertura global alcanza como mínimo el 70%.

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