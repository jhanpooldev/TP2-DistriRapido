import api, { extraerError } from '../api/client'

/**
 * Extrae el nombre del archivo del encabezado Content-Disposition.
 * Se usa cuando el backend decide el nombre; si no viene, se usa el fallback.
 */
export function nombreDesdeContentDisposition(header, fallback = 'resumen-ruta.csv') {
  if (typeof header !== 'string') return fallback

  const conComillas = header.match(/filename\s*=\s*"([^"]+)"/i)
  if (conComillas) return conComillas[1]

  const sinComillas = header.match(/filename\s*=\s*([^;]+)/i)
  if (sinComillas) return sinComillas[1].trim()

  return fallback
}

/** Dispara la descarga de un Blob sin navegar fuera de la aplicacion. */
export function descargarArchivo(contenido, nombre) {
  const blob = contenido instanceof Blob
    ? contenido
    : new Blob([contenido], { type: 'text/csv;charset=utf-8' })

  const url = URL.createObjectURL(blob)
  const enlace = document.createElement('a')
  enlace.href = url
  enlace.download = nombre
  enlace.style.display = 'none'
  document.body.appendChild(enlace)
  enlace.click()
  enlace.remove()
  URL.revokeObjectURL(url)
}

/** US-008: descarga el resumen CSV de una ruta guardada. */
export async function exportarResumenRuta(idRuta) {
  try {
    const respuesta = await api.get(`/rutas/${idRuta}/export`, { responseType: 'blob' })
    const nombre = nombreDesdeContentDisposition(
      respuesta.headers?.['content-disposition'],
      `ruta-${String(idRuta).slice(0, 8)}.csv`
    )
    descargarArchivo(respuesta.data, nombre)
    return nombre
  } catch (error) {
    // El backend devuelve JSON aunque se haya pedido un blob; hay que leerlo
    // para no mostrar un mensaje generico cuando la causa es un 403 o un 404.
    const datos = error?.response?.data
    if (datos instanceof Blob) {
      try {
        const json = JSON.parse(await datos.text())
        if (typeof json.detail === 'string') {
          const nuevoError = new Error(json.detail)
          nuevoError.response = { status: error.response.status, data: json }
          throw nuevoError
        }
      } catch (lectura) {
        if (lectura?.response) throw lectura
      }
    }
    throw new Error(extraerError(error, 'No se pudo exportar el resumen de la ruta'))
  }
}
