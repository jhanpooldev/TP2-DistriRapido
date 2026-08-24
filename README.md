# 🚚 EcoLogística Lima - Optimizador de Rutas Sostenibles para DistriRápido S.A.C.

## 📌 Tabla de Contenidos (TOC)

1. [Equipo de Desarrollo](#-equipo-de-desarrollo)
2. [Descripción del Proyecto](#-descripción-del-proyecto)
3. [Contexto del Problema](#-contexto-del-problema)
4. [Objetivos del Proyecto](#-objetivos-del-proyecto)
5. [Análisis del Negocio](#-análisis-del-negocio)
6. [Stakeholders Involucrados](#-stakeholders-involucrados)
7. [Indicadores Clave de Éxito (KPIs)](#-indicadores-clave-de-éxito-kpis)
8. [Funcionalidades Principales](#-funcionalidades-principales)
9. [Arquitectura del Sistema](#-arquitectura-del-sistema)
10. [Estructura del Proyecto](#-estructura-del-proyecto)
11. [Tecnologías Utilizadas](#-tecnologías-utilizadas)
12. [Instalación y Puesta en Marcha](#-instalación-y-puesta-en-marcha)
13. [Variables de Entorno](#-variables-de-entorno)
14. [Ejecución de Pruebas](#-ejecución-de-pruebas)
15. [Estándares y Buenas Prácticas Aplicadas](#-estándares-y-buenas-prácticas-aplicadas)
16. [Metodología de Desarrollo](#-metodología-de-desarrollo)
17. [Documentación del Proyecto](#-documentación-del-proyecto)
18. [Video Explicativo](#-video-explicativo)
19. [Licencia](#-licencia)

---

## 👥 Equipo de Desarrollo

| Nombre | Rol |
| :--- | :--- |
| Nombre del integrante 1 | Backend Developer |
| Nombre del integrante 2 | Frontend Developer |
| Nombre del integrante 3 | QA / Testing |
| Nombre del integrante 4 | Datos / Documentación |

> **Nota:** Reemplazar los nombres y roles por los integrantes reales del equipo.

---

## 🧠 Descripción del Proyecto

**EcoLogística Lima** es un sistema web desarrollado para **DistriRápido S.A.C.**, orientado a la optimización de rutas de distribución urbana mediante criterios de eficiencia operativa y sostenibilidad.

El sistema busca generar rutas de distribución más eficientes considerando información relacionada con vehículos, entregas, distancias, tiempos, capacidad de carga y restricciones operativas.

El proyecto será desarrollado como un **Producto Mínimo Viable (PMV)** durante un periodo académico de **12 semanas**, aplicando principios de desarrollo incremental, Scrum, Git Flow, pruebas automatizadas y buenas prácticas de ingeniería de software.

La solución permitirá centralizar información logística y proporcionar una herramienta que facilite la planificación y toma de decisiones relacionadas con las rutas de distribución.

---

## 🌎 Contexto del Problema

La distribución urbana de productos requiere coordinar múltiples variables, como vehículos disponibles, pedidos, ubicaciones de entrega, capacidad de carga, tiempos de atención y distancias entre puntos.

Una planificación manual o poco optimizada puede ocasionar:

- Rutas excesivamente largas.
- Incremento del consumo de combustible.
- Mayor tiempo de distribución.
- Recorridos innecesarios.
- Uso ineficiente de vehículos.
- Retrasos en las entregas.
- Incremento de costos operativos.
- Mayor generación de emisiones contaminantes.
- Dificultad para comparar diferentes alternativas de rutas.

Este problema adquiere mayor complejidad en entornos urbanos como Lima, donde las condiciones de distribución pueden variar considerablemente.

Por ello, **EcoLogística Lima** propone utilizar herramientas computacionales para apoyar la planificación y optimización de rutas de distribución.

---

## 🎯 Objetivos del Proyecto

### Objetivo General

Desarrollar un sistema web capaz de generar y gestionar rutas de distribución optimizadas para **DistriRápido S.A.C.**, considerando restricciones operativas y criterios de eficiencia y sostenibilidad.

### Objetivos Específicos

- Optimizar las rutas utilizadas para las entregas.
- Reducir distancias recorridas innecesariamente.
- Disminuir los tiempos estimados de distribución.
- Mejorar la utilización de los vehículos disponibles.
- Considerar la capacidad de carga de los vehículos.
- Facilitar la planificación de entregas.
- Centralizar la información logística.
- Proporcionar información para la toma de decisiones.
- Incorporar criterios relacionados con la sostenibilidad.
- Automatizar parte del proceso de planificación de rutas.

---

## 🏢 Análisis del Negocio

El proceso logístico considerado por el sistema comprende principalmente:

1. Registro de vehículos disponibles.
2. Registro de características y capacidades de los vehículos.
3. Registro de pedidos o entregas.
4. Registro de ubicaciones de destino.
5. Identificación de restricciones operativas.
6. Planificación de las entregas.
7. Generación de rutas.
8. Optimización de las rutas propuestas.
9. Asignación de entregas a vehículos.
10. Visualización de las rutas.
11. Seguimiento de resultados.
12. Generación de información para la toma de decisiones.

El sistema busca proporcionar una herramienta de apoyo para que los responsables de la operación logística puedan seleccionar alternativas de distribución más eficientes.

---

## 👥 Stakeholders Involucrados

| Stakeholder | Rol |
| :--- | :--- |
| Administrador | Gestiona usuarios, vehículos y configuración del sistema |
| Responsable Logístico | Planifica y optimiza las rutas |
| Conductores | Ejecutan las rutas asignadas |
| Personal de Distribución | Gestiona pedidos y entregas |
| Empresa DistriRápido S.A.C. | Utiliza la solución para mejorar su operación logística |
| Cliente | Recibe los productos mediante las rutas planificadas |
| Sistema | Procesa información y genera alternativas de rutas |

---

## 📈 Indicadores Clave de Éxito (KPIs)

| KPI | Objetivo |
| :--- | :--- |
| Reducción de distancia recorrida | ≥ 15% |
| Reducción del tiempo estimado de distribución | ≥ 10% |
| Utilización de vehículos | ≥ 80% |
| Rutas válidas generadas | ≥ 95% |
| Reducción de recorridos innecesarios | ≥ 15% |
| Tiempo de generación de una ruta | ≤ 60 segundos |
| Cobertura de pruebas automatizadas | ≥ 70% |

> Los valores de los KPIs podrán ser ajustados durante la etapa de planificación y validación del PMV.

---

## 🚀 Funcionalidades Principales

### 🔹 Gestión de Usuarios

- Registro y gestión de usuarios.
- Autenticación.
- Control de acceso.
- Gestión de roles.

### 🔹 Gestión de Vehículos

- Registro de vehículos.
- Actualización de información.
- Capacidad de carga.
- Tipo de vehículo.
- Estado de disponibilidad.
- Consulta de vehículos disponibles.

### 🔹 Gestión de Entregas

- Registro de pedidos.
- Registro de destinos.
- Ubicación de entregas.
- Peso o volumen de carga.
- Estado de las entregas.
- Gestión de prioridades.

### 🔹 Optimización de Rutas

- Generación automática de rutas.
- Asignación de entregas a vehículos.
- Consideración de restricciones.
- Optimización de distancia.
- Optimización del tiempo de recorrido.
- Comparación de alternativas.
- Identificación de rutas no válidas.

### 🔹 Criterios de Sostenibilidad

- Estimación de distancia recorrida.
- Estimación de consumo de combustible.
- Estimación de emisiones.
- Comparación entre rutas.
- Indicadores de eficiencia ambiental.

### 🔹 Visualización

- Visualización de rutas.
- Información de vehículos.
- Información de entregas.
- Estado de las rutas.
- Indicadores logísticos.
- Panel de control.

### 🔹 Reportes

- Reportes de rutas.
- Distancias recorridas.
- Tiempo estimado.
- Uso de vehículos.
- Indicadores de sostenibilidad.
- Resultados de optimización.

---

## 🏛 Arquitectura del Sistema

El sistema utilizará una arquitectura con separación clara entre **Frontend, Backend y Base de Datos**.

### Frontend SPA

Aplicación desarrollada con **React + Vite**, responsable de:

- Interfaz de usuario.
- Navegación.
- Formularios.
- Visualización de información.
- Consumo de APIs.
- Gestión de estados.
- Visualización de rutas y resultados.

### Backend API REST

Aplicación desarrollada con **FastAPI**, responsable de:

- Lógica de negocio.
- Validación de información.
- Gestión de usuarios.
- Gestión de vehículos.
- Gestión de entregas.
- Procesamiento de rutas.
- Optimización.
- Seguridad.
- Exposición de APIs.

### Base de Datos

Se utilizará una base de datos relacional administrada mediante **SQLAlchemy ORM**.

La base de datos será responsable de:

- Persistencia de usuarios.
- Persistencia de vehículos.
- Persistencia de entregas.
- Persistencia de rutas.
- Persistencia de resultados.
- Relaciones entre entidades.
- Integridad de la información.

### Comunicación

La comunicación entre Frontend y Backend se realizará mediante APIs REST utilizando HTTP/HTTPS.

---

## 📁 Estructura del Proyecto

```text
ecologistica-lima/
│
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── config/
│   │   │   ├── security/
│   │   │   └── dependencies/
│   │   │
│   │   ├── middleware/
│   │   │
│   │   ├── models/
│   │   │
│   │   ├── schemas/
│   │   │
│   │   ├── repositories/
│   │   │
│   │   ├── services/
│   │   │
│   │   ├── routers/
│   │   │
│   │   └── main.py
│   │
│   ├── tests/
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── features/
│   │   ├── pages/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── hooks/
│   │   ├── context/
│   │   └── main.jsx
│   │
│   ├── tests/
│   ├── package.json
│   └── vite.config.js
│
├── docs/
│   ├── inicio/
│   ├── planificacion/
│   ├── ejecucion/
│   ├── seguimiento_control/
│   ├── cierre/
│   └── otros/
│
├── tests/
│
├── docker/
│
├── README.md
├── SPECS.md
├── CONSTITUTION.md
├── CHANGELOG.md
├── .gitignore
└── .env.example