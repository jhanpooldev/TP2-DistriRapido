# Usabilidad y cuestionario SUS

[← Volver al README principal](../../../README.md)

---

**Nombre del Proyecto:** EcoLogística Lima – Optimizador de Rutas Sostenibles para DistriRápido S.A.C.

**Líder del Proyecto:** Jhunior Harold Cosme Tenorio

**Sprint:** 4

**Periodo:** 09/11/2026 – 17/11/2026

**Fecha de elaboración del instrumento:** 17/11/2026

**Estado:** **Instrumento preparado. No aplicado. Sin resultados reales.**

---

## Control de Versiones del Documento

| Versión | Fecha | Autor | Descripción del Cambio |
|:---:|:---:|:---|:---|
| 1.0.0 | 17/11/2026 | Jhunior Harold Cosme Tenorio / Equipo EcoLogística | Instrumento SUS, protocolo de aplicación y plantilla de resultados. Sin respuestas registradas. |

---

## 1. Objetivo

Evaluar la **usabilidad percibida** del panel de EcoLogística Lima mediante la escala
**System Usability Scale (SUS)**, un instrumento estandarizado de diez ítems que produce
un puntaje de 0 a 100.

Este documento entrega:

- el cuestionario adaptado al español;
- la escala de respuesta;
- la fórmula de cálculo;
- el protocolo de aplicación;
- la plantilla de registro de respuestas;
- el plan de análisis.

**No contiene resultados porque la encuesta no se aplicó a participantes reales.** No se
registran puntajes, comentarios, nombres ni fechas de sesión que no hayan ocurrido.

---

## 2. Alcance y participantes

### 2.1 Perfil requerido

| Característica | Criterio |
|---|---|
| Rol | Operador Logístico o Administrador con acceso al panel. |
| Experiencia previa | Al menos una sesión de uso del sistema, guiada o autónoma. |
| Conocimiento técnico | No se exige; el instrumento mide usabilidad percibida, no conocimiento informático. |
| Disponibilidad | 15–20 minutos: 5–8 minutos de tarea y 5 minutos de cuestionario. |
| Consentimiento | Informado y verbal o escrito antes de comenzar. |

### 2.2 Tamaño de muestra

Para un SUS exploratorio se recomienda un mínimo de **cinco participantes**. Con esa
cantidad se obtiene una señal inicial, no un resultado estadísticamente representativo.
Si se dispone de más personas, se registran todas y se reporta el promedio y la
desviación estándar.

> **No se ha reclutado a ningún participante.** La tabla de la sección 6 está vacía a
> propósito.

---

## 3. Cuestionario SUS adaptado al español

**Instrucciones para la persona participante:**

> A continuación encontrarás diez afirmaciones sobre el sistema que acabas de usar. Marca
> tu grado de acuerdo con cada una en una escala de 1 a 5, donde **1 = Totalmente en
> desacuerdo** y **5 = Totalmente de acuerdo**. No hay respuestas correctas o incorrectas.
> Responde según tu impresión, no según lo que creas que el equipo espera.

| # | Afirmación | 1 | 2 | 3 | 4 | 5 |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|
| 1 | Creo que me gustaría usar este sistema con frecuencia. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 2 | Encontré el sistema innecesariamente complejo. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 3 | Pensé que el sistema era fácil de usar. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 4 | Creo que necesitaría el apoyo de un técnico para poder usar este sistema. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 5 | Encontré las diversas funciones de este sistema bien integradas. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 6 | Pensé que había demasiada inconsistencia en este sistema. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 7 | Imagino que la mayoría de las personas aprenderían a usar este sistema muy rápidamente. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 8 | Encontré el sistema muy engorroso de usar. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 9 | Me sentí muy seguro al usar el sistema. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 10 | Necesité aprender muchas cosas antes de poder empezar a usar este sistema. | ☐ | ☐ | ☐ | ☐ | ☐ |

**Escala:** 1 = Totalmente en desacuerdo · 2 = En desacuerdo · 3 = Neutral · 4 = De
acuerdo · 5 = Totalmente de acuerdo.

---

## 4. Cálculo del puntaje

El puntaje SUS se calcula por participante y luego se promedia.

### 4.1 Regla por ítem

| Ítems | Tipo | Contribución |
|:---:|:---|:---|
| 1, 3, 5, 7, 9 | Positivos | `respuesta − 1` |
| 2, 4, 6, 8, 10 | Negativos | `5 − respuesta` |

Cada ítem aporta entre 0 y 4 puntos. La suma de los diez ítems queda entre 0 y 40.

### 4.2 Fórmula

```text
SUS = (suma de contribuciones) × 2.5
```

El resultado queda en una escala de **0 a 100**, donde valores más altos indican mejor
usabilidad percibida.

### 4.3 Interpretación de referencia

| Rango | Lectura habitual |
|---|---|
| ≥ 80 | Excelente |
| 68 – 79 | Bueno / por encima del promedio |
| 50 – 67 | Aceptable con reservas |
| < 50 | Bajo; requiere revisión |

El umbral de referencia habitual es **68**. No se usa para aprobar o desaprobar el
sistema, sino para orientar la conversación con el equipo.

> Estas bandas son referencias de la literatura SUS. **No se aplican a este proyecto
> porque no hay puntaje medido.**

---

## 5. Protocolo de aplicación

1. **Preparar el entorno.** Backend y frontend en ejecución, base con datos de prueba
   suficientes para que el participante pueda registrar un pedido y armar una ruta.
2. **Explicar el propósito.** Se evalúa el sistema, no a la persona. No hay respuestas
   correctas.
