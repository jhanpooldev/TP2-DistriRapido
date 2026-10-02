# Revisión del sprint

[⬅ Volver al README principal](../../README.md)

---

**Nombre del Proyecto:** EcoLogística Lima – Optimizador de Rutas Sostenibles para DistriRápido S.A.C.

**Líder del Proyecto:** Jhunior Harold Cosme Tenorio

---

## Control de Versiones del Documento

| Versión | Fecha | Autor | Descripción del Cambio |
|:---:|:---:|:---|:---|
| 1.0.0 | 01/10/2026 | Jhunior Harold Cosme Tenorio / Equipo EcoLogística | Elaboración inicial del Informe de Estado correspondiente al cierre del Sprint 1. |

---

## 1. Resumen Ejecutivo del Sprint 1

Durante el **Sprint 1** (periodo del 18/09/2026 al 01/10/2026), el equipo de desarrollo de **EcoLogística Lima** se enfocó en consolidar la arquitectura base de software, el pipeline de desarrollo bajo estándares OpenSpec, la especificación desambiguada y la implementación funcional del módulo crítico de **Autenticación Multifactor (MFA/2FA) y Gestión Segura del Ciclo de Vida de Sesiones**.

El objetivo central del Sprint fue mitigar los riesgos de acceso no autorizado y suplantación de identidad para los operadores y administradores de **DistriRápido S.A.C.**, implementando políticas estrictas de ciberseguridad alineadas con las reglas de negocio del proyecto (`RN-001` a `RN-006`) y las recomendaciones OWASP ASVS v4.0.

- **Velocidad Planificada:** 26 Puntos de Historia (Story Points).
- **Velocidad Completada:** 26 Puntos de Historia (100% de cumplimiento).
- **Estado General del Sprint:** Exitoso / En cronograma.

---

## 2. Historias de Usuario completadas en este Sprint

A continuación se detallan las Historias de Usuario (HU) desarrolladas, verificadas y puestas en funcionamiento durante la iteración:

### HU-01: Autenticación Primaria de Usuarios con Hashing Criptográfico (5 SP)
- **Descripción:** Como operador o administrador de DistriRápido S.A.C., deseo iniciar sesión mediante mi correo institucional y contraseña cifrada para acceder al sistema de forma segura.
- **Criterios de Aceptación Cumplidos:**
  - Validación de existencia de usuario y coincidencia de contraseña utilizando hashing irreversible `PBKDF2-HMAC-SHA256` con salt criptográfica aleatoria de 16 bytes e iteraciones controladas (`RN-004`).
  - Respuesta HTTP 200 en credenciales válidas; respuesta genérica HTTP 401 "Credenciales incorrectas" en fallo de autenticación para mitigar enumeración de usuarios (OWASP).
  - Emisión de sesión definitiva con token JWT (expiración de 8 horas según `RN-005`) para usuarios que no tengan MFA activado.

### HU-02: Enrolamiento y Configuración de MFA con TOTP y Código QR (5 SP)
- **Descripción:** Como usuario autenticado, deseo activar el segundo factor de autenticación en mi celular mediante Google Authenticator o Microsoft Authenticator para proteger mi cuenta contra accesos no autorizados.
- **Criterios de Aceptación Cumplidos:**
  - Generación de clave secreta aleatoria Base32 de 160 bits acorde al estándar RFC 6238.
  - Generación de URI estándar `otpauth://` y renderizado dinámico de imagen de Código QR en Base64 (`data:image/png;base64,...`) para escaneo directo desde dispositivos móviles.
  - Generación de 5 códigos alfanuméricos de respaldo de un solo uso hasheados con SHA-256 para situaciones de contingencia o pérdida del móvil.
  - Transición de estado segura: el MFA permanece inactivo hasta que el usuario confirme la posesión del dispositivo enviando un código de prueba válido de 6 dígitos a `/api/auth/mfa/enable`.

### HU-03: Desafío de Autenticación de Doble Factor y Códigos de Respaldo (5 SP)
- **Descripción:** Como usuario con MFA activado, deseo que el sistema me solicite el código de 6 dígitos de mi celular tras validar mi contraseña para completar un acceso de dos pasos.
- **Criterios de Aceptación Cumplidos:**
  - El paso 1 del login detecta el estado MFA y emite un token de desafío efímero (`mfa_token`) con validez estricta de 5 minutos y ámbito restringido (`scope: mfa_pending`), impidiendo acceso directo a los recursos de negocio.
  - El paso 2 (`/api/auth/mfa/verify`) valida el código de 6 dígitos con ventana de tiempo de 30 segundos y tolerancia de desfase de reloj (clock skew) de ±30s.
  - Soporte de acceso de emergencia mediante cualquiera de los 5 códigos de respaldo; al ser utilizado, el código queda marcado como consumido (`usado = true`), impidiendo ataques de repetición.

