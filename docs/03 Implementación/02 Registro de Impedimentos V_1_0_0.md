# Registro de impedimentos

[⬅ Volver al README principal](../../README.md)

---

**Nombre del Proyecto:** EcoLogística Lima – Optimizador de Rutas Sostenibles para DistriRápido S.A.C.

**Líder del Proyecto:** Jhunior Harold Cosme Tenorio

---

## Control de Versiones del Documento

| Versión | Fecha | Autor | Descripción del Cambio |
|:---:|:---:|:---|:---|
| 1.0.0 | 01/10/2026 | Andrew Steven Vega Reyes / Jhunior Harold Cosme Tenorio | Registro formal y consolidación de impedimentos técnicos y operativos del Sprint 1. |

---

## Matriz de Registro de Impedimentos

| Impedimento # | Fecha de Registro | Descripción del Impedimento así como el Impacto en el Proyecto | Prioridad | Reportado por | Fecha tope de Resolución | Estado | Fecha de Resolución | Resolución/Comentarios |
|:---:|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---|
| **IMP-01** | 20/09/2026 | **Falta de biblioteca para validación de emails en Pydantic:** Al ejecutar los esquemas de validación de usuarios en Python 3.14, Pydantic arrojó error de importación por ausencia de `email-validator`. **Impacto:** Bloqueó el arranque de la API y la ejecución de los tests unitarios. | Alta | Jhanpool Ernesto Flores Torres | 22/09/2026 | Resuelto | 21/09/2026 | Se incorporó la dependencia `email-validator>=2.2.0` al archivo `requirements.txt` y se instaló en el entorno virtual `.venv`. Pruebas de esquema validadas al 100%. |
| **IMP-02** | 22/09/2026 | **Restricción de directiva de ejecución de scripts en PowerShell Windows:** La directiva de seguridad del sistema operativo impedía la invocación de scripts `.ps1` de npm (`ExecutionPolicy: Restricted`). **Impacto:** Imposibilidad de ejecutar comandos CLI automáticos de frontend desde terminales PowerShell estándar. | Media | Ricardo David Tucto Ubaldo | 25/09/2026 | Resuelto | 23/09/2026 | Se documentó y estandarizó la ejecución invocando directamente `npm.cmd` o utilizando la terminal Bash integrada en Git, garantizando compatibilidad multiplataforma. |
| **IMP-03** | 24/09/2026 | **Riesgo de bypass de MFA en el Paso 1 de autenticación:** La especificación preliminar no definía qué credencial se retornaba al validar usuario y contraseña antes de ingresar el código TOTP. Si se emitía un token estándar, se vulneraba el doble factor. **Impacto:** Vulnerabilidad crítica de seguridad y ambigüedad en el diseño de la API. | Crítica | Jhanpool Ernesto Flores Torres | 27/09/2026 | Resuelto | 26/09/2026 | Se creó un token efímero de desafío (`mfa_token`) con validez estricta de 5 minutos y scope exclusivo (`mfa_pending`), el cual no permite el consumo de ningún endpoint protegido de negocio hasta completar el paso 2. |
| **IMP-04** | 26/09/2026 | **Falsos rechazos por desincronización de reloj (*Clock Drift*) en TOTP:** Dispositivos móviles con desfase de algunos segundos respecto al servidor fallaban al enviar códigos de 6 dígitos. **Impacto:** Bloqueo accidental de usuarios legítimos y degradación de la experiencia de usuario. | Alta | Andrew Steven Vega Reyes | 29/09/2026 | Resuelto | 28/09/2026 | Se configuró el motor `pyotp` con tolerancia de ventana de tiempo `valid_window = 1` (±30 segundos), absorbiendo variaciones de sincronización horaria de los teléfonos conforme a RFC 6238. |
| **IMP-05** | 28/09/2026 | **Tokens JWT reutilizables tras cierre de sesión (Falta de revocación):** Al utilizar JWT sin estado, un atacante con acceso a un token copiado podía seguir consumiendo la API aunque el usuario hubiera pulsado "Cerrar Sesión". **Impacto:** Riesgo de secuestro de sesión y no cumplimiento del estándar OWASP ASVS. | Alta | Jhunior Harold Cosme Tenorio | 30/09/2026 | Resuelto | 29/09/2026 | Se incorporó el claim `jti` (JWT ID único) en cada token y se implementó una lista negra de revocación en memoria que invalida el `jti` inmediatamente al llamar `/api/auth/logout`. |
| **IMP-06** | 29/09/2026 | **Regla de bloqueo por reintentos (RN-002) no cubría el paso de verificación MFA:** Inicialmente el bloqueo por 3 intentos fallidos solo se aplicaba al ingreso de contraseña y no al ingreso del código de 6 dígitos. **Impacto:** Posibilidad de ataques de fuerza bruta automatizados sobre los 1,000,000 de códigos posibles de TOTP. | Alta | Jhanpool Ernesto Flores Torres | 01/10/2026 | Resuelto | 30/09/2026 | Se integró el contador de intentos fallidos y el disparador de bloqueo por 15 minutos en el endpoint `/api/auth/mfa/verify`, protegiendo integralmente ambos factores de autenticación. |

---

[⬅ Volver al README principal](../../README.md)
