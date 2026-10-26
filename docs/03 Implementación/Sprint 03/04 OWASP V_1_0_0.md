# Reporte de Seguridad OWASP Top 10 (2025)

[← Volver al README principal](../../../README.md)

---

**Nombre del Proyecto:** EcoLogística Lima – Optimizador de Rutas Sostenibles para DistriRápido S.A.C.

**Líder del Proyecto:** Jhunior Harold Cosme Tenorio

**Herramienta de Escaneo:** SonarQube Community (contenedor Docker local) + SonarScanner CLI

**Sprint:** 3 · **Periodo:** 02/11/2026 – 08/11/2026

**Fecha del análisis:** 26/10/2026

**Versión del análisis:** V_1_0_0 (documento 1.1.0)

---

## Control de Versiones del Documento

| Versión | Fecha | Autor | Descripción del Cambio |
|:---:|:---:|:---|:---|
| 1.0.0 | 26/10/2026 | Jhunior Harold Cosme Tenorio / Equipo EcoLogística | Revisión de seguridad OWASP del Sprint 3. |
| 1.1.0 | 26/10/2026 | Jhunior Harold Cosme Tenorio / Equipo EcoLogística | Se migra la matriz a **OWASP Top 10:2025** y se incorporan los resultados reales de SonarQube, los hotspots revisados y la remediación aplicada. |

---

## Objetivo y metodología

Este documento evalúa el PMV contra las diez categorías del **OWASP Top 10:2025**
(lista oficial publicada por OWASP). La revisión combinó:

- análisis estático real con **SonarQube Community** sobre `src/backend/app` y
  `src/frontend/src` (3 886 líneas de código, 14 archivos JavaScript/TypeScript
  analizados y el backend Python completo);
- lectura dirigida del código de autenticación, autorización, rutas, exportación,
  configuración y manejo de errores;
- ejecución de la suite **pytest** (65 pruebas) y **Vitest** (24 pruebas);
- auditoría de dependencias del frontend con `npm audit`;
- auditoría funcional de la API con `auditoria_api.py` y `smoke_sprint2.py` sobre
  PostgreSQL 18;
- revisión de CORS, cabeceras de seguridad, secretos y documentación expuesta.

**Resultado global de SonarQube:** Quality Gate **OK**, **0 vulnerabilidades**,
**0 Security Hotspots** y **0 incidencias abiertas** después de corregir 7 hallazgos
iniciales (5 bugs y 2 code smells). Las evidencias están en
[`docs/05 Evidencias/sonar-sprint3/`](../../05%20Evidencias/sonar-sprint3/).

> **Alcance honesto:** SonarQube es un análisis estático. No se ejecutó OWASP ZAP ni una
> prueba de penetración, y `pip-audit` no está instalado. Por tanto, este documento **no
> certifica** que la aplicación esté libre de vulnerabilidades: registra los controles
> presentes, los hotspots revisados y las brechas que permanecen abiertas.

### Nota de alineación con la plantilla de la consigna

La plantilla oficial del Sprint 3 rotula las categorías con los nombres y el orden de
**OWASP Top 10:2021** (por ejemplo, A02 *Cryptographic Failures*, A03 *Injection*,
A06 *Vulnerable and Outdated Components*, A10 *SSRF*). Para no usar una versión
obsoleta, la matriz principal sigue la **lista oficial 2025**. La sección 4 incluye la
tabla de correspondencia 2021 → 2025, de modo que todas las filas de la plantilla
quedan cubiertas y trazables.

---

## 1. Matriz de Cumplimiento OWASP Top 10 2025

Estados permitidos: **Limpio** (sin hallazgos en SonarQube y control verificado),
**Bajo Revisión** (sin hallazgos estáticos, pero con brecha de proceso o verificación
pendiente) y **Vulnerable** (hallazgo explotable abierto).

