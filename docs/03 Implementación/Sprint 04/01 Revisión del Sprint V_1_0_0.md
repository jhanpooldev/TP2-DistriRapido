# Revisión del sprint

[← Volver al README principal](../../../README.md)

---

**Nombre del Proyecto:** EcoLogística Lima – Optimizador de Rutas Sostenibles para DistriRápido S.A.C.

**Líder del Proyecto:** Jhunior Harold Cosme Tenorio

**Sprint:** 4

**Periodo:** 09/11/2026 – 17/11/2026

**Fecha de verificación local:** 17/11/2026

> El periodo se registra desde el cierre del Sprint 3 (08/11/2026) hasta la fecha de la
> verificación local (17/11/2026). **No se declara una fecha de aceptación formal del
> cliente** porque no se realizó una sesión de revisión con stakeholders; la demostración
> descrita en este documento es la verificación funcional ejecutada por el equipo.

---

## Control de Versiones del Documento

| Versión | Fecha | Autor | Descripción del Cambio |
|:---:|:---:|:---|:---|
| 1.0.0 | 17/11/2026 | Jhunior Harold Cosme Tenorio / Equipo EcoLogística | Acta de Revisión del Sprint 4 con la suite E2E, las métricas de rendimiento, el instrumento SUS y los workflows de CI/CD. |

---

## Alcance comprometido

El Sprint 4 es un **sprint de consolidación de calidad**, no de funcionalidad de negocio.
No incorpora historias de usuario nuevas del backlog: el PMV ya quedó cerrado en el
Sprint 3 con US-001 a US-008 y EN-01 a EN-03. El trabajo se organizó como entregables
técnicos internos.

> Los identificadores `ET-S4-xx` son **etiquetas internas de trabajo de este sprint**.
> No son códigos de historia de usuario del backlog y no deben interpretarse como
> US-009 o similares.

| ID interno | Entregable | Tipo | Estado |
|---|---|---|---|
| ET-S4-01 | Suite E2E con Playwright en Chromium, Firefox y WebKit | Pruebas | Completado |
| ET-S4-02 | Métricas de rendimiento y pruebas de resiliencia HTTP | Pruebas | Completado |
| ET-S4-03 | Instrumento de usabilidad SUS | Usabilidad | **Preparado, no aplicado** |
| ET-S4-04 | Workflows de CI, pruebas y despliegue a Producción | CI/CD | **Implementado, no ejecutado en GitHub** |
| ET-S4-05 | Limpieza del repositorio y exclusión de artefactos | Mantenimiento | Completado |
| ET-S4-06 | Documentación del Sprint 4 y navegación del README | Documentación | Completado |

**Resultado:** cuatro entregables completados y dos con alcance parcial honestamente
declarado (SUS sin respuestas reales y despliegue a Producción sin proveedor
configurado). No se declara terminado nada que no haya sido ejecutado o verificado.

---

## Entregables completados

### ET-S4-01 — Suite E2E con Playwright

Se incorporó una suite de pruebas de extremo a extremo que ejercita la aplicación real
—frontend Vite y backend FastAPI— sobre una base PostgreSQL local.

| Archivo | Casos | Propósito |
|---|---:|---|
| `src/frontend/e2e/auth.spec.js` | 7 | Login válido e inválido, validación de campos, visibilidad de las cinco secciones, rol Administrador frente a Operador y cierre de sesión. |
| `src/frontend/e2e/flujo-principal.spec.js` | 7 | Registro de pedidos, validación de formulario, cálculo y guardado de ruta, exportación CSV, bloqueo con un solo pedido, filtro sin resultados, edición y eliminación. |
| `src/frontend/e2e/resiliencia.spec.js` | 11 | Salud, 401 sin token, 401 con token inválido, 422 de coordenadas, 400 con un solo punto, 404 de ruta inexistente, 400 de placa duplicada, cabeceras de endurecimiento, caché y errores de red/500 en la interfaz. |
| `src/frontend/e2e/rendimiento.spec.js` | 1 | Medición de TTFB, FCP, LCP, `DOMContentLoaded`, `load` y tiempos de los endpoints principales. |
| `src/frontend/e2e/evidencias.spec.js` | 1 | Generación de capturas reales de las pantallas principales (solo Chromium). |

