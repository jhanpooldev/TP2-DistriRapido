[← Volver al README Principal](../../README.md)

# Repositorio de Evidencias y Resultados de Validación

Carpeta destinada al resguardo de evidencias técnicas, resultados de corridas de verificación, auditorías y recursos de validación del sistema **EcoLogística Lima — DistriRápido S.A.C.**

## Control de Versiones del Documento

| Versión | Fecha | Autor | Descripción del Cambio |
|:---:|:---:|:---|:---|
| 1.0.0 | 19/10/2026 | Jhunior Harold Cosme Tenorio / Equipo EcoLogística | Inventario inicial de evidencias del Sprint 2. |
| 1.1.0 | 08/11/2026 | Jhunior Harold Cosme Tenorio / Equipo EcoLogística | Se agregan las cifras del Sprint 3 (65 pytest, 24 Vitest, 60.82 % backend), la reejecución de auditoría y smoke test, y la evidencia real de SonarQube en `sonar-sprint3/`. |
| 1.2.0 | 17/11/2026 | Jhunior Harold Cosme Tenorio / Equipo EcoLogística | Se agregan las cifras del Sprint 4 (66 pytest, 24 Vitest, 79 E2E), las métricas de rendimiento por navegador y las capturas de `playwright-sprint4/`. |
| 1.3.0 | 23/11/2026 | Equipo EcoLogística | Se agrega la auditoría documentación vs. código: 103 pytest / 73 %, 32 Vitest / 93,07 % y build de 87 módulos; se conservan las corridas históricas como registro. |

---

## 1. Evidencias de Pruebas Automatizadas y Auditoría de API

Las suites automatizadas y scripts de verificación residen junto al código en `src/backend` para garantizar repetibilidad:

| Tipo de Evidencia | Herramienta / Suite | Ubicación | Estado |
|---|---|---|---|
| **Pruebas Unitarias e Integración (backend)** | pytest (66 pruebas) | `src/backend/tests/` | **66/66 exitosas** sobre base de prueba hermética |
| **Cobertura del backend** | pytest-cov | `src/backend/coverage.xml` | **61 %** global (1 030 sentencias, 399 sin cubrir) |
| **Pruebas de lógica (frontend)** | Vitest (24 pruebas, 3 archivos) | `src/frontend/src/**/*.test.js` | **24/24 exitosas**; 93.22 % sentencias sobre `src/logica/**` |
| **Pruebas E2E (Sprint 4)** | Playwright 1.65.1 (Chromium, Firefox y WebKit) | `src/frontend/e2e/` | **79 aprobadas, 2 omitidas, 0 fallidas** el 17/11/2026 |
| **Métricas de rendimiento E2E** | Performance API + Playwright | `docs/05 Evidencias/playwright-sprint4/performance-*.json` | TTFB 3–12 ms, FCP 124–252 ms, LCP 124–744 ms |
| **Capturas E2E** | Playwright (solo Chromium) | `docs/05 Evidencias/playwright-sprint4/*.png` | **7 capturas** de login, panel, rutas, mapa, impacto y vehículos |
| **Auditoría de Endpoints y Aislamiento** | Script `auditoria_api.py` | `src/backend/auditoria_api.py` | **SIN ANOMALÍAS** el 26/10/2026 sobre PostgreSQL 18 local |
| **Smoke Test End-to-End** | Script `smoke_sprint2.py` | `src/backend/smoke_sprint2.py` | **TODO OK** el 26/10/2026 sobre PostgreSQL 18 local |
| **Compilación Frontend** | Vite Build (`npm run build`) | `src/frontend/` | **Compilación exitosa** con Vite 8.3.5; 85 módulos |
| **Dependencias del frontend** | `npm audit --json` | `src/frontend/` | **0 vulnerabilidades** tras actualizar `follow-redirects` a 1.16.3 (19/11/2026) |
| **Integración continua** | GitHub Actions + CodeQL | `.github/workflows/` | **Ejecutada en GitHub el 19/11/2026**; ver sección 1.3 |
| **Auditoría documentación vs. código (23/11/2026)** | pytest + Vitest + Vite build | `docs/02 Planificación/11 Matriz de Trazabilidad V_1_0_0.md` | **103/103 backend** (73 % de cobertura), **32/32 frontend** (93,07 % instrumentado) y **build de 87 módulos**. E2E no reejecutadas: sin Docker/PostgreSQL local. |