| Categoría OWASP 2025 | Estado en el Proyecto | Hallazgos de SonarQube |
|:---|:---:|:---|
| **A01:2025 — Broken Access Control** | Bajo Revisión | 0 vulnerabilidades. JWT + RBAC + aislamiento por operador implementados; falta cobertura de integración en `rutas.py` (30 %). |
| **A02:2025 — Security Misconfiguration** | Bajo Revisión | 0 vulnerabilidades. CORS explícito y cabeceras de endurecimiento; faltan CSP, rate limiting y ocultar Swagger en Producción. |
| **A03:2025 — Software Supply Chain Failures** | Bajo Revisión | 0 vulnerabilidades. `npm audit`: 0 hallazgos en 106 dependencias; `pip-audit` no ejecutado y workflows no corridos en GitHub. |
| **A04:2025 — Cryptographic Failures** | Bajo Revisión | 0 vulnerabilidades. bcrypt + HS256 + validación de secreto; HTTPS no se termina en la aplicación. |
| **A05:2025 — Injection** | Limpio | 0 vulnerabilidades. SQLAlchemy ORM, Pydantic, `textContent` y neutralización de fórmulas CSV con pruebas aprobadas. |
| **A06:2025 — Insecure Design** | Bajo Revisión | 0 vulnerabilidades. Reglas de negocio RN-009/010/011/014/018 implementadas; RN-002 (bloqueo por intentos) sigue pendiente. |
| **A07:2025 — Authentication Failures** | Bajo Revisión | 0 vulnerabilidades. JWT de 8 h, bcrypt y 401 uniforme; sin MFA, sin bloqueo por intentos y sin revocación de tokens. |
| **A08:2025 — Software or Data Integrity Failures** | Bajo Revisión | 0 vulnerabilidades. Dependencias fijadas y CI/CD configurado; sin firma de artefactos y sin ejecución real del pipeline. |
| **A09:2025 — Security Logging & Alerting Failures** | Bajo Revisión | 0 vulnerabilidades. `X-Request-ID`, log de login fallido y error genérico; sin monitoreo centralizado ni alertas. |
| **A10:2025 — Mishandling of Exceptional Conditions** | Limpio | 0 vulnerabilidades. Manejador global de excepciones, mensaje genérico y `request_id`; sin fuga de trazas al cliente. |

**Resumen cuantitativo:** 2 categorías **Limpio**, 8 **Bajo Revisión**, 0 **Vulnerable**.

---

## 2. Detalles de Security Hotspots y Vulnerabilidades Críticas

### 2.1 Vulnerabilidades críticas

**No hay vulnerabilidades abiertas.** SonarQube reporta `vulnerabilities = 0` y
`security_hotspots = 0` en el análisis final del 26/10/2026. La calificación de
seguridad es **A (1.0)**.

La primera corrida tampoco registró vulnerabilidades, pero sí **5 bugs y 2 code
smells**. Como los bugs afectaban el manejo de promesas y el rendimiento de una
expresión regular, se corrigieron antes de cerrar el informe (ver sección 5).

### 2.2 Security Hotspots

SonarQube **no generó hotspots automáticos** (`security_hotspots = 0`). Para cumplir
el requisito de documentar hotspots, se revisaron manualmente las zonas sensibles del
código y se registran a continuación con su ubicación y mitigación:

| # | Hotspot revisado | Ubicación | Riesgo potencial | Mitigación aplicada / control existente | Estado |
|:---:|:---|:---|:---|:---|:---:|
| H-01 | Generación y validación de JWT | `app/core/security.py`, `app/api/v1/endpoints/dependencies.py` | Robo de token, firma débil o expiración excesiva | HS256 con `JWT_SECRET` validado en Staging/Producción (≥ 32 caracteres), expiración de 8 h, verificación de firma, expiración y existencia del usuario. | Mitigado |
| H-02 | Verificación de contraseñas | `app/core/security.py`, `app/api/v1/endpoints/auth.py` | Almacenamiento inseguro o fuga del hash | `bcrypt.hashpw`/`checkpw`; el hash nunca se devuelve; `401` uniforme sin distinguir si el correo existe. | Mitigado |
| H-03 | Exportación CSV | `app/services/exportacion.py`, `app/api/v1/endpoints/rutas.py` | Inyección de fórmulas al abrir el archivo en Excel/Sheets | Celdas que inician con `=`, `+`, `-`, `@`, tabulador o salto de línea se prefijan con apóstrofo; las coordenadas negativas se conservan numéricas; el endpoint reutiliza la autorización de la ruta. | Mitigado |
| H-04 | Construcción de popups del mapa | `src/frontend/src/components/MapView.jsx` | XSS por dirección o destinatario malicioso | Nodos creados con `document.createElement` y `textContent`; no se interpola HTML. React escapa el resto de la interfaz. | Mitigado |
| H-05 | Llamadas a servicios externos (Nominatim/OSRM) | `app/api/v1/endpoints/geocoding.py`, `src/frontend/src/logica/rutaCalles.js` | SSRF o abuso de un servicio de terceros | URLs fijas de Nominatim/OSRM; el usuario solo envía texto y coordenadas; timeout, reintentos acotados y caché. El backend no acepta una URL arbitraria. | Mitigado |
| H-06 | CORS y cabeceras de seguridad | `app/main.py`, `app/core/config.py` | Origen comodín o clickjacking | Orígenes explícitos (`localhost:5173`/`127.0.0.1:5173` por defecto), sin `*`; `X-Content-Type-Options`, `X-Frame-Options: DENY`, `Referrer-Policy`, `Permissions-Policy` y HSTS cuando el esquema es HTTPS. | Mitigado |
| H-07 | Registro de eventos de autenticación | `app/api/v1/endpoints/auth.py` | Contraseñas o tokens en logs | El login fallido registra el correo saneado (sin saltos de línea) y nunca la contraseña. | Mitigado |

