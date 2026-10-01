# Sistema Web de Optimizacion de Rutas Sostenibles - EcoLogistica Lima

## Tabla de Contenidos (TOC)

1. [Descripcion del Proyecto](#descripcion-del-proyecto)
2. [Contexto del Problema](#contexto-del-problema)
3. [Objetivos del Proyecto](#objetivos-del-proyecto)
4. [Analisis del Negocio](#analisis-del-negocio)
5. [Stakeholders Involucrados](#stakeholders-involucrados)
6. [Indicadores Clave de Exito (KPIs)](#indicadores-clave-de-exito-kpis)
7. [Funcionalidades Principales](#funcionalidades-principales)
8. [Arquitectura del Sistema](#arquitectura-del-sistema)
9. [Estructura del Proyecto](#estructura-del-proyecto)
10. [Tecnologias Utilizadas](#tecnologias-utilizadas)
11. [Instalacion y Puesta en Marcha](#instalacion-y-puesta-en-marcha)
12. [Variables de Entorno](#variables-de-entorno)
13. [Ejecucion de Pruebas](#ejecucion-de-pruebas)
14. [Estandares y Buenas Practicas Aplicadas](#estandares-y-buenas-practicas-aplicadas)
15. [Metodologia de Desarrollo](#metodologia-de-desarrollo)
16. [Documentacion del Proyecto](#documentacion-del-proyecto)
17. [Integrantes del Equipo](#integrantes-del-equipo)
18. [Licencia](#licencia)

---


## Descripcion del Proyecto

Este proyecto consiste en el desarrollo de un sistema web inteligente orientado a la optimizacion de rutas de reparto sostenibles para la empresa DistriRápido S.A.C. en la ciudad de Lima, considerando la capacidad de los vehiculos y criterios de optimizacion de recursos logisticos.

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

Desarrollar un sistema web capaz de generar rutas de reparto optimizadas y sostenibles para DistriRápido S.A.C., reduciendo costos operativos y el impacto ambiental.

### Objetivos Especificos

- Optimizar las rutas de reparto minimizando distancias y tiempos
- Reducir el consumo de combustible y emisiones de CO2
- Registrar y validar los puntos de entrega de cada reparto
- Gestionar los parametros de calculo de los vehiculos de la flota
- Visualizar las rutas generadas sobre un mapa interactivo
- Automatizar la planificacion de rutas de distribucion
- Facilitar la validacion operativa y la estimacion del ahorro obtenido

Los objetivos de seguimiento en tiempo real y de gestion avanzada de flota quedan
identificados como trabajo futuro (ver "Documentacion del Proyecto").

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

El Producto Minimo Viable (PMV) cubre los pasos **1, 2, 4, 5 y 8**. La gestion
detallada de conductores (paso 3), el seguimiento en tiempo real (paso 7) y el
monitoreo GPS quedan fuera del alcance del PMV (ver `SPECS.md`).

---

## Stakeholders Involucrados

| Stakeholder | Rol |
| :--- | :--- |
| Clientes | Reciben productos en sus domicilios |
| Conductores | Realizan las entregas en campo |
| Administrador del Sistema | Gestiona usuarios, roles y parametros de la operacion |
| Operador Logístico | Registra puntos de entrega y genera rutas |
| Gerencia de Operaciones | Consulta indicadores y supervise el proceso logistico |
| Sistema | Genera rutas optimizadas automaticamente |

---

## Indicadores Clave de Exito (KPIs)

Metas verificables del PMV, alineadas con la Declaracion de la Vision
(`docs/inicio/03. Declaracion de la vision`) y validadas con los casos de prueba
del proyecto.

| KPI | Objetivo del PMV |
| :--- | :--- |
| Reduccion de la distancia total por ruta | >= 15% frente a la ruta no optimizada |
| Reduccion de emisiones estimadas de CO2 | >= 10% frente a la ruta no optimizada |
| Tiempo de generacion de una ruta (hasta 20 puntos) | <= 5 segundos (P95) |
| Flujo principal de generacion de ruta | <= 3 pasos y <= 3 minutos |
| Operador logistico con flujo funcional de punta a punta | >= 90% de los casos de prueba |
| Cobertura de pruebas automatizadas | >= 70% global, >= 80% en validacion |

Las expectativas operativas mas ambiciosas del negocio (25% menos kilometraje,
20% menos combustible, 95% de entregas a tiempo) se consideran metas
post-PMV y no se comprometen para la version `v1.0.0`.

---

## Funcionalidades Principales

### Gestion de Puntos de Entrega
- Registro de puntos de entrega con direccion o coordenadas
- Validacion de ubicaciones y del peso del paquete
- Modificacion y eliminacion de puntos no confirmados
- Gestion completa de datos mediante operaciones CRUD

### Gestion de Flota
- Parametros de calculo por vehiculo (capacidad, consumo, emision, velocidad)
- Asignacion de vehiculos a rutas
- Control de capacidad de carga

### Optimizacion de Rutas
- Motor propio de optimizacion (Haversine + Vecino Mas Cercano + 2-opt)
- Generacion automatica de rutas optimizadas
- Consideracion de restricciones (capacidad, centro de distribucion)
- Minimizacion de distancias y tiempos
- Calculo de emisiones de CO2 estimado

### Indicadores y Visualizacion
- Mapa interactivo con rutas generadas
- Comparacion lado a lado de la ruta optimizada y la no optimizada
- Dashboard con metricas clave
- Filtros por fecha, estado y vehiculo

### Seguridad
- Autenticacion JWT con expiracion de 8 horas
- Control de acceso basado en roles (Administrador, Operador Logistico, Gerente)
- Contrasenas almacenadas con hash bcrypt irreversible
- Bloqueo por intentos fallidos y control de acceso por rol

---

## Arquitectura del Sistema

El sistema sigue una arquitectura de tres capas con separacion clara de responsabilidades:

- **Frontend SPA** — Aplicacion React con enrutamiento del lado del cliente, organizada por modulos segun el rol del usuario (administrador, operador, gerente).
- **Backend API REST** — FastAPI con patron Service Layer, endpoints asincronos y validacion de entrada mediante Pydantic.
- **Base de datos relacional** — PostgreSQL gestionado mediante SQLAlchemy ORM con migraciones Alembic.
- **Autenticacion** — JWT gestionado en el backend; el frontend almacena el token y lo adjunta en cada peticion.
- **Motor de Optimizacion** — Heuristica propia en Python (Haversine + Vecino Mas Cercano + 2-opt). El acceso a servicios externos de mapas se encapsula detras de un adaptador de integracion.

La comunicacion entre frontend y backend se realiza a traves de HTTP/REST. El CORS esta configurado para aceptar peticiones desde el frontend.

El detalle de la arquitectura por niveles (C4) se encuentra en `docs/inicio/12. Modelo C4`.

---

## Estructura del Proyecto

```text
/
|-- .env                         # Configuracion local (NO versionado)
|-- .env.example                # Plantilla de variables de entorno
|-- .gitignore                  # Excluye node_modules, venv, .env, etc.
|-- AGENT.md                    # Estandares de codificacion
|-- CHANGELOG.md                # Historial de cambios
|-- CONSTITUTION.md             # Decisiones arquitecturales del proyecto
|-- README.md
|-- SPECS.md                    # Especificacion tecnica
|-- docs/
|   |-- inicio/                 # 13 documentos de la fase de Inicio
|   `-- planificacion/          # Backlog, Jira, riesgos, presupuesto
`-- src/
    |-- backend/                # FastAPI (Python)
    |   |-- app/
    |   |   |-- main.py             # Aplicacion, CORS, manejador de errores
    |   |   |-- core/               # Configuracion, seguridad, conexion a BD
    |   |   |-- models/             # Modelos SQLAlchemy (ORM)
    |   |   |-- schemas/            # Modelos Pydantic de entrada y salida
    |   |   |-- api/v1/endpoints/   # Controladores (rutas de la API)
    |   |   |-- services/           # Logica de negocio (incluye optimizer/)
    |   |   |-- repositories/       # Acceso a datos
    |   |   `-- integrations/       # Adaptadores de servicios externos
    |   |-- alembic/               # Migraciones
    |   |-- tests/                 # Pruebas pytest
    |   `-- requirements.txt
    `-- frontend/               # React + Vite
        |-- src/
        |   |-- api/                 # Cliente HTTP (axios)
        |   |-- context/             # Estado global (Context API)
        |   |-- components/          # Componentes UI reutilizables
        |   |-- features/            # Modulos por funcionalidad
        |   |-- pages/               # Paginas
        |   |-- routes/              # Definicion de rutas
        |   `-- styles/              # Tailwind CSS
        |-- package.json
        `-- vite.config.js
```

El archivo `.env` vive en la **raíz del repositorio** y el backend lo carga desde
allí; el frontend lo lee mediante `envDir` en Vite. Nunca se versiona.

Las pruebas automatizadas residen dentro de cada aplicacion: `src/backend/tests`
para el backend y archivos `*.test.jsx` junto al codigo del frontend.

---

## Tecnologias Utilizadas

| Capa | Tecnologia |
| :--- | :--- |
| Frontend | React + Vite |
| Estilos | Tailwind CSS |
| Backend | FastAPI (Python) |
| ORM | SQLAlchemy + Alembic |
| Base de datos | PostgreSQL |
| Autenticacion | JWT (PyJWT + bcrypt) |
| Optimizacion | Heuristica propia en Python (Haversine + NN + 2-opt) |
| Pruebas Backend | pytest + pytest-cov |
| Pruebas Frontend | Vitest + Testing Library |
| Calidad de codigo | Ruff (Python) · ESLint + Prettier (JavaScript) |
| Integracion continua | GitHub Actions |
| Control de versiones | Git + GitHub |

---

## Instalacion y Puesta en Marcha

### Requisitos previos

- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- Git

### 1. Clonar el repositorio

```bash
git clone https://github.com/jhanpooldev/TP2-DistriRapido.git
cd TP2-DistriRapido
```

### 2. Configurar el Backend

```bash
cd src/backend

# Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

# Instalar dependencias
pip install -r requirements.txt

# Copiar y configurar variables de entorno
cp .env.example ../../.env      # Linux / macOS
copy ..\..\.env.example ..\..\.env   # Windows

# Editar .env con las credenciales de PostgreSQL (ver seccion Variables de Entorno)

# Crear la base de datos (una sola vez)
createdb distrirapido
createdb distrirapido_test

# Ejecutar migraciones
alembic upgrade head

# Iniciar el servidor de desarrollo
uvicorn app.main:app --reload
```

El backend estara disponible en `http://localhost:8000`.
La documentacion interactiva de la API (Swagger) se encuentra en `http://localhost:8000/docs`.

### 3. Configurar el Frontend

```bash
cd src/frontend

# Instalar dependencias
npm install

# Iniciar el servidor de desarrollo
npm run dev
```

El frontend estara disponible en `http://localhost:5173`.

---

## Variables de Entorno

Copia el archivo `.env.example` ubicado en la raiz del proyecto y renombralo como `.env`. Ese archivo queda en la raiz y es el unico lugar donde se configura el backend y el frontend. Las variables requeridas son:

| Variable | Descripcion | Ejemplo |
| :--- | :--- | :--- |
| `DB_HOST` | Host de la base de datos | `localhost` |
| `DB_PORT` | Puerto de PostgreSQL | `5432` |
| `DB_NAME` | Nombre de la base de datos de trabajo | `distrirapido` |
| `DB_NAME_TEST` | Base de datos usada solo por las pruebas | `distrirapido_test` |
| `DB_USER` | Usuario de PostgreSQL | `postgres` |
| `DB_PASSWORD` | Contraseña de PostgreSQL | `tu_password` |
| `JWT_SECRET` | Clave secreta para firmar tokens JWT | `clave_segura_aleatoria` |
| `JWT_ALGORITHM` | Algoritmo de firma JWT | `HS256` |
| `JWT_EXPIRE_HOURS` | Duracion del token en horas | `8` |
| `HOME_ADDRESS` | Direccion del centro de distribucion | `Av. Javier Prado Este 4200, Lima` |
| `HOME_LAT` | Latitud del centro de distribucion | `-12.1150000` |
| `HOME_LNG` | Longitud del centro de distribucion | `-76.9700000` |
| `MAP_PROVIDER` | Proveedor de distancias | `haversine` |
| `MAX_PUNTOS_POR_RUTA` | Limite de puntos por ruta | `20` |
| `VITE_API_URL` | URL base del backend (frontend) | `http://localhost:8000` |

Nunca incluyas el archivo `.env` en el repositorio. Esta excluido por `.gitignore`.
La plantilla `.env.example` jamas debe contener credenciales reales.

---

## Ejecucion de Pruebas

### Backend (pytest)

```bash
cd src/backend
source venv/bin/activate          # Windows: venv\Scripts\activate

# Ejecutar todas las pruebas
pytest

# Con reporte de cobertura
pytest --cov=app --cov-report=term-missing
```

Las pruebas de integracion utilizan la base de datos `DB_NAME_TEST`, separada de la
base de datos de trabajo para no destruir datos.

### Frontend (Vitest)

```bash
cd src/frontend

# Ejecutar pruebas
npm run test

# Con reporte de cobertura
npm run test:cobertura

# Modo watch
npm run test:tdd
```

Objetivo de cobertura: Total >= 70% · Modulo de validacion >= 80% · Codigo nuevo o modificado >= 80% (DoD global).

### Lint y formato

```bash
# Backend
cd src/backend
ruff check .
ruff format .

# Frontend
cd src/frontend
npm run lint
npm run format
```

---

## Estandares y Buenas Practicas Aplicadas

| Estandar | Aplicacion |
| :--- | :--- |
| ISO/IEC 25010 | Calidad del software |
| OWASP Top 10 | Seguridad |
| WCAG 2.1 AA | Accesibilidad |
| Git Flow | Control de versiones |
| Scrum | Gestion agil |
| TDD | Calidad y testing |
| Convenciones | Semantic Versioning (SemVer) |

---

## Metodologia de Desarrollo

El proyecto utiliza:

- **Scrum** — Desarrollo iterativo con sprints quincenales
- **Git Flow** — Ramas `main`, `develop`, `feature/*`, `release/*` y `hotfix/*`
- **TDD** — Ciclo Red → Green → Refactor
- **Conventional Commits** — Mensajes de commit estandarizados (`feat:`, `fix:`, `docs:`, etc.)
- **Desarrollo incremental basado en MVP**

El detalle del backlog, los sprints y la Definition of Done se encuentran en
`docs/planificacion/01 Transformando a ágil V_1_0_0.md`.

---

## Documentacion del Proyecto

La documentacion sigue la estructura definida en `CONSTITUTION.md`.

### Fase de Inicio (`docs/inicio/`)

| # | Documento |
| :--- | :--- |
| 01 | Seleccion del enfoque del proyecto |
| 02 | Acta de constitucion del proyecto |
| 03 | Declaracion de la vision |
| 04 | Registro de supuestos y restricciones |
| 05 | Registro de interesados |
| 06 | Requisitos funcionales (RF-001 a RF-014) |
| 07 | Requisitos no funcionales (RNF-001 a RNF-015) |
| 08 | Identificacion y perfiles de usuarios |
| 09 | Reglas de negocio y trazabilidad (RN-001 a RN-020) |
| 10 | Evaluacion e identificacion del stack tecnologico |
| 11 | Diseno e ingenieria de base de datos |
| 12 | Arquitectura de software (modelo C4) |
| 13 | Analisis multidimensional de restricciones |

### Fase de Planificacion (`docs/planificacion/`)

| # | Documento |
| :--- | :--- |
| 01 | Transformando a agil (backlog priorizado y Definition of Done) |
| 02 | Artefactos Jira |
| 03 | Registro de riesgos |
| 04 | Presupuesto del proyecto |

Las carpetas de las fases posteriores (ejecucion, seguimiento y control, cierre)
se crearan en su momento, cuando exista la evidencia que contienen.

---

## Integrantes del Equipo

| # | Apellidos y Nombres | Codigo |
| :--- | :--- | :--- |
| 01 | Cosme Tenorio, Jhunior Harold | 75262183 |
| 02 | Flores Torres, Jhanpool Ernesto | 7843259 |
| 03 | Tucto Ubaldo, Ricardo David | 72120490 |
| 04 | Vega Reyes, Andrew Steven | 72638273 |

El detalle completo de cada integrante (rol, area responsable y datos de
contacto) se registra en
[`docs/inicio/05. Registro de interesados`](docs/inicio/05.%20Registro%20de%20interesados%20V_1_0_0.md).

---

## Licencia

Proyecto desarrollado con fines academicos para el curso Taller de Proyectos 2 — Ingenieria de Sistemas e Informatica.

---

## Enlaces

- **Repositorio:** https://github.com/jhanpooldev/TP2-DistriRapido
- **Documentacion PMBOK:** [`docs/`](docs/)
- **Fase de Inicio:** [`docs/inicio/`](docs/inicio/)
- **Fase de Planificacion:** [`docs/planificacion/`](docs/planificacion/)
- **Especificacion tecnica:** [SPECS.md](SPECS.md)
- **Constitucion del proyecto:** [CONSTITUTION.md](CONSTITUTION.md)
- **Estandares de codificacion:** [AGENT.md](AGENT.md)
- **Historial de cambios:** [CHANGELOG.md](CHANGELOG.md)
- **Video explicativo:** [Enlace pendiente]
