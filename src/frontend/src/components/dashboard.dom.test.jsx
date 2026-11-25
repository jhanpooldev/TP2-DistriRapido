// @vitest-environment happy-dom
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react'

import Dashboard from './Dashboard'

const mocks = vi.hoisted(() => ({
  get: vi.fn(),
  post: vi.fn(),
  put: vi.fn(),
  delete: vi.fn(),
  extraerError: vi.fn(
    (error, fallback = 'No se pudo completar la operacion') =>
      error?.response?.data?.detail || error?.message || fallback
  ),
  exportarResumenRuta: vi.fn(async () => 'resumen.csv'),
}))

vi.mock('../api/client', () => ({
  default: {
    get: mocks.get,
    post: mocks.post,
    put: mocks.put,
    delete: mocks.delete,
  },
  extraerError: mocks.extraerError,
}))

vi.mock('../logica/exportar', () => ({
  exportarResumenRuta: mocks.exportarResumenRuta,
}))

// Los reemplazos conservan las firmas de los componentes perezosos. El archivo
// verific aquí es Dashboard: los componentes reales se prueban en su propio archivo.
vi.mock('./MapPicker', () => ({
  default: ({ onPick }) => (
    <div>
      <button type="button" onClick={() => onPick(-12.1, -77, 'Av. Fijada')}>Fijar direccion</button>
      <button type="button" onClick={() => onPick(-12.2, -77.1)}>Fijar coordenadas</button>
    </div>
  ),
}))

vi.mock('./MapView', () => ({
  default: () => <div data-testid="mapa-ruta">Mapa de la ruta</div>,
}))

vi.mock('./SelectorPuntos', () => ({
  default: ({ puntos = [], seleccionados = [], onChange }) => (
    <div>
      <button
        type="button"
        onClick={() => onChange([...new Set([...seleccionados, puntos[0]?.id_punto].filter(Boolean))])}
      >
        Agregar punto 1
      </button>
      <button
        type="button"
        onClick={() => onChange([...new Set([...seleccionados, puntos[1]?.id_punto].filter(Boolean))])}
      >
        Agregar punto 2
      </button>
      <button type="button" onClick={() => onChange([])}>Vaciar puntos</button>
    </div>
  ),
}))

vi.mock('./RutasTab', () => ({
  default: ({ rutas = [], onVerMapa, onCambiado, onMensaje, soloLectura }) => (
    <div>
      <span>{soloLectura ? 'Rutas (solo lectura)' : 'Rutas (editable)'}</span>
      <button type="button" onClick={() => onVerMapa(rutas[0])}>Ver mapa</button>
      <button type="button" onClick={() => onCambiado([], { total: 0, page: 1 })}>Cambiar rutas</button>
      <button type="button" onClick={() => onMensaje({ tipo: 'ok', texto: 'Aviso de rutas' })}>
        Emitir mensaje
      </button>
    </div>
  ),
}))

vi.mock('./ImpactoTab', () => ({
  default: () => <div>Impacto ambiental cargado</div>,
}))

vi.mock('./IndicadoresTab', () => ({
  default: () => <div>Panel de indicadores cargado</div>,
}))

const punto = (id, destinatario, peso) => ({
  id_punto: id,
  direccion: `Direccion ${id}`,
  destinatario,
  latitud: -12.115,
  longitud: -76.97,
  peso_kg: peso,
})

const puntos = [punto('a', 'Ana', 5), punto('b', 'Beto', 7)]

const vehiculo = {
  id_vehiculo: 1,
  placa: 'ABC-123',
  capacidad_kg: 100,
  factor_emision_co2: 2.68,
  consumo_litros_km: 0.12,
  velocidad_promedio_kmh: 35,
  tipo_combustible: 'Diesel',
}

const ruta = {
  id_ruta: '11111111-2222-3333-4444-555555555555',
  fecha_generacion: '2026-11-19T10:00:00Z',
  estado: 'Confirmada',
  distancia_total_km: 10,
  tiempo_estimado_min: 20,
  co2_estimado_kg: 2,
  origen_lat: -12.115,
  origen_lng: -76.97,
  origen_direccion: 'Centro de distribucion',
  puntos,
}

const operador = { nombre: 'Operador Demo', rol: { nombre: 'Operador Logístico' } }
const administrador = { id_rol: 1, nombre: 'Admin', rol: { nombre: 'Administrador' } }
const gerente = { nombre: 'Gerente', rol: { nombre: 'Gerente' } }