**Lectura:** los hotspots son áreas que requieren juicio humano, no defectos
confirmados. Ninguno quedó abierto en SonarQube porque la herramienta no los marcó y la
revisión manual encontró un control o una mitigación para cada uno.

---

## 3. Evaluación detallada por categoría

### A01:2025 — Broken Access Control

**Controles presentes**

- `get_current_user` valida el token Bearer, la firma, la expiración y la existencia
  del usuario; responde `401` con `WWW-Authenticate: Bearer`.
- `get_current_admin` y `get_current_operador` aplican control por rol.
- `GET`, `PUT`, `DELETE` y `GET /export` de una ruta comprueban que el usuario sea el
  operador propietario o un administrador (`_ruta_autorizada`).
- `POST /auth/register` exige rol Administrador; antes era público y permitía escalar
  privilegios.
- La auditoría funcional `auditoria_api.py` verificó aislamiento entre operadores,
  `403`/`404` según corresponda y que un operador no pueda exportar rutas ajenas.

**Brecha**

No todos los endpoints tienen una prueba de integración con PostgreSQL que ejercite el
`403` de un operador ajeno. La cobertura de `rutas.py` es 30 %, por lo que el control
existe en el código pero no está cubierto de forma exhaustiva por la suite. SonarQube
no reporta vulnerabilidades de acceso.

### A02:2025 — Security Misconfiguration

**Controles presentes**

- CORS con orígenes explícitos; no se usa `*`. La propiedad se normaliza en
  `origenes_cors` y se prueba en `test_cors_no_usa_comodin_por_defecto`.
- Cabeceras `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`,
  `Referrer-Policy: no-referrer`, `Permissions-Policy` y HSTS condicionado a HTTPS.
- `.env` excluido por `.gitignore`; `.env.example` sin credenciales reales.
- El manejador global devuelve un mensaje genérico y un `request_id`, sin trazas.

**Brechas**

- No hay **rate limiting** ni **CSP**.
- La documentación Swagger (`/docs`, `/redoc`, `/openapi.json`) está habilitada por
  defecto; en Producción debería deshabilitarse o protegerse.
- No hay un ambiente de Staging donde validar la configuración de producción.

### A03:2025 — Software Supply Chain Failures

**Evidencia ejecutada**

| Componente | Verificación | Resultado |
|:---|:---|:---|
| Frontend (npm) | `npm audit --json` | **0 vulnerabilidades** en 106 dependencias (34 de producción, 73 de desarrollo, 27 opcionales). |
| Backend (pip) | — | **No se ejecutó** `pip-audit` ni un SCA equivalente. |
| Integridad del build | `npm run build` | Exitoso con Vite 8.3.5; 83 módulos transformados. |
| Pipeline | `.github/workflows/ci.yml`, `codeql.yml` | Configurados y validados por sintaxis; **no ejecutados en GitHub** desde este entorno. |

**Brecha**

No se puede afirmar que las dependencias Python estén libres de vulnerabilidades. Las
versiones están fijadas en `requirements.txt`, lo que facilita una auditoría futura,
pero esa auditoría no forma parte de la verificación de este sprint. Tampoco hay firma
de artefactos ni procedencia SLSA.

