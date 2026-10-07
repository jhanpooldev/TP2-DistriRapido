# Revisión del Sprint

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
| 1.0.0 | 18/10/2026 | Andrew Steven Vega Reyes / Jhunior Harold Cosme Tenorio | Revisión del Sprint 1 (US-001, US-003, EN-01, EN-02). |

---

## 1. Resumen del Sprint

| Categoría | ID | Story Points | Observación |
|---|---|:---:|---|
| **Terminadas** | US-001 | 3 | Registro de puntos de entrega completo, con geocodificación y selección en mapa. |
| **Terminadas** | US-003 | 8 | Ruteo por distancia con Haversine, Vecino Más Cercano y 2-opt. |
| **Terminadas** | EN-01 | 5 | Rendimiento medido: máximo de 20.2 ms con 20 puntos, frente al SLA de 5 s. |
| **En proceso** | EN-02 | 5 | Autenticación JWT terminada; HTTPS sin implementar. |
| **Pendientes** | — | 0 | No quedaron historias nuevas sin iniciar. |
| **Total comprometido** | | **21** | 16 SP cerrados y 5 SP parcialmente entregados. |

**Detalle de EN-02.** De los 5 Story Points del elemento, la parte de autenticación
(token, hash de contraseña y control por rol) está implementada y verificada por
pruebas. La parte de cifrado en tránsito no está implementada y depende del ambiente
de despliegue, por lo que el elemento no puede declararse cerrado.

**Scope creep.** No se incorporaron historias nuevas al sprint. El trabajo adicional
detectado durante la ejecución fue correctivo sobre historias ya comprometidas:

- Filtrado del listado de puntos por operador, alineándose con **RN-001**.
- Inclusión del rol en la respuesta de `GET /api/v1/auth/me`, requerida por **RN-003**.
- Incorporación del factor de emisión en el cálculo de **RN-017**.
- Corrección de la desviación del 50 % del cálculo de emisiones frente a lo esperado.

---

## 2. Gráfico de Progreso del Sprint

No se configuró integración continua en este periodo, de modo que no se dispone de una
serie histórica de avance recuperable del repositorio. El estado se representa con el
porcentaje de Story Points cerrados al cierre de cada elemento:

| Elemento | 05/10 | 08/10 | 12/10 | 15/10 | 18/10 |
|---|:---:|:---:|:---:|:---:|:---:|
| US-001 (3 SP) | 0 % | 100 % | 100 % | 100 % | 100 % |
| US-003 (8 SP) | 0 % | 30 % | 100 % | 100 % | 100 % |
| EN-01 (5 SP) | 0 % | 0 % | 60 % | 100 % | 100 % |
| EN-02 (5 SP) | 20 % | 35 % | 50 % | 60 % | 60 % |
| **Acumulado** | **1 %** | **27 %** | **61 %** | **76 %** | **76 %** |

La distribución por elemento se reconstruye a partir de las fechas de registro y
resolución del `02 Registro de Impedimentos V_1_0_0.md` y de las marcas de commit del
repositorio. **No es una medición automática** y no debe leerse como una curva de
velocidad obtenida de una herramienta de gestión.

---

## 3. Cuadro Comparativo de Historias de Usuario por Sprint

| Sprint | Historia de Usuario / Enabler | Épica | SP Comprometidos | SP Completados | % Avance | Estado |
|:---:|---|:---:|:---:|:---:|:---:|:---|
| 1 | US-001 | EP-01 | 3 | 3 | 100 % | Completada |
| 1 | US-003 | EP-02 | 8 | 8 | 100 % | Completada |
| 1 | EN-01 | EP-02 | 5 | 5 | 100 % | Completada |
| 1 | EN-02 | EP-01 | 5 | 3 | 60 % | Parcial |
| 2 | US-004 | EP-03 | 5 | 5 | 100 % | Completada |
| 2 | US-005 | EP-03 | 5 | 5 | 100 % | Completada |
| 2 | US-002 | EP-01 | 3 | 3 | 100 % | Completada |
| 2 | US-007 | EP-04 | 3 | 3 | 100 % | Completada |

**Totales:** Sprint 1, 21 SP comprometidos y 16 cerrados (76 %). Sprint 2, 16 SP
comprometidos y 16 cerrados (100 %).

