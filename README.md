@"
# Sistema Web de Optimizacion de Rutas Sostenibles - EcoLogistica Lima

## Tabla de Contenidos (TOC)

1. [Equipo de Desarrollo](#equipo-de-desarrollo)
2. [Descripcion del Proyecto](#descripcion-del-proyecto)
3. [Contexto del Problema](#contexto-del-problema)
4. [Objetivos del Proyecto](#objetivos-del-proyecto)
5. [Analisis del Negocio](#analisis-del-negocio)
6. [Stakeholders Involucrados](#stakeholders-involucrados)
7. [Indicadores Clave de Exito (KPIs)](#indicadores-clave-de-exito-kpis)
8. [Funcionalidades Principales](#funcionalidades-principales)
9. [Arquitectura del Sistema](#arquitectura-del-sistema)
10. [Estructura del Proyecto](#estructura-del-proyecto)
11. [Tecnologias Utilizadas](#tecnologias-utilizadas)
12. [Instalacion y Puesta en Marcha](#instalacion-y-puesta-en-marcha)
13. [Variables de Entorno](#variables-de-entorno)
14. [Ejecucion de Pruebas](#ejecucion-de-pruebas)
15. [Estandares y Buenas Practicas Aplicadas](#estandares-y-buenas-practicas-aplicadas)
16. [Metodologia de Desarrollo](#metodologia-de-desarrollo)
17. [Licencia](#licencia)

---

## Equipo de Desarrollo

| Nombre | Rol |
| :--- | :--- |
| Jhanpool | [Rol] |
| [Nombre] | [Rol] |
| [Nombre] | [Rol] |
| [Nombre] | [Rol] |

---

## Descripcion del Proyecto

Este proyecto consiste en el desarrollo de un sistema web inteligente orientado a la optimizacion de rutas de reparto sostenibles para la empresa DistriRapido S.A.C. en la ciudad de Lima.

El sistema busca reducir costos operativos, minimizar el impacto ambiental y mejorar la eficiencia en la distribucion de productos mediante tecnicas de optimizacion de rutas y analisis de datos en tiempo real.

---

## Contexto del Problema

La distribucion de productos en la ciudad de Lima presenta multiples desafios debido a:

- Alto trafico vehicular en horas punta
- Rutas ineficientes que generan sobrecostos operativos
- Emisiones de CO2 elevadas por recorridos innecesarios
- Tiempos de entrega prolongados
- Dificultad para gestionar flotas de vehiculos
- Falta de visibilidad en tiempo real de las operaciones

DistriRapido S.A.C. enfrenta problemas de rentabilidad y sostenibilidad debido a la ineficiencia en la planificacion de rutas de reparto, lo que afecta su competitividad en el mercado.

El problema pertenece al proceso logistico de distribucion y corresponde a un problema de optimizacion combinatoria (Problema del Viajero - TSP y VRP).

---

## Objetivos del Proyecto

### Objetivo General

Desarrollar un sistema web capaz de generar rutas de reparto optimizadas y sostenibles para DistriRapido S.A.C., reduciendo costos operativos y el impacto ambiental.

### Objetivos Especificos

- Optimizar las rutas de reparto minimizando distancias y tiempos
- Reducir el consumo de combustible y emisiones de CO2
- Mejorar los tiempos de entrega de productos
- Gestionar eficientemente la flota de vehiculos
- Proporcionar visibilidad en tiempo real de las operaciones
- Automatizar la planificacion de rutas de distribucion

---

## Analisis del Negocio

El proceso logistico identificado incluye:

1. Recepcion de pedidos de clientes
2. Consolidacion de pedidos por zona geografica
3. Asignacion de vehiculos y conductores
4. Planificacion de rutas de reparto
5. Optimizacion de rutas considerando restricciones
6. Ejecucion de entregas
7. Seguimiento y monitoreo en tiempo real
8. Evaluacion de desempeno y metricas

---

## Stakeholders Involucrados

| Stakeholder | Rol |
| :--- | :--- |
| Clientes | Reciben productos en sus domicilios |
| Conductores | Realizan las entregas en campo |
| Administradores de Flota | Gestionan vehiculos y conductores |
| Gerencia de Operaciones | Supervisa el proceso logistico |
| Sistema | Genera rutas optimizadas automaticamente |

---

## Indicadores Clave de Exito (KPIs)

| KPI | Objetivo |
| :--- | :--- |
| Reduccion de kilometros recorridos | >= 25% |
| Ahorro de combustible | >= 20% |
| Reduccion de emisiones de CO2 | >= 25% |
| Tiempo de entrega promedio | <= 45 minutos |
| Entregas a tiempo | >= 95% |
| Costo operativo reducido | >= 20% |
| Satisfaccion del cliente | >= 85% |

---

## Funcionalidades Principales

### Gestion de Pedidos
- Registro de pedidos de clientes
- Gestion de direcciones y zonas de entrega
- Priorizacion de pedidos urgentes

### Gestion de Flota
- Registro de vehiculos y conductores
- Asignacion de vehiculos a rutas
- Gestion de disponibilidad de flota

### Optimizacion de Rutas
- Motor basado en algoritmos de optimizacion (TSP/VRP)
- Generacion automatica de rutas optimizadas
- Consideracion de restricciones (trafico, horarios, capacidad)

### Visualizacion y Seguimiento
- Mapa interactivo con rutas generadas
- Seguimiento en tiempo real de entregas
- Dashboard con metricas clave

### Seguridad
- Autenticacion JWT con expiracion de 8 horas
- Control de acceso basado en roles (administrador, conductor, cliente)

---

## Arquitectura del Sistema

El sistema sigue una arquitectura de tres capas con separacion clara de responsabilidades:

- **Frontend SPA** — Aplicacion React con enrutamiento del lado del cliente, organizada por modulos segun el rol del usuario (admin, conductor, cliente).
- **Backend API REST** — FastAPI con patron Service Layer, endpoints asincronos y validacion de entrada mediante Pydantic.
- **Base de datos relacional** — PostgreSQL gestionado mediante SQLAlchemy ORM con migraciones Alembic.
- **Autenticacion** — JWT gestionado en el backend; el frontend almacena el token y lo adjunta en cada peticion.
- **Motor de Optimizacion** — Algoritmos de optimizacion implementados en Python para la generacion de rutas.

La comunicacion entre frontend y backend se realiza a traves de HTTP/REST. El CORS esta configurado para aceptar peticiones desde el frontend.

---

## Estructura del Proyecto