### A04:2025 — Cryptographic Failures

**Controles presentes**

- Contraseñas con `bcrypt.hashpw`/`checkpw`; nunca se almacena la contraseña en claro ni
  se devuelve el hash.
- JWT firmado con HS256 y expiración configurable (8 horas por defecto).
- `config.py` rechaza el secreto de ejemplo y los secretos de menos de 32 caracteres
  cuando `ENVIRONMENT` es `staging`, `production` o `produccion`.
- HSTS se agrega cuando la petición llega por HTTPS (`X-Forwarded-Proto: https`).

**Brecha**

**HTTPS no está implementado en la aplicación.** El entorno local sirve HTTP; el
cifrado en tránsito depende del proxy o del hosting de Staging, que no se configuró. El
valor por defecto de `JWT_SECRET` sigue existiendo para desarrollo; la validación solo
se activa en entornos desplegados.

### A05:2025 — Injection

**Controles presentes**

- SQLAlchemy ORM con consultas parametrizadas; no se identificaron concatenaciones de
  SQL con entrada del usuario.
- Pydantic valida correo, coordenadas, peso, longitud de campos y tipos.
- La exportación CSV neutraliza celdas que empiezan por `=`, `+`, `-`, `@`, tabulador o
  salto de línea, y conserva los números negativos de las coordenadas.
- Los popups del mapa se construyen con `document.createElement` y `textContent`.
- React escapa por defecto el texto renderizado.

**Pruebas**

| Prueba | Resultado |
|:---|:---:|
| `test_csv_neutraliza_formulas_en_texto` | Aprobada |
| `test_coordenadas_negativas_no_se_escapan` | Aprobada |
| `test_celda_csv_detecta_formula_con_espacios_iniciales` | Aprobada |
| `test_direccion_vacia_o_solo_espacios_se_rechaza` | Aprobada |
| `test_coordenada_fuera_de_rango_se_rechaza` | Aprobada |
| `test_peso_deve_ser_positivo` | Aprobada |

SonarQube no reporta vulnerabilidades de inyección. La regla `javascript:S8786`
(expresión regular con retroceso superlineal) se corrigió en `rutaCalles.js`, aunque es
un problema de rendimiento y no de inyección.

### A06:2025 — Insecure Design

**Controles presentes**

- Una ruta exige al menos 2 puntos y como máximo 20 (RN-010, EN-01).
- La capacidad del vehículo se valida antes de confirmar la ruta (RN-014).
- La ruta inicia y termina en el centro de distribución (RN-011).
- El ahorro de CO₂ se acota en cero y no se muestran porcentajes negativos (RN-018).
- La exportación se bloquea en la interfaz si la ruta no fue calculada.

**Brecha**

**RN-002 no está implementada:** no hay bloqueo de la cuenta tras tres intentos
fallidos durante 15 minutos. Un atacante puede intentar fuerza bruta sin límite. Tampoco
hay rate limiting en el login ni en la geocodificación.

### A07:2025 — Authentication Failures

**Controles presentes**

- Contraseñas con bcrypt.
- Token JWT con expiración de 8 horas y validación de firma.
- Respuesta `401` uniforme para credenciales inválidas, sin distinguir si el correo
  existe.
- El log de login fallido limpia saltos de línea del correo y no registra la contraseña.
- `GET /auth/me` devuelve el rol sin exponer el hash.

**Brecha**

- Sin bloqueo por intentos fallidos (**RN-002**).
- Sin MFA/TOTP; la especificación existe en
  [`docs/04 Arquitectura/02 Especificación MFA y Sesiones`](../../04%20Arquitectura/02%20Especificacion%20MFA%20y%20Sesiones%20V_1_0_0.md),
  pero no está implementada.
- Sin rotación de tokens ni lista de revocación.

### A08:2025 — Software or Data Integrity Failures

**Controles presentes**

- Dependencias fijadas en `requirements.txt` y `package-lock.json` en el frontend.
- CI configurado para ejecutar pruebas, cobertura y build antes de fusionar.
- CodeQL configurado para Python y JavaScript/TypeScript.
- El despliegue a Staging está desactivado por defecto y requiere una variable explícita.
- El CSV se genera en el backend con BOM UTF-8 y nombre de archivo ASCII predecible.

