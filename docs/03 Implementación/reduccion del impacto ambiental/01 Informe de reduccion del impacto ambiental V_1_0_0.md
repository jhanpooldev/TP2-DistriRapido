# Informe de reducción del impacto ambiental

**Proyecto:** EcoLogística Lima — Optimizador de Rutas Sostenibles para DistriRápido S.A.C.  
**Versión del informe:** 1.0.0  
**Fecha de medición:** 09/11/2026  
**Alcance:** optimización del consumo de recursos del frontend y del backend existentes, sin reemplazar tecnologías, eliminar funcionalidades ni alterar reglas de negocio.  
**Repositorio:** `D:\Ricardo\TP2-DistriRapido`

---

## 1. Control del documento

| Elemento | Valor |
|---|---|
| Tipo de documento | Informe técnico de sostenibilidad digital |
| Norma de referencia | SWDM v4 (Sustainable Web Design Model) |
| Unidad de medida | bytes transferidos, kWh y g CO₂e |
| Escenario de uso | 500 000 visitas anuales al frontend |
| Herramienta de medición | Lighthouse CI 0.15.1, Chrome Headless 156, 3 ejecuciones |
| Ruta medida | `http://127.0.0.1:4173/` (pantalla pública de login) |
| Estado | Implementado y medido en entorno local; ver limitaciones en la sección 8 |

> Este informe no declara conformidad total con WSG, ISO/IEC 25010 ni con la
> norma ISO 14064. Presenta mejoras verificables y explicita qué no se pudo
> medir. No se atribuyen reducciones de CO₂ que no provengan de la fórmula y
> de los datos de transferencia registrados.

---

## 2. Resumen ejecutivo

Se aplicaron ocho optimizaciones sobre la aplicación existente, construida con
**FastAPI + PostgreSQL/SQLAlchemy + React/Vite**. El enunciado original habla de
un stack MERN; la adaptación se detalla en la sección 3.1. No se sustituyó
ninguna tecnología ni se cambió la lógica de optimización de rutas.

### 2.1 Resultado medido con Lighthouse

La medición se hizo sobre el build de producción servido con `vite preview`, con
emulación móvil predeterminada de Lighthouse y tres ejecuciones por versión.
Los valores de la tabla son la mediana de las tres ejecuciones o el valor
consistente en todas ellas.

| Indicador | Línea base (`e58541c`) | Versión optimizada | Variación |
|---|---:|---:|---:|
| Peso total transferido | 130 946 B | 72 564 B | **−44,58 %** |
| JavaScript transferido | 120 159 B | 68 004 B | **−43,40 %** |
| CSS transferido | 9 707 B | 3 560 B | **−63,33 %** |
| Documento HTML | 923 B | 843 B | −8,67 % |
| Peticiones iniciales | 4 | 6 | +2 (trade-off por *code splitting*) |
| First Contentful Paint (FCP) | 1 528,96 ms | 1 383,56 ms | **−9,51 %** |
| Largest Contentful Paint (LCP) | 1 678,96 ms | 1 533,56 ms | **−8,66 %** |
| Speed Index | 1 528,96 ms | 1 383,56 ms | **−9,51 %** |
| Total Blocking Time (TBT) | 0 ms | 0 ms | Sin cambio |
| Cumulative Layout Shift (CLS) | 0 | 0 | Sin cambio |
| Rendimiento | 99 | 100 | +1 punto |
| Accesibilidad | 100 | 100 | Sin cambio |
| Buenas prácticas | 96 | 96 | Sin cambio |
| SEO | 91 | 91 | Sin cambio |

El total incluye `favicon.ico` (157 B), que Lighthouse contabiliza como
petición; las filas de JavaScript, CSS y HTML no lo suman. Por eso el total no
coincide exactamente con la suma de esas tres filas.

Las cuatro categorías cumplieron los umbrales de `.lighthouserc.js`
(≥ 90). El archivo `src/frontend/.lighthouseci/assertion-results.json` quedó
vacío, lo que significa que no hubo aserciones fallidas.

### 2.2 Resultado de build

| Artefacto inicial | Línea base | Optimizado | Variación |
|---|---:|---:|---:|
| JS inicial sin comprimir | 390,29 kB | 198,26 kB | **−49,20 %** |
| JS inicial gzip | 120,85 kB | 67,39 kB | **−44,24 %** |
| CSS inicial sin comprimir | 27,76 kB | 12,75 kB | **−54,07 %** |
| CSS inicial gzip | 9,37 kB | 3,21 kB | **−65,74 %** |

