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


## Descripcion del Proyecto

Este proyecto consiste en el desarrollo de un sistema web inteligente orientado a la optimizacion de rutas de reparto sostenibles para la empresa DistriRapido S.A.C. en la ciudad de Lima, considerando restricciones de trafico, capacidad de vehiculos, horarios de entrega y optimizacion de recursos logisticos.

El sistema busca reducir costos operativos, minimizar el impacto ambiental y mejorar la eficiencia en la distribucion de productos mediante tecnicas de optimizacion combinatoria (TSP - Problema del Viajero y VRP - Problema de Rutas de Vehiculos).

---

## Contexto del Problema

La distribucion de productos en la ciudad de Lima presenta multiples desafios debido a:

- Alto trafico vehicular en horas punta
- Rutas ineficientes que generan sobrecostos operativos
- Emisiones de CO2 elevadas por recorridos innecesarios
- Tiempos de entrega prolongados
- Dificultad para gestionar flotas de vehiculos
- Falta de visibilidad en tiempo real de las operaciones

Actualmente, gran parte del proceso se realiza manualmente o mediante herramientas limitadas, ocasionando:

- Rutas no optimizadas
- Aumento de costos operativos
- Insatisfaccion del cliente
- Impacto ambiental negativo
- Baja eficiencia en la distribucion

DistriRapido S.A.C. enfrenta problemas de rentabilidad y sostenibilidad debido a la ineficiencia en la planificacion de rutas de reparto, lo que afecta su competitividad en el mercado.

El problema pertenece al proceso logistico de distribucion y corresponde a un problema de optimizacion combinatoria NP-Hard de alta complejidad computacional (TSP y VRP).

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
- Facilitar la validacion operativa de rutas

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
- Gestion completa de datos mediante operaciones CRUD

### Gestion de Flota
- Registro de vehiculos y conductores
- Asignacion de vehiculos a rutas
- Gestion de disponibilidad de flota
- Control de capacidad de carga

### Optimizacion de Rutas
- Motor basado en algoritmos de optimizacion (TSP/VRP)
- Generacion automatica de rutas optimizadas
- Consideracion de restricciones (trafico, horarios, capacidad)
- Minimizacion de distancias y tiempos

### Visualizacion y Seguimiento
- Mapa interactivo con rutas generadas
- Seguimiento en tiempo real de entregas
- Dashboard con metricas clave
- Filtros por conductor, vehiculo y zona

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
├── backend/
│ ├── app/
│ │ ├── core/ # Configuracion, seguridad y dependencias
│ │ ├── middleware/ # Middlewares personalizados
│ │ └── modules/
│ │ ├── auth/ # Autenticacion y tokens JWT
│ │ ├── pedidos/ # Gestion de pedidos de clientes
│ │ ├── flota/ # Gestion de vehiculos y conductores
│ │ ├── rutas/ # Optimizacion de rutas (TSP/VRP)
│ │ └── monitoreo/ # Seguimiento en tiempo real
│ ├── requirements.txt
│ └── .env
├── docs/
│ ├── inicio/
│ ├── planificacion/
│ ├── ejecucion/
│ ├── seguimiento_control/
│ ├── cierre/
│ └── otros/
├── frontend/
│ ├── src/
│ │ ├── components/ # Componentes reutilizables
│ │ ├── pages/ # Paginas organizadas por rol
│ │ ├── routes/ # Definicion de rutas
│ │ └── context/ # Estado global con Context API
│ ├── test/ # Pruebas unitarias y de integracion
│ ├── package.json
│ └── vite.config.js
├── tests/ # Pruebas automatizadas
├── .env.example
├── .gitignore
├── README.md
├── CONSTITUTION.md
└── AGENT.md

## Tecnologias Utilizadas

| Capa | Tecnologia |
| :--- | :--- |
| Frontend | React + Vite |
| Estilos | Tailwind CSS |
| Backend | FastAPI (Python) |
| ORM | SQLAlchemy + Alembic |
| Base de datos | PostgreSQL |
| Autenticacion | JWT (PyJWT + bcrypt) |
| Optimizacion | OR-Tools / Google Maps API |
| Pruebas Backend | pytest + pytest-cov |
| Pruebas Frontend | Vitest + Cypress |
| Control de versiones | Git + GitHub |

---

## Instalacion y Puesta en Marcha

### Requisitos previos

- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- Git

### 1. Clonar el repositorio

`ash
git clone https://github.com/jhanpooldev/TP2-DistriRapido.git
cd TP2-DistriRapido
2. Configurar el Backend
bash
cd backend

# Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

# Instalar dependencias
pip install -r requirements.txt

# Copiar y configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales (ver seccion Variables de Entorno)

# Ejecutar migraciones
alembic upgrade head

# Iniciar el servidor de desarrollo
uvicorn app.main:app --reload
El backend estara disponible en http://localhost:8000.
La documentacion interactiva de la API (Swagger) se encuentra en http://localhost:8000/docs.

3. Configurar el Frontend
bash
cd frontend

# Instalar dependencias
npm install

# Iniciar el servidor de desarrollo
npm run dev
El frontend estara disponible en http://localhost:5173.

Variables de Entorno
Copia el archivo .env.example ubicado en backend/ y renombralo como .env. Las variables requeridas son:

VariableDescripcionEjemplo
DB_HOSTHost de la base de datoslocalhost
DB_PORTPuerto de PostgreSQL5432
DB_NAMENombre de la base de datosdistrirapido
DB_USERUsuario de PostgreSQLpostgres
DB_PASSWORDContraseña de PostgreSQLtu_password
JWT_SECRETClave secreta para firmar tokens JWTclave_segura_aleatoria
JWT_ALGORITHMAlgoritmo de firma JWTHS256
JWT_EXPIRE_HOURSDuracion del token en horas8
GOOGLE_MAPS_API_KEYAPI Key para Google Mapstu_api_key
Nunca incluyas el archivo .env en el repositorio. Esta excluido por .gitignore.

Ejecucion de Pruebas
Backend (pytest)
bash
cd backend
source venv/bin/activate

# Ejecutar todas las pruebas
pytest

# Con reporte de cobertura
pytest --cov=app --cov-report=term-missing
Frontend (Vitest)
bash
cd frontend

# Ejecutar pruebas
npm run test

# Con reporte de cobertura
npm run test:cobertura

# Modo TDD (watch)
npm run test:tdd
Frontend (Cypress - E2E)
bash
cd frontend

# Modo interactivo
npm run test:cypress:open

# Modo headless (CI)
npm run test:cypress:run
Objetivo de cobertura: Total >= 70% · Modulo de validacion >= 80%

Estandares y Buenas Practicas Aplicadas
EstandarAplicacion
ISO/IEC 25010Calidad del software
OWASP Top 10Seguridad
WCAG 2.1 AAAccesibilidad
Git FlowControl de versiones
ScrumGestion agil
TDDCalidad y testing
Metodologia de Desarrollo
El proyecto utiliza:

Scrum — Desarrollo iterativo con sprints cortos

Git Flow — Ramas main, develop, feature/* y release/*

TDD — Ciclo Red -> Green -> Refactor

Conventional Commits — Mensajes de commit estandarizados (feat:, fix:, docs:, etc.)

Desarrollo incremental basado en MVP

Licencia
Proyecto desarrollado con fines academicos para el curso Taller de Proyectos 2 – Ingenieria de Sistemas e Informatica.

Enlaces
Repositorio: https://github.com/jhanpooldev/TP2-DistriRapido

Documentacion: /docs/

Video explicativo: [Enlace pendiente]