Cada caso se ejecuta en los tres proyectos configurados, salvo las capturas, que se
omiten en Firefox y WebKit. La configuración está en
[`src/frontend/playwright.config.js`](../../../src/frontend/playwright.config.js) y
los ayudantes compartidos en
[`src/frontend/e2e/utils.js`](../../../src/frontend/e2e/utils.js).

**Resultado real de la corrida del 17/11/2026:**

| Indicador | Valor |
|---|---:|
| Casos por navegador | 27 |
| Ejecuciones totales | 81 |
| Aprobadas | **79** |
| Omitidas | **2** (capturas en Firefox y WebKit) |
| Fallidas | **0** |
| Inestables (*flaky*) | **0** |
| Duración total | 105,1 s |
| Navegadores | Chromium 159, Firefox 159, WebKit 27.2 |

El reporte crudo está en
[`docs/05 Evidencias/playwright-sprint4/resultados.json`](../../05%20Evidencias/playwright-sprint4/resultados.json)
y las capturas en la misma carpeta.

### ET-S4-02 — Rendimiento y resiliencia

La medición de rendimiento usa la **Performance API del navegador**, no una estimación:
`responseStart` para TTFB, `first-contentful-paint` para FCP y
`largest-contentful-paint` para LCP. Las peticiones a la API se cronometran con
`Date.now()` alrededor de cada llamada. Todas las cifras se capturaron en local el
17/11/2026, con viewport de 1280 × 720 y el servidor de desarrollo de Vite.

| Métrica de navegación | Chromium | Firefox | WebKit |
|---|---:|---:|---:|
| Login — TTFB | 4 ms | 7 ms | 3 ms |
| Login — FCP | 124 ms | 125 ms | 156 ms |
| Login — LCP | 124 ms | 125 ms | 156 ms |
| Panel — TTFB | 12 ms | 5 ms | 3 ms |
| Panel — FCP | 252 ms | 219 ms | 203 ms |
| Panel — LCP | 744 ms | 708 ms | 664 ms |

| Endpoint | Chromium | Firefox | WebKit |
|---|---:|---:|---:|
| `GET /health` | 7 ms | 7 ms | 5 ms |
| `POST /auth/login` | 213 ms | 229 ms | 216 ms |
| `GET /puntos-entrega` | 11 ms | 9 ms | 11 ms |
| `GET /rutas` | 13 ms | 13 ms | 12 ms |
| `GET /vehiculos` | 7 ms | 7 ms | 7 ms |

Las pruebas de resiliencia comprueban códigos y cabeceras reales de la API, además del
comportamiento de la interfaz cuando el backend no responde o devuelve un error 500.
El detalle metodológico y los límites están en
[`03 Analisis PlayWrigth V_1_0_0.md`](03%20Analisis%20PlayWrigth%20V_1_0_0.md).

### ET-S4-03 — Instrumento SUS (preparado, no aplicado)

Se elaboró el cuestionario **System Usability Scale (SUS)** en español, con sus diez
ítems, escala Likert de cinco puntos, fórmula de puntuación, protocolo de aplicación y
plantilla de registro. **No se aplicó a participantes reales y no existen resultados que
reportar.** No se inventan puntajes, participantes ni comentarios.

El instrumento completo está en
[`04 Usabilidad V_1_0_0.md`](04%20Usabilidad%20V_1_0_0.md). Su aplicación queda como
pendiente del sprint y requiere personas reales.

### ET-S4-04 — Workflows de CI/CD

| Archivo | Función | Estado real |
|---|---|---|
| `.github/workflows/ci.yml` | Validación de dependencias, Ruff mínimo, compilación e importación del backend; `npm ci` y build del frontend. | Implementado y validado por sintaxis YAML. |
| `.github/workflows/tests.yml` | pytest con cobertura, Vitest con cobertura y Playwright en tres navegadores, con publicación de artefactos. | Implementado y validado por sintaxis YAML; **no ejecutado en GitHub desde este entorno**. |
| `.github/workflows/deploy-production.yml` | Despliegue a Producción por *deploy hook*, con verificación de salud y activación explícita. | Implementado y **desactivado por defecto**; sin proveedor, URL ni secretos configurados. |
| `.github/workflows/deploy-staging.yml` | Despliegue a Staging existente. | Se cambió su disparador de `CI` a `Tests`; sigue desactivado por defecto. |

