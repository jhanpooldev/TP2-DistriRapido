# Revisión del sprint

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
| 1.0.0 | 26/10/2026 | Jhunior Harold Cosme Tenorio / Equipo EcoLogística | Acta de Revisión del Sprint 3 con US-006, US-008 y EN-03 parcial. |
| 1.1.0 | 26/10/2026 | Jhunior Harold Cosme Tenorio / Equipo EcoLogística | Se incorpora el trazado por calles, los resultados reales de SonarQube y la remediación de hallazgos. |

---

## Alcance comprometido

| ID | Título | Épica | SP | Estado |
|---|---|---|---:|---|
| US-006 | Ver el detalle de cada parada de entrega en el mapa | EP-03 | 2 | Completada |
| US-008 | Exportar o descargar el resumen de una ruta | EP-04 | 2 | Completada |
| EN-03 | Configurar pipeline CI/CD con despliegue a Staging | EP-04 | 8 | Parcial |

**Compromiso total:** 12 Story Points.

**Resultado:** 4 Story Points cerrados y 8 Story Points en estado parcial. EN-03 no se
declara terminado porque su criterio de aceptación exige que la nueva versión quede
accesible en Staging sin intervención manual, y en este repositorio no existe un host
de Staging ni credenciales para activarlo. El pipeline de integración continua sí está
implementado y el flujo de despliegue quedó preparado y desactivado por defecto.

Además de las historias comprometidas, el incremento incluye una **mejora visual del
mapa** solicitada durante el sprint: el recorrido se dibuja por calles reales en lugar
de una línea recta entre paradas.

---

## Historias de Usuario completadas en este Sprint

