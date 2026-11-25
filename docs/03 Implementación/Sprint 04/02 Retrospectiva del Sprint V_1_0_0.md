# Retrospectiva del sprint

[← Volver al README principal](../../../README.md)

---

**Nombre del Proyecto:** EcoLogística Lima – Optimizador de Rutas Sostenibles para DistriRápido S.A.C.

**Líder del Proyecto:** Jhunior Harold Cosme Tenorio

**Sprint:** 4

**Periodo:** 09/11/2026 – 17/11/2026

**Fecha de verificación local:** 17/11/2026

---

## Control de Versiones del Documento

| Versión | Fecha | Autor | Descripción del Cambio |
|:---:|:---:|:---|:---|
| 1.0.0 | 17/11/2026 | Jhunior Harold Cosme Tenorio / Equipo EcoLogística | Retrospectiva del Sprint 4 con los aprendizajes de la suite E2E, las métricas y la preparación del SUS. |

---

## ¿Qué aprendimos?

1. **Una prueba E2E vale por lo que verifica, no por la herramienta que usa.** Tener
   Playwright instalado no demuestra nada; lo que aporta valor es que la suite recorra
   el login, registre pedidos, calcule una ruta, la exporte y compruebe los códigos
   HTTP reales. La corrida del 17/11/2026 dejó **79 pruebas aprobadas y 2 omitidas**
   sobre 81 ejecuciones, con **0 fallidas**.

2. **Los datos de prueba deben ser únicos y limpiarse por API.** La suite comparte una
   sola base PostgreSQL. Si un caso deja un pedido o una ruta, el siguiente puede
   encontrar resultados inesperados. Los ayudantes de `e2e/utils.js` crean datos con
   identificadores únicos y los eliminan en `finally`, incluso cuando la aserción falla.

3. **Las aserciones deben leer la interfaz real, no lo que el equipo recuerda.** Tres
   pruebas fallaron en la primera corrida por suponer textos que no existían: el nombre
   del operador era `Operador Demo` en la base local y no `Operador Principal` (el
   sembrado actual de `main.py` usa `Operador Principal`); el CSV exportado usa la
   columna `Orden,Destinatario`; y el mensaje de filtro vacío vive en un `p.vacio`
   concreto. Corregir la aserción —sin debilitarla— fue más honesto que cambiar la
   aplicación para que coincidiera con el test.

4. **Un test de resiliencia no es solo un `expect(status).toBe(400)`.** También importa
   que la interfaz informe del fallo. Los casos que abortan la petición o simulan un
   `500` comprueban que el panel muestra el aviso y no se queda en blanco. Eso conecta
   la prueba técnica con la experiencia del operador.

5. **Medir rendimiento con la Performance API exige calentamiento.** La primera carga
   contra Vite compila dependencias y produce cifras infladas. Se hace una primera
   navegación, se recarga y se mide la segunda. Aun así, los valores son locales y no
   sustituyen una medición de producción.

6. **El SUS no se puede simular.** Un cuestionario de usabilidad sin participantes
   reales no produce un puntaje válido. Se preparó el instrumento completo —diez ítems,
   escala, fórmula y protocolo— y se dejó constancia de que **no se aplicó**. Inventar
   respuestas habría convertido un entregable incompleto en una afirmación falsa.

7. **Un workflow sin ejecución es una hipótesis, no una evidencia.** Los workflows
   se validaron primero con `yaml.safe_load`; el 19/11/2026 se ejecutaron en GitHub sobre
   el commit `85eac48` y Tests, CI, CodeQL y Green Audit terminaron en verde. La lección
   se mantiene: hasta que corrieron, eran una hipótesis, no un pipeline probado.

## ¿Qué estamos haciendo bien?

1. **Verificación con cifras reproducibles.** Cada número de la revisión proviene de un
   comando ejecutado: 66 pruebas de backend, 24 de frontend, 79 E2E aprobadas y tiempos
   de API medidos en los tres navegadores. Los JSON crudos quedaron en
   `docs/Evidencias/playwright-sprint4/`.

2. **Cobertura de flujos, no solo de pantallas.** La suite no se limita al login:
   registra pedidos, arma y guarda rutas, exporta el CSV, edita, elimina y verifica el
   mapa y el impacto ambiental. También cubre el rol Administrador frente al Operador.

3. **Honestidad sobre lo pendiente.** El SUS y el despliegue a Producción se declaran
   como no completados. No se presentan como logros por el hecho de tener archivos o
   plantillas. La ejecución en GitHub sí quedó acreditada el 19/11/2026.

4. **Limpieza del repositorio.** Los reportes de Playwright (`playwright-report/`,
   `test-results/`, `blob-report/`) quedaron fuera de Git. Solo se versionan las
   evidencias seleccionadas, no los artefactos completos.

5. **Separación de responsabilidades en CI.** `ci.yml` valida dependencias y
   compilación; `tests.yml` ejecuta pytest, Vitest y Playwright; `deploy-production.yml`
   despliega solo con activación explícita. Cada workflow tiene un propósito claro.

6. **Documentación enlazada.** Los cuatro entregables del sprint y el índice de
   evidencias se conectan con el README principal, sin rutas rotas.

## ¿Qué podemos hacer mejor?

### Personas

- **Aplicar el SUS con personas reales.** El instrumento está listo, pero necesita al
  menos cinco participantes representativos del rol Operador. Sin ellos no hay dato de
  usabilidad que defender.
- **Repartir el conocimiento de Playwright.** Hoy la suite la mantiene una sola persona.
  Otra integrante debe poder agregar un caso y explicar los ayudantes de `e2e/utils.js`.
