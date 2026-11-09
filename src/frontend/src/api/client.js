import axios from 'axios'

const api = axios.create({ baseURL: '/api/v1', timeout: 30000 })

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

api.interceptors.response.use((respuesta) => {
  const metodo = (respuesta.config?.method || 'get').toLowerCase()
  // Cualquier escritura invalida la cache: la siguiente lectura debe ver el
  // cambio recien guardado, no una copia de hasta 60 segundos atras.
  if (metodo !== 'get') limpiarCache()
  return respuesta
})

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
