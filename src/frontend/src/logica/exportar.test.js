import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

const { get } = vi.hoisted(() => ({ get: vi.fn() }))

vi.mock('../api/client', () => ({
  default: { get },
  extraerError: (error, fallback) => {
    const detail = error?.response?.data?.detail
    return typeof detail === 'string' ? detail : fallback
  },
}))

import {
  descargarArchivo,
  exportarResumenRuta,
  nombreDesdeContentDisposition,
} from './exportar'

let enlace

beforeEach(() => {
  get.mockReset()
  enlace = { style: {}, click: vi.fn(), remove: vi.fn() }
  globalThis.document = {
    createElement: vi.fn(() => enlace),
    body: { appendChild: vi.fn() },
  }
  globalThis.URL.createObjectURL = vi.fn(() => 'blob:prueba')
  globalThis.URL.revokeObjectURL = vi.fn()
})

afterEach(() => {
  delete globalThis.document
  delete globalThis.URL.createObjectURL
  delete globalThis.URL.revokeObjectURL
})

describe('nombreDesdeContentDisposition', () => {
  it('lee el nombre entre comillas', () => {
    expect(nombreDesdeContentDisposition('attachment; filename="ruta-123.csv"')).toBe('ruta-123.csv')
  })

  it('lee el nombre sin comillas', () => {
    expect(nombreDesdeContentDisposition('attachment; filename=ruta-456.csv')).toBe('ruta-456.csv')
  })

  it('usa el fallback si no hay encabezado', () => {
    expect(nombreDesdeContentDisposition(undefined, 'resumen.csv')).toBe('resumen.csv')
    expect(nombreDesdeContentDisposition('attachment', 'resumen.csv')).toBe('resumen.csv')
  })
})

describe('descargarArchivo', () => {
  it('crea, pulsa y elimina el enlace temporal', () => {
    descargarArchivo(new Blob(['contenido']), 'ruta.csv')

    expect(globalThis.document.body.appendChild).toHaveBeenCalledWith(enlace)
    expect(enlace.download).toBe('ruta.csv')
    expect(enlace.click).toHaveBeenCalledOnce()
    expect(enlace.remove).toHaveBeenCalledOnce()
    expect(globalThis.URL.revokeObjectURL).toHaveBeenCalledWith('blob:prueba')
  })

  it('acepta texto plano y lo convierte en blob', () => {
    descargarArchivo('a,b,c', 'ruta.csv')
    expect(globalThis.URL.createObjectURL).toHaveBeenCalledOnce()
    expect(enlace.download).toBe('ruta.csv')
  })
})

describe('exportarResumenRuta', () => {
  it('descarga el CSV con el nombre indicado por el backend', async () => {
    get.mockResolvedValue({
      data: new Blob(['Orden,Destinatario']),
      headers: { 'content-disposition': 'attachment; filename="ruta-abc.csv"' },
    })

    const nombre = await exportarResumenRuta('12345678-1234-1234-1234-123456789abc')

    expect(get).toHaveBeenCalledWith(
      '/rutas/12345678-1234-1234-1234-123456789abc/export',
      { responseType: 'blob' }
    )
    expect(nombre).toBe('ruta-abc.csv')
    expect(enlace.download).toBe('ruta-abc.csv')
  })

  it('usa un nombre de respaldo si falta Content-Disposition', async () => {
    get.mockResolvedValue({ data: new Blob(['x']), headers: {} })

    const nombre = await exportarResumenRuta('12345678-1234-1234-1234-123456789abc')

    expect(nombre).toBe('ruta-12345678.csv')
  })

  it('propaga el detalle del backend cuando la respuesta de error es un blob', async () => {
    get.mockRejectedValue({
      response: {
        status: 403,
        data: new Blob([JSON.stringify({ detail: 'No autorizado' })]),
      },
    })

    await expect(exportarResumenRuta('12345678-1234-1234-1234-123456789abc'))
      .rejects.toThrow('No autorizado')
  })

  it('propaga el detalle cuando el error ya es JSON', async () => {
    get.mockRejectedValue({
      response: { status: 404, data: { detail: 'Ruta no encontrada' } },
    })

    await expect(exportarResumenRuta('12345678-1234-1234-1234-123456789abc'))
      .rejects.toThrow('Ruta no encontrada')
  })
})
