import React, { useState } from 'react'
import api, { extraerError } from '../api/client'
import SelectorPuntos from './SelectorPuntos'

const ESTADOS = ['Confirmada', 'Borrador', 'En curso', 'Completada']

export default function RutasTab({ rutas, puntos, vehiculos, onVerMapa, onCambiado, onMensaje }) {
  const [filtros, setFiltros] = useState({ desde: '', hasta: '', estado: '' })
  const [editando, setEditando] = useState(null)
  const [formEdicion, setFormEdicion] = useState({ id_vehiculo: 1, punto_ids: [] })
  const [buscando, setBuscando] = useState(false)

  const hayFiltros = Boolean(filtros.desde || filtros.hasta || filtros.estado)
  const rutaEditando = rutas.find(r => r.id_ruta === editando) || null

  const recargar = async (params = {}) => {
    const r = await api.get('/rutas', { params })
    onCambiado(r.data)
    return r.data
  }

  const filtrar = async (e) => {
    e?.preventDefault()
    setBuscando(true)
    try {
      const params = {}
      if (filtros.desde) params.desde = filtros.desde
      if (filtros.hasta) params.hasta = filtros.hasta
      if (filtros.estado) params.estado = filtros.estado
      const resultados = await recargar(params)
      onMensaje(
        resultados.length === 0
          ? { tipo: 'info', texto: 'Ninguna ruta coincide con el filtro aplicado.' }
          : { tipo: 'ok', texto: `${resultados.length} ruta(s) encontrada(s).` }
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
      await recargar()
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
    window.scrollTo({ top: 0, behavior: 'smooth' })
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
      await recargar()
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
      if (editando === ruta.id_ruta) cancelarEdicion()
      onMensaje({ tipo: 'ok', texto: 'Ruta eliminada.' })
      await recargar()
    } catch (err) {
      onMensaje({ tipo: 'error', texto: extraerError(err, 'No se pudo eliminar la ruta') })
    }
  }

  const vehiculoEdicion = vehiculos.find(v => v.id_vehiculo === Number(formEdicion.id_vehiculo))
  const pesoEdicion = puntos
    .filter(p => formEdicion.punto_ids.includes(p.id_punto))
    .reduce((suma, p) => suma + Number(p.peso_kg || 0), 0)
  const excedeEdicion = vehiculoEdicion && pesoEdicion > Number(vehiculoEdicion.capacidad_kg)
  const edicionValida = new Set(formEdicion.punto_ids).size >= 2 && !excedeEdicion

  const estadoBadge = (estado) => {
    if (estado === 'Confirmada') return 'badge-success'
    if (estado === 'Completada') return 'badge-info'
    if (estado === 'En curso') return 'badge-warning'
    return 'badge-muted'
  }

  return (
    <div>
      <div className="seccion-titulo">
        <h2>Rutas guardadas</h2>
        <p>Busca por fecha o estado, o vuelve a editar una ruta ya creada.</p>
      </div>

      {rutaEditando && (
        <form onSubmit={guardarEdicion} className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', gap: 12, flexWrap: 'wrap' }}>
            <h3>Editando la ruta {rutaEditando.id_ruta.slice(0, 8)}...</h3>
            <span className="texto-suave">Pulsa "Guardar y recalcular" para confirmar</span>
          </div>

          <SelectorPuntos
            puntos={puntos}
            seleccionados={formEdicion.punto_ids}
            onChange={ids => setFormEdicion({ ...formEdicion, punto_ids: ids })}
            vehiculos={vehiculos}
            idVehiculo={formEdicion.id_vehiculo}
          />

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
          </div>

          <p className={excedeEdicion ? 'texto-error' : 'texto-suave'}>
            Carga seleccionada: {pesoEdicion.toFixed(1)} kg
            {vehiculoEdicion ? ` / ${vehiculoEdicion.capacidad_kg} kg disponibles` : ''}
            {excedeEdicion ? ' — supera la capacidad del vehiculo.' : ''}
          </p>

          <div className="btn-grupo sep">
            <button type="submit" disabled={!edicionValida}>Guardar y recalcular</button>
            <button type="button" className="btn-secondary" onClick={cancelarEdicion}>Cancelar</button>
          </div>
        </form>
      )}

      <form onSubmit={filtrar} className="card">
        <h3>Buscar rutas</h3>
        <div className="grid">
          <div className="form-group">
            <label htmlFor="filtro-desde">Desde</label>
            <input
              id="filtro-desde"
              type="date"
              value={filtros.desde}
              onChange={e => setFiltros({ ...filtros, desde: e.target.value })}
            />
          </div>
          <div className="form-group">
            <label htmlFor="filtro-hasta">Hasta</label>
            <input
              id="filtro-hasta"
              type="date"
              value={filtros.hasta}
              onChange={e => setFiltros({ ...filtros, hasta: e.target.value })}
            />
          </div>
          <div className="form-group">
            <label htmlFor="filtro-estado">Estado</label>
            <select
              id="filtro-estado"
              value={filtros.estado}
              onChange={e => setFiltros({ ...filtros, estado: e.target.value })}
            >
              <option value="">Todos</option>
              {ESTADOS.map(s => <option key={s} value={s}>{s}</option>)}
            </select>
          </div>
        </div>
        <div className="btn-grupo">
          <button type="submit" disabled={buscando}>{buscando ? 'Buscando...' : 'Aplicar filtro'}</button>
          <button type="button" className="btn-secondary" onClick={limpiar} disabled={!hayFiltros}>
            Limpiar
          </button>
        </div>
      </form>

      <div className="tabla-envoltura">
        {rutas.length === 0 ? (
          <p className="vacio">
            {hayFiltros
              ? 'Ninguna ruta coincide con el filtro aplicado. Prueba con otro rango de fechas o estado.'
              : 'Todavia no guardaste ninguna ruta. Arma una en el paso 1 de esta misma pestana.'}
          </p>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>Ruta</th>
                <th>Fecha</th>
                <th className="num">Distancia (km)</th>
                <th className="num">CO2 (kg)</th>
                <th className="num">Ahorro</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {rutas.map(r => (
                <tr key={r.id_ruta}>
                  <td><strong>{r.id_ruta.slice(0, 8)}...</strong></td>
                  <td>{new Date(r.fecha_generacion).toLocaleString()}</td>
                  <td className="num">{r.distancia_total_km}</td>
                  <td className="num">{r.co2_estimado_kg}</td>
                  <td className="num">
                    {r.sin_reduccion_significativa ? (
                      <span className="texto-suave">—</span>
                    ) : (
                      <span className="texto-ok">{r.ahorro_co2_pct}%</span>
                    )}
                  </td>
                  <td><span className={`badge ${estadoBadge(r.estado)}`}>{r.estado}</span></td>
                  <td>
                    <div className="btn-grupo">
                      <button type="button" className="btn-secondary btn-sm" onClick={() => onVerMapa(r)}>
                        Mapa
                      </button>
                      <button type="button" className="btn-secondary btn-sm" onClick={() => iniciarEdicion(r)}>
                        Editar
                      </button>
                      <button type="button" className="btn-secondary btn-sm btn-eliminar" onClick={() => eliminar(r)}>
                        Eliminar
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}