Ningún workflow usa credenciales en el código: el despliegue depende de
`PRODUCTION_DEPLOY_ENABLED`, `PRODUCTION_DEPLOY_HOOK`, `PRODUCTION_HEALTH_URL` y sus
equivalentes de Staging, definidos como *secrets* o *variables* del repositorio.

**Limitación declarada:** los workflows se validaron con `yaml.safe_load`, pero no se
ejecutaron en GitHub porque no se realizó `push` ni se dispone de acceso a las
ejecuciones del repositorio. Por tanto **no se afirma que existan corridas en verde**.

### ET-S4-05 — Limpieza del repositorio

- `.gitignore` excluye `playwright-report/`, `test-results/`, `blob-report/`,
  `playwright/.cache/` y `playwright/.auth/`, además de las reglas previas para
  `node_modules/`, `.env`, `dist/`, `build/`, cachés de Python, archivos de sistema y de
  editor.
- No existe ningún archivo `.gitignore~`.
- Las evidencias seleccionadas se copiaron a
  `docs/05 Evidencias/playwright-sprint4/`; el reporte HTML completo permanece ignorado
  por Git y se conserva como artefacto del workflow de pruebas.

### ET-S4-06 — Documentación y navegación

- Cuatro entregables Markdown en `docs/03 Implementación/Sprint 4/`.
- Enlaces directos desde el README principal y desde el índice de evidencias.
- Badges de GitHub Actions apuntando a los workflows reales del repositorio.
- `CHANGELOG.md` actualizado con los cambios del sprint.

---

## Criterios de aceptación verificados

| Elemento | Criterio | Resultado | Evidencia |
|---|---|---|---|
| ET-S4-01 | La suite corre en Chromium, Firefox y WebKit en modo *headless*. | **Cumplido.** 79 aprobadas y 2 omitidas sobre 81 ejecuciones. | `resultados.json`; `playwright.config.js`. |
| ET-S4-01 | Cubre flujos de negocio reales, no solo el login. | **Cumplido.** Pedidos, rutas, mapa, impacto, vehículos, exportación, edición y eliminación. | `flujo-principal.spec.js`; capturas 02–07. |
| ET-S4-01 | Genera reporte HTML y artefactos. | **Cumplido.** Reporte HTML local y publicación como artefacto en `tests.yml`. | `playwright.config.js`; `.github/workflows/tests.yml`. |
| ET-S4-02 | Mide TTFB, FCP, LCP y tiempos de API. | **Cumplido.** Valores reales en los tres navegadores. | `performance-*.json`. |
| ET-S4-02 | Verifica respuestas HTTP y resiliencia. | **Cumplido.** 401, 400, 404, 422, cabeceras, caché y errores de interfaz. | `resiliencia.spec.js`. |
| ET-S4-03 | Instrumento SUS listo para aplicar. | **Cumplido.** Cuestionario, fórmula y protocolo. | `04 Usabilidad V_1_0_0.md`. |
| ET-S4-03 | Resultados SUS con participantes reales. | **No cumplido.** No se aplicó la encuesta. | Declarado como pendiente. |
| ET-S4-04 | Tres workflows con secretos, sin credenciales duras. | **Cumplido.** `ci.yml`, `tests.yml`, `deploy-production.yml`. | Archivos YAML validados. |
| ET-S4-04 | Ejecución real en GitHub y despliegue a Producción. | **No cumplido.** Sin `push`, sin proveedor y sin URL. | Declarado como pendiente. |
| ET-S4-05 | Artefactos de Playwright fuera de Git. | **Cumplido.** Verificado con `git check-ignore`. | `.gitignore`. |
| ET-S4-06 | Enlaces de retorno y navegación. | **Cumplido.** Cada documento enlaza al README principal. | Este documento y los otros tres. |

