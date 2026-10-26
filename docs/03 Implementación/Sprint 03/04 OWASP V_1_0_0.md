# Revisión OWASP Top 10

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
| 1.0.0 | 08/11/2026 | Jhunior Harold Cosme Tenorio / Equipo EcoLogística | Revisión de seguridad OWASP Top 10 del Sprint 3. |

---

## Objetivo y metodología

Este documento contrasta el código del PMV con las diez categorías del **OWASP Top 10
(2021)**. La revisión combinó:

- lectura del código de autenticación, autorización, rutas, exportación y configuración;
- ejecución de la suite pytest, incluidas las pruebas de seguridad del Sprint 3;
- auditoría de dependencias del frontend con `npm audit`;
- revisión de la configuración de CORS, cabeceras y secretos.

**No se ejecutó** un escaneo dinámico (OWASP ZAP), un análisis SAST de SonarQube ni una
prueba de penetración. Por tanto, este documento **no certifica** que la aplicación esté
libre de vulnerabilidades; registra los controles presentes y las brechas conocidas.

---

## Resumen por categoría

| Categoría OWASP 2021 | Estado en el PMV | Evidencia / brecha |
|:---|:---|:---|
| A01 — Broken Access Control | Parcial | JWT + RBAC + aislamiento por operador; faltan pruebas de integración de todos los endpoints. |
| A02 — Cryptographic Failures | Parcial | bcrypt y validación de secreto en Staging/Producción; HTTPS no está implementado en la aplicación. |
| A03 — Injection | Mitigado en el código revisado | SQLAlchemy ORM, Pydantic, neutralización de fórmulas CSV y uso de `textContent` en popups. |
| A04 — Insecure Design | Parcial | Reglas de capacidad y mínimo de puntos; RN-002 (bloqueo por intentos) no está implementada. |
| A05 — Security Misconfiguration | Parcial | CORS explícito y cabeceras de endurecimiento; no hay rate limiting ni configuración TLS local. |
| A06 — Vulnerable and Outdated Components | Parcial | `npm audit` sin vulnerabilidades; no se ejecutó un SCA de dependencias Python. |
| A07 — Identification and Authentication Failures | Parcial | JWT de 8 horas, bcrypt y 401 uniforme; sin bloqueo por intentos ni MFA. |
| A08 — Software and Data Integrity Failures | Parcial | Dependencias fijadas y CI/CD configurado; sin firma de artefactos ni despliegue verificado. |
| A09 — Security Logging and Monitoring Failures | Parcial | `X-Request-ID`, logs de error y de login fallido sin contraseña; no hay monitoreo centralizado. |
| A10 — Server-Side Request Forgery (SSRF) | Mitigado en el código revisado | La geocodificación usa URLs fijas de Nominatim y solo recibe parámetros de búsqueda. |

---

## A01 — Broken Access Control

### Controles presentes

- `get_current_user` valida el token Bearer, su firma, su expiración y la existencia del
  usuario; responde `401` con `WWW-Authenticate: Bearer`.
- `get_current_admin` y `get_current_operador` aplican control por rol.
- `GET`, `PUT`, `DELETE` y `GET /export` de una ruta comprueban que el usuario sea el
  operador propietario o un administrador (`_ruta_autorizada`).
- `POST /auth/register` exige rol Administrador; antes era público y permitía escalar
  privilegios.
- El aislamiento por operador está cubierto por la auditoría de API y por pruebas del
  backend.

### Brecha

No todas las rutas tienen una prueba de integración con base de datos que verifique el
`403` de un operador ajeno. La cobertura de `rutas.py` es 30 %, por lo que el control
existe en el código pero no está ejercitado de forma exhaustiva por la suite actual.

---

## A02 — Cryptographic Failures

### Controles presentes

- Contraseñas con `bcrypt.hashpw` y `bcrypt.checkpw`; nunca se almacena la contraseña en
  claro ni se devuelve el hash en las respuestas.
- JWT firmado con HS256 y expiración configurable (8 horas por defecto).
- `config.py` rechaza el secreto de ejemplo y los secretos de menos de 32 caracteres
  cuando `ENVIRONMENT` es `staging`, `production` o `produccion`.
- La cabecera `Strict-Transport-Security` se agrega cuando la petición llega por HTTPS
  (`X-Forwarded-Proto: https`).

### Brecha

- **HTTPS no está implementado en la aplicación.** El entorno local sirve HTTP; el
  cifrado en tránsito depende del proxy o del hosting de Staging, que no se configuró.
