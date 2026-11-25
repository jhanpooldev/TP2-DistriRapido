// @vitest-environment happy-dom
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react'
import L from 'leaflet'

import { obtenerTrazadoCalles } from '../logica/rutaCalles'
import { exportarResumenRuta } from '../logica/exportar'
import api from '../api/client'
import ImpactoTab from './ImpactoTab'
import IndicadoresTab from './IndicadoresTab'
import Login from './Login'
import MapPicker from './MapPicker'
import MapView from './MapView'
import Paginacion from './Paginacion'
import RutasTab from './RutasTab'
import SelectorPuntos from './SelectorPuntos'

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
  obtenerTrazadoCalles: vi.fn(async () => null),
  leaflet: {
    map: vi.fn(),
    tileLayer: vi.fn(),
    marker: vi.fn(),
    polyline: vi.fn(),
    divIcon: vi.fn(() => ({})),
    latLngBounds: vi.fn(() => ({})),
    instanciaMapa: {},
    capa: {},
    marcador: {},
  },
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

vi.mock('../logica/rutaCalles', () => ({
  obtenerTrazadoCalles: mocks.obtenerTrazadoCalles,
}))

vi.mock('leaflet/dist/leaflet.css', () => ({}))

vi.mock('leaflet', () => {
  const mapa = mocks.leaflet.instanciaMapa
  mapa.on = vi.fn()
  mapa.remove = vi.fn()
  mapa.getCenter = vi.fn(() => ({ lat: -12.115, lng: -76.97 }))
  mapa.flyTo = vi.fn()
  mapa.fitBounds = vi.fn()
  mapa.setView = vi.fn()
  mapa.removeLayer = vi.fn()

  const capa = mocks.leaflet.capa
  capa.on = vi.fn(() => capa)
  capa.addTo = vi.fn(() => capa)
  capa.remove = vi.fn()

  const marcador = mocks.leaflet.marcador
  marcador.on = vi.fn(() => marcador)
  marcador.addTo = vi.fn(() => marcador)
  marcador.bindPopup = vi.fn(() => marcador)
  marcador.setLatLng = vi.fn()
  marcador.remove = vi.fn()
  marcador.getLatLng = vi.fn(() => ({ lat: -12.12, lng: -77.01 }))

  return {
    default: {
      map: vi.fn(() => mapa),
      tileLayer: vi.fn(() => capa),
      marker: vi.fn(() => marcador),
      polyline: vi.fn(() => capa),
      divIcon: mocks.leaflet.divIcon,
      latLngBounds: mocks.leaflet.latLngBounds,
    },
  }
})

const punto = (id, destinatario, peso, latitud, longitud) => ({
  id_punto: id,
  direccion: `Direccion ${id}`,
  destinatario,
  latitud,
  longitud,
  peso_kg: peso,
})

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
  id_vehiculo: 1,
  estado: 'Confirmada',
  distancia_total_km: 10,
  tiempo_estimado_min: 20,
  co2_estimado_kg: 2,
  distancia_sin_optimizar_km: 12,
  tiempo_sin_optimizar_min: 24,
  co2_sin_optimizar_kg: 3,
  ahorro_distancia_pct: 16.7,
  ahorro_co2_pct: 33.3,
  ahorro_co2_kg: 1,
  origen_lat: -12.115,
  origen_lng: -76.97,
  origen_direccion: 'Centro de distribucion',
  puntos: [punto('a', 'Ana', 5, -12.1151, -76.9701), punto('b', 'Beto', 6, -12.13, -77.0)],
}

