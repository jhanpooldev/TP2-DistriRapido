[← Volver al README Principal](../../README.md)

# Transformando a Ágil

**Proyecto:** EcoLogística Lima – Optimizador de Rutas Sostenibles para DistriRápido S.A.C.
**Versión:** 1.0.0 | **Fecha:** 10/09/2026

## 1. Metodología de Transformación

Este documento transforma la línea base de requisitos establecida en el Acta de Constitución (Fase de Inicio) en elementos de trabajo ágiles, siguiendo dos rutas de mapeo:

- **Requerimientos Funcionales (RF-01 a RF-05)** → se mapean jerárquicamente hacia **Épicas**, que a su vez se descomponen en **Historias de Usuario (US)** con valor directo para el operador logístico.
- **Requerimientos No Funcionales (RNF)** → se transforman en **Historias Técnicas (Enablers)** de rendimiento, seguridad y despliegue, ya que no representan funcionalidad visible para el usuario final pero son indispensables para la calidad del producto.

Para efectos de este entregable, se definen los siguientes Requisitos No Funcionales (RNF), derivados de los KPIs de la Declaración de Visión y de las limitaciones técnicas del Acta de Constitución:

| ID | Requisito No Funcional | Origen |
|---|---|---|
| RNF-01 | El sistema debe generar una ruta optimizada en menos de 5 segundos para hasta 20 puntos de entrega. | KPI de rendimiento, Declaración de Visión |
| RNF-02 | El acceso al sistema debe requerir autenticación, y toda comunicación debe viajar cifrada (HTTPS). | Buena práctica de seguridad no cubierta explícitamente en el Acta |
| RNF-03 | Todo cambio integrado a la rama principal debe desplegarse automáticamente a un ambiente de Staging. | Buenas prácticas de desarrollo, consigna del repositorio |

## 2. Backlog Priorizado (resumen)

Elementos ordenados por valor de negocio y riesgo técnico, con estimación en Story Points (secuencia de Fibonacci). Esta tabla es la fuente directa para cargar el Backlog en Jira.

| Orden | ID | Elemento | Tipo | Épica | SP | Prioridad | Sprint sugerido |
|:---:|---|---|---|---|:---:|---|:---:|
| 1 | US-001 | Registrar puntos de entrega de una ruta | Historia de Usuario | EP-01 | 3 | Alta | Sprint 1 |
| 2 | US-003 | Generar ruta optimizada por distancia y tiempo | Historia de Usuario | EP-02 | 8 | Alta | Sprint 1 |
| 3 | EN-01 | Optimizar el rendimiento del algoritmo de ruteo | Enabler | EP-02 | 5 | Alta | Sprint 1 |
| 4 | EN-02 | Implementar autenticación segura (JWT + HTTPS) | Enabler | EP-01 | 5 | Alta | Sprint 1 |
| 5 | US-004 | Visualizar el impacto ambiental estimado (CO₂) | Historia de Usuario | EP-02 | 5 | Alta | Sprint 2 |
| 6 | US-005 | Ver la ruta calculada en un mapa interactivo | Historia de Usuario | EP-03 | 5 | Alta | Sprint 2 |
| 7 | US-002 | Editar o eliminar una ruta existente | Historia de Usuario | EP-01 | 3 | Media | Sprint 2 |
| 8 | US-007 | Listar y buscar mis rutas guardadas | Historia de Usuario | EP-04 | 3 | Media | Sprint 2 |
| 9 | US-006 | Ver el detalle de cada parada en el mapa | Historia de Usuario | EP-03 | 2 | Media | Sprint 3 |
| 10 | EN-03 | Configurar pipeline CI/CD con despliegue a Staging | Enabler | EP-04 | 8 | Media | Sprint 3 |
| 11 | US-008 | Exportar o descargar el resumen de una ruta | Historia de Usuario | EP-04 | 2 | Baja | Sprint 3 |