- El valor por defecto de `JWT_SECRET` sigue existiendo para desarrollo. La validación
  solo se activa en entornos desplegados.

---

## A03 — Injection

### Controles presentes

- SQLAlchemy ORM con consultas parametrizadas; no se identificaron concatenaciones de
  SQL con entrada del usuario.
- Pydantic valida correo, coordenadas, peso, longitud de campos y tipos.
- La exportación CSV neutraliza celdas que empiezan por `=`, `+`, `-`, `@`, tabulador o
  salto de línea, y conserva los números negativos de las coordenadas.
- Los popups del mapa se construyen con `document.createElement` y `textContent`; no se
  interpola HTML con dirección o destinatario.
- React escapa por defecto el texto renderizado en la interfaz.

### Pruebas

| Prueba | Resultado |
|:---|:---|
| `test_csv_neutraliza_formulas_en_texto` | Aprobada |
| `test_coordenadas_negativas_no_se_escapan` | Aprobada |
| `test_celda_csv_detecta_formula_con_espacios_iniciales` | Aprobada |
| `test_direccion_vacia_o_solo_espacios_se_rechaza` | Aprobada |
| `test_coordenada_fuera_de_rango_se_rechaza` | Aprobada |
| `test_peso_deve_ser_positivo` | Aprobada |

---

## A04 — Insecure Design

### Controles presentes

- Una ruta exige al menos 2 puntos y como máximo 20 (`RN-010`, `EN-01`).
- La capacidad del vehículo se valida antes de confirmar la ruta (`RN-014`).
- La ruta inicia y termina en el centro de distribución (`RN-011`).
- El ahorro de CO₂ se acota en cero y no se muestran porcentajes negativos (`RN-018`).
- La exportación se bloquea en la interfaz si la ruta no fue calculada.

### Brecha

- **RN-002 no está implementada:** no hay bloqueo de la cuenta tras tres intentos
  fallidos durante 15 minutos. Un atacante puede intentar fuerza bruta sin límite.
- No hay rate limiting en el login ni en la geocodificación.

---

## A05 — Security Misconfiguration

### Controles presentes

- CORS con orígenes explícitos (`http://localhost:5173` y `http://127.0.0.1:5173` por
  defecto); no se usa `*`.
- Cabeceras `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`,
  `Referrer-Policy: no-referrer` y `Permissions-Policy` en las respuestas.
- `.env` está excluido por `.gitignore`; `.env.example` no contiene credenciales reales.
- El manejador global de errores devuelve un mensaje genérico y un `request_id`, sin
  trazas internas.

### Brecha

- No hay rate limiting.
- La documentación Swagger (`/docs`) está habilitada por defecto; en Producción debería
  deshabilitarse o protegerse.
- No se configuró CSP (Content Security Policy).
- No hay un ambiente de Staging donde validar la configuración de producción.

---

## A06 — Vulnerable and Outdated Components

### Evidencia ejecutada

| Componente | Verificación | Resultado |
|:---|:---|:---|
| Frontend (npm) | `npm audit --json` | **0 vulnerabilidades** en 106 dependencias (34 de producción, 73 de desarrollo, 27 opcionales). |
| Backend (pip) | — | **No se ejecutó** `pip-audit` ni un SCA equivalente. |

### Brecha

No se puede afirmar que las dependencias Python estén libres de vulnerabilidades. Las
versiones están fijadas en `requirements.txt`, lo que facilita una auditoría futura,
pero esa auditoría no forma parte de la verificación de este sprint.

---

## A07 — Identification and Authentication Failures

### Controles presentes

- Contraseñas con bcrypt.
- Token JWT con expiración de 8 horas y validación de firma.
- Respuesta `401` uniforme para credenciales inválidas, sin distinguir si el correo
  existe.
- El log de login fallido limpia saltos de línea del correo y no registra la contraseña.
- `GET /auth/me` devuelve el rol sin exponer el hash.

### Brecha

- Sin bloqueo por intentos fallidos (**RN-002**).
- Sin MFA/TOTP; la especificación existe en
  [`docs/04 Arquitectura/02 Especificación MFA y Sesiones`](../../04%20Arquitectura/02%20Especificacion%20MFA%20y%20Sesiones%20V_1_0_0.md),
  pero no está implementada.
- Sin rotación de tokens ni lista de revocación.

---

## A08 — Software and Data Integrity Failures

