# Análisis de Playwright y pruebas de extremo a extremo

[← Volver al README principal](../../../README.md)

---

**Nombre del Proyecto:** EcoLogística Lima – Optimizador de Rutas Sostenibles para DistriRápido S.A.C.

**Líder del Proyecto:** Jhunior Harold Cosme Tenorio

**Sprint:** 4

**Periodo:** 09/11/2026 – 17/11/2026

**Fecha de ejecución:** 17/11/2026

---

## Control de Versiones del Documento

| Versión | Fecha | Autor | Descripción del Cambio |
|:---:|:---:|:---|:---|
| 1.0.0 | 17/11/2026 | Jhunior Harold Cosme Tenorio / Equipo EcoLogística | Análisis de la suite E2E, las métricas de rendimiento y las pruebas de resiliencia. |

---

## 1. Objetivo y alcance

Este documento describe la suite de pruebas de extremo a extremo (E2E) incorporada en el
Sprint 4, la metodología de medición de rendimiento y los resultados reales obtenidos el
17/11/2026.

La suite verifica la aplicación completa —frontend React/Vite y backend FastAPI sobre
PostgreSQL— desde el navegador, sin mocks de la API salvo en los casos que
deliberadamente simulan fallos de red o errores del servidor.

**Queda fuera del alcance de este documento:**

- el despliegue en Producción (no existe un ambiente desplegado);
- la prueba de usabilidad SUS (ver [`04 Usabilidad V_1_0_0.md`](04%20Usabilidad%20V_1_0_0.md));
- la auditoría Lighthouse (corresponde a `green-audit.yml` y al informe de impacto
  ambiental del repositorio).

---

## 2. Herramientas y versiones

| Elemento | Versión / valor |
|---|---|
| Framework de pruebas | `@playwright/test` 1.65.1 |
| Chromium | Chrome for Testing 159.0.8154.6 (build v1255) |
| Firefox | Firefox 159.0 (build v1572) |
| WebKit | WebKit 27.2 (build v2388) |
| Node.js local | 24.15.0 |
| Frontend | React 18.3.1 + Vite 8.3.5 |
| Backend | FastAPI 0.115.6 + Uvicorn 0.34.0 |
| Base de datos | PostgreSQL 18 local |
| Sistema operativo de la corrida | Windows (entorno local) |
| Viewport | 1280 × 720 |
| Zona horaria / idioma | `America/Lima` / `es-PE` |

---

## 3. Arquitectura de la suite

La configuración vive en
[`src/frontend/playwright.config.js`](../../../src/frontend/playwright.config.js) y
toma decisiones explícitas:

| Decisión | Valor | Motivo |
|---|---|---|
| `testDir` | `./e2e` | Las pruebas viven junto al frontend que verifican. |
| `outputDir` | `./test-results/artifacts` | Separa trazas y capturas de fallo del reporte HTML. |
| `fullyParallel` | `false` | La base de datos es compartida; el paralelismo produciría interferencias. |
| `workers` | `1` | Ejecución en serie por la misma razón. |
| `retries` | `0` local, `1` en CI | En local se quiere ver el fallo real; en CI se tolera un fallo transitorio. |
| `headless` | `true` | La suite no depende de una sesión gráfica. |
| `trace` | `retain-on-failure` | Traza completa solo cuando algo falla. |
| `screenshot` | `only-on-failure` | Evita llenar el disco de imágenes en cada corrida. |
| `video` | `retain-on-failure` | Permite revisar el fallo sin volver a ejecutar. |
| `baseURL` | `http://127.0.0.1:5173` | Evita la resolución IPv6 de `localhost` en Windows. |

### 3.1 Proyectos de navegador

```js
projects: [
  { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
  { name: 'firefox',  use: { ...devices['Desktop Firefox'] } },
  { name: 'webkit',   use: { ...devices['Desktop Safari'] } },
]
```

Los tres proyectos son obligatorios: la consigna exige compatibilidad con los tres
motores. El caso de capturas se omite en Firefox y WebKit mediante
`test.skip(({ browserName }) => browserName !== 'chromium', ...)` para no duplicar
imágenes equivalentes.

