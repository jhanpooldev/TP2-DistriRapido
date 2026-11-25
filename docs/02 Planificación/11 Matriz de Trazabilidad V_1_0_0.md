[← Volver al README Principal](../../README.md)

# 11 Matriz de Trazabilidad: Documentación vs. Sistema

**Proyecto:** EcoLogística Lima – Optimizador de Rutas Sostenibles para DistriRápido S.A.C.  \
**Versión:** 1.0.0 | **Fecha de auditoría:** 23/11/2026  \
**Fuente de verdad:** `docs/02 Planificación/` y `docs/Arquitectura/` (`SPECS.md:5-8`).

> Esta matriz compara cada requisito documentado con el comportamiento **real** del código al
> momento de la auditoría. No marca como "Cumplido" un requisito por la existencia de un
> archivo con nombre parecido: se verificó la lógica ejecutable. Los estados son
> **Cumplido**, **Parcialmente cumplido**, **No implementado** y **No verificable**.
> Las contradicciones documentales se conservan y se enlazan desde la sección final.
>
> **Actualización del 25/11/2026:** se conserva la versión del archivo y la fecha de la
> auditoría original; las filas afectadas por el cierre del feedback final muestran el
> estado verificado en esa fecha posterior. El detalle de cada cambio está en la sección 7.

## 1. Requisitos Funcionales

| ID | Requisito documentado | Documento de origen | Ubicación en el código | Estado | Acción necesaria |
|:---|:---|:---|:---|:---|:---|
| RF-001 | Login con correo/contraseña, sesión con expiración y mensaje único de credenciales incorrectas | `05 Requisitos funcionales:36-53` | `backend/app/api/v1/endpoints/auth.py:36-51`; `core/security.py:15-25` | Cumplido | Ninguna. Se verificó bcrypt, JWT de 8 h y 401 uniforme. |
| RF-002 | Alta de usuarios por administrador; **sin rol debe asignarse "Operador Logístico" por defecto** | `05 Requisitos funcionales:57-74` | `schemas/__init__.py` (`id_rol` opcional); `auth.py:20-54` (`resolver_id_rol`); `tests/test_auth_reglas.py` | Cumplido | Implementado y verificado: omisión de rol, rol inexistente y correo duplicado. |
| RF-003 | Control de acceso por rol (Administrador, Operador, Gerente) | `05 Requisitos funcionales:78-95`; `07 Usuarios roles y permisos:91-107` | `dependencies.py:13-73`; `Dashboard.jsx` (`tabsVisibles`, `puedeGestionar`); `RutasTab.jsx` (`soloLectura`); `indicadores.py` | Cumplido | Backend restringe escrituras y el frontend oculta formularios/acciones no autorizadas al Gerente; indicadores visibles para los tres roles. |
| RF-004 | Registro de puntos con dirección/coordenadas, peso y destinatario; rechazo de dirección inválida | `05 Requisitos funcionales:99-116` | `puntos.py:19-32`; `schemas/__init__.py:36-58`; `geocoding.py:118-215` | Cumplido | Ninguna. Coordenadas `(0,0)` rechazadas y búsqueda acotada a Perú. |
| RF-005 | Modificar y eliminar puntos que no estén en ruta confirmada | `05 Requisitos funcionales:120-137` | `puntos.py:79-140`; `Dashboard.jsx` (edición en línea y confirmación de borrado); `tests/test_puntos_reglas.py` | Cumplido | Implementado en UI y backend; mensaje de rechazo igual al documentado. |
| RF-006 | Ruta optimizada desde el centro, con al menos dos puntos | `05 Requisitos funcionales:141-158`; `RN-010` | `rutas.py:55-70,95-124`; `services/optimizer/__init__.py:23-71` | Cumplido | Ninguna. heurística Haversine + Vecino Más Cercano + 2-opt verificada por 10 pruebas. |
| RF-007 | Capacidad del vehículo; puntos excedentes **pendientes** | `05 Requisitos funcionales:162-179`; `RN-014` | `rutas.py:72-83` rechaza la ruta completa | **No verificable** | Ninguna: la desviación aprobada está registrada en CHANGELOG `:384-387` y en esta matriz (RN-014). No implementar sin nueva decisión. |
| RF-008 | Comparación de impacto (distancia, tiempo, CO₂) optimizada vs. no optimizada | `05 Requisitos funcionales:183-...`; `RN-018` | `optimizer/__init__.py:79-111`; `rutas.py:112-118` | Cumplido | Ninguna. Porcentajes nunca negativos; umbral 1 %. |
| RF-009 | Visualización del mapa con fallback tabular si falla el proveedor | `05 Requisitos funcionales:218-221` | `frontend/components/MapView.jsx:136-149,261-273,344-360` | Cumplido | Ninguna. Línea discontinua + aviso + Reintentar verificados. |
| RF-010 | Confirmación explícita antes de guardar; gestión de rutas | `05 Requisitos funcionales:...`; `RN-012` | `rutas.py:126-135` (optimizar stateless vs. confirmar persistente); `Dashboard.jsx:227-248` | Cumplido | Ninguna. |
| RF-011 | Histórico de rutas con filtros | `05 Requisitos funcionales:...` | `rutas.py:294-355`; `RutasTab.jsx:10-330` | Cumplido | Ninguna. Filtros por fecha/estado y paginación reales. |
| RF-012 | Indicadores de sostenibilidad a partir de rutas confirmadas | `05 Requisitos funcionales:...:288-305`; `RN-019` | `services/indicadores.py`; `endpoints/indicadores.py`; `IndicadoresTab.jsx`; `tests/test_indicadores.py` | Cumplido | Emisiones totales, por entrega y ahorro porcentual calculados sobre rutas confirmadas. |
| RF-013 | Panel del gerente: cantidad de rutas, distancia total y emisiones | `05 Requisitos funcionales:288-305`; `RN-020` | `IndicadoresTab.jsx`; `Dashboard.jsx` (pestaña "Indicadores"); `tests/test_indicadores.py` | Cumplido | Panel con rutas, distancia y emisiones; cero y aviso cuando no hay rutas. |
| RF-014 | Cierre de sesión explícito que invalide el acceso | `05 Requisitos funcionales:309-326`; `SPECS.md:261` | `security.py` (`jti` y revocación); `auth.py:89-97`; `Dashboard.jsx` (`cerrarSesion`) | Cumplido | El botón "Salir" revoca el token en backend y luego limpia la sesión local. |

