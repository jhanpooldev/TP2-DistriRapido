# CONSTITUTION.md

## Estructura del Proyecto

Siempre utilizar una estructura de proyecto modular y mantenible.

**Proyecto:**

**EcoLogística Lima - Optimizador de Rutas Sostenibles para DistriRápido S.A.C.**

El proyecto será desarrollado como un Producto Mínimo Viable (PMV) durante un periodo académico de 12 semanas.

**Estructura raíz:**

/backend         # FastAPI (Python)

/frontend        # React + Vite

/docs            # Documentación

/tests           # Pruebas automatizadas

/docker          # Configuraciones Docker (opcional)

**Documentación:**

/docs/inicio

/docs/planificacion

/docs/ejecucion

/docs/seguimiento_control

/docs/cierre

/docs/otros

**Siempre incluir:**

- `README.md` (con Tabla de Contenidos)
- `.gitignore`
- `.env.example`
- `CHANGELOG.md`
- `CONSTITUTION.md`
- `SPECS.md`

El archivo `.env` no deberá incluirse en el repositorio.


---

## Estrategia de Desarrollo

Utilizar desarrollo incremental mediante **Scrum + Git Flow**.

**Reglas:**

- Implementar una funcionalidad a la vez.
- Una User Story por Pull Request.
- Validar cada funcionalidad antes de continuar.
- Ejecutar las pruebas antes de integrar los cambios.
- Mantener el PMV funcional durante el desarrollo.
- Mantener evidencia de la evolución progresiva.
- Evitar implementar múltiples funcionalidades mayores al mismo tiempo.


---

## Estándares de Codificación

### Python (Backend - FastAPI)

**Usar:**

- `snake_case` para variables y funciones.
- `PascalCase` para clases y modelos de Pydantic.
- Ruff o Black para formateo.
- Type hints obligatorios.

**Seguir:**

- Principios SOLID.
- Clean Code.
- Convenciones RESTful API.
- Patrón Service Layer.
- Patrón Repository cuando sea aplicable.
- Separación de responsabilidades.

### JavaScript (Frontend - React)

**Usar:**

- `camelCase` para variables y funciones.
- `PascalCase` para componentes React.
- ESLint.
- Prettier.
- Componentes funcionales.
- React Hooks.

**Seguir:**

- Principios SOLID cuando sean aplicables.
- Clean Code.
- Organización basada en funcionalidades (Feature-based).
- Componentes reutilizables.
- Separación entre presentación y lógica.

**Evitar:**

- Class components.
- Lógica de negocio dentro de componentes de UI.
- Código duplicado innecesariamente.
- Componentes excesivamente grandes.


---

## Estándares del Backend

Utilizar:

- FastAPI.
- Pydantic para validación de datos.
- SQLAlchemy ORM.
- Endpoints asíncronos cuando sea posible.
- Patrón Service Layer.
- Patrón Repository cuando sea necesario.
- APIs RESTful.
- Swagger/OpenAPI para documentación automática.

El Backend será responsable de:

- Implementar la lógica de negocio.
- Validar los datos.
- Gestionar la persistencia.
- Exponer las APIs.
- Procesar la información relacionada con las rutas sostenibles.
- Gestionar las reglas de negocio.


---

## Estándares del Frontend

Utilizar:

- React.
- Vite.
- Componentes funcionales.
- React Hooks.
- Context API para manejo de estado cuando sea necesario.
- Axios para peticiones HTTP.
- Tailwind CSS para estilos.
- ESLint.
- Prettier.

El Frontend será responsable de:

- Presentar la interfaz UI/UX.
- Gestionar la interacción con el usuario.
- Consumir las APIs del Backend.
- Mostrar información y resultados.
- Gestionar estados de carga y error.

La lógica principal del negocio deberá permanecer en el Backend.


---

## Arquitectura del Sistema

Utilizar una arquitectura con separación clara entre Frontend y Backend.

**Frontend:**