beforeEach(() => {
  vi.clearAllMocks()
  mocks.get.mockImplementation((url) => {
    if (url === '/puntos-entrega') {
      return Promise.resolve({ data: { puntos, total: puntos.length, page: 1 } })
    }
    if (url === '/rutas') {
      return Promise.resolve({
        data: [ruta],
        headers: { 'x-total-count': '1', 'x-page': '1', 'x-total-pages': '1' },
      })
    }
    if (url === '/vehiculos') return Promise.resolve({ data: [vehiculo] })
    if (url === '/geocoding/reverse') return Promise.resolve({ data: { direccion: 'Av. Inversa' } })
    return Promise.resolve({ data: [] })
  })
  mocks.post.mockImplementation((url) => {
    if (url === '/rutas/optimizar' || url === '/rutas') return Promise.resolve({ data: ruta })
    return Promise.resolve({ data: { id_vehiculo: 2, placa: 'XYZ-456' } })
  })
  mocks.put.mockResolvedValue({})
  mocks.delete.mockResolvedValue({})
  mocks.exportarResumenRuta.mockResolvedValue('resumen.csv')
  mocks.extraerError.mockImplementation(
    (error, fallback = 'No se pudo completar la operacion') =>
      error?.response?.data?.detail || error?.message || fallback
  )
  window.confirm = vi.fn(() => true)
  window.scrollTo = vi.fn()
})

afterEach(() => {
  cleanup()
})

describe('Dashboard: carga inicial, pestañas y permisos', () => {
  it('carga pedidos, rutas y vehículos con paginación', async () => {
    render(<Dashboard user={operador} onLogout={vi.fn()} />)

    expect(await screen.findByText('Pedidos registrados')).toBeTruthy()
    expect(screen.getByText('Registrar pedido de entrega')).toBeTruthy()
    expect(screen.getByText('Ana')).toBeTruthy()
    expect(mocks.get).toHaveBeenCalledWith('/puntos-entrega', { params: { page: 1, limit: 12 } })
    expect(mocks.get).toHaveBeenCalledWith('/rutas', { params: { page: 1, limit: 12 } })
    expect(mocks.get).toHaveBeenCalledWith('/vehiculos')
  })

  it('navega por pestañas con el teclado', async () => {
    render(<Dashboard user={administrador} onLogout={vi.fn()} />)

    fireEvent.keyDown(screen.getByRole('tab', { name: 'Pedidos' }), { key: 'ArrowRight' })
    expect(await screen.findByText(/Armar una ruta/)).toBeTruthy()

    fireEvent.keyDown(screen.getByRole('tab', { name: 'Rutas' }), { key: 'End' })
    expect(await screen.findByText('Panel de indicadores cargado')).toBeTruthy()

    fireEvent.keyDown(screen.getByRole('tab', { name: 'Indicadores' }), { key: 'Home' })
    expect(await screen.findByText('Registrar pedido de entrega')).toBeTruthy()

    fireEvent.keyDown(screen.getByRole('tab', { name: 'Pedidos' }), { key: 'ArrowLeft' })
    expect(await screen.findByText('Panel de indicadores cargado')).toBeTruthy()
  })

  it('el administrador registra vehículos con la placa normalizada', async () => {
    render(<Dashboard user={administrador} onLogout={vi.fn()} />)
    fireEvent.click(screen.getByRole('tab', { name: 'Vehiculos' }))

    expect(await screen.findByRole('heading', { name: 'Agregar vehiculo' })).toBeTruthy()
    fireEvent.change(screen.getByLabelText('Placa'), { target: { value: 'xyz-456' } })
    fireEvent.change(screen.getByLabelText('Capacidad (kg)'), { target: { value: '900' } })
    fireEvent.change(screen.getByLabelText('Factor de emision (kg CO2/L)'), { target: { value: '2.6' } })
    fireEvent.change(screen.getByLabelText('Consumo (L/km)'), { target: { value: '0.11' } })
    fireEvent.change(screen.getByLabelText('Velocidad promedio (km/h)'), { target: { value: '40' } })
    fireEvent.change(screen.getByLabelText('Combustible'), { target: { value: 'GLP' } })
    fireEvent.submit(screen.getByRole('button', { name: 'Agregar vehiculo' }).closest('form'))

    await waitFor(() =>
      expect(mocks.post).toHaveBeenCalledWith('/vehiculos', expect.objectContaining({ placa: 'XYZ-456' }))
    )
    expect(await screen.findByText(/Vehiculo XYZ-456 agregado/)).toBeTruthy()
  })

  it('el gerente solo ve lectura y no formularios de escritura', async () => {
    render(<Dashboard user={gerente} onLogout={vi.fn()} />)

    expect(await screen.findByText(/acceso de solo lectura/)).toBeTruthy()
    expect(screen.queryByText('Registrar pedido de entrega')).toBeNull()
    expect(document.getElementById('tab-vehiculos')).toBeNull()

    fireEvent.click(screen.getByRole('tab', { name: 'Rutas' }))
    expect(await screen.findByText('Rutas (solo lectura)')).toBeTruthy()
    expect(screen.queryByText(/Armar una ruta/)).toBeNull()
  })
})

