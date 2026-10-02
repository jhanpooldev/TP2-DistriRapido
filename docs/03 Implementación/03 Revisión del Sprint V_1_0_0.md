# Revisión del sprint

[⬅ Volver al README principal](../../README.md)

---

**Nombre del Proyecto:** EcoLogística Lima – Optimizador de Rutas Sostenibles para DistriRápido S.A.C.

**Líder del Proyecto:** Jhunior Harold Cosme Tenorio

---

## Control de Versiones del Documento

| Versión | Fecha | Autor | Descripción del Cambio |
|:---:|:---:|:---|:---|
| 1.0.0 | 01/10/2026 | Jhunior Harold Cosme Tenorio / Equipo EcoLogística | Elaboración del acta formal de Revisión del Sprint (Sprint Review) del Sprint 1. |

---

## Historias de Usuario completadas en este Sprint

Durante la ejecución del Sprint 1, el equipo de desarrollo completó satisfactoriamente el 100% de las Historias de Usuario comprometidas en el Sprint Backlog (26 Story Points):

### 1. HU-01: Registro y Autenticación Primaria con Hash Seguro (5 SP)
- **Objetivo:** Permitir el registro de usuarios y el inicio de sesión validando credenciales mediante hashing criptográfico sin almacenar texto en claro.
- **Detalle de Implementación:**
  - Implementación del algoritmo `PBKDF2-HMAC-SHA256` con salt aleatoria de 128 bits e iteraciones calibradas (`RN-004`).
  - Validación estricta de esquemas con Pydantic (`EmailStr`, longitud mínima de 8 caracteres).
  - Emisión de JWT con expiración de 8 horas (`RN-005`) cuando el usuario no requiere MFA.
  - Mensajes de error indeterminados en fallo de credenciales para mitigar ataques de enumeración (OWASP Top 10).

### 2. HU-02: Generación de Secreto TOTP, Código QR y Códigos de Respaldo (5 SP)
- **Objetivo:** Proveer a los usuarios una interfaz y API para vincular sus dispositivos móviles mediante aplicaciones autenticadoras estándar.
- **Detalle de Implementación:**
  - Generación de claves Base32 de 160 bits compatibles con el estándar abierto RFC 6238 (`pyotp`).
  - Generación dinámica de URI `otpauth://` e imagen QR en formato Data URL Base64 para escaneo móvil.
  - Creación de 5 códigos de recuperación de respaldo alfanuméricos de 8 caracteres de un solo uso hasheados con SHA-256.
  - Máquina de estados: el MFA solo pasa a estado activo cuando el usuario confirma un código válido emitido por su dispositivo.

### 3. HU-03: Verificación de Segundo Factor y Soporte de Códigos de Emergencia (5 SP)
- **Objetivo:** Ejecutar la validación del segundo factor en dos pasos para el acceso de usuarios con MFA activado.
- **Detalle de Implementación:**
  - Endpoint `/api/auth/login` emite token efímero de desafío `mfa_token` (vida útil: 5 minutos, ámbito `mfa_pending`).
  - Endpoint `/api/auth/mfa/verify` valida código TOTP de 6 dígitos con ventana de tiempo de 30 segundos y tolerancia de ±30s por desfase de reloj.
  - Validación alternativa mediante código de respaldo; al ser utilizado, el código se marca como consumido en base de datos impidiendo su reutilización.

### 4. HU-04: Gestión Segura de Sesiones y Revocación JTI en Logout (5 SP)
- **Objetivo:** Garantizar que las sesiones puedan ser revocadas inmediatamente cuando el usuario cierre sesión o se detecte actividad anómala.
- **Detalle de Implementación:**
  - Firma criptográfica de tokens con algoritmo HMAC-SHA256 (`HS256`).
  - Incorporación del claim `jti` (JWT ID único) en cada token emitido.
  - Endpoint `/api/auth/logout` que registra el `jti` en la lista negra de revocación.
  - Endpoint protegido `/api/auth/me` que verifica firma, expiración y ausencia en la lista de revocación antes de dar acceso.

