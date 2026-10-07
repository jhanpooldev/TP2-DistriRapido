import React, { useState, useEffect } from 'react'
import api, { extraerError } from '../api/client'
import MapView from './MapView'
import MapPicker from './MapPicker'
import RutasTab from './RutasTab'
import ImpactoTab from './ImpactoTab'
import SelectorPuntos from './SelectorPuntos'

const TABS = [
  { id: 'puntos', num: 1, label: 'Pedidos' },
  { id: 'rutas', num: 2, label: 'Rutas' },
  { id: 'mapa', num: 3, label: 'Mapa' },
  { id: 'impacto', num: 4, label: 'Impacto' },
  { id: 'vehiculos', num: 5, label: 'Vehiculos' },
]

const MAX_PUNTOS = 20

export default function Dashboard({ user, onLogout }) {
  const [activeTab, setActiveTab] = useState('puntos')
  const [puntos, setPuntos] = useState([])
  const [rutas, setRutas] = useState([])
  const [vehiculos, setVehiculos] = useState([])
  const [mensaje, setMensaje] = useState(null)
  const [selectedRoute, setSelectedRoute] = useState(null)
  const [previewRoute, setPreviewRoute] = useState(null)

  const [puntoForm, setPuntoForm] = useState({ direccion: '', latitud: '', longitud: '', peso_kg: '', destinatario: '' })
  const [optimizeForm, setOptimizeForm] = useState({ id_vehiculo: 1, punto_ids: [] })
  const [geoLoading, setGeoLoading] = useState(false)

  const mostrar = (tipo, texto) => setMensaje(texto ? { tipo, texto } : null)
  const cerrarMensaje = () => setMensaje(null)

  useEffect(() => {
    fetchPuntos()
    fetchRutas()
    fetchVehiculos()
  }, [])

  const fetchPuntos = async () => {
    try { const r = await api.get('/puntos-entrega'); setPuntos(r.data.puntos) } catch (e) { mostrar('error', extraerError(e)) }
  }
  const fetchRutas = async () => {
    try { const r = await api.get('/rutas'); setRutas(r.data) } catch (e) { mostrar('error', extraerError(e)) }
  }
  const fetchVehiculos = async () => {
    try { const r = await api.get('/vehiculos'); setVehiculos(r.data) } catch (e) { mostrar('error', extraerError(e)) }
  }

  const crearPunto = async (e) => {
    e.preventDefault()
    try {
      await api.post('/puntos-entrega', puntoForm)
      setPuntoForm({ direccion: '', latitud: '', longitud: '', peso_kg: '', destinatario: '' })
      fetchPuntos()
      mostrar('ok', 'Pedido registrado. Ya aparece en la pestaña Rutas para armar la ruta.')
    } catch (err) { mostrar('error', extraerError(err)) }
  }

  const handlePickLocation = async (lat, lng, direccionSugerida) => {
    setPuntoForm(prev => ({ ...prev, latitud: lat.toFixed(6), longitud: lng.toFixed(6) }))

    if (direccionSugerida) {
      setPuntoForm(prev => ({ ...prev, direccion: direccionSugerida }))
      return
    }

    setGeoLoading(true)
    try {
      const r = await api.get('/geocoding/reverse', { params: { latitud: lat, longitud: lng } })
      setPuntoForm(prev => ({ ...prev, direccion: r.data.direccion }))
    } catch (e) {
      mostrar('error', 'Coordenadas fijadas. No se pudo obtener la direccion automaticamente; escribela a mano.')
    } finally {
      setGeoLoading(false)
    }
  }

  const cantidadPuntos = new Set(optimizeForm.punto_ids).size
  const vehiculoSel = vehiculos.find(v => v.id_vehiculo === Number(optimizeForm.id_vehiculo))
  const pesoTotal = puntos
    .filter(p => optimizeForm.punto_ids.includes(p.id_punto))
    .reduce((suma, p) => suma + Number(p.peso_kg || 0), 0)
  const excedeCapacidad = Boolean(vehiculoSel) && pesoTotal > Number(vehiculoSel.capacidad_kg)
  const puedeCalcular = cantidadPuntos >= 2 && cantidadPuntos <= MAX_PUNTOS && !excedeCapacidad

  const optimizeRuta = async (e) => {
    e.preventDefault()
    try {
      const r = await api.post('/rutas/optimizar', optimizeForm)
      setPreviewRoute(r.data)
      setSelectedRoute(null)
      mostrar('ok', 'Ruta optimizada. Revisa el resultado en la pestaña Mapa.')
      setActiveTab('mapa')
    } catch (err) { mostrar('error', extraerError(err)) }
  }

  const confirmRuta = async (e) => {
    e.preventDefault()
    try {
      const r = await api.post('/rutas', optimizeForm)
      mostrar('ok', 'Ruta confirmada y guardada.')
      setPreviewRoute(null)
      await fetchRutas()
      setSelectedRoute(r.data)
      setActiveTab('mapa')
    } catch (err) { mostrar('error', extraerError(err)) }
  }

  const verEnMapa = (ruta) => {
    setPreviewRoute(null)
    setSelectedRoute(ruta)
    setActiveTab('mapa')
  }

  const mensajeDeValidacion = () => {
    if (cantidadPuntos === 0) return 'Agrega al menos 2 pedidos para poder calcular la ruta.'
    if (cantidadPuntos === 1) return 'Falta al menos 1 pedido: una ruta necesita 2 puntos.'
    if (cantidadPuntos > MAX_PUNTOS) return `Maximo ${MAX_PUNTOS} puntos por ruta (llevas ${cantidadPuntos}).`
    if (excedeCapacidad) return `La carga de ${pesoTotal.toFixed(1)} kg supera la capacidad de ${vehiculoSel.placa} (${vehiculoSel.capacidad_kg} kg).`
    return `${cantidadPuntos} pedidos seleccionados · ${pesoTotal.toFixed(1)} kg de ${vehiculoSel?.capacidad_kg ?? '—'} kg disponibles.`
  }

  return (
    <div className="container">
      <header className="app-header">
        <div className="app-marca">
          <div className="app-logo">E</div>
          <div>
            <h1>EcoLogistica Lima</h1>
            <div className="app-lema">Rutas de entrega mas cortas, menos combustible y menos CO2</div>
          </div>
        </div>
        <div className="app-usuario">
          <span>{user?.nombre}</span>
          <button type="button" className="btn-secondary btn-sm" onClick={onLogout}>Salir</button>
        </div>
      </header>

      {mensaje && (
        <div className={`alert alert-${mensaje.tipo === 'error' ? 'error' : mensaje.tipo === 'info' ? 'info' : 'success'}`}>
          <span>{mensaje.texto}</span>
          <button type="button" onClick={cerrarMensaje} aria-label="Cerrar aviso">&times;</button>
        </div>
      )}

      <div className="nav-tabs">
        {TABS.map(t => (
          <button
            key={t.id}
            type="button"
            className={`nav-tab ${activeTab === t.id ? 'active' : ''}`}
            onClick={() => setActiveTab(t.id)}
          >
            <span className="nav-num">{t.num}</span>
            {t.label}
          </button>
        ))}
      </div>

      {activeTab === 'puntos' && (
        <div>
          <div className="card">
            <h3>Como funciona</h3>
            <div className="como-funciona">
              <div className="paso">
                <span className="paso-num">1</span>
                <div>
                  <strong>Registra los pedidos</strong>
                  <span>Cada entrega con su direccion, peso y destinatario.</span>
                </div>
              </div>
              <div className="paso">
                <span className="paso-num">2</span>
                <div>
                  <strong>Arma la ruta</strong>
                  <span>Los pedidos se ordenan del mas cercano al mas lejano y la
                    aplicacion elige el siguiente.</span>
                </div>
              </div>
              <div className="paso">
                <span className="paso-num">3</span>
                <div>
                  <strong>Mide el ahorro</strong>
                  <span>Kilometos, minutos y kilos de CO2 que deja de emitir.</span>
                </div>
              </div>
            </div>
          </div>

          <div className="seccion-titulo">
            <h2>Registrar pedido de entrega</h2>
            <p>Marca la ubicacion en el mapa y los campos se completan solos.</p>
          </div>

          <div className="card">
            <MapPicker
              latitud={puntoForm.latitud}
              longitud={puntoForm.longitud}
              onPick={handlePickLocation}
            />
          </div>

          <form onSubmit={crearPunto} className="card">
            <div className="grid">
              <div className="form-group">
                <label>Direccion {geoLoading && '(buscando...)'}</label>
                <input
                  value={puntoForm.direccion}
                  onChange={e => setPuntoForm({ ...puntoForm, direccion: e.target.value })}
                  placeholder="Se completa al hacer click en el mapa"
                  required
                />
              </div>
              <div className="form-group">
                <label>Latitud</label>
                <input
                  type="number"
                  step="any"
                  value={puntoForm.latitud}
                  onChange={e => setPuntoForm({ ...puntoForm, latitud: e.target.value })}
                  placeholder="Ej. -12.115000"
                  required
                />
              </div>
              <div className="form-group">
                <label>Longitud</label>
                <input
                  type="number"
                  step="any"
                  value={puntoForm.longitud}
                  onChange={e => setPuntoForm({ ...puntoForm, longitud: e.target.value })}
                  placeholder="Ej. -76.970000"
                  required
                />
              </div>
              <div className="form-group">
                <label>Peso (kg)</label>
                <input
                  type="number"
                  step="0.1"
                  value={puntoForm.peso_kg}
                  onChange={e => setPuntoForm({ ...puntoForm, peso_kg: e.target.value })}
                  required
                />
              </div>
              <div className="form-group">
                <label>Destinatario</label>
                <input
                  value={puntoForm.destinatario}
                  onChange={e => setPuntoForm({ ...puntoForm, destinatario: e.target.value })}
                  required
                />
              </div>
            </div>
            <button type="submit" className="sep">Registrar pedido</button>
          </form>

          <div className="seccion-titulo">
            <h2>Pedidos registrados</h2>
            <p>{puntos.length} pedido(s) disponibles para planificar.</p>
          </div>

          <div className="tabla-envoltura">
            {puntos.length === 0 ? (
              <p className="vacio">Todavia no hay pedidos. Registra el primero con el formulario de arriba.</p>
            ) : (
              <table className="table">
                <thead>
                  <tr>
                    <th>Destinatario</th>
                    <th>Direccion</th>
                    <th className="num">Lat</th>
                    <th className="num">Lng</th>
                    <th className="num">Peso (kg)</th>
                  </tr>
                </thead>
                <tbody>
                  {puntos.map(p => (
                    <tr key={p.id_punto}>
                      <td><strong>{p.destinatario}</strong></td>
                      <td>{p.direccion}</td>
                      <td className="num">{p.latitud}</td>
                      <td className="num">{p.longitud}</td>
                      <td className="num">{p.peso_kg}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </div>
      )}

      {activeTab === 'rutas' && (
        <div>
          <div className="seccion-titulo">
            <h2>Armar una ruta</h2>
            <p>
              Elige los pedidos, deja que la aplicacion los ordene por cercania y calcula la ruta
              mas corta. Luego guardala para verla en el mapa.
            </p>
          </div>

          <SelectorPuntos
            puntos={puntos}
            seleccionados={optimizeForm.punto_ids}
            onChange={ids => setOptimizeForm({ ...optimizeForm, punto_ids: ids })}
            vehiculos={vehiculos}
            idVehiculo={optimizeForm.id_vehiculo}
            maxPuntos={MAX_PUNTOS}
          />

          <form onSubmit={optimizeRuta} className="card">
            <h3>2. Elige el vehiculo y calcula</h3>
            <div className="grid">
              <div className="form-group">
                <label>Vehiculo</label>
                <select
                  value={optimizeForm.id_vehiculo}
                  onChange={e => setOptimizeForm({ ...optimizeForm, id_vehiculo: Number(e.target.value) })}
                  required
                >
                  {vehiculos.map(v => (
                    <option key={v.id_vehiculo} value={v.id_vehiculo}>
                      {v.placa} ({v.capacidad_kg} kg)
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <p className={excedeCapacidad ? 'texto-error' : 'texto-suave'}>{mensajeDeValidacion()}</p>

            <div className="btn-grupo sep">
              <button type="button" onClick={optimizeRuta} disabled={!puedeCalcular}>
                Optimizar (simular)
              </button>
              <button type="button" className="btn-secondary" onClick={confirmRuta} disabled={!puedeCalcular}>
                Confirmar y guardar
              </button>
            </div>
          </form>

          <RutasTab
            rutas={rutas}
            puntos={puntos}
            vehiculos={vehiculos}
            onVerMapa={verEnMapa}
            onCambiado={setRutas}
            onMensaje={(m) => mostrar(m.tipo, m.texto)}
          />
        </div>
      )}

      {activeTab === 'impacto' && (
        <ImpactoTab rutas={rutas} onVerMapa={verEnMapa} />
      )}

      {activeTab === 'mapa' && (
        <div>
          <div className="seccion-titulo">
            <h2>Ruta en el mapa</h2>
            <p>Comprueba el orden de entrega antes de enviarlo al conductor.</p>
          </div>

          <div className="card">
            <h3>Seleccionar ruta</h3>
            {rutas.length === 0 ? (
              <p className="texto-suave">
                No hay rutas guardadas. Armala primero en la pestaña <strong>Rutas</strong>.
              </p>
            ) : (
              <select
                value={selectedRoute?.id_ruta || ''}
                onChange={e => {
                  const ruta = rutas.find(r => r.id_ruta === e.target.value)
                  setSelectedRoute(ruta || null)
                  setPreviewRoute(null)
                }}
              >
                <option value="">-- Seleccionar una ruta --</option>
                {rutas.map(r => (
                  <option key={r.id_ruta} value={r.id_ruta}>
                    {r.id_ruta.slice(0, 8)}... · {r.distancia_total_km} km · {r.estado}
                  </option>
                ))}
              </select>
            )}
          </div>

          {previewRoute && (
            <div className="alert alert-info">
              Vista previa: esta ruta todavia no esta guardada. Pulsa
              <strong> Confirmar y guardar </strong> en la pestaña Rutas para conservarla.
            </div>
          )}

          {(previewRoute || selectedRoute) && (() => {
            const ruta = previewRoute || selectedRoute
            return (
              <div className="card">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: 14, flexWrap: 'wrap', marginBottom: 16 }}>
                  <h2 style={{ margin: 0 }}>
                    {previewRoute ? 'Ruta optimizada (simulacion)' : `Ruta ${selectedRoute.id_ruta.slice(0, 8)}...`}
                  </h2>
                  <div className="grid" style={{ margin: 0, gridTemplateColumns: 'repeat(3, minmax(80px, auto))', gap: 18 }}>
                    <div>
                      <div className="stat-value">{ruta.distancia_total_km}</div>
                      <div className="stat-label">km</div>
                    </div>
                    <div>
                      <div className="stat-value">{ruta.tiempo_estimado_min}</div>
                      <div className="stat-label">min</div>
                    </div>
                    <div>
                      <div className="stat-value">{ruta.co2_estimado_kg}</div>
                      <div className="stat-label">kg CO2</div>
                    </div>
                  </div>
                </div>

                <MapView puntos={ruta.puntos} center={[-12.115, -76.97]} zoom={12} />

                <h3 className="sep">Orden de entrega</h3>
                <div className="tabla-envoltura">
                  <table className="table">
                    <thead>
                      <tr>
                        <th>#</th>
                        <th>Direccion</th>
                        <th>Destinatario</th>
                        <th className="num">Peso (kg)</th>
                      </tr>
                    </thead>
                    <tbody>
                      {ruta.puntos.map((p, i) => (
                        <tr key={p.id_punto}>
                          <td><span className="sel-orden">{i + 1}</span></td>
                          <td>{p.direccion}</td>
                          <td>{p.destinatario}</td>
                          <td className="num">{p.peso_kg}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )
          })()}
        </div>
      )}

      {activeTab === 'vehiculos' && (
        <div>
          <div className="seccion-titulo">
            <h2>Vehiculos</h2>
            <p>De aqui salen la capacidad, el consumo y el factor de emision usados en cada calculo.</p>
          </div>
          <div className="tabla-envoltura">
            <table className="table">
              <thead>
                <tr>
                  <th>Placa</th>
                  <th className="num">Capacidad (kg)</th>
                  <th className="num">Consumo (L/km)</th>
                  <th className="num">Velocidad (km/h)</th>
                  <th>Combustible</th>
                </tr>
              </thead>
              <tbody>
                {vehiculos.map(v => (
                  <tr key={v.id_vehiculo}>
                    <td><strong>{v.placa}</strong></td>
                    <td className="num">{v.capacidad_kg}</td>
                    <td className="num">{v.consumo_litros_km}</td>
                    <td className="num">{v.velocidad_promedio_kmh}</td>
                    <td><span className="badge badge-info">{v.tipo_combustible}</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}
