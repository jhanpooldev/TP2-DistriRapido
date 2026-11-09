# Estándares de Ingeniería de Software aplicados a la optimización ambiental

**Proyecto:** EcoLogística Lima — Optimizador de Rutas Sostenibles para DistriRápido S.A.C.  
**Versión del documento:** 1.0.0  
**Fecha:** 09/11/2026  
**Documento relacionado:** `01 Informe de reduccion del impacto ambiental V_1_0_0.md`

---

## 1. Propósito y alcance

Este documento explica cómo se aplicaron estándares de ingeniería de software y
de sostenibilidad digital a las ocho optimizaciones del proyecto. No es una
declaración de certificación ni de conformidad total. Su objetivo es dejar
trazabilidad entre cada decisión técnica, la norma o guía que la respalda y la
evidencia verificable en el repositorio.

### 1.1 Arquitectura real y adaptación del enunciado

El enunciado menciona un stack MERN. El proyecto real usa **FastAPI +
PostgreSQL/SQLAlchemy + React/Vite**. No se reemplazó ninguna tecnología para
"cumplir" el enunciado; se adaptaron las técnicas al stack existente:

| Técnica del enunciado | Equivalente aplicado en este proyecto |
|---|---|
| Optimización de consultas MongoDB | Índices, `count()` y *eager loading* en SQLAlchemy/PostgreSQL |
| Paginación MERN | `page`/`limit` en FastAPI y controles React |
| Optimización de imágenes | `preconnect` y ajuste de tiles remotos; no hay raster propio |
| *Lazy loading* / *code splitting* | `React.lazy`, `Suspense` y `manualChunks` de Vite |
| Limpieza de dependencias | Verificación de `package.json` y `npm ls`; sin dependencias muertas |
| Reducción de peticiones | Caché TTL, deduplicación de GET y carga bajo demanda |
| Caché | `Map` TTL en cliente y `Cache-Control` en FastAPI |
| Compresión | `GZipMiddleware` + middleware Brotli propio |

La lógica de negocio y las reglas de negocio (RN) no se alteraron. La
compatibilidad de la API se preservó explícitamente.

---

## 2. ISO/IEC 25010

Se toma la edición 2011 de ISO/IEC 25010, con sus ocho características de
calidad de producto. La tabla relaciona cada característica con una decisión y
una evidencia concreta; no se atribuye una certificación.

| Característica | Aplicación en el proyecto | Evidencia |
|---|---|---|
| **Adecuación funcional** | Se conservan las reglas de rutas, capacidad, estados, roles y cálculo de CO₂. La paginación no cambia el conjunto de datos, solo su entrega por páginas. | 66 pruebas backend y 24 frontend; `RutaResponse` y `PuntoEntregaList` mantienen sus claves |
| **Eficiencia de desempeño** | Menos bytes iniciales, menos consultas por listado, compresión y caché. | Lighthouse: 130 946 B → 72 564 B; build JS gzip 120,85 → 67,39 kB |
| **Compatibilidad** | Se mantienen `/puntos-entrega` con `{puntos}` y `/rutas` como lista; se conserva `skip`; se exponen cabeceras por CORS. | `puntos.py`, `rutas.py`, `main.py`, pruebas existentes |
| **Usabilidad** | Paginación clara, estados de carga accesibles, `aria-live`, etiquetas de navegación. | `Paginacion.jsx`, `Suspense`, Lighthouse accesibilidad 100 |
| **Fiabilidad** | `pool_pre_ping`, `pool_recycle`, respaldo GZip si Brotli no está disponible, manejo de errores existente. | `database.py`, `compression.py`, `main.py` |
| **Seguridad** | `no-store` en autenticación, limpieza de caché al cerrar sesión, claves de caché por token, sin cambios en JWT/bcrypt/OWASP. | `client.js`, `App.jsx`, `main.py` |
| **Mantenibilidad** | Middleware y componente de paginación con responsabilidad única; funciones pequeñas; comentarios que explican el porqué. | `compression.py`, `Paginacion.jsx`, `_opciones_de_ruta()` |
| **Portabilidad** | Sin servicios nuevos obligatorios; funciona con el mismo FastAPI, PostgreSQL y Vite. Brotli es opcional. | `requirements.txt`, `compression.py`, `vite.config.js` |

### 2.1 Lectura de la tabla

La mejora más fuerte está en **eficiencia de desempeño** y **mantenibilidad**.
La adecuación funcional y la compatibilidad se trataron como restricciones no
negociables: cualquier optimización que rompiera un script o un cliente se
descartaba. La portabilidad se preservó al no introducir Redis, TanStack Query,
un CDN obligatorio ni un servicio de imágenes.

