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
  envDir: '../../',
})