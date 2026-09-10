[← Volver al README Principal](../../README.md)

# Registro de Riesgos

**Proyecto:** EcoLogística Lima – Optimizador de Rutas Sostenibles para DistriRápido S.A.C.
**Versión:** 1.0.0 | **Fecha:** 10/09/2026

## Metodología de Cálculo

**Severidad (Exposición) = Probabilidad (1 a 5) × Impacto (1 a 5)**

- **Probabilidad:** 1 (Muy baja) a 5 (Muy alta)
- **Impacto:** 1 (Insignificante) a 5 (Catastrófico)
- **Bandas de Severidad:** Low = 1-6 · Medium = 8-12 · High = 15-25

## Matriz de Evaluación de Riesgos

| ID | Descripción del Riesgo | Categoría | Prob. | Imp. | Severidad | Plan de Mitigación (Preventivo) | Plan de Contingencia (Reactivo) | Responsable |
|---|---|---|:---:|:---:|:---:|---|---|---|
| RSK-01 | Indisponibilidad o límites de cuota de las APIs externas de geolocalización (OpenStreetMap/Leaflet). | Técnica / Infraestructura | 2 | 4 | 8 (Media) | Monitorear el consumo de cuotas e implementar alertas de umbral al 70%. | Migrar temporalmente a un proveedor de mapas alterno o usar caché local de resultados ya calculados. | Backend Developer / Arquitecto |
| RSK-02 | La complejidad del algoritmo de optimización de rutas excede el tiempo disponible en el sprint. | Técnica | 3 | 5 | 15 (Alta) | Implementar primero una heurística simple (Nearest Neighbor) y refinar de forma incremental (2-opt) en sprints posteriores. | Congelar el algoritmo en su versión heurística básica y postergar el refinamiento a una versión posterior al PMV. | Backend Developer / Arquitecto |
| RSK-03 | Curva de aprendizaje elevada en el framework del frontend (React). | Recursos Humanos / Capacidades | 3 | 3 | 9 (Media) | Realizar 2 jornadas de Pair Programming y pases de conocimiento al inicio del Sprint 1. | Reasignar temporalmente las tareas de mayor complejidad al integrante con más experiencia en frontend. | Frontend Developer / Scrum Master |
| RSK-04 | Disponibilidad limitada de los integrantes por carga académica de otros cursos paralelos. | Operativa | 3 | 3 | 9 (Media) | Planificar la capacidad semanal en Jira por integrante y distribuir tareas de forma equitativa. | Redistribuir tareas entre el resto del equipo o negociar una extensión interna de 2-3 días dentro del mismo sprint. | Director de Proyecto / Scrum Master |
| RSK-05 | Conflictos de código o pérdida de avances por mal manejo de Git. | Operativa / Técnica | 2 | 3 | 6 (Baja) | Flujo de ramas definido (feature branches), commits frecuentes y Pull Request obligatorio antes de integrar a main. | Restaurar desde el último commit estable en main y reforzar capacitación exprés en Git al equipo. | QA & DevOps |
| RSK-06 | Vulnerabilidades de seguridad no detectadas antes del despliegue. | Seguridad | 2 | 5 | 10 (Media) | Análisis estático automatizado (SonarQube/CodeQL) obligatorio en cada Pull Request, según el DoD global. | Rollback inmediato del despliegue afectado y priorización de un parche de emergencia en el siguiente ciclo. | QA & DevOps |
| RSK-07 | Configuración incompleta o incorrecta de Jira afecta la trazabilidad del backlog y del sprint. | Gestión / Herramientas | 2 | 2 | 4 (Baja) | Checklist de configuración inicial de Jira (jerarquía, backlog, roadmap, versión) validado por el Director de Proyecto. | Sesión de reconfiguración guiada antes del cierre del Sprint 1, usando este documento como referencia. | Director de Proyecto |
| RSK-08 | Cambios de alcance (scope creep) durante el refinamiento del backlog. | Alcance | 3 | 4 | 12 (Media) | Todo ítem nuevo pasa por una evaluación de impacto antes de ingresar al sprint en curso. | Mover el ítem nuevo al backlog del siguiente sprint en lugar de interrumpir el sprint activo. | Director de Proyecto |

## Resumen por Nivel de Severidad

| Nivel | Cantidad de Riesgos | IDs |
|---|:---:|---|
| Alta (15-25) | 1 | RSK-02 |
| Media (8-12) | 5 | RSK-01, RSK-03, RSK-04, RSK-06, RSK-08 |
| Baja (1-6) | 2 | RSK-05, RSK-07 |

El único riesgo de severidad **Alta** (RSK-02) coincide con el riesgo técnico más crítico ya identificado en el Acta de Constitución (impacto "Alto" sobre el algoritmo de optimización), lo que confirma la coherencia entre ambos documentos y justifica que su mitigación se priorice desde el primer sprint.

---

[← Volver al README Principal](../../README.md)