---

## 3. Principios de Green Software Foundation

La Green Software Foundation resume la sostenibilidad del software en cuatro
principios. La aplicación en este proyecto es la siguiente:

| Principio | Significado operativo | Aplicación real | Límite honesto |
|---|---|---|---|
| **Eficiencia de carbono** | Emitir menos carbono por unidad de trabajo | Menos bytes de red y menos consultas; cálculo SWDM con datos medidos | Solo se midió el login público; no se mide la huella completa |
| **Eficiencia energética** | Usar menos energía para la misma función | JS inicial −49,20 % sin comprimir; CSS −54,07 %; compresión de respuestas; índices y *eager loading* | No se midió energía de CPU ni de servidor |
| **Conciencia de carbono** | Ejecutar más trabajo cuando la red eléctrica es más limpia y menos cuando es más intensa | No implementado: no hay señal horaria de intensidad de carbono ni cola de trabajos | Se documenta como brecha, no se simula |
| **Eficiencia de hardware** | Alargar la vida útil del dispositivo y reducir hardware embebido | Menos peso y menos trabajo de CPU en el primer render; Leaflet se carga solo al abrir un mapa | No se midió la vida útil ni el carbono incorporado |

### 3.1 Por qué no se implementó conciencia de carbono

Implementar conciencia de carbono requeriría una fuente de intensidad horaria,
un planificador de tareas y posiblemente una cola. Eso violaría YAGNI y añadiría
infraestructura no justificada para un PMV académico. Se prefiere declarar la
brecha antes que inventar una funcionalidad que no existe.

---

## 4. W3C Web Sustainability Guidelines (WSG)

### 4.1 Referencia y numeración

