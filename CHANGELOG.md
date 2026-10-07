# CHANGELOG

Todas las novedades relevantes de **EcoLogística Lima – Optimizador de Rutas Sostenibles para DistriRápido S.A.C.**

El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y el
versionado sigue [SemVer](https://semver.org/lang/es/) (`MAJOR.MINOR.PATCH`).

---

## [No publicado]

### Estructura del PFA alineada a las 5 estructuras de la pauta

- El repositorio cumple ahora las cinco estructuras requeridas del PFA a nivel de
  raíz: `docs/` (Documentación), `src/` (Código), `pruebas/` (Pruebas),
  `base de datos/` (Scripts SQL) y `modelos/` (Modelamiento).
- **`src/backend/esquema.sql`**: DDL completo de PostgreSQL, generado
  automáticamente desde los modelos SQLAlchemy (`src/backend/app/models`) e
  incluyendo constraints, checks e índices. Vive dentro del backend, junto al
  código que lo usa, para mantener limpia la raíz del proyecto. Complementa la
  ausencia de migraciones (el proyecto crea el esquema con
  `Base.metadata.create_all` al arrancar).
- **`pruebas/`**: índice que consigna el plan de pruebas y las evidencias, y
  referencia las suites automatizadas (`src/backend/tests`) y las herramientas de
  verificación de extremo a extremo (`auditoria_api.py`, `smoke_sprint2.py`).
- **`modelos/`**: índice que consigna el modelamiento del PMV (C4, diseño de base
  de datos y reglas de negocio) residente en la fase de Inicio.
- `README.md` (sección Estructura del Proyecto) actualizado para reflejar las
  cinco estructuras y la ubicación real de `auditoria_api.py` y `smoke_sprint2.py`.

### Experiencia de uso (UX) y seleccion de pedidos por cercania

- **Paleta visual reescrita** en `src/frontend/src/styles/index.css` con variables
  de color (verde azulado ecologico sobre fondo neutro). Se reemplazaron los azules
  saturados y grises que "tapaban" el contenido por colores suaves y coherentes entre
  el login, el mapa, los marcadores y las alertas.
- **Proposito del programa visible**: la pantalla de ingreso explica "para que sirve"
  y el panel inicial muestra "Como funciona" en tres pasos (registrar pedidos, armar la
  ruta, medir el ahorro).
- **Navegacion por flujo**: el menu superior enumera los pasos (1 Pedidos, 2 Rutas,
  3 Mapa, 4 Impacto, 5 Vehiculos) y las pestanas sin datos muestran que accion tomar
  en lugar de tablas vacias.
- **Seleccion de pedidos por cercania**: nuevo componente `SelectorPuntos` que ordena
  los pedidos del mas cercano al mas lejano respecto al ultimo punto agregado (o el
  centro de Lima), muestra la distancia de cada uno, permite buscar por direccion o
  destinatario, y con un clic agrega "el siguiente mas cercano". Incluye barra de
  ocupacion de la carga del vehiculo y bloquea un pedido que excedera la capacidad.
- **El flujo de deteccion de cercania se comparte con la edicion de rutas**: editar una
  ruta guardada usa el mismo selector, de modo que el pedido mas cercano tambien puede
  sumarse a una ruta existente.
- **Utilidad `distancia.js`** con `haversineKm` (la misma formula del backend),
  `ordenarPorCercania`, `masCercano` y `formatoKm`, probada en aislamiento.
- **Detalles menores**: alertas con boton de cierre, botones con jerarquia
  (primario/secundario/ghost/eliminar), tablas con desplazamiento en pantallas
  pequenas, formularios con etiquetas vinculadas y mensajes de validacion mas claros.

### Documentación del Sprint 1 y limpieza del repositorio

- Restaurados los cuatro entregables de la fase de Implementación, que habían
  sido sobrescritos con el contenido del Sprint 2:
  `01 Informe de estado del proyecto V_1_0_0.md`,
  `02 Registro de Impedimentos V_1_0_0.md`,
  `03 Revisión del Sprint V_1_0_0.md` y
  `04 Retrospectiva del Sprint V_1_0_0.md`.
- **Consolidada la retrospectiva del Sprint 1** en `04 Retrospectiva del Sprint V_1_0_0.md`,
  el nombre que exige la consigna. El archivo previo declaraba cifras que el repositorio no
  respalda (15 pruebas en verde, 92 % de cobertura) y presentaba MFA como parte del Sprint 1;
  ambos datos se retiraron. El título interno se conserva como `# Reprospectiva del sprint`,
  conforme a la plantilla oficial.
- Los entregables del Sprint 2 quedaron archivados en `docs/03 Implementación/sprint 2/`
  con versión `V_2_0_0`, tras retirar de ellos las cifras de cobertura y de total de
  pruebas que no resultaban verificables.
- **Eliminado `backend/` de la raíz del repositorio** (24 archivos versionados).
  Era una implementación heredada e inactiva, con MFA y una organización distinta de
  módulos, que coexistía con el backend real en `src/backend` y podía inducir a
  trabajar sobre el código equivocado.
- **README corregido** para que refleje el repositorio real: se retiraron Tailwind,
  Alembic, Vitest, Testing Library y GitHub Actions, que no existen en el proyecto; se
  documentó que no hay migraciones, ni lint, ni pruebas de frontend; y se añadieron los
  enlaces a los entregables de ambos sprints.
- `docs/inicio/14. Especificacion MFA y Sesiones` incluye ahora una nota de estado que
  aclara que el módulo de MFA **no está implementado**, y se corrigió la ruta interna
  del borrador OpenSpec.

### Herramientas de verificación corregidas

- `auditoria_api.py` ya no toma los puntos del listado del operador para calcular
  rutas: creaba sus propios puntos y los eliminaba al terminar. La auditoría usaba el
  operador demo sembrado, que acumula puntos de sesiones anteriores, de modo que un
  punto residual con coordenadas inválidas producía "rutas" de miles de kilómetros
  dentro de Lima y activaba falsas anomalías.
- `smoke_sprint2.py` se autoprovisiona: si no hay ninguna ruta guardada, crea una con
  puntos propios. Antes dependía de una ruta preexistente y la borraba al finalizar,
  por lo que solo podía ejecutarse una vez.
- El factor de emisión dejó de estar fijo en `smoke_sprint2.py` y se lee del vehículo
  de la ruta, conforme a **RN-017**. La comprobación anterior validaba una constante
  del propio script en lugar de la regla de negocio.
- Ambos scripts son ahora **herméticos**: dejan la base de datos en el mismo estado en
  que la encontraron y su ejecución es repetible.

### Limitación conocida registrada

- Con **exactamente tres puntos**, la búsqueda local 2-opt no se ejecuta: el recorrido
  `range(1, len(best) - 2)` queda vacío y la ruta devuelta es la del Vecino Más Cercano
  sin refinar. Si el orden de entrada resulta mejor, la API puede informar una distancia
  optimizada levemente mayor que la no optimizada. El ahorro no llega a ser negativo
  porque se acota en cero. Registrado como **IMP-10**.

### Sprint 2 implementado (US-002, US-004, US-005, US-007)

- **US-004**: las respuestas de ruta incorporan `ahorro_co2_kg`,
  `ahorro_co2_pct`, `ahorro_distancia_pct` y `sin_reduccion_significativa`.
  Los porcentajes nunca son negativos (RN-018) y las reducciones inferiores al
  1 % se reportan como "sin reducción significativa" en lugar de mostrar un
  ahorro engañoso. Los kilos ahorrados se calculan con el factor de emisión real
  del vehículo, no con la diferencia en kilómetros. Nueva pestaña
  **Impacto Ambiental** con la comparación lado a lado.
- **US-005**: el mapa Leaflet/OpenStreetMap detecta el fallo del proveedor de
  tiles y muestra un mensaje controlado con opción de reintentar, en lugar de
  presentar un mapa en blanco. Si el mapa base no carga, el orden de entrega
  sigue visible en la tabla.
- **US-002**: `PUT /api/v1/rutas/{id}` reemplaza los puntos de una ruta
  guardada y recalcula distancia, tiempo y CO₂. Interfaz con botones
  **Editar** (multiselección de puntos, validación de capacidad) y
  **Eliminar** con confirmación.
- **US-007**: `GET /api/v1/rutas` acepta `desde`, `hasta` y `estado`. Las fechas
  admiten `YYYY-MM-DD` o ISO completo, el rango es inclusivo y un formato
  inválido devuelve `400` explicando el formato esperado en vez de ignorarse en
  silencio. La interfaz muestra un aviso cuando el filtro no arroja resultados.
- **Corrección de defectos**:
  - `PUT /rutas/{id}` no confirmaba la transacción, por lo que las ediciones se
    perdían al cerrar la sesión. Ahora la edición persiste y no crea una ruta
    duplicada.
  - El borrado de una ruta dejaba filas huérfanas en `ruta_puntos`.
  - RN-013 se aplica de forma explícita: no se puede eliminar una ruta con
    entregas en curso o completadas.
  - Los filtros de fecha con `hasta` exclusive del día completo excluían las
    rutas creadas ese mismo día.
- **Depuración completa (auditoría de API)**: se corrigieron los siguientes
  defectos detectados al revisar cada endpoint contra `SPECS.md`:
  - `GET /api/v1/auth/me` no devolvía el rol del usuario. `UsuarioResponse` ahora
    incluye `rol` anidado con `RolResponse`, y el campo es obligatorio para
    reflejar que `id_rol` es `NOT NULL` en la base de datos. El hash de la
    contraseña nunca se expone.
  - `POST /auth/register` era público, lo que permitía que cualquiera creara un
    Administrador y escalara privilegios. Ahora exige rol Administrador.
  - `DELETE /puntos-entrega/{id}` dejaba filas huérfanas en `ruta_puntos` al
    borrar un punto asignado a una ruta. Ahora se bloquea con `400`.
  - `PUT /puntos-entrega/{id}` no existía en la API. Se añadió con las mismas
    validaciones de creación y devuelve el recurso actualizado.
  - `GET /api/v1/health` figuraba en `SPECS.md` sin implementar. Ahora responde
    `200` con el estado de la base de datos y devuelve `503` cuando la base de
    datos no responde, en lugar de aparentar un servicio sano.
  - El arranque de la API fallaba si la base de datos no estaba disponible, con
    lo que `/health` no podía reportar el problema. El inicializador registra el
    error y la API arranca para que el chequeo de salud sea útil.
  - `RutaResponse.puntos` usaba una lista mutable por defecto, compartida entre
    instancias. Ahora usa `default_factory`.
- **Correcciones en el frontend**:
  - `App.jsx` usaba su propia instancia de Axios, sin timeout ni manejo de
    errores, y cerraba la sesión en silencio si el backend no respondía. Ahora
    usa el cliente compartido, solo cierra la sesión ante un `401` y ofrece
    reintentar cuando el servidor está caído.
  - `Login.jsx` usaba `fetch` sin timeout y mostraba errores en inglés. Ahora usa
    el cliente compartido, muestra mensajes en español y evita el doble envío.
  - El botón "Reintentar" del mapa recargaba toda la aplicación con
    `window.location.reload()`, perdiendo el estado. Ahora solo recrea la capa de
    tiles.
  - El contador de fallos de tiles se reiniciaba con cada tile correcto, por lo
    que un proveedor de mapas parcialmente caído no mostraba aviso. Ahora los
    errores solo se limpian al reintentar.
  - `MapView` y `MapPicker` no destruían la instancia de Leaflet al
    desmontarse, duplicando contenedores al cambiar de pestaña. Ahora liberan el
    mapa en el cleanup del efecto.
- **Verificación**: 51 pruebas unitarias (`pytest`), una auditoría de API de
  extremo a extremo (`auditoria_api.py`, sin anomalías) y un smoke test
  (`smoke_sprint2.py`) cubren los criterios de aceptación, el aislamiento entre
  usuarios y los permisos por rol.

### Desviación conocida

- **RN-014**: si la carga supera la capacidad del vehículo, la API rechaza la
  operación completa en lugar de dejar los puntos excedentes "pendientes". Es
  el comportamiento más simple de Implementar y de explicar; se documenta como
  desviación respecto del texto de la regla.
- **HTTPS**: el entorno local sirve por HTTP; la Johns Hopkins exige HTTPS en
  Staging, previsto para el Sprint 3.

### Sprint 1 verificado contra los criterios de aceptación

Se auditó el código contra los ítems **US-001, US-003, EN-01 y EN-02** (21 Story
Points, 05/10/2026 – 18/10/2026) y se corrigieron las brechas encontradas:

- **EN-02**: las peticiones sin token o con token inválido devolvían `403`; ahora
  devuelven `401 Unauthorized` con cabecera `WWW-Authenticate: Bearer`, según el
  criterio de aceptación.
- **US-001**: se valida que la dirección no sea vacío y que las coordenadas no
  correspondan a una geolocalización fallida (`0,0`); el sistema rechaza el punto
  con un mensaje explicativo en lugar de registrarlo.
- **US-003 / EN-01**: los límites de 2 a 20 puntos por ruta se validan en el
  endpoint y devuelven mensajes en español; antes el mensaje provenía del
  validador de Pydantic. La interfaz deshabilita los botones de cálculo cuando
  la selección es inválida e informa el límite alcanzado.
- **Corrección de defecto**: `GET /api/v1/rutas/{id}/puntos` serializaba la
  entidad intermedia `RutaPunto` y fallaba en tiempo de ejecución; ahora devuelve
  los datos del punto correctamente.
- Se eliminó la duplicación de cálculo entre `POST /rutas/optimizar` y
  `POST /rutas`, centralizándolo en una función compartida.

### Añadido

- Suite de pruebas automatizadas en `src/backend/tests/` (25 pruebas) que cubre
  el motor de ruteo, las validaciones de entrada y la seguridad JWT, incluidas
  las pruebas del SLA de 5 segundos con 20 puntos de EN-01.

### Documentado como desviación

- **RNF-02 (HTTPS)**: el desarrollo y la demostración se realizan sobre HTTP en
  `localhost`. El cifrado en tránsito queda planteado para el ambiente de
  Staging, que se configura en el Sprint 3 con EN-03.

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