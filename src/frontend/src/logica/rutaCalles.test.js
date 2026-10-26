import { beforeEach, describe, expect, it, vi } from 'vitest'
import {
  construirUrlTrazado,
  limpiarCacheTrazados,
  normalizarTrazado,
  obtenerTrazadoCalles,
} from './rutaCalles'

const RECORRIDO = [
  [-12.115, -76.97],
  [-12.10, -76.95],
]

function respuestaOk() {
  return {
    ok: true,
    json: async () => ({
      code: 'Ok',
      routes: [
        {
          distance: 6136.6,
          geometry: {
            coordinates: [
              [-76.97, -12.115],
              [-76.96, -12.11],
              [-76.95, -12.10],
            ],
          },
        },
      ],
    }),
  }
}

beforeEach(() => {
  limpiarCacheTrazados()
})

describe('construirUrlTrazado', () => {
  it('envia los puntos como longitud,latitud como exige OSRM', () => {
    const url = construirUrlTrazado(RECORRIDO)

    expect(url).toContain('/route/v1/driving/-76.97,-12.115;-76.95,-12.1')
    expect(url).toContain('overview=full')
    expect(url).toContain('geometries=geojson')
  })
})

describe('normalizarTrazado', () => {
  it('convierte la geometria GeoJSON a pares latitud,longitud', () => {
    const resultado = normalizarTrazado({
      code: 'Ok',
      routes: [
        {
          distance: 1500,
          geometry: { coordinates: [[-76.97, -12.115], [-76.96, -12.11]] },
        },
      ],
    })

    expect(resultado.trazado).toEqual([
      [-12.115, -76.97],
      [-12.11, -76.96],
    ])
    expect(resultado.distanciaKm).toBeCloseTo(1.5)
  })

  it('descarta respuestas sin ruta o con geometria insuficiente', () => {
    expect(normalizarTrazado({ code: 'NoRoute' })).toBeNull()
    expect(normalizarTrazado({ code: 'Ok', routes: [] })).toBeNull()
    expect(
      normalizarTrazado({ code: 'Ok', routes: [{ geometry: { coordinates: [[-76.97, -12.115]] } }] })
    ).toBeNull()
  })
})

describe('obtenerTrazadoCalles', () => {
  it('devuelve null cuando hay menos de dos puntos', async () => {
    const fetchImpl = vi.fn()

    expect(await obtenerTrazadoCalles([], { fetchImpl })).toBeNull()
    expect(await obtenerTrazadoCalles([RECORRIDO[0]], { fetchImpl })).toBeNull()
    expect(fetchImpl).not.toHaveBeenCalled()
  })

  it('consulta una sola vez el mismo recorrido', async () => {
    const fetchImpl = vi.fn().mockResolvedValue(respuestaOk())

    const primero = await obtenerTrazadoCalles(RECORRIDO, { fetchImpl })
    const segundo = await obtenerTrazadoCalles(RECORRIDO, { fetchImpl })

    expect(fetchImpl).toHaveBeenCalledTimes(1)
    expect(primero).toEqual(segundo)
    expect(primero.trazado).toHaveLength(3)
  })

  it('usa una url distinta cuando cambia el orden de las paradas', async () => {
    const fetchImpl = vi.fn().mockResolvedValue(respuestaOk())

    await obtenerTrazadoCalles(RECORRIDO, { fetchImpl })
    await obtenerTrazadoCalles([...RECORRIDO].reverse(), { fetchImpl })

    expect(fetchImpl).toHaveBeenCalledTimes(2)
    expect(fetchImpl.mock.calls[0][0]).not.toBe(fetchImpl.mock.calls[1][0])
  })

  it('devuelve null si el servicio responde con error o sin red', async () => {
    const sinRed = vi.fn().mockRejectedValue(new Error('offline'))
    const conError = vi.fn().mockResolvedValue({ ok: false, json: async () => ({}) })

    expect(await obtenerTrazadoCalles(RECORRIDO, { fetchImpl: sinRed })).toBeNull()
    expect(await obtenerTrazadoCalles(RECORRIDO, { fetchImpl: conError })).toBeNull()
  })

  it('no consulta el servicio si la peticion ya fue cancelada', async () => {
    const fetchImpl = vi.fn()
    const controlador = new AbortController()
    controlador.abort()

    const resultado = await obtenerTrazadoCalles(RECORRIDO, {
      fetchImpl,
      signal: controlador.signal,
    })

    expect(resultado).toBeNull()
    expect(fetchImpl).not.toHaveBeenCalled()
  })
})