## 2. Requisitos No Funcionales

| ID | Requisito documentado | Documento de origen | Ubicación en el código | Estado | Acción necesaria |
|:---|:---|:---|:---|:---|:---|
| RNF-001 | Ruta ≤5 s P95 con 20 puntos; ≤50 s con 50 puntos | `06 Requisitos no funcionales:22` | `tests/test_optimizer.py` (17.9–20.2 ms con 20) | Cumplido (20 pts) / No verificable (50 pts) | El límite de `MAX_PUNTOS_POR_RUTA=20` impide medir 50 puntos. Documentar alcance. |
| RNF-002 | Lectura ≤1,5 s P95 con ≤50 registros | `06 Requisitos no funcionales:23` | E2E `rendimiento.spec.js` mide API | No verificable | No hay informe P95 versionado con ese criterio. No inventar medición. |
| RNF-003 | ≥10 TPS, error ≤1 % | `06 Requisitos no funcionales:24` | Sin prueba de carga | No verificable | Requiere herramienta de carga no presente. |
| RNF-004 | 0 % accesos no autorizados; 401/403 en <300 ms | `06 Requisitos no funcionales:25` | `dependencies.py:13-73`; `client.js` (interceptor 401); `App.jsx` (`auth:expired`); `tests/test_rnf004_latencia.py` | Cumplido en medición local | 10 muestras con calentamiento: 401 mediana 2.96 ms / máxima 3.75 ms; 403 mediana 3.10 ms / máxima 3.50 ms. No sustituye el SLA en producción. |
| RNF-005 | 0 % vulnerabilidades OWASP explotables; 100 % entradas validadas | `06 Requisitos no funcionales:26` | Pydantic + `login_attempts.py` + 429 con `Retry-After`; HTTPS/CSP fuera del alcance local | Parcialmente cumplido | RN-002 y bloqueo por intentos implementados y probados; HTTPS/CSP siguen dependiendo de infraestructura. |
| RNF-006 | bcrypt al 100 % y 100 % de tráfico HTTPS | `06 Requisitos no funcionales:27` | `security.py:9-13` ✅; HSTS condicional en `main.py:139-144` | **Parcialmente cumplido** | HTTPS requiere terminación TLS/proveedor; fuera del entorno local. |
| RNF-007 | Disponibilidad ≥95 %; modo degradado sin mapa en 100 % de los casos | `06 Requisitos no funcionales:28` | `MapView.jsx:136-149,261-273`; `/health` con 503 | Cumplido (degradación) / No verificable (disponibilidad) | Sin monitoreo desplegado. |
| RNF-008 | Pérdida de datos 0 %; reintento sin duplicados | `06 Requisitos no funcionales:29` | `commit()` en escrituras; `rutas.py:275-289` | Parcialmente cumplido | Añadir rollbacks explícitos y validación de duplicados en `punto_ids`. |
| RNF-009 | Flujo en ≤3 pasos y ≤3 minutos | `06 Requisitos no funcionales:30` | Flujo real: registrar → seleccionar → optimizar → confirmar | No verificable | No hay medición de pasos/tiempo de usuario; SUS sin aplicar. |
| RNF-010 | WCAG 2.1 AA, contraste ≥4,5:1, 100 % campos etiquetados | `06 Requisitos no funcionales:31`; `Sprint 03/05 WCAG` | `Dashboard.jsx` (tabs y formularios); `index.css` (foco y `prefers-reduced-motion`); `MapPicker.jsx` (teclado) | Parcialmente cumplido | `aria-controls`, foco visible, movimiento reducido y marcador por teclado corregidos; auditoría WCAG completa sigue pendiente. |
| RNF-011 | Cobertura global ≥70 % (≥80 % en validación) | `06 Requisitos no funcionales:32` | `pytest --cov=app`: **74 %**; `vitest --coverage`: **87,03 % global** con componentes React | Cumplido | Medido el 25/11/2026: backend 74 % (1 218/312), frontend 87,03 % sentencias (819/941), 78,14 % ramas y 89,94 % líneas. El 93,07 % del 23/11 era solo de archivos instrumentados. |
| RNF-012 | Bajo acoplamiento y documentación actualizada | `06 Requisitos no funcionales:33` | Capas en backend; 61 documentos | Parcialmente cumplido | Service Layer/Repository ausente; no refactorizar sin decisión (ver contradicciones). |
| RNF-013 | Chrome/Edge/Firefox 100 % funcionalidades | `06 Requisitos no funcionales:34` | E2E en Chromium, Firefox y WebKit | Parcialmente cumplido | WebKit ≠ Safari; Edge no ejecutado. No afirmar cobertura total. |
| RNF-014 | Hosting gratuito, variables de entorno, 0 % gasto infraestructura | `06 Requisitos no funcionales:35` | `.env.example`; `client.js` usa `VITE_API_URL` con valor por defecto `/api/v1`; deploys desactivados | No verificable | La variable ya se consume sin cambiar el valor por defecto; sigue sin existir despliegue real que verificar. |
| RNF-015 | Errores esperados con mensaje descriptivo y estado consistente | `06 Requisitos no funcionales:36` | `HTTPException` en endpoints; `extraerError` y 401 global en `client.js` | Cumplido | Mensajes de RF-002/RF-005 alineados y sesión expirada tratada en todo el panel. |

