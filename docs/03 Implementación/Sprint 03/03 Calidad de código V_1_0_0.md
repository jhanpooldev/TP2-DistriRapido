# Evaluación de Calidad de Código — SonarQube

[← Volver al README principal](../../../README.md)

---

**Nombre del Proyecto:** EcoLogística Lima – Optimizador de Rutas Sostenibles para DistriRápido S.A.C.

**Fecha de Análisis:** 2026-10-26

**Versión del Análisis:** V_1_0_0 (revisión 1.1.0 del documento)

**Líder del Proyecto:** Jhunior Harold Cosme Tenorio

**Sprint:** 3 · **Periodo:** 02/11/2026 – 08/11/2026

**Herramienta:** SonarQube Community (contenedor Docker local) + SonarScanner CLI

---

## Control de Versiones del Documento

| Versión | Fecha | Autor | Descripción del Cambio |
|:---:|:---:|:---|:---|
| 1.0.0 | 26/10/2026 | Jhunior Harold Cosme Tenorio / Equipo EcoLogística | Informe de calidad de código del Sprint 3. |
| 1.1.0 | 26/10/2026 | Jhunior Harold Cosme Tenorio / Equipo EcoLogística | Se reemplazan las métricas estimadas por el análisis real de SonarQube y se documenta la remediación. |

---

## 1. Resumen Ejecutivo de Quality Gate

- **Estado del Quality Gate:** **PASSED (OK)**.
- **Porcentaje de Cobertura de Pruebas (Coverage):** **9.8 %** global según SonarQube.
  - Cobertura de líneas: **6.6 %**.
  - Cobertura de ramas: **85.2 %** sobre las líneas cubiertas.
  - Cobertura medida directamente: backend **60.82 %** (pytest-cov) y frontend lógico
    **93.22 %** de sentencias (Vitest/V8). La diferencia se explica en la sección 4.
- **Duplicación de Código:** **1.4 %** (66 líneas duplicadas en 4 bloques sobre
  3 886 líneas de código).

> **Lectura honesta del Quality Gate:** SonarQube devolvió `status = OK`, pero también
> `ignoredConditions = true` porque se trata del **primer análisis** del proyecto y no
> existe una versión anterior contra la cual evaluar las condiciones de código nuevo.
> Por tanto, el resultado se reporta como "Quality Gate OK con condiciones ignoradas",
> no como una certificación de calidad del 100 % del código.

---

## 2. Métricas Principales

| Categoría | Cantidad Detectada | Severidad (Bloqueante / Alta / Media / Baja) |
|:---|---:|:---|
| **Bugs** | **0** | Sin hallazgos abiertos (antes de la remediación: 5, todos de severidad Alta). |
| **Vulnerabilidades** | **0** | Sin hallazgos abiertos. |
| **Code Smells** | **0** | Sin hallazgos abiertos (antes: 2; uno Bloqueante y uno Alta). |
| **Security Hotspots** | **0** | Sin hotspots detectados; la tasa de revisión no aplica porque no hay elementos que revisar. |

**Calificaciones (ratings):**

| Dimensión | Rating | Escala |
|:---|:---:|:---|
| Fiabilidad (Reliability) | **A** | 1.0 |
| Seguridad (Security) | **A** | 1.0 |
| Mantenibilidad (Maintainability) | **A** | 1.0 |

**Complejidad:** 610 ciclomática y 355 cognitiva. **Líneas de código (ncloc):** 3 886.

---

## 3. Plan de Remediación y Deuda Técnica

- **Deuda Técnica Estimada:** **0 h 00 min** al cierre (SonarQube `sqale_index = 0`).
  Antes de la remediación era de **0 h 30 min** (`sqale_index = 30`).
- **Ratio de deuda técnica:** 0.0 %.

**Hallazgos iniciales y correcciones aplicadas:**

| # | Hallazgo | Regla | Ubicación | Corrección aplicada | Estado |
|:---:|:---|:---|:---|:---|:---:|
| 1 | Promesa sin `await`, `.catch()` ni `void` explícito | `javascript:S9383` | `Dashboard.jsx:52` | `void fetchPuntos()` dentro del `useEffect`. | Corregido |
| 2 | Promesa sin manejo explícito | `javascript:S9383` | `Dashboard.jsx:53` | `void fetchRutas()`. | Corregido |
| 3 | Promesa sin manejo explícito | `javascript:S9383` | `Dashboard.jsx:54` | `void fetchVehiculos()`. | Corregido |
| 4 | Promesa sin manejo explícito | `javascript:S9383` | `Dashboard.jsx:72` | `void fetchPuntos()` tras crear un pedido. | Corregido |
| 5 | Promesa sin manejo de rechazo en el trazado | `javascript:S9383` | `MapView.jsx:190` | Se agregó `.catch()` que deja el estado en "aproximado". | Corregido |
| 6 | Expresión regular con retroceso (rendimiento superlineal) | `javascript:S8786` | `rutaCalles.js:13` | `replace(/\/+$/, '')` se reemplazó por una función con `endsWith`. | Corregido |
| 7 | Método `cors_origins` en conflicto con el campo `CORS_ORIGINS` | `python:S1845` (Bloqueante) | `config.py:45` | La propiedad se renombró a `origenes_cors`; se actualizaron `main.py` y `test_sprint3.py`. | Corregido |

