# Reprospectiva del sprint

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
| 1.0.0 | 18/10/2026 | Jhunior Harold Cosme Tenorio / Equipo EcoLogística | Reprospectiva del Sprint 1. |

---

## 1. ¿Qué esperaba el equipo que iba a ser diferente esta vez?

1. **Que el Sprint 0 hubiera cerrado la fase de análisis.** La expectativa era
   arrancar directamente con la construcción de US-001, US-003, EN-01 y EN-02, sin
   fases previas de descubrimiento.
2. **Que el cálculo de rutas funcionara sobre coordenadas reales de Lima.** Se esperaba
   que medir la distancia entre dos puntos fuera un detalle de implementación, y que el
   esfuerzo del sprint estuviera en el algoritmo de optimización.
3. **Que el requerimiento no funcional de rendimiento se cumpliera sin trabajo
   adicional.** Se esperaba que una implementación razonable respondiera por debajo de los
   5 segundos sin necesidad de una etapa específica de medición.
4. **Que la autenticación fuera un bloque único.** Se esperaba que EN-02 se cerrara
   completo una vez implementado el inicio de sesión.
5. **Que los criterios de aceptación detectaran todos los defectos de cada historia.**
   Se esperaba que, al declarar Completa una historia, quedara poco por corregir
   después.

---

## 2. ¿Qué fue diferente esta vez?

1. **Hubo trabajo bloqueante antes de poder construir.** El esquema de usuario no podía
   validarse por falta de `email-validator`, de modo que la aplicación no arrancaba y
   la suite de pruebas no se podía ejecutar. El sprint se inició con una corrección de
   entorno, no con la historia.
2. **El punto crítico fue la métrica, no el algoritmo.** La distancia como diferencia de
   coordenadas parecía correcta y producía rutas subóptimas. La fórmula geodésica resultó
   ser la decisión de diseño decisiva de US-003.
3. **El rendimiento superó lo previsto.** La búsqueda exhaustiva de permutaciones no
   era viable, pero la heurística de dos etapas quedó dos órdenes de magnitud por debajo
   del SLA, con un máximo de 20.2 ms para 20 puntos.
4. **Aparecieron defectos fuera de los criterios de aceptación.** El listado de puntos no
   se filtraba por operador y la respuesta de `GET /auth/me` omitía el rol. Ninguno de
   los dos estaba recogido en los criterios de aceptación de las historias del sprint.
5. **EN-02 no pudo cerrarse.** El cifrado en tránsito depende del ambiente de
   despliegue, que no forma parte del PMV local, de modo que el elemento quedó en 5 de 5
   Story Points parcialmente entregados.
6. **El balance fue de 16 de 21 Story Points.** La brecha corresponde íntegramente a
   EN-02.

---

## 3. ¿Qué aprendimos?

1. **Un criterio de aceptación describe el resultado esperado, no el estado real del
   sistema.** Los defectos de aislamiento entre usuarios y de respuesta sin rol
   existían porque nadie los buscó: no estaban escritos.
2. **Medir antes de optimizar define el algoritmo correcto.** La medición con 20 puntos
   convirtió el rendimiento de una suposición en un dato, y ese dato justificó la
   heurística de forma objetiva.
3. **La geometría es parte del dominio, no un detalle de implementación.** En un área
   geográfica concreta, la distancia entre coordenadas no es una resta.
4. **Una configuración con valores por defecto es una decisión de seguridad, no una
   comodidad de desarrollo.** El valor por defecto de `JWT_SECRET` permite firmar
   tokens con una clave conocida si el entorno no está preparado.
5. **Un Enabler puede tener dos alcances.** EN-02 mezclaba autenticación de aplicación
   y cifrado en transporte; el primero es código del proyecto y el segundo no. Conviene
   separarlos para que el criterio de cierre sea verificable.

---

## 4. ¿Qué estamos haciendo bien?

