[← Volver al README Principal](../../README.md)

# 07 Reporte Final de Lecciones Aprendidas (Final Lessons Learned Report)

**Proyecto:** EcoLogística Lima – Optimizador de Rutas Sostenibles para DistriRápido S.A.C.  
**Fecha de Reunión de Cierre:** no se registró una reunión de cierre; esta matriz consolida
las cuatro retrospectivas de sprint con fecha de corte 19/11/2026  
**Versión:** 1.0.0

> Las prácticas y mejoras se extraen de las retrospectivas reales de los
> [Sprint 1](../03%20Implementación/Sprint%2001/04%20Retrospectiva%20del%20Sprint%20V_1_0_0.md),
> [Sprint 2](../03%20Implementación/Sprint%2002/04%20Retrospectiva%20del%20Sprint%20V_2_0_0.md),
> [Sprint 3](../03%20Implementación/Sprint%2003/02%20Retrospectiva%20del%20Sprint%20V_1_0_0.md)
> y [Sprint 4](../03%20Implementación/Sprint%2004/02%20Retrospectiva%20del%20Sprint%20V_1_0_0.md),
> de los registros de impedimentos y de la auditoría de cierre. Serie de cierre:
> [01 Estado](01%20Reporte%20de%20Estado%20V_1_0_0.md) ·
> [02 Variación](02%20Reporte%20de%20Variación%20V_1_0_0.md) ·
> [03 EVM](03%20Reporte%20de%20Análisis%20de%20Valor%20Ganado%20-%20EVM%20V_1_0_0.md) ·
> [04 Tableros](04%20Tableros%20de%20Control%20-%20Híbridos%20V_1_0_0.md) ·
> [05 Radiadores](05%20Radiadores%20de%20Información%20V_1_0_0.md) ·
> [06 Reporte Final](06%20Reporte%20Final%20del%20Proyecto%20V_1_0_0.md) ·
> [07 Lecciones](07%20Reporte%20Final%20de%20Lecciones%20Aprendidas%20V_1_0_0.md).

## 1. Matriz Consolidada de Aprendizajes

