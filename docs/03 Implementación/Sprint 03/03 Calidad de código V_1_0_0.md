# Calidad de código

[← Volver al README principal](../../../README.md)

---

**Nombre del Proyecto:** EcoLogística Lima – Optimizador de Rutas Sostenibles para DistriRápido S.A.C.

**Líder del Proyecto:** Jhunior Harold Cosme Tenorio

**Sprint:** 3

**Periodo:** 02/11/2026 – 08/11/2026

**Fecha de verificación local:** 26/10/2026

---

## Control de Versiones del Documento

| Versión | Fecha | Autor | Descripción del Cambio |
|:---:|:---:|:---|:---|
| 1.0.0 | 08/11/2026 | Jhunior Harold Cosme Tenorio / Equipo EcoLogística | Informe de calidad de código del Sprint 3. |

---

## Objetivo y alcance

Este informe registra las métricas de calidad obtenidas de forma local sobre el código
del Sprint 3. No sustituye un Quality Gate de SonarQube ni una certificación externa.
Cuando una herramienta no se pudo ejecutar, se indica expresamente.

Alcance:

- `src/backend` — código de la API, servicios, modelos, esquemas y pruebas pytest.
- `src/frontend` — componentes React, lógica de `src/logica/**` y configuración de
  Vitest/Vite.
- `.github/workflows/` — configuración de CI/CD y CodeQL.
- `sonar-project.properties` — configuración preparada, sin ejecución.

---

## Resumen de métricas ejecutadas

| Métrica | Herramienta / comando | Resultado | Estado |
|:---|:---|:---|:---|
| Pruebas del backend | `python -m pytest -q --cov=app --cov-report=term-missing` | **64 aprobadas**, 0 fallidas | Ejecutado |
| Cobertura global del backend | `coverage report --precision=2` | **59.89 %** (880 sentencias, 353 sin cubrir) | Ejecutado |
| Cobertura del módulo nuevo US-008 | Reporte de cobertura | **100 %** (`app/services/exportacion.py`) | Ejecutado |
| Pruebas del frontend | `npm run coverage` | **16 aprobadas** en 2 archivos | Ejecutado |
| Cobertura del frontend | Vitest + `@vitest/coverage-v8` | **98.43 %** sentencias, **87.09 %** ramas, **100 %** funciones y líneas sobre `src/logica/**` | Ejecutado |
| Compilación de producción | `npm run build` | **Exitosa** con Vite 8.3.5 | Ejecutado |
| Dependencias del frontend | `npm audit --json` | **0 vulnerabilidades** en 106 dependencias | Ejecutado |
| Análisis estático Python | `ruff check .` | **109 hallazgos** de estilo/tipado | Ejecutado con hallazgos |
| Reglas críticas de Ruff | `ruff check app tests --select E9,F63,F7,F82` | **Sin hallazgos** | Ejecutado |
| Sintaxis de workflows | `yaml.safe_load` sobre los YAML | **Válida** | Ejecutado |
| SonarQube / SonarCloud | `sonar-scanner` | No ejecutado | **NO EJECUTADO** |
| CodeQL | `.github/workflows/codeql.yml` | Configurado, no ejecutado en GitHub | **NO EJECUTADO** |
| ESLint | — | No configurado en el repositorio | **NO DISPONIBLE** |

---

## Cobertura del backend por módulo

| Módulo | Cobertura | Lectura |
|:---|---:|:---|
| `app/services/exportacion.py` | 100 % | US-008 cubierto por pruebas unitarias. |
| `app/core/config.py` | 100 % | Validación de secretos y CORS. |
| `app/core/security.py` | 100 % | Hash y JWT. |
| `app/models/__init__.py` | 100 % | Modelos SQLAlchemy. |
| `app/schemas/__init__.py` | 100 % | Validación Pydantic. |
| `app/api/v1/endpoints/salud.py` | 100 % | Health check. |
| `app/api/v1/router.py` | 100 % | Registro de rutas. |
| `app/services/optimizer/__init__.py` | 82 % | Motor de ruteo. |
| `app/main.py` | 59 % | Arranque, CORS y cabeceras. |
| `app/core/database.py` | 62 % | Conexión y sesión. |
| `app/api/v1/endpoints/rutas.py` | 30 % | Requiere pruebas de integración con PostgreSQL. |
| `app/api/v1/endpoints/puntos.py` | 37 % | Requiere pruebas de integración con PostgreSQL. |
| `app/api/v1/endpoints/dependencies.py` | 35 % | Dependencias de autenticación. |
| `app/api/v1/endpoints/auth.py` | 47 % | Login y registro. |
| `app/api/v1/endpoints/geocoding.py` | 25 % | Dependencia externa de mapas. |
| `app/api/v1/endpoints/vehiculos.py` | 54 % | Consulta de vehículos. |