1. **La trazabilidad entre reglas de negocio, código y pruebas.** Cada corrección
   apunta a una RN concreta, y las pruebas documentan el comportamiento esperado.
2. **La verificación automatizada de extremo a extremo.** La auditoría ejercita cada
   endpoint, comprueba el aislamiento entre usuarios y no deja datos de prueba
   residuales en la base de datos.
3. **La corrección dentro del propio sprint.** Los seis impedimentos resolubles se
   resolvieron antes del cierre, sin trasladarse al sprint siguiente.
4. **La documentación del estado real.** Los elementos incompletos quedan registrados
   como pendientes en lugar de presentarse como terminados.
5. **El trabajo en equipo.** Los hallazgos del rol de calidad llegaron
   temprano y pudieron corregirse dentro del sprint.

---

## 5. ¿Qué podemos hacer mejor?

1. **Añadir pruebas automatizadas del frontend.** La revisión manual no detecta
   regresiones de interacción ni de presentación.
2. **Completar los criterios de aceptación con aislamiento y control de acceso.**
   Ninguna historia de datos de usuario debería cerrarse sin una prueba que demuestre
   que un usuario no accede a los recursos de otro.
3. **Eliminar los valores por defecto sensibles del código.** La aplicación no debería
   arrancar con una clave de firma conocida.
4. **Integrar la verificación en el flujo de trabajo.** No hay integración continua
   configurada, por lo que la suite de pruebas depende de que alguien la ejecute
   manualmente.
5. **Separar los alcances de los Enablers.** Un elemento con dependencias externas no
   puede usarse como criterio de cierre único.
6. **Escalar las brechas de especificación.** MFA y RN-002 están descritas en la
   documentación y ausentes en el código; esa diferencia debe estar visible.
7. **Cubrir los casos límite del algoritmo.** Con tres puntos exactos la búsqueda local
   2-opt no llega a ejecutarse, y esa limitación no estaba contemplated en ningún criterio
   de aceptación.

---

## 6. ¿Cuál fue la mayor pérdida de esta sesión?

### 6.1. Costo en tiempo

El mayor costo de tiempo no provino de construir las historias, sino de los seis
impedimentos resueltos, cada uno con un ciclo de uno a dos días entre su registro y su
resolución. En conjunto, consumieron una parte sustancial de la capacidad del sprint.
Los tres impedimentos que permanecen abiertos (HTTPS, clave por defecto y RN-002) no
generaron costo de rework dentro del sprint, pero generan trabajo pendiente en la
siguiente iteración.

### 6.2. Costo de frustración

La frustración se concentró en el momento de descubrir que las historias no podían
ejecutarse sin corregir primero el arranque de la aplicación, y en la sorpresa de
encontrar defectos de aislamiento de datos que no estaban en ningún criterio de
aceptación. Ambos casos producen la misma sensación: el avance depende de factores que
nadie había verificado.

### 6.3. Costo de oportunidad

Al quedar EN-02 abierto, la capacidad que pudo aplicarse a cerrar el cifrado en
transito se destinó a corregir defectos de historias ya terminadas. En la siguiente
iteración habrá que retomar el elemento incompleto, lo que reduce el tiempo disponible
para el trabajo nuevo del Sprint 2.

### 6.4. Probabilidad de repetición

| Causa | Probabilidad estimada de repetición |
|---|:---:|
| Arranque del entorno sin verificar antes de construir | 40 % |
| Criterios de aceptación sin cubrir aislamiento de datos | 70 % |
| Valores por defecto sensibles en el código | 50 % |
| Enablers con dependencias externas mezcladas en un mismo elemento | 60 % |
| Casos límite del algoritmo no cubiertos por los criterios de aceptación | 65 % |

**Estimación global de repetición de la causa dominante (criterios de aceptación
incompletos): 70 %.** Se considera alta porque se trata de un patrón de trabajo, no de
un incidente puntual, y porque en este sprint la causa ya se presentó en dos historias
distintas.

