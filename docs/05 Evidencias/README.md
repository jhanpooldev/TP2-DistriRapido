[← Volver al README Principal](../../README.md)

# Repositorio de Evidencias y Resultados de Validación

Carpeta destinada al resguardo de evidencias técnicas, resultados de corridas de verificación, auditorías y recursos de validación del sistema **EcoLogística Lima — DistriRápido S.A.C.**

## Control de Versiones del Documento

| Versión | Fecha | Autor | Descripción del Cambio |
|:---:|:---:|:---|:---|
| 1.0.0 | 01/11/2026 | Jhunior Harold Cosme Tenorio / Equipo EcoLogística | Inventario inicial de evidencias del Sprint 2. |
| 1.1.0 | 26/10/2026 | Jhunior Harold Cosme Tenorio / Equipo EcoLogística | Se agregan las cifras del Sprint 3 (65 pytest, 24 Vitest, 60.82 % backend), la reejecución de auditoría y smoke test, y la evidencia real de SonarQube en `sonar-sprint3/`. |

---

## 1. Evidencias de Pruebas Automatizadas y Auditoría de API

Las suites automatizadas y scripts de verificación residen junto al código en `src/backend` para garantizar repetibilidad:

| Tipo de Evidencia | Herramienta / Suite | Ubicación | Estado |
|---|---|---|---|
| **Pruebas Unitarias e Integración (backend)** | pytest (65 pruebas) | `src/backend/tests/` | **65/65 exitosas** sobre base de prueba hermética |
| **Cobertura del backend** | pytest-cov | `src/backend/coverage.xml` | **60.82 %** global (883 sentencias, 346 sin cubrir) |
| **Pruebas de lógica (frontend)** | Vitest (24 pruebas, 3 archivos) | `src/frontend/src/**/*.test.js` | **24/24 exitosas**; 93.22 % sentencias sobre `src/logica/**` |
| **Auditoría de Endpoints y Aislamiento** | Script `auditoria_api.py` | `src/backend/auditoria_api.py` | **SIN ANOMALÍAS** el 26/10/2026 sobre PostgreSQL 18 local |
| **Smoke Test End-to-End** | Script `smoke_sprint2.py` | `src/backend/smoke_sprint2.py` | **TODO OK** el 26/10/2026 sobre PostgreSQL 18 local |
| **Compilación Frontend** | Vite Build (`npm run build`) | `src/frontend/` | **Compilación exitosa** con Vite 8.3.5; 83 módulos |
| **Dependencias del frontend** | `npm audit --json` | `src/frontend/` | **0 vulnerabilidades** en 106 dependencias |
| **Integración continua** | GitHub Actions + CodeQL | `.github/workflows/` | Configurada y validada por sintaxis; **no ejecutada en GitHub** desde este entorno |

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

---

## 2. Entregables de Revisión y Validación por Sprint

Los informes de avance, impedimentos, revisiones y retrospectivas se organizan en sus respectivas carpetas por sprint:

- **Sprint 1 (05/10/2026 – 18/10/2026):** [`docs/03 Implementación/Sprint 1/`](../03%20Implementación/Sprint%201/)
  - Informe de estado del proyecto
  - Registro de impedimentos
  - Revisión del sprint
  - Retrospectiva del sprint
- **Sprint 2 (19/10/2026 – 01/11/2026):** [`docs/03 Implementación/Sprint 2/`](../03%20Implementación/Sprint%202/)
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

El Sprint 3 cerró **US-006** y **US-008**. **EN-03** quedó parcial: el pipeline de
integración continua está configurado, pero el despliegue en Staging no se realizó
porque no existe un host ni credenciales para ese ambiente.

---

## 3. Guía para Incorporar Nuevas Evidencias

- **Capturas de Pantalla:** Guardar las capturas en `img/` dentro del sprint correspondiente o en `docs/05 Evidencias/` si son de carácter global, recortadas exclusivamente al área de interés.
- **Reportes de Cobertura y Rendimiento:** `pytest-cov` genera `src/backend/coverage.xml` y Vitest genera `src/frontend/coverage/`; ambos son artefactos generados y están excluidos por `.gitignore`. Para conservar una evidencia, copiar el reporte con la nomenclatura `coverage-sprint-X.xml` o `coverage-sprint-X.json`.
- **Diagramas Exportados:** Formatos PNG, SVG o PDF de diagramas C4 o de base de datos para presentaciones ejecutivas.