La cobertura global es **59.89 %**, inferior al objetivo de 70 % del `SPECS.md`. La
brecha no está en el código nuevo del Sprint 3, sino en los endpoints que dependen de
una base de datos y que no se ejercitan en las pruebas unitarias.

---

## Cobertura del frontend

| Archivo | Sentencias | Ramas | Funciones | Líneas |
|:---|---:|---:|---:|---:|
| `src/logica/distancia.js` | 96.55 % | 87.50 % | 100 % | 100 % |
| `src/logica/exportar.js` | 100 % | 86.66 % | 100 % | 100 % |
| **Total `src/logica/**`** | **98.43 %** | **87.09 %** | **100 %** | **100 %** |

Las líneas sin cubrir corresponden a ramas defensivas de `distancia.js` (32-41) y al
manejo de un error que no devuelve un `Blob` en `exportar.js` (53-59).

**Limitación:** los componentes React (`MapView`, `MapPicker`, `SelectorPuntos`,
`Dashboard`, `RutasTab`, `Login`) no tienen pruebas automatizadas. La cobertura anterior
no debe interpretarse como cobertura de la interfaz.

---

## Análisis estático con Ruff

La ejecución completa de Ruff produjo **109 hallazgos**, todos de estilo, tipado o
convención:

| Regla | Cantidad | Naturaleza | Riesgo |
|:---|---:|:---|:---|
| `B008` | 45 | `Depends()` de FastAPI en valores por defecto | Convención del framework; no es un defecto funcional. |
| `UP006` | 22 | Anotaciones `List`/`Dict` en lugar de `list`/`dict` | Modernización de tipado. |
| `I001` | 17 | Imports sin ordenar | Estilo. |
| `UP045` | 9 | `Optional[X]` en lugar de `X | None` | Modernización de tipado. |
| `UP017` | 7 | `datetime.timezone.utc` en lugar de `datetime.UTC` | Modernización; no se aplicó para conservar compatibilidad con Python 3.10. |
| `UP035` | 5 | Imports de `typing` obsoletos | Modernización. |
| `C408` | 2 | `dict()` innecesario | Estilo. |
| `B017` | 1 | `pytest.raises(Exception)` genérico | Calidad de prueba. |
| `SIM102` | 1 | `if` anidable | Estilo. |

Se corrigieron los imports sin uso y el uso de `datetime.utcnow()` en el optimizador,
que generaba una advertencia de fecha sin zona horaria. Las reglas críticas
`E9` (errores de sintaxis), `F63` (comparaciones sospechosas), `F7` (errores de
estructura) y `F82` (nombres no definidos) no reportan hallazgos.

No se configuró ESLint ni Prettier. El `DoD` global los menciona, pero el repositorio no
tiene archivo de configuración ni dependencias instaladas para esas herramientas.

---

## Calidad del código nuevo del Sprint 3

| Elemento | Cobertura / verificación | Cumple DoD de 80 % |
|:---|:---|:---:|
| `exportacion.py` (US-008) | 100 % con 8 pruebas unitarias | Sí |
| Neutralización de fórmulas CSV | Pruebas específicas | Sí |
| Endpoint `/export` | Registro y autorización por revisión; sin prueba de integración con BD | Parcial |
| Popups de `MapView` (US-006) | Revisión de código; sin prueba de componente | No verificado |
| Configuración CI/CD (EN-03) | YAML válido; sin ejecución real | No verificado |

---

## Hallazgos y riesgos de calidad

| # | Hallazgo | Impacto | Acción |
|:---:|:---|:---|:---|
| 1 | Cobertura global del backend en 59.89 %. | No se alcanza el objetivo de 70 %. | ACT-S3-02 y ACT-S3-03. |
| 2 | Sin pruebas de componentes React. | Los popups de US-006 no tienen red de seguridad automatizada. | ACT-S3-04. |
| 3 | SonarQube no ejecutado. | No existe Quality Gate ni medición de deuda técnica. | ACT-S3-05. |
| 4 | ESLint/Prettier no configurados. | El análisis estático del frontend depende de Vitest y de revisión manual. | Evaluar en el siguiente ciclo. |
| 5 | 109 hallazgos de Ruff no bloqueantes. | Ruido en el análisis; no hay errores críticos. | Corregir por lotes en una tarea de mantenimiento. |
| 6 | Workflows no ejecutados en GitHub. | La configuración es válida, pero no hay evidencia de una corrida real. | ACT-S3-01. |

---

## Conclusión

El código del Sprint 3 es funcional y verificable en sus módulos nuevos: las 64 pruebas
del backend y las 16 del frontend pasan, el build de producción compila y el módulo de
exportación tiene cobertura completa. Sin embargo, **la calidad no se declara
certificada**: la cobertura global del backend está por debajo del objetivo, la interfaz
no tiene pruebas de componentes, SonarQube no se ejecutó y el pipeline no se ha
ejecutado en GitHub. Esas brechas quedan registradas con acciones concretas en la
retrospectiva.

---

[← Volver al README principal](../../../README.md)
