// Trazado de la ruta por calles usando OSRM (Open Source Routing Machine).
//
// Solo se usa para dibujar el recorrido en el mapa. La optimizacion y los
// kilometros del resumen siguen calculandose en el backend con la formula
// geodesica (haversine), por lo que aqui no se altera ningun indicador.
//
// El servidor publico de OSRM es gratuito y no requiere clave, pero es un
// servicio de demostracion: si no responde, el mapa cae a una linea recta
// aproximada en lugar de romperse.

const OSRM_BASE = String(
  import.meta.env?.VITE_OSRM_URL || 'https://router.project-osrm.org'
).replace(/\/+$/, '')

const PERFIL = 'driving'
const TIEMPO_MAXIMO_MS = 8000
const MAX_CACHE = 25

const cache = new Map()

function claveDeRuta(coordenadas) {
  return coordenadas
    .map(([lat, lng]) => `${Number(lat).toFixed(5)},${Number(lng).toFixed(5)}`)
    .join(';')
}

/** OSRM recibe longitud,latitud (no latitud,longitud). */
export function construirUrlTrazado(coordenadas) {
  const waypoints = coordenadas
    .map(([lat, lng]) => `${Number(lng)},${Number(lat)}`)
    .join(';')
  const params = new URLSearchParams({
    overview: 'full',
    geometries: 'geojson',
    steps: 'false',
  })
  return `${OSRM_BASE}/route/v1/${PERFIL}/${waypoints}?${params.toString()}`
}

/** Convierte la geometria GeoJSON de OSRM ([lng, lat]) a [lat, lng] de Leaflet. */
export function normalizarTrazado(payload) {
  if (payload?.code !== 'Ok') return null

  const ruta = payload.routes?.[0]
  const coordenadas = ruta?.geometry?.coordinates

  if (!Array.isArray(coordenadas) || coordenadas.length < 2) return null

  return {
    trazado: coordenadas.map(([lng, lat]) => [Number(lat), Number(lng)]),
    distanciaKm: Number(ruta.distance) / 1000,
  }
}

export async function obtenerTrazadoCalles(
  coordenadas,
  { signal, fetchImpl = globalThis.fetch } = {}
) {
  if (!Array.isArray(coordenadas) || coordenadas.length < 2) return null
  if (typeof fetchImpl !== 'function') return null

  const clave = claveDeRuta(coordenadas)
  if (cache.has(clave)) return cache.get(clave)

  const controlador = new AbortController()
  const abortar = () => controlador.abort()

  if (signal) {
    if (signal.aborted) return null
    signal.addEventListener('abort', abortar, { once: true })
  }

  const temporizador = setTimeout(() => controlador.abort(), TIEMPO_MAXIMO_MS)

  try {
    const respuesta = await fetchImpl(construirUrlTrazado(coordenadas), {
      signal: controlador.signal,
    })

    if (!respuesta?.ok) return null

    const resultado = normalizarTrazado(await respuesta.json())
    if (!resultado) return null

    if (cache.size >= MAX_CACHE) {
      cache.delete(cache.keys().next().value)
    }
    cache.set(clave, resultado)

    return resultado
  } catch {
    // Sin red, timeout o respuesta invalida: el mapa usa el trazado recto.
    return null
  } finally {
    clearTimeout(temporizador)
    signal?.removeEventListener('abort', abortar)
  }
}

/** Utilidad de pruebas para no arrastrar resultados entre casos. */
export function limpiarCacheTrazados() {
  cache.clear()
}