### 5. HU-05: Protección contra Fuerza Bruta y Bloqueo de Cuenta (6 SP)
- **Objetivo:** Prevenir ataques de diccionario y fuerza bruta bloqueando las cuentas tras múltiples intentos fallidos.
- **Detalle de Implementación:**
  - Contador de intentos fallidos consecutivos aplicado a contraseñas y códigos MFA.
  - Bloqueo automático por **15 minutos** al acumular **3 intentos fallidos** (`RN-002`).
  - Retorno de código de estado HTTP 423 (Locked) informando el tiempo exacto restante de bloqueo.
  - Restablecimiento automático del contador al transcurrir el periodo o tras una autenticación exitosa.

---

## Demostración del trabajo completado

Demostración a los stakeholders de las funcionalidades implementadas.

La sesión de demostración se desarrolló en vivo ante el docente de la asignatura (en rol de Evaluador Académico) y representantes simulados de la Gerencia de Operaciones de DistriRápido S.A.C., verificando los siguientes puntos de aceptación:

1. **Revisión de Especificación y Criterios BDD (Gherkin):**
   - Se exhibió el documento `docs/01 Inicio/14. Especificacion MFA y Sesiones V_1_0_0.md` y los archivos OpenSpec, demostrando la trazabilidad completa entre las reglas de negocio (`RN-001` a `RN-006`) y los criterios de aceptación en rutas Gold, Feliz e Infeliz.
2. **Documentación Swagger / OpenAPI:**
   - Se inspeccionó la interfaz Swagger UI en `http://localhost:8000/docs`, comprobando que los 8 endpoints REST cuentan con schemas tipados, validaciones de Pydantic y documentación clara de códigos de error HTTP (200, 201, 400, 401, 423).
3. **Flujo de Usuario en Tiempo Real (Panel Web `http://localhost:8000/`):**
   - **Registro:** Se creó la cuenta `jhanpool@distrirapido.pe` con rol de Operador Logístico.
   - **Setup MFA:** Se generó la clave Base32, se mostró el Código QR en pantalla y se listaron los 5 códigos de respaldo.
   - **Escaneo con Google Authenticator:** Se escaneó el Código QR desde un teléfono celular Android/iOS real, sincronizando la cuenta *"EcoLogística Lima"*.
   - **Confirmación:** Se ingresó el token dinámico de 6 dígitos activando el doble factor.
   - **Login en 2 Pasos:** Se cerró sesión y se inició sesión nuevamente. El sistema solicitó el código de 6 dígitos del celular y emitió la sesión de 8 horas con éxito tras ingresarlo.
   - **Prueba de Código de Respaldo:** Se simuló el extravío del celular ingresando un código de respaldo de 8 caracteres; el sistema permitió el acceso y rechazó el segundo intento con el mismo código.
   - **Prueba de Bloqueo por Fuerza Bruta (`RN-002`):** Se provocaron 3 errores consecutivos de contraseña/MFA, disparándose el bloqueo de 15 minutos con mensaje HTTP 423.
   - **Prueba de Revocación en Logout:** Se cerró sesión y se demostró que el token previo queda inservible al llamar a `/api/auth/me` (HTTP 401: Token revocado).
4. **Verificación Automatizada con Pytest:**
   - Se ejecutó el comando de pruebas en vivo, evidenciando **12 tests unitarios e integrales en verde** y un **91% de cobertura de código**, superando ampliamente la meta del 80%.

---

## Pendientes

Para el siguiente ciclo de desarrollo (**Sprint 2**), se acuerda abordar los siguientes requerimientos del Product Backlog:

1. **HU-06: Gestión de Pedidos y Puntos de Entrega:** Registro de pedidos con peso, volumen, ventana de entrega y coordenadas de latitud/longitud en Lima Metropolitana.
2. **HU-07: Motor de Optimización de Rutas con Google OR-Tools:** Algoritmo de ruteo vehicular capacitado (CVRP) minimizando distancia recorrida y tiempo total.
3. **HU-08: Estimador de Emisiones de CO₂:** Cálculo matemático de huella de carbono estimada por ruta comparando ruta optimizada vs. ruta empírica.
4. **Persistencia Relacional en PostgreSQL con Alembic:** Migración del almacenamiento de usuarios y sesiones hacia base de datos PostgreSQL en contenedor Docker.

---

[⬅ Volver al README principal](../../README.md)
