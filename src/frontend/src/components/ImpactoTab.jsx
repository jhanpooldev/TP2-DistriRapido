import { useMemo, useState } from 'react'

export default function ImpactoTab({ rutas, onVerMapa }) {
  const [idSeleccionada, setIdSeleccionada] = useState('')

  const ruta = useMemo(
    () => rutas.find(r => r.id_ruta === idSeleccionada) || null,
    [rutas, idSeleccionada]
  )

  if (rutas.length === 0) {
    return (
      <div>
        <div className="seccion-titulo">
          <h2>Impacto ambiental</h2>
          <p>Comparacion entre la ruta del orden de llegada y la ruta optimizada.</p>
        </div>
        <div className="card">
          <p className="vacio" style={{ padding: 0 }}>
            Todavia no hay rutas guardadas. Arma una en la pestana <strong>Rutas</strong> para ver
            cuantos kilometos y kilos de CO2 ahorra.
          </p>
        </div>
      </div>
    )
  }

  const reduccionSignificativa = ruta && !ruta.sin_reduccion_significativa && ruta.ahorro_co2_pct > 0

  return (
    <div>
      <div className="seccion-titulo">
        <h2>Impacto ambiental</h2>
        <p>Lo que deja optimizar: menos distancia, menos tiempo y menos emisiones.</p>
      </div>

      <div className="card">
        <div className="form-group" style={{ marginBottom: 0 }}>
          <label htmlFor="ruta-impacto">Ruta a evaluar</label>
          <select
            id="ruta-impacto"
            value={idSeleccionada}
            onChange={e => setIdSeleccionada(e.target.value)}
          >
            <option value="">-- Selecciona una ruta --</option>
            {rutas.map(r => (
              <option key={r.id_ruta} value={r.id_ruta}>
                {r.id_ruta.slice(0, 8)}... · {new Date(r.fecha_generacion).toLocaleDateString()} ·{' '}
                {r.co2_estimado_kg} kg CO2
              </option>
            ))}
          </select>
        </div>
      </div>

      {ruta && (
        <div className="card">
          <h3>Comparacion de emisiones</h3>

          <div className="tabla-envoltura" style={{ marginBottom: 18 }}>
            <table className="table">
              <thead>
                <tr>
                  <th>Escenario</th>
                  <th className="num">Distancia (km)</th>
                  <th className="num">Tiempo (min)</th>
                  <th className="num">CO2 (kg)</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Sin optimizar (orden de llegada)</td>
                  <td className="num">{ruta.distancia_sin_optimizar_km}</td>
                  <td className="num">{ruta.tiempo_sin_optimizar_min}</td>
                  <td className="num">{ruta.co2_sin_optimizar_kg}</td>
                </tr>
                <tr>
                  <td><strong>Ruta optimizada</strong></td>
                  <td className="num"><strong>{ruta.distancia_total_km}</strong></td>
                  <td className="num"><strong>{ruta.tiempo_estimado_min}</strong></td>
                  <td className="num"><strong>{ruta.co2_estimado_kg}</strong></td>
                </tr>
              </tbody>
            </table>
          </div>

          <div className="grid">
            <div className="stat-card">
              <div className="stat-value">{ruta.ahorro_distancia_pct}%</div>
              <div className="stat-label">Menos distancia</div>
            </div>
            <div className="stat-card">
              <div className="stat-value">
                {reduccionSignificativa ? `${ruta.ahorro_co2_pct}%` : '0%'}
              </div>
              <div className="stat-label">Menos CO2</div>
            </div>
            <div className="stat-card">
              <div className="stat-value">{reduccionSignificativa ? ruta.ahorro_co2_kg : 0}</div>
              <div className="stat-label">kg CO2 evitados</div>
            </div>
          </div>

          {reduccionSignificativa ? (
            <div className="alert alert-success">
              <span>
                <strong>La optimizacion evito {ruta.ahorro_co2_kg} kg de CO2</strong> y recorrio{' '}
                {ruta.ahorro_distancia_pct}% menos distancia que la ruta por orden de llegada.
              </span>
            </div>
          ) : (
            <div className="alert alert-info">
              <span>
                <strong>No hubo una reduccion significativa de CO2.</strong> La ruta optimizada es
                practicamente igual a la del orden de llegada, por lo que no se reporta un porcentaje
                de ahorro.
              </span>
            </div>
          )}

          <button type="button" className="btn-secondary" onClick={() => onVerMapa(ruta)}>
            Ver ruta en el mapa
          </button>
        </div>
      )}
    </div>
  )
}
