import React, { useState } from 'react'
import api, { extraerError } from '../api/client'

const ESTADOS = ['Confirmada', 'Borrador', 'En curso', 'Completada']

export default function RutasTab({ rutas, puntos, vehiculos, onVerMapa, onCambiado, onMensaje }) {
  const [filtros, setFiltros] = useState({ desde: '', hasta: '', estado: '' })
  const [editando, setEditando] = useState(null)
  const [formEdicion, setFormEdicion] = useState({ id_vehiculo: 1, punto_ids: [] })
  const [buscando, setBuscando] = useState(false)

  const hayFiltros = Boolean(filtros.desde || filtros.hasta || filtros.estado)

  const filtrar = async (e) => {
    e?.preventDefault()
    setBuscando(true)
    try {
      const params = {}
      if (filtros.desde) params.desde = filtros.desde
      if (filtros.hasta) params.hasta = filtros.hasta
      if (filtros.estado) params.estado = filtros.estado
      const r = await api.get('/rutas', { params })
      onCambiado(r.data)
      onMensaje(
        r.data.length === 0
          ? { tipo: 'info', texto: 'Sin resultados: ningun registro coincide con el filtro aplicado.' }
          : { tipo: 'ok', texto: `${r.data.length} ruta(s) encontradas.` }
      )
    } catch (e) {
      onMensaje({ tipo: 'error', texto: extraerError(e, 'No se pudo filtrar las rutas') })
    } finally {
      setBuscando(false)
    }
  }

  const limpiar = async () => {
    setFiltros({ desde: '', hasta: '', estado: '' })
    try {
      const r = await api.get('/rutas')
      onCambiado(r.data)
      onMensaje({ tipo: 'ok', texto: 'Filtros limpiados.' })
    } catch (e) {
      onMensaje({ tipo: 'error', texto: extraerError(e, 'No se pudo recargar las rutas') })
    }
  }

  const iniciarEdicion = (ruta) => {
    setEditando(ruta.id_ruta)
    setFormEdicion({
      id_vehiculo: ruta.id_vehiculo,
      punto_ids: ruta.puntos.map(p => p.id_punto),
    })
  }

  const cancelarEdicion = () => {
    setEditando(null)
    setFormEdicion({ id_vehiculo: 1, punto_ids: [] })
  }

  const guardarEdicion = async (e) => {
    e.preventDefault()
    try {
      await api.put(`/rutas/${editando}`, formEdicion)
      onMensaje({ tipo: 'ok', texto: 'Ruta actualizada y recalculada con los puntos seleccionados.' })
      cancelarEdicion()
      const r = await api.get('/rutas')
      onCambiado(r.data)
    } catch (err) {
      onMensaje({ tipo: 'error', texto: extraerError(err, 'No se pudo actualizar la ruta') })
    }
  }

  const eliminar = async (ruta) => {
    const confirmar = window.confirm(
      `Eliminar la ruta ${ruta.id_ruta.slice(0, 8)}...? Esta accion no se puede deshacer.`
    )
    if (!confirmar) return

    try {
      await api.delete(`/rutas/${ruta.id_ruta}`)
      onMensaje({ tipo: 'ok', texto: 'Ruta eliminada.' })
      const r = await api.get('/rutas')
      onCambiado(r.data)
    } catch (err) {
      onMensaje({ tipo: 'error', texto: extraerError(err, 'No se pudo eliminar la ruta') })
    }
  }

  const capacidadVehiculo = vehiculos.find(v => v.id_vehiculo === Number(formEdicion.id_vehiculo))
  const pesoSeleccionado = puntos
    .filter(p => formEdicion.punto_ids.includes(p.id_punto))
    .reduce((suma, p) => suma + Number(p.peso_kg || 0), 0)
  const excedeCapacidad = capacidadVehiculo && pesoSeleccionado > Number(capacidadVehiculo.capacidad_kg)
  const edicionValida = new Set(formEdicion.punto_ids).size >= 2 && !excedeCapacidad

  return (
    <div>
      <h2>Rutas guardadas</h2>

      <form onSubmit={filtrar} className="card" style={{ marginBottom: '20px' }}>
        <h3>Buscar rutas</h3>
        <div className="grid">
          <div className="form-group">
            <label>Desde</label>
            <input
              type="date"
              value={filtros.desde}
              onChange={e => setFiltros({ ...filtros, desde: e.target.value })}
            />
          </div>
          <div className="form-group">
            <label>Hasta</label>
            <input
              type="date"
              value={filtros.hasta}
              onChange={e => setFiltros({ ...filtros, hasta: e.target.value })}
            />
          </div>
          <div className="form-group">
            <label>Estado</label>
            <select
              value={filtros.estado}
              onChange={e => setFiltros({ ...filtros, estado: e.target.value })}
            >
              <option value="">Todos</option>
              {ESTADOS.map(s => (
                <option key={s} value={s}>{s}</option>
              ))}
            </select>
          </div>
        </div>
        <div style={{ display: 'flex', gap: '10px', marginTop: '10px' }}>
          <button type="submit" disabled={buscando}>
            {buscando ? 'Buscando...' : 'Aplicar filtro'}
          </button>
          <button type="button" className="btn-secondary" onClick={limpiar} disabled={!hayFiltros}>
            Limpiar
          </button>
        </div>
      </form>

      {hayFiltros && rutas.length === 0 ? (
        <div className="alert alert-success">
          Sin resultados. Ninguna ruta coincide con el filtro aplicado. Prueba con otro rango de
          fechas o estado.
        </div>
      ) : (
        <div className="card">
          <table className="table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Fecha</th>
                <th>Distancia (km)</th>
                <th>CO₂ (kg)</th>
                <th>Ahorro CO₂</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {rutas.map(r => (
                <React.Fragment key={r.id_ruta}>
                  <tr>
                    <td>{r.id_ruta.slice(0, 8)}...</td>
                    <td>{new Date(r.fecha_generacion).toLocaleString()}</td>
                    <td>{r.distancia_total_km}</td>
                    <td>{r.co2_estimado_kg}</td>
                    <td>
                      {r.sin_reduccion_significativa ? (
                        <span style={{ color: '#666' }}>Sin reducción</span>
                      ) : (
                        <span style={{ color: '#1e8449', fontWeight: 'bold' }}>{r.ahorro_co2_pct}%</span>
                      )}
                    </td>
                    <td><span className={`badge ${r.estado === 'Confirmada' ? 'badge-success' : 'badge-warning'}`}>{r.estado}</span></td>
                    <td>
                      <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                        <button type="button" className="btn-secondary" onClick={() => onVerMapa(r)}>
                          Mapa
                        </button>
                        <button type="button" className="btn-secondary" onClick={() => iniciarEdicion(r)}>
                          Editar
                        </button>
                        <button type="button" className="btn-secondary" onClick={() => eliminar(r)}>
                          Eliminar
                        </button>
                      </div>
                    </td>
                  </tr>

                  {editando === r.id_ruta && (
                    <tr>
                      <td colSpan={7} style={{ background: '#f7f9fa' }}>
                        <form onSubmit={guardarEdicion}>
                          <h4 style={{ margin: '10px 0' }}>Editar puntos de la ruta</h4>
                          <div className="grid">
                            <div className="form-group">
                              <label>Vehiculo</label>
                              <select
                                value={formEdicion.id_vehiculo}
                                onChange={e => setFormEdicion({ ...formEdicion, id_vehiculo: Number(e.target.value) })}
                              >
                                {vehiculos.map(v => (
                                  <option key={v.id_vehiculo} value={v.id_vehiculo}>
                                    {v.placa} ({v.capacidad_kg} kg)
                                  </option>
                                ))}
                              </select>
                            </div>
                            <div className="form-group">
                              <label>Puntos de la ruta</label>
                              <select
                                multiple
                                value={formEdicion.punto_ids}
                                onChange={e => {
                                  const selected = Array.from(e.target.selectedOptions).map(o => o.value)
                                  setFormEdicion({ ...formEdicion, punto_ids: selected })
                                }}
                                style={{ height: '150px' }}
                              >
                                {puntos.map(p => (
                                  <option key={p.id_punto} value={p.id_punto}>
                                    {p.direccion} ({p.peso_kg} kg)
                                  </option>
                                ))}
                              </select>
                            </div>
                          </div>

                          <p style={{ fontSize: '13px', color: excedeCapacidad ? '#c0392b' : '#555' }}>
                            Carga seleccionada: {pesoSeleccionado.toFixed(1)} kg
                            {capacidadVehiculo ? ` / ${capacidadVehiculo.capacidad_kg} kg disponibles` : ''}
                            {excedeCapacidad ? ' — supera la capacidad del vehiculo.' : ''}
                          </p>

                          <div style={{ display: 'flex', gap: '10px' }}>
                            <button type="submit" disabled={!edicionValida}>
                              Guardar y recalcular
                            </button>
                            <button type="button" className="btn-secondary" onClick={cancelarEdicion}>
                              Cancelar
                            </button>
                          </div>
                        </form>
                      </td>
                    </tr>
                  )}
                </React.Fragment>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}