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
| 1.0.0 | 26/10/2026 | Jhunior Harold Cosme Tenorio / Equipo EcoLogística | Retrospectiva del Sprint 3. |
| 1.1.0 | 26/10/2026 | Jhunior Harold Cosme Tenorio / Equipo EcoLogística | Se agregan aprendizajes del trazado por calles y del análisis real de SonarQube. |

---

## ¿Qué aprendimos?

1. **Un pipeline de CI no equivale a un pipeline de CD.** El workflow de integración
   continua puede ejecutar pruebas, cobertura y build, pero EN-03 exige además que la
   versión quede accesible en Staging. Sin un host y sus credenciales, el criterio no se
   cumple. Llamar "terminado" al enabler por tener el archivo YAML habría sido una
   afirmación falsa.
2. **La cobertura global puede ocultar brechas por módulo, y también puede inflarse.**
   El backend está en 60.82 % global, pero `exportacion.py` tiene 100 % y el optimizador
   90 %. En cambio, SonarQube reporta 9.8 % global porque incluye todos los componentes
   React sin pruebas. Aprender a leer las dos cifras —y explicar por qué difieren— es
   más útil que perseguir un único número.
3. **La exportación también es una superficie de ataque.** Un destinatario llamado
   `=HYPERLINK(...)` puede convertirse en una fórmula al abrir el CSV en Excel. La
   neutralización de celdas y la distinción entre texto y números negativos fue una
   corrección de seguridad, no un detalle de formato.
4. **La accesibilidad no termina en el contraste.** El color `--texto-tenue` pasó de
   4.39:1 a 4.92:1 sobre `--surface-2`, pero también se corrigieron una etiqueta sin
   campo asociado, un mapa sin nombre accesible, el borde de los controles y los
   nombres accesibles de las acciones repetidas. Todas son parte del mismo criterio
   WCAG.
5. **Un mapa que "parece Google Maps" exige separar lo visual de lo métrico.** Al
   dibujar la ruta por calles con OSRM, la distancia dibujada (31.0 km) no coincide con
   la planificada por haversine (24.206 km). Mezclar ambas cifras habría producido un
   reporte engañoso; se decidió mostrar la distancia del trazado aparte y aclarar que los
   indicadores del resumen siguen siendo geodésicos.
6. **Un servicio externo sin SLA no puede ser un requisito bloqueante.** OSRM público
   respondió correctamente en la verificación, pero no garantiza disponibilidad. El
   respaldo a línea discontinua y el aviso en pantalla son parte del diseño, no un
   parche.
7. **SonarQube encontró defectos que la suite de pruebas no veía.** Las cuatro promesas
   sin manejo de rechazo en `Dashboard.jsx` y `MapView.jsx` no rompían las pruebas, pero
   podían dejar la interfaz en estado "cargando" ante un fallo inesperado. La regla
   `S9383` obligó a hacer explícito el manejo.

## ¿Qué estamos haciendo bien?

1. **Verificación con cifras reproducibles.** Cada métrica de esta retrospectiva se
   obtuvo de un comando ejecutado y no de una estimación; las evidencias de SonarQube
   quedaron guardadas en `docs/05 Evidencias/sonar-sprint3/`.
2. **Seguridad por defecto en la exportación.** El CSV se genera en el backend, se
   codifica con BOM para Excel, se neutralizan fórmulas y se reutiliza la autorización
   de la ruta.
3. **Documentación de límites.** El Quality Gate de Sonar, el despliegue en Staging y
   los scripts de extremo a extremo se registran con su estado real. Cuando se pudo
   ejecutar la auditoría de API y el smoke test, se ejecutaron y se reportaron.
4. **Remediación trazable de hallazgos estáticos.** Los 7 hallazgos iniciales de
   SonarQube se corrigieron en el código y se volvió a analizar: 0 bugs, 0 code smells,
   0 hotspots y deuda técnica de 0 minutos.
5. **El frontend dejó de ser una caja negra.** La suite Vitest existe, se ejecuta con
   `npm run coverage` y dejó un reporte `lcov` que SonarQube consume.

## ¿Qué podemos hacer mejor?

### Personas

- **Repartir la responsabilidad del pipeline.** La configuración de CI/CD quedó
  concentrada en el rol de DevOps. Al menos otra persona debe poder explicar los jobs,
  los secretos y el criterio de activación de Staging.
- **Revisar la accesibilidad con una persona ajena al desarrollo.** La revisión manual
  detectó etiquetas y contraste, pero no sustituye una prueba con lector de pantalla.
- **Asignar un revisor formal por Pull Request.** El DoD exige revisión de otra persona
  y hoy no hay evidencia de ese paso en el repositorio.

### Relaciones

- **Acordar el ambiente de Staging al inicio del sprint.** La falta de host y
  credenciales se descubrió al implementar EN-03, no al planificarlo. Ese acuerdo debía
  existir antes de comprometer los 8 Story Points.
- **Fijar el contrato del CSV con quien lo consume.** El archivo se diseñó para Excel y
  Google Sheets; conviene validarlo con el repartidor o con gerencia antes de congelar
  las columnas.