> Ejecución de las suites de validación:
> ```bash
> # Backend: pruebas y cobertura
> cd src/backend
> python -m pytest -q --cov=app --cov-report=term-missing --cov-report=xml
>
> # Frontend: pruebas, cobertura y build
> cd ../frontend
> npm run coverage
> npm run build
>
> # Auditoría y smoke test (requieren PostgreSQL y el backend levantado)
> cd ../backend
> python auditoria_api.py 8099
> python smoke_sprint2.py 8099
> ```

### 1.1 Evidencias del análisis SonarQube (Sprint 3)

El 26/10/2026 se ejecutó **SonarQube Community** en un contenedor Docker local y
**SonarScanner CLI** sobre el repositorio. Las respuestas crudas de la API se conservan
en la carpeta [`sonar-sprint3/`](sonar-sprint3/):

| Archivo | Contenido | Resultado registrado |
|---|---|---|
| [`measures.json`](sonar-sprint3/measures.json) | Métricas del proyecto | 0 bugs, 0 vulnerabilidades, 0 code smells, 0 hotspots, deuda 0 min, cobertura 9.8 %, duplicación 1.4 % |
| [`quality-gate.json`](sonar-sprint3/quality-gate.json) | Estado del Quality Gate | **OK** con `ignoredConditions: true` (primer análisis, sin versión anterior) |
| [`issues.json`](sonar-sprint3/issues.json) | Incidencias abiertas | **0 incidencias** después de la remediación |

La primera corrida detectó 5 bugs y 2 code smells; se corrigieron en el código y se
volvió a analizar. El detalle de cada corrección está en
[`03 Calidad de código`](../03%20Implementación/Sprint%2003/03%20Calidad%20de%20código%20V_1_0_0.md)
y en [`04 OWASP`](../03%20Implementación/Sprint%2003/04%20OWASP%20V_1_0_0.md).

> **Reproducción:** el servidor se levanta con
> `docker run -d --name sonarqube -p 9000:9000 sonarqube:community`; el análisis se
> ejecuta con `sonarsource/sonar-scanner-cli` usando un token de SonarQube. El
> contenedor y el token son locales y no se versionan.

### 1.2 Evidencias de Playwright (Sprint 4)

El 17/11/2026 se ejecutó la suite E2E completa sobre Chromium, Firefox y WebKit. Las
evidencias seleccionadas están en [`playwright-sprint4/`](playwright-sprint4/):

| Archivo | Contenido | Resultado registrado |
|---|---|---|
| [`resultados.json`](playwright-sprint4/resultados.json) | Reporte JSON completo | 79 aprobadas, 2 omitidas, 0 fallidas, 105,1 s |
| [`performance-chromium.json`](playwright-sprint4/performance-chromium.json) | Navegación y API en Chromium | TTFB 4–12 ms; FCP 124–252 ms; LCP 124–744 ms |
| [`performance-firefox.json`](playwright-sprint4/performance-firefox.json) | Navegación y API en Firefox | TTFB 5–7 ms; FCP 125–219 ms; LCP 125–708 ms |
| [`performance-webkit.json`](playwright-sprint4/performance-webkit.json) | Navegación y API en WebKit | TTFB 3 ms; FCP 156–203 ms; LCP 156–664 ms |
| `01-login.png` … `07-panel-vehiculos-administrador.png` | Capturas de las pantallas principales | Generadas solo en Chromium |

El detalle metodológico está en
[`03 Analisis PlayWrigth`](../03%20Implementación/Sprint%2004/03%20Analisis%20PlayWrigth%20V_1_0_0.md)
y el índice de la carpeta en
[`playwright-sprint4/README.md`](playwright-sprint4/README.md).

> El reporte HTML completo (`playwright-report/`) no se versiona; se regenera con
> `npm run test:e2e` y el workflow `tests.yml` lo publica como artefacto.

### 1.3 Evidencias de CI/CD (Sprint 4)

El 19/11/2026 se publicó el commit `85eac48` en `main` y se ejecutaron los workflows del
repositorio:

| Workflow | Run | Resultado | Artefactos |
|---|---:|---|---|
| **Tests** | `44560349236` | **Success** (backend, frontend y E2E) | `playwright-report`, `playwright-results`, `playwright-evidencias`, `backend-coverage`, `frontend-coverage` |
| **CI** | `44560349613` | **Success** | `frontend-build` |
| **CodeQL** | `44560349282` | **Success** | — |
| **Green Audit** | `44560349327` | **Success** | Publicación configurada; la API no listó el artefacto en esa corrida |
| **Deploy Staging** | `44561128925` | **Skipped** | — (sin host ni credenciales) |
| **Deploy Production** | `44561129181` | **Skipped** | — (sin proveedor ni credenciales) |

