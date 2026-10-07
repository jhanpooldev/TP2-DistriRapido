# Informe de estado del proyecto

[← Volver al README principal](../../README.md)

---

**Nombre del Proyecto:** EcoLogística Lima – Optimizador de Rutas Sostenibles para DistriRápido S.A.C.

**Líder del Proyecto:** Jhunior Harold Cosme Tenorio

**Sprint:** 1 – Registrador de puntos de entrega y primer motor de ruteo

**Periodo:** 05/10/2026 – 18/10/2026

---

## Control de Versiones del Documento

| Versión | Fecha | Autor | Descripción del Cambio |
|:---:|:---:|:---|:---|
| 1.0.0 | 18/10/2026 | Jhunior Harold Cosme Tenorio / Equipo EcoLogística | Elaboración del Informe de Estado del Sprint 1 (US-001, US-003, EN-01, EN-02). |

---

## 1. Alcance comprometido del Sprint 1

El Sprint 1 se definió en el backlog priorizado de
`docs/planificacion/01 Transformando a ágil V_1_0_0.md` (secciones 1.1 y 2) con cuatro
elementos y 21 Story Points:

| ID | Elemento | Tipo | Épica | SP |
|---|---|---|---|:---:|
| US-001 | Registrar puntos de entrega de una ruta | Historia de Usuario | EP-01 | 3 |
| US-003 | Generar ruta optimizada por distancia y tiempo | Historia de Usuario | EP-02 | 8 |
| EN-01 | Optimizar el rendimiento del algoritmo de ruteo | Enabler | EP-02 | 5 |
| EN-02 | Implementar autenticación segura (JWT + HTTPS) | Enabler | EP-01 | 5 |
| | **Total comprometido** | | | **21** |

---

## 2. Resumen del estado al cierre

| Elemento | SP | Estado | Evidencia en el repositorio |
|---|:---:|:---:|---|
| US-001 | 3 | Completada | `src/backend/app/api/v1/endpoints/puntos.py`, pestaña de puntos en `src/frontend/src/components/Dashboard.jsx` |
| US-003 | 8 | Completada | `src/backend/app/services/optimizer/__init__.py`, `POST /api/v1/rutas/optimizar` |
| EN-01 | 5 | Completada | `test_rendimiento_veinte_puntos_menor_a_cinco_segundos` en `src/backend/tests/test_optimizer.py` |
| EN-02 | 5 | **Parcial** | JWT implementado en `src/backend/app/core/security.py`; HTTPS no implementado |

**Resultado:** 16 de 21 Story Points completados (76 %). Los 5 Story Points
correspondientes a EN-02 quedan parcialmente entregados.

---

## 3. Historias de Usuario completadas en este Sprint

### US-001 — Registrar puntos de entrega de una ruta (3 SP)

*Épica EP-01. Criterio de aceptación: el operador registra los puntos y el sistema los
muestra en la lista; una dirección que no puede geolocalizarse produce un error y no
se agrega.*

Trabajo implementado:

- API `POST /api/v1/puntos-entrega` con validación de dirección obligatoria
  (**RN-007**), latitud entre −90 y 90, longitud entre −180 y 180 y peso mayor que
  cero (**RN-008**).
- API `GET /api/v1/puntos-entrega` que devuelve únicamente los puntos del operador
  autenticado, verificado en `src/backend/auditoria_api.py`.
- Endpoints de geocodificación `GET /api/v1/geocoding/search` y
  `GET /api/v1/geocoding/reverse`, que permitió el criterio de error ante una
  dirección no geolocalizable.
- Interfaz con formulario de alta, selección de coordenadas sobre el mapa mediante
  `MapPicker` y tabla con los puntos registrados.

**Estado: completada.**

### US-003 — Generar ruta optimizada por distancia y tiempo (8 SP)

*Épica EP-02. Criterio de aceptación: entre 2 y 20 puntos válidos, el sistema devuelve
el orden óptimo de visita en menos de 5 segundos; con un solo punto indica que se
requieren al menos 2.*