**Brecha**

- Los workflows no se ejecutaron en GitHub desde este entorno.
- No hay firma de artefactos ni verificación de procedencia (SLSA/provenance).
- El despliegue a Staging no se verificó.

### A09:2025 — Security Logging & Alerting Failures

**Controles presentes**

- Cada petición recibe un `X-Request-ID`, que se devuelve al cliente y se usa en los
  logs de error.
- Los errores no controlados se registran con traza en el servidor y se devuelve un
  mensaje genérico al cliente.
- Los intentos de login fallidos se registran sin la contraseña.

**Brecha**

- No hay monitoreo centralizado, alertas ni retención definida de logs.
- No se registran eventos de auditoría de cambios de rutas o puntos.
- No se probó una alerta ante un fallo real; solo se verificó el formato del log.

### A10:2025 — Mishandling of Exceptional Conditions

**Controles presentes**

- `@app.exception_handler(Exception)` captura errores no controlados, registra la traza
  en el servidor y devuelve `500` con `request_id` y un mensaje genérico.
- `lifespan` permite que la API arranque aunque PostgreSQL no esté disponible, y
  `/health` responde `503` con el estado de la base de datos.
- El frontend maneja rechazos de promesas: las cargas del `useEffect` usan `void` y la
  petición del trazado por calles tiene `.catch()` que deja el estado en "aproximado".
- OSRM tiene timeout y respaldo visual; un fallo del servicio externo no rompe el mapa.
- `auditoria_api.py` verificó respuestas `4xx`/`5xx` controladas: ruta malformada,
  token ausente, coordenadas inválidas, recurso inexistente y punto en uso.

**Brecha**

No se ejecutó una prueba de caos (cortar PostgreSQL, OSRM o Nominatim en caliente) más
allá de la verificación funcional del respaldo del mapa. La categoría queda **Limpio**
desde el análisis estático, no desde una validación de resiliencia completa.

---

## 4. Correspondencia con la plantilla oficial (2021 → 2025)

| Fila de la plantilla | Categoría oficial 2025 que la cubre | Dónde se evalúa |
|:---|:---|:---|
| A01 Broken Access Control | A01 Broken Access Control | Sección A01 |
| A02 Cryptographic Failures | A04 Cryptographic Failures | Sección A04 |
| A03 Injection | A05 Injection | Sección A05 |
| A04 Insecure Design | A06 Insecure Design | Sección A06 |
| A05 Security Misconfiguration | A02 Security Misconfiguration | Sección A02 |
| A06 Vulnerable and Outdated Components | A03 Software Supply Chain Failures | Sección A03 |
| A07 Identification and Authentication Failures | A07 Authentication Failures | Sección A07 |
| A08 Software and Data Integrity Failures | A08 Software or Data Integrity Failures | Sección A08 |
| A09 Security Logging and Monitoring Failures | A09 Security Logging & Alerting Failures | Sección A09 |
| A10 SSRF | No es una categoría independiente en 2025; el control de URLs externas se documenta como hotspot H-05 y bajo A02/A10. | Sección 2.2 y A10 |

---

## 5. Remediación aplicada a partir de SonarQube

| # | Hallazgo | Regla | Ubicación | Corrección aplicada | Estado |
|:---:|:---|:---|:---|:---|:---:|
| 1 | Promesa sin `await`, `.catch()` ni `void` | `javascript:S9383` | `Dashboard.jsx:52` | `void fetchPuntos()`. | Corregido |
| 2 | Promesa sin manejo explícito | `javascript:S9383` | `Dashboard.jsx:53` | `void fetchRutas()`. | Corregido |
| 3 | Promesa sin manejo explícito | `javascript:S9383` | `Dashboard.jsx:54` | `void fetchVehiculos()`. | Corregido |
| 4 | Promesa sin manejo explícito | `javascript:S9383` | `Dashboard.jsx:72` | `void fetchPuntos()` tras crear un pedido. | Corregido |
| 5 | Promesa sin rechazo manejado en el trazado | `javascript:S9383` | `MapView.jsx:190` | `.catch()` que deja el estado en "aproximado". | Corregido |
| 6 | Regex con retroceso superlineal | `javascript:S8786` | `rutaCalles.js:13` | `replace(/\/+$/, '')` reemplazado por `quitarBarrasFinales()` con `endsWith`. | Corregido |
| 7 | Método en conflicto con el campo `CORS_ORIGINS` | `python:S1845` (Bloqueante) | `config.py:45` | Propiedad renombrada a `origenes_cors`; actualizados `main.py` y `test_sprint3.py`. | Corregido |