El JS inicial optimizado es la suma de `index` (57,73 kB), `react`
(139,81 kB) y `rolldown-runtime` (0,72 kB). El panel (`Dashboard`, 19,65 kB),
Leaflet (148,60 kB), su CSS (15,09 kB) y las pestañas se descargan después del
login o al abrir la sección correspondiente.

### 2.3 Resultado ambiental estimado

Con la fórmula SWDM v4 indicada en el enunciado:

```text
E = GB transferidos × 0,815 kWh/GB × 442 g CO₂e/kWh
```

| Concepto | Línea base | Optimizado | Ahorro |
|---|---:|---:|---:|
| GB por visita | 0,000130946 | 0,000072564 | 0,000058382 |
| Energía por visita | 0,000106721 kWh | 0,000059140 kWh | 0,000047581 kWh |
| CO₂e por visita | 0,047171 g | 0,026140 g | **0,021031 g** |
| Energía anual (500 000 visitas) | 53,3605 kWh | 29,5698 kWh | **23,7907 kWh** |
| CO₂e anual (500 000 visitas) | 23,5853 kg | 13,0699 kg | **10,5155 kg** |

El ahorro porcentual calculado es **44,58 %** en transferencia y emisiones de
red. Es una estimación de red, no una medición de ciclo de vida completo.

---

## 3. Contexto, alcance y metodología

### 3.1 Adaptación del enunciado MERN a la arquitectura real

El repositorio no usa MongoDB, Express ni Node.js en el backend. La tabla
siguiente documenta la correspondencia aplicada; no se reemplazó ninguna pieza
del sistema.

| Elemento del enunciado | Implementación real | Adaptación aplicada |
|---|---|---|
| MongoDB | PostgreSQL + SQLAlchemy ORM | Índices, `count()` y *eager loading* en SQLAlchemy |
| Express | FastAPI | Middleware ASGI, dependencias y *service layer* existentes |
| React | React 18 + Vite | Carga diferida, *code splitting* y caché de cliente |
| Node.js backend | Python 3.12 + Uvicorn | `GZipMiddleware` y middleware Brotli propio |
| Optimización de consultas NoSQL | Consultas SQL relacionales | Evitar N+1 con `selectinload`/`joinedload` e índices compuestos |
| Imágenes del bundle | No hay imágenes raster locales | `preconnect` a OSM/OSRM y ajuste de tiles remotos |

La lógica de negocio —cálculo de rutas, ahorro de CO₂, reglas de capacidad,
roles y estados— no se modificó.

### 3.2 Entorno de medición

| Elemento | Detalle |
|---|---|
| Sistema operativo | Windows, entorno local del estudiante |
| Node.js / npm | 24.16.0 / 11.13.0 |
| Chrome | HeadlessChrome 156.0.0.0 |
| Lighthouse CI | `@lhci/cli@0.15.1` |
| Servidor | `vite preview --host 127.0.0.1 --port 4173 --strictPort` |
| Build | `npm run build` con Vite 8.3.5 |
| Backend de pruebas | Python 3.12.16 en entorno virtual temporal |
| Base de datos | No disponible; ver sección 8 |

La línea base se obtuvo desde un *worktree* limpio en `e58541c`, sin cambios
locales, para que la comparación no dependiera del árbol de trabajo modificado.

### 3.3 Comandos ejecutados

```powershell
# Frontend
cd src/frontend
npm ci
npm test -- --reporter=dot
npm run build

# Lighthouse (3 ejecuciones, configuración de la raíz)
$env:CHROME_PATH = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
npx --yes @lhci/cli@0.15.1 autorun --config=../../.lighthouserc.js

# Backend (Python 3.12 en venv temporal)
python -m pytest --cov=app --cov-report=term-missing -q
python -m compileall -q app
```

---

## 4. Las ocho optimizaciones

### 4.1 Optimización de consultas

**Problema.** El listado de rutas resolvía los puntos y el vehículo de cada ruta
con consultas adicionales. En un listado de *n* rutas se producía el patrón N+1:
una consulta por ruta, otra por sus puntos y otra por el factor de emisión.

