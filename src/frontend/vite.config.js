import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Puerto fijo del backend. Se evita leer una variable de entorno porque un
// API_PORT heredado en la terminal hacia el proxy a un puerto equivocado y
// solo se manifestaba como "ECONNREFUSED" en el login.
const API_PORT = 8000

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: { '/api': `http://127.0.0.1:${API_PORT}` },
  },
  // Lighthouse CI sirve el build con `vite preview`; el proxy mantiene las
  // llamadas /api en el mismo origen para que el login funcione igual.
  preview: {
    port: 4173,
    proxy: { '/api': `http://127.0.0.1:${API_PORT}` },
  },
  build: {
    // Separa Leaflet y React del codigo de la aplicacion: los chunks
    // comparten cache entre despliegues y el inicial queda mas pequeno.
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('node_modules/react') || id.includes('node_modules/react-dom')) {
            return 'react'
          }
          if (id.includes('node_modules/leaflet')) return 'leaflet'
          return undefined
        },
      },
    },
  },
  envDir: '../../',
})