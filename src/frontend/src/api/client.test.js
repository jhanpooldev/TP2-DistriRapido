import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import api, { API_BASE_URL } from './client'

function memoriaLocalStorage() {
  const datos = new Map()
  return {
    getItem: clave => datos.get(clave) ?? null,
    setItem: (clave, valor) => datos.set(clave, String(valor)),
    removeItem: clave => datos.delete(clave),
    clear: () => datos.clear(),
  }
}

class EventoFalso {
  constructor(tipo, opciones = {}) {
    this.type = tipo
    this.detail = opciones.detail
  }
}

describe('configuración del cliente HTTP', () => {
  let adaptadorOriginal
  let almacen
  let dispatchEvent

  beforeEach(() => {
    adaptadorOriginal = api.defaults.adapter
    almacen = memoriaLocalStorage()
    dispatchEvent = vi.fn()
    vi.stubGlobal('localStorage', almacen)
    vi.stubGlobal('window', { CustomEvent: EventoFalso, dispatchEvent })
  })

  afterEach(() => {
    api.defaults.adapter = adaptadorOriginal
    vi.unstubAllGlobals()
  })

  it('usa /api/v1 como base por defecto', () => {
    expect(API_BASE_URL).toBe('/api/v1')
    expect(api.defaults.baseURL).toBe('/api/v1')
  })

  it('un 401 autenticado cierra la sesión en todo el panel', async () => {
    almacen.setItem('token', 'token-viejo')
    api.defaults.adapter = async () => Promise.reject({
      response: { status: 401 },
      config: { url: '/rutas' },
    })

    await expect(api.get('/rutas')).rejects.toBeTruthy()

    expect(almacen.getItem('token')).toBeNull()
    expect(dispatchEvent).toHaveBeenCalledTimes(1)
    expect(dispatchEvent.mock.calls[0][0].type).toBe('auth:expired')
  })

  it('un 401 del login no cierra una sesión inexistente', async () => {
    api.defaults.adapter = async () => Promise.reject({
      response: { status: 401 },
      config: { url: '/auth/login' },
    })

    await expect(api.post('/auth/login', {})).rejects.toBeTruthy()

    expect(dispatchEvent).not.toHaveBeenCalled()
  })
})