Trabajo implementado:

- Motor de ruteo propio con tres funciones en
  `src/backend/app/services/optimizer/__init__.py`:
  - `haversine` para la distancia geodésica entre coordenadas, en lugar de una
    distancia euclidiana plana que subestimaba los trayectos entre distritos
    alejados de Lima.
  - `nearest_neighbor` para construir una secuencia inicial partiendo del centro de
    distribución (**RN-011**).
  - `two_opt` para refinar la secuencia intercambiando aristas y reducir la distancia
    sin perder ninguno de los puntos.
- `POST /api/v1/rutas/optimizar` devuelve el orden calculado sin persistir, y
  `POST /api/v1/rutas` lo confirma y guarda (**RN-012**).
- Validación de cantidad mínima de puntos (**RN-010**): con menos de dos puntos la API
  responde `400` indicando el requisito.
- Cálculo de distancia total (**RN-015**), tiempo estimado (**RN-016**) y emisiones de
  CO₂ (**RN-017**) con los parámetros del vehículo asignado, y control de capacidad
  vehicular (**RN-014**).
- En la interfaz, los botones **Optimizar (Simular)** y **Confirmar y Guardar**
  permanecen deshabilitados mientras no se cumplan las condiciones de cálculo.

**Estado: completada.**

### EN-01 — Optimizar el rendimiento del algoritmo de ruteo (5 SP)

*Épica EP-02. Es el Enabler del requerimiento no funcional RNF-01: respuesta en menos
de 5 segundos para 20 puntos.*

Trabajo implementado:

- Se descartó la enumeración exhaustiva de permutaciones, cuyo costo factorial resultaba
  inviable a partir de una docena de puntos, y se adoptó la heurística
  Vecino Más Cercano seguida de 2-opt, de complejidad polinómica.
- El límite de 20 puntos por ruta se declara en configuración
  (`MAX_PUNTOS_POR_RUTA`) y la API responde con un error controlado si se supera.

**Verificación.** La prueba `test_rendimiento_veinte_puntos_menor_a_cinco_segundos`
mide cinco ejecuciones con 20 puntos y exige que la más lenta sea menor a 5 segundos.
Las duraciones obtenidas en el entorno del proyecto fueron:

| Ejecución | 1 | 2 | 3 | 4 | 5 |
|---|:---:|:---:|:---:|:---:|:---:|
| Tiempo | 20.2 ms | 20.0 ms | 19.8 ms | 17.9 ms | 18.3 ms |

Máximo registrado: **20.2 ms**, muy por debajo del SLA de 5 segundos.

**Estado: completada.**

### EN-02 — Implementar autenticación segura (JWT + HTTPS) (5 SP)

*Épica EP-01. Es el Enabler del requerimiento no funcional RNF-02: acceso con
autenticación y comunicación cifrada.*

Trabajo implementado (la parte de autenticación):

- Emisión de tokens JWT firmados con HS256 y caducidad configurable
  (`JWT_EXPIRE_HOURS`), ver **RN-005**.
- Contraseñas almacenadas con hash bcrypt irreversible, ver **RN-004**.
- Verificación de firma y caducidad del token en cada petición a un endpoint
  protegido; sin token o con token inválido la API responde `401`.
- Control de acceso por rol: Administrador, Operador Logístico y Gerente, ver
  **RN-003**.
- `POST /api/v1/auth/login` y `GET /api/v1/auth/me`.
- Pruebas en `src/backend/tests/test_security.py` que cubren hash y verificación de
  contraseña, decodificación de un token válido, rechazo de un token inválido, rechazo
  de un token firmado con otra clave y rechazo de un token expirado.

Trabajo **no** implementado:

- El cifrado en tránsito (HTTPS/TLS) no está implementado en el código de la
  aplicación. `src/backend` sirve HTTP sobre localhost y no existe configuración de
  certificado en el repositorio. El cifrado en tránsito queda a cargo del ambiente de
  despliegue, que no forma parte del PMV local.