describe('Dashboard: operaciones del operador', () => {
  it('registra un pedido y permite cerrar el aviso', async () => {
    render(<Dashboard user={operador} onLogout={vi.fn()} />)

    fireEvent.change(screen.getByLabelText('Direccion'), { target: { value: 'Av. Nueva 123' } })
    fireEvent.change(screen.getByLabelText('Latitud'), { target: { value: '-12.12' } })
    fireEvent.change(screen.getByLabelText('Longitud'), { target: { value: '-77.01' } })
    fireEvent.change(screen.getByLabelText('Peso (kg)'), { target: { value: '5.5' } })
    fireEvent.change(screen.getByLabelText('Destinatario'), { target: { value: 'Carla' } })
    fireEvent.submit(screen.getByRole('button', { name: 'Registrar pedido' }).closest('form'))

    expect(await screen.findByText(/Pedido registrado/)).toBeTruthy()
    expect(mocks.post).toHaveBeenCalledWith('/puntos-entrega', expect.objectContaining({ destinatario: 'Carla' }))
    fireEvent.click(screen.getByRole('button', { name: 'Cerrar aviso' }))
    expect(screen.queryByText(/Pedido registrado/)).toBeNull()
  })

  it('fija coordenadas desde el mapa y consulta la dirección inversa', async () => {
    render(<Dashboard user={operador} onLogout={vi.fn()} />)

    fireEvent.click(screen.getByRole('button', { name: 'Fijar direccion' }))
    expect(screen.getByLabelText('Direccion').value).toBe('Av. Fijada')
    expect(mocks.get).not.toHaveBeenCalledWith('/geocoding/reverse', expect.anything())

    fireEvent.click(screen.getByRole('button', { name: 'Fijar coordenadas' }))
    await waitFor(() => expect(screen.getByLabelText('Direccion').value).toBe('Av. Inversa'))
    expect(mocks.get).toHaveBeenCalledWith('/geocoding/reverse', {
      params: { latitud: -12.2, longitud: -77.1 },
    })
  })

  it('edita y elimina un pedido', async () => {
    render(<Dashboard user={operador} onLogout={vi.fn()} />)
    await screen.findByText('Ana')

    fireEvent.click(screen.getAllByRole('button', { name: 'Editar' })[0])
    const campo = document.getElementById('editar-direccion-a')
    fireEvent.change(campo, { target: { value: 'Av. Editada' } })
    fireEvent.submit(screen.getByRole('button', { name: 'Guardar cambios' }).closest('form'))
    await waitFor(() => expect(mocks.put).toHaveBeenCalledWith('/puntos-entrega/a', expect.anything()))
    expect(await screen.findByText('Pedido actualizado.')).toBeTruthy()

    fireEvent.click(screen.getAllByRole('button', { name: /Eliminar pedido/ })[0])
    await waitFor(() => expect(mocks.delete).toHaveBeenCalledWith('/puntos-entrega/a'))
    expect(await screen.findByText('Pedido eliminado de la lista de planificación.')).toBeTruthy()
  })

  it('calcula, confirma y exporta una ruta', async () => {
    render(<Dashboard user={operador} onLogout={vi.fn()} />)
    await screen.findByText('Ana')
    fireEvent.click(screen.getByRole('tab', { name: 'Rutas' }))
    await screen.findByText('Rutas (editable)')

    fireEvent.click(screen.getByRole('button', { name: 'Agregar punto 1' }))
    fireEvent.click(screen.getByRole('button', { name: 'Agregar punto 2' }))
    expect(await screen.findByText(/2 pedidos seleccionados/)).toBeTruthy()

    fireEvent.click(screen.getByRole('button', { name: 'Optimizar (simular)' }))
    await waitFor(() => expect(mocks.post).toHaveBeenCalledWith('/rutas/optimizar', expect.anything()))
    expect(await screen.findByText(/Vista previa/)).toBeTruthy()

    fireEvent.click(screen.getByRole('button', { name: 'Confirmar y guardar' }))
    await waitFor(() => expect(mocks.post).toHaveBeenCalledWith('/rutas', expect.anything()))
    expect(await screen.findByText('Ruta confirmada y guardada.')).toBeTruthy()

    fireEvent.click(screen.getByRole('button', { name: /Exportar resumen de la ruta/ }))
    await waitFor(() => expect(mocks.exportarResumenRuta).toHaveBeenCalledWith(ruta.id_ruta))
  })

  it('selecciona una ruta guardada en el mapa y la exporta', async () => {
    render(<Dashboard user={operador} onLogout={vi.fn()} />)
    fireEvent.click(screen.getByRole('tab', { name: 'Mapa' }))

    fireEvent.change(await screen.findByLabelText('Ruta guardada'), {
      target: { value: ruta.id_ruta },
    })
    expect(await screen.findByTestId('mapa-ruta')).toBeTruthy()
    fireEvent.click(screen.getByRole('button', { name: /Exportar resumen de la ruta/ }))
    await waitFor(() => expect(mocks.exportarResumenRuta).toHaveBeenCalledWith(ruta.id_ruta))
  })

  it('revoca la sesión antes de avisar al componente padre', async () => {
    const onLogout = vi.fn()
    render(<Dashboard user={operador} onLogout={onLogout} />)

    fireEvent.click(screen.getByRole('button', { name: 'Salir' }))

    await waitFor(() => expect(mocks.post).toHaveBeenCalledWith('/auth/logout'))
    expect(onLogout).toHaveBeenCalledTimes(1)
  })
})