**Total del backlog: 49 Story Points** · Sprint 1: 21 SP · Sprint 2: 16 SP · Sprint 3: 12 SP (capacidad estimada de referencia: 4 integrantes × 10 h/semana × 2 semanas por sprint).

## 3. Épicas, Historias de Usuario e Historias Técnicas

### EP-01 · Gestión de Puntos de Entrega y Rutas
*(Origen: RF-01, RF-05)*

#### US-001
**Título:** Registrar puntos de entrega de una ruta
**Épica Relacionada:** EP-01 Gestión de Puntos de Entrega y Rutas
**Redacción:**
> Como operador logístico de DistriRápido S.A.C.,
> quiero registrar los puntos de entrega de una ruta (dirección o coordenadas),
> para poder generar posteriormente una ruta optimizada a partir de ellos.

**Criterios de Aceptación:**

```gherkin
Escenario: Registro exitoso de un punto de entrega
Dado que el operador está autenticado en el panel de gestión
Cuando ingresa una dirección válida y hace clic en "Agregar punto"
Entonces el sistema guarda el punto y lo muestra en la lista de puntos de la ruta en construcción

Escenario: Intento de registrar una dirección inválida
Dado que el operador está en el formulario de registro de puntos
Cuando ingresa una dirección que no puede ser geolocalizada
Entonces el sistema muestra un mensaje de error y no agrega el punto a la lista
```

#### US-002
**Título:** Editar o eliminar una ruta existente
**Épica Relacionada:** EP-01 Gestión de Puntos de Entrega y Rutas
**Redacción:**
> Como operador logístico,
> quiero editar o eliminar una ruta previamente guardada,
> para mantener actualizada la información cuando cambian los pedidos.

**Criterios de Aceptación:**

```gherkin
Escenario: Eliminación exitosa de una ruta
Dado que el operador visualiza el listado de sus rutas guardadas
Cuando selecciona una ruta y confirma la opción "Eliminar"
Entonces la ruta desaparece del listado y del almacenamiento del sistema

Escenario: Edición de los puntos de una ruta guardada
Dado que el operador abre una ruta existente en modo edición
Cuando agrega o quita un punto de entrega y guarda los cambios
Entonces el sistema recalcula la ruta optimizada con la nueva configuración de puntos
```

### EP-02 · Motor de Optimización de Rutas
*(Origen: RF-02, RF-03)*

#### US-003
**Título:** Generar ruta optimizada por distancia y tiempo
**Épica Relacionada:** EP-02 Motor de Optimización de Rutas
**Redacción:**
> Como operador logístico,
> quiero que el sistema calcule automáticamente la ruta más eficiente entre mis puntos de entrega,
> para reducir el tiempo y el combustible utilizado en el reparto.

**Criterios de Aceptación:**

```gherkin
Escenario: Cálculo exitoso con múltiples puntos
Dado que el operador registró entre 2 y 20 puntos de entrega válidos
Cuando solicita "Calcular ruta optimizada"
Entonces el sistema devuelve el orden óptimo de visita en menos de 5 segundos

Escenario: Intento de cálculo sin puntos suficientes
Dado que el operador registró un solo punto de entrega
Cuando solicita "Calcular ruta optimizada"
Entonces el sistema muestra un mensaje indicando que se requieren al menos 2 puntos
```

#### US-004
**Título:** Visualizar el impacto ambiental estimado (CO₂) de la ruta
**Épica Relacionada:** EP-02 Motor de Optimización de Rutas
**Redacción:**
> Como operador logístico,
> quiero ver cuánto CO₂ se ahorra con la ruta optimizada frente a la ruta original,
> para reportar el beneficio ambiental de usar el sistema.

**Criterios de Aceptación:**

```gherkin
Escenario: Comparación exitosa de emisiones
Dado que el sistema ya calculó una ruta optimizada
Cuando el operador abre la sección "Impacto ambiental"
Entonces el sistema muestra el porcentaje de reducción de CO₂ respecto a la ruta no optimizada

Escenario: Ruta sin mejora ambiental significativa
Dado que la ruta optimizada resulta prácticamente igual a la ruta original
Cuando el operador consulta el impacto ambiental
Entonces el sistema indica que no hubo una reducción significativa, sin mostrar porcentajes negativos o erróneos
```