---

## 4. Evaluación del Equipo

La evaluación se apoya únicamente en los cambios verificables del sprint.

| Integrante | Desempeño | Evidencia en el repositorio |
|---|:---:|---|
| **Jhanpool Ernesto Flores Torres** — Backend y arquitectura | Excelente | Implementó el motor de ruteo (`haversine`, `nearest_neighbor`, `two_opt`), las reglas de validación de puntos y la capa de seguridad con JWT y bcrypt. |
| **Ricardo David Tucto Ubaldo** — Frontend y UX/UI | Excelente | Construyó el formulario de registro de puntos, la selección de coordenadas en mapa y la vista de ruta optimizada, con estados deshabilitados coherentes con las reglas de negocio. |
| **Andrew Steven Vega Reyes** — QA y DevOps | Excelente | Detectó y registró los impedimentos, e implementó la auditoría de extremo a extremo que verifica el aislamiento entre usuarios y la ausencia de datos de prueba residuales. |

### Fortalezas del equipo

1. **Corrección dentro del propio sprint.** Los seis impedimentos resolubles se
   resolvieron antes del cierre, y no se trasladaron trabajo al sprint siguiente.
2. **Trazabilidad entre reglas de negocio y código.** Cada corrección apunta a una RN
   concreta, lo que facilita la defensa del proyecto ante stakeholders.
3. **Verificación automatizada.** La suite de pruebas del backend creció durante el
   sprint hasta 51 pruebas en verde, y sin afirmaciones de cobertura en porcentajes.

### Oportunidades de mejora

1. **Ausencia de pruebas automatizadas en el frontend.** Solo existen `npm run build`
   y revisión manual; una regresión visual o de interacción no se detecta
   automáticamente.
2. **Puntos de configuración con valores por defecto.** `JWT_SECRET` conserva un valor
   por defecto en `config.py`, lo que permite firmar tokens con una clave conocida si
   el entorno no está configurado.
3. **Brecha entre especificación y código.** La MFA descrita en `docs/inicio/14` y la
   regla **RN-002** de bloqueo por intentos fallidos no tienen implementación, y su
   estado no era visible en la documentación del proyecto.

---

## 5. Desviaciones y Acciones

| # | Desviación detectada | Causa | Acción correctiva aplicada o prevista | Responsable |
|:---:|---|---|---|---|
| DEV-01 | La distancia se calculaba como euclidiana plana, con lo que las rutas entre distritos alejados de Lima resultaban subóptimas. | No se consideró una fórmula geodésica al implementar US-003. | Se adoptó Haversine con radio terrestre de 6 371 km y se añadió la prueba `test_haversine_distancia_conocida`. | Jhanpool Ernesto Flores Torres |
| DEV-02 | El coste factorial de la búsqueda de permutaciones hacía inviable el SLA de EN-01. | Enfoque exhaustivo en lugar de una heurística. | Se implementó Vecino Más Cercano con refinamiento 2-opt; el tiempo con 20 puntos bajó a del orden de 20 ms. | Jhanpool Ernesto Flores Torres |
| DEV-03 | El listado de puntos no se filtraba por operador. | El endpoint devolvía el conjunto completo sin aplicar el filtro de propiedad. | Se aplicó el filtro por operador y se añadió la verificación correspondiente en `auditoria_api.py`. | Andrew Steven Vega Reyes |
| DEV-04 | `GET /auth/me` no devolvía el rol del usuario. | El esquema de respuesta se copió de la entidad sin incluir la relación. | `UsuarioResponse` incorporó el objeto `rol` y se añadió prueba. | Ricardo David Tucto Ubaldo |
| DEV-05 | El cálculo de emisiones se desviaba un 50 % del valor esperado. | El factor de emisión se aplicaba con un valor fijo en lugar del parámetro del vehículo. | El factor pasó a leerse del vehículo asignado, conforme a **RN-017**. | Jhanpool Ernesto Flores Torres |
| DEV-06 | El cifrado en tránsito no está implementado, por lo que EN-02 no se cierra. | Dependencia del ambiente de despliegue, fuera del PMV local. | Se documenta como pendiente y se traslada a la siguiente iteración. | Jhunior Harold Cosme Tenorio |
| DEV-07 | La clave de firma JWT conserva un valor por defecto en el código. | Facilidad de ejecución local sin exigir configuración previa. | Se documentó el riesgo; queda pendiente eliminar el valor por defecto. | Andrew Steven Vega Reyes |
| DEV-08 | RN-002 (bloqueo tras tres intentos fallidos) no está implementada. | La regla no se incluyó entre los criterios de aceptación de EN-02. | Se registra como pendiente y se traslada a la siguiente iteración. | Jhunior Harold Cosme Tenorio |

