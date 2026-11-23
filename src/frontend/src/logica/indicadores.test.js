import { describe, expect, it } from 'vitest'
import {
  formatearNumero,
  tarjetasIndicadores,
  tarjetasSostenibilidad,
} from './indicadores'

describe('formatearNumero', () => {
  it('usa dos decimales y separador de miles', () => {
    expect(formatearNumero(1234.5)).toBe('1,234.50')
  })

  it('muestra un guion cuando el valor no es numerico', () => {
    expect(formatearNumero(undefined)).toBe('—')
  })
})

describe('tarjetasIndicadores', () => {
  it('muestra rutas, distancia y emisiones en cero', () => {
    const tarjetas = tarjetasIndicadores({
      cantidad_rutas: 0,
      distancia_total_km: 0,
      emisiones_estimadas_kg: 0,
    })
    expect(tarjetas).toHaveLength(3)
    expect(tarjetas[0].valor).toBe('0')
    expect(tarjetas[1].unidad).toBe('km')
    expect(tarjetas[2].unidad).toBe('kg CO₂')
  })
})

describe('tarjetasSostenibilidad', () => {
  it('muestra emisiones totales, por entrega y ahorro', () => {
    const tarjetas = tarjetasSostenibilidad({
      emisiones_totales_kg: 24,
      emisiones_por_entrega_kg: 2,
      ahorro_co2_kg: 6,
      ahorro_co2_pct: 20,
    })
    expect(tarjetas).toHaveLength(4)
    expect(tarjetas[1].valor).toBe('2.00')
    expect(tarjetas[3].unidad).toBe('%')
  })

  it('devuelve una lista vacia si no hay datos', () => {
    expect(tarjetasSostenibilidad(null)).toEqual([])
  })
})
