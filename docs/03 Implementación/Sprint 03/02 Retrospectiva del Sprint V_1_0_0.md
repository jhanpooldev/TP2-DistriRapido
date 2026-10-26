# Retrospectiva del sprint

[← Volver al README principal](../../../README.md)

---

**Nombre del Proyecto:** EcoLogística Lima – Optimizador de Rutas Sostenibles para DistriRápido S.A.C.

**Líder del Proyecto:** Jhunior Harold Cosme Tenorio

**Sprint:** 3

**Periodo:** 02/11/2026 – 08/11/2026

**Fecha de verificación local:** 26/10/2026

---

## Control de Versiones del Documento

| Versión | Fecha | Autor | Descripción del Cambio |
|:---:|:---:|:---|:---|
| 1.0.0 | 08/11/2026 | Jhunior Harold Cosme Tenorio / Equipo EcoLogística | Retrospectiva del Sprint 3. |

---

## ¿Qué aprendimos?

1. **Un pipeline de CI no equivale a un pipeline de CD.** El workflow de integración
   continua puede ejecutar pruebas, cobertura y build, pero EN-03 exige además que la
   versión quede accesible en Staging. Sin un host y sus credenciales, el criterio no se
   cumple. Llamar "terminado" al enabler por tener el archivo YAML habría sido una
   afirmación falsa.
2. **La cobertura global puede ocultar brechas por módulo.** El backend está en 59.89 %
   global, pero el módulo nuevo de exportación (`exportacion.py`) tiene 100 % y el
   optimizador 82 %. La deuda se concentra en los endpoints que dependen de PostgreSQL,
   no en la lógica de negocio nueva.
3. **La exportación también es una superficie de ataque.** Un destinatario llamado
   `=HYPERLINK(...)` puede convertirse en una fórmula al abrir el CSV en Excel. La
   neutralización de celdas y la distinción entre texto y números negativos fue una
   corrección de seguridad, no un detalle de formato.
4. **La accesibilidad no termina en el contraste.** El color `--texto-tenue` pasó de
   4.39:1 a 4.92:1 sobre `--surface-2`, pero también se corrigieron una etiqueta sin
   campo asociado, un mapa sin nombre accesible, el borde de los controles y los
   nombres accesibles de las acciones repetidas. Todas son parte del mismo criterio
   WCAG.
5. **Las pruebas de lógica del frontend son baratas y útiles.** Con Vitest se cubrieron
   `distancia.js` y `exportar.js` sin montar componentes ni depender del navegador. La
   deuda pendiente es la capa de interfaz, no la lógica pura.

## ¿Qué estamos haciendo bien?

1. **Verificación con cifras reproducibles.** Cada métrica de esta retrospectiva se
   obtuvo de un comando ejecutado y no de una estimación.
2. **Seguridad por defecto en la exportación.** El CSV se genera en el backend, se
   codifica con BOM para Excel, se neutralizan fórmulas y se reutiliza la autorización
   de la ruta.
3. **Documentación de límites.** El Quality Gate de Sonar, el despliegue en Staging y
   los scripts de extremo a extremo se registran como no ejecutados en lugar de
   presentarse como aprobados.
4. **Correcciones pequeñas y trazables.** Los cambios de accesibilidad y de análisis
   estático se limitaron a los archivos afectados y no alteraron la arquitectura.
5. **El frontend dejó de ser una caja negra.** La suite Vitest existe, se ejecuta con
   `npm run coverage` y dejó un reporte `lcov` listo para Sonar.

## ¿Qué podemos hacer mejor?

### Personas

- **Repartir la responsabilidad del pipeline.** La configuración de CI/CD quedó
  concentrada en el rol de DevOps. Al menos otra persona debe poder explicar los jobs,
  los secretos y el criterio de activación de Staging.
- **Revisar la accesibilidad con una persona ajena al desarrollo.** La revisión manual
  detectó etiquetas y contraste, pero no sustituye una prueba con lector de pantalla.

### Relaciones