**Antes** (`src/backend/app/api/v1/endpoints/rutas.py`, versión base):

```python
rutas = query.order_by(Ruta.fecha_generacion.desc()).offset(skip).limit(limit).all()
return [_ruta_to_response(db, r) for r in rutas]
```

`_ruta_to_response` volvía a consultar `RutaPunto` y `_factor_co2_de_ruta`
volvía a consultar `ParametrosVehiculo` por cada ruta.

**Después** (código actual):

```python
def _opciones_de_ruta():
    """Carga en pocas consultas los puntos y el vehiculo de cada ruta."""
    return (
        selectinload(Ruta.puntos).selectinload(RutaPunto.punto),
        joinedload(Ruta.vehiculo),
    )

def _cargar_ruta(db: Session, ruta_id: uuid.UUID):
    return (
        db.query(Ruta)
        .options(*_opciones_de_ruta())
        .filter(Ruta.id_ruta == ruta_id)
        .first()
    )
```

```python
rutas = (
    query.options(*_opciones_de_ruta())
    .order_by(Ruta.fecha_generacion.desc())
    .offset(offset)
    .limit(limit)
    .all()
)
```

También se agregó `joinedload(Usuario.rol)` en el login y en la dependencia de
autenticación, porque el rol se consultaba en cada petición autenticada.

**Índices agregados** (`models/__init__.py` y `esquema.sql`):

```python
Index("ix_usuarios_id_rol", "id_rol")
Index("ix_puntos_entrega_operador_fecha", "id_operador", "fecha_registro")
Index("ix_rutas_operador_fecha", "id_operador", "fecha_generacion")
Index("ix_rutas_estado", "estado")
Index("ix_ruta_puntos_punto", "id_punto")
```

`init_db()` ejecuta además `CREATE INDEX IF NOT EXISTS` para que una base ya
creada reciba los índices sin borrar datos.

**Evidencia.** Las 66 pruebas de backend pasan. No se pudo ejecutar
`EXPLAIN ANALYZE` contra PostgreSQL porque no hay servicio local; por eso no se
afirma una mejora porcentual de latencia de base de datos. La mejora es
estructural: menos viajes y menos escaneos completos.

**Estado:** completado en código; pendiente de medición con PostgreSQL real.

---

### 4.2 Paginación en backend y frontend

**Problema.** Los listados devolvían hasta 100 registros y el frontend pedía el
catálogo completo al iniciar. La tabla y el mapa cargaban datos que el usuario
todavía no necesitaba.

**Backend, antes** (`puntos.py`):

```python
@router.get("", response_model=PuntoEntregaList)
def list_puntos(skip: int = 0, limit: int = 100, ...):
    puntos = db.query(PuntoEntrega).filter(...).offset(skip).limit(limit).all()
    return {"puntos": puntos}
```

**Backend, después:**

```python
PAGE_SIZE_DEFAULT = 12
PAGE_SIZE_MAX = 100

@router.get("", response_model=PuntoEntregaList)
def list_puntos(
    page: int = Query(1, ge=1),
    limit: int = Query(PAGE_SIZE_DEFAULT, ge=1, le=PAGE_SIZE_MAX),
    skip: Optional[int] = Query(None, ge=0, description="Offset explicito; reemplaza a page si se envia"),
    ...
):
    filtro = PuntoEntrega.id_operador == operador.id_usuario
    total = db.query(func.count(PuntoEntrega.id_punto)).filter(filtro).scalar() or 0
    offset = skip if skip is not None else (page - 1) * limit
    puntos = (
        db.query(PuntoEntrega)
        .filter(filtro)
        .order_by(PuntoEntrega.fecha_registro.desc(), PuntoEntrega.id_punto)
        .offset(offset)
        .limit(limit)
        .all()
    )
    return {
        "puntos": puntos,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit,
    }
```

`GET /rutas` conserva el cuerpo como lista para no romper clientes existentes.
Los metadatos viajan en cabeceras:

```python
total = query.order_by(None).count()
offset = skip if skip is not None else (page - 1) * limit
pages = (total + limit - 1) // limit

response.headers["X-Total-Count"] = str(total)
response.headers["X-Total-Pages"] = str(pages)
response.headers["X-Page"] = str(page)
response.headers["X-Page-Size"] = str(limit)
```