**Verificación posterior:** segunda corrida de SonarQube con `issues.total = 0`,
`bugs = 0`, `vulnerabilities = 0`, `code_smells = 0`, `security_hotspots = 0` y
`sqale_index = 0`. Quality Gate **OK** (condiciones de código nuevo ignoradas por ser
el primer análisis, `ignoredConditions = true`).

---

## 6. Pruebas de seguridad ejecutadas

| Prueba / verificación | Resultado |
|:---|:---:|
| `test_cors_no_usa_comodin_por_defecto` | Aprobada |
| `test_produccion_rechaza_secreto_de_ejemplo` | Aprobada |
| `test_produccion_rechaza_secreto_corto` | Aprobada |
| `test_produccion_acepta_secreto_largo` | Aprobada |
| `test_cabeceras_de_seguridad_y_correlacion` | Aprobada |
| `test_token_invalido_devuelve_none` | Aprobada |
| `test_token_firmado_con_otra_clave_se_rechaza` | Aprobada |
| `test_token_expirado_se_rechaza` | Aprobada |
| `npm audit --json` | 0 vulnerabilidades |
| `auditoria_api.py 8000` | SIN ANOMALÍAS |
| `smoke_sprint2.py 8000` | TODO OK |
| SonarQube (segunda corrida) | 0 vulnerabilidades, 0 hotspots, Quality Gate OK |

### No ejecutado

- OWASP ZAP o cualquier escaneo dinámico (DAST).
- `pip-audit` o SCA de dependencias Python.
- Prueba de penetración manual.
- Verificación de HTTPS en un ambiente desplegado.
- Prueba de caos sobre PostgreSQL, OSRM o Nominatim.

---

## 7. Hallazgos priorizados

| # | Hallazgo | Categoría 2025 | Severidad | Estado |
|:---:|:---|:---|:---:|:---|
| 1 | Sin bloqueo por intentos fallidos ni rate limiting en login. | A06 / A07 | Alta | Abierto |
| 2 | HTTPS no implementado en la aplicación; Staging no disponible. | A04 | Alta | Abierto |
| 3 | Sin SCA de dependencias Python (`pip-audit`). | A03 | Media | Abierto |
| 4 | Swagger público y sin CSP en la configuración por defecto. | A02 | Media | Abierto |
| 5 | Sin monitoreo centralizado ni auditoría de cambios. | A09 | Media | Abierto |
| 6 | Cobertura de integración insuficiente en endpoints de rutas. | A01 | Media | Abierto |
| 7 | Workflows de CI/CD y CodeQL no ejecutados en GitHub. | A08 | Media | Abierto |
| 8 | Sin MFA ni revocación de tokens. | A07 | Media | Abierto |

Las acciones concretas y sus responsables están registradas en la retrospectiva
(ACT-S3-01 a ACT-S3-10), en
[`02 Retrospectiva del Sprint`](02%20Retrospectiva%20del%20Sprint%20V_1_0_0.md).

---

## 8. Conclusión

El PMV incorpora controles razonables para un proyecto académico: autenticación JWT,
bcrypt, RBAC, aislamiento por operador, validación Pydantic, ORM, cabeceras de
seguridad, CORS explícito, neutralización de fórmulas en la exportación y manejo
controlado de excepciones. El análisis real de SonarQube confirma **0 vulnerabilidades**
y **0 Security Hotspots** abiertos, y los 7 hallazgos iniciales se corrigieron en el
código antes de volver a analizar.

Sin embargo, **no se declara que el sistema sea seguro ni que cumpla OWASP Top 10 de
forma certificada**. Persisten brechas de alta prioridad —RN-002, rate limiting y
HTTPS— y no se ejecutaron escaneos dinámicos ni SCA de Python. El estado real es
"controles parciales verificados por análisis estático, revisión y pruebas", no "sin
vulnerabilidades".

---

[← Volver al README principal](../../../README.md)
