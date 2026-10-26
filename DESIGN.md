# DESIGN.md

Documento de decisiones de diseño, convenciones y arquitectura del sistema **EcoLogística Lima — DistriRápido S.A.C.**

---

## 1. Decisiones de Diseño y Arquitectura

El diseño global del sistema está documentado en los siguientes artefactos del repositorio:

1. **Constitución del Proyecto:** [CONSTITUTION.md](CONSTITUTION.md)
   - Estrategia de desarrollo ágil (Scrum + Git Flow).
   - Estándares de codificación para Python (FastAPI) y React (JavaScript/JSX).
   - Patrones arquitecturales: Service Layer, Repository, Feature-based frontend.
   - Políticas de seguridad (OWASP Top 10, JWT con expiración de 8 horas, bcrypt).
   - Directrices para pruebas automatizadas (TDD con pytest y Vitest).

2. **Especificación Técnica del Sistema:** [SPECS.md](SPECS.md)
   - Definición funcional y matemática del algoritmo de ruteo sostenible.
   - Fórmula geodésica de Haversine, heurística de Vecino Más Cercano y refinamiento 2-opt.
   - Parámetros de emisión de CO₂ y consumo de combustible por tipo de vehículo.
   - Actores y matriz de permisos.

3. **Arquitectura de Software (Modelo C4):** [`docs/04 Arquitectura/01 Modelo C4 V_1_0_0.md`](docs/04%20Arquitectura/01%20Modelo%20C4%20V_1_0_0.md)
   - Diagrama de Contexto del Sistema (Nivel 1).
   - Diagrama de Contenedores (Nivel 2: React SPA, FastAPI REST API, PostgreSQL).
   - Diagrama de Componentes Backend y Frontend (Nivel 3).
   - Diagrama de Código y Patrones de Diseño (Nivel 4).

4. **Especificación de Seguridad y MFA:** [`docs/04 Arquitectura/02 Especificacion MFA y Sesiones V_1_0_0.md`](docs/04%20Arquitectura/02%20Especificacion%20MFA%20y%20Sesiones%20V_1_0_0.md)
   - Especificaciones OpenSpec en [`docs/04 Arquitectura/specs/`](docs/04%20Arquitectura/specs/).
   - Algoritmo TOTP (RFC 6238), política de bloqueo por intentos fallidos y revocación de JWT.

5. **Diseño de Base de Datos:** [`docs/02 Planificación/10 Base de datos V_1_0_0.md`](docs/02%20Planificación/10%20Base%20de%20datos%20V_1_0_0.md)
   - Modelo conceptual (ER), modelo lógico relacional (3FN) y DDL físico versionado en `src/backend/esquema.sql`.

6. **Instrucciones para Agentes de Inteligencia Artificial:** [AGENTS.md](AGENTS.md)
   - Convenciones, límites técnicos y buenas prácticas de pair-programming.