### 3.2 Arranque automático de la aplicación

Playwright levanta los dos servidores antes de ejecutar la suite y los reutiliza si ya
están corriendo en local:

| Servidor | Comando | Verificación de disponibilidad |
|---|---|---|
| Backend | `venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000` (Windows) o `python -m uvicorn ...` (Linux/CI) | `GET /health` |
| Frontend | `npm run dev -- --host 127.0.0.1 --port 5173 --strictPort` | `http://127.0.0.1:5173` |

Esto hace que `npm run test:e2e` sea suficiente para reproducir la suite, sin pasos
manuales previos.

### 3.3 Reportes y artefactos

| Reporte | Salida | Versionado |
|---|---|---|
| Consola | `list` | No aplica |
| HTML | `playwright-report/` | **Ignorado por Git**; se publica como artefacto en CI |
| JSON | `test-results/results.json` | Se copia como evidencia a `docs/Evidencias/playwright-sprint4/resultados.json` |
| Trazas / capturas / videos de fallo | `test-results/artifacts/` | **Ignorados por Git**; se publican como artefacto en CI |

---

## 4. Inventario de pruebas

La suite contiene **27 casos** por navegador, distribuidos en cinco archivos. Con tres
proyectos, la corrida produce **81 ejecuciones**.

| Archivo | Casos | Categoría | Qué verifica |
|---|---:|---|---|
| `auth.spec.js` | 7 | Autenticación y navegación | Formulario de acceso, credenciales inválidas, campos obligatorios, cinco secciones del panel, visibilidad del alta de vehículos según rol y cierre de sesión. |
| `flujo-principal.spec.js` | 7 | Negocio | Registro de pedido, validación de formulario, cálculo/guardado/exportación de ruta, bloqueo con un solo pedido, filtro sin resultados, edición y eliminación. |
| `resiliencia.spec.js` | 11 | API y errores | Salud, 401 sin token, 401 con token inválido, 422 de coordenadas, 400 con un solo punto, 404 de ruta inexistente, 400 de placa duplicada, cabeceras de endurecimiento, caché y errores de interfaz. |
| `rendimiento.spec.js` | 1 | Rendimiento | TTFB, FCP, LCP, `DOMContentLoaded`, `load` y tiempos de los endpoints principales. |
| `evidencias.spec.js` | 1 | Evidencia visual | Capturas de login, panel, rutas, mapa, impacto y vehículos (solo Chromium). |

### 4.1 Ayudantes compartidos

`src/frontend/e2e/utils.js` centraliza:

- `loginApi(request)` y `loginUi(page)`: autenticación por API y por interfaz.
- `crearPuntosDePrueba(request, token, cantidad)`: crea pedidos con identificadores
  únicos.
- `crearRuta(request, token, idVehiculo, idsPuntos)`: genera una ruta real.
- `limpiarRutaYPuntos(request, token, idRuta, puntos)`: elimina los datos en `finally`.
- `obtenerVehiculoId(request, token)`: obtiene el primer vehículo disponible sin fijar
  un id concreto.

El uso de `finally` garantiza que un fallo de aserción no deje datos huérfanos en la
base compartida.

---

## 5. Flujos de negocio cubiertos

| Requisito / funcionalidad | Caso E2E | Evidencia |
|---|---|---|
| Login y sesión (RF-01, RN-005) | `auth.spec.js` | 7 casos en tres navegadores. |
| Registro de pedidos (US-001) | `flujo-principal.spec.js` — registro y validación | Tabla de pedidos actualizada. |
| Cálculo y guardado de ruta (US-003) | `flujo-principal.spec.js` — calcula, guarda y exporta | Ruta visible en la pestaña Rutas. |
| Exportación CSV (US-008) | `flujo-principal.spec.js` — descarga y encabezado `Orden,Destinatario` | Archivo descargado y contenido verificado. |
| Mapa y detalle de paradas (US-005, US-006) | `evidencias.spec.js` — pestaña Mapa | Captura `04-panel-mapa.png`. |
| Impacto ambiental (US-004) | `evidencias.spec.js` — pestaña Impacto | Captura `05-panel-impacto.png`. |
| Gestión de flota (RF-05) | `auth.spec.js` y `evidencias.spec.js` | Capturas 06 y 07; formulario solo para Administrador. |
| Edición y eliminación de ruta (US-002) | `flujo-principal.spec.js` — edita y elimina | Ruta recalculada y luego ausente. |
| Listado y filtro de rutas (US-007) | `flujo-principal.spec.js` — filtro sin resultados | Mensaje de filtro vacío visible. |
| Menos de 2 puntos (RN-010) | `flujo-principal.spec.js` y `resiliencia.spec.js` | Bloqueo en UI y `400` en API. |
| Capacidad y validación de entrada (RN-014, RN-007) | `resiliencia.spec.js` | `422` de coordenadas y validaciones de formulario. |