- **Acordar con el negocio el alcance del mapa.** El trazado por calles se pidió durante
  el sprint y se implementó como mejora visual; debió entrar al backlog para no competir
  con las historias comprometidas.

### Procesos

- **Definir "Done" con evidencia operativa, no solo con archivos.** Para EN-03, el
  criterio de éxito debe incluir una URL de Staging respondiendo y una ejecución real
  del pipeline.
- **Agregar pruebas de integración con PostgreSQL al pipeline.** Hoy la cobertura de
  `rutas.py` es 30 % porque las pruebas unitarias no levantan la base de datos, aunque
  el workflow sí tiene un servicio PostgreSQL disponible.
- **No declarar cerrado un sprint con una cobertura global por debajo del objetivo.**
  La brecha debe reflejarse en el acta y en el informe de estado.
- **Separar la verificación funcional de la aceptación del cliente.** La demostración
  reproducible no reemplaza un acta firmada por los stakeholders.

### Herramientas

- **Mantener SonarQube en el flujo local.** Ya se ejecutó con Docker y produjo métricas
  reales; el siguiente paso es automatizarlo en CI con `SONAR_TOKEN` para que no dependa
  de una corrida manual.
- **Incorporar un escáner de accesibilidad automatizado.** axe o WAVE darían una señal
  repetible; la revisión manual seguiría siendo necesaria para el juicio final.
- **Instalar `pip-audit` en el entorno de verificación.** `npm audit` cubre el frontend,
  pero el backend no tiene un SCA de dependencias Python.
- **Evaluar una instancia propia de OSRM.** El servidor público es adecuado para el PMV,
  pero no para producción.

### Acciones a realizar

| # | Acción de mejora concreta | Eje | Responsable | Fecha Límite | Criterio de éxito |
|:---:|:---|:---:|:---:|:---:|:---|
| **ACT-S3-01** | Definir el host de Staging y activar `deploy-staging.yml` con `STAGING_DEPLOY_ENABLED=true`, `STAGING_DEPLOY_HOOK` y `STAGING_HEALTH_URL`. | Procesos | Andrew Steven Vega Reyes | 13/11/2026 | El workflow de CI termina en verde, dispara el despliegue y la URL de salud de Staging responde `200`. |
| **ACT-S3-02** | Agregar pruebas de integración con PostgreSQL para rutas y exportación. | Herramientas | Jhanpool Ernesto Flores Torres | 20/11/2026 | `rutas.py` supera el 70 % de cobertura y las pruebas corren en el servicio PostgreSQL del pipeline. |
| **ACT-S3-03** | Elevar la cobertura global del backend de 60.82 % a ≥ 70 %. | Procesos | Jhanpool Ernesto Flores Torres | 27/11/2026 | `coverage report` muestra ≥ 70 % global y el umbral queda configurado en CI. |
| **ACT-S3-04** | Incorporar pruebas de componentes React para los popups de US-006, el trazado por calles y la descarga de US-008. | Herramientas | Ricardo David Tucto Ubaldo | 20/11/2026 | `npm run test` cubre `MapView` y la interacción de exportación con Testing Library y jsdom. |
| **ACT-S3-05** | ~~Ejecutar SonarQube/SonarCloud y registrar el Quality Gate real.~~ **Completada el 26/10/2026** con SonarQube Community en Docker. | Herramientas | Andrew Steven Vega Reyes | 26/10/2026 | Quality Gate `OK`, 0 bugs, 0 vulnerabilidades, 0 hotspots y evidencias JSON en `docs/05 Evidencias/sonar-sprint3/`. |
| **ACT-S3-06** | Implementar RN-002 (bloqueo por intentos fallidos) y rate limiting. | Procesos | Jhanpool Ernesto Flores Torres | 27/11/2026 | Tres intentos fallidos bloquean la cuenta 15 minutos y el endpoint de login limita la tasa de peticiones. |
| **ACT-S3-07** | Ejecutar una auditoría de accesibilidad con axe o WAVE y una prueba con lector de pantalla. | Herramientas | Ricardo David Tucto Ubaldo | 27/11/2026 | Se registra el informe, se corrigen los hallazgos críticos y se repite la prueba. |
| **ACT-S3-08** | Automatizar SonarQube en el pipeline de GitHub con `SONAR_TOKEN` y `SONAR_ENABLED=true`. | Herramientas | Andrew Steven Vega Reyes | 27/11/2026 | Cada Pull Request publica el Quality Gate y falla si aparecen bugs o vulnerabilidades nuevas. |
| **ACT-S3-09** | Evaluar el despliegue de una instancia propia de OSRM o un proveedor de ruteo con SLA. | Herramientas | Jhunior Harold Cosme Tenorio | 04/12/2026 | El mapa usa una instancia con SLA y se documenta su disponibilidad y límite de peticiones. |
| **ACT-S3-10** | Instalar `pip-audit` y agregar la auditoría de dependencias Python al pipeline. | Herramientas | Jhanpool Ernesto Flores Torres | 04/12/2026 | `pip-audit` se ejecuta sin vulnerabilidades altas o críticas y el resultado queda en el reporte de CI. |

---

[← Volver al README principal](../../../README.md)