- **Revisar los flujos con quien opera el sistema.** Las pruebas reflejan lo que el
  equipo cree que hace el operador; conviene validarlas con alguien que use el panel a
  diario.

### Relaciones

- **Acordar el proveedor de Producción antes de escribir el workflow.** El despliegue
  quedó preparado, pero sin host, URL ni secretos. Esa decisión debía tomarse al inicio
  del sprint, no al final.
- **Definir con gerencia qué métricas de rendimiento importan.** TTFB, FCP y LCP son
  útiles, pero el negocio también necesita saber cuánto tarda una ruta completa en
  condiciones reales de red.
- **Coordinar con el responsable de QA la evidencia visual.** Lighthouse CI está
  configurado en `green-audit.yml`, pero no se generó la carpeta `.lighthouseci/` en
  local. Hay que acordar si la evidencia visual es obligatoria y cómo se conserva.

### Procesos

- **Ejecutar los workflows en GitHub y adjuntar la corrida.** La validación de sintaxis
  no reemplaza una ejecución real. La corrida se hizo el 19/11/2026 sobre `85eac48` y
  quedó enlazada en la revisión; falta completar el despliegue a Staging/Producción.
- **Convertir la suite E2E en un gate obligatorio.** Hoy `tests.yml` la ejecuta, pero
  no se ha verificado que un Pull Request no pueda fusionarse con E2E en rojo.
- **Fijar un umbral de cobertura y sostenerlo.** El backend está en 61 % y el objetivo
  es 70 %. Sin un umbral en CI, la brecha se arrastra de sprint en sprint.
- **Documentar los datos de prueba.** La suite crea pedidos y rutas reales; conviene
  registrar qué deja y cómo se limpia para que otra persona pueda reproducirla.

### Herramientas

- **Agregar pruebas de componentes React.** La suite E2E no reemplaza pruebas unitarias
  de `MapView`, `RutasTab` o `ImpactoTab`.
- **Evaluar `@axe-core/playwright`.** Permitiría una señal automática de accesibilidad
  dentro de la misma suite, complementando la revisión manual del Sprint 3.
- **Considerar un entorno dedicado para E2E.** La base compartida y la ejecución en
  serie limitan la velocidad; un contenedor efímero por corrida sería más limpio.
- **Conservar el reporte HTML como artefacto enlazado.** Se publica en CI y la corrida
  `44560349236` lo dejó como artefacto `playwright-report`; conviene enlazarlo desde la
  documentación cuando la URL sea estable.

### Acciones a realizar

| # | Acción de mejora concreta | Eje | Responsable | Fecha límite | Criterio de éxito |
|:---:|:---|:---:|:---:|:---:|:---|
| **ACT-S4-01** | Aplicar el cuestionario SUS a al menos cinco participantes del rol Operador y registrar los puntajes reales. | Personas | Ricardo David Tucto Ubaldo | 01/12/2026 | El documento `04 Usabilidad` contiene participantes, respuestas y puntaje SUS calculado con la fórmula estándar. |
| **ACT-S4-02** | Ejecutar `ci.yml`, `tests.yml` y `deploy-production.yml` en GitHub con un `push` autorizado y enlazar las corridas. | Procesos | Andrew Steven Vega Reyes | 24/11/2026 | Cada workflow tiene una corrida visible; se registra el resultado real, sea verde o rojo. |
| **ACT-S4-03** | Definir proveedor, URL y secretos de Producción y activar `PRODUCTION_DEPLOY_ENABLED=true`. | Relaciones | Jhunior Harold Cosme Tenorio | 01/12/2026 | El workflow despliega y `PRODUCTION_HEALTH_URL` responde `200`; la URL queda documentada. |
| **ACT-S4-04** | Agregar pruebas de componentes React para `MapView`, `RutasTab` e `ImpactoTab`. | Herramientas | Ricardo David Tucto Ubaldo | 01/12/2026 | `npm run test` cubre componentes con Testing Library y jsdom, además de `src/logica/**`. |
| **ACT-S4-05** | Elevar la cobertura global del backend de 61 % a ≥ 70 % y fijar el umbral en CI. | Procesos | Jhanpool Ernesto Flores Torres | 08/12/2026 | `coverage report` muestra ≥ 70 % y `tests.yml` falla si baja del umbral. |
| **ACT-S4-06** | Incorporar `@axe-core/playwright` y reportar hallazgos de accesibilidad en la suite E2E. | Herramientas | Andrew Steven Vega Reyes | 08/12/2026 | La suite ejecuta una verificación automática y el informe queda como artefacto. |
| **ACT-S4-07** | Generar y conservar la evidencia visual de Lighthouse CI (`.lighthouseci/`) o documentar su exclusión. | Herramientas | Andrew Steven Vega Reyes | 24/11/2026 | Existe la carpeta con los reportes o una nota firmada que justifica no conservarla. |
| **ACT-S4-08** | Documentar el ciclo de vida de los datos de prueba de la suite E2E. | Procesos | Jhanpool Ernesto Flores Torres | 24/11/2026 | `e2e/utils.js` y la revisión explican qué se crea, qué se limpia y cómo verificarlo. |

> **Estado al 19/11/2026:** ACT-S4-02 se cumplió parcialmente. `ci.yml`, `tests.yml`,
> `codeql.yml` y `green-audit.yml` corrieron en verde sobre `85eac48`; `deploy-staging.yml`
> y `deploy-production.yml` quedaron omitidos. Las demás acciones siguen abiertas.

---

[← Volver al README principal](../../../README.md)
