# CHANGELOG

Todas las novedades relevantes de **EcoLogística Lima – Optimizador de Rutas Sostenibles para DistriRápido S.A.C.**

El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y el
versionado sigue [SemVer](https://semver.org/lang/es/) (`MAJOR.MINOR.PATCH`).

---

## [No publicado]

### Cambios documentales en curso

Saneamiento de coherencia interna entre los artefactos de las fases de Inicio y
Planificación, previo al inicio de la codificación del Sprint 0 (Hito H3).
Ver las secciones **Enmiendas a la Constitución** y **Verificación realizada**
más abajo.

---

## [0.1.0] — 2026-10-01

### Añadido

- `CONSTITUTION.md` como documento rector del proyecto.
- `SPECS.md` con la especificación técnica (actores, reglas de negocio, restricciones, API y modelo de datos).
- `README.md` con el contexto del problema, objetivos, stack e instrucciones de ejecución.
- `AGENT.md` con los estándares de codificación y límites del repositorio.
- `docs/inicio/` — 13 documentos de la fase de Inicio (enfoque, acta de constitución, visión, supuestos y restricciones, interesados, requisitos funcionales y no funcionales, usuarios, reglas de negocio, stack tecnológico, base de datos, modelo C4 y análisis de restricciones).
- `docs/planificacion/` — 4 documentos de la fase de Planificación (transformación a ágil con backlog priorizado y DoD, artefactos Jira, registro de riesgos y presupuesto).

### Cambiado

- Nomenclatura de las carpetas de documentación a minúsculas y sin acentos (`docs/inicio`, `docs/planificacion`), alineada con la estructura exigida por `CONSTITUTION.md` y la restricción RES-02.
- Renombrado del archivo de constitución de `Constitucion.md` a `CONSTITUTION.md` para cumplir la nomenclatura literal exigida por RES-02.
- `SPECS.md` alineado con el alcance del PMV: actores, RF-001 a RF-006, API REST bajo `/api/v1`, modelo de datos de cinco tablas, motor de optimización propio, KPIs y criterios de aceptación.
- `README.md` reorganizado por completo (descripción, problema, objetivos, análisis de negocio, KPIs, funcionalidades, arquitectura, estructura, stack, instalación, variables, pruebas, estándares, metodología y documentación), con Tabla de Contenidos funcional.

### Corregido

- **RN-010** (mínimo de puntos para generar una ruta): decía "al menos un punto de entrega", en contradicción directa con el criterio de aceptación de **US-003** y con la ruta dorada de **RF-006**, que exigen **al menos dos puntos**. Corregido a ≥ 2 puntos de entrega (además del centro de distribución).
- **RN-017** (cálculo de CO₂): la fórmula dependía de un consumo de combustible que no existía en el modelo de datos. Se agregó el atributo `consumo_litros_km` a `PARAMETROS_VEHICULO` para que el cálculo sea realizable.
- **RN-011** (centro de distribución como origen): se documentó que en el PMV el punto de origen se configura mediante variables de entorno (`HOME_ADDRESS`, `HOME_LAT`, `HOME_LNG`), ya que no existía entidad de configuración en el modelo del PMV.
- **RN-018** (comparación optimizada vs. no optimizada): se agregaron `distancia_sin_optimizar_km` y `tiempo_sin_optimizar_min` a la tabla `RUTAS`, ya que la comparación de ahorro exige esos valores y solo se almacenaba el CO₂ de referencia.
- **Modelo C4 / Base de datos**: el diagrama ER omitía la entidad `PARAMETROS_VEHICULO` pese a estar definida en el DDL. Se incorporó al diagrama.
- **Persistencia de rutas**: se documentó que las rutas se persisten directamente en estado `Confirmada`, coherente con RN-012, y se agregó la restricción `UNIQUE (id_ruta, orden)` en `ruta_puntos` para garantizar un orden de visita único por ruta.
- **Stack tecnológico**: se eliminó la mención de Cypress como herramienta de pruebas del frontend (el alcance usa Vitest) y se aclaró que OR-Tools queda reservado para una versión futura, mientras el PMV usa heurística propia (Haversine + Vecino Más Cercano + 2-opt).
- **Supuesto SUP-01**: la validación del nivel gratuito del proveedor de mapas se reprogramó al Sprint 2, cuando se integra el adaptador externo; en el Sprint 1 el cálculo de distancias es local y no consume cuota.
- **Ubicación del `.env`**: el árbol de proyecto del `README.md` sugería un `.env` dentro de `src/backend`, en contradicción con los pasos de instalación. Se unificó en la raíz del repositorio.
- **Calendario de sprints**: `docs/planificacion/01` y `02` no distinguían entre el Sprint 0 (base del proyecto, hito H3) y el Sprint 1. Se añadió la tabla de calendario completa y se fijaron las fechas reales del Sprint 1 (05/10/2026 – 18/10/2026) en los artefactos de Jira.
- **Numeración de documentos**: los títulos internos ("Documento 01" a "Documento 08") no coincidían con la numeración de los archivos (`06.` a `13.`). Se unificó usando la numeración del archivo como canónica.
- **Rutas de documentos**: `docs/planificacion/02 Artefactos Jira` referenciaba `docs/02 Planificación/img/`, una ruta con formato ajeno al del repositorio. Corregida a `docs/planificacion/img/`, indicando que la carpeta se crea al tomar la primera captura.
- **`README.md`**: el Markdown estaba corrupto (cercas de código perdidas y tablas convertidas en texto corrido). Se repararon las secciones de instalación, variables de entorno, pruebas, buenas prácticas y metodología.

### Documentación

- `.gitignore` creado en la raíz, excluyendo `node_modules`, `venv`, `__pycache__`, `.coverage`, artefactos de build y el archivo `.env`.
- `.gitattributes` creado para normalizar los finales de línea a LF en el repositorio, evitando el ruido de conversiones CRLF entre sistemas operativos.
- `.env.example` creado como plantilla de configuración, sin ningún valor real de credenciales.
- Estructura de código fuente normalizada a `src/backend` y `src/frontend`, conforme a la organización exigida por la consigna.
- `docs/` queda con las carpetas `inicio/` y `planificacion/`. Las carpetas de las fases posteriores (ejecucion, seguimiento y control, cierre) se crearán cuando exista la evidencia que las compone.

---

## Enmiendas a la Constitución

Registro de los cambios aprobados en los documentos constitutivos, conforme al
procedimiento de enmienda definido en `CONSTITUTION.md` (consenso del equipo
4/4 + Product Owner).

### Enmienda 1 — Estructura del código fuente

- **Sección afectada:** Estructura del Proyecto.
- **Antes:** `/backend`, `/frontend` y `/tests` en la raíz del repositorio.
- **Después:** `/src/backend` y `/src/frontend`; las pruebas automatizadas residen dentro de cada aplicación (`src/backend/tests` con pytest y `src/frontend/src/**/*.test.jsx` con Vitest).
- **Justificación:** la consigna del curso exige organización del código en carpetas independientes y claramente identificadas. Se elimina la carpeta `/tests` de raíz para evitar duplicar la suite y repartirla entre las aplicaciones que la consumen.

### Enmienda 2 — Docker y `docker-compose.yml`

- **Sección afectada:** Estructura del Proyecto.
- **Antes:** `/docker` y `docker-compose.yml` listados como parte de la estructura a incluir.
- **Después:** se mantienen como **opcionales y no aplicados en el PMV**, por no existir Docker en el entorno de desarrollo del equipo.
- **Justificación:** mantener el costo de infraestructura en S/ 0.00 sin depender de un motor de contenedores no disponible. El despliegue en hosting gratuito se documenta en `README.md` sin contenedores.

### Enmienda 3 — Integrantes del equipo en el `README.md`

- **Sección afectada:** Requisitos de Documentación → README.md.
- **Antes:** el `README.md` no listaba a los integrantes, pese a que `CONSTITUTION.md` lo exige de forma obligatoria.
- **Después:** se incorpora la sección **Integrantes del Equipo** con los cuatro integrantes y sus códigos, más un enlace al Registro de Interesados para el detalle de roles y datos de contacto.
- **Justificación:** dar cumplimiento al requisito de la Constitución sin duplicar información sensible que ya reside en los documentos de la fase de Inicio.

---

## Verificación realizada

- Todos los enlaces internos entre documentos Markdown resuelven a archivos existentes.
- Las 18 anclas de la Tabla de Contenidos del `README.md` corresponden a encabezados reales.
- Estructura de encabezados: sin saltos de nivel en ningún documento y todas las cercas de código balanceadas.
- Todas las tablas Markdown tienen un número de columnas uniforme entre su encabezado y sus filas.
- **DDL de `docs/inicio/11` validado**: las 6 claves foráneas apuntan a tablas y columnas existentes; los tipos de las FK coinciden con sus PK (`INTEGER` ~ `SERIAL`, `UUID` ~ `UUID`); los 8 índices referencian columnas existentes; el modelo lógico y el DDL coinciden en los 45 atributos; las 6 tablas aparecen en `SPECS.md`.
- `.env` queda correctamente excluido por `.gitignore`, mientras que `.env.example` permanece versionable.
- `docs/` contiene únicamente `inicio/` y `planificacion/`, sin carpetas vacías ni archivos auxiliares.
- Búsqueda de referencias obsoletas (`docs/01 Inicio`, `docs/Planificación`, `Constitucion.md`): sin coincidencias pendientes. Las apariciones restantes son referencias históricas dentro del propio `CHANGELOG.md`.
- `/src/backend/tests` y `/src/frontend/src/**/*.test.jsx` aparecen de forma consistente en `CONSTITUTION.md`, `AGENT.md`, `README.md` y `CHANGELOG.md`.