Las cabeceras se expusieron en `CORSMiddleware` para que el frontend pueda
leerlas.

**Frontend, antes** (`Dashboard.jsx`):

```javascript
const fetchRutas = async () => {
  try { const r = await api.get('/rutas'); setRutas(r.data) } catch (e) { ... }
}
```

**Frontend, después:**

```javascript
const fetchRutas = async (page = 1) => {
  try {
    const r = await api.get('/rutas', {
      params: { page, limit: RUTAS_POR_PAGINA },
    })
    setRutas(r.data)
    setTotalRutas(Number(r.headers['x-total-count'] ?? r.data.length))
    setPaginaRutas(Number(r.headers['x-page'] ?? page))
  } catch (e) { mostrar('error', extraerError(e)) }
}
```

Se añadió `Paginacion.jsx`, un componente reutilizable con navegación
`Anterior`/`Siguiente`, etiqueta accesible y estado `aria-live`. La tabla de
pedidos y la de rutas usan 12 elementos por página.

**Compatibilidad.** `GET /puntos-entrega` sigue entregando `puntos` y ahora
también `total`, `page`, `limit` y `pages`. `GET /rutas` sigue siendo una lista.
`skip` se mantiene para los scripts `auditoria_api.py` y `smoke_sprint2.py`.

**Estado:** completado en código y en frontend; pendiente de prueba E2E con base
de datos.

---

### 4.3 Optimización de imágenes

**Hallazgo.** El repositorio no contiene imágenes raster locales (PNG, JPG,
WebP ni AVIF). Los únicos recursos de imagen son los *tiles* remotos de
OpenStreetMap que Leaflet solicita en tiempo de ejecución. Por tanto, no había
un pipeline de imágenes del que eliminar peso.

**Adaptación aplicada.** Se redujo el coste de conexión y la cantidad de tiles
solicitados durante el paneo:

```html
<!-- src/frontend/index.html -->
<link rel="preconnect" href="https://a.tile.openstreetmap.org" />
<link rel="preconnect" href="https://b.tile.openstreetmap.org" />
<link rel="preconnect" href="https://c.tile.openstreetmap.org" />
<link rel="preconnect" href="https://router.project-osrm.org" crossorigin />
```

```javascript
// src/frontend/src/components/MapView.jsx
const capa = L.tileLayer(OSM_TILE_URL, {
  attribution: OSM_ATTRIBUTION,
  maxZoom: 19,
  updateWhenIdle: true, // no pide tiles intermedios durante el paneo
  keepBuffer: 2,
})
```

**Estado:** no aplicable para imágenes del bundle; adaptado con `preconnect` y
ajuste de tiles remotos. No se controla el formato ni la compresión de los
tiles de OSM.

---

### 4.4 Carga diferida y *code splitting*

**Problema.** El build base generaba un único JS de 390,29 kB (120,85 kB gzip)
que incluía React, Leaflet, el panel y todas las pestañas.

**Antes** (`App.jsx` y `Dashboard.jsx`):

```javascript
import Dashboard from './components/Dashboard'
// ...
import MapView from './MapView'
import MapPicker from './MapPicker'
import RutasTab from './RutasTab'
import ImpactoTab from './ImpactoTab'
import SelectorPuntos from './SelectorPuntos'
```

**Después:**

```javascript
// App.jsx
const Dashboard = lazy(() => import('./components/Dashboard'))

// Dashboard.jsx
const MapView = lazy(() => import('./MapView'))
const MapPicker = lazy(() => import('./MapPicker'))
const RutasTab = lazy(() => import('./RutasTab'))
const ImpactoTab = lazy(() => import('./ImpactoTab'))
const SelectorPuntos = lazy(() => import('./SelectorPuntos'))
```

Cada bloque pesado se envuelve en `Suspense` con un estado de carga accesible.
Además, `vite.config.js` separa React y Leaflet en chunks propios:

```javascript
manualChunks(id) {
  if (id.includes('node_modules/react') || id.includes('node_modules/react-dom')) {
    return 'react'
  }
  if (id.includes('node_modules/leaflet')) return 'leaflet'
  return undefined
}
```

**Resultado real del build:**

