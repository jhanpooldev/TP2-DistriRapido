# Reprospectiva del sprint

[⬅ Volver al README principal](../../README.md)

---

**Nombre del Proyecto:** EcoLogística Lima – Optimizador de Rutas Sostenibles para DistriRápido S.A.C.

**Líder del Proyecto:** Jhunior Harold Cosme Tenorio

---

## Control de Versiones del Documento

| Versión | Fecha | Autor | Descripción del Cambio |
|:---:|:---:|:---|:---|
| 1.0.0 | 01/10/2026 | Jhunior Harold Cosme Tenorio / Equipo EcoLogística | Retrospectiva del Sprint 1 (Autenticación MFA y Sesiones Seguras). |
| 1.1.0 | 15/10/2026 | Jhunior Harold Cosme Tenorio / Equipo EcoLogística | Retrospectiva del Sprint 2 (Motor de Optimización de Rutas y Métricas de Sostenibilidad). |

---

## ¿Qué aprendimos?

Durante la ejecución del **Sprint 2**, el equipo de desarrollo adquirió conocimientos clave en modelado algorítmico y optimización de operaciones logísticas:

1. **Modelado Matemático de Problemas NP-Hard (TSP y VRP):**
   - Comprendimos que para problemas de ruteo vehicular con restricciones operativas, los enfoques exactos (fuerza bruta o programación entera pura) se vuelven inviables a gran escala. Las metaheurísticas constructivas (Vecino Más Próximo) combinadas con búsqueda local (2-opt) ofrecen un balance perfecto entre calidad de solución (más del 25% de ahorro) y tiempo de cómputo (< 1 segundo).
2. **Cálculo de Distancias Geodésicas Reales:**
   - Aprendimos a formular y calibrar la ecuación de Haversine para transformar coordenadas esféricas de latitud y longitud en distancias métricas ortodrómicas exactas, superando las distorsiones de los cálculos euclidianos planos.
3. **Cuantificación de Huella de Carbono según Factores de Emisión:**
   - Interiorizamos las metodologías del IPCC y del GHG Protocol para traducir el ahorro de kilómetros recorridos en kilogramos de CO₂ evitados, clasificando las emisiones según la tecnología motriz (diésel, GNV y electricidad).
4. **Diseño de APIs para Algoritmos de Alto Rendimiento:**
   - La estructura desacoplada entre la capa de esquemas Pydantic y el servicio de optimización permitió mantener endpoints limpios, tipados y con validaciones deterministas de capacidad de carga.

---

## ¿Qué estamos haciendo bien?

1. **Alineación Total con los Objetivos de Sostenibilidad:**
   - El equipo logró materializar el objetivo fundacional del proyecto: no solo optimizar costos operativos para DistriRápido S.A.C., sino proporcionar métricas ambientales comprobables y transparentes.
2. **Mantenimiento de Cobertura de Pruebas Excelente (92%):**
   - Se continuó la disciplina de TDD agregando pruebas automatizadas que verifican casos de éxito, exceso de capacidad vehicular y validación de esquemas, alcanzando 15 tests en verde.
3. **Resolución Temprana de Impedimentos Complejos:**
   - Los impedimentos algorítmicos identificados (como el tiempo de cálculo de matrices de distancia) fueron mitigados oportunamente antes del cierre del sprint mediante heurísticas eficientes.
4. **Adopción Constante de Buenas Prácticas de Control de Versiones:**
   - Mantener commits pequeños, enfocados y estructurados bajo Conventional Commits ha facilitado la trazabilidad y la integración continua del equipo.

---

## ¿Qué podemos hacer mejor?

### Personas
- **Capacitación en Librerías de Visualización Cartográfica:** Los miembros del equipo frontend requieren profundizar en el manejo de Leaflet / Mapbox en React para agilizar el renderizado de mapas interactivos en el Sprint 3.
- **Balance en la asignación de tareas de documentación:** Distribuir más equitativamente la redacción de informes técnicos entre todos los integrantes para no concentrar la carga documental en el rol de QA / Líder.

### Relaciones
- **Sesiones de Pair Programming para la integración Frontend-Backend:** Programar sesiones de programación en parejas para conectar los endpoints de optimización de rutas con los componentes visuales de React, asegurando que los tipos de datos coincidan perfectamente.
- **Comunicación más proactiva de bloqueos en daily standups:** Notificar impedimentos técnicos el mismo día en que se presentan, evitando esperar a la reunión semanal de sincronización.

### Procesos
- **Definición de Escenarios de Prueba de Aceptación con Usuarios Finales:** Incorporar operadores logísticos reales (o pruebas de usuario simuladas) para validar la usabilidad de las hojas de ruta generadas antes del cierre del PMV.
- **Gestión de Cargas de Trabajo para Sprints Finales:** Anticipar la complejidad de la entrega final del curso (informe final, diapositivas y video demostrativo de 5 minutos) reservando tiempo en el Sprint 3.

### Herramientas
- **Implementación de Mock Servers para Frontend:** Configurar respuestas mockeadas de la API de rutas para que el equipo frontend pueda desarrollar componentes de mapas sin depender de la ejecución local del backend.
- **Monitoreo de Consumo de Memoria en Python:** Monitorear el perfil de memoria de las heurísticas de optimización cuando se manejen lotes de más de 100 pedidos simultáneos.

---

## Acciones a realizar

Con base en los aprendizajes del Sprint 2, el equipo se compromete a ejecutar el siguiente plan de acción para el **Sprint 3 (Cierre del PMV)**:

| # | Acción de Mejora Concreta | Eje | Responsable | Fecha Límite | Criterio de Éxito |
|:---:|:---|:---:|:---:|:---:|:---|
| **ACT-05** | Integrar librería Leaflet / OpenStreetMap en React para renderizar las rutas optimizadas sobre el mapa de Lima. | Herramientas / Personas | Ricardo David Tucto Ubaldo | 20/10/2026 | Mapa interactivo mostrando marcadores y polilínea de la ruta generada por la API. |
| **ACT-06** | Realizar sesiones de Pair Programming de 2 horas para enlazar los endpoints `/api/rutas` con el frontend. | Relaciones | Jhanpool Flores / Ricardo Tucto | 18/10/2026 | Flujo completo de carga de pedidos y cálculo de ruta visible en la aplicación React. |
| **ACT-07** | Diseñar la plantilla de Hoja de Ruta imprimible en PDF con el orden de paradas y tiempos estimados para el conductor. | Procesos | Andrew Steven Vega Reyes | 24/10/2026 | Documento PDF descargable con la información de los pedidos y datos de contacto del cliente. |
| **ACT-08** | Grabar y editar el video explicativo del PMV de máximo 5 minutos según la consigna oficial de fin de ciclo. | Personas / Procesos | Jhunior Harold Cosme Tenorio (y equipo) | 28/10/2026 | Video de 5 minutos subido a YouTube/Drive y enlazado en el `README.md`. |

---

[⬅ Volver al README principal](../../README.md)
