# Registro de impedimentos

[⬅ Volver al README principal](../../README.md)

---

**Nombre del Proyecto:** EcoLogística Lima – Optimizador de Rutas Sostenibles para DistriRápido S.A.C.

**Líder del Proyecto:** Jhunior Harold Cosme Tenorio

---

## Control de Versiones del Documento

| Versión | Fecha | Autor | Descripción del Cambio |
|:---:|:---:|:---|:---|
| 1.0.0 | 01/10/2026 | Andrew Steven Vega Reyes / Jhunior Harold Cosme Tenorio | Registro inicial de impedimentos técnicos del Sprint 1 (Autenticación y Seguridad). |
| 1.1.0 | 15/10/2026 | Andrew Steven Vega Reyes / Jhunior Harold Cosme Tenorio | Incorporación y resolución de impedimentos técnicos y matemáticos del Sprint 2 (Optimización de Rutas). |

---

## Matriz de Registro de Impedimentos

| Impedimento # | Fecha de Registro | Descripción del Impedimento así como el Impacto en el Proyecto | Prioridad | Reportado por | Fecha tope de Resolución | Estado | Fecha de Resolución | Resolución/Comentarios |
|:---:|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---|
| **IMP-01** | 20/09/2026 | **Falta de biblioteca para validación de emails en Pydantic:** Al ejecutar los esquemas de validación de usuarios en Python 3.14, Pydantic arrojó error por ausencia de `email-validator`. **Impacto:** Bloqueó el arranque de la API y los tests unitarios. | Alta | Jhanpool Ernesto Flores Torres | 22/09/2026 | Resuelto | 21/09/2026 | Se incorporó `email-validator>=2.2.0` al `requirements.txt` y se instaló en el entorno virtual `.venv`. Pruebas validadas al 100%. |
| **IMP-02** | 22/09/2026 | **Restricción de directiva de ejecución en PowerShell Windows:** La directiva de seguridad del sistema operativo impedía la invocación de scripts `.ps1` de npm (`ExecutionPolicy: Restricted`). **Impacto:** Imposibilidad de ejecutar comandos CLI de frontend en terminales PowerShell estándar. | Media | Ricardo David Tucto Ubaldo | 25/09/2026 | Resuelto | 23/09/2026 | Se documentó la invocación directa mediante `npm.cmd` o terminal Git Bash, garantizando compatibilidad multiplataforma. |
| **IMP-03** | 24/09/2026 | **Riesgo de bypass de MFA en Paso 1:** No se definía qué credencial se retornaba al validar contraseña antes de ingresar el código TOTP. **Impacto:** Riesgo de vulnerabilidad si se entregaba un token con privilegios plenos. | Crítica | Jhanpool Ernesto Flores Torres | 27/09/2026 | Resuelto | 26/09/2026 | Se implementó el token efímero `mfa_token` (5 min, scope `mfa_pending`) sin permisos sobre rutas de negocio hasta superar el paso 2. |
| **IMP-04** | 26/09/2026 | **Falsos rechazos por desincronización de reloj (*Clock Drift*) en TOTP:** Teléfonos móviles con desfase de algunos segundos fallaban al enviar códigos de 6 dígitos. **Impacto:** Bloqueo de operadores legítimos. | Alta | Andrew Steven Vega Reyes | 29/09/2026 | Resuelto | 28/09/2026 | Se configuró tolerancia de ventana de tiempo `valid_window = 1` (±30s) en `pyotp` acorde al estándar RFC 6238. |
| **IMP-05** | 28/09/2026 | **Tokens JWT reutilizables post-logout (Falta de revocación):** Al usar tokens sin estado, las sesiones seguían válidas tras cerrar sesión. **Impacto:** No cumplimiento con OWASP ASVS. | Alta | Jhunior Harold Cosme Tenorio | 30/09/2026 | Resuelto | 29/09/2026 | Se incorporó el claim `jti` y una lista de revocación en memoria que invalida el token de inmediato al invocar `/api/auth/logout`. |
| **IMP-06** | 29/09/2026 | **Bloqueo por fuerza bruta (RN-002) no cubría el segundo factor:** El umbral de 3 intentos solo evaluaba contraseñas y no códigos MFA. **Impacto:** Riesgo de ataques de fuerza bruta sobre los códigos TOTP. | Alta | Jhanpool Ernesto Flores Torres | 01/10/2026 | Resuelto | 30/09/2026 | Se unificó el contador de intentos fallidos en `/api/auth/mfa/verify`, bloqueando la cuenta por 15 minutos ante 3 fallos consecutivos. |
| **IMP-07** | 04/10/2026 | **Discrepancia en distancias geográficas por curvatura terrestre:** El cálculo euclidiano plano arrojaba errores significativos de distancia entre distritos distantes de Lima (ej. Puente Piedra vs. Lurín). **Impacto:** Rutas subóptimas y tiempos de entrega mal calculados. | Alta | Jhanpool Ernesto Flores Torres | 07/10/2026 | Resuelto | 06/10/2026 | Se implementó la fórmula ortodrómica del semiverseno (Haversine con radio terrestre R = 6,371 km), logrando precisión métrica en coordenadas geográficas. |
| **IMP-08** | 07/10/2026 | **Complejidad computacional NP-Hard en rutas con múltiples puntos:** El cálculo por fuerza bruta factorial `O(n!)` congelaba el servidor con más de 12 puntos de entrega. **Impacto:** Tiempos de respuesta inaceptables en la API superando los 60 segundos. | Crítica | Jhanpool Ernesto Flores Torres | 10/10/2026 | Resuelto | 09/10/2026 | Se implementó la heurística de optimización combinatoria 2-opt precedida por el Vecino Más Próximo, resolviendo rutas de 50 puntos en menos de 0.8 segundos (`O(n²)`). |
| **IMP-09** | 09/10/2026 | **Falta de factor de emisión de CO₂ estandarizado para la flota:** No se contaba con coeficientes de emisión diferenciados por tipo de combustible en el contexto peruano. **Impacto:** Cálculos ambientales poco creíbles o inconsistentes ante auditorías de sostenibilidad. | Media | Jhunior Harold Cosme Tenorio | 12/10/2026 | Resuelto | 11/10/2026 | Se calibraron factores de emisión oficiales del MINAM y GHG Protocol para reparto urbano: Diésel (0.240 kg/km), GNV (0.180 kg/km) y Eléctrico (0.045 kg/km). |
| **IMP-10** | 11/10/2026 | **Sobrecarga de vehículos sin validación previa de capacidad:** El modelo permitía generar rutas aun cuando la suma de carga de los paquetes superaba la capacidad de la van. **Impacto:** Violación de la regla de negocio `RN-008` y riesgo operativo real. | Alta | Ricardo David Tucto Ubaldo | 13/10/2026 | Resuelto | 12/10/2026 | Se incorporó validación estricta en el servicio de rutas que calcula la sumatoria de peso y rechaza con HTTP 400 detallando el exceso de carga en kilogramos. |

---

[⬅ Volver al README principal](../../README.md)