### EP-03 · Visualización en Mapa
*(Origen: RF-04)*

#### US-005
**Título:** Ver la ruta calculada en un mapa interactivo
**Épica Relacionada:** EP-03 Visualización en Mapa
**Redacción:**
> Como operador logístico,
> quiero visualizar la ruta optimizada sobre un mapa interactivo,
> para entender el recorrido antes de asignarlo al repartidor.

**Criterios de Aceptación:**

```gherkin
Escenario: Visualización correcta de la ruta
Dado que el sistema calculó una ruta optimizada
Cuando el operador accede a la vista de mapa
Entonces el mapa muestra el trazado completo de la ruta con los puntos en el orden calculado

Escenario: Mapa sin conexión a la API de geolocalización
Dado que la API externa de mapas no está disponible
Cuando el operador intenta abrir la vista de mapa
Entonces el sistema muestra un mensaje de error controlado en lugar de un mapa en blanco o una falla no manejada
```

#### US-006
**Título:** Ver el detalle de cada parada de entrega en el mapa
**Épica Relacionada:** EP-03 Visualización en Mapa
**Redacción:**
> Como operador logístico,
> quiero hacer clic sobre cada parada del mapa y ver su información,
> para verificar rápidamente los datos de cada punto de entrega.

**Criterios de Aceptación:**

```gherkin
Escenario: Despliegue de información de una parada
Dado que la ruta se muestra correctamente en el mapa
Cuando el operador hace clic sobre un marcador de parada
Entonces el sistema despliega la dirección y el orden de visita de ese punto

Escenario: Parada sin información adicional registrada
Dado que un punto fue registrado solo con coordenadas, sin dirección textual
Cuando el operador hace clic sobre ese marcador
Entonces el sistema muestra las coordenadas como información mínima, sin generar un error
```

### EP-04 · Panel de Gestión del Operador
*(Origen: RF-05)*

#### US-007
**Título:** Listar y buscar mis rutas guardadas
**Épica Relacionada:** EP-04 Panel de Gestión del Operador
**Redacción:**
> Como operador logístico,
> quiero listar y buscar mis rutas guardadas por fecha o estado,
> para encontrar rápidamente una ruta específica entre varias.

**Criterios de Aceptación:**

```gherkin
Escenario: Búsqueda exitosa por rango de fechas
Dado que el operador tiene varias rutas guardadas en distintas fechas
Cuando filtra el listado por un rango de fechas específico
Entonces el sistema muestra únicamente las rutas creadas dentro de ese rango

Escenario: Búsqueda sin resultados
Dado que el operador filtra por un criterio que ninguna ruta cumple
Cuando ejecuta la búsqueda
Entonces el sistema muestra un mensaje de "sin resultados" en lugar de una lista vacía sin explicación
```

#### US-008
**Título:** Exportar o descargar el resumen de una ruta
**Épica Relacionada:** EP-04 Panel de Gestión del Operador
**Redacción:**
> Como operador logístico,
> quiero exportar el resumen de una ruta optimizada,
> para compartirlo con el repartidor o archivarlo como evidencia.

**Criterios de Aceptación:**

```gherkin
Escenario: Exportación exitosa del resumen
Dado que el operador visualiza una ruta ya calculada
Cuando selecciona la opción "Exportar resumen"
Entonces el sistema genera un archivo descargable con los puntos, el orden de visita y el impacto ambiental estimado

Escenario: Intento de exportar una ruta no calculada
Dado que el operador tiene una ruta con puntos registrados pero aún no calculada
Cuando intenta exportar el resumen
Entonces el sistema le solicita calcular la ruta antes de permitir la exportación
```

### Historias Técnicas (Enablers)
*(Origen: Requisitos No Funcionales)*

