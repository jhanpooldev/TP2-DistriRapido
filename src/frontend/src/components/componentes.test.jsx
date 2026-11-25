import { describe, expect, it } from 'vitest'
import { renderToStaticMarkup } from 'react-dom/server'

import Dashboard from './Dashboard'
import ImpactoTab from './ImpactoTab'
import IndicadoresTab from './IndicadoresTab'
import Login from './Login'
import Paginacion from './Paginacion'
import RutasTab from './RutasTab'
import SelectorPuntos from './SelectorPuntos'

const punto = (id, destinatario, peso) => ({
  id_punto: id,
  direccion: `Direccion ${id}`,
  destinatario,
  latitud: -12.1,
  longitud: -77.0,
  peso_kg: peso,
})

describe('componentes del panel (renderizado en servidor)', () => {
  it('Paginacion resume un solo bloque sin controles', () => {
    const html = renderToStaticMarkup(
      <Paginacion page={1} pages={1} total={25} etiqueta="pedidos" />
    )
    expect(html).toContain('25 pedidos en total.')
    expect(html).not.toContain('Siguiente')
  })

  it('Paginacion expone navegacion y pagina actual con varios bloques', () => {
    const html = renderToStaticMarkup(
      <Paginacion page={2} pages={3} total={36} etiqueta="pedidos" />
    )
    expect(html).toContain('Pagina 2 de 3')
    expect(html).toContain('Anterior')
    expect(html).toContain('Siguiente')
    expect(html).toContain('Paginacion de pedidos')
  })

  it('Login muestra el formulario, el aviso y los campos obligatorios', () => {
    const html = renderToStaticMarkup(
      <Login onLogin={() => {}} aviso="Sesion finalizada" />
    )
    expect(html).toContain('EcoLogistica Lima')
    expect(html).toContain('Sesion finalizada')
    expect(html).toContain('id="correo"')
    expect(html).toContain('id="password"')
    expect(html).toContain('Ingresar')
    expect(html).not.toContain('Credenciales invalidas')
  })

  it('IndicadoresTab muestra el estado de carga antes de resolver la API', () => {
    const html = renderToStaticMarkup(<IndicadoresTab />)
    expect(html).toContain('Cargando indicadores...')
    expect(html).toContain('role="status"')
  })

  it('SelectorPuntos lista los pedidos disponibles y la carga del vehiculo', () => {
    const puntos = [punto('a', 'Ana', 5), punto('b', 'Beto', 7)]
    const html = renderToStaticMarkup(
      <SelectorPuntos
        puntos={puntos}
        seleccionados={[]}
        onChange={() => {}}
        vehiculos={[{ id_vehiculo: 1, placa: 'ABC-123', capacidad_kg: 100 }]}
        idVehiculo={1}
      />
    )
    expect(html).toContain('0 de 2 pedidos')
    expect(html).toContain('Ana')
    expect(html).toContain('Beto')
    expect(html).toContain('Siguiente mas cercano')
    expect(html).toContain('Carga:')
  })

  it('SelectorPuntos avisa cuando no hay pedidos registrados', () => {
    const html = renderToStaticMarkup(
      <SelectorPuntos puntos={[]} seleccionados={[]} onChange={() => {}} />
    )
    expect(html).toContain('Todavia no hay pedidos registrados')
    expect(html).toContain('Aun no agregaste ningun pedido')
  })

  it('ImpactoTab explica que falta una ruta guardada', () => {
    const html = renderToStaticMarkup(<ImpactoTab rutas={[]} onVerMapa={() => {}} />)
    expect(html).toContain('Impacto ambiental')
    expect(html).toContain('Todavia no hay rutas guardadas')
  })

  it('ImpactoTab ofrece el selector cuando hay rutas', () => {
    const ruta = {
      id_ruta: 'ruta-1',
      fecha_generacion: '2026-11-19T00:00:00Z',
      co2_estimado_kg: 1.2,
    }
    const html = renderToStaticMarkup(<ImpactoTab rutas={[ruta]} onVerMapa={() => {}} />)
    expect(html).toContain('id="ruta-impacto"')
    expect(html).toContain('Selecciona una ruta')
  })

  it('RutasTab muestra el estado vacio sin rutas guardadas', () => {
    const html = renderToStaticMarkup(
      <RutasTab
        rutas={[]}
        puntos={[]}
        vehiculos={[]}
        onVerMapa={() => {}}
        onCambiado={() => {}}
        onMensaje={() => {}}
      />
    )
    expect(html).toContain('Todavia no guardaste ninguna ruta')
  })

  it('Dashboard del operador muestra las seis secciones y el formulario de pedidos', () => {
    const html = renderToStaticMarkup(
      <Dashboard user={{ nombre: 'Operador Demo', rol: { nombre: 'Operador Logistico' } }} onLogout={() => {}} />
    )
    expect(html).toContain('Operador Demo')
    expect(html).toContain('Registrar pedido de entrega')
    expect(html).toContain('id="tab-indicadores"')
    expect(html).toContain('id="tab-vehiculos"')
    expect(html).toContain('Saltar al contenido principal')
  })

  it('Dashboard del gerente oculta vehiculos y formularios de escritura', () => {
    const html = renderToStaticMarkup(
      <Dashboard user={{ nombre: 'Gerente', rol: { nombre: 'Gerente' } }} onLogout={() => {}} />
    )
    expect(html).toContain('acceso de solo lectura a pedidos y rutas')
    expect(html).not.toContain('id="tab-vehiculos"')
    expect(html).not.toContain('Registrar pedido de entrega')
    expect(html).toContain('id="tab-indicadores"')
  })
})