**Resultado después de la remediación:** 0 problemas abiertos (`issues.total = 0`),
0 bugs, 0 vulnerabilidades, 0 code smells, 0 hotspots y deuda técnica de 0 minutos.

**Deuda pendiente fuera de SonarQube (no cuantificada por la herramienta):**

| # | Deuda | Motivo por el que no aparece en SonarQube | Acción |
|:---:|:---|:---|:---|
| 1 | Componentes React sin pruebas | SonarQube la refleja como cobertura baja (9.8 %), no como incidencia. | ACT-S3-04 |
| 2 | Endpoints sin pruebas de integración con PostgreSQL | Requiere infraestructura de pruebas, no es un defecto estático. | ACT-S3-02 y ACT-S3-03 |
| 3 | 112 hallazgos de Ruff de estilo/tipado | SonarQube solo reporta 0 incidencias; Ruff aplica otras reglas. | Limpieza por lotes |
| 4 | ESLint y Prettier no configurados | No es una incidencia de código. | Evaluar en el siguiente ciclo |
| 5 | `pip-audit` no ejecutado | Requiere instalar la herramienta. | ACT-S3-10 |

---

## 4. Cobertura medida por herramienta

### 4.1 Cobertura del backend (pytest-cov)

| Métrica | Resultado |
|:---|---:|
| Pruebas aprobadas | **65** |
| Sentencias | 883 |
| Sentencias sin cubrir | 346 |
| **Cobertura global** | **60.82 %** |

| Módulo | Cobertura | Lectura |
|:---|---:|:---|
| `app/services/exportacion.py` | 100 % | US-008 cubierto por pruebas unitarias. |
| `app/core/config.py` | 100 % | Validación de secretos y CORS. |
| `app/core/security.py` | 100 % | Hash y JWT. |
| `app/models/__init__.py` | 100 % | Modelos SQLAlchemy. |
| `app/schemas/__init__.py` | 100 % | Validación Pydantic. |
| `app/api/v1/endpoints/salud.py` | 100 % | Health check. |
| `app/api/v1/router.py` | 100 % | Registro de rutas. |
| `app/services/optimizer/__init__.py` | 90 % | Motor de ruteo, incluido el origen en la respuesta. |
| `app/core/database.py` | 62 % | Conexión y sesión. |
| `app/main.py` | 59 % | Arranque, CORS y cabeceras. |
| `app/api/v1/endpoints/vehiculos.py` | 54 % | Consulta de vehículos. |
| `app/api/v1/endpoints/auth.py` | 47 % | Login y registro. |
| `app/api/v1/endpoints/puntos.py` | 37 % | Requiere pruebas de integración con PostgreSQL. |
| `app/api/v1/endpoints/dependencies.py` | 35 % | Dependencias de autenticación. |
| `app/api/v1/endpoints/rutas.py` | 30 % | Requiere pruebas de integración con PostgreSQL. |
| `app/api/v1/endpoints/geocoding.py` | 25 % | Dependencia externa de mapas. |

### 4.2 Cobertura del frontend (Vitest + V8)

| Archivo | Sentencias | Ramas | Funciones | Líneas |
|:---|---:|---:|---:|---:|
| `src/logica/distancia.js` | 96.55 % | 87.50 % | 100 % | 100 % |
| `src/logica/exportar.js` | 100 % | 86.66 % | 100 % | 100 % |
| `src/logica/rutaCalles.js` | 87.03 % | 83.33 % | 81.81 % | 95.34 % |
| **Total `src/logica/**`** | **93.22 %** | **85.24 %** | **91.3 %** | **97.84 %** |

### 4.3 Por qué SonarQube reporta 9.8 %

SonarQube importa `src/backend/coverage.xml` y `src/frontend/coverage/lcov.info`, pero
calcula la cobertura sobre **todas** las fuentes del proyecto (`src/backend/app` y
`src/frontend/src`). Los componentes React (`Dashboard`, `MapView`, `RutasTab`,
`MapPicker`, `SelectorPuntos`, `ImpactoTab`, `Login`, `App`) no tienen pruebas, por lo
que arrastran la cifra global hacia abajo. No es una contradicción: es la diferencia
entre "cobertura del código con pruebas" y "cobertura de todo el producto".

**Limitación explícita:** la cobertura global de SonarQube (9.8 %) no alcanza el
objetivo de 70 % del `SPECS.md`. El backend (60.82 %) tampoco lo alcanza. La deuda se
concentra en endpoints que dependen de PostgreSQL y en la capa de interfaz.

