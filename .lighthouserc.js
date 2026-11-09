/**
 * Configuracion de Lighthouse CI para el frontend publico.
 *
 * El workflow `green-audit.yml` ejecuta `lhci autorun` desde `src/frontend`,
 * por lo que `startServerCommand` sirve el build de produccion con
 * `vite preview` en el mismo origen que usa la aplicacion.
 *
 * Se audita la pantalla de login porque es la unica ruta publica que no
 * requiere credenciales ni base de datos. El panel autenticado se documenta
 * como limite en el informe ambiental.
 */
module.exports = {
  ci: {
    collect: {
      url: ['http://127.0.0.1:4173/'],
      startServerCommand:
        'npm run preview -- --host 127.0.0.1 --port 4173 --strictPort',
      // Vite imprime "Local" con codigos ANSI alrededor del texto; se busca
      // solo la palabra para no depender de los escapes de color.
      startServerReadyPattern: 'Local',
      startServerReadyTimeout: 60000,
      numberOfRuns: 3,
      settings: {
        // Emulacion movil por defecto de Lighthouse: es el escenario mas
        // exigente en red y CPU y el que mejor representa el consumo real.
        chromeFlags: '--no-sandbox',
        skipAudits: ['uses-http2'],
      },
    },
    assert: {
      assertions: {
        'categories:performance': ['error', { minScore: 0.9 }],
        'categories:accessibility': ['error', { minScore: 0.9 }],
        'categories:best-practices': ['error', { minScore: 0.9 }],
        'categories:seo': ['error', { minScore: 0.9 }],
        // El objetivo Green IT es reducir bytes y peticiones, no solo la nota.
        'resource-summary:script:size': ['warn', { maxNumericValue: 260000 }],
        'resource-summary:total:size': ['warn', { maxNumericValue: 500000 }],
      },
    },
    upload: {
      target: 'filesystem',
      outputDir: './.lighthouseci',
    },
  },
}