Se consultó la versión vigente el 09/11/2026
([W3C Group Note Draft, 16/10/2026](https://www.w3.org/TR/web-sustainability-guidelines/)).
En esa versión, las directrices citadas por el enunciado tienen estas
definiciones literales:

- **1.2** → *WSG layers of guidance* (capas de orientación: principios,
  directrices, criterios de éxito y documentación).
- **2.4** → *Design efficient and streamlined user journeys* (diseño de
  recorridos de usuario eficientes y simplificados).
- **3.1** → *Set goals based on performance and energy impact* (objetivos
  basados en rendimiento e impacto energético).

La correspondencia se mantiene literal; no se reinterpretan los números.

### 4.2 Correspondencia

| WSG | Nombre en la versión consultada | Aplicación en EcoLogística Lima | Evidencia |
|---|---|---|---|
| **1.2** | *WSG layers of guidance* | Se usaron las capas de orientación —directrices, criterios de éxito e información adicional— como marco de decisión. | Este documento y el informe ambiental |
| **2.4** | *Design efficient and streamlined user journeys* | Paginación de tablas, pestañas cargadas bajo demanda, estados de carga y menos pasos para llegar al dato. | `Paginacion.jsx`, `Dashboard.jsx`, `RutasTab.jsx` |
| **3.1** | *Set goals based on performance and energy impact* | Umbrales de Lighthouse ≥ 90, presupuesto de tamaño de JS/total y cálculo SWDM. | `.lighthouserc.js`, `green-audit.yml`, informe ambiental |
| 3.3 | *Modularize bandwidth-heavy components* | Leaflet, mapas y pestañas se separan en chunks. | `vite.config.js`, `App.jsx`, `Dashboard.jsx` |
| 3.7 | *Defer the loading of non-critical resources* | `React.lazy` + `Suspense`; catálogo completo solo al abrir rutas/mapa. | `Dashboard.jsx` |
| 3.12 | *Use dependencies sparingly and maintain them* | Solo 4 dependencias de ejecución; sin `moment`/`lodash`; `brotli` justificado. | `package.json`, `npm ls` |
| 3.16 | *Reduce the number and complexity of database queries* | Índices, `count()` y *eager loading*; sin N+1 en listados. | `rutas.py`, `models/__init__.py` |
| 4.2 | *Optimize caching and support offline access* | Caché TTL de 60 s, deduplicación e invalidación; `Cache-Control` en vehículos. | `client.js`, `main.py` |
| 4.3 | *Reduce data transfer with compression* | Brotli + GZip en respuestas; assets comprimidos por el servidor de build. | `compression.py`, `main.py` |

### 4.3 Advertencia de greenwashing

No se declara "sitio sostenible" ni "conformidad WSG total". Se declara una
reducción medida de transferencia y una estimación SWDM de red. La sección 8 del
informe ambiental enumera los límites. Esta distinción sigue el criterio de WSG
sobre no presentar mejoras parciales como sostenibilidad total.

---

## 5. Clean Code, SOLID, DRY y YAGNI

### 5.1 Clean Code

| Práctica | Ejemplo real |
|---|---|
| Nombres que expresan intención | `PAGE_SIZE_DEFAULT`, `_opciones_de_ruta`, `puntosTodosCargados`, `CargandoPanel` |
| Funciones pequeñas y con una responsabilidad | `BrotliMiddleware` comprime; `Paginacion` pinta controles; `_cargar_ruta` carga una ruta con relaciones |
| Comentarios que explican el porqué | Comentarios sobre N+1, `strictPort`, invalidación de caché y compatibilidad de API |
| Sin código muerto | Se reemplazaron imports directos por `lazy`; no se dejaron ramas sin uso |
| Manejo explícito de errores | `try/catch` con `extraerError`; `HTTPException` existente; fallback de compresión |
| Consistencia de estilo | Se mantuvieron nombres en español, comillas simples y estructura de componentes del proyecto |

### 5.2 SOLID

| Principio | Aplicación | Evidencia |
|---|---|---|
| **S** — Responsabilidad única | El middleware Brotli solo comprime; `Paginacion` solo controla páginas; `_cargar_ruta` solo carga una ruta con relaciones. | `compression.py`, `Paginacion.jsx`, `rutas.py` |
| **O** — Abierto/cerrado | La compresión se añade como middleware sin modificar cada endpoint. | `main.py` |
| **L** — Sustitución de Liskov | Las respuestas de `/puntos-entrega` y `/rutas` siguen siendo compatibles con los consumidores existentes. | `puntos.py`, `rutas.py`, scripts existentes |
| **I** — Segregación de interfaces | `Paginacion` recibe solo `page`, `pages`, `total`, `onChange` y `etiqueta`; no obliga a pasar un objeto gigante. | `Paginacion.jsx` |
| **D** — Inversión de dependencias | Se conserva la *service layer* y la dependencia `get_db`; el middleware depende de la interfaz ASGI, no de un servidor concreto. | `main.py`, `database.py` |

No se afirma que todo el repositorio sea SOLID puro; se documentan las
decisiones nuevas que siguen esos principios.

### 5.3 DRY

| Duplicación evitada | Solución |
|---|---|
| Controles de paginación repetidos en dos tablas | Componente `Paginacion` |
| Carga de puntos/vehículo repetida en varios endpoints | `_opciones_de_ruta()` y `_cargar_ruta()` |
| Lógica de caché repetida en cada llamada | Adaptador único en `client.js` |
| Conversión de ruta a respuesta repetida | `_ruta_to_response()` existente, reutilizada |

### 5.4 YAGNI

| Tentación | Decisión |
|---|---|
| Añadir TanStack Query | No: la caché TTL de 60 s y la deduplicación cubren el caso de uso |
| Añadir Redis | No: el PMV no tiene infraestructura de caché distribuida |
| Añadir un servicio de imágenes | No: no hay imágenes raster propias |
| Añadir una librería de paginación | No: 36 líneas de componente resuelven el requisito |
| Añadir compresión en cada endpoint | No: middleware transversal |
| Añadir una cola de trabajos "verde" | No: no hay requisito ni fuente de intensidad de carbono |

### 5.5 Muestras reales antes/después

**Consultas de rutas.** Antes, `_ruta_to_response` consultaba los puntos y el
vehículo de cada ruta por separado. Ahora se cargan con *eager loading*:

```python
# Antes: una consulta por ruta y otra por vehículo
rutas = query.order_by(Ruta.fecha_generacion.desc()).offset(skip).limit(limit).all()
return [_ruta_to_response(db, r) for r in rutas]

# Después: puntos y vehículo precargados
def _opciones_de_ruta():
    return (
        selectinload(Ruta.puntos).selectinload(RutaPunto.punto),
        joinedload(Ruta.vehiculo),
    )

rutas = (
    query.options(*_opciones_de_ruta())
    .order_by(Ruta.fecha_generacion.desc())
    .offset(offset)
    .limit(limit)
    .all()
)
```

**Carga inicial del frontend.** Antes todo el panel y Leaflet entraban en el
bundle inicial; ahora se cargan bajo demanda:

```javascript
// Antes
import Dashboard from './components/Dashboard'
import MapView from './MapView'

// Después
const Dashboard = lazy(() => import('./components/Dashboard'))
const MapView = lazy(() => import('./MapView'))
```

**Caché de cliente.** Antes cada montaje repetía el GET; ahora hay TTL de 60 s,
deduplicación e invalidación en escrituras:

```javascript
// Después (fragmento real de src/frontend/src/api/client.js)
const entrada = cache.get(clave)
if (entrada && entrada.expira > Date.now()) {
  return { ...entrada.respuesta, config }
}
if (enVuelo.has(clave)) return enVuelo.get(clave)
```

Estas muestras provienen del código del repositorio, no de ejemplos genéricos.

---

## 6. Guía verde del backend (FastAPI + SQLAlchemy + PostgreSQL)

Prácticas aplicadas, con su justificación ambiental:

1. **Paginación en la API.** Evita transferir y serializar filas que el cliente
   no va a mostrar. `page`/`limit` con máximo 100.
2. **Consulta de conteo separada.** `count()` permite mostrar el total sin
   cargar todos los registros; es una consulta barata comparada con transferir
   el catálogo.
3. **Índices alineados a los filtros.** `id_operador + fecha`, `estado`,
   `id_vehiculo` y `id_punto` reducen escaneos completos.
4. **Eager loading.** `selectinload`/`joinedload` evitan el N+1 en listados y en
   la autorización por rol.
5. **Pool de conexiones acotado.** `pool_size`, `max_overflow`, `pool_recycle`
   y `pool_pre_ping` reducen el coste de abrir conexiones y evitan conexiones
   muertas.
6. **Compresión de respuestas.** Brotli/GZip reducen bytes de JSON y CSV.
7. **Cabeceras de caché.** `Cache-Control` para el catálogo de vehículos y
   `no-store` para autenticación.
8. **Consultas de autorización sin viajes extra.** `joinedload(Usuario.rol)` en
   login y en `get_current_user`.
9. **Compatibilidad de API.** Los scripts y clientes existentes no se rompen;
   una optimización que rompe consumidores no es sostenible.
10. **Pruebas y compilación.** 66 pruebas y `compileall` antes de dar por válido
    el cambio.

### 6.1 Lo que no se hizo

- No se añadió un ORM alternativo ni se reescribieron consultas estables.
- No se añadió caché de segundo nivel ni Redis.
- No se cambiaron reglas de negocio para "ahorrar" datos.
- No se midió `EXPLAIN ANALYZE` por falta de PostgreSQL local; se documenta como
  pendiente.

---

## 7. Guía verde del frontend (React + Vite)

Prácticas aplicadas:

1. **Carga diferida por funcionalidad.** `Dashboard`, mapas y pestañas se cargan
   cuando se necesitan.
2. **Separación de vendors.** React y Leaflet tienen chunks propios, cacheables
   entre despliegues.
3. **Paginación visible.** Las tablas muestran 12 registros y permiten navegar
   sin descargar todo.
4. **Caché TTL y deduplicación.** Menos peticiones repetidas al cambiar de
   pestaña o re-renderizar.
5. **Invalidación correcta.** Las escrituras y el logout limpian la caché; no se
   sirven datos obsoletos.
6. **Catálogo bajo demanda.** El selector de puntos no pide `limit=100` hasta
   que el usuario entra a la pestaña que lo usa.
7. **`preconnect`.** Se adelanta el handshake con los tiles de OSM y OSRM.
8. **Tiles eficientes.** `updateWhenIdle` y `keepBuffer` reducen peticiones
   intermedias durante el paneo.
9. **Dependencias mínimas.** Solo axios, leaflet, react y react-dom; sin
   librerías de utilidades pesadas.
10. **Accesibilidad preservada.** Los estados de carga usan `role="status"` y
    `aria-live`; Lighthouse mantiene accesibilidad 100.

### 7.1 Trade-offs documentados

- El *code splitting* aumentó las peticiones iniciales de 4 a 6. Se acepta
  porque el total de bytes bajó 44,58 % y los chunks pesados quedan fuera del
  primer render.
- La caché TTL puede mostrar datos de hasta 60 s de antigüedad; se invalida en
  cada escritura y en el logout. Es un balance entre frescura y ahorro.
- La paginación cambia la forma de consumir los listados, pero no su contenido.
  Los clientes antiguos siguen funcionando por compatibilidad de claves,
  cabeceras y `skip`.

---

## 8. Matriz de las ocho optimizaciones

| # | Optimización | ISO/IEC 25010 | GSF | WSG | Clean Code / SOLID / DRY / YAGNI | Estado |
|---|---|---|---|---|---|---|
| 1 | Consultas e índices | Eficiencia, fiabilidad | Eficiencia energética | 3.16 | SRP, DRY, YAGNI | Completado en código; pendiente E2E |
| 2 | Paginación backend/frontend | Eficiencia, usabilidad, compatibilidad | Eficiencia de carbono/energía | 2.4 | DRY, SRP, LSP | Completado en código |
| 3 | Imágenes | Eficiencia | Eficiencia de carbono | 2.4, 3.3 | YAGNI | No aplicable (sin raster); adaptado |
| 4 | Lazy loading / code splitting | Eficiencia, mantenibilidad | Eficiencia energética/hardware | 3.3, 3.7 | SRP, YAGNI | Completado y medido |
| 5 | Limpieza de dependencias | Mantenibilidad, portabilidad | Eficiencia de carbono | 3.12 | YAGNI, DRY | Completado (verificado) |
| 6 | Reducción de peticiones | Eficiencia | Eficiencia de carbono/energía | 3.7, 4.2 | DRY, SRP | Parcial (sin medición E2E) |
| 7 | Caché | Eficiencia, fiabilidad | Eficiencia energética | 4.2 | SRP, DRY | Completado |
| 8 | Compresión Brotli/GZip | Eficiencia, compatibilidad | Eficiencia de carbono/energía | 4.3 | SRP, OCP | Completado a nivel de app |

---

## 9. Tabla de cumplimiento del encargo

| Requisito del encargo | Evidencia | Estado |
|---|---|---|
| Trabajar sobre el proyecto existente sin reemplazar tecnologías | Stack FastAPI/PostgreSQL/React/Vite intacto | Cumplido |
| No eliminar funcionalidades ni alterar reglas de negocio | Pruebas 66 + 24; API compatible | Cumplido |
| Ocho optimizaciones | Matriz de la sección 8 | Cumplido con matices (3 y 6) |
| Paginación `page`/`limit`, por defecto 12 | `puntos.py`, `rutas.py`, `Dashboard.jsx` | Cumplido |
| Optimización de imágenes | `preconnect`, tiles; no hay raster | No aplicable/adaptado |
| Lazy loading / code splitting | `React.lazy`, `Suspense`, `manualChunks` | Cumplido |
| Limpieza de dependencias | `npm ls`; sin dependencias muertas | Cumplido (sin eliminaciones) |
| Reducción de peticiones | Caché/dedupe y carga bajo demanda | Parcial (sin E2E) |
| Caché | TTL cliente + `Cache-Control` | Cumplido |
| Compresión Brotli/GZip | Middleware + prueba TestClient | Cumplido a nivel de app |
| Lighthouse CI real | `green-audit.yml`, `.lighthouserc.js`, 3 ejecuciones | Cumplido |
| Workflow sin `|| true` | `green-audit.yml` | Cumplido |
| Fórmula SWDM v4 y 500 000 visitas | Informe ambiental, sección 5 | Cumplido |
| ISO/IEC 25010 | Sección 2 | Cumplido |
| Cuatro principios GSF | Sección 3 | Cumplido |
| WSG 1.2/2.4/3.1 | Sección 4 | Cumplido con nota de numeración |
| Clean Code/SOLID/DRY/YAGNI | Sección 5 | Cumplido |
| Guías verde backend/frontend | Secciones 6 y 7 | Cumplido |
| Dos documentos solicitados | Este documento y el informe ambiental | Cumplido |
| No commit/push sin autorización | Sin commit/push | Cumplido |

---

## 10. Brechas y siguientes pasos

1. **Medición de base de datos.** Falta PostgreSQL local y `EXPLAIN ANALYZE`
   para convertir la mejora estructural en una cifra de latencia.
2. **Auditoría del panel autenticado.** Lighthouse solo mide el login público;
   falta un usuario de prueba y datos sembrados en CI.
3. **Medición de peticiones del panel.** La caché y la carga bajo demanda están
   implementadas, pero no instrumentadas con un contador E2E.
4. **Conciencia de carbono.** No hay fuente horaria de intensidad ni
   planificador; se declara como no implementado.
5. **Compresión en producción.** Falta validar el middleware detrás de un proxy
   inverso o CDN real.
6. **Catálogos mayores a 100 registros.** Los selectores y las vistas de mapa e
   impacto usan `limit=100`; con más datos habrá que paginar también esas
   vistas o añadir un endpoint de catálogo resumido.
7. **Imágenes remotas.** Los tiles de OSM no se controlan; si en el futuro se
   añaden imágenes propias, deberá aplicarse un pipeline WebP/AVIF y `srcset`.

Estas brechas no invalidan lo medido: delimitan lo que se puede afirmar. La
posición del proyecto es **progreso verificable, no sostenibilidad total**.