- **Acordar el ambiente de Staging al inicio del sprint.** La falta de host y
  credenciales se descubrió al implementar EN-03, no al planificarlo. Ese acuerdo debía
  existir antes de comprometer los 8 Story Points.
- **Fijar el contrato del CSV con quien lo consume.** El archivo se diseñó para Excel y
  Google Sheets; conviene validarlo con el repartidor o con gerencia antes de congelar
  las columnas.

### Procesos

- **Definir "Done" con evidencia operativa, no solo con archivos.** Para EN-03, el
  criterio de éxito debe incluir una URL de Staging respondiendo y una ejecución real
  del pipeline.
- **Agregar pruebas de integración con PostgreSQL al pipeline.** Hoy la cobertura de
  `rutas.py` es 30 % porque las pruebas unitarias no levantan la base de datos, aunque
  el workflow sí tiene un servicio PostgreSQL disponible.
- **No declarar cerrado un sprint con una cobertura global por debajo del objetivo.**
  La brecha debe reflejarse en el acta y en el informe de estado.

### Herramientas

- **Activar Sonar con un proyecto real.** La configuración existe, pero sin token ni
  Quality Gate consultado no se puede afirmar nada sobre vulnerabilidades.
- **Incorporar un escáner de accesibilidad automatizado.** axe o WAVE darían una señal
  repetible; la revisión manual seguiría siendo necesaria para el juicio final.
- **Instalar PostgreSQL en el entorno de verificación.** Los scripts `auditoria_api.py`
  y `smoke_sprint2.py` quedaron sin reejecutar en este sprint por esa ausencia.

### Acciones a realizar

| # | Acción de mejora concreta | Eje | Responsable | Fecha Límite | Criterio de éxito |
|:---:|:---|:---:|:---:|:---:|:---|
| **ACT-S3-01** | Definir el host de Staging y activar `deploy-staging.yml` con `STAGING_DEPLOY_ENABLED=true`, `STAGING_DEPLOY_HOOK` y `STAGING_HEALTH_URL`. | Procesos | Andrew Steven Vega Reyes | 13/11/2026 | El workflow de CI termina en verde, dispara el despliegue y la URL de salud de Staging responde `200`. |
| **ACT-S3-02** | Agregar pruebas de integración con PostgreSQL para rutas y exportación. | Herramientas | Jhanpool Ernesto Flores Torres | 20/11/2026 | `rutas.py` supera el 70 % de cobertura y las pruebas corren en el servicio PostgreSQL del pipeline. |
| **ACT-S3-03** | Elevar la cobertura global del backend de 59.89 % a ≥ 70 %. | Procesos | Jhanpool Ernesto Flores Torres | 27/11/2026 | `coverage report` muestra ≥ 70 % global y el umbral queda configurado en CI. |
| **ACT-S3-04** | Incorporar pruebas de componentes React para los popups de US-006 y la descarga de US-008. | Herramientas | Ricardo David Tucto Ubaldo | 20/11/2026 | `npm run test` cubre `MapView` y la interacción de exportación con Testing Library y jsdom. |
| **ACT-S3-05** | Ejecutar SonarQube/SonarCloud y registrar el Quality Gate real. | Herramientas | Andrew Steven Vega Reyes | 27/11/2026 | El análisis se ejecuta con `SONAR_TOKEN` y el resultado queda enlazado en el repositorio. |
| **ACT-S3-06** | Implementar RN-002 (bloqueo por intentos fallidos) y rate limiting. | Procesos | Jhanpool Ernesto Flores Torres | 27/11/2026 | Tres intentos fallidos bloquean la cuenta 15 minutos y el endpoint de login limita la tasa de peticiones. |
| **ACT-S3-07** | Ejecutar una auditoría de accesibilidad con axe o WAVE y una prueba con lector de pantalla. | Herramientas | Ricardo David Tucto Ubaldo | 27/11/2026 | Se registra el informe, se corrigen los hallazgos críticos y se repite la prueba. |

---

[← Volver al README principal](../../../README.md)