| Categoría de Gestión | Prácticas Efectivas (Qué mantener) | Oportunidades de Mejora (Qué evitar/ajustar) | Recomendación para Futuros Equipos |
|:---|:---|:---|:---|
| **Desempeño del Equipo** (Dinámica ágil y general) | Retrospectiva por sprint con aprendizajes concretos; ocho acciones `ACT-S4-01` a `ACT-S4-08` con responsable y fecha; aprendizaje colaborativo al corregir el `ReferenceError` del panel y las tres aserciones E2E mal supuestas. | No se recolectó Mood Chart ni satisfacción del equipo; solo ACT-S4-02 se cumplió parcialmente y las otras siete acciones siguen abiertas. | Registrar el estado de ánimo por iteración desde el Sprint 1 y revisar el estado de las acciones al inicio de cada sprint, no solo al final. |
| **Evolución y Control del Alcance** (Predictivo vs. Adaptativo) | Línea base de 49 SP estable; PMV acotado a los pasos 1, 2, 4, 5 y 8; cambios de alcance trazados en el CHANGELOG sin re-baselining encubierto. | Sprint 0 no planificado; Sprint 4 reconducido a calidad; HTTPS, MFA, RN-002 y despliegue quedaron fuera sin una solicitud formal de cambio aprobada. | Registrar cada exclusión como cambio de alcance con aprobación y fecha, y distinguir por escrito entre "no implementado" y "fuera de alcance". |
| **Desempeño e Integración del Cronograma Híbrido** | Velocidad observable de 16, 16 y 4 SP; hitos con fechas planificadas y reales; E2E en tres navegadores con 79 aprobadas y 0 fallidas. | H4 con 7 días de desfase; H6 sin cierre formal; SPI 0.7347 y 13 SP parciales arrastrados desde los Sprints 1 y 3. | Publicar burndown y burnup desde el primer sprint y tratar los enablers con dependencia externa como riesgos del cronograma, no como tareas ordinarias. |
| **Gestión del Presupuesto y Costos** | BAC estimado de $9,978.08 con desglose verificable y contingencia del 12 %; distinción explícita entre costo de oportunidad y desembolso. | No se registró AC, horas reales ni ejecución de contingencia; CV, CPI y EAC quedaron no evaluables. | Llevar un registro simple de horas reales por sprint desde el inicio; sin AC no existe cierre financiero posible, por riguroso que sea el presupuesto. |
| **Técnicas de Estimación** (Velocidad, duración, recursos) | Secuencia Fibonacci para 49 SP; medición real de 17.9–20.2 ms frente al SLA de 5 s; estimación de 480 horas trazable a 4 × 10 h/semana × 12 semanas. | Los 13 SP parciales no tenían porcentaje de avance verificable, por lo que no pudieron acreditarse como EV; las estimaciones nunca se contrastaron con horas ejecutadas. | Definir una regla de acreditación de SP parciales antes del primer sprint y registrar el porcentaje completado con evidencia, no por percepción. |
| **Procesos de Aseguramiento de Calidad** | 66 pytest, 24 Vitest y 79 E2E; corrección de 5 bugs y 2 code smells; neutralización de fórmulas CSV; Quality Gate y SonarQube con 0 hallazgos. | Cobertura backend 61 %/63 % sin reconciliar y por debajo del 70 %; Quality Gate con `ignoredConditions: true` y `new_coverage = 0.0`; Lighthouse limitado al login. | Fijar umbrales de cobertura que fallen el pipeline, versionar la salida cruda de cobertura y auditar pantallas autenticadas además del login. |
| **Involucramiento de Interesados (Stakeholders)** | Stakeholders identificados en el registro de interesados y KPIs públicos en el README; cadena de evidencia con capturas reales del sistema. | Sin sesión de revisión ni aceptación formal; SUS preparado pero no aplicado a operadores; satisfacción no medida. | Agendar la validación con operadores desde el Sprint 1 y dejar constancia de la fecha y de los participantes, aunque el proyecto sea académico. |
| **Gestión de Riesgos, Incidentes e Impedimentos** | Matriz RSK-01 a RSK-08 con severidad calculada; IMP-01, IMP-03 e IMP-S2-01 resueltos; IMP-10 documentado como limitación. | Hallazgos nuevos de cierre (credenciales demo, JWT inseguro por defecto, `VITE_API_URL` no efectiva, tope de 100 registros) no están en la matriz; no hubo incidentes de producción porque no hubo despliegue. | Actualizar la matriz de riesgos al cierre con los hallazgos de auditoría y hacer explícito que "sin incidentes" puede significar "sin exposición real". |

## 2. Conclusiones de la Retrospectiva de Cierre

El proyecto entregó un PMV funcional y verificable en local, con trazabilidad documental
amplia y evidencia cruda de pruebas, y aprendió a separar lo ejecutado de lo declarado:
"CI verde" no es "despliegue logrado", "instrumento SUS preparado" no es "usabilidad
medida", y "presupuesto estimado" no es "costo ejecutado". Esa disciplina permitió cerrar
36 de 49 SP y dejar los 13 restantes, las brechas de cobertura y los pendientes de
seguridad claramente identificados en lugar de disfrazados como logros.

El cierre, sin embargo, es **parcial**: faltan video MP4, aceptación formal de
stakeholders, SUS aplicado, Mood Chart, AC real para completar el EVM y despliegue en un
entorno controlado. Ninguna de esas ausencias se ha rellenado con cifras o imágenes
inventadas. Las ocho acciones `ACT-S4-01` a `ACT-S4-08`, con responsables y fechas hasta
el 08/12/2026, constituyen la lista concreta de trabajo pendiente y son la principal
herencia para un siguiente equipo: mantener la honestidad de la medición, cerrar la
brecha de cobertura y convertir la operación local en una entrega desplegable y
verificable por los interesados.

---

[← Volver al README Principal](../../README.md)