Los detalles de la corrida de Tests están en el job
`E2E - Playwright en Chromium, Firefox y WebKit` (15:56:00–16:00:07Z). Los logs no se
pueden leer sin autenticación, pero la conclusión de cada job y los artefactos publicados
son verificables en la API pública de GitHub.

---

## 2. Entregables de Revisión y Validación por Sprint

Los informes de avance, impedimentos, revisiones y retrospectivas se organizan en sus respectivas carpetas por sprint:

- **Sprint 1 (05/10/2026 – 18/10/2026):** [`docs/03 Implementación/Sprint 01/`](../03%20Implementación/Sprint%2001/)
  - Informe de estado del proyecto
  - Registro de impedimentos
  - Revisión del sprint
  - Retrospectiva del sprint
- **Sprint 2 (19/10/2026 – 01/11/2026):** [`docs/03 Implementación/Sprint 02/`](../03%20Implementación/Sprint%2002/)
  - Informe de estado del proyecto
  - Registro de impedimentos
  - Revisión del sprint
  - Retrospectiva del sprint
- **Sprint 3 (02/11/2026 – 08/11/2026):** [`docs/03 Implementación/Sprint 03/`](../03%20Implementación/Sprint%2003/)
  - [Revisión del Sprint V_1_0_0](../03%20Implementación/Sprint%2003/01%20Revisión%20del%20Sprint%20V_1_0_0.md)
  - [Retrospectiva del Sprint V_1_0_0](../03%20Implementación/Sprint%2003/02%20Retrospectiva%20del%20Sprint%20V_1_0_0.md)
  - [Calidad de código V_1_0_0](../03%20Implementación/Sprint%2003/03%20Calidad%20de%20código%20V_1_0_0.md)
  - [OWASP V_1_0_0](../03%20Implementación/Sprint%2003/04%20OWASP%20V_1_0_0.md)
  - [WCAG V_1_0_0](../03%20Implementación/Sprint%2003/05%20WCAG%20V_1_0_0.md)
- **Sprint 4 (09/11/2026 – 17/11/2026):** [`docs/03 Implementación/Sprint 04/`](../03%20Implementación/Sprint%2004/)
  - [Revisión del Sprint V_1_0_0](../03%20Implementación/Sprint%2004/01%20Revisión%20del%20Sprint%20V_1_0_0.md)
  - [Retrospectiva del Sprint V_1_0_0](../03%20Implementación/Sprint%2004/02%20Retrospectiva%20del%20Sprint%20V_1_0_0.md)
  - [Análisis de Playwright V_1_0_0](../03%20Implementación/Sprint%2004/03%20Analisis%20PlayWrigth%20V_1_0_0.md)
  - [Usabilidad SUS V_1_0_0](../03%20Implementación/Sprint%2004/04%20Usabilidad%20V_1_0_0.md)

El Sprint 3 cerró **US-006** y **US-008**. **EN-03** quedó parcial: el pipeline de
integración continua está configurado, pero el despliegue en Staging no se realizó
porque no existe un host ni credenciales para ese ambiente.

El Sprint 4 no agregó historias de negocio: consolidó la calidad con la suite E2E, las
métricas de rendimiento y los workflows de CI/CD. El **SUS quedó preparado pero no
aplicado** y el **despliegue a Producción no está configurado**; ambas brechas se
declaran en los documentos del sprint. Los workflows de CI, Tests, CodeQL y Green Audit
**se ejecutaron en verde el 19/11/2026**; los deploys de Staging y Producción quedaron
omitidos por falta de host y credenciales.

---

## 3. Guía para Incorporar Nuevas Evidencias

- **Capturas de Pantalla:** Guardar las capturas en `img/` dentro del sprint correspondiente o en `docs/05 Evidencias/` si son de carácter global, recortadas exclusivamente al área de interés.
- **Reportes de Cobertura y Rendimiento:** `pytest-cov` genera `src/backend/coverage.xml` y Vitest genera `src/frontend/coverage/`; ambos son artefactos generados y están excluidos por `.gitignore`. Para conservar una evidencia, copiar el reporte con la nomenclatura `coverage-sprint-X.xml` o `coverage-sprint-X.json`.
- **Reportes de Playwright:** `playwright-report/` y `test-results/` están excluidos por `.gitignore`. Para conservar una evidencia, copiar solo los JSON y capturas seleccionadas a `docs/05 Evidencias/playwright-sprintX/`, como se hizo en el Sprint 4.
- **Diagramas Exportados:** Formatos PNG, SVG o PDF de diagramas C4 o de base de datos para presentaciones ejecutivas.
