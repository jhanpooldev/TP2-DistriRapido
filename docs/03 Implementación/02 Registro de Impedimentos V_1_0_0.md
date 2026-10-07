# Registro de impedimentos

[← Volver al README principal](../../README.md)

---

**Nombre del Proyecto:** EcoLogística Lima – Optimizador de Rutas Sostenibles para DistriRápido S.A.C.

**Líder del Proyecto:** Jhunior Harold Cosme Tenorio

**Sprint:** 1

**Periodo:** 05/10/2026 – 18/10/2026

---

## Control de Versiones del Documento

| Versión | Fecha | Autor | Descripción del Cambio |
|:---:|:---:|:---|:---|
| 1.0.0 | 18/10/2026 | Andrew Steven Vega Reyes / Jhunior Harold Cosme Tenorio | Registro de impedimentos del Sprint 1 (US-001, US-003, EN-01, EN-02). |

---

## Criterio de registro

Se registran únicamente los impedimentos que pueden evidenciarse a partir del
repositorio: o bien una corrección verificable en el código, o bien una prueba que la
respalda, o bien una limitación documentada que siga vigente. Las fechas corresponden
al periodo del Sprint 1 definido en `docs/planificacion/01`.

---

## Matriz de Registro de Impedimentos

| Impedimento # | Fecha de Registro | Descripción del Impedimento así como el Impacto en el Proyecto | Prioridad | Reportado por | Fecha tope de Resolución | Estado | Fecha de Resolución | Resolución/Comentarios |
|:---:|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---|
| **IMP-01** | 06/10/2026 | **Dependencia de validación de correo ausente.** Los esquemas de usuario no podían validarse por falta del paquete `email-validator`, que Pydantic requiere para el tipo `EmailStr`. **Impacto:** la API no arrancaba y la suite de pruebas no podía ejecutarse, bloqueando US-001 y US-003 desde el inicio del sprint. | Alta | Jhanpool Ernesto Flores Torres | 07/10/2026 | Resuelto | 06/10/2026 | Se incorporó `email-validator==2.2.0` a `src/backend/requirements.txt` y se instaló en el entorno virtual. Los esquemas de usuario y de registro quedaron operativos. |
| **IMP-02** | 07/10/2026 | **La distancia euclidiana plana subestimaba los trayectos entre distritos alejados de Lima.** Calcular la distancia como diferencia de coordenadas producia rutas subóptimas y tiempos de entrega incorrectos. **Impacto:** US-003 quedaba incumplido en su sustancia: el sistema entregaba un orden de visita que no correspondía a la distancia real recorrida. | Alta | Jhanpool Ernesto Flores Torres | 09/10/2026 | Resuelto | 08/10/2026 | Se implementó la fórmula del semiverseno (Haversine) con el radio terrestre R = 6 371 km en `haversine()`. La prueba `test_haversine_distancia_conocida` acota el resultado entre 1 850 y 1 930 km para un par de coordenadas de referencia. |
| **IMP-03** | 08/10/2026 | **Coste factorial inviable del cálculo de rutas.** La búsqueda exhaustiva de permutaciones crecía como O(n!) y hacía impracticable el cálculo a partir de una docena de puntos. **Impacto:** EN-01 era inalcanzable; el tiempo de respuesta superaba con creces el SLA de 5 segundos del RNF-01. | Crítica | Jhanpool Ernesto Flores Torres | 11/10/2026 | Resuelto | 10/10/2026 | Se adoptó la heurística Vecino Más Cercano como solución constructiva inicial, refinada con la búsqueda local 2-opt. El tiempo medido con 20 puntos fue del orden de 20 ms. |
| **IMP-04** | 10/10/2026 | **El cálculo de rutas no respetaba la cantidad mínima de puntos.** Era posible solicitar el cálculo con un solo punto de entrega. **Impacto:** Incumplimiento de la regla **RN-010** y del criterio de aceptación de US-003, que exige un mensaje indicando que se requieren al menos dos puntos. | Media | Ricardo David Tucto Ubaldo | 12/10/2026 | Resuelto | 11/10/2026 | La API valida el mínimo de puntos y responde `400` con el requisito. En la interfaz, las acciones de cálculo y confirmación permanecen deshabilitadas mientras no se cumpla la condición. |
| **IMP-05** | 12/10/2026 | **Puntos de entrega visibles para cualquier operador.** El listado de puntos no se filtraba por operador, por lo que un usuario autenticado podía observar los puntos registrados por otro. **Impacto:** Ruptura del aislamiento de datos entre usuarios y de **RN-001** en su vertiente de acceso al recurso propio. | Alta | Andrew Steven Vega Reyes | 14/10/2026 | Resuelto | 13/10/2026 | El listado devuelve únicamente los puntos del operador autenticado. El aislamiento se verifica en `src/backend/auditoria_api.py`, que comprueba que un operador nuevo no ve ni accede a los puntos ni a las rutas de otro. |
| **IMP-06** | 14/10/2026 | **Respuesta de `/auth/me` sin información de rol.** El endpoint devolvía los datos del usuario pero no su rol, por lo que la interfaz no podía distinguir a un administrador de un operador. **Impacto:** EN-02 quedaba incompleto en su parte de control de acceso por rol (**RN-003**). | Media | Ricardo David Tucto Ubaldo | 16/10/2026 | Resuelto | 15/10/2026 | `UsuarioResponse` incorporó el objeto `rol` anidado con su identificador y nombre. La prueba asociada verifica que el rol se devuelve y que el hash de la contraseña nunca se expone. |
| **IMP-07** | 16/10/2026 | **El cifrado en tránsito (HTTPS) no está resuelto.** La aplicación sirve HTTP sobre localhost y no existe configuración de certificado TLS en el repositorio. **Impacto:** EN-02 no puede declararse completo: la mitad del RNF-02, relativa a que toda comunicación viaje cifrada, sigue abierta. | Media | Jhunior Harold Cosme Tenorio | 18/10/2026 | **Abierto** | — | Se documenta como pendiente y se traslada al ambiente de despliegue, que queda fuera del PMV local. No se implementó mitigación en el código de la aplicación. |
| **IMP-08** | 16/10/2026 | **Clave de firma JWT con valor por defecto en el código.** `src/backend/app/core/config.py` define un valor por defecto para `JWT_SECRET`, de modo que, si `.env` no está configurado, la aplicación firmaría tokens con una clave conocida y documentada en el propio repositorio. **Impacto:** Riesgo para **RN-006** y para la validez de la autenticación de EN-02. | Alta | Andrew Steven Vega Reyes | 18/10/2026 | **Abierto** | — | Se verificó que `.env.example` solicita generar una clave aleatoria y que el `.env` local la define, y se documentó el riesgo. La eliminación del valor por defecto en el código no se realizó en este sprint. |
| **IMP-09** | 17/10/2026 | **Bloqueo por intentos fallidos (RN-002) no implementado.** La regla de bloqueo tras tres intentos durante 15 minutos, definida en `docs/inicio/09`, no tiene implementación en `src/backend`. **Impacto:** El login no mitiga ataques de fuerza bruta, lo que debilita la postura de seguridad que EN-02 debía establecer. | Media | Jhunior Harold Cosme Tenorio | 18/10/2026 | **Abierto** | — | Se registra como pendiente. La regla no formaba parte de los criterios de aceptación de EN-02, por lo que no bloqueó el cierre del elemento, pero queda incorporada a las acciones del Sprint 2. |
| **IMP-10** | 18/10/2026 | **Con exactamente tres puntos, la búsqueda 2-opt no se ejecuta.** En `two_opt` el rango de recorrido es `range(1, len(best) - 2)`, que queda vacío cuando hay tres puntos, de modo que la búsqueda local no revierte ningún segmento y la ruta devuelta es la del Vecino Más Cercano sin refinar. **Impacto:** Si el orden en que el cliente envía los puntos resulta mejor que el del Vecino Más Cercano, la API puede informar `distancia_total_km` levemente mayor que `distancia_sin_optimizar_km`. El ahorro no se vuelve negativo porque `calcular_ahorro` lo acota en cero, pero el ahorro real del caso queda en cero. Con cuatro o más puntos la búsqueda sí actúa. | Media | Jhanpool Ernesto Flores Torres | 01/11/2026 | **Abierto** | — | Se documenta como limitación conocida. El endpoint `POST /api/v1/rutas/optimizar` es válido y su SLA de 5 segundos se cumple con holgura; el defecto afecta la calidad del resultado y no la disponibilidad del servicio. Corrección propuesta: ampliar el rango de `two_opt` y comparar siempre el resultado contra el orden de entrada. |

---

## Resumen

| Estado | Cantidad |
|:---:|:---:|
| Resueltos | 6 |
| Abiertos | 4 |
| **Total** | **10** |

Los cuatro impedimentos abiertos (IMP-07, IMP-08, IMP-09 e IMP-10) se trasladan como
pendientes en el Informe de Estado y en la Revisión del Sprint, y su tratamiento se
detalla en las acciones de la Retrospectiva.

---

[← Volver al README principal](../../README.md)