---

## 6. Pruebas de resiliencia HTTP

Los casos de `resiliencia.spec.js` comprueban el comportamiento real de la API y de la
interfaz:

| Caso | Entrada | Resultado esperado | Resultado real |
|---|---|---|---|
| Salud con API y BD disponibles | `GET /health` | `200` con `estado=ok`, `base_datos=ok`, `version=1.0.0` | Cumplido. |
| Acceso sin token | `GET /puntos-entrega` | `401` con `WWW-Authenticate: Bearer` | Cumplido. |
| Token inválido | `GET /puntos-entrega` con token falso | `401` | Cumplido. |
| Coordenadas fuera de rango | `POST /puntos-entrega` con latitud 91 | `422` y mención de `latitud` | Cumplido. |
| Ruta con un solo punto | `POST /rutas` con un punto | `400` con "al menos 2 puntos" | Cumplido. |
| Ruta inexistente | `GET /rutas/{uuid}` | `404` con "Ruta no encontrada" | Cumplido. |
| Placa duplicada | `POST /vehiculos` con placa existente | `400` con "Placa ya existe" | Cumplido. |
| Cabeceras de endurecimiento | `GET /health` con `X-Request-ID` | `X-Request-ID` conservado, `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: no-referrer`, `Permissions-Policy` con geolocalización | Cumplido. |
| Caché de autenticación | `POST /auth/login` | `Cache-Control: no-store` | Cumplido. |
| Caché de catálogo | `GET /vehiculos` | `Cache-Control: private, max-age=300` | Cumplido. |
| Backend caído en la interfaz | `page.route` aborta `/puntos-entrega` | Aviso "No se pudo conectar con el servidor" | Cumplido. |
| Error 500 en la interfaz | `page.route` responde `500` con `detail` | El panel muestra el detalle del error | Cumplido. |

Los casos que crean datos —ruta con un solo punto, placa duplicada— limpian lo creado
con `limpiarRutaYPuntos` o reutilizan datos existentes sin modificarlos.

---

## 7. Metodología de rendimiento

### 7.1 Métricas de navegación

El caso `rendimiento.spec.js` instala un `PerformanceObserver` **antes** de navegar para
no perder el LCP y luego lee:

| Métrica | Fuente | Interpretación |
|---|---|---|
| TTFB | `navigation.responseStart` | Tiempo hasta el primer byte de la respuesta. |
| FCP | `paint` → `first-contentful-paint` | Primer contenido pintado. |
| LCP | `PerformanceObserver` → `largest-contentful-paint` | Elemento de mayor contenido visible. |
| `DOMContentLoaded` | `navigation.domContentLoadedEventEnd` | Fin del parseo del HTML. |
| `load` | `navigation.loadEventEnd` | Fin de la carga de recursos. |

Se realiza una **primera navegación de calentamiento** y se mide la **segunda**, porque
la primera carga contra Vite compila dependencias y produce cifras que no representan el
comportamiento estable.

Para el panel se crea un **contexto nuevo** con el `storageState` de la sesión, de modo
que la medición no reutiliza la caché del contexto de login.

### 7.2 Tiempos de API

Cada endpoint se cronometra con `Date.now()` alrededor de la petición:

