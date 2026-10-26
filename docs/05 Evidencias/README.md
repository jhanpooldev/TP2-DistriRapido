[← Volver al README Principal](../../README.md)

# Repositorio de Evidencias y Resultados de Validación

Carpeta destinada al resguardo de evidencias técnicas, resultados de corridas de verificación, auditorías y recursos de validación del sistema **EcoLogística Lima — DistriRápido S.A.C.**

---

## 1. Evidencias de Pruebas Automatizadas y Auditoría de API

Las suites automatizadas y scripts de verificación residen junto al código en `src/backend` para garantizar repetibilidad:

| Tipo de Evidencia | Herramienta / Suite | Ubicación | Estado |
|---|---|---|---|
| **Pruebas Unitarias e Integración** | pytest (51 pruebas) | `src/backend/tests/` | **51/51 exitosas** sobre base de prueba hermética |
| **Auditoría de Endpoints y Aislamiento** | Script `auditoria_api.py` | `src/backend/auditoria_api.py` | **100% verificado**: validación de RBAC, aislamiento por operador y respuestas HTTP |
| **Smoke Test End-to-End** | Script `smoke_sprint2.py` | `src/backend/smoke_sprint2.py` | **100% verificado**: flujo completo de login, puntos, ruteo y métricas |
| **Compilación Frontend** | Vite Build (`npm run build`) | `src/frontend/` | **Compilación exitosa** sin advertencias ni errores |

> Ejecución de las suites de validación (con el backend levantado):
> ```bash
> cd src/backend
> python -m pytest
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

---

## 3. Guía para Incorporar Nuevas Evidencias

- **Capturas de Pantalla:** Guardar las capturas en `img/` dentro del sprint correspondiente o en `docs/05 Evidencias/` si son de carácter global, recortadas exclusivamente al área de interés.
- **Reportes de Cobertura y Rendimiento:** Cuando se integre `pytest-cov`, depositar el reporte HTML/JSON en esta ubicación con la nomenclatura `coverage-sprint-X.json`.
- **Diagramas Exportados:** Formatos PNG, SVG o PDF de diagramas C4 o de base de datos para presentaciones ejecutivas.