## 3. Reglas de Negocio

| ID | Requisito documentado | Documento de origen | Ubicación en el código | Estado | Acción necesaria |
|:---|:---|:---|:---|:---|:---|
| RN-001 | Credenciales válidas para ingresar | `08 Reglas de negocio:14-16` | `auth.py:36-51`; `security.py:9-13` | Cumplido | Ninguna. |
| RN-002 | **3 intentos fallidos consecutivos → bloqueo de 15 minutos** | `08 Reglas de negocio:18-20` | `core/login_attempts.py`; `auth.py:57-86`; `tests/test_auth_reglas.py` | Cumplido | Tercer fallo bloquea 15 min; intentos posteriores devuelven 429 con `Retry-After`; login correcto reinicia el contador. |
| RN-003 | RBAC por rol | `08 Reglas de negocio:22-24` | `dependencies.py:61-73`; `Dashboard.jsx`; `RutasTab.jsx` | Cumplido | Igual que RF-003: permisos en backend y vistas de solo lectura para Gerente. |
| RN-004 | Contraseñas solo bcrypt | `08 Reglas de negocio:26-28` | `security.py:9-13` | Cumplido | Ninguna. |
| RN-005 | Sesión expira a las 8 horas | `08 Reglas de negocio:30-32` | `security.py` (expiración 8 h, `jti` y revocación); `auth.py:89-97` | Cumplido | Expiración y revocación explícita verificadas. |
| RN-006 | Secretos por entorno, sin exponer en errores | `08 Reglas de negocio:34-36` | `config.py` (`_secreto_de_desarrollo`, validadores); `.env.example`; `tests/test_sprint3.py` | Cumplido | Sin clave fija: en desarrollo se genera una clave efímera y se descartan ejemplos/vacíos; en Staging/Producción la variable es obligatoria y ≥32 caracteres. No se modificó `.env`. |
| RN-007 | Dirección/coordenada geocodificable | `08 Reglas de negocio:42-44` | `schemas/__init__.py:51-58`; `geocoding.py` | Parcialmente cumplido | La validación real depende del proveedor externo; se documenta el límite. |
| RN-008 | Peso > 0 | `08 Reglas de negocio:46-48` | `schemas/__init__.py:40` | Cumplido | Ninguna. |
| RN-009 | Puntos en rutas confirmadas no se modifican/eliminan ni se reasignan | `08 Reglas de negocio:50-52` | `puntos.py:79-140`; `rutas.py` (`_validar_puntos_disponibles` en crear/editar); pruebas de reglas | Cumplido | Bloqueo aplicado al confirmar, editar, modificar punto y eliminar punto; mensajes documentados. |
| RN-010 | Mínimo dos puntos | `08 Reglas de negocio:54-56` | `rutas.py:55-61`; `test_optimizer.py` | Cumplido | Ninguna. |
| RN-011 | Centro de distribución por `HOME_*` | `08 Reglas de negocio:58-61` | `config.py:37-39`; `optimizer:161-163` | Cumplido | Ninguna. |
| RN-012 | Confirmación antes de guardar | `08 Reglas de negocio:63-65` | `rutas.py:126-135` | Cumplido | Ninguna. |
| RN-013 | No eliminar rutas con entregas completadas | `08 Reglas de negocio:67-69` | `rutas.py` (`ESTADOS_CON_ENTREGAS`, `ESTADOS_EDITABLES`); `tests/test_rutas_reglas.py` | Cumplido | Edición y eliminación rechazadas en estados avanzados. |
| RN-014 | Capacidad; excedentes pendientes | `08 Reglas de negocio:75-77` | `rutas.py:72-83` | Parcialmente cumplido | Desviación aprobada en CHANGELOG `:384-387`: se rechaza la operación. Mantener y documentar. |
| RN-015 | Distancia = centro → paradas → centro | `08 Reglas de negocio:79-81` | `optimizer:64-71` | Cumplido | Ninguna. |
| RN-016 | Tiempo = distancia / velocidad | `08 Reglas de negocio:83-85` | `optimizer:76-77` | Cumplido | Ninguna. |
| RN-017 | CO₂ = km × consumo × factor | `08 Reglas de negocio:87-92` | `optimizer:73-74,113-115` | Cumplido | Ninguna. |
| RN-018 | Comparación sin porcentajes negativos | `08 Reglas de negocio:94-96` | `optimizer:79-111`; `test_sprint2.py` | Cumplido | Ninguna. |
| RN-019 | Indicadores de sostenibilidad sobre rutas confirmadas | `08 Reglas de negocio:98-100` | `services/indicadores.py`; `endpoints/indicadores.py`; `tests/test_indicadores.py` | Cumplido | Cálculo sobre rutas confirmadas; emisiones por entrega = total / entregas. |
| RN-020 | Indicadores logísticos del gerente (rutas, distancia, emisiones; cero si no hay rutas) | `08 Reglas de negocio:102-104` | `services/indicadores.py`; `IndicadoresTab.jsx`; `tests/test_indicadores.py` | Cumplido | Cero y mensaje cuando no hay rutas; totales agregados desde BD. |

