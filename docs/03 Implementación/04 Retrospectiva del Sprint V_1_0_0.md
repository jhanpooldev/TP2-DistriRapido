# Reprospectiva del sprint

[⬅ Volver al README principal](../../README.md)

---

**Nombre del Proyecto:** EcoLogística Lima – Optimizador de Rutas Sostenibles para DistriRápido S.A.C.

**Líder del Proyecto:** Jhunior Harold Cosme Tenorio

---

## Control de Versiones del Documento

| Versión | Fecha | Autor | Descripción del Cambio |
|:---:|:---:|:---|:---|
| 1.0.0 | 01/10/2026 | Jhunior Harold Cosme Tenorio / Equipo EcoLogística | Elaboración de la Retrospectiva del Sprint 1 tras la sesión de revisión con el equipo. |

---

## ¿Qué aprendimos?

Durante el desarrollo del Sprint 1, el equipo consolidó aprendizajes técnicos y metodológicos significativos:

1. **Metodología Guiada por Especificaciones (Spec-Driven Development):**
   - Aprendimos que definir contratos claros en formato OpenSpec antes de escribir código reduce drásticamente el retrabajo y elimina ambigüedades respecto a parámetros cuantificables (tiempos de expiración, ventanas de tolerancia, umbrales de reintentos).
2. **Implementación Estricta del Estándar TOTP (RFC 6238):**
   - Comprendimos la importancia de considerar el desfase temporal (*Clock Drift*) entre el servidor y los dispositivos móviles, aplicando una tolerancia de ventana de tiempo (±30s) para evitar falsos rechazos en usuarios legítimos.
3. **Gestión de Ciclo de Vida de Sesiones Stateless:**
   - Asimilamos que los tokens JWT no pueden invalidarse por sí solos antes de su fecha de expiración; para cumplir con OWASP ASVS y soportar un logout seguro es indispensable incorporar el claim `jti` y una lista de revocación (blacklist).
4. **Auditoría de Requisitos con Inteligencia Artificial:**
   - La aplicación de prompts estructurados de auditoría técnica permitió detectar tempranamente riesgos de seguridad críticos, como la necesidad de un token efímero intermedio (`mfa_token`) para evitar bypass del segundo factor.

---

## ¿Qué estamos haciendo bien?

1. **Compromiso y Ritmo de Desarrollo Sostenible:**
   - Se completó el 100% de las Historias de Usuario comprometidas (26 Story Points) dentro de los tiempos estipulados sin sobrecargar a ningún miembro del equipo.
2. **Cultura de Pruebas Automatizadas desde el Inicio:**
   - Se alcanzó una cobertura de código del **91%**, implementando pruebas para rutas Gold, Feliz e Infeliz que garantizan la estabilidad del sistema frente a futuros cambios.
3. **Control de Versiones Limpio y Trazable:**
   - Uso disciplinado de ramas individuales por integrante (ej. rama `flores`) y adopción rigurosa del estándar **Conventional Commits** (`feat:`, `test:`, `docs:`), facilitando la revisión y auditoría del código.
4. **Documentación Viva y Sincronizada:**
   - Mantenimiento coherente entre los diagramas, reglas de negocio (`RN-001` a `RN-006`), especificaciones OpenSpec y la implementación real en FastAPI.

---

## ¿Qué podemos hacer mejor?

### Personas
- **Gestión individual del tiempo en tareas de investigación:** Se invirtió tiempo excesivo investigando librerías secundarias antes de validar la compatibilidad de paquetes con la versión de Python instalada. Se debe definir un límite de tiempo (*timebox*) para la evaluación de tecnologías antes de consultar con el equipo.
- **Autonomía en resolución de bloqueos de entorno:** Mejorar la documentación compartida sobre configuraciones locales de Windows (permisos de PowerShell, variables de entorno) para que cada miembro resuelva incidencias de entorno con mayor agilidad.

### Relaciones
- **Comunicación cruzada Frontend - Backend:** Aunque la especificación de API fue clara en Swagger, se requiere una mayor sincronización diaria entre el desarrollador backend y el equipo frontend durante la fase de definición de payloads para evitar ajustes tardíos en los nombres de atributos.
- **Feedback temprano en Pull Requests:** Establecer revisiones de código (*code reviews*) más frecuentes y con comentarios constructivos entre pares antes de fusionar ramas a la rama principal.

### Procesos
- **Definición de Criterios de Aceptación (DoD - Definition of Done):** Asegurar que la "Definición de Terminado" incluya siempre la actualización del archivo `README.md` y la ejecución del análisis estático de código antes de dar por cerrada una Historia de Usuario.
- **Estimación de Historias de Usuario con dependencias criptográficas:** En futuras estimaciones se debe contemplar un margen adicional para la elaboración de pruebas de borde (edge cases) como desincronización horaria, claves duplicadas y ataques de fuerza bruta.

### Herramientas
- **Estandarización de Contenedores Docker:** Avanzar en la configuración de Docker y Docker Compose para garantizar que el entorno de desarrollo sea idéntico entre todos los integrantes, evitando disparidades entre sistemas operativos o versiones locales de paquetes.
- **Automatización de CI/CD con GitHub Actions:** Configurar pipelines automáticos que ejecuten `pytest` y la verificación de cobertura en cada push a cualquier rama remota.

---

## Acciones a realizar

Con base en el análisis de los cuatro ejes, el equipo se compromete a ejecutar el siguiente plan de acción para el **Sprint 2**:

| # | Acción de Mejora Concreta | Eje | Responsable | Fecha Límite | Criterio de Éxito |
|:---:|:---|:---:|:---:|:---:|:---|
| **ACT-01** | Configurar archivo `docker-compose.yml` para levantar PostgreSQL y la API de FastAPI en un entorno estandarizado. | Herramientas | Andrew Steven Vega Reyes | 05/10/2026 | Contenedores levantando con `docker compose up` en los equipos de los 4 integrantes. |
| **ACT-02** | Implementar reuniones diarias de sincronización (*Daily Standups*) de máximo 10 minutos a través de Discord/Meet. | Relaciones | Jhunior Harold Cosme Tenorio | 02/10/2026 | Registro de asistencia y resolución de impedimentos en menos de 24 horas. |
| **ACT-03** | Crear workflow de GitHub Actions (`.github/workflows/ci.yml`) para ejecución automática de tests en cada Pull Request. | Procesos | Andrew Steven Vega Reyes / Jhanpool Flores | 07/10/2026 | Verificación de build y cobertura verde visible en los PRs de GitHub. |
| **ACT-04** | Establecer un canal compartido de contratos de API para validar conjuntamente los modelos Pydantic y componentes React antes de iniciar el código del Sprint 2. | Personas / Procesos | Jhanpool Flores / Ricardo Tucto | 04/10/2026 | Contrato de endpoints de rutas y pedidos aprobado por ambas partes en Swagger/OpenSpec. |

---

[⬅ Volver al README principal](../../README.md)