| Chunk | Peso | gzip | Cuándo se descarga |
|---|---:|---:|---|
| `index` | 57,73 kB | 21,65 kB | Inicial |
| `react` | 139,81 kB | 45,32 kB | Inicial (compartido y cacheable) |
| `rolldown-runtime` | 0,72 kB | 0,42 kB | Inicial |
| `Dashboard` | 19,65 kB | 5,74 kB | Después del login |
| `leaflet` | 148,60 kB | 43,33 kB | Al abrir un mapa |
| `leaflet.css` | 15,09 kB | 6,36 kB | Al abrir un mapa |
| `MapView` / `MapPicker` | 7,98 / 4,82 kB | 3,27 / 2,34 kB | Al abrir el mapa correspondiente |
| `RutasTab` / `ImpactoTab` | 8,05 / 4,33 kB | 2,66 / 1,35 kB | Al abrir la pestaña |

El JS inicial baja de 390,29 a 198,26 kB sin comprimir y de 120,85 a 67,39 kB
gzip. El número de peticiones iniciales sube de 4 a 6 por la separación en
chunks; es un *trade-off* deliberado: menos bytes totales y mejor caché a largo
plazo, a cambio de dos peticiones HTTP/1.1 adicionales en el primer acceso. En
HTTP/2 el coste de esas peticiones es menor.

**Estado:** completado y medido.

---

### 4.5 Limpieza y verificación de dependencias

**Hallazgo.** El frontend declara solo cuatro dependencias de ejecución:
`axios`, `leaflet`, `react` y `react-dom`. No se encontraron `moment`,
`lodash`, `jquery` ni librerías equivalentes. El backend usa las dependencias
necesarias para FastAPI, SQLAlchemy, PostgreSQL, JWT, bcrypt, validación y
pruebas.

**Verificación real:**

```text
$ npm ls --depth=0
ecologistica-frontend@1.0.0
+-- @vitejs/plugin-react@6.1.2
+-- @vitest/coverage-v8@5.0.5
+-- axios@1.20.0
+-- leaflet@1.9.4
+-- react-dom@18.3.1
+-- react@18.3.1
+-- vite@8.3.5
`-- vitest@5.0.5

$ npm ls moment lodash
`-- (empty)
```

No se eliminó ninguna dependencia porque no había una dependencia declarada sin
uso. La única adición de backend es `brotli==1.1.0`, necesaria para la
compresión Brotli y justificada en la sección 4.8. Se evitó añadir TanStack
Query, Redis, una librería de paginación o un servicio de imágenes: la
funcionalidad se resolvió con APIs nativas y código propio pequeño.

**Estado:** completado (verificación sin cambios destructivos).

---

### 4.6 Reducción de peticiones HTTP

Se aplicaron tres mecanismos:

1. **Paginación:** las tablas piden 12 registros, no el catálogo completo.
2. **Caché TTL + deduplicación:** dos componentes que piden el mismo GET al
   mismo tiempo comparten una sola petición; una repetición dentro de 60 s se
   sirve desde memoria.
3. **Carga bajo demanda:** el catálogo de puntos solo se pide al entrar a la
   pestaña de rutas, y el histórico de rutas solo al abrir mapa o impacto. Para
   no anular la paginación, esa carga usa `limit=100`, el máximo de la API.

**Código real** (`src/frontend/src/api/client.js`):

```javascript
const CACHE_TTL_MS = 60_000
const CACHE_MAX_ENTRADAS = 50
const cache = new Map()
const enVuelo = new Map()

api.defaults.adapter = async (config) => {
  const esGet = (config.method || 'get').toLowerCase() === 'get'
  const cacheable = esGet && config.cache !== false && config.responseType !== 'blob'
  if (!cacheable) return adaptadorOriginal(config)

  const clave = claveDeCache(config)
  const entrada = cache.get(clave)
  if (entrada && entrada.expira > Date.now()) {
    return { ...entrada.respuesta, config }
  }
  if (enVuelo.has(clave)) return enVuelo.get(clave)

  const peticion = adaptadorOriginal(config)
    .then((respuesta) => {
      guardarEnCache(clave, respuesta)
      return respuesta
    })
    .finally(() => enVuelo.delete(clave))

  enVuelo.set(clave, peticion)
  return peticion
}
```

Cualquier `POST`, `PUT` o `DELETE` limpia la caché para que la siguiente lectura
vea el cambio. El cierre de sesión también la limpia.