## 4. Historias de usuario, entregables y criterios de aceptación

| ID | Requisito documentado | Documento de origen | Ubicación en el código | Estado | Acción necesaria |
|:---|:---|:---|:---|:---|:---|
| US-001 | Registrar punto de entrega | `01 Transformando a ágil:68-...` | `puntos.py:19-32`; `Dashboard.jsx:188-197,400-460` | Cumplido | Añadir `min`/`max` en el formulario para evitar 422 evitable. |
| US-002 | Editar/eliminar punto y recalcular ruta | `01 Transformando a ágil:...` | `Dashboard.jsx` (acciones de pedidos); `RutasTab.jsx` (edición de rutas); `puntos.py` | Cumplido | Igual que RF-005. |
| US-003 | 2–20 puntos en <5 s | `01 Transformando a ágil:...` | `rutas.py:55-70`; `test_optimizer.py` | Cumplido | Ninguna. |
| US-004 | CO₂ sin porcentajes negativos | `01 Transformando a ágil:...` | `optimizer:79-111` | Cumplido | Ninguna. |
| US-005 | Mapa con error controlado | `01 Transformando a ágil:...` | `MapView.jsx` | Cumplido | Ninguna. |
| US-006 | Detalle de parada en el mapa | `01 Transformando a ágil:...` | `MapView.jsx:25-77` (popups con `textContent`) | Cumplido | Ninguna. |
| US-007 | Búsqueda de rutas por fechas | `01 Transformando a ágil:...` | `rutas.py` (`_parsear_fecha` UTC); `RutasTab.jsx` (`ESTADOS` con Cancelada); `tests/test_rutas_reglas.py` | Cumplido | Fechas timezone-aware, estado Cancelada incluido y paginación `page`/`limit` con `X-Page` coherente. |
| US-008 | Exportar resumen CSV | `01 Transformando a ágil:...` | `exportacion.py:22-96`; `exportar.js:37-64` | Cumplido | Ninguna. |
| EN-01 | P95/5 s y degradación >20 puntos | `01 Transformando a ágil:...` | `config.py:42`; `test_optimizer.py` | Cumplido | Ninguna. |
| EN-02 | JWT con 401 | `01 Transformando a ágil:...` | `dependencies.py:13-59`; `client.js`; `App.jsx` | Parcialmente cumplido | Logout global ante 401 implementado; HTTPS sigue pendiente de infraestructura. |
| EN-03 | CI/CD a Staging | `01 Transformando a ágil:...` | 6 workflows; deploys `skipped` | Parcialmente cumplido | Sin host/secretos: no es subsanable en este entorno. |
| ET-S4-01..06 | Suite E2E, métricas, SUS, CI, limpieza y documentación | `Sprint 04/01 Revisión:35-57` | `frontend/e2e/**`; evidencias; SUS sin aplicar | Parcialmente cumplido | SUS y Lighthouse autenticado siguen pendientes; no son código. |