- Capa de presentación.
- Interfaz UI/UX.
- Componentes React.
- Consumo de APIs.

**Backend:**

- Capa de API.
- Capa de servicios.
- Capa de acceso a datos.
- Lógica de negocio.
- Validación.
- Persistencia.

La arquitectura deberá favorecer:

- Separación de responsabilidades.
- Mantenibilidad.
- Escalabilidad.
- Modularidad.
- Bajo acoplamiento.
- Alta cohesión.


---

## Estrategia de Pruebas (TDD)

Utilizar **TDD (Test-Driven Development)** en las funcionalidades principales.

**Ciclo:**

1. **RED** – Escribir una prueba que falla.
2. **GREEN** – Implementar el código mínimo para que pase.
3. **REFACTOR** – Mejorar el código sin romper las pruebas.

**Herramientas de Pruebas:**

- `pytest + pytest-cov` (backend).
- `Vitest + @vitest/coverage-v8` (frontend).

**Objetivo de Cobertura:**

- Total ≥ 70%.
- Módulo de validación ≥ 80%.
- Módulo CSP ≥ 70%, cuando sea implementado.
- No integrar código que rompa las pruebas existentes.


---

## Seguridad

Seguir las buenas prácticas de **OWASP Top 10**:

- JWT con expiración de 8 horas cuando se implemente autenticación.
- Validación de entrada mediante Pydantic.
- Prevención de SQL Injection mediante SQLAlchemy.
- Hashing de contraseñas con bcrypt.
- Rate limiting.
- Variables de entorno para secretos.
- HTTPS en producción.
- Manejo seguro de errores.

Nunca almacenar en el repositorio:

- Contraseñas.
- Tokens.
- Claves API.
- Credenciales.
- Secretos.


---

## Reglas de Git

Utilizar **Conventional Commits**:

- `feat:` nueva funcionalidad.
- `fix:` corrección de errores.
- `refactor:` refactorización.
- `docs:` documentación.
- `test:` pruebas.
- `chore:` mantenimiento.

**Estrategia de ramas (Git Flow):**

- `main` → producción, siempre estable.
- `develop` → integración.
- `feature/*` → nuevas funcionalidades.
- `release/*` → preparación de releases.
- `hotfix/*` → correcciones urgentes.

**Ejemplos:**

- `feature/login`
- `feature/optimizacion-rutas`
- `feature/gestion-vehiculos`
- `feature/gestion-entregas`
- `feature/reportes`

**Pull Requests:**

- Obligatorias para `main` y `develop`.
- Mínimo 1 revisor.
- Todas las pruebas deben pasar.
- Cada PR deberá corresponder a una funcionalidad, corrección o tarea.
- Los cambios deberán estar descritos claramente.
- Las PR deberán integrarse mediante GitHub.


---

## Versionamiento Semántico

Utilizar **Semantic Versioning (SemVer)**:

`MAJOR.MINOR.PATCH`

**MAJOR:**

Cambios incompatibles con versiones anteriores.

`v1.0.0 → v2.0.0`

**MINOR:**

Nueva funcionalidad compatible.

`v1.0.0 → v1.1.0`

**PATCH:**

Corrección de errores.

`v1.0.0 → v1.0.1`

**Versión del PMV:**

El Producto Mínimo Viable deberá identificarse obligatoriamente como:

`v1.0.0`

La versión `v1.0.0` deberá registrarse mediante un **Git Tag**.


---

## Límites (Boundaries)

**NO modificar sin motivo justificado:**

- `requirements.txt`.
- `package-lock.json`.
- Valores reales del `.env`.
- Migraciones generadas automáticamente.
- Configuraciones funcionales.
- Código existente que funcione correctamente.

Nunca eliminar código existente que funcione a menos que sea reemplazado de forma segura.

Los cambios importantes deberán ser justificados, probados y registrados mediante Git.


---

## Variables de Entorno

Utilizar variables de entorno para configuraciones sensibles.

**Archivos:**