beforeEach(() => {
  vi.clearAllMocks()
  mocks.exportarResumenRuta.mockResolvedValue('resumen.csv')
  mocks.obtenerTrazadoCalles.mockResolvedValue(null)
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

describe('Paginacion e Login con interacción real', () => {
  it('Paginacion invoca onChange con la pagina anterior y siguiente', () => {
    const onChange = vi.fn()
    render(<Paginacion page={2} pages={3} total={36} onChange={onChange} etiqueta="pedidos" />)

    fireEvent.click(screen.getByRole('button', { name: 'Anterior' }))
    fireEvent.click(screen.getByRole('button', { name: 'Siguiente' }))

    expect(onChange.mock.calls).toEqual([[1], [3]])
  })

  it('Login envia credenciales y entrega el token al padre', async () => {
    const onLogin = vi.fn()
    mocks.post.mockResolvedValue({ data: { access_token: 'token-real' } })
    render(<Login onLogin={onLogin} />)

    fireEvent.change(screen.getByLabelText('Correo'), { target: { value: 'ana@demo.com' } })
    fireEvent.change(screen.getByLabelText('Contrasena'), { target: { value: 'clave123' } })
    fireEvent.click(screen.getByRole('button', { name: 'Ingresar' }))

    await waitFor(() => expect(onLogin).toHaveBeenCalledWith('token-real'))
    const [url, cuerpo] = mocks.post.mock.calls[0]
    expect(url).toBe('/auth/login')
    expect(cuerpo.get('correo')).toBe('ana@demo.com')
    expect(cuerpo.get('password')).toBe('clave123')
  })

  it('Login muestra credenciales invalidas ante un 401', async () => {
    mocks.post.mockRejectedValue({ response: { status: 401 } })
    render(<Login onLogin={vi.fn()} />)

    fireEvent.change(screen.getByLabelText('Correo'), { target: { value: 'ana@demo.com' } })
    fireEvent.change(screen.getByLabelText('Contrasena'), { target: { value: 'mala' } })
    fireEvent.click(screen.getByRole('button', { name: 'Ingresar' }))

    expect(await screen.findByText('Credenciales invalidas')).toBeTruthy()
  })
})

describe('IndicadoresTab con datos, sin datos y error', () => {
  it('muestra las tarjetas despues de consultar ambos endpoints', async () => {
    mocks.get.mockImplementation((url) => {
      if (url === '/indicadores') {
        return Promise.resolve({
          data: { cantidad_rutas: 3, distancia_total_km: 12.3, emisiones_estimadas_kg: 4.5 },
        })
      }
      return Promise.resolve({
        data: {
          emisiones_totales_kg: 9,
          emisiones_por_entrega_kg: 1.5,
          ahorro_co2_kg: 2,
          ahorro_co2_pct: 20,
          entregas: 6,
        },
      })
    })

    render(<IndicadoresTab />)

    expect(await screen.findByText('Panel de indicadores')).toBeTruthy()
    expect(screen.getByText('Rutas generadas')).toBeTruthy()
    expect(screen.getByText('Emisiones por entrega')).toBeTruthy()
    expect(screen.getByText(/6 entregas consideradas/)).toBeTruthy()
  })

  it('muestra los avisos de sin datos y el error de la API', async () => {
    mocks.get
      .mockResolvedValueOnce({ data: { sin_datos: true, mensaje: 'Sin rutas confirmadas' } })
      .mockResolvedValueOnce({ data: { sin_datos: true, mensaje: 'Sin emisiones registradas' } })
    const primera = render(<IndicadoresTab />)
    expect(await screen.findByText('Sin rutas confirmadas')).toBeTruthy()
    expect(screen.getByText('Sin emisiones registradas')).toBeTruthy()
    primera.unmount()

    mocks.get.mockReset()
    mocks.get.mockRejectedValue(new Error('servidor caido'))
    render(<IndicadoresTab />)
    expect(await screen.findByText('servidor caido')).toBeTruthy()
  })
})

describe('SelectorPuntos con interacción real', () => {
  const puntos = [
    punto('a', 'Ana', 4, -12.1151, -76.9701),
    punto('b', 'Beto', 6, -13, -77),
  ]

  it('agrega, filtra, quita y vacia la seleccion', async () => {
    const onChange = vi.fn()
    const vista = render(
      <SelectorPuntos
        puntos={puntos}
        seleccionados={[]}
        onChange={onChange}
        vehiculos={[vehiculo]}
        idVehiculo={1}
      />
    )

    fireEvent.click(screen.getAllByRole('button', { name: 'Agregar' })[0])
    expect(onChange).toHaveBeenCalledWith(['a'])

    fireEvent.change(screen.getByLabelText('Pedidos disponibles'), { target: { value: 'Beto' } })
    expect(screen.queryByText('Ana')).toBeNull()
    expect(screen.getByText(/Beto/)).toBeTruthy()

    fireEvent.click(screen.getByRole('button', { name: '+ Siguiente mas cercano' }))
    expect(onChange).toHaveBeenCalledWith(['b'])

    vista.rerender(
      <SelectorPuntos
        puntos={puntos}
        seleccionados={['a']}
        onChange={onChange}
        vehiculos={[vehiculo]}
        idVehiculo={1}
      />
    )
    fireEvent.click(screen.getByRole('button', { name: 'Vaciar seleccion' }))
    expect(onChange).toHaveBeenCalledWith([])
  })

  it('avisa cuando no hay mas pedidos o la carga no cabe', async () => {
    const onChange = vi.fn()
    const primera = render(
      <SelectorPuntos
        puntos={puntos}
        seleccionados={['a', 'b']}
        onChange={onChange}
        vehiculos={[vehiculo]}
        idVehiculo={1}
      />
    )
    fireEvent.click(screen.getByRole('button', { name: '+ Siguiente mas cercano' }))
    expect(await screen.findByText('No quedan pedidos disponibles para agregar.')).toBeTruthy()
    fireEvent.click(screen.getByRole('button', { name: 'Quitar Direccion a' }))
    expect(onChange).toHaveBeenCalledWith(['b'])
    primera.unmount()

    render(
      <SelectorPuntos
        puntos={puntos}
        seleccionados={['a']}
        onChange={vi.fn()}
        vehiculos={[{ ...vehiculo, capacidad_kg: 8 }]}
        idVehiculo={1}
      />
    )
    fireEvent.click(screen.getAllByRole('button', { name: 'Agregar' })[0])
    expect(await screen.findByText(/llegaria a 10.0 kg/)).toBeTruthy()
  })

  it('bloquea la seleccion cuando la carga ya supera la capacidad', () => {
    render(
      <SelectorPuntos
        puntos={puntos}
        seleccionados={['a']}
        onChange={vi.fn()}
        vehiculos={[{ ...vehiculo, capacidad_kg: 3 }]}
        idVehiculo={1}
      />
    )

    expect(screen.getByText(/supera la capacidad de ABC-123/)).toBeTruthy()
    expect(screen.getByRole('button', { name: '+ Siguiente mas cercano' }).disabled).toBe(true)
  })
})

describe('ImpactoTab con una ruta seleccionada', () => {
  it('muestra la comparacion y permite ver el mapa', async () => {
    const onVerMapa = vi.fn()
    render(<ImpactoTab rutas={[ruta]} onVerMapa={onVerMapa} />)

    fireEvent.change(screen.getByLabelText('Ruta a evaluar'), { target: { value: ruta.id_ruta } })

    expect(await screen.findByText('Comparacion de emisiones')).toBeTruthy()
    expect(screen.getByText('33.3%')).toBeTruthy()
    expect(screen.getByText(/La optimizacion evito 1 kg de CO2/)).toBeTruthy()
    fireEvent.click(screen.getByRole('button', { name: 'Ver ruta en el mapa' }))
    expect(onVerMapa).toHaveBeenCalledWith(ruta)
  })

  it('informa cuando no hay reduccion significativa', async () => {
    render(
      <ImpactoTab
        rutas={[{ ...ruta, sin_reduccion_significativa: true, ahorro_co2_pct: 0 }]}
        onVerMapa={vi.fn()}
      />
    )

    fireEvent.change(screen.getByLabelText('Ruta a evaluar'), { target: { value: ruta.id_ruta } })
    expect(await screen.findByText(/No hubo una reduccion significativa de CO2/)).toBeTruthy()
  })
})

describe('RutasTab con filtros, edicion y exportacion', () => {
  const propsBase = () => ({
    rutas: [ruta],
    puntos: ruta.puntos,
    vehiculos: [vehiculo],
    total: 1,
    page: 1,
    onVerMapa: vi.fn(),
    onCambiado: vi.fn(),
    onMensaje: vi.fn(),
  })

  it('aplica filtros, limpia y avisa cuando no hay resultados', async () => {
    const props = propsBase()
    mocks.get.mockResolvedValue({ data: [], headers: {} })
    render(<RutasTab {...props} />)

    fireEvent.change(screen.getByLabelText('Desde'), { target: { value: '2026-11-01' } })
    fireEvent.change(screen.getByLabelText('Estado'), { target: { value: 'Confirmada' } })
    fireEvent.click(screen.getByRole('button', { name: 'Aplicar filtro' }))

    await waitFor(() =>
      expect(props.onMensaje).toHaveBeenCalledWith({
        tipo: 'info',
        texto: 'Ninguna ruta coincide con el filtro aplicado.',
      })
    )
    expect(mocks.get).toHaveBeenCalledWith(
      '/rutas',
      expect.objectContaining({ params: expect.objectContaining({ estado: 'Confirmada', page: 1 }) })
    )

    fireEvent.click(screen.getByRole('button', { name: 'Limpiar' }))
    await waitFor(() =>
      expect(props.onMensaje).toHaveBeenCalledWith({ tipo: 'ok', texto: 'Filtros limpiados.' })
    )
  })

  it('edita, elimina y exporta una ruta', async () => {
    const props = propsBase()
    mocks.get.mockResolvedValue({ data: [ruta], headers: { 'x-total-count': '1', 'x-page': '1' } })
    mocks.put.mockResolvedValue({ data: ruta })
    mocks.delete.mockResolvedValue({})
    render(<RutasTab {...props} />)

    fireEvent.click(screen.getByRole('button', { name: /Editar la ruta/ }))
    expect(await screen.findByText(/Editando la ruta/)).toBeTruthy()
    fireEvent.click(screen.getByRole('button', { name: 'Guardar y recalcular' }))
    await waitFor(() => expect(mocks.put).toHaveBeenCalled())

    fireEvent.click(screen.getByRole('button', { name: /Eliminar la ruta/ }))
    await waitFor(() => expect(mocks.delete).toHaveBeenCalledWith(`/rutas/${ruta.id_ruta}`))

    fireEvent.click(screen.getByRole('button', { name: /Exportar resumen de la ruta/ }))
    await waitFor(() => expect(mocks.exportarResumenRuta).toHaveBeenCalledWith(ruta.id_ruta))
  })

  it('la vista de solo lectura oculta acciones de escritura', () => {
    const props = propsBase()
    render(<RutasTab {...props} soloLectura />)

    expect(screen.queryByRole('button', { name: /Editar la ruta/ })).toBeNull()
    expect(screen.queryByRole('button', { name: /Eliminar la ruta/ })).toBeNull()
    fireEvent.click(screen.getByRole('button', { name: /Ver la ruta/ }))
    expect(props.onVerMapa).toHaveBeenCalledWith(ruta)
  })

  it('rechaza exportar una ruta sin distancia calculada', async () => {
    const props = propsBase()
    props.rutas = [{ ...ruta, distancia_total_km: null }]
    render(<RutasTab {...props} />)

    fireEvent.click(screen.getByRole('button', { name: /Exportar resumen de la ruta/ }))
    await waitFor(() =>
      expect(props.onMensaje).toHaveBeenCalledWith({
        tipo: 'error',
        texto: 'Calcula la ruta antes de exportar su resumen.',
      })
    )
  })
})

describe('Mapa y geocodificación', () => {
  it('MapPicker valida la búsqueda y fija un resultado de geocodificación', async () => {
    const onPick = vi.fn()
    mocks.get.mockResolvedValue({
      data: {
        resultados: [
          { direccion: 'Av. Javier Prado', descripcion: 'Surco', latitud: -12.1, longitud: -77.1 },
        ],
      },
    })
    render(<MapPicker latitud="" longitud="" onPick={onPick} />)

    fireEvent.click(screen.getByRole('button', { name: 'Buscar' }))
    expect(await screen.findByText('Escribe al menos 2 caracteres')).toBeTruthy()

    fireEvent.change(screen.getByLabelText('Buscar una direccion en el mapa'), {
      target: { value: 'Javier' },
    })
    fireEvent.click(screen.getByRole('button', { name: 'Buscar' }))
    const resultado = await screen.findByText('Av. Javier Prado')
    fireEvent.click(resultado)

    expect(onPick).toHaveBeenCalledWith(-12.1, -77.1, 'Av. Javier Prado')
    expect(screen.getByText(/Ubicacion fijada: Av. Javier Prado/)).toBeTruthy()
  })

  it('MapPicker avisa cuando el navegador no ofrece geolocalización', async () => {
    render(<MapPicker latitud="" longitud="" onPick={vi.fn()} />)

    fireEvent.click(screen.getByRole('button', { name: 'Mi ubicacion' }))
    expect(await screen.findByText('Tu navegador no soporta geolocalizacion.')).toBeTruthy()
  })

  it('MapPicker coloca el marcador cuando recibe coordenadas', () => {
    render(<MapPicker latitud="-12.1" longitud="-77" onPick={vi.fn()} />)

    expect(L.marker).toHaveBeenCalledWith([-12.1, -77], expect.anything())
  })

  it('MapPicker fija el centro por teclado y reacciona al arrastre del marcador', () => {
    const onPick = vi.fn()
    render(<MapPicker latitud="" longitud="" onPick={onPick} />)

    const region = screen.getByRole('region')
    fireEvent.keyDown(region, { key: 'Enter' })
    expect(onPick).toHaveBeenCalledWith(-12.115, -76.97)

    const manejadorArrastre = mocks.leaflet.marcador.on.mock.calls.find(
      ([evento]) => evento === 'dragend'
    )?.[1]
    manejadorArrastre({ target: { getLatLng: () => ({ lat: -12.12, lng: -77.01 }) } })
    expect(onPick).toHaveBeenCalledWith(-12.12, -77.01)
  })

  it('MapView muestra el respaldo y permite reintentar la capa', async () => {
    render(
      <MapView
        puntos={ruta.puntos}
        origenLat={ruta.origen_lat}
        origenLng={ruta.origen_lng}
        origenDireccion={ruta.origen_direccion}
      />
    )

    expect(screen.getByText(/Calculando el trazado por calles/)).toBeTruthy()
    const manejadorError = mocks.leaflet.capa.on.mock.calls.find(([e]) => e === 'tileerror')?.[1]
    manejadorError()
    manejadorError()
    manejadorError()
    manejadorError()
    expect(await screen.findByText(/No se pudo cargar el mapa base/)).toBeTruthy()

    fireEvent.click(screen.getByRole('button', { name: 'Reintentar' }))
    expect(screen.queryByText(/No se pudo cargar el mapa base/)).toBeNull()
  })

  it('MapView usa el trazado por calles cuando el proveedor responde', async () => {
    mocks.obtenerTrazadoCalles.mockResolvedValue({
      trazado: [
        [-12.115, -76.97],
        [-12.12, -77],
      ],
      distanciaKm: 4.2,
    })
    render(
      <MapView
        puntos={ruta.puntos}
        origenLat={ruta.origen_lat}
        origenLng={ruta.origen_lng}
      />
    )

    expect(await screen.findByText(/Trazado por calles: 4.2 km/)).toBeTruthy()
    expect(L.polyline).toHaveBeenCalled()
  })
})
