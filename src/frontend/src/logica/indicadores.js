/** Presentación de los indicadores devueltos por el backend (RF-012/RF-013). */

const formateadores = new Map()

function formateador(decimales) {
  if (!formateadores.has(decimales)) {
    formateadores.set(
      decimales,
      new Intl.NumberFormat('es-PE', {
        minimumFractionDigits: decimales,
        maximumFractionDigits: decimales,
      }),
    )
  }
  return formateadores.get(decimales)
}

export function formatearNumero(valor, decimales = 2) {
  const numero = Number(valor)
  return Number.isFinite(numero) ? formateador(decimales).format(numero) : '—'
}

export function tarjetasIndicadores(datos) {
  if (!datos) return []
  return [
    { id: 'rutas', etiqueta: 'Rutas generadas', valor: formatearNumero(datos.cantidad_rutas, 0), unidad: '' },
    { id: 'distancia', etiqueta: 'Distancia total', valor: formatearNumero(datos.distancia_total_km), unidad: 'km' },
    { id: 'emisiones', etiqueta: 'Emisiones estimadas', valor: formatearNumero(datos.emisiones_estimadas_kg), unidad: 'kg CO₂' },
  ]
}

export function tarjetasSostenibilidad(datos) {
  if (!datos) return []
  return [
    { id: 'totales', etiqueta: 'Emisiones totales', valor: formatearNumero(datos.emisiones_totales_kg), unidad: 'kg CO₂' },
    { id: 'entrega', etiqueta: 'Emisiones por entrega', valor: formatearNumero(datos.emisiones_por_entrega_kg), unidad: 'kg CO₂' },
    { id: 'ahorro', etiqueta: 'Ahorro de CO₂', valor: formatearNumero(datos.ahorro_co2_kg), unidad: 'kg' },
    { id: 'ahorro-pct', etiqueta: 'Reducción porcentual', valor: formatearNumero(datos.ahorro_co2_pct), unidad: '%' },
  ]
}