### HU-04: Gestión Segura de Sesiones y Revocación Inmediata en Logout (5 SP)
- **Descripción:** Como usuario del sistema, deseo cerrar mi sesión de forma definitiva para garantizar que nadie pueda reutilizar mis credenciales en caso de dejar el navegador abierto.
- **Criterios de Aceptación Cumplidos:**
  - Inclusión de identificador criptográfico único `jti` (JWT ID) en el payload de cada token emitido.
  - Al invocar `POST /api/auth/logout`, el `jti` se añade de manera inmediata a la lista de revocación (blacklist).
  - Cualquier consulta subsiguiente a `/api/auth/me` con un token revocado es rechazada con HTTP 401 "Token revocado. La sesión fue cerrada previamente".
  - Control de expiración absoluta de 8 horas (`RN-005`).

### HU-05: Protección contra Fuerza Bruta y Bloqueo de Cuenta (6 SP)
- **Descripción:** Como oficial de seguridad del sistema, deseo bloquear temporalmente las cuentas que acumulen intentos fallidos de inicio de sesión para impedir ataques de fuerza bruta y diccionario.
- **Criterios de Aceptación Cumplidos:**
  - Monitoreo continuo de intentos fallidos tanto en contraseña (Paso 1) como en código TOTP (Paso 2).
  - Al acumular **3 intentos fallidos consecutivos**, la cuenta queda bloqueada automáticamente por un periodo estricto de **15 minutos** (`RN-002`).
  - Respuestas HTTP 423 (Locked) detallando el tiempo restante de bloqueo e impidiendo autenticación incluso si se ingresa la clave correcta antes de expirar el bloqueo.

---

## 3. Demostración del trabajo completado

Demostración a los stakeholders de las funcionalidades implementadas.

La sesión de demostración del Sprint 1 se llevó a cabo ante el docente evaluador y el equipo técnico simulando el rol de la Gerencia de Operaciones de DistriRápido S.A.C., abarcando las siguientes evidencias funcionales:

1. **Inspección de la Especificación Formal y Auditoría de IA:**
   - Se presentó el documento formal `docs/01 Inicio/14. Especificacion MFA y Sesiones V_1_0_0.md` y los archivos OpenSpec (`auth_mfa_borrador.openspec.yaml` y `auth_mfa_final.openspec.yaml`), evidenciando cómo la IA auditó el borrador detectando ambigüedades en timeouts, desincronización de reloj y tokens zombies, las cuales fueron subsanadas con criterios BDD Gherkin.
2. **Exploración de la API en Swagger UI (`/docs`):**
   - Demostración interactiva de los 8 endpoints REST creados en FastAPI bajo el prefijo `/api/auth`, verificando schemas de validación de Pydantic, códigos de respuesta HTTP y documentación OpenAPI autogenerada.
3. **Flujo Visual Interactivo en el Panel Web (`http://localhost:8000/`):**
   - **Registro de Usuario:** Creación de usuario operador con validación de correo corporativo y contraseña de 8+ caracteres.
   - **Enrolamiento MFA en Vivo:** Generación en pantalla del Código QR dinámico y clave Base32; escaneo exitoso desde la aplicación Google Authenticator en teléfono móvil real.
   - **Confirmación con Código de 6 dígitos:** Activación exitosa de MFA en la cuenta.
   - **Demostración del Desafío en 2 Pasos:** Cierre de sesión, ingreso de contraseña en Paso 1 (recibiendo `mfa_required: true`), e ingreso del código dinámico en Paso 2 para acceder al panel.
   - **Demostración de Código de Respaldo:** Acceso simulado sin teléfono utilizando un código alfanumérico de 8 caracteres y posterior verificación de rechazo ante intento de reutilización.
   - **Demostración del Bloqueo por Fuerza Bruta (`RN-002`):** Ejecución de 3 intentos fallidos consecutivos provocando el bloqueo inmediato con código HTTP 423 por 15 minutos.
   - **Demostración de Revocación en Logout:** Invocación de logout e intento posterior de llamada a `/api/auth/me`, comprobando el rechazo por token revocado en lista negra.
4. **Ejecución de Pruebas Automatizadas en Terminal:**
   - Ejecución en vivo de la suite `pytest` obteniendo **12 pruebas automatizadas aprobadas (100% pass)** y una **cobertura de código del 91%**, superando el umbral del 80% exigido en la consigna.

---

## 4. Pendientes

Los elementos planificados que quedan en el Product Backlog para su ejecución en las siguientes iteraciones corresponden a:

1. **Módulo de Planificación y Optimización de Rutas (Sprint 2):**
   - Integración de la librería de optimización combinatoria Google OR-Tools para resolver el problema de rutas con restricciones de capacidad vehicular y ventanas horarias (CVRP / TSP).
2. **Módulo de Gestión de Pedidos y Puntos de Entrega (Sprint 2):**
   - Endpoints CRUD para registro, geocodificación de coordenadas (latitud/longitud) y validación de direcciones en Lima Metropolitana.
3. **Persistencia en Base de Datos PostgreSQL con Alembic (Sprint 2):**
   - Configuración de scripts de migración de base de datos relacional para migrar el repositorio en memoria hacia PostgreSQL 14+ manteniendo compatibilidad de interfaces.
4. **Desarrollo del Frontend Completo en React + Vite (Sprint 2 y 3):**
   - Traslado de los componentes del panel visual hacia la arquitectura modular de React con Context API y visualización de mapas con Leaflet / Mapbox.

---

[⬅ Volver al README principal](../../README.md)
