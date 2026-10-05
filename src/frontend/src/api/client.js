import axios from 'axios'

const api = axios.create({ baseURL: '/api/v1', timeout: 30000 })

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
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