**Resultado honesto.** En la carga inicial del login las peticiones subieron de
4 a 6 por el *code splitting*; no se redujo el número inicial. La reducción
aplica a la navegación posterior del panel y a las consultas repetidas, pero no
se instrumentó un contador de peticiones del panel autenticado. Por eso esta
optimización se marca **parcial** y no se le atribuye un porcentaje.

**Estado:** parcial (implementado; sin medición E2E del panel).

---

### 4.7 Caché

Se usaron dos capas, sin añadir infraestructura:

| Capa | Implementación | Vigencia |
|---|---|---|
| Cliente | `Map` TTL en `client.js` | 60 s; invalidación en escrituras y logout |
| HTTP | `Cache-Control: private, max-age=300` en `/api/v1/vehiculos` | 5 min |
| HTTP | `Cache-Control: no-store` en `/api/v1/auth/*` | Sin caché |
| Navegador | Chunks con hash de Vite | Cacheables entre despliegues |

```python
# src/backend/app/main.py
if request.method == "GET" and response.status_code == 200:
    if request.url.path == "/api/v1/vehiculos":
        response.headers.setdefault("Cache-Control", "private, max-age=300")
    elif request.url.path.startswith("/api/v1/auth/"):
        response.headers.setdefault("Cache-Control", "no-store")
```

No se añadió Redis ni un CDN porque el PMV no los tiene y el enunciado pide no
sobreingeniería. La caché de cliente es deliberadamente pequeña (máximo 50
entradas) y acotada por token, para no mezclar respuestas entre sesiones.

**Estado:** completado.

---

### 4.8 Compresión de respuestas (Brotli/Gzip)

**Antes.** FastAPI no comprimía las respuestas; el JSON de listados viajaba
completo.

**Después.** Se agregó `GZipMiddleware` de Starlette y un middleware Brotli
propio, con `brotli` como dependencia opcional. Si el paquete no está instalado
o el cliente no acepta `br`, la petición sigue sin cambios y GZip actúa como
respaldo.

```python
# src/backend/app/main.py
app.add_middleware(GZipMiddleware, minimum_size=500)
app.add_middleware(BrotliMiddleware, minimum_size=500)
```

```python
# src/backend/app/core/compression.py
if "br" not in cabeceras.get("accept-encoding", "").lower():
    await self.app(scope, receive, send)
    return

# Se comprime en esta capa y se evita que GZip vuelva a comprimir.
scope = dict(scope)
scope["headers"] = [
    (nombre, valor)
    for nombre, valor in scope["headers"]
    if nombre.lower() != b"accept-encoding"
] + [(b"accept-encoding", b"identity")]
```

**Prueba real del middleware** (Starlette `TestClient`, sin base de datos):

```text
brotli OK: content-encoding=br, content-length=159
gzip OK: content-encoding=gzip, content-length=271
identity OK: content-length=5361
```

Es decir, un cuerpo JSON de 5 361 B pasó a 159 B con Brotli (−97,03 %) y a
271 B con GZip (−94,94 %) en la prueba controlada. Esta prueba valida el
middleware, no el balanceador ni el servidor de producción.

**Estado:** completado a nivel de aplicación; la compresión de los assets
estáticos del frontend depende del hosting (Vite preview ya sirve los archivos
comprimidos en la medición de Lighthouse).

---

## 5. Cálculo ambiental con SWDM v4

### 5.1 Fórmula y datos

Se usa exactamente la fórmula solicitada:

```text
E = GB × 0,815 kWh/GB × 442 g CO₂e/kWh
```

Los GB se obtienen del peso transferido medido por Lighthouse, no de una
estimación manual:

```text
Línea base: 130 946 B ÷ 1 000 000 000 = 0,000130946 GB
Optimizado:  72 564 B ÷ 1 000 000 000 = 0,000072564 GB
```

### 5.2 Desarrollo

**Línea base, por visita:**

```text
E = 0,000130946 × 0,815 = 0,000106721 kWh
CO₂e = 0,000106721 × 442 = 0,047171 g
```

**Optimizado, por visita:**

```text
E = 0,000072564 × 0,815 = 0,000059140 kWh
CO₂e = 0,000059140 × 442 = 0,026140 g
```

**Ahorro por visita:**

```text
0,047171 − 0,026140 = 0,021031 g CO₂e
0,021031 ÷ 0,047171 = 44,58 %
```