---

## 5. Análisis estático complementario

### 5.1 Ruff (Python)

`ruff check .` reporta **112 hallazgos**, todos de estilo, tipado o convención:

| Regla | Cantidad | Naturaleza | Riesgo |
|:---|---:|:---|:---|
| `B008` | 45 | `Depends()` de FastAPI en valores por defecto | Convención del framework; no es un defecto funcional. |
| `UP006` | 22 | Anotaciones `List`/`Dict` en lugar de `list`/`dict` | Modernización de tipado. |
| `I001` | 17 | Imports sin ordenar | Estilo. |
| `UP045` | 12 | `Optional[X]` en lugar de `X | None` | Modernización de tipado. |
| `UP017` | 7 | `datetime.timezone.utc` en lugar de `datetime.UTC` | Modernización; no se aplicó para conservar compatibilidad con Python 3.10. |
| `UP035` | 5 | Imports de `typing` obsoletos | Modernización. |
| `C408` | 2 | `dict()` innecesario | Estilo. |
| `B017` | 1 | `pytest.raises(Exception)` genérico | Calidad de prueba. |
| `SIM102` | 1 | `if` anidable | Estilo. |

Las reglas críticas `E9` (errores de sintaxis), `F63` (comparaciones sospechosas),
`F7` (errores de estructura) y `F82` (nombres no definidos) no reportan hallazgos.
ESLint y Prettier no están configurados en el repositorio; SonarQube cubre parcialmente
el análisis del frontend.

### 5.2 Dependencias y compilación

| Verificación | Resultado |
|:---|:---|
| `npm audit --json` | **0 vulnerabilidades** en 106 dependencias (34 de producción, 73 de desarrollo, 27 opcionales). |
| `npm run build` | **Exitosa** con Vite 8.3.5; **83 módulos** transformados. |
| `pip-audit` | **No ejecutado** (herramienta no instalada). |
| GitHub Actions / CodeQL | Configurados y validados por sintaxis; **no ejecutados en GitHub** desde este entorno. |

### 5.3 Auditoría funcional

| Verificación | Resultado |
|:---|:---|
| `python auditoria_api.py 8000` | **SIN ANOMALÍAS**: login, RBAC, aislamiento por operador, rutas, puntos, vehículos, exportación, geocodificación y códigos de error. |
| `python smoke_sprint2.py 8000` | **TODO OK**: flujo completo de ruta, edición, recálculo de CO₂ y borrado. |

---

## 6. Reproducibilidad del análisis

El análisis se ejecutó sobre el código del repositorio con SonarQube Community en Docker:

```bash
# 1. Servidor local
docker run -d --name sonarqube -p 9000:9000 sonarqube:community

# 2. Reportes que consume SonarQube
cd src/backend && python -m pytest -q --cov=app --cov-report=xml
cd ../frontend && npm run coverage

# 3. Análisis (token generado en SonarQube)
docker run --rm --add-host=host.docker.internal:host-gateway \
  -e SONAR_HOST_URL=http://host.docker.internal:9000 \
  -e SONAR_TOKEN=<token> \
  -v "$PWD:/usr/src" -w /usr/src \
  sonarsource/sonar-scanner-cli
```

> **Estado del entorno:** al finalizar el análisis el contenedor se detuvo para liberar
> recursos. Para volver a abrir el panel se ejecuta
> `docker start sonarqube` y se accede a `http://localhost:9000` con el usuario `admin`.
> El token del escáner es local y no se versiona; si se perdió, se genera uno nuevo en
> *My Account → Security*.

**Evidencias exportadas** (respuestas de la API de SonarQube):

- [`measures.json`](../../05%20Evidencias/sonar-sprint3/measures.json)
- [`quality-gate.json`](../../05%20Evidencias/sonar-sprint3/quality-gate.json)
- [`issues.json`](../../05%20Evidencias/sonar-sprint3/issues.json)

---

## 7. Conclusión

El código del Sprint 3 compila, pasa sus 65 pruebas de backend y 24 de frontend, y no
tiene bugs, vulnerabilidades ni code smells abiertos en SonarQube. La remediación de los
7 hallazgos iniciales redujo la deuda técnica de 30 minutos a 0 y dejó las tres
calificaciones en **A**.

La calidad **no se declara certificada**: la cobertura global de SonarQube es 9.8 %, el
backend está en 60.82 % (objetivo 70 %), la interfaz no tiene pruebas de componente, el
Quality Gate se evaluó con condiciones ignoradas por ser el primer análisis y los
workflows no se ejecutaron en GitHub. Estas brechas quedan registradas con acciones
concretas en la retrospectiva (ACT-S3-02 a ACT-S3-10).

---

[← Volver al README principal](../../../README.md)