#### EN-01
**Título:** Optimizar el rendimiento del algoritmo de ruteo
**Épica Relacionada:** EP-02 Motor de Optimización de Rutas *(Enabler de RNF-01)*
**Redacción:**
> Como equipo de desarrollo,
> quiero optimizar la implementación del algoritmo de cálculo de rutas,
> para cumplir el tiempo de respuesta máximo de 5 segundos establecido como requisito no funcional.

**Criterios de Aceptación:**

```gherkin
Escenario: Cumplimiento del SLA de rendimiento
Dado un conjunto de prueba de 20 puntos de entrega
Cuando se ejecuta el endpoint de cálculo de ruta
Entonces el tiempo de respuesta medido es menor a 5 segundos en al menos el 95% de las ejecuciones de prueba

Escenario: Degradación controlada con volumen alto
Dado un conjunto de prueba que excede los 20 puntos de entrega
Cuando se ejecuta el cálculo de ruta
Entonces el sistema informa al usuario que el volumen excede el límite soportado, en lugar de bloquearse sin respuesta
```

#### EN-02
**Título:** Implementar autenticación segura (JWT + HTTPS)
**Épica Relacionada:** EP-01 Gestión de Puntos de Entrega y Rutas *(Enabler de RNF-02)*
**Redacción:**
> Como equipo de desarrollo,
> quiero implementar autenticación basada en tokens (JWT) sobre conexiones cifradas,
> para proteger el acceso a los datos de rutas de los operadores.

**Criterios de Aceptación:**

```gherkin
Escenario: Acceso autorizado con token válido
Dado que el operador envía un token JWT válido y no expirado
Cuando solicita cualquier endpoint protegido de la API
Entonces el sistema responde con los datos solicitados

Escenario: Rechazo de acceso sin token o con token inválido
Dado que la solicitud no incluye un token o el token está expirado
Cuando se intenta acceder a un endpoint protegido
Entonces el sistema responde con un error 401 (No autorizado) sin exponer datos
```

#### EN-03
**Título:** Configurar pipeline CI/CD con despliegue a Staging
**Épica Relacionada:** EP-04 Panel de Gestión del Operador *(Enabler de RNF-03)*
**Redacción:**
> Como equipo de DevOps,
> quiero configurar un pipeline de integración y despliegue continuo,
> para que cada cambio aprobado se despliegue automáticamente en el ambiente de Staging.

**Criterios de Aceptación:**

```gherkin
Escenario: Despliegue automático tras merge exitoso
Dado que un Pull Request fue aprobado y fusionado a la rama principal
Cuando el pipeline de CI/CD se ejecuta
Entonces la nueva versión queda desplegada y accesible en el ambiente de Staging sin intervención manual

Escenario: Bloqueo de despliegue ante fallo de pruebas
Dado que el pipeline ejecuta las pruebas automatizadas tras un push
Cuando alguna prueba falla
Entonces el pipeline detiene el despliegue a Staging y notifica el fallo al equipo
```

## 4. Definition of Done (DoD) Global del Proyecto

Toda Historia de Usuario o Historia Técnica se considera **"Done"** únicamente cuando cumple **todos** los siguientes criterios:

- [ ] Código implementado y funcionando según los Criterios de Aceptación definidos.
- [ ] Cobertura de pruebas unitarias ≥ 80% sobre el código nuevo o modificado.
- [ ] Análisis estático de código ejecutado (SonarQube / CodeQL) sin vulnerabilidades críticas ni bloqueantes abiertas.
- [ ] Revisión de código (Peer Review) aprobada por al menos un integrante distinto al autor, mediante Pull Request.
- [ ] Cambios desplegados automáticamente y verificados en el ambiente de Staging/Pruebas.
- [ ] Documentación de API/código actualizada (especificación OpenAPI/Swagger para endpoints nuevos o modificados).
- [ ] Sin errores críticos ni bloqueantes conocidos en el flujo cubierto por la historia.
- [ ] Tarjeta movida a la columna "Done" del tablero Scrum en Jira, con la evidencia enlazada (PR, pipeline).

---

[← Volver al README Principal](../../README.md)
