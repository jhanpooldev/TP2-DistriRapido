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
        <h2>Impacto ambiental</h2>
        <div className="card">
          <p style={{ color: '#666', margin: 0 }}>
            Todavia no hay rutas confirmadas. Genera y guarda una ruta para ver el impacto
            ambiental estimado.
          </p>
        </div>
      </div>
    )
  }

  const reduccionSignificativa = ruta && !ruta.sin_reduccion_significativa && ruta.ahorro_co2_pct > 0

  return (
    <div>
      <h2>Impacto ambiental</h2>

      <div className="card" style={{ marginBottom: '20px' }}>
        <h3>Ruta a evaluar</h3>
        <select
          value={idSeleccionada}
          onChange={e => setIdSeleccionada(e.target.value)}
          style={{ maxWidth: '460px', width: '100%', padding: '8px', border: '1px solid #ccc', borderRadius: '4px' }}
        >
          <option value="">-- Selecciona una ruta --</option>
          {rutas.map(r => (
            <option key={r.id_ruta} value={r.id_ruta}>
              {r.id_ruta.slice(0, 8)}... - {new Date(r.fecha_generacion).toLocaleDateString()} -{' '}
              {r.co2_estimado_kg} kg CO₂
            </option>
          ))}
        </select>
      </div>

      {ruta && (
        <div className="card">
          <h3>Comparación de emisiones</h3>

          <table className="table" style={{ marginBottom: '20px' }}>
            <thead>
              <tr>
                <th>Escenario</th>
                <th>Distancia (km)</th>
                <th>Tiempo (min)</th>
                <th>CO₂ (kg)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Ruta no optimizada (orden de ingreso)</td>
                <td>{ruta.distancia_sin_optimizar_km}</td>
                <td>{ruta.tiempo_sin_optimizar_min}</td>
                <td>{ruta.co2_sin_optimizar_kg}</td>
              </tr>
              <tr>
                <td><strong>Ruta optimizada</strong></td>
                <td>{ruta.distancia_total_km}</td>
                <td>{ruta.tiempo_estimado_min}</td>
                <td>{ruta.co2_estimado_kg}</td>
              </tr>
            </tbody>
          </table>

          {reduccionSignificativa ? (
            <div className="alert alert-success">
              <strong>Reduccion de CO₂: {ruta.ahorro_co2_pct}%</strong>
              <br />
              Se evitaron aproximadamente {ruta.ahorro_co2_kg} kg de CO₂ y{' '}
              {ruta.ahorro_distancia_pct}% menos de distancia frente a la ruta sin optimizar.
            </div>
          ) : (
            <div className="alert alert-success">
              <strong>No hubo una reduccion significativa de CO₂.</strong>
              <br />
              La ruta optimizada es practicamente igual a la ruta no optimizada, por lo que no se
              reporta un porcentaje de ahorro. {ruta.sin_reduccion_significativa && ruta.ahorro_co2_pct === 0 && 'El ahorro se reporta en cero y no como un valor negativo.'}
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