---

## 6. Aspectos Positivos y Negativos

### Aspectos positivos

1. **16 de 21 Story Points cerrados en el sprint comprometido**, sin histórias nuevas
   añadidas al alcance.
2. **Margen amplio frente al SLA de rendimiento:** 20.2 ms frente a los 5 segundos
   exigidos, con un margen superior a dos órdenes de magnitud.
3. **Corrección de defectos dentro de la propia iteración**, sin deuda técnica
   trasladada.
4. **Auditoría de extremo a extremo reutilizable**, que ejercita cada endpoint y
   verifica el aislamiento entre usuarios.
5. **Base de pruebas del backend en verde** con 51 pruebas al cierre del sprint.

### Aspectos negativos

1. **EN-02 quedó parcialmente entregado** por la dependencia del cifrado en tránsito,
   que no está resuelto en el código de la aplicación.
2. **Sin pruebas automatizadas en el frontend**, lo que deja la capa de interfaz fuera
   de la red de seguridad del ciclo de verificación.
3. **Puntos de configuración con valores por defecto** en el código, entre ellos la
   clave de firma JWT.
4. **Brechas entre especificación y código** (MFA y RN-002) que no estaban visibles en
   la documentación del proyecto.
5. **La búsqueda local 2-opt no actúa con exactamente tres puntos.** El recorrido
   `range(1, len(best) - 2)` queda vacío para tres puntos, por lo que la ruta devuelta
   es la del Vecino Más Cercano sin refinar y puede resultar marginally peor que el
   orden de entrada. El ahorro no llega a ser negativo porque se acota en cero, pero el
   resultado no es el óptimo.

---

## 7. Informe de Software (Versiones y Tecnologías)

### Stack activo

| Componente | Tecnología | Versión |
|---|---|---|
| API | Python | 3.13 |
| Framework de API | FastAPI | 0.115.6 |
| Servidor ASGI | Uvicorn | 0.34.0 |
| ORM | SQLAlchemy | 2.0.36 |
| Validación | Pydantic | 2.10.4 |
| Base de datos | PostgreSQL | 16 (Docker) |
| Autenticación | PyJWT | 2.10.1 |
| Hash de contraseñas | bcrypt | 4.2.1 |
| Pruebas del backend | pytest | 8.3.4 |
| Interfaz | React | 19.0.0 |
| Empaquetador | Vite | 5.4.21 |
| Mapas | Leaflet + OpenStreetMap / Nominatim | 1.9.4 |
| Control de versiones | Git y GitHub | — |

### Comandos de verificación

| Comando | Resultado |
|---|---|
| `pytest tests/ -q` | 51 pruebas en verde. |
| `python auditoria_api.py 8099` | Auditoría de extremo a extremo sin anomalías. |
| `python smoke_sprint2.py 8099` | Verificación de flujo completo correcta. |
| `npm run build` | Compilación de producción correcta. |

Los dos scripts de verificación son herméticos: crean sus propios datos de prueba, los
eliminan al finalizar y dejan la base de datos sin cambios, de modo que su ejecución
es repetible.

### Brechas de tooling

- No hay gestor de migraciones de base de datos; el esquema se crea directamente desde
  los modelos de SQLAlchemy.
- No hay integración continua configurada en el repositorio.
- No hay pruebas automatizadas en el frontend.

---

## 8. Enlaces de Retorno

- [Volver al README principal](../../README.md)
- Informe de estado del Sprint 1: `01 Informe de estado del proyecto V_1_0_0.md`
- Registro de impedimentos del Sprint 1: `02 Registro de Impedimentos V_1_0_0.md`
- Retrospectiva del Sprint 1: `04 Retrospectiva del Sprint V_1_0_0.md`
- Entregables del Sprint 2: `sprint 2/`

---

[← Volver al README principal](../../README.md)