3. **Firmar o registrar el consentimiento.** Se informa que la participación es
   voluntaria y que los datos se reportan de forma anónima.
4. **Entregar la tarea.** Por ejemplo: "Registra dos pedidos, calcula una ruta y expórtala.
   Puedes pensar en voz alta si te resulta cómodo."
5. **Observar sin intervenir.** El facilitador solo responde dudas de interpretación del
   cuestionario, no de la interfaz.
6. **Aplicar el cuestionario.** Preferiblemente en papel o en un formulario sin campos de
   nombre. Registrar el rol y la experiencia previa, no la identidad.
7. **Agradecer y cerrar.** Recordar que los resultados se usarán para mejorar el panel.

### 5.1 Consentimiento (texto base)

> Esta evaluación busca conocer tu opinión sobre el panel de EcoLogística Lima. No es un
> examen y no afecta tu trabajo. Tus respuestas se registrarán de forma anónima y se
> usarán solo para mejorar el sistema. Puedes detenerte en cualquier momento.

### 5.2 Reglas de registro

- No registrar nombres, correos ni datos personales en la tabla de resultados.
- Usar códigos (`P01`, `P02`, …) y guardar la relación código–persona solo si es
  estrictamente necesario, en un archivo aparte y no versionado.
- No completar respuestas faltantes con promedios ni con suposiciones.
- Si una persona no responde un ítem, se registra la omisión y se excluye del cálculo o se
  documenta el criterio aplicado.

---

## 6. Resultados

### 6.1 Estado

**No se aplicó el cuestionario.** No existen respuestas, puntajes ni comentarios reales.

| Elemento | Estado |
|---|---|
| Instrumento elaborado | **Sí** |
| Protocolo definido | **Sí** |
| Participantes reclutados | **No** |
| Sesiones realizadas | **No** |
| Respuestas registradas | **No** |
| Puntaje SUS calculado | **No** |
| Informe de hallazgos | **No** |

### 6.2 Plantilla de registro (vacía)

La siguiente tabla es una **plantilla**. Sus filas no representan participantes reales y
no deben completarse con datos inventados.

| Código | Rol | Experiencia previa | Ítems 1–10 | Suma | SUS |
|:---:|:---|:---|:---|:---:|:---:|
| P01 | — | — | — | — | — |
| P02 | — | — | — | — | — |
| P03 | — | — | — | — | — |
| P04 | — | — | — | — | — |
| P05 | — | — | — | — | — |

### 6.3 Plantilla de resumen (vacía)

| Indicador | Valor |
|---|---:|
| Participantes válidos | — |
| Promedio SUS | — |
| Mediana | — |
| Desviación estándar | — |
| Mínimo | — |
| Máximo | — |
| Comentarios cualitativos | — |

### 6.4 Plan de análisis cuando existan datos

1. Calcular el SUS por participante con la fórmula de la sección 4.
2. Reportar promedio, mediana, desviación estándar, mínimo y máximo.
3. Comparar el promedio con el umbral de referencia de 68, sin convertirlo en una
   aprobación formal.
4. Agrupar los comentarios cualitativos por tema: navegación, claridad de mensajes,
   registro de pedidos, cálculo de rutas, mapa e impacto ambiental.
5. Cruzar los temas con los hallazgos WCAG del Sprint 3 para distinguir problemas de
   accesibilidad de problemas de usabilidad percibida.
6. Registrar las acciones de mejora con responsable y fecha, y repetir la medición
   después de aplicarlas.

---

## 7. Relación con otros entregables

| Entregable | Relación |
|---|---|
| [`03 Analisis PlayWrigth V_1_0_0.md`](03%20Analisis%20PlayWrigth%20V_1_0_0.md) | La suite E2E verifica que los flujos funcionen; el SUS mide cómo se sienten al usarlos. |
| [`Sprint 03/05 WCAG V_1_0_0.md`](../Sprint%2003/05%20WCAG%20V_1_0_0.md) | WCAG evalúa accesibilidad técnica; SUS evalúa percepción. Se complementan, no se sustituyen. |
| [`Sprint 03/01 Revisión del Sprint V_1_0_0.md`](../Sprint%2003/01%20Revisi%C3%B3n%20del%20Sprint%20V_1_0_0.md) | Allí se registra la revisión manual de accesibilidad y sus límites. |

---

## 8. Limitaciones

1. **Sin resultados reales.** El documento no puede usarse para afirmar que el sistema es
   usable o que cumple un objetivo de usabilidad.
2. **SUS mide percepción, no eficiencia.** No reemplaza métricas de tarea como tiempo,
   errores o clics.
3. **Muestra pequeña.** Cinco participantes dan una señal inicial, no representatividad
   estadística.
4. **Sesgo del facilitador.** Si la persona que aplica el cuestionario conoce el sistema,
   puede influir sin querer; conviene que otra persona facilite la sesión.
5. **Sin prueba con lector de pantalla.** El SUS no cubre por sí solo la experiencia de
   personas con discapacidad visual.
6. **El instrumento está en español.** Si se aplica a personas que no dominan el idioma,
   el resultado puede verse afectado.

---

## 9. Próximos pasos

1. Reclutar al menos cinco participantes del rol Operador.
2. Aplicar el cuestionario con el protocolo de la sección 5.
3. Registrar las respuestas en la plantilla de la sección 6.2.
4. Calcular y reportar los puntajes en la sección 6.3.
5. Convertir los hallazgos en acciones concretas y repetir la medición después de los
   cambios.

> Mientras estos pasos no se ejecuten, el estado del entregable sigue siendo
> **"instrumento preparado, sin resultados"**.

---

[← Volver al README principal](../../../README.md)