- `.env` → configuración local, no subir al repositorio.
- `.env.example` → plantilla de configuración.

El `.env.example` no deberá contener:

- Contraseñas reales.
- Tokens reales.
- Claves API reales.
- Credenciales reales.

El `.gitignore` deberá incluir el archivo `.env`.


---

## Requisitos de Documentación

Siempre documentar:

- Problemática del proyecto.
- Justificación del PMV.
- Objetivos.
- Integrantes del equipo.
- Tecnologías utilizadas.
- Arquitectura del sistema.
- Endpoints de API.
- Esquema de base de datos.
- Instrucciones de instalación.
- Instrucciones de ejecución.
- Instrucciones de build.
- Instrucciones de despliegue.

**Documentación técnica:**

- Endpoints de API → FastAPI / Swagger / OpenAPI.
- Esquema de base de datos → `SPECS.md`.
- Instrucciones de instalación → `README.md`.
- Decisiones arquitectónicas → `CONSTITUTION.md`.
- Historial de cambios → `CHANGELOG.md`.


---

## Documentación PMBOK

La documentación deberá organizarse dentro de `docs/` según las áreas establecidas en la consigna.

**Inicio:**

`docs/inicio/`

- Problemática.
- Justificación.
- Objetivos.
- Actores.
- Alcance inicial.

**Planificación:**

`docs/planificacion/`

- Requisitos.
- Alcance.
- Cronograma.
- Recursos.
- Riesgos.
- Plan de trabajo.

**Ejecución:**

`docs/ejecucion/`

- Desarrollo.
- Implementación.
- Avances.
- Decisiones técnicas.
- Integración.

**Seguimiento y Control:**

`docs/seguimiento_control/`

- Seguimiento del avance.
- Control de cambios.
- Riesgos.
- Incidencias.
- Estado del proyecto.

**Cierre:**

`docs/cierre/`

- Resultados.
- Conclusiones.
- Lecciones aprendidas.
- Cumplimiento de objetivos.
- Trabajo futuro.

**Otros:**

`docs/otros/`

Documentación adicional necesaria para el proyecto.


---

## README.md

El archivo `README.md` deberá contener obligatoriamente:

- Nombre del proyecto.
- Tabla de Contenidos.
- Integrantes del equipo.
- Problemática abordada.
- Justificación del PMV.
- Tecnologías utilizadas.
- Arquitectura del sistema.
- Instrucciones de instalación.
- Instrucciones de build.
- Instrucciones de despliegue.
- Enlace al video explicativo.
- Enlaces a la documentación ubicada en `docs/`.

El README deberá mantenerse actualizado durante todo el desarrollo.


---

## SPECS.md

El archivo `SPECS.md` deberá contener la especificación técnica del sistema.

Deberá documentar como mínimo:

- Entidades principales.
- Relaciones entre entidades.
- Esquema de base de datos.
- Reglas de negocio relevantes.
- Estructura de las APIs.
- Parámetros de entrada.
- Respuestas esperadas.
- Restricciones técnicas.


---

## Evidencia de Desarrollo

El repositorio deberá evidenciar:

- Historial de commits.
- Uso de ramas.
- Pull Requests.
- Integración de cambios.
- Evolución progresiva del PMV.
- Trabajo colaborativo entre los integrantes.

**Objetivo según la rúbrica:**

- Más de 5 ramas.
- Más de 20 commits significativos.
- Pull Requests correctamente integradas.
- Participación de los integrantes.
- Evolución progresiva del proyecto.

No se deberán crear commits, ramas o Pull Requests artificiales únicamente para cumplir con la rúbrica.


---

## Video Explicativo

El proyecto deberá contar con un video explicativo de máximo **5 minutos**.

El video deberá:

- Presentar la problemática.
- Presentar la solución propuesta.
- Demostrar el PMV.
- Mostrar las funcionalidades principales.
- Mostrar el sistema funcionando.
- Explicar brevemente el valor de la solución.

El enlace deberá estar incluido en el `README.md`.


