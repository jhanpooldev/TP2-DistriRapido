[← Volver al README Principal](../../README.md)

# Presupuesto del Proyecto

**Proyecto:** EcoLogística Lima – Optimizador de Rutas Sostenibles para DistriRápido S.A.C.
**Versión:** 1.0.0 | **Fecha:** 10/09/2026

> **Nota de moneda:** este artefacto expresa los montos en USD, conforme al formato exigido por la consigna de Planificación. El Acta de Constitución (Fase de Inicio) expresó el presupuesto referencial en Soles (S/); ambos son estimaciones de costo de oportunidad y no desembolsos reales, dado el carácter académico del proyecto.

## 1. Costo de Recursos Humanos (CAPEX)

Cálculo: **Costo = Horas Asignadas × Tarifa Hora (USD)**. Tarifas referenciales de mercado para talento junior/semi-senior remoto en la región. Total de horas del equipo: 4 integrantes × 10 h/semana × 12 semanas = 480 horas.

| Rol | Horas Asignadas | Tarifa/Hora (USD) | Costo (USD) | Cubierto principalmente por |
|---|:---:|:---:|---:|---|
| Project Manager | 70 | $18.00 | $1,260.00 | Jhunior Cosme (Director de Proyecto) |
| Software Architect | 30 | $25.00 | $750.00 | Jhanpool Flores (Backend/Arquitecto) |
| Senior Developer | 150 | $22.00 | $3,300.00 | Jhanpool Flores, apoyo puntual del resto del equipo |
| Junior Developer | 130 | $15.00 | $1,950.00 | Todo el equipo (tareas de menor complejidad) |
| QA Engineer | 70 | $16.00 | $1,120.00 | Andrew Vega (QA & DevOps) |
| UI/UX Designer | 30 | $17.00 | $510.00 | Ricardo Tucto (Frontend/UX-UI) |
| **Subtotal RRHH** | **480** | | **$8,890.00** | |

## 2. Costo de Licenciamiento y Herramientas

| Herramienta | Uso | Costo (USD) |
|---|---|---:|
| Visual Studio Code | IDE de desarrollo | $0.00 (gratuito) |
| Atlassian Jira Software | Gestión ágil (plan Free, hasta 10 usuarios) | $0.00 (plan gratuito) |
| Figma | Diseño UI/UX (plan Starter) | $0.00 (plan gratuito) |
| SonarCloud | Análisis estático de código (repositorios públicos) | $0.00 (plan gratuito) |
| GitHub | Control de versiones y CI/CD (GitHub Actions) | $0.00 (plan gratuito) |
| **Subtotal Licenciamiento** | | **$0.00** |

## 3. Costo de Infraestructura Cloud y Servicios (OPEX)

| Servicio | Detalle | Costo (USD) |
|---|---|---:|
| Hosting Frontend (Vercel) | Plan gratuito | $0.00 |
| Hosting Backend (Render) | Plan gratuito, con upgrade puntual a tier básico para evitar "cold starts" durante la demo final | $7.00 |
| Base de datos gestionada (Supabase) | Plan gratuito (PostgreSQL) | $0.00 |
| Dominio personalizado (opcional) | 1 año, dominio .com | $12.00 |
| Certificado SSL | Incluido en el hosting (Let's Encrypt) | $0.00 |
| **Subtotal Infraestructura (OPEX)** | | **$19.00** |

## 4. Reserva de Contingencia

Calculada sobre el subtotal del proyecto (RRHH + Licenciamiento + Infraestructura), con base en la severidad de los riesgos identificados en el Registro de Riesgos (predominancia de riesgos de severidad Media/Alta justifica el extremo superior del rango sugerido de 10-15%).

**Contingencia aplicada: 12%**

## 5. Tabla Resumen Financiera

| Categoría | Costo Subtotal (USD) | Porcentaje del Total |
|---|---:|---:|
| 1. Recursos Humanos (CAPEX) | $8,890.00 | 99.8% |
| 2. Licenciamiento de Software | $0.00 | 0.0% |
| 3. Infraestructura Cloud (OPEX) | $19.00 | 0.2% |
| **SUBTOTAL DE PROYECTO** | **$8,909.00** | **100.0%** |
| 4. Reserva de Contingencia (12%) | $1,069.08 | N/A |
| **PRESUPUESTO TOTAL ESTIMADO** | **$9,978.08** | **100.0%** |

## 6. Justificación de la Consolidación

El presupuesto está dominado casi en su totalidad (99.8%) por el costo de oportunidad de las horas del equipo, lo cual es coherente con el alcance de un PMV académico: no existe inversión real en licencias (uso exclusivo de planes gratuitos) y la infraestructura cloud se mantiene en niveles free-tier, con un margen mínimo reservado ($19.00) únicamente para evitar fricciones técnicas durante la demostración final del producto. La contingencia del 12% responde directamente al perfil de riesgo cuantificado en el Registro de Riesgos, donde predominan riesgos de severidad Media con un riesgo de severidad Alta (RSK-02, ligado al algoritmo de optimización), lo que justifica no aplicar el extremo inferior (10%) del rango sugerido.

---

[← Volver al README Principal](../../README.md)
