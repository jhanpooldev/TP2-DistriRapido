# AGENTS.md

## Estructura del Proyecto

Siempre utiliza una estructura de proyecto modular y mantenible.

**Estructura del Proyecto:**

```text
/docs/01 Inicio             # Documentación de inicio y visión del proyecto
/docs/02 Planificación       # Planificación, requisitos, base de datos y plan de pruebas
/docs/03 Implementación      # Entregables por sprint (Sprint 1, Sprint 2)
/docs/04 Arquitectura       # Arquitectura del sistema, Modelo C4 y especificaciones técnicas
/docs/05 Evidencias         # Evidencias de pruebas, auditorías y validaciones
/src/backend                # Backend FastAPI (Python)
/src/frontend               # Frontend React + Vite
```

**Siempre incluir:**

- `README.md`
- `DESIGN.md`
- `AGENTS.md`
- `CONSTITUTION.md`
- `SPECS.md`
- `CHANGELOG.md`
- `.gitignore`
- `.env.example`

Las pruebas automatizadas viven dentro de cada aplicación:
`/src/backend/tests` (pytest) y `/src/frontend/src/**/*.test.jsx` (Vitest).

Docker y `docker-compose.yml` son opcionales y no se aplican en el PMV.

---

## Estrategia de Desarrollo

Utilizar desarrollo incremental.

**Reglas:**

- Implementar una funcionalidad a la vez.
- Validar cada funcionalidad antes de pasar a la siguiente.
- Ejecutar las pruebas antes de continuar.
- Nunca implementar múltiples funcionalidades mayores al mismo tiempo.

---

## Estándares de Codificación

### Python (Backend - FastAPI)

**Usar:**

- `snake_case` para variables y funciones
- `PascalCase` para clases y modelos de Pydantic
- Ruff o Black para formateo
- Type hints (obligatorio)

**Seguir:**

- Principios SOLID
- Clean Code
- Convenciones RESTful API
- Patrón Service Layer
- Patrón Repository cuando sea aplicable

### JavaScript (Frontend - React)

**Usar:**

- `camelCase` para variables
- `PascalCase` para componentes de React
- ESLint
- Prettier

**Seguir:**

- Principios SOLID
- Clean Code

---

## Estándares del Backend

Utilizar:

- FastAPI
- Pydantic para validación de entrada
- SQLAlchemy ORM
- Patrón Service Layer
- Patrón Repository cuando sea aplicable

---

## Estándares del Frontend

Utilizar:

- Componentes funcionales
- React Hooks
- Estructura de carpetas basada en funcionalidades (Feature-based)
- Context API para manejo de estado
- Axios para peticiones HTTP

**Evitar:**

- Class components
- Lógica de negocio dentro de componentes de UI

---

## Herramientas a Utilizar

Siempre utilizar:

- Git
- Bash
- npm (frontend) / pip (backend)

**Calidad de Código:**

- Ruff (Python) / ESLint (JavaScript)
- Black (Python) / Prettier (JavaScript)

**Pruebas:**

- `pytest + pytest-cov` (backend)
- `Vitest + @vitest/coverage-v8` (frontend)

---

## Límites (Boundaries)

**NO modificar:**

- `requirements.txt` sin motivo justificado
- `package-lock.json` sin motivo justificado
- Valores del `.env`
- Migraciones generadas automáticamente salvo que sea necesario

Nunca eliminar código existente que funcione a menos que se esté reemplazando de forma segura.

---

## Seguridad

Seguir:

- OWASP Top 10
- Manejo seguro de JWT (expiración de 8 horas)
- Validación de entrada usando Pydantic
- Rate limiting
- Hashing de contraseñas con bcrypt
- Prevención de SQL injection (SQLAlchemy)

---

## Reglas de Git

Utilizar **Conventional Commits**:

- `feat:` nueva funcionalidad
- `fix:` corrección de errores
- `refactor:` refactorización de código
- `docs:` documentación
- `test:` pruebas
- `chore:` mantenimiento

**Importante:** Realizar commit después de completar cada funcionalidad.

---

---

