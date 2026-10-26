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
| 1.0.0 | 08/11/2026 | Jhunior Harold Cosme Tenorio / Equipo EcoLogística | Acta de Revisión del Sprint 3. |

---

## Alcance comprometido

El Sprint 3 comprende las últimas historias del backlog priorizado:

| ID | Título | Épica | SP | Estado |
|---|---|---|---:|:---|
| US-006 | Ver el detalle de cada parada de entrega en el mapa | EP-03 | 2 | Completada |
| US-008 | Exportar o descargar el resumen de una ruta | EP-04 | 2 | Completada |
| EN-03 | Configurar pipeline CI/CD con despliegue a Staging | EP-04 | 8 | Parcial |

**Compromiso total:** 12 Story Points.

**Resultado:** 4 Story Points cerrados y 8 Story Points en estado parcial. EN-03 no se
declara terminado porque su criterio de aceptación exige que la nueva versión quede
accesible en Staging sin intervención manual, y en este repositorio no existe un host
de Staging ni credenciales para activarlo. El pipeline de integración continua sí está
implementado y el flujo de despliegue quedó preparado y desactivado por defecto.

---

## Qué se implementó en cada elemento

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

### EN-03 — Pipeline CI/CD (parcial)

Se incorporaron los siguientes archivos:

| Archivo | Contenido |
|:---|:---|
| `.github/workflows/ci.yml` | Backend con pytest y cobertura, frontend con Vitest y build, PostgreSQL 16 de servicio, Ruff mínimo y carga de artefactos. |
| `.github/workflows/deploy-staging.yml` | Despliegue por *deploy hook* y verificación de salud, desactivado por defecto mediante `STAGING_DEPLOY_ENABLED`. |
| `sonar-project.properties` | Configuración de fuentes, pruebas y reportes de cobertura para SonarQube/SonarCloud. |

El job de SonarQube es opcional y solo se ejecuta si el repositorio define
`SONAR_ENABLED=true` y el secreto `SONAR_TOKEN`. No se ejecutó en este sprint.

**Limitación:** no se dispone de host de Staging, dominio, credenciales ni *deploy hook*.
Por ese motivo no se puede cumplir el escenario "la nueva versión queda desplegada y
accesible en Staging sin intervención manual". El workflow queda preparado, pero no se
afirma que haya desplegado nada.

---

## Criterios de aceptación verificados

| Elemento | Criterio | Resultado | Evidencia |
|:---|:---|:---|:---|
| US-006 | Al hacer clic en un marcador se muestra dirección y orden de visita. | Cumplido por revisión de código. | `MapView.jsx` (`crearPopupParada`, `bindPopup`). |
| US-006 | Un punto sin dirección muestra las coordenadas sin error. | Cumplido por revisión de código. | Rama `if (!direccion)` del popup. |
| US-006 | El detalle es alcanzable con teclado. | Cumplido por revisión de código; no probado con lector de pantalla. | `keyboard: true`, `title` y `alt` en cada marcador. |
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
| Pruebas del backend | `python -m pytest -q --cov=app --cov-report=term-missing` | **64 pruebas aprobadas**. |
| Cobertura del backend | `coverage report --precision=2` | **59.89 %** global (880 sentencias, 353 sin cubrir). |
| Módulo de exportación | Reporte de cobertura | **100 %** (`app/services/exportacion.py`). |
| Pruebas del frontend | `npm run coverage` | **16 pruebas aprobadas** en 2 archivos. |
| Cobertura del frontend | Reporte de Vitest/V8 | **98.43 %** sentencias, **87.09 %** ramas, **100 %** funciones y líneas sobre `src/logica/**`. |
| Compilación del frontend | `npm run build` | **Exitosa** con Vite 8.3.5; 82 módulos transformados. |
| Dependencias del frontend | `npm audit --json` | **0 vulnerabilidades** en 106 dependencias. |
| Análisis estático | `ruff check .` | **109 hallazgos** de estilo/tipado; ninguno de la familia `E9`, `F63`, `F7` o `F82`. |
| Verificación mínima de Ruff | `ruff check app tests --select E9,F63,F7,F82` | **Sin hallazgos**. |
| Sintaxis YAML | `yaml.safe_load` sobre los tres workflows | **Válida**. |

### Verificaciones no ejecutadas

| Verificación | Motivo |
|:---|:---|
| `auditoria_api.py` y `smoke_sprint2.py` | No hay servicio PostgreSQL instalado en el entorno local. |
| Ejecución real de GitHub Actions | Los workflows se validaron por revisión y sintaxis, pero no se ejecutaron en GitHub desde este entorno. |
| SonarQube / SonarCloud | No hay servidor, organización ni token disponibles; el Quality Gate no se consultó. |
| Despliegue en Staging | No existe host ni credenciales de Staging. |
| Escaneo dinámico OWASP ZAP | No solicitado ni disponible en el entorno. |
| Auditoría WCAG automatizada (axe/WAVE) | No instalada; la revisión fue manual y de contraste. |

---

## Demostración del trabajo completado

El incremento es reproducible sobre la aplicación en ejecución. No se afirma que se
haya realizado una sesión de demostración ante stakeholders, porque el repositorio no
registra evidencia de ese evento.

Recorrido de verificación:

1. Iniciar sesión como operador y abrir la pestaña **Mapa**.
2. Seleccionar una ruta guardada y hacer clic sobre un marcador. Se comprueba el número
   de parada, la dirección, el destinatario y el peso.
3. Verificar un punto registrado solo con coordenadas: el popup muestra las coordenadas
   como información mínima.
4. En la pestaña **Rutas**, pulsar **Exportar** sobre una ruta calculada y comprobar que
   el archivo CSV se descarga con el nombre `ruta-XXXXXXXX-AAAAMMDD.csv`.
5. Abrir el CSV en una hoja de cálculo y verificar que los textos con `=`, `+`, `-` o `@`
   aparecen como texto y no como fórmulas.
6. Intentar exportar una ruta sin distancia calculada: la interfaz solicita calcularla
   primero.
7. Revisar `.github/workflows/ci.yml` y `.github/workflows/deploy-staging.yml` como
   evidencia de configuración del pipeline.

---

## Pendientes y limitaciones

1. **EN-03 no está cerrado.** Falta definir el host de Staging, cargar
   `STAGING_DEPLOY_HOOK` y `STAGING_HEALTH_URL`, activar
   `STAGING_DEPLOY_ENABLED=true` y ejecutar el despliegue.
2. **La cobertura global del backend es 59.89 %**, por debajo del objetivo de 70 % del
   `SPECS.md`. El módulo nuevo de exportación sí alcanza 100 %.
3. **Las pruebas de la interfaz cubren solo `src/logica/**`.** No hay pruebas de
   componentes React ni de los popups de US-006.
4. **SonarQube no se ejecutó.** No se declara un Quality Gate aprobado ni un estado de
   vulnerabilidades.
5. **Los scripts de extremo a extremo no se reejecutaron** por ausencia de PostgreSQL.
6. **RN-002, HTTPS en la aplicación, MFA y rate limiting** siguen pendientes, según el
   alcance ya documentado en sprints anteriores.

---

[← Volver al README principal](../../../README.md)