**Proyección anual para 500 000 visitas:**

```text
Línea base: 0,047171 g × 500 000 = 23 585,34 g = 23,5853 kg CO₂e
Optimizado: 0,026140 g × 500 000 = 13 069,86 g = 13,0699 kg CO₂e
Ahorro: 10 515,47 g = 10,5155 kg CO₂e
Energía: 53,3605 − 29,5698 = 23,7907 kWh
```

### 5.3 Interpretación y límites del cálculo

- La reducción del **44,58 %** corresponde al peso de red del login público.
- No incluye energía de servidores, fabricación de dispositivos, red de acceso,
  refrigeración ni desplazamientos del personal.
- No se aplica un factor de intensidad de carbono horario variable; se usa el
  valor fijo de 442 g CO₂e/kWh indicado en el enunciado.
- 500 000 visitas es un escenario de proyección, no una medición de tráfico
  real.
- Si se usaran 1 000 000 de visitas, el ahorro estimado sería 21,031 kg CO₂e;
  es una regla de tres, no un dato adicional medido.

---

## 6. Verificación ejecutada

| Verificación | Comando | Resultado |
|---|---|---|
| Pruebas backend | `python -m pytest --cov=app --cov-report=term-missing -q` | **66 passed**, 1 warning, 3,47 s |
| Cobertura backend | incluida en pytest | **63 %** (1 030 sentencias, 378 sin cubrir) |
| Pruebas frontend | `npm test -- --reporter=dot` | **24 passed**, 3 archivos, 448 ms |
| Build frontend | `npm run build` | 85 módulos, build correcto en 632 ms |
| Sintaxis Python | `python -m compileall -q app` | Correcto |
| YAML del workflow | `yaml.safe_load` sobre `green-audit.yml` | Correcto; job `lighthouse` |
| Lighthouse | `lhci autorun` (3 ejecuciones) | 4 categorías ≥ 90; sin aserciones fallidas |
| Compresión | prueba con `TestClient` | Brotli y GZip verificados |
| Dependencias | `npm ls --depth=0` | Sin dependencias declaradas sin uso |

La cobertura de backend subió de 60,82 % (dato previo del README) a 63 % en esta
ejecución. No se modificó el README para no mezclar una medición nueva con el
histórico del proyecto; el dato queda aquí y en la salida de pytest.

---

## 7. Archivos modificados y creados

### Backend

- `src/backend/app/api/v1/endpoints/auth.py`
- `src/backend/app/api/v1/endpoints/dependencies.py`
- `src/backend/app/api/v1/endpoints/puntos.py`
- `src/backend/app/api/v1/endpoints/rutas.py`
- `src/backend/app/core/compression.py` *(nuevo)*
- `src/backend/app/core/database.py`
- `src/backend/app/main.py`
- `src/backend/app/models/__init__.py`
- `src/backend/app/schemas/__init__.py`
- `src/backend/esquema.sql`
- `src/backend/requirements.txt` *(solo `brotli==1.1.0`)*

### Frontend

- `src/frontend/index.html`
- `src/frontend/src/App.jsx`
- `src/frontend/src/api/client.js`
- `src/frontend/src/components/Dashboard.jsx`
- `src/frontend/src/components/MapPicker.jsx`
- `src/frontend/src/components/MapView.jsx`
- `src/frontend/src/components/RutasTab.jsx`
- `src/frontend/src/components/Paginacion.jsx` *(nuevo)*
- `src/frontend/src/styles/index.css`
- `src/frontend/vite.config.js`

### CI y documentación

- `.lighthouserc.js` *(nuevo)*
- `.github/workflows/green-audit.yml` *(nuevo)*
- `.gitignore` *(ignora `.lighthouseci/`)*
- `CHANGELOG.md`
- `SPECS.md` *(nota de paginación y compatibilidad)*
- `docs/03 Implementación/reduccion del impacto ambiental/01 Informe de reduccion del impacto ambiental V_1_0_0.md`
- `docs/03 Implementación/reduccion del impacto ambiental/02 Estandares Ingeniería de software V_1_0_0.md`

---

## 8. Limitaciones y riesgos

1. **Sin PostgreSQL local.** No hay servicio PostgreSQL en el entorno de
   medición ni archivo `.env`. Las pruebas de backend son unitarias y las rutas
   que dependen de base de datos no se ejecutaron de extremo a extremo. No se
   midió latencia real, `EXPLAIN ANALYZE` ni el número exacto de consultas
   eliminadas.
