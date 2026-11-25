[← Volver al README principal](../../../README.md)

# Evidencias de Playwright — Sprint 4

Resultados reales de la suite de extremo a extremo ejecutada el **17/11/2026** sobre
Chromium, Firefox y WebKit.

## Resumen de la corrida

| Indicador | Valor |
|---|---:|
| Ejecuciones | 81 |
| Aprobadas | **79** |
| Omitidas | **2** |
| Fallidas | **0** |
| Inestables | **0** |
| Duración | 105,1 s |

La omisión corresponde al caso de capturas visuales en Firefox y WebKit; se ejecuta solo
en Chromium.

## Archivos

| Archivo | Contenido |
|---|---|
| [`resultados.json`](resultados.json) | Reporte JSON completo de Playwright (configuración, suites, casos y estadísticas). |
| [`performance-chromium.json`](performance-chromium.json) | TTFB, FCP, LCP y tiempos de API en Chromium. |
| [`performance-firefox.json`](performance-firefox.json) | TTFB, FCP, LCP y tiempos de API en Firefox. |
| [`performance-webkit.json`](performance-webkit.json) | TTFB, FCP, LCP y tiempos de API en WebKit. |
| [`01-login.png`](01-login.png) | Pantalla de acceso. |
| [`02-panel-pedidos.png`](02-panel-pedidos.png) | Panel con la tabla de pedidos. |
| [`03-panel-rutas.png`](03-panel-rutas.png) | Pestaña de rutas guardadas. |
| [`04-panel-mapa.png`](04-panel-mapa.png) | Mapa con la ruta y el detalle de paradas. |
| [`05-panel-impacto.png`](05-panel-impacto.png) | Comparación de emisiones. |
| [`06-panel-vehiculos-operador.png`](06-panel-vehiculos-operador.png) | Flota vista por el Operador. |
| [`07-panel-vehiculos-administrador.png`](07-panel-vehiculos-administrador.png) | Alta de vehículos vista por el Administrador. |

## Métricas de rendimiento

| Métrica | Chromium | Firefox | WebKit |
|---|---:|---:|---:|
| Login — TTFB | 4 ms | 7 ms | 3 ms |
| Login — FCP | 124 ms | 125 ms | 156 ms |
| Login — LCP | 124 ms | 125 ms | 156 ms |
| Panel — TTFB | 12 ms | 5 ms | 3 ms |
| Panel — FCP | 252 ms | 219 ms | 203 ms |
| Panel — LCP | 744 ms | 708 ms | 664 ms |

| Endpoint | Chromium | Firefox | WebKit |
|---|---:|---:|---:|
| `GET /health` | 7 ms | 7 ms | 5 ms |
| `POST /auth/login` | 213 ms | 229 ms | 216 ms |
| `GET /puntos-entrega` | 11 ms | 9 ms | 11 ms |
| `GET /rutas` | 13 ms | 13 ms | 12 ms |
| `GET /vehiculos` | 7 ms | 7 ms | 7 ms |

## Reproducción

```bash
cd src/frontend
npm ci
npx playwright install chromium firefox webkit
npm run test:e2e
```

El reporte HTML completo (`playwright-report/`) no se versiona; se regenera en cada
corrida y el workflow `tests.yml` lo publica como artefacto.

## Documentación relacionada

- [Revisión del Sprint 4](../../03%20Implementación/Sprint%2004/01%20Revisión%20del%20Sprint%20V_1_0_0.md)
- [Análisis de Playwright](../../03%20Implementación/Sprint%2004/03%20Analisis%20PlayWrigth%20V_1_0_0.md)
- [Retrospectiva del Sprint 4](../../03%20Implementación/Sprint%2004/02%20Retrospectiva%20del%20Sprint%20V_1_0_0.md)
- [Usabilidad SUS](../../03%20Implementación/Sprint%2004/04%20Usabilidad%20V_1_0_0.md)

---

[← Volver al README principal](../../../README.md)