- `GET /health`
- `POST /auth/login`
- `GET /puntos-entrega?page=1&limit=12`
- `GET /rutas?page=1&limit=12`
- `GET /vehiculos`

### 7.3 Resultados reales del 17/11/2026

**Navegación:**

| Métrica | Chromium | Firefox | WebKit |
|---|---:|---:|---:|
| Login — TTFB | 4 ms | 7 ms | 3 ms |
| Login — FCP | 124 ms | 125 ms | 156 ms |
| Login — LCP | 124 ms | 125 ms | 156 ms |
| Login — `DOMContentLoaded` | 86 ms | 119 ms | 81 ms |
| Login — `load` | 86 ms | 126 ms | 82 ms |
| Panel — TTFB | 12 ms | 5 ms | 3 ms |
| Panel — FCP | 252 ms | 219 ms | 203 ms |
| Panel — LCP | 744 ms | 708 ms | 664 ms |
| Panel — `DOMContentLoaded` | 179 ms | 211 ms | 130 ms |
| Panel — `load` | 223 ms | 220 ms | 132 ms |

**API:**

| Endpoint | Chromium | Firefox | WebKit | Estado |
|---|---:|---:|---:|---:|
| `GET /health` | 7 ms | 7 ms | 5 ms | 200 |
| `POST /auth/login` | 213 ms | 229 ms | 216 ms | 200 |
| `GET /puntos-entrega` | 11 ms | 9 ms | 11 ms | 200 |
| `GET /rutas` | 13 ms | 13 ms | 12 ms | 200 |
| `GET /vehiculos` | 7 ms | 7 ms | 7 ms | 200 |

Los archivos crudos están en:

- [`performance-chromium.json`](../../Evidencias/playwright-sprint4/performance-chromium.json)
- [`performance-firefox.json`](../../Evidencias/playwright-sprint4/performance-firefox.json)
- [`performance-webkit.json`](../../Evidencias/playwright-sprint4/performance-webkit.json)

### 7.4 Umbrales aplicados por la prueba

La prueba falla si:

- TTFB de login o panel es 0 o ≥ 3 000 ms;
- FCP de login o panel es 0 o ≥ 5 000 ms;
- LCP disponible es ≥ 8 000 ms;
- cualquier endpoint responde con estado ≥ 400;
- cualquier endpoint tarda ≥ 5 000 ms.

Estos umbrales son **de sanidad**, no de rendimiento óptimo: detectan una regresión
grave, no miden la calidad de producción.

---

## 8. Resultados de la corrida

| Indicador | Valor |
|---|---:|
| Fecha y hora de inicio | 17/11/2026, 18:39:14 UTC |
| Duración | 105,1 s |
| Casos por navegador | 27 |
| Ejecuciones totales | 81 |
| Aprobadas | **79** |
| Omitidas | **2** |
| Fallidas | **0** |
| Inestables (*flaky*) | **0** |
| Errores de la suite | **0** |

Desglose por navegador:

| Navegador | Aprobadas | Omitidas | Fallidas |
|---|---:|---:|---:|
| Chromium | 27 | 0 | 0 |
| Firefox | 26 | 1 | 0 |
| WebKit | 26 | 1 | 0 |

La única omisión por navegador corresponde al caso de capturas, que se ejecuta solo en
Chromium.

---

## 9. Evidencias

La carpeta
[`docs/Evidencias/playwright-sprint4/`](../../Evidencias/playwright-sprint4/)
contiene:

| Archivo | Contenido |
|---|---|
| `resultados.json` | Reporte JSON completo de Playwright (configuración, suites, casos y estadísticas). |
| `performance-chromium.json` | Métricas de navegación y API en Chromium. |
| `performance-firefox.json` | Métricas de navegación y API en Firefox. |
| `performance-webkit.json` | Métricas de navegación y API en WebKit. |
| `01-login.png` | Pantalla de acceso. |
| `02-panel-pedidos.png` | Panel con la tabla de pedidos. |
| `03-panel-rutas.png` | Pestaña de rutas guardadas. |
| `04-panel-mapa.png` | Mapa con la ruta y el detalle de paradas. |
| `05-panel-impacto.png` | Comparación de emisiones. |
| `06-panel-vehiculos-operador.png` | Flota vista por el Operador. |
| `07-panel-vehiculos-administrador.png` | Alta de vehículos vista por el Administrador. |

