import React, { useState, useEffect } from 'react'
import api, { extraerError } from '../api/client'
import MapView from './MapView'
import MapPicker from './MapPicker'
import RutasTab from './RutasTab'
import ImpactoTab from './ImpactoTab'

export default function Dashboard({ user, onLogout }) {
  const [activeTab, setActiveTab] = useState('puntos')
  const [puntos, setPuntos] = useState([])
  const [rutas, setRutas] = useState([])
  const [vehiculos, setVehiculos] = useState([])
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [selectedRoute, setSelectedRoute] = useState(null)
  const [previewRoute, setPreviewRoute] = useState(null)

  const [puntoForm, setPuntoForm] = useState({ direccion: '', latitud: '', longitud: '', peso_kg: '', destinatario: '' })
  const [optimizeForm, setOptimizeForm] = useState({ id_vehiculo: 1, punto_ids: [] })
  const [geoLoading, setGeoLoading] = useState(false)

  const mostrar = (tipo, texto) => {
    if (tipo === 'error') {
      setError(texto)
      setSuccess('')
    } else {
      setSuccess(texto)
      setError('')
    }
  }

  useEffect(() => {
    fetchPuntos()
    fetchRutas()
    fetchVehiculos()
  }, [])

  const fetchPuntos = async () => {
    try { const r = await api.get('/puntos-entrega'); setPuntos(r.data.puntos) } catch (e) { setError(extraerError(e)) }
  }
  const fetchRutas = async () => {
    try { const r = await api.get('/rutas'); setRutas(r.data) } catch (e) { setError(extraerError(e)) }
  }
  const fetchVehiculos = async () => {
    try { const r = await api.get('/vehiculos'); setVehiculos(r.data) } catch (e) { setError(extraerError(e)) }
  }

  const crearPunto = async (e) => {
    e.preventDefault()
    try {
      await api.post('/puntos-entrega', puntoForm)
      setPuntoForm({ direccion: '', latitud: '', longitud: '', peso_kg: '', destinatario: '' })
      fetchPuntos()
      mostrar('ok', 'Punto creado')
    } catch (err) { mostrar('error', extraerError(err)) }
  }

  const handlePickLocation = async (lat, lng, direccionSugerida) => {
    setPuntoForm(prev => ({ ...prev, latitud: lat.toFixed(6), longitud: lng.toFixed(6) }))

    if (direccionSugerida) {
      setPuntoForm(prev => ({ ...prev, direccion: direccionSugerida }))
      mostrar('ok', '')
      return
    }

    setGeoLoading(true)
    try {
      const r = await api.get('/geocoding/reverse', { params: { latitud: lat, longitud: lng } })
      setPuntoForm(prev => ({ ...prev, direccion: r.data.direccion }))
      mostrar('ok', '')
    } catch (e) {
      mostrar('error', 'Coordenadas fijadas. No se pudo obtener la direccion automaticamente; escribela a mano.')
    } finally {
      setGeoLoading(false)
    }
  }

  const cantidadPuntos = new Set(optimizeForm.punto_ids).size
  const maxPuntos = 20
  const exceedsMax = cantidadPuntos > maxPuntos
  const vehiculoSel = vehiculos.find(v => v.id_vehiculo === Number(optimizeForm.id_vehiculo))
  const pesoTotal = puntos
    .filter(p => optimizeForm.punto_ids.includes(p.id_punto))
    .reduce((suma, p) => suma + Number(p.peso_kg || 0), 0)
  const excedeCapacidad = Boolean(vehiculoSel) && pesoTotal > Number(vehiculoSel.capacidad_kg)
  const puedeCalcular = cantidadPuntos >= 2 && !exceedsMax && !excedeCapacidad

  const optimizeRuta = async (e) => {
    e.preventDefault()
    try {
      const r = await api.post('/rutas/optimizar', optimizeForm)
      setPreviewRoute(r.data)
      setSelectedRoute(null)
      setSuccess('Ruta optimizada. Revisa el resultado en la pestaña Mapa.')
      setActiveTab('mapa')
    } catch (err) { mostrar('error', extraerError(err)) }
  }

  const confirmRuta = async (e) => {
    e.preventDefault()
    try {
      const r = await api.post('/rutas', optimizeForm)
      setSuccess('Ruta confirmada y guardada')
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

  return (
    <div className="container">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h1>EcoLogística Lima</h1>
        <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
          <span>Bienvenido, {user?.nombre}</span>
          <button className="btn-secondary" onClick={onLogout}>Salir</button>
        </div>
      </div>

      {error && <div className="alert alert-error">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}

      <div className="nav-tabs">
        <button className={`nav-tab ${activeTab === 'puntos' ? 'active' : ''}`} onClick={() => setActiveTab('puntos')}>
          Puntos de Entrega
        </button>
        <button className={`nav-tab ${activeTab === 'rutas' ? 'active' : ''}`} onClick={() => setActiveTab('rutas')}>
          Rutas
        </button>
        <button className={`nav-tab ${activeTab === 'mapa' ? 'active' : ''}`} onClick={() => setActiveTab('mapa')}>
          Mapa
        </button>
        <button className={`nav-tab ${activeTab === 'impacto' ? 'active' : ''}`} onClick={() => setActiveTab('impacto')}>
          Impacto Ambiental
        </button>
        <button className={`nav-tab ${activeTab === 'vehiculos' ? 'active' : ''}`} onClick={() => setActiveTab('vehiculos')}>
          Vehículos
        </button>
      </div>

      {activeTab === 'puntos' && (
        <div>
          <h2>Registrar Punto de Entrega</h2>
          <p style={{ color: '#555', marginBottom: '15px' }}>
            Marca la ubicacion en el mapa y los campos se completan automaticamente.
          </p>
          <div className="card" style={{ marginBottom: '20px' }}>
            <MapPicker
              latitud={puntoForm.latitud}
              longitud={puntoForm.longitud}
              onPick={handlePickLocation}
            />
          </div>

          <form onSubmit={crearPunto} className="card" style={{ marginBottom: '30px' }}>
            <div className="grid">
              <div className="form-group">
                <label>Direccion {geoLoading && '(buscando...)'}</label>
                <input
                  value={puntoForm.direccion}
                  onChange={e => setPuntoForm({...puntoForm, direccion: e.target.value})}
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
                  onChange={e => setPuntoForm({...puntoForm, latitud: e.target.value})}
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
                  onChange={e => setPuntoForm({...puntoForm, longitud: e.target.value})}
                  placeholder="Ej. -76.970000"
                  required
                />
              </div>
              <div className="form-group">
                <label>Peso (kg)</label>
                <input type="number" step="0.1" value={puntoForm.peso_kg} onChange={e => setPuntoForm({...puntoForm, peso_kg: e.target.value})} required />
              </div>
              <div className="form-group">
                <label>Destinatario</label>
                <input value={puntoForm.destinatario} onChange={e => setPuntoForm({...puntoForm, destinatario: e.target.value})} required />
              </div>
            </div>
            <button type="submit" style={{ marginTop: '10px' }}>Registrar Punto</button>
          </form>

          <h2>Puntos Registrados</h2>
          <div className="card">
            <table className="table">
              <thead><tr><th>Dirección</th><th>Lat</th><th>Lng</th><th>Peso (kg)</th><th>Destinatario</th></tr></thead>
              <tbody>
                {puntos.map(p => (
                  <tr key={p.id_punto}>
                    <td>{p.direccion}</td><td>{p.latitud}</td><td>{p.longitud}</td>
                    <td>{p.peso_kg}</td><td>{p.destinatario}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {activeTab === 'rutas' && (
        <div>
          <h2>Optimizar Ruta</h2>
          <form onSubmit={optimizeRuta} className="card" style={{ marginBottom: '20px' }}>
            <div className="grid">
              <div className="form-group">
                <label>Vehículo</label>
                <select value={optimizeForm.id_vehiculo} onChange={e => setOptimizeForm({...optimizeForm, id_vehiculo: Number(e.target.value)})} required>
                  {vehiculos.map(v => <option key={v.id_vehiculo} value={v.id_vehiculo}>{v.placa} ({v.capacidad_kg} kg)</option>)}
                </select>
              </div>
              <div className="form-group">
                <label>Puntos a incluir</label>
                <select multiple value={optimizeForm.punto_ids} onChange={e => {
                  const selected = Array.from(e.target.selectedOptions).map(o => o.value)
                  setOptimizeForm({...optimizeForm, punto_ids: selected})
                }} style={{ height: '120px' }} required>
                  {puntos.map(p => <option key={p.id_punto} value={p.id_punto}>{p.direccion} ({p.peso_kg} kg)</option>)}
                </select>
              </div>
            </div>
            <div style={{ display: 'flex', gap: '10px', alignItems: 'center', flexWrap: 'wrap' }}>
              <button type="button" onClick={optimizeRuta} disabled={!puedeCalcular}>Optimizar (Simular)</button>
              <button type="button" onClick={confirmRuta} className="btn-secondary" disabled={!puedeCalcular}>Confirmar y Guardar</button>
              <span style={{ fontSize: '13px', color: excedeCapacidad ? '#c0392b' : '#555' }}>
                {cantidadPuntos === 0
                  ? 'Selecciona al menos 2 puntos.'
                  : exceedsMax
                    ? `Maximo ${maxPuntos} puntos por ruta (tienes ${cantidadPuntos}).`
                    : excedeCapacidad
                      ? `Peso ${pesoTotal.toFixed(1)} kg supera la capacidad de ${vehiculoSel.placa} (${vehiculoSel.capacidad_kg} kg).`
                      : `${cantidadPuntos} punto(s) seleccionado(s) - ${pesoTotal.toFixed(1)} kg.`}
              </span>
            </div>
          </form>

          <RutasTab
            rutas={rutas}
            puntos={puntos}
            vehiculos={vehiculos}
            onVerMapa={verEnMapa}
            onCambiado={setRutas}
            onMensaje={mostrar}
          />
        </div>
      )}

      {activeTab === 'impacto' && (
        <ImpactoTab rutas={rutas} onVerMapa={verEnMapa} />
      )}

      {activeTab === 'mapa' && (
        <div>
          <h2>Visualización de Ruta en Mapa</h2>
          <div className="card" style={{ marginBottom: '20px' }}>
            <h3>Seleccionar Ruta</h3>
            {rutas.length === 0 ? (
              <p style={{ color: '#666' }}>No hay rutas guardadas. Crea una ruta en la pestaña "Rutas" primero.</p>
            ) : (
              <select
                value={selectedRoute?.id_ruta || ''}
                onChange={e => {
                  const ruta = rutas.find(r => r.id_ruta === e.target.value)
                  setSelectedRoute(ruta || null)
                  setPreviewRoute(null)
                }}
                style={{ maxWidth: '400px', width: '100%', padding: '8px', border: '1px solid #ccc', borderRadius: '4px' }}
              >
                <option value="">-- Seleccionar una ruta --</option>
                {rutas.map(r => (
                  <option key={r.id_ruta} value={r.id_ruta}>
                    {r.id_ruta.slice(0, 8)}... - {r.distancia_total_km} km - {r.estado}
                  </option>
                ))}
              </select>
            )}
          </div>

          {previewRoute && (
            <div className="alert alert-success">
              Vista previa de la ruta optimizada (simulación, no guardada). Usa "Confirmar y Guardar" en la pestaña Rutas para persistirla.
            </div>
          )}

          {(previewRoute || selectedRoute) && (() => {
            const ruta = previewRoute || selectedRoute
            return (
              <div className="card" style={{ marginTop: '20px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px', flexWrap: 'wrap', gap: '12px' }}>
                  <h2 style={{ margin: 0 }}>
                    {previewRoute ? 'Ruta Optimizada (Simulación)' : `Ruta Guardada ${selectedRoute.id_ruta.slice(0, 8)}...`}
                  </h2>
                  <div style={{ display: 'flex', gap: '20px' }}>
                    <div>
                      <div className="stat-value">{ruta.distancia_total_km} km</div>
                      <div className="stat-label">Distancia</div>
                    </div>
                    <div>
                      <div className="stat-value">{ruta.tiempo_estimado_min} min</div>
                      <div className="stat-label">Tiempo</div>
                    </div>
                    <div>
                      <div className="stat-value">{ruta.co2_estimado_kg} kg</div>
                      <div className="stat-label">CO₂</div>
                    </div>
                  </div>
                </div>

                <MapView puntos={ruta.puntos} center={[-12.115, -76.97]} zoom={12} />

                <h3 style={{ marginTop: '20px' }}>Orden de entrega</h3>
                <table className="table">
                  <thead><tr><th>#</th><th>Dirección</th><th>Destinatario</th><th>Peso (kg)</th></tr></thead>
                  <tbody>
                    {ruta.puntos.map((p, i) => (
                      <tr key={p.id_punto}>
                        <td>{i + 1}</td>
                        <td>{p.direccion}</td>
                        <td>{p.destinatario}</td>
                        <td>{p.peso_kg}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )
          })()}
        </div>
      )}

      {activeTab === 'vehiculos' && (
        <div>
          <h2>Vehículos</h2>
          <div className="card">
            <table className="table">
              <thead><tr><th>Placa</th><th>Capacidad (kg)</th><th>Consumo (L/km)</th><th>Velocidad (km/h)</th><th>Combustible</th></tr></thead>
              <tbody>
                {vehiculos.map(v => (
                  <tr key={v.id_vehiculo}>
                    <td>{v.placa}</td><td>{v.capacidad_kg}</td><td>{v.consumo_litros_km}</td>
                    <td>{v.velocidad_promedio_kmh}</td><td>{v.tipo_combustible}</td>
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
