# Sistema Web de Optimización de Rutas Sostenibles — EcoLogística Lima

Optimizador de rutas de reparto sostenible para **DistriRápido S.A.C.**, desarrollado
en el curso Taller de Proyectos 2 — Ingeniería de Sistemas e Informática.

## Tabla de Contenidos (TOC)

1. [Descripción del Proyecto](#descripción-del-proyecto)
2. [Contexto del Problema](#contexto-del-problema)
3. [Objetivos del Proyecto](#objetivos-del-proyecto)
4. [Análisis del Negocio](#análisis-del-negocio)
5. [Stakeholders Involucrados](#stakeholders-involucrados)
6. [Indicadores Clave de Éxito (KPIs)](#indicadores-clave-de-éxito-kpis)
7. [Funcionalidades Principales](#funcionalidades-principales)
8. [Arquitectura del Sistema](#arquitectura-del-sistema)
9. [Estructura del Proyecto](#estructura-del-proyecto)
10. [Tecnologías Utilizadas](#tecnologías-utilizadas)
11. [Instalación y Puesta en Marcha](#instalación-y-puesta-en-marcha)
12. [Variables de Entorno](#variables-de-entorno)
13. [Ejecución de Pruebas](#ejecución-de-pruebas)
14. [Estándares y Buenas Prácticas Aplicadas](#estándares-y-buenas-prácticas-aplicadas)
15. [Metodología de Desarrollo](#metodología-de-desarrollo)
16. [Documentación del Proyecto](#documentación-del-proyecto)
17. [Integrantes del Equipo](#integrantes-del-equipo)
18. [Licencia](#licencia)

---

## Descripción del Proyecto

Este proyecto consiste en el desarrollo de un sistema web orientado a la optimización
de rutas de reparto sostenibles para la empresa DistriRápido S.A.C. en la ciudad de
Lima, considerando la capacidad de los vehículos y criterios de optimización de
recursos logísticos.

El sistema busca reducir costos operativos, minimizar el impacto ambiental y mejorar la
eficiencia en la distribución de productos mediante técnicas de optimización combinatoria
(TSP — Problema del Viajero y VRP — Problema de Rutas de Vehículos).

---

## Contexto del Problema

La distribución de productos en la ciudad de Lima presenta múltiples desafíos:

- Alto tráfico vehicular en horas punta.
- Rutas ineficientes que generan sobrecostos operativos.
- Emisiones de CO₂ elevadas por recorridos innecesarios.
- Tiempos de entrega prolongados.
- Dificultad para gestionar flotas de vehículos.
- Falta de visibilidad en tiempo real de las operaciones.

DistriRápido S.A.C. enfrenta problemas de rentabilidad y sostenibilidad debido a la
ineficiencia en la planificación de rutas de reparto, lo que afecta su competitividad
en el mercado.

El problema pertenece al proceso logístico de distribución y corresponde a un problema
de optimización combinatoria NP-Hard de alta complejidad computacional.

---

## Objetivos del Proyecto

### Objetivo General

Desarrollar un sistema web capaz de generar rutas de reparto optimizadas y sostenibles
para DistriRápido S.A.C., reduciendo costos operativos y el impacto ambiental.

### Objetivos Específicos

- Optimizar las rutas de reparto minimizando distancias y tiempos.
- Reducir el consumo de combustible y las emisiones de CO₂.
- Registrar y validar los puntos de entrega de cada reparto.
- Gestionar los parámetros de cálculo de los vehículos de la flota.
- Visualizar las rutas generadas sobre un mapa interactivo.
- Automatizar la planificación de rutas de distribución.
- Facilitar la validación operativa y la estimación del ahorro obtenido.

El seguimiento en tiempo real y la gestión avanzada de flota quedan identificados como
trabajo futuro.

---

## Análisis del Negocio

El proceso logístico identificado incluye:

1. Recepción de pedidos de clientes.
2. Consolidación de pedidos por zona geográfica.
3. Asignación de vehículos y conductores.
4. Planificación de rutas de reparto.
5. Optimización de rutas considerando restricciones.
6. Ejecución de entregas.
7. Seguimiento y monitoreo en tiempo real.
8. Evaluación de desempeño y métricas.

El Producto Mínimo Viable (PMV) cubre los pasos **1, 2, 4, 5 y 8**. La gestión detallada
de conductores, el seguimiento en tiempo real y el monitoreo GPS quedan fuera del
alcance del PMV (ver `SPECS.md`).

---

## Stakeholders Involucrados

| Stakeholder | Rol |
| :--- | :--- |
| Clientes | Reciben productos en sus domicilios |
| Conductores | Realizan las entregas en campo |
| Administrador del Sistema | Gestiona usuarios, roles y parámetros de la operación |
| Operador Logístico | Registra puntos de entrega y genera rutas |
| Gerencia de Operaciones | Consulta indicadores y supervisa el proceso logístico |
| Sistema | Genera rutas optimizadas automáticamente |

---

## Indicadores Clave de Éxito (KPIs)

| KPI | Objetivo del PMV | Estado de verificación |
| :--- | :--- | :--- |
| Tiempo de generación de una ruta (hasta 20 puntos) | ≤ 5 segundos | **Verificado**: máximo de 20.2 ms medido en `src/backend/tests/test_optimizer.py` |
| Distancia calculada entre coordenadas | Geodésica | **Verificado**: fórmula de Haversine con prueba de distancia conocida |
| Ruta no generable con menos de 2 puntos | Rechazo con mensaje | **Verificado**: la API responde `400` (**RN-010**) |
| Aislamiento de datos por usuario | Un operador no accede a los recursos de otro | **Verificado** en `src/backend/auditoria_api.py` |
| Emisiones estimadas de CO₂ | Según el factor del vehículo asignado | **Verificado** (**RN-017**) |
| Reducción de distancia frente a la ruta no optimizada | ≥ 15 % | **Pendiente**: requiere prueba comparativa de referencia |
| Reducción de emisiones frente a la ruta no optimizada | ≥ 10 % | **Pendiente**: requiere prueba comparativa de referencia |
| Flujo principal de generación de ruta | ≤ 3 pasos y ≤ 3 minutos | **Pendiente**: sin medición formal registrada |
| Cobertura de pruebas automatizadas | ≥ 70 % global | **No verificado**: no hay herramienta de cobertura configurada |

---

## Funcionalidades Principales

### Gestión de Puntos de Entrega

- Registro de puntos de entrega con dirección o coordenadas.
- Geocodificación de direcciones con Nominatim (OpenStreetMap).
- Validación de ubicación y del peso del paquete (**RN-007**, **RN-008**).
- Modificación y eliminación de puntos no confirmados.
- Aislamiento de los puntos por operador autenticado (**RN-001**).

### Gestión de Flota

- Parámetros de cálculo por vehículo: capacidad, consumo, emisión y velocidad.
- Asignación de vehículos a rutas.
- Control de capacidad de carga (**RN-014**).

### Optimización de Rutas

- Motor propio de optimización: Haversine + Vecino Más Cercano + 2-opt.
- Consideración de restricciones: capacidad y centro de distribución.
- Cálculo de distancia total (**RN-015**), tiempo estimado (**RN-016**) y emisiones de
  CO₂ (**RN-017**).
- Límite configurable de puntos por ruta (`MAX_PUNTOS_POR_RUTA`, por defecto 20).

### Indicadores y Visualización

- Mapa interactivo con la ruta generada (Leaflet + OpenStreetMap).
- Selección de coordenadas sobre el mapa al registrar un punto.
- Dashboard con los indicadores calculados.

### Seguridad

Implementado y verificado:

- Autenticación JWT con expiración configurable (8 horas por defecto, **RN-005**).
- Contraseñas almacenadas con hash bcrypt irreversible (**RN-004**).
- Control de acceso basado en roles: Administrador, Operador Logístico y Gerente
  (**RN-003**).
- Validación de firma y caducidad del token en cada petición protegida.

Pendiente:

- Bloqueo por intentos fallidos (**RN-002**): no implementado.
- HTTPS (**RNF-02**): no implementado en la aplicación; corresponde al ambiente de
  despliegue.
- Autenticación multifactor (MFA con TOTP): especificada en
  [`docs/inicio/14. Especificación MFA y Sesiones`](docs/inicio/14.%20Especificacion%20MFA%20y%20Sesiones%20V_1_0_0.md),
  no implementada.

### Limitación conocida del motor de ruteo

Con **exactamente tres puntos**, la búsqueda local 2-opt no se ejecuta: el rango
recorrido queda vacío y la ruta devuelta es la del Vecino Más Cercano sin refinar. Si el
orden en que se envían los puntos resulta mejor que ese, la API puede informar una
`distancia_total_km` levemente mayor que `distancia_sin_optimizar_km`. El ahorro no llega
a ser negativo porque se acota en cero. Con cuatro o más puntos la búsqueda actúa con
normalidad. Registrado como **IMP-10** en el
[`Registro de Impedimentos del Sprint 1`](docs/03%20Implementación/02%20Registro%20de%20Impedimentos%20V_1_0_0.md).

---

## Arquitectura del Sistema

El sistema sigue una arquitectura por capas con separación de responsabilidades:

- **Frontend SPA** — Aplicación React + Vite, organizada por componentes y contexto
  global.
- **Backend API REST** — FastAPI con Service Layer y validación de entrada mediante
  Pydantic.
- **Base de datos relacional** — PostgreSQL gestionado con SQLAlchemy ORM. El esquema
  se crea desde los modelos al iniciar la aplicación (`Base.metadata.create_all`); el
  proyecto **no incluye** gestor de migraciones.
- **Autenticación** — JWT gestionado en el backend; el frontend almacena el token y lo
  adjunta en cada petición.
- **Motor de optimización** — Heurística propia en Python
  (`src/backend/app/services/optimizer/`).

La comunicación entre frontend y backend se realiza por HTTP/REST, con CORS configurado
para el origen del frontend. En desarrollo, Vite redirige `/api` al backend.

El detalle de la arquitectura por niveles (C4) se encuentra en
[`docs/inicio/12. Modelo C4`](docs/inicio/12.%20Modelo%20C4%20V_1_0_0.md).

---

## Estructura del Proyecto

El repositorio cumple las **cinco estructuras requeridas** del PFA:

| # | Estructura | Contenido |
| :--- | :--- | :--- |
| 1 | `docs/` | Documentación (Inicio, Planificación, Implementación) |
| 2 | `src/` | Código fuente (backend y frontend) |
| 3 | `pruebas/` | Pruebas: plan, evidencias e índice de las suites automatizadas |
| 4 | `base de datos/` | Scripts SQL (DDL del esquema) |
| 5 | `modelos/` | Modelamiento (C4, base de datos, reglas de negocio) |

```text
/
|-- .env                          # Configuración local (NO versionado)
|-- .env.example                 # Plantilla de variables de entorno
|-- .gitattributes
|-- .gitignore                   # Excluye venv, node_modules, .env, cachés, etc.
|-- AGENT.md                     # Estándares de codificación
|-- CHANGELOG.md                 # Historial de cambios
|-- CONSTITUTION.md              # Decisiones arquitecturales del proyecto
|-- README.md
|-- SPECS.md                     # Especificación técnica
|
|-- docs/                        # Estructura 1: Documentación
|   |-- inicio/                  # Fase de Inicio (14 documentos)
|   |-- planificacion/           # Backlog, artefactos Jira, riesgos, presupuesto
|   `-- 03 Implementación/       # Entregables por sprint
|       |-- 01 Informe de estado del proyecto V_1_0_0.md
|       |-- 02 Registro de Impedimentos V_1_0_0.md
|       |-- 03 Revisión del Sprint V_1_0_0.md
|       |-- 04 Retrospectiva del Sprint V_1_0_0.md
|       `-- sprint 2/            # Entregables archivados del Sprint 2 (V_2_0_0)
|
|-- src/                         # Estructura 2: Código
|   |-- backend/                 # FastAPI (Python)
|   |   |-- app/
|   |   |   |-- main.py             # Aplicación, CORS, manejador de errores
|   |   |   |-- core/               # Configuración, seguridad, conexión a BD
|   |   |   |-- models/             # Modelos SQLAlchemy (ORM)
|   |   |   |-- schemas/            # Modeles Pydantic de entrada y salida
|   |   |   |-- api/v1/endpoints/   # Controladores (rutas de la API)
|   |   |   `-- services/           # Lógica de negocio (incluye optimizer/)
|   |   |-- tests/                 # Pruebas pytest
|   |   |-- auditoria_api.py        # Auditoría de extremo a extremo de la API
|   |   |-- smoke_sprint2.py        # Verificación de flujo completo
|   |   `-- requirements.txt
|   `-- frontend/                # React + Vite
|       |-- src/
|       |   |-- api/                 # Cliente HTTP (axios)
|       |   |-- context/             # Estado global (Context API)
|       |   |-- components/          # Componentes de interfaz
|       |   |-- pages/               # Páginas
|       |   `-- styles/              # CSS plano
|       |-- package.json
|       `-- vite.config.js
|
|-- pruebas/                    # Estructura 3: Pruebas
|   `-- README.md               # Índice: plan, evidencias y suites automatizadas
|-- base de datos/              # Estructura 4: Scripts SQL
|   |-- esquema.sql             # DDL PostgreSQL (generado de los modelos ORM)
|   `-- README.md               # Índice de contenidos
`-- modelos/                    # Estructura 5: Modelamiento
    `-- README.md               # Índice de modelos (C4, base de datos, RN)
```

El archivo `.env` vive en la **raíz del repositorio** y el backend lo carga desde allí;
el frontend lo lee mediante `envDir` en Vite. Nunca se versiona.

**Pruebas automatizadas:** solo el backend tiene suite de pruebas, en
`src/backend/tests`. El frontend **no incluye pruebas automatizadas**. La estructura
`pruebas/` es el índice y repositorio de evidencias; no duplica la suite.

---

## Tecnologías Utilizadas

| Capa | Tecnología | Versión |
| :--- | :--- | :--- |
| Frontend | React | 18.3.1 |
| Empaquetador | Vite | 5.4.8 |
| Cliente HTTP (frontend) | axios | 1.7.7 |
| Mapas | Leaflet + OpenStreetMap / Nominatim | 1.9.4 |
| Estilos | CSS plano | — |
| Backend | FastAPI | 0.115.6 |
| Servidor ASGI | Uvicorn | 0.34.0 |
| ORM | SQLAlchemy | 2.0.36 |
| Driver de PostgreSQL | psycopg2-binary | 2.9.10 |
| Validación | Pydantic + pydantic-settings | 2.10.4 / 2.7.0 |
| Autenticación | PyJWT + bcrypt | 2.10.1 / 4.2.1 |
| Optimización | Heurística propia (Haversine + NN + 2-opt) | — |
| Base de datos | PostgreSQL | 16 |
| Pruebas backend | pytest | 8.3.4 |
| Control de versiones | Git + GitHub | — |

**No se utilizan:** Tailwind CSS, Alembic, Vitest, Testing Library, Ruff, ESLint,
Prettier ni GitHub Actions.

---

## Instalación y Puesta en Marcha

### Requisitos previos

- Python 3.10 o superior.
- Node.js 18 o superior.
- PostgreSQL 14 o superior, instalado y ejecutándose en el puerto `5432`.
- Git.

### 1. Clonar el repositorio

```bash
git clone https://github.com/jhanpooldev/TP2-DistriRapido.git
cd TP2-DistriRapido
```

### 2. Crear las bases de datos

```bash
createdb -U postgres distrirapido
createdb -U postgres distrirapido_test
```

### 3. Configurar el Backend

```bash
cd src/backend

# Crear y activar el entorno virtual
python -m venv venv
source venv/bin/activate          # Linux / macOS
venv\Scripts\activate             # Windows

# Instalar dependencias
pip install -r requirements.txt

# Copiar la plantilla de variables de entorno a la raíz del repositorio
cp ../../.env.example ../../.env        # Linux / macOS
copy ..\..\.env.example ..\..\.env     # Windows

# Iniciar el servidor de desarrollo
uvicorn app.main:app --reload
```

Las tablas se crean automáticamente al arrancar la aplicación a partir de los modelos
SQLAlchemy. No hay migraciones que ejecutar.

El backend queda disponible en `http://localhost:8000`.
Documentación interactiva de la API (Swagger): `http://localhost:8000/docs`.

### 4. Configurar el Frontend

```bash
cd src/frontend

npm install
npm run dev
```

El frontend queda disponible en `http://localhost:5173`.

> En algunos equipos `localhost` resuelve a `::1` (IPv6) mientras que el proxy de Vite
> escucha en IPv4. Si la interfaz no logra conectar, usa `http://127.0.0.1:5173`.

---

## Variables de Entorno

Copia `.env.example` de la raíz y renómbralo como `.env`. Ese archivo queda en la raíz y
es el único lugar donde se configura el backend y el frontend.

| Variable | Descripción | Ejemplo |
| :--- | :--- | :--- |
| `DB_HOST` | Host de la base de datos | `localhost` |
| `DB_PORT` | Puerto de PostgreSQL | `5432` |
| `DB_NAME` | Base de datos de trabajo | `distrirapido` |
| `DB_NAME_TEST` | Base de datos usada solo por las pruebas | `distrirapido_test` |
| `DB_USER` | Usuario de PostgreSQL | `postgres` |
| `DB_PASSWORD` | Contraseña de PostgreSQL | `cambiar_por_tu_password` |
| `JWT_SECRET` | Clave secreta para firmar tokens JWT | `cambiar_por_una_clave_aleatoria_y_segura` |
| `JWT_ALGORITHM` | Algoritmo de firma JWT | `HS256` |
| `JWT_EXPIRE_HOURS` | Duración del token en horas | `8` |
| `HOME_ADDRESS` | Dirección del centro de distribución | `Av. Javier Prado Este 4200, Surco, Lima` |
| `HOME_LAT` | Latitud del centro de distribución | `-12.1150000` |
| `HOME_LNG` | Longitud del centro de distribución | `-76.9700000` |
| `MAP_PROVIDER` | Proveedor de distancias | `haversine` |
| `MAX_PUNTOS_POR_RUTA` | Límite de puntos por ruta | `20` |
| `VITE_API_URL` | URL base del backend (frontend) | `http://localhost:8000` |

Nunca incluyas el archivo `.env` en el repositorio: está excluido por `.gitignore`. La
plantilla `.env.example` nunca debe contener credenciales reales.

> **Advertencia de seguridad:** `src/backend/app/core/config.py` define un valor por
> defecto para `JWT_SECRET`. Si `.env` no está configurado, la aplicación firmará tokens
> con una clave conocida. Sustituye el valor en `.env` antes de cualquier uso real.

---

## Ejecución de Pruebas

### Backend (pytest)

```bash
cd src/backend
source venv/bin/activate          # Windows: venv\Scripts\activate

pytest
```

Resultado actual: **51 pruebas en verde**. Las pruebas usan la base `DB_NAME_TEST`,
separada de la base de trabajo para no destruir datos.

### Verificación de extremo a extremo

Con el backend en ejecución (en un puerto libre):

```bash
cd src/backend
python auditoria_api.py 8099      # Auditoría de cada endpoint y aislamiento por usuario
python smoke_sprint2.py 8099      # Verificación del flujo completo
```

Ambos scripts terminan sin anomalías y son **herméticos**: crean sus propios datos de
prueba, los eliminan al terminar y dejan la base de datos en el mismo estado en que la
encontraron, por lo que pueden repetirse cuantas veces sea necesario.

> La auditoría cubre el aislamiento entre operadores, la validación de entrada y la
> consignación de las transacciones de escritura. No mide la calidad del resultado del
> algoritmo de ruteo más allá de que la distancia calculada sea coherente con el área
> geográfica de los puntos.

### Frontend

`src/frontend` **no incluye pruebas automatizadas**. La verificación disponible es la
compilación de producción:

```bash
cd src/frontend
npm run build
```

Las pruebas del frontend son una acción pendiente registrada en la Retrospectiva del
Sprint 1 (ACT-S1-05).

### Lint y formato

El proyecto **no tiene configuradas** herramientas de lint ni de formateo.

---

## Estándares y Buenas Prácticas Aplicadas

| Estándar | Aplicación |
| :--- | :--- |
| ISO/IEC 25010 | Calidad del software |
| OWASP Top 10 | Seguridad |
| WCAG 2.1 AA | Accesibilidad |
| Git Flow | Control de versiones |
| Scrum | Gestión ágil |
| Convenciones | Semantic Versioning (SemVer) |

---

## Metodología de Desarrollo

- **Scrum** — Desarrollo iterativo con sprints quincenales.
- **Git Flow** — Ramas `main`, `develop`, `feature/*`, `release/*` y `hotfix/*`.
- **Desarrollo incremental basado en MVP.**
- **Conventional Commits** — Mensajes de commit estandarizados (`feat:`, `fix:`,
  `docs:`, etc.).

El detalle del backlog, los sprints y la Definition of Done se encuentran en
[`docs/planificacion/01 Transformando a ágil`](docs/planificacion/01%20Transformando%20a%20ágil%20V_1_0_0.md).

---

## Documentación del Proyecto

### Fase de Inicio (`docs/inicio/`)

| # | Documento |
| :--- | :--- |
| 01 | Selección del enfoque del proyecto |
| 02 | Acta de constitución del proyecto |
| 03 | Declaración de la visión |
| 04 | Registro de supuestos y restricciones |
| 05 | Registro de interesados |
| 06 | Requisitos funcionales (RF-001 a RF-014) |
| 07 | Requisitos no funcionales (RNF-001 a RNF-015) |
| 08 | Identificación y perfiles de usuarios |
| 09 | Reglas de negocio y trazabilidad (RN-001 a RN-020) |
| 10 | Evaluación e identificación del stack tecnológico |
| 11 | Diseño e ingeniería de base de datos |
| 12 | Arquitectura de software (modelo C4) |
| 13 | Análisis multidimensional de restricciones |
| 14 | Especificación MFA y sesiones (no implementada) |

### Fase de Planificación (`docs/planificacion/`)

| # | Documento |
| :--- | :--- |
| 01 | Transformando a ágil (backlog priorizado y Definition of Done) |
| 02 | Artefactos Jira |
| 03 | Registro de riesgos |
| 04 | Presupuesto del proyecto |

### Fase de Implementación (`docs/03 Implementación/`)

Entregables del **Sprint 1** (US-001, US-003, EN-01, EN-02 — periodo 05/10/2026 al
18/10/2026):

| # | Documento |
| :--- | :--- |
| 01 | [Informe de estado del proyecto V_1_0_0.md](docs/03%20Implementación/01%20Informe%20de%20estado%20del%20proyecto%20V_1_0_0.md) |
| 02 | [Registro de Impedimentos V_1_0_0.md](docs/03%20Implementación/02%20Registro%20de%20Impedimentos%20V_1_0_0.md) |
| 03 | [Revisión del Sprint V_1_0_0.md](docs/03%20Implementación/03%20Revisión%20del%20Sprint%20V_1_0_0.md) |
| 04 | [Retrospectiva del Sprint V_1_0_0.md](docs/03%20Implementación/04%20Retrospectiva%20del%20Sprint%20V_1_0_0.md) |

Entregables del **Sprint 2** (US-002, US-004, US-005, US-007 — periodo 19/10/2026 al
01/11/2026), archivados en [`docs/03 Implementación/sprint 2/`](docs/03%20Implementación/sprint%202/):

| # | Documento |
| :--- | :--- |
| 01 | [Informe de estado del proyecto V_2_0_0.md](docs/03%20Implementación/sprint%202/01%20Informe%20de%20estado%20del%20proyecto%20V_2_0_0.md) |
| 02 | [Registro de Impedimentos V_2_0_0.md](docs/03%20Implementación/sprint%202/02%20Registro%20de%20Impedimentos%20V_2_0_0.md) |
| 03 | [Revisión del Sprint V_2_0_0.md](docs/03%20Implementación/sprint%202/03%20Revisión%20del%20Sprint%20V_2_0_0.md) |
| 04 | [Retrospectiva del Sprint V_2_0_0.md](docs/03%20Implementación/sprint%202/04%20Retrospectiva%20del%20Sprint%20V_2_0_0.md) |

---

## Integrantes del Equipo

| # | Apellidos y Nombres | Rol |
| :--- | :--- | :--- |
| 01 | Cosme Tenorio, Jhunior Harold | Líder del proyecto |
| 02 | Flores Torres, Jhanpool Ernesto | Backend y arquitectura |
| 03 | Tucto Ubaldo, Ricardo David | Frontend y UX/UI |
| 04 | Vega Reyes, Andrew Steven | QA y DevOps |

El detalle completo de cada integrante se registra en
[`docs/inicio/05. Registro de interesados`](docs/inicio/05.%20Registro%20de%20interesados%20V_1_0_0.md).

---

## Licencia

Proyecto desarrollado con fines académicos para el curso Taller de Proyectos 2 —
Ingeniería de Sistemas e Informática.

---

## Enlaces

- **Repositorio:** https://github.com/jhanpooldev/TP2-DistriRapido
- **Documentación:** [`docs/`](docs/)
- **Fase de Inicio:** [`docs/inicio/`](docs/inicio/)
- **Fase de Planificación:** [`docs/planificacion/`](docs/planificacion/)
- **Fase de Implementación:** [`docs/03 Implementación/`](docs/03%20Implementación/)
- **Especificación técnica:** [SPECS.md](SPECS.md)
- **Constitución del proyecto:** [CONSTITUTION.md](CONSTITUTION.md)
- **Estándares de codificación:** [AGENT.md](AGENT.md)
- **Historial de cambios:** [CHANGELOG.md](CHANGELOG.md)