### Controles presentes

- Dependencias con versiones fijadas en el backend y `package-lock.json` en el frontend.
- CI configurado para ejecutar pruebas, cobertura y build antes de fusionar.
- CodeQL configurado para Python y JavaScript/TypeScript.
- El despliegue a Staging está desactivado por defecto y requiere una variable explícita.

### Brecha

- Los workflows no se ejecutaron en GitHub desde este entorno.
- No hay firma de artefactos ni verificación de procedencia (SLSA/provenance).
- El despliegue a Staging no se verificó.

---

## A09 — Security Logging and Monitoring Failures

### Controles presentes

- Cada petición recibe un `X-Request-ID`, que se devuelve al cliente y se usa en los
  logs de error.
- Los errores no controlados se registran con traza en el servidor y se devuelve un
  mensaje genérico al cliente.
- Los intentos de login fallidos se registran sin la contraseña.

### Brecha

- No hay monitoreo centralizado, alertas ni retención definida de logs.
- No se registran eventos de auditoría de cambios de rutas o puntos.

---

## A10 — Server-Side Request Forgery (SSRF)

### Controles presentes

- La geocodificación usa URLs fijas de Nominatim
  (`https://nominatim.openstreetmap.org/search` y `/reverse`).
- El usuario solo controla el parámetro `q` y las coordenadas; no puede elegir el host
  ni el esquema de la URL.
- El endpoint exige autenticación de operador o administrador.
- Hay timeout, reintentos acotados y caché para reducir el abuso del servicio externo.

### Brecha

No se identificó una vulnerabilidad SSRF directa en el código revisado. La dependencia
de un servicio externo sigue siendo un riesgo de disponibilidad, no de SSRF.

---

## Pruebas de seguridad ejecutadas

| Prueba / verificación | Resultado |
|:---|:---|
| `test_cors_no_usa_comodin_por_defecto` | Aprobada |
| `test_produccion_rechaza_secreto_de_ejemplo` | Aprobada |
| `test_produccion_rechaza_secreto_corto` | Aprobada |
| `test_produccion_acepta_secreto_largo` | Aprobada |
| `test_cabeceras_de_seguridad_y_correlacion` | Aprobada |
| `test_token_invalido_devuelve_none` | Aprobada |
| `test_token_firmado_con_otra_clave_se_rechaza` | Aprobada |
| `test_token_expirado_se_rechaza` | Aprobada |
| `npm audit --json` | 0 vulnerabilidades |

### No ejecutado

- OWASP ZAP o escaneo dinámico.
- SonarQube/SonarCloud y su Quality Gate.
- `pip-audit` o SCA de dependencias Python.
- Prueba de penetración manual.
- Verificación de HTTPS en un ambiente desplegado.

---

## Hallazgos priorizados

| # | Hallazgo | Categoría | Severidad | Estado |
|:---:|:---|:---|:---:|:---|
| 1 | Sin bloqueo por intentos fallidos ni rate limiting en login. | A04 / A07 | Alta | Abierto |
| 2 | HTTPS no implementado en la aplicación; Staging no disponible. | A02 | Alta | Abierto |
| 3 | Sin SCA de dependencias Python. | A06 | Media | Abierto |
| 4 | Swagger público y sin CSP en la configuración por defecto. | A05 | Media | Abierto |
| 5 | Sin monitoreo centralizado ni auditoría de cambios. | A09 | Media | Abierto |
| 6 | Cobertura de integración insuficiente en endpoints de rutas. | A01 | Media | Abierto |
| 7 | Workflows de CI/CD y CodeQL no ejecutados en GitHub. | A08 | Media | Abierto |

---

## Conclusión

El PMV incorpora controles razonables para un proyecto académico: autenticación JWT,
bcrypt, RBAC, aislamiento por operador, validación Pydantic, ORM, cabeceras de
seguridad, CORS explícito y neutralización de fórmulas en la exportación. También
incorpora una validación de secreto para entornos desplegados y un pipeline con análisis
estático mínimo y CodeQL.

Sin embargo, **no se declara que el sistema sea seguro ni que cumpla OWASP Top 10 de
forma certificada**. Persisten brechas de alta prioridad —RN-002, rate limiting y
HTTPS— y no se ejecutaron escaneos dinámicos ni SCA de Python. El estado real es
"controles parciales verificados por revisión y pruebas unitarias", no "sin
vulnerabilidades".

---

[← Volver al README principal](../../../README.md)