2. **Lighthouse solo audita el login público.** El panel autenticado requiere
   credenciales y base de datos; no se automatizó su auditoría. Los pesos de los
   chunks del panel se obtuvieron del build, no de Lighthouse.
3. **Entorno local.** Los tiempos de Lighthouse dependen del hardware y de la
   red del estudiante. Los porcentajes de peso son más estables que los tiempos;
   aun así, tres ejecuciones no sustituyen una medición de campo (RUM).
4. **Peticiones iniciales.** El *code splitting* aumentó las peticiones de 4 a
   6. La afirmación de sostenibilidad se basa en bytes y energía, no en una
   reducción del número de peticiones iniciales.
5. **Catálogos de más de 100 registros.** Los selectores y las vistas de mapa e
   impacto piden `limit=100`, el máximo permitido por la API. Con más de 100
   puntos o rutas, esas vistas muestran solo los 100 más recientes; las tablas
   sí siguen paginando el total completo.
6. **Imágenes.** No hay imágenes raster propias. Los tiles de OpenStreetMap son
   remotos y no se controlan; no se puede afirmar que se hayan optimizado.
7. **Compresión.** El middleware se validó con `TestClient`. No se verificó a
   través de un proxy inverso, CDN o servidor de producción. El build estático
   servido por `vite preview` no usa el middleware de FastAPI.
8. **Cálculo SWDM.** Es una estimación de red con los factores del enunciado.
   No es un análisis de ciclo de vida ni una auditoría de huella de carbono.
9. **Git.** No se hizo commit ni push; los cambios quedan en el árbol de trabajo
   a la espera de autorización explícita.

---

## 9. Conclusiones

- La transferencia inicial del login bajó **44,58 %** y el JS inicial gzip
  **44,24 %**, con mejora de FCP y LCP y sin perder accesibilidad ni SEO.
- La carga diferida y la separación de chunks son la palanca principal del
  ahorro: Leaflet y el panel ya no bloquean el primer render.
- La paginación, los índices y el *eager loading* atacan el consumo del backend,
  aunque su efecto no se pudo cuantificar sin PostgreSQL.
- La compresión Brotli/GZip funciona a nivel de aplicación y reduce respuestas
  JSON de forma significativa en la prueba controlada.
- El ahorro anual estimado para 500 000 visitas es **10,515 kg CO₂e** y
  **23,791 kWh**; es una cifra pequeña y debe presentarse como estimación de
  red, no como resultado de ciclo de vida.

### Siguientes pasos recomendados

1. Levantar PostgreSQL en CI/local y ejecutar `EXPLAIN ANALYZE` antes/después de
   los índices y del *eager loading*.
2. Automatizar una sesión autenticada en Lighthouse CI con un usuario de prueba
   y datos sembrados.
3. Medir peticiones reales del panel con el panel de red o instrumentación RUM.
4. Evaluar un CDN con Brotli para los assets estáticos y una política de caché
   de largo plazo para los chunks con hash.
5. Revisar si el catálogo completo de puntos puede seguir paginándose en los
   selectores en lugar de pedir `limit=100`.

---

## Anexo A. Evidencia de Lighthouse

Los reportes HTML/JSON de las tres ejecuciones quedaron en:

```text
src/frontend/.lighthouseci/
```

El directorio está ignorado por Git (`.gitignore`) para no versionar artefactos
generados. Para reproducir la medición:

```powershell
cd src/frontend
npm run build
$env:CHROME_PATH = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
npx --yes @lhci/cli@0.15.1 autorun --config=../../.lighthouserc.js
```

La línea base se midió desde el *worktree* limpio `e58541c` en
`C:\Users\estudianteuc\AppData\Local\Temp\opencode\baseline-frontend` con
`vite preview` en el puerto 4173, usando la misma configuración de Lighthouse.
Ese *worktree* es temporal y no forma parte del repositorio.

## Anexo B. Configuración de umbrales

`.lighthouserc.js` exige como mínimo 90 en rendimiento, accesibilidad, buenas
prácticas y SEO. Además advierte si el JS supera 260 000 B o el total supera
500 000 B. El workflow no usa `|| true`: si una categoría baja del umbral, el
job falla.