---

## 7. Acciones a realizar

| # | Acción de mejora concreta | Eje | Responsable | Fecha Límite | Criterio de éxito |
|:---:|:---|:---:|:---:|:---:|:---|
| **ACT-S1-01** | Exigir, en toda historia con datos de usuario, una prueba que demuestre que un usuario autenticado no lee ni modifica recursos de otro. | Procesos | Andrew Steven Vega Reyes | 01/11/2026 | Cada historia con datos de usuario incluye la prueba de aislamiento y la suite completa queda en verde. |
| **ACT-S1-02** | Eliminar el valor por defecto de `JWT_SECRET` en `src/backend/app/core/config.py` y exigir que el proceso no arranque sin clave válida. | Seguridad | Jhanpool Ernesto Flores Torres | 25/10/2026 | La aplicación no inicia si `JWT_SECRET` no está definida, y la prueba asociada lo verifica. |
| **ACT-S1-03** | Implementar la regla RN-002 de bloqueo tras tres intentos fallidos durante 15 minutos. | Seguridad | Jhanpool Ernesto Flores Torres | 01/11/2026 | El login bloquea la cuenta durante 15 minutos tras tres intentos fallidos, con prueba que lo demuestre. |
| **ACT-S1-04** | Definir HTTPS en el ambiente de despliegue y documentar el procedimiento de verificación. | Seguridad | Jhunior Harold Cosme Tenorio | 08/11/2026 | La verificación del entorno confirma que la API responde por HTTPS y que el procedimiento queda documentado. |
| **ACT-S1-05** | Incorporar pruebas automatizadas del frontend para `App`, `Login` y el flujo de sesión. | Herramientas | Ricardo David Tucto Ubaldo | 08/11/2026 | `npm run test` ejecuta pruebas del inicio de sesión y del cierre de sesión en verde. |
| **ACT-S1-06** | Dividir los Enablers de seguridad en alcance de aplicación y alcance de infraestructura, con criterios de cierre separados. | Procesos | Jhunior Harold Cosme Tenorio | 01/11/2026 | El backlog de Sprints 2 y 3 separa ambos alcances y cada uno tiene un criterio de cierre verificable. |
| **ACT-S1-07** | Marcar en la documentación de especificación qué reglas tienen implementación y cuáles no. | Comunicación | Andrew Steven Vega Reyes | 25/10/2026 | MFA y RN-002 aparecen identificadas como pendientes en la documentación del proyecto. |
| **ACT-S1-08** | Configurar la ejecución de la suite de pruebas y de la auditoría como paso obligatorio previo a la entrega de cada sprint. | Herramientas | Andrew Steven Vega Reyes | 01/11/2026 | Existe un procedimiento documentado y la auditoría se ejecuta y se registra en cada cierre de sprint. |
| **ACT-S1-09** | Ampliar el rango recorrido por `two_opt` para que la búsqueda local se aplique también con tres puntos, y comparar el resultado con el orden de entrada antes de devolverlo. | Procesos | Jhanpool Ernesto Flores Torres | 01/11/2026 | Con tres puntos la ruta devuelta no es peor que el orden de entrada, y existe una prueba que lo cubre. |

---

## 8. Herramientas

- **Git y GitHub** para control de versiones e historial.
- **FastAPI, SQLAlchemy y PostgreSQL** para el backend.
- **React, Vite y Leaflet con OpenStreetMap** para el frontend.
- **pytest** para las pruebas automatizadas del backend.
- **`auditoria_api.py`** para la auditoría de extremo a extremo y el aislamiento entre
  usuarios.
- **`smoke_sprint2.py`** para la verificación de flujo completo.
- **Docker** para el servicio de PostgreSQL.
- **`markdownlint-cli2`** para la validación de los documentos de este sprint.

---

[← Volver al README principal](../../README.md)