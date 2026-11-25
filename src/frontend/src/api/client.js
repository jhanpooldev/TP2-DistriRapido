import axios from 'axios'

const PREFIJO_API = '/api/v1'

/** Normaliza VITE_API_URL para que siempre apunte al prefijo real de FastAPI. */
export function normalizarUrlBase(valor) {
  const base = String(valor ?? '').trim()
  if (!base) return PREFIJO_API

  const sinBarraFinal = base.replace(/\/+$/, '')
  if (sinBarraFinal.endsWith(PREFIJO_API)) return sinBarraFinal
  if (sinBarraFinal.endsWith('/api')) return `${sinBarraFinal}/v1`
  return `${sinBarraFinal}${PREFIJO_API}`
}

const BASE_URL = normalizarUrlBase(import.meta.env.VITE_API_URL)

export const API_BASE_URL = BASE_URL

const api = axios.create({ baseURL: BASE_URL, timeout: 30000 })

// Cache TTL en memoria para GET. Evita repetir la misma consulta al cambiar
// de pestaña o al re-renderizar, y se invalida en cuanto hay una mutacion.
const CACHE_TTL_MS = 60_000
const CACHE_MAX_ENTRADAS = 50
const cache = new Map()
const enVuelo = new Map()

function claveDeCache(config) {
  const token = config.headers?.Authorization || ''
  const params = config.params ? JSON.stringify(config.params) : ''
  return `${token}|${config.url}|${params}`
}

function guardarEnCache(clave, respuesta) {
  if (cache.size >= CACHE_MAX_ENTRADAS) {
    cache.delete(cache.keys().next().value)
  }
  cache.set(clave, { expira: Date.now() + CACHE_TTL_MS, respuesta })
}

/** Limpia la cache local. Se exporta para pruebas y para cierres de sesion. */
export function limpiarCache() {
  cache.clear()
  enVuelo.clear()
}

const adaptadorOriginal = typeof api.defaults.adapter === 'function'
  ? api.defaults.adapter
  : axios.getAdapter(api.defaults.adapter)

// Se envuelve el adaptador para poder servir una respuesta cacheada o
// reutilizar una peticion identica que ya esta en curso (deduplicacion).
api.defaults.adapter = async (config) => {
  const esGet = (config.method || 'get').toLowerCase() === 'get'
  const cacheable = esGet && config.cache !== false && config.responseType !== 'blob'

  if (!cacheable) return adaptadorOriginal(config)

  const clave = claveDeCache(config)
  const entrada = cache.get(clave)
  if (entrada && entrada.expira > Date.now()) {
    return { ...entrada.respuesta, config }
  }
  if (entrada) cache.delete(clave)

  if (enVuelo.has(clave)) return enVuelo.get(clave)

  const peticion = adaptadorOriginal(config)
    .then((respuesta) => {
      guardarEnCache(clave, respuesta)
      return respuesta
    })
    .finally(() => enVuelo.delete(clave))

  enVuelo.set(clave, peticion)
  return peticion
}

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
  (respuesta) => {
    const metodo = (respuesta.config?.method || 'get').toLowerCase()
    // Cualquier escritura invalida la cache: la siguiente lectura debe ver el
    // cambio recien guardado, no una copia de hasta 60 segundos atras.
    if (metodo !== 'get') limpiarCache()
    return respuesta
  },
  (error) => {
    if (error?.response?.status === 401) {
      // Un 401 en cualquier petición autenticada invalida la sesión en todo el
      // panel, no solo en la pestaña que hizo la llamada. Login y /me gestionan
      // sus propios mensajes, por lo que no emiten el evento aquí.
      limpiarCache()
      localStorage.removeItem('token')
      const url = error.config?.url || ''
      const esValidacion =
        url.includes('/auth/login') || url.includes('/auth/me') || url.includes('/auth/logout')
      if (!esValidacion && typeof window !== 'undefined' && window.CustomEvent) {
        window.dispatchEvent(
          new window.CustomEvent('auth:expired', {
            detail: 'Su sesión expiró. Vuelva a iniciar sesión.',
          })
        )
      }
    }
    return Promise.reject(error)
  }
)

export function extraerError(error, porDefecto = 'Ocurrio un error inesperado') {
  const detail = error?.response?.data?.detail
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail) && detail.length > 0) {
    return detail.map(d => d.msg || String(d)).join(' | ')
  }

  // Sin respuesta del servidor: casi siempre el backend esta apagado.
  if (error?.response === undefined) {
    const mensaje = error?.message || ''
    if (error?.code === 'ECONNABORTED' || /timeout/i.test(mensaje)) {
      return 'El servidor tardo demasiado en responder. Intenta de nuevo.'
    }
    return 'No se pudo conectar con el servidor. Verifica que el backend este corriendo en el puerto 8000.'
  }

  return `Error ${error.response.status}: ${porDefecto}`
}

export default api
