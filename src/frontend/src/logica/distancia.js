export const CENTRO_LIMA = { latitud: -12.115, longitud: -76.97 }

/**
 * Distancia en linea recta entre dos coordenadas, en kilometros.
 * Formula de Haversine: la misma que usa el backend para calcular las rutas,
 * de modo que la distancia que ve el usuario en pantalla y la que viaja en la
 * respuesta de la API no se contradicen.
 */
export function haversineKm(a, b) {
  const R = 6371
  const rad = Math.PI / 180
  const dLat = (Number(b.latitud) - Number(a.latitud)) * rad
  const dLng = (Number(b.longitud) - Number(a.longitud)) * rad
  const h =
    Math.sin(dLat / 2) ** 2 +
    Math.cos(Number(a.latitud) * rad) * Math.cos(Number(b.latitud) * rad) * Math.sin(dLng / 2) ** 2
  return 2 * R * Math.asin(Math.min(1, Math.sqrt(h)))
}

/** Distancia desde el origen hasta el punto mas cercano de la lista. */
export function distanciaAlMasCercano(origen, puntos) {
  if (!origen || puntos.length === 0) return null
  return Math.min(...puntos.map(p => haversineKm(origen, p)))
}

/**
 * Devuelve el punto mas cercano al origen. Se usa para completar la ruta de
 * forma automatica: en lugar de que el operador revise uno por uno, la
 * aplicacion le entrega el siguiente pedido mas cercano.
 */
export function masCercano(origen, puntos) {
  if (!origen || puntos.length === 0) return null
  return puntos.reduce((mejor, p) => (haversineKm(origen, p) < haversineKm(origen, mejor) ? p : mejor))
}

/**
 * Puntos ordenados del mas cercano al mas lejano respecto del origen.
 * El orden no se altera dentro de la ruta ya elegida: sirve para presentar
 * los pedidos pendientes segun lo cerca que esten del ultimo punto de entrega.
 */
export function ordenarPorCercania(origen, puntos) {
  if (!origen) return [...puntos]
  return [...puntos].sort((a, b) => haversineKm(origen, a) - haversineKm(origen, b))
}

/** Distancia total siguiendo el orden de la lista (para previsualizar). */
export function distanciaTotalEnOrden(orden) {
  let total = 0
  for (let i = 1; i < orden.length; i += 1) total += haversineKm(orden[i - 1], orden[i])
  return total
}

/** Formatea kilometros con un decimal y sin ceros de relleno. */
export function formatoKm(km) {
  if (km == null) return '—'
  if (km < 1) return `${Math.round(km * 1000)} m`
  return `${km.toFixed(1)} km`
}
