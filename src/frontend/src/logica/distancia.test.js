import { describe, expect, it } from 'vitest'
import {
  CENTRO_LIMA,
  distanciaAlMasCercano,
  distanciaTotalEnOrden,
  formatoKm,
  haversineKm,
  masCercano,
  ordenarPorCercania,
} from './distancia'

describe('haversineKm', () => {
  it('calcula un grado de latitud como ~111 km', () => {
    const km = haversineKm({ latitud: 0, longitud: 0 }, { latitud: 1, longitud: 0 })
    expect(km).toBeGreaterThan(111)
    expect(km).toBeLessThan(111.3)
  })

  it('devuelve 0 para el mismo punto', () => {
    expect(haversineKm(CENTRO_LIMA, CENTRO_LIMA)).toBe(0)
  })
})

describe('seleccion por cercania', () => {
  const origen = { latitud: 0, longitud: 0 }
  const cerca = { id: 'cerca', latitud: 0.01, longitud: 0 }
  const lejos = { id: 'lejos', latitud: 0.5, longitud: 0 }

  it('encuentra el mas cercano', () => {
    expect(masCercano(origen, [lejos, cerca])).toBe(cerca)
    expect(distanciaAlMasCercano(origen, [lejos, cerca])).toBeLessThan(2)
  })

  it('ordena sin mutar la lista original', () => {
    const original = [lejos, cerca]
    expect(ordenarPorCercania(origen, original).map(p => p.id)).toEqual(['cerca', 'lejos'])
    expect(original.map(p => p.id)).toEqual(['lejos', 'cerca'])
  })

  it('devuelve null sin origen o sin puntos', () => {
    expect(masCercano(null, [cerca])).toBeNull()
    expect(masCercano(origen, [])).toBeNull()
    expect(distanciaAlMasCercano(null, [cerca])).toBeNull()
  })
})

describe('formato y distancia acumulada', () => {
  it('formatea metros y kilometros', () => {
    expect(formatoKm(null)).toBe('—')
    expect(formatoKm(0.5)).toBe('500 m')
    expect(formatoKm(2.34)).toBe('2.3 km')
  })

  it('suma solo los tramos entre puntos', () => {
    const puntos = [
      { latitud: 0, longitud: 0 },
      { latitud: 0, longitud: 0.01 },
      { latitud: 0, longitud: 0.02 },
    ]
    expect(distanciaTotalEnOrden(puntos)).toBeGreaterThan(2)
    expect(distanciaTotalEnOrden([puntos[0]])).toBe(0)
  })
})