El reporte HTML completo (`playwright-report/`) **no se versiona** por su tamaño y porque
se regenera en cada corrida; el workflow `tests.yml` lo publica como artefacto.

---

## 10. Integración con GitHub Actions

El workflow
[`.github/workflows/tests.yml`](../../../.github/workflows/tests.yml) ejecuta la
suite en un runner `ubuntu-latest`:

1. Servicio PostgreSQL 16.
2. Python 3.12 y dependencias del backend.
3. Node.js 22 y `npm ci`.
4. `npx playwright install --with-deps chromium firefox webkit`.
5. `npm run test:e2e`.
6. Publicación de `playwright-report/`, `test-results/` y las evidencias visuales como
   artefactos, incluso si la suite falla.

**Estado real:** el workflow **se ejecutó en GitHub el 19/11/2026** sobre el commit
`85eac48` (run `44560349236`, conclusión **success**). El job E2E terminó en verde entre
las 15:56:00 y las 16:00:07 UTC y publicó `playwright-report`, `playwright-results` y
`playwright-evidencias`. Los logs detallados no son legibles sin autenticación, pero la
conclusión del job y los artefactos son verificables en la API pública de GitHub.

---

## 11. Cómo ejecutar la suite

```bash
cd src/frontend
npm ci
npx playwright install chromium firefox webkit

npm run test:e2e            # Los tres navegadores
npm run test:e2e:headed     # Con interfaz gráfica
npm run test:e2e:report     # Abre el reporte HTML
```

En Windows, si PowerShell bloquea `npx.ps1`, se puede usar:

```powershell
node node_modules/@playwright/test/cli.js test
```

La suite requiere PostgreSQL en ejecución y el archivo `.env` configurado en la raíz. El
`webServer` de Playwright levanta el backend y el frontend automáticamente.

---

## 12. Limitaciones

1. **Medición local, no productiva.** Los tiempos provienen del servidor de desarrollo de
   Vite y de PostgreSQL local; no incluyen latencia de red ni CDN.
2. **Una sola base de datos compartida.** La suite corre en serie (`workers: 1`); no está
   preparada para paralelismo.
3. **Capturas solo en Chromium.** Firefox y WebKit omiten el caso de evidencias visuales.
4. **Sin pruebas de componentes.** La suite E2E no sustituye pruebas unitarias de React.
5. **Sin comparación visual (regresión de imágenes).** No se usa `toHaveScreenshot`; las
   capturas son evidencia, no una aserción visual.
6. **Sin auditoría de accesibilidad automatizada.** No se ejecutó axe ni otra herramienta
   dentro de la suite.
7. **Ejecución en CI verificada; despliegue pendiente.** La suite corrió en GitHub el
   19/11/2026, pero el despliegue a Producción sigue sin proveedor ni credenciales.
8. **LCP dependiente del navegador.** Si un motor no expone
   `largest-contentful-paint`, el caso lo reporta como `null` y no inventa un valor.

---

## 13. Conclusiones

- La aplicación es **funcional y estable en los tres motores**: 79 pruebas aprobadas, 0
  fallidas y 0 inestables sobre 81 ejecuciones.
- Los flujos de negocio críticos —login, pedidos, rutas, mapa, impacto, exportación y
  flota— están cubiertos con datos reales y limpieza posterior.
- La API responde con los códigos y cabeceras esperados, y la interfaz informa de los
  fallos de red y de servidor sin quedarse en blanco.
- El rendimiento local es holgadamente inferior a los umbrales de sanidad: TTFB de 3–12
  ms, FCP de 124–252 ms y LCP de 124–744 ms.
- Lo que falta es verificable y está declarado: despliegue a Producción, aplicación del
  SUS y pruebas de componentes. La ejecución real en GitHub quedó acreditada el
  19/11/2026 con la corrida `44560349236`.

---

[← Volver al README principal](../../../README.md)
