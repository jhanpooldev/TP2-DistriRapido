# Retrospectiva del sprint

[← Volver al README principal](../../../README.md)

---

**Nombre del Proyecto:** EcoLogística Lima – Optimizador de Rutas Sostenibles para DistriRápido S.A.C.

**Líder del Proyecto:** Jhunior Harold Cosme Tenorio

**Sprint:** 2

**Periodo:** 19/10/2026 – 01/11/2026

---

## Control de Versiones del Documento

| Versión | Fecha | Autor | Descripción del Cambio |
|:---:|:---:|:---|:---|
| 1.0.0 | 01/10/2026 | Jhunior Harold Cosme Tenorio / Equipo EcoLogística | Retrospectiva del Sprint 1. |
| 2.0.0 | 05/10/2026 | Jhunior Harold Cosme Tenorio / Equipo EcoLogística | Retrospectiva del Sprint 2. |
| 2.1.0 | 05/10/2026 | Jhunior Harold Cosme Tenorio / Equipo EcoLogística | Corregida para reflejar el desarrollo real del Sprint 2: se retiraron las cifras de cobertura y de total de pruebas que no resultaban verificables y se alineó el contenido con el código entregado en `src/`. |

## ¿Qué aprendimos?

1. **Un commit explícito es parte del contrato de un endpoint de escritura.** El
   fallo más grave del sprint no estaba en el algoritmo sino en la transacción:
   `PUT /api/v1/rutas/{id}` modificaba el objeto sin confirmar, y el comportamiento
   observable era que "a veces" los cambios no quedaban. Se refuerza que la
   persistencia forma parte del criterio de aceptación de una historia.
2. **Las reglas de negocio deben establecerse antes de exponerlas.** RN-009, RN-013 y
   RN-014 se aplicaron de forma explícita en el servicio de rutas, no en la capa de
   validación genérica, porque dependen del estado de la ruta.
3. **Un indicador ambiental sin fuente de datos es una cifra inventada.** Cuando el
   ahorro de CO₂ usaba un factor fijo, el número era correcto en apariencia y falso en
   la práctica. El factor de emisión pertenece al vehículo.
4. **El rendimiento del motor quedó holgado frente al SLA.** Con 20 puntos, las cinco
   ejecuciones medidas se situaron entre 17.9 ms y 20.2 ms, muy por debajo de los
   5 segundos exigidos por EN-01. La heurística NN + 2-opt cumple con holgura, lo que
   permite reevaluar el número de puntos en un sprint futuro.
5. **Las interfaces heredan los defectos de sus dependencias.** El botón Reintentar
   recargaba la aplicación y las instancias de Leaflet no se destruían; ninguno de los
   dos problemas estaba en la lógica de negocio.

## ¿Qué estamos haciendo bien?

1. **Verificación automatizada de extremo a extremo.** La suite creció de 41 a 51
   pruebas y se unió a un smoke test y a una auditoría de API que detectan
   incoherencias que las pruebas unitarias no alcanzan a ver.
2. **Corrección de defectos en el propio sprint, no en el siguiente.** Los seis
   impedimentos del Sprint 2 se resolvieron dentro de la propia iteración.
3. **Trazabilidad entre reglas de negocio, código y pruebas.** Cada corrección queda
   asociada a una RN concreta, lo que facilita la defensa del proyecto.
4. **Compromisos de versiones pequeños y descriptivos**, con mensajes que explican el
   motivo y no solo el cambio.

## ¿Qué podemos hacer mejor?

### Personas

- **Distribución de la revisión entre pares.** La revisión del código de rutas y la
  del motor se concentraron en el rol de backend. Rotar revisores entre sprints
  reparte el contexto del motor.
- **Práctica del motor por más de una persona.** `haversine`, `nearest_neighbor` y
   `two_opt` solo los comprende a fondo quien los escribió, lo que genera un punto
   único de falla para el Sprint 3.

### Relaciones

- **Acordar el contrato de datos antes de integrar.** El frontend y el backend
  colaboraron sobre la forma de la respuesta de la ruta; fijar esa estructura como
  esquema compartido evitaría la espera entre capas.
- **Documentar el alcance de cada sprint en el momento de la planificación.** Durante
   este sprint se detectó que los entregables de `docs/03 Implementación/`
   correspondían al Sprint 2 pese a nombrarse Sprint 1. La discrepancia se originó en
   una actualización posterior de esos archivos.

### Procesos

- **Añadir la transacción al criterio de aceptación.** Ninguna historia de escritura
   debe considerarse terminada sin una comprobación de que el dato persiste.
- **Incorporar pruebas del frontend.** El ciclo Red-Green-Refactor se aplicó solo al
   backend, por lo que la capa React no tiene red de seguridad ante
   regresiones.
- **Cerrar las reglas de negocio antes de declararlas en el README.** RN-002 aparece
   descrita en el README pero no está implementada; esa diferencia debe quedar
   registrada como pendiente, no como funcionalidad.

### Herramientas

- **Automatizar la verificación de la capa de Leaflet y del cliente HTTP.** Requirió
  revisión manual detectar que Reintentar recargaba la aplicación y que los mapas no se
   destruían al desmontarse.
- **Versionar el factor de emisión como configuración.** Hoy vive en los parámetros
   del vehículo, lo que es correcto, pero no hay un registro de su procedencia.
- **Reservar un entorno limpio para la auditoría de API.** La verificación mediante
   un servidor con pruebas anteriores, o un proceso ocupando el puerto, dejó atrás
   datos de prueba en la base de datos.

### Acciones a realizar

| # | Acción de mejora concreta | Eje | Responsable | Fecha Límite | Criterio de éxito |
|:---:|:---|:---:|:---:|:---:|:---|
| **ACT-S2-01** | Incorporar al criterio de aceptación de toda historia de escritura una comprobación de persistencia que relea el recurso tras confirmar la transacción. | Procesos | Andrew Steven Vega Reyes | 06/11/2026 | Cada historia de escritura incluye una prueba que relee el recurso y confirma que el cambio quedó guardado. |
| **ACT-S2-02** | Crear la suite de pruebas del frontend con Vitest para `App`, `Login` y el flujo de sesión. | Herramientas | Ricardo David Tucto Ubaldo | 13/11/2026 | `npm run test` ejecuta pruebas sobre el inicio de sesión y el cierre de sesión. |
| **ACT-S2-03** | Implementar RN-002 con contador de intentos fallidos y bloqueo temporal, o retirar la regla del alcance declarado. | Procesos | Jhanpool Ernesto Flores Torres | 13/11/2026 | Tres intentos fallidos bloquean la cuenta durante 15 minutos, verificado por prueba automatizada. |
| **ACT-S2-04** | Fijar un contrato de datos único entre `schemas` del backend y el cliente HTTP del frontend. | Relaciones | Jhanpool Ernesto Flores Torres / Ricardo David Tucto Ubaldo | 20/11/2026 | La respuesta de ruta se define una sola vez y el frontend la consume sin duplicar nombres de campo. |
| **ACT-S2-05** | Documentar en el README, junto a cada funcionalidad, si está implementada o pendiente. | Procesos | Jhunior Harold Cosme Tenorio | 06/11/2026 | El README no afirma funcionalidades que el repositorio no respalde. |

---

[← Volver al README principal](../../../README.md)