---

## Verificación ejecutada

Todas las cifras provienen de comandos ejecutados el 17/11/2026 en el entorno local.

| Verificación | Comando | Resultado |
|---|---|---|
| Pruebas del backend | `python -m pytest -q --cov=app --cov-report=term` | **66 aprobadas**, 0 fallidas. |
| Cobertura del backend | Reporte de `pytest-cov` | **61 %** global (1 030 sentencias, 399 sin cubrir). |
| Pruebas del frontend | `npm test` (Vitest) | **24 aprobadas** en 3 archivos. |
| Compilación del frontend | `npm run build` | **Exitosa** con Vite 8.3.5. |
| Suite E2E | `npm run test:e2e` | **79 aprobadas, 2 omitidas, 0 fallidas** en 105,1 s. |
| Navegadores E2E | Chromium, Firefox y WebKit | Los tres ejecutaron la suite. |
| Sintaxis YAML | `yaml.safe_load` sobre `.github/workflows/*.yml` | **Válida** en los seis workflows. |
| Exclusión de artefactos | `git check-ignore -v` | `playwright-report/`, `test-results/` y `node_modules/` ignorados. |
| Enlaces relativos | Revisión de rutas Markdown | **Verificados** (ver nota de la sección final). |

> La cobertura del backend subió de 60.82 % (Sprint 3) a **61 %** porque la suite creció
> a 66 pruebas y se modificó código del panel y de vehículos. Sigue por debajo del
> objetivo de 70 % del `SPECS.md`; no se presenta como cumplido.

---

## Demostración del trabajo completado

La suite es reproducible con la base PostgreSQL local y las dependencias instaladas:

```bash
cd src/frontend
npm run test:e2e            # Chromium, Firefox y WebKit
npm run test:e2e:report     # Abre el reporte HTML local
```

Recorrido funcional que cubre la suite:

1. Abrir el login y validar los campos obligatorios y las credenciales incorrectas.
2. Iniciar sesión como Operador y comprobar las cinco secciones del panel.
3. Registrar un pedido desde la interfaz y verlo en la tabla.
4. Seleccionar dos pedidos, calcular la ruta, guardarla y exportar el CSV.
5. Abrir la ruta en el mapa y revisar el detalle de cada parada.
6. Consultar el impacto ambiental y la flota de vehículos.
7. Iniciar sesión como Administrador y comprobar el formulario de alta de vehículos.
8. Ejecutar los casos de resiliencia: 401, 400, 404, 422, cabeceras, caché y caída de red.
9. Revisar las capturas en `docs/05 Evidencias/playwright-sprint4/`.

---

## Pendientes y limitaciones

1. **SUS sin resultados reales.** No se aplicó el cuestionario; no hay puntaje ni
   participantes que reportar. Ver [`04 Usabilidad V_1_0_0.md`](04%20Usabilidad%20V_1_0_0.md).
2. **GitHub Actions no ejecutado.** Los workflows están escritos y su sintaxis validada,
   pero no se ejecutaron en GitHub ni se verificaron corridas en verde.
3. **Despliegue a Producción no configurado.** No existe proveedor, URL ni secretos; el
   workflow está desactivado por defecto.
4. **Rendimiento medido en local.** Los tiempos corresponden al servidor de desarrollo
   de Vite y a PostgreSQL local; no representan un ambiente productivo ni una red real.
5. **Evidencia visual de Lighthouse ausente.** La carpeta `.lighthouseci/` no existe en
   el entorno local. El workflow `green-audit.yml` sí está configurado, pero no se
   ejecutó en GitHub.
6. **Sin pruebas de componentes React.** La suite E2E cubre flujos completos, pero sigue
   sin haber pruebas unitarias de componentes ni de los popups del mapa.
7. **Las capturas se generan solo en Chromium.** Firefox y WebKit omiten ese caso para
   no duplicar imágenes equivalentes.
8. **La suite comparte una sola base de datos.** Se ejecuta en serie (`workers: 1`) para
   evitar interferencias; no está preparada para ejecución paralela.

---

[← Volver al README principal](../../../README.md)