**Estado: parcialmente completada.** La autenticación por token está resuelta y
verificada; el requisito de comunicación cifrada sigue abierto.

---

## 4. Demostración del trabajo completado

La demostración del Sprint 1 corresponde al incremento efectivamente construido y es
reproducible sobre la aplicación en ejecución. **No se afirma que una sesión de
demostración ante stakeholders se haya realizado**, porque el repositorio no registra
evidencia de ese evento.

Con el backend en ejecución y el frontend en `http://localhost:5173`:

1. **Autenticación (EN-02).** Se inicia sesión con `operador@distrirapido.com` /
   `operador123`. Se consulta `GET /api/v1/auth/me` y se observa que la respuesta
   incluye el rol del usuario. Se repite la llamada sin token y se obtiene `401`.
2. **Registro de puntos (US-001).** En la pestaña de puntos se agrega una dirección;
   el sistema la geocodifica, permite ajustar las coordenadas sobre el mapa y la
   registra. La tabla muestra el punto añadido. Una dirección no geolocalizable
   produce un mensaje de error y no se agrega a la lista.
3. **Generación de ruta (US-003).** Con dos o más puntos se pulsa **Optimizar
   (Simular)**: la respuesta indica el orden óptimo de visita, la distancia, el tiempo
   estimado y el CO₂ estimado. Con un solo punto, el botón permanece deshabilitado y la
   API responde `400` si se invoca directamente.
4. **Rendimiento (EN-01).** Se mide la respuesta con 20 puntos; se obtiene un tiempo
   del orden de milisegundos, muy por debajo de los 5 segundos exigidos.

En el backend, la verificación se apoya en herramientas versionadas:

- `pytest` — 51 pruebas en verde.
- `src/backend/auditoria_api.py` — auditoría de extremo a extremo que ejercita cada
  endpoint, incluido el aislamiento entre usuarios, y finaliza sin anomalías.

---

## 5. Pendientes

Estos puntos no forman parte de los entregables del Sprint 1 y deben gestionarse en
iteraciones posteriores:

1. **HTTPS / RNF-02 (cierre de EN-02).** El cifrado en tránsito no está implementado;
   corresponde definirlo en el ambiente de despliegue.
2. **RN-002 — Bloqueo por intentos fallidos.** La regla de bloqueo tras tres intentos
   durante 15 minutos, definida en `docs/inicio/09`, no está implementada en
   `src/backend`.
3. **Clave de firma con valor por defecto.** `src/backend/app/core/config.py` define un
   valor por defecto para `JWT_SECRET`, de modo que la aplicación firmaría tokens con
   una clave conocida si `.env` no estuviera configurado. El archivo `.env.example`
   solicita cambiarla y el `.env` local sí la define, pero el valor por defecto en el
   código es un riesgo que conviene eliminar.
4. **Autenticación multifactor.** `docs/inicio/14. Especificación MFA y Sesiones`
   describe un módulo de MFA con TOTP que **no está implementado** en `src/backend`. Se
   mantiene como especificación pendiente.
5. **Con tres puntos exactos, la búsqueda local 2-opt no se ejecuta.** El rango
   recorrido por `two_opt` en `src/backend/app/services/optimizer/__init__.py` queda
   vacío con tres puntos, por lo que la ruta devuelta es la del Vecino Más Cercano sin
   refinar. Si el orden de entrada resulta mejor, la API puede informar una distancia
   optimizada ligeramente mayor que la no optimizada; el ahorro no llega a ser negativo
   porque se acota en cero. Con cuatro o más puntos la búsqueda actúa con normalidad.
6. **Pruebas automatizadas del frontend.** `src/frontend` no incluye pruebas; su
   verificación se limita a `npm run build`.
7. **US-002, US-004, US-005 y US-007** (Sprint 2) y **US-006, US-008 y EN-03**
   (Sprint 3).

Los entregables del Sprint 2 se encuentran archivados en `docs/03 Implementación/sprint 2/`.

---

[← Volver al README principal](../../README.md)