---

## Buenas Prácticas del Repositorio

El repositorio deberá mantenerse:

- Organizado.
- Limpio.
- Accesible.
- Actualizado.
- Sin archivos innecesarios.
- Sin credenciales.
- Sin archivos temporales innecesarios.

Se deberá utilizar correctamente el `.gitignore`.

La URL del repositorio deberá mantenerse estable durante todo el periodo académico.


---

## Requisitos de Entrega

Antes de finalizar el proyecto se deberá verificar:

- [ ] Repositorio GitHub creado y accesible.
- [ ] URL estable.
- [ ] Enlace compartido con el docente.
- [ ] Frontend implementado.
- [ ] Backend implementado.
- [ ] Separación clara Frontend / Backend.
- [ ] Arquitectura documentada.
- [ ] `.gitignore` configurado.
- [ ] `.env` excluido.
- [ ] `.env.example` disponible.
- [ ] Más de 5 ramas.
- [ ] Más de 20 commits significativos.
- [ ] Pull Requests integradas.
- [ ] Git Flow aplicado.
- [ ] Conventional Commits aplicado.
- [ ] Versionamiento semántico aplicado.
- [ ] Tag `v1.0.0` creado.
- [ ] `README.md` completo.
- [ ] `SPECS.md` completo.
- [ ] `CHANGELOG.md` actualizado.
- [ ] Documentación PMBOK completa.
- [ ] Evidencia de trabajo colaborativo.
- [ ] PMV funcional.
- [ ] Pruebas automatizadas implementadas.
- [ ] Cobertura ≥ 70%.
- [ ] Video explicativo de máximo 5 minutos.
- [ ] Enlace del video incluido en README.


---

## Criterios de Calidad

El proyecto deberá orientarse al nivel **Sobresaliente (3)** de la rúbrica.

Se deberá procurar alcanzar:

- Repositorio correctamente configurado.
- Más de 5 ramas.
- Más de 20 commits descriptivos.
- Pull Requests correctamente integradas.
- Git Flow aplicado.
- Versionamiento semántico correcto.
- PMV etiquetado como `v1.0.0`.
- Frontend y Backend claramente separados.
- Arquitectura mantenible.
- Código limpio y organizado.
- `.gitignore` correctamente configurado.
- Documentación completa.
- README completo.
- Trabajo colaborativo evidenciado.
- Evolución progresiva del PMV.
- PMV funcional.
- Video accesible y de máximo 5 minutos.


---

## Gestión de Cambios

Todo cambio importante que afecte:

- Arquitectura.
- Tecnologías.
- Requisitos.
- Alcance.
- Base de datos.
- Seguridad.
- Estructura del proyecto.

Deberá ser documentado y registrado mediante Git.

Los cambios relevantes deberán reflejarse en:

- `CHANGELOG.md`.
- `SPECS.md`, cuando corresponda.
- Documentación dentro de `docs/`, cuando corresponda.


---

## Enmiendas a la Constitución

Esta constitución solo puede ser modificada mediante:

- Consenso del equipo (4/4 votos).
- Acuerdo del Product Owner (profesor).

Todas las enmiendas deberán quedar documentadas en el `CHANGELOG.md`.

Ninguna modificación podrá contradecir los requisitos establecidos en la consigna oficial del Proyecto de Fin de Asignatura.


---

## Principio Fundamental

El proyecto deberá demostrar no solamente que el **Producto Mínimo Viable funciona**, sino también que existe evidencia de:

- Planificación.
- Desarrollo progresivo.
- Trabajo colaborativo.
- Control de versiones.
- Arquitectura organizada.
- Buenas prácticas de programación.
- Pruebas automatizadas.
- Seguridad.
- Documentación técnica.
- Versionamiento semántico.
- Cumplimiento de los requisitos académicos.

La prioridad será mantener un proyecto **funcional, mantenible, documentado, trazable y alineado con los criterios de evaluación del PFA de EcoLogística Lima**.