## 5. Arquitectura, modelo de datos y estándares

| ID | Requisito documentado | Documento de origen | Ubicación en el código | Estado | Acción necesaria |
|:---|:---|:---|:---|:---|:---|
| ARQ-01 | Capas con Service Layer y Repository | `AGENTS.md:66-67,92-93`; `C4:61-93` | Lógica de negocio dentro de endpoints; solo `services/optimizer` y `services/exportacion` | Parcialmente cumplido | No refactorizar: cambiaría la arquitectura actual sin una decisión aprobada. Registrar como deuda. |
| ARQ-02 | Modelo de datos con 6 tablas y relaciones | `10 Base de datos:47-220` | `models/__init__.py:7-92`; `esquema.sql:8-88` | Cumplido | Ninguna para tablas/campos/claves. |
| ARQ-03 | CHECK de positividad y estados en DDL | `10 Base de datos:74,85-88,98-105,201-209` | Modelos y `esquema.sql` sin CHECK | Parcialmente cumplido | Los Pydantic ya validan entradas; agregar CHECK a modelos/DDL no altera tablas existentes sin migraciones. Registrar como deuda. |
| ARQ-04 | Alembic como tecnología de migraciones | `09 Evaluación de tecnologías:39` | No existe; `database.py:58-63` usa `create_all` | No implementado | `10 Base de datos:256` decide no usarlo. Conservar la decisión documentada; no agregar dependencia. |
| ARQ-05 | Configuración del frontend por `VITE_API_URL` | `.env.example:63-67` | `client.js` (`normalizarUrlBase`, `API_BASE_URL`) | Cumplido | La variable se normaliza para garantizar el prefijo `/api/v1`; un host sin prefijo ya no produce 404. Probado en `client.test.js`. |
| SEG-01 | MFA TOTP y sesiones con `jti` | `Arquitectura/02 Especificacion MFA...:97-235` | No implementado | No implementado | Fuera del PMV vigente (CHANGELOG `:268-285` corrige la afirmación de implementación). Requiere nueva dependencia y decisión. |
| SEG-02 | HTTPS de extremo a extremo | `SPECS.md:478`; `README.md:207-208` | Solo HSTS condicional | No implementado | Requiere proveedor/certificado. No simulable localmente. |
| ACC-01 | WCAG 2.1 AA sin brechas | `05 WCAG:53-75,248` | `Dashboard.jsx`; `index.css`; `MapPicker.jsx` | Parcialmente cumplido | Correcciones señaladas aplicadas; no se afirma auditoría WCAG completa sin herramienta/evidencia externa. |
| PRB-01 | Backend 66/66; frontend 24/24; E2E 79/81 | `docs/Evidencias/README.md:22-38` | `src/backend/tests/**`; `src/frontend/src/**/*.test.{js,jsx}`; `e2e/**` | Cumplido | Vigente el 25/11/2026: backend **109/109**, frontend **83/83** y build correcto de 87 módulos. E2E solo archivadas (79 aprobadas, 2 omitidas); el flujo local se verificó en navegador sin errores. |
| PRB-02 | Cobertura ≥70 % global | `SPECS.md:416-421` | `pytest --cov=app`: 74 %; `vitest --coverage`: 87,03 % global | Cumplido | Ambos umbrales superados el 25/11/2026 con instrumentación de lógica y componentes React. |
| CIE-01 | Video MP4 de ~5 min | Consigna de cierre | `docs/05 Video proyecto/README.md` (pendiente) | No implementado | Requiere grabación real; no generar archivo ficticio. |
| CIE-02 | Aceptación formal y SUS aplicado | `docs/04 Cierre/06 Reporte Final:124-137` | Sin acta ni encuesta | No verificable | Depende de stakeholders; no inventar resultados. |
| CIE-03 | Costo real (AC) para CV/CPI/EAC | `docs/04 Cierre/03 EVM:83-105` | Sin registros de horas/desembolsos | No verificable | Registrar AC real antes de calcular. |

## 6. Contradicciones documentales registradas (no resueltas arbitrariamente)

1. **MFA implementado vs. no implementado:** commits `697dab9`/`b13009b`/`c743d60` (01/10) afirman implementación; `CHANGELOG:268-285` y `README:209-211` (posteriores) la retiran. Prevalece documentalmente "no implementado", coherente con el código. La tabla de "Cumplido" dentro de `Arquitectura/02 Especificacion MFA...:241-249` contradice su propio estado `:10-18`; se conserva.
2. **Esquema RNF duplicado:** `01 Transformando a ágil:17-21` (`RNF-01..03`) vs `06 Requisitos no funcionales:22-36` (`RNF-001..015`). Se usa la tabla formal `06…`; README `:207` sigue con `RNF-02` como HTTPS.
3. **HTTPS previsto vs. pendiente:** `CHANGELOG:388-389,420-422` vs `README:207-208` y cierre 19/11. Prevalece "pendiente" por ser más reciente y coincidir con el código.
4. **RN-014 regla vs. desviación:** `08 Reglas de negocio:75-77` exige puntos pendientes; `CHANGELOG:384-387` documenta el rechazo completo como desviación. Se mantiene la desviación y se reporta en RF-007.
5. **Cobertura histórica 61 % vs 63 % vs 9,8 %:** no reconciliada (`docs/04 Cierre/02 Reporte de Variación:49`). Para el código actual existe salida cruda de `pytest --cov=app`: **73 %** el 23/11/2026 y **74 %** el 25/11/2026; las cifras antiguas se conservan como registro histórico, no como resultado vigente. En frontend, el 93,07 % del 23/11 era solo de archivos instrumentados; la cifra global vigente es **87,03 %**.
6. **Stack Tailwind/Alembic/MERN:** `Modelo C4:43,52` y `CONSTITUTION:152` vs `README:371`, `CHANGELOG:278-282`, `10 Base de datos:256`. Prevalece "no se usan" por ser la corrección registrada.
7. **Sprint 0 y Sprint 4:** "no previstos" en cierre vs. planificación/ejecución real. Se conservan ambos con fechas.
8. **Jira:** plantilla sin completar vs. captura local `Table_Scrum.png`. La URL se normalizó a `https://lewolfdx.atlassian.net/` y el documento se versionó como `V_1_1_0.md`; la evidencia sigue siendo local y no se afirma tablero verificable en línea.

## 7. Cierre de la brecha detectada (23/11/2026)

Los estados de las secciones 1–5 reflejan el código **después** de las correcciones derivadas de esta
matriz. Los commits que cerraron la brecha son:

| Commit | Alcance |
|:---|:---|
| `9f14fe3` | Incorporación de esta matriz. |
| `a571d2c` | RF-002, RN-002 y RF-014 en backend. |
| `d443f3c` | RN-009 al confirmar, RN-013 al editar, fechas UTC y paginación. |
| `f79ddbf` | RF-012/RF-013, RN-019/RN-020 y panel del gerente. |
| `e1962ea` | RF-005 en UI, `VITE_API_URL`, logout/revocación, 401 global y accesibilidad. |
| `7898589` | RBAC de solo lectura para Gerente y fijación del mapa por teclado. |

**Verificación ejecutada el 23/11/2026:** `pytest tests -q` → 103/103; `npm test` → 32/32;
`npm run build` → correcto; `pytest --cov=app` → 73 %; `npm run coverage` → 93,07 % sobre
archivos instrumentados.

**Verificación vigente del 25/11/2026 (cierre del feedback final):**

| Acción | Resultado verificable |
|:---|:---|
| URL de Jira y renombrado del documento a `V_1_1_0.md` | Enlaces del README y del radiador actualizados; capturas locales verificadas |
| Pruebas DOM de componentes y del panel | `componentes.dom.test.jsx` (20) y `dashboard.dom.test.jsx` (10), con `happy-dom` y `@testing-library/react` |
| RNF-004 | `test_rnf004_latencia.py`: 401 mediana 2.96 ms / máxima 3.75 ms; 403 mediana 3.10 ms / máxima 3.50 ms |
| RN-006 | Clave JWT fija eliminada; clave efímera en desarrollo y validación estricta en Staging/Producción |
| `pytest tests -q --disable-warnings` | **109/109** |
| `pytest tests -q --cov=app --cov-report=term` | **74 %** (1 218 sentencias, 312 sin cubrir) |
| `npm test` | **83/83** en 8 archivos |
| `npm run coverage -- --coverage.reporter=text-summary` | **87,03 %** sentencias, 78,14 % ramas, 89,49 % funciones, 89,94 % líneas |
| `npm run build` | Correcto: 87 módulos transformados |
| Verificación manual en navegador | Login, `/auth/me`, recarga con token, logout y seis pestañas: sin errores de consola ni respuestas HTTP ≥ 400 |

No se ejecutaron E2E automatizados con backend/PostgreSQL reales por falta de Docker y servidor local; se
conserva el resultado archivado de 79 aprobadas / 2 omitidas. Estos cambios están sin
commitear a la espera de autorización explícita.

---

[← Volver al README Principal](../../README.md)
