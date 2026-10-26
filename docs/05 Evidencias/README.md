[← Volver al README Principal](../../README.md)

# Repositorio de Evidencias y Resultados de Validación

Carpeta destinada al resguardo de evidencias técnicas, resultados de corridas de verificación, auditorías y recursos de validación del sistema **EcoLogística Lima — DistriRápido S.A.C.**

---

## 1. Evidencias de Pruebas Automatizadas y Auditoría de API

Las suites automatizadas y scripts de verificación residen junto al código en `src/backend` para garantizar repetibilidad:

| Tipo de Evidencia | Herramienta / Suite | Ubicación | Estado |
|---|---|---|---|
| **Pruebas Unitarias e Integración (backend)** | pytest (64 pruebas) | `src/backend/tests/` | **64/64 exitosas** sobre base de prueba hermética |
| **Cobertura del backend** | pytest-cov | `src/backend/coverage.xml` | **59.89 %** global (880 sentencias, 353 sin cubrir) |
| **Pruebas de lógica (frontend)** | Vitest (16 pruebas, 2 archivos) | `src/frontend/src/**/*.test.js` | **16/16 exitosas**; 98.43 % sentencias sobre `src/logica/**` |
| **Auditoría de Endpoints y Aislamiento** | Script `auditoria_api.py` | `src/backend/auditoria_api.py` | Última ejecución satisfactoria en el Sprint 2; **no reejecutada en el Sprint 3** por ausencia de PostgreSQL local |
| **Smoke Test End-to-End** | Script `smoke_sprint2.py` | `src/backend/smoke_sprint2.py` | Última ejecución satisfactoria en el Sprint 2; **no reejecutada en el Sprint 3** por ausencia de PostgreSQL local |
| **Compilación Frontend** | Vite Build (`npm run build`) | `src/frontend/` | **Compilación exitosa** con Vite 8.3.5; 82 módulos |
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