La definición de "Done" aplicada es la del **DoD global** del proyecto
([`docs/02 Planificación/01 Transformando a ágil`](../../02%20Planificación/01%20Transformando%20a%20ágil%20V_1_0_0.md#4-definition-of-done-dod-global-del-proyecto)):

- código implementado y funcionando según los criterios de aceptación;
- cobertura de pruebas ≥ 80 % sobre el código nuevo o modificado;
- análisis estático y de seguridad sin vulnerabilidades críticas ni bloqueantes abiertas;
- revisión de código aprobada por otra persona;
- despliegue automático verificado en Staging;
- documentación de API/código actualizada;
- sin errores críticos en el flujo cubierto;
- tarjeta en "Done" con evidencia enlazada.

### US-006 — Detalle de cada parada en el mapa

`src/frontend/src/components/MapView.jsx` construye un popup para cada marcador con:

- número y orden de visita de la parada;
- dirección registrada;
- destinatario;
- peso del paquete.

Cuando el punto solo tiene coordenadas y no tiene dirección textual, el popup muestra
las coordenadas con seis decimales como información mínima, sin producir un error. El
popup se arma con nodos DOM y `textContent`, no con interpolación de HTML, para que una
dirección o un destinatario no puedan inyectar etiquetas en el mapa.

Los marcadores incluyen `title`, `alt` y `keyboard: true` para que el detalle pueda
alcanzarse con teclado. El contenedor del mapa tiene `role="region"` y una etiqueta
descriptiva.

**Cumplimiento del DoD:**

| Criterio del DoD | Evidencia | Estado |
|:---|:---|:---:|
| Código según criterios de aceptación | Popup de parada y marcador numerado en `MapView.jsx`. | Cumple |
| Cobertura ≥ 80 % del código nuevo | El popup de `MapView.jsx` no tiene prueba de componente; la cobertura de `rutaCalles.js` (87.03 % de sentencias) corresponde al trazado, no al popup. | **Parcial** |
| Análisis estático sin bloqueantes | SonarQube local: 0 bugs, 0 code smells y 0 hotspots tras la remediación. | Cumple |
| Revisión por otra persona | No hay Pull Request registrado en el repositorio. | **No verificable** |
| Despliegue en Staging | No existe ambiente de Staging. | **No cumple** |
| Documentación actualizada | Este documento, `CHANGELOG.md` y `README.md`. | Cumple |
| Sin errores críticos en el flujo | Verificación en navegador del 26/10/2026. | Cumple |
| Tarjeta en "Done" con evidencia | La evidencia queda enlazada en este repositorio; no hay tablero Jira accesible para verificar el movimiento. | **No verificable** |

### US-008 — Exportación del resumen de una ruta

- `GET /api/v1/rutas/{ruta_id}/export` devuelve un archivo CSV en UTF-8 con BOM,
  generado en el backend (`src/backend/app/services/exportacion.py`).
- El archivo contiene los datos generales de la ruta, el impacto ambiental estimado y
  la tabla de puntos en orden de visita.
- Los textos se neutralizan contra inyección de fórmulas en hojas de cálculo: una celda
  que empiece por `=`, `+`, `-` o `@` recibe un apóstrofo de protección, mientras que
  las coordenadas negativas se conservan como números.
- El nombre del archivo es ASCII y predecible: `ruta-<8 caracteres>-<fecha>.csv`.
- La interfaz bloquea la exportación cuando la ruta aún no tiene distancia calculada y
  muestra el mensaje "Calcula la ruta antes de exportar su resumen".
- El endpoint reutiliza la autorización de la ruta: un operador no puede exportar rutas
  de otro operador y un administrador sí puede hacerlo.

**Cumplimiento del DoD:**

| Criterio del DoD | Evidencia | Estado |
|:---|:---|:---:|
| Código según criterios de aceptación | 8 pruebas en `src/backend/tests/test_sprint3.py`. | Cumple |
| Cobertura ≥ 80 % del código nuevo | `app/services/exportacion.py`: **100 %**. | Cumple |
| Análisis estático sin bloqueantes | SonarQube local: 0 bugs, 0 code smells y 0 hotspots. | Cumple |
| Revisión por otra persona | No hay Pull Request registrado. | **No verificable** |
| Despliegue en Staging | No existe ambiente de Staging. | **No cumple** |
| Documentación actualizada | Endpoint descrito en este documento y en `README.md`. | Cumple |
| Sin errores críticos en el flujo | Pruebas unitarias y exportación verificada en la interfaz. | Cumple |
| Tarjeta en "Done" con evidencia | Evidencia enlazada aquí; tablero Jira no accesible. | **No verificable** |

### Mejora incluida — Trazado de la ruta por calles

El mapa dejó de dibujar una línea recta entre paradas. El frontend consulta el servidor
público de **OSRM** (OpenStreetMap) y dibuja la geometría real de las calles, incluyendo
la salida y el retorno al centro de distribución, que se marca como `CD`.

- Módulo nuevo: `src/frontend/src/logica/rutaCalles.js` (URL de OSRM, normalización de
  la geometría, timeout de 8 s, cancelación y caché de 25 recorridos).
- Respaldo: si OSRM no responde, se dibuja una línea discontinua y se avisa en pantalla.
- La API expone `origen_lat`, `origen_lng` y `origen_direccion` en `RutaResponse` para
  que el mapa cierre el circuito sin duplicar la configuración `HOME_*`.
- Los kilómetros, minutos y emisiones del resumen **siguen calculándose con haversine**;
  el mapa muestra aparte la distancia real del trazado por calles para no mezclar ambas
  mediciones.

**Cumplimiento del DoD:** código implementado, 8 pruebas nuevas (cobertura del módulo
87.03 % de sentencias y 95.34 % de líneas), sin hallazgos abiertos en SonarQube y
documentación actualizada. Quedan las mismas excepciones de Staging y revisión por Pull
Request.

### EN-03 — Pipeline CI/CD (no completada)

Se incorporaron los siguientes archivos:

| Archivo | Contenido |
|:---|:---|
| `.github/workflows/ci.yml` | Backend con pytest y cobertura, frontend con Vitest y build, PostgreSQL 16 de servicio, Ruff mínimo y carga de artefactos. |
| `.github/workflows/deploy-staging.yml` | Despliegue por *deploy hook* y verificación de salud, desactivado por defecto mediante `STAGING_DEPLOY_ENABLED`. |
| `.github/workflows/codeql.yml` | Análisis CodeQL para Python y JavaScript/TypeScript. |
| `sonar-project.properties` | Configuración de fuentes, pruebas, cobertura y versión para SonarQube/SonarCloud. |

**Limitación:** no se dispone de host de Staging, dominio, credenciales ni *deploy hook*.
Por ese motivo no se puede cumplir el escenario "la nueva versión queda desplegada y
accesible en Staging sin intervención manual". El workflow queda preparado, pero no se
afirma que haya desplegado nada. Los workflows tampoco se ejecutaron en GitHub desde
este entorno; solo se validó su sintaxis YAML.

---

## Criterios de aceptación verificados

| Elemento | Criterio | Resultado | Evidencia |
|:---|:---|:---|:---|
| US-006 | Al hacer clic en un marcador se muestra dirección y orden de visita. | Cumplido por revisión de código. | `MapView.jsx` (`crearPopupParada`, `bindPopup`). |
| US-006 | Un punto sin dirección muestra las coordenadas sin error. | Cumplido por revisión de código. | Rama `if (!direccion)` del popup. |
| US-006 | El detalle es alcanzable con teclado. | Cumplido por revisión de código; no probado con lector de pantalla. | `keyboard: true`, `title` y `alt` en cada marcador. |
| US-006 | El recorrido se muestra por calles y cierra en el centro de distribución. | Cumplido y verificado en navegador. | 4 paradas: 31.0 km por calles y marcador `CD`. |
| US-008 | Se genera un archivo descargable con puntos, orden e impacto ambiental. | Cumplido y probado. | 8 pruebas en `tests/test_sprint3.py`; cobertura de `exportacion.py` 100 %. |
| US-008 | Una ruta no calculada no permite exportar. | Cumplido en la interfaz. | `RutasTab.jsx` y `Dashboard.jsx`. |
| US-008 | El CSV no ejecuta fórmulas al abrirse en una hoja de cálculo. | Cumplido y probado. | `test_csv_neutraliza_formulas_en_texto`, `test_celda_csv_detecta_formula_con_espacios_iniciales`. |
| EN-03 | El pipeline ejecuta pruebas y detiene el despliegue ante un fallo. | Configurado, no ejecutado en GitHub. | `.github/workflows/ci.yml`, `deploy-staging.yml`. |
| EN-03 | La versión queda desplegada y accesible en Staging sin intervención manual. | **No cumplido.** | No existe host ni credenciales de Staging. |

---

## Verificación ejecutada

Todas las cifras siguientes provienen de ejecuciones locales realizadas el 26/10/2026.

| Verificación | Comando | Resultado |
|:---|:---|:---|
| Pruebas del backend | `python -m pytest -q --cov=app --cov-report=term-missing --cov-report=xml` | **65 pruebas aprobadas**. |
| Cobertura del backend | `coverage report --precision=2` | **60.82 %** global (883 sentencias, 346 sin cubrir). |
| Módulo de exportación | Reporte de cobertura | **100 %** (`app/services/exportacion.py`). |
| Motor de optimización | Reporte de cobertura | **90 %** (`app/services/optimizer/__init__.py`). |
| Pruebas del frontend | `npm run coverage` | **24 pruebas aprobadas** en 3 archivos. |
| Cobertura del frontend | Reporte de Vitest/V8 | **93.22 %** sentencias, **85.24 %** ramas, **91.3 %** funciones y **97.84 %** líneas sobre `src/logica/**`. |
| Compilación del frontend | `npm run build` | **Exitosa** con Vite 8.3.5; **83 módulos** transformados. |
| Dependencias del frontend | `npm audit --json` | **0 vulnerabilidades** en 106 dependencias. |
| Análisis estático Python | `ruff check .` | **112 hallazgos** de estilo/tipado; ninguno de la familia `E9`, `F63`, `F7` o `F82`. |
| Verificación mínima de Ruff | `ruff check app tests --select E9,F63,F7,F82` | **Sin hallazgos**. |
| Sintaxis YAML | `yaml.safe_load` sobre los workflows | **Válida**. |
| Auditoría de API | `python auditoria_api.py 8000` | **SIN ANOMALÍAS** sobre PostgreSQL 18. |
| Smoke test de extremo a extremo | `python smoke_sprint2.py 8000` | **TODO OK**. |
| Análisis SonarQube | `sonar-scanner` (Docker, SonarQube Community) | **Quality Gate: OK**; 0 bugs, 0 vulnerabilidades, 0 code smells, 0 hotspots; duplicación 1.4 %. |
| Evidencia de SonarQube | `docs/05 Evidencias/sonar-sprint3/*.json` | Medidas, Quality Gate y lista de incidencias exportadas. |

### Detalle del análisis SonarQube

| Métrica | Valor |
|:---|---:|
| Quality Gate | **OK** (las condiciones de código nuevo se marcan como `ignoredConditions` por ser el primer análisis del proyecto) |
| Cobertura global | **9.8 %** (6.6 % de líneas, 85.2 % de ramas sobre las líneas cubiertas) |
| Duplicación de líneas | **1.4 %** (66 líneas, 4 bloques) |
| Bugs | **0** |
| Vulnerabilidades | **0** |
| Code Smells | **0** |
| Security Hotspots | **0** |
| Deuda técnica | **0 min** (antes de la remediación: 30 min) |
| Fiabilidad / Seguridad / Mantenibilidad | **A / A / A** |
| Líneas de código (ncloc) | 3 886 |

La cobertura global de SonarQube (9.8 %) es menor que la cobertura del backend
(60.82 %) y que la del frontend lógico (93.22 %) porque el análisis incluye todos los
componentes React (`MapView`, `Dashboard`, `Login`, `RutasTab`, etc.), que no tienen
pruebas de componente. Es una brecha real y se registra como tal.

### Remediación aplicada a partir de SonarQube

| Hallazgo | Regla | Corrección aplicada |
|:---|:---|:---|
| 4 promesas sin manejo de rechazo en `Dashboard.jsx` y `MapView.jsx` | `javascript:S9383` | `void` explícito en las cargas del `useEffect` y `.catch()` en la petición del trazado. |
| Expresión regular con retroceso en `rutaCalles.js` | `javascript:S8786` | Se reemplazó `replace(/\/+$/, '')` por una función con `endsWith`. |
| Nombre de método en conflicto con el campo `CORS_ORIGINS` | `python:S1845` | La propiedad se renombró a `origenes_cors` y se actualizaron `main.py` y las pruebas. |

---

### Verificaciones no ejecutadas

| Verificación | Motivo |
|:---|:---|
| Ejecución real de GitHub Actions | Los workflows se validaron por revisión y sintaxis, pero no se ejecutaron en GitHub desde este entorno. |
| Despliegue en Staging | No existe host ni credenciales de Staging. |
| Escaneo dinámico OWASP ZAP | No solicitado ni disponible en el entorno. |
| Auditoría WCAG automatizada (axe/WAVE) | No instalada; la revisión fue manual y de contraste. |
| `pip-audit` (dependencias Python) | No instalado en el entorno de verificación. |

---

## Demostración del trabajo completado

El incremento es reproducible sobre la aplicación en ejecución. **No se registra un acta
de sesión con stakeholders**; la demostración descrita a continuación es la verificación
funcional ejecutada por el equipo sobre el sistema real, no una afirmación de aceptación
formal por parte del cliente.

Recorrido de verificación:

1. Iniciar sesión como operador y abrir la pestaña **Rutas**.
2. Generar una ruta con al menos 2 pedidos y abrirla en la pestaña **Mapa**. El mapa
   dibuja el recorrido por calles, muestra el marcador `CD` del centro de distribución y
   el texto "Trazado por calles: X km (OSRM / OpenStreetMap)".
3. Hacer clic sobre un marcador y comprobar el número de parada, la dirección, el
   destinatario y el peso.
4. Verificar un punto registrado solo con coordenadas: el popup muestra las coordenadas
   como información mínima.
5. Desconectar la red o bloquear OSRM: el mapa cae a la línea discontinua y muestra el
   aviso de trazado aproximado sin romper la aplicación.
6. En la pestaña **Rutas**, pulsar **Exportar** sobre una ruta calculada y comprobar que
   el archivo CSV se descarga con el nombre `ruta-XXXXXXXX-AAAAMMDD.csv`.
7. Abrir el CSV en una hoja de cálculo y verificar que los textos con `=`, `+`, `-` o `@`
   aparecen como texto y no como fórmulas.
8. Revisar el panel de SonarQube (`http://localhost:9000/dashboard?id=jhanpooldev_TP2-DistriRapido`)
   y las evidencias JSON en `docs/05 Evidencias/sonar-sprint3/`.

---

## Pendientes y limitaciones

1. **EN-03 no está cerrado.** Falta definir el host de Staging, cargar
   `STAGING_DEPLOY_HOOK` y `STAGING_HEALTH_URL`, activar
   `STAGING_DEPLOY_ENABLED=true` y ejecutar el despliegue.
2. **La cobertura global del backend es 60.82 %** y la cobertura global de SonarQube es
   9.8 %, por debajo del objetivo de 70 % del `SPECS.md`. El módulo nuevo de exportación
   alcanza 100 % y el módulo de trazado por calles 87.03 % de sentencias.
3. **Las pruebas de la interfaz cubren solo `src/logica/**`.** No hay pruebas de
   componentes React ni de los popups de US-006.
4. **El servidor público de OSRM es de demostración.** No ofrece garantía de
   disponibilidad ni SLA; para producción debe desplegarse una instancia propia o
   contratarse un proveedor con SLA.
5. **La revisión por Pull Request no es verificable** en el repositorio local y el
   tablero Jira no es accesible desde este entorno.
6. **RN-002, HTTPS en la aplicación, MFA y rate limiting** siguen pendientes, según el
   alcance ya documentado en sprints anteriores.

---

[← Volver al README principal](../../../README.md)
