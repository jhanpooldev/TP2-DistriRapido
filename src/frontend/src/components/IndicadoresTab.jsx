import React, { useEffect, useState } from 'react'
import api, { extraerError } from '../api/client'
import {
  formatearNumero,
  tarjetasIndicadores,
  tarjetasSostenibilidad,
} from '../logica/indicadores'

function Tarjetas({ items }) {
  return (
    <div className="grid">
      {items.map(item => (
        <div key={item.id}>
          <div className="stat-value">
            {item.valor}{item.unidad ? ` ${item.unidad}` : ''}
          </div>
          <div className="stat-label">{item.etiqueta}</div>
        </div>
      ))}
    </div>
  )
}

/** RF-012/RF-013: panel del gerente con indicadores logicos y de sostenibilidad. */
export default function IndicadoresTab() {
  const [indicadores, setIndicadores] = useState(null)
  const [sostenibilidad, setSostenibilidad] = useState(null)
  const [cargando, setCargando] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    let activo = true
    Promise.all([
      api.get('/indicadores'),
      api.get('/indicadores/sostenibilidad'),
    ])
      .then(([respuestaGeneral, respuestaSostenibilidad]) => {
        if (!activo) return
        setIndicadores(respuestaGeneral.data)
        setSostenibilidad(respuestaSostenibilidad.data)
      })
      .catch((e) => {
        if (activo) setError(extraerError(e))
      })
      .finally(() => {
        if (activo) setCargando(false)
      })
    return () => { activo = false }
  }, [])

  if (cargando) {
    return <div className="cargando" role="status" aria-live="polite">Cargando indicadores...</div>
  }
  if (error) {
    return <div className="alert alert-error" role="alert">{error}</div>
  }

  return (
    <div>
      <div className="seccion-titulo">
        <h2>Panel de indicadores</h2>
        <p>
          Resumen de las rutas confirmadas: distancia, emisiones y ahorro frente al recorrido sin optimizar.
        </p>
      </div>

      {indicadores?.sin_datos && (
        <p className="alert alert-info" role="status">{indicadores.mensaje}</p>
      )}

      <section className="card" aria-labelledby="indicadores-logisticos">
        <h3 id="indicadores-logisticos">Indicadores logísticos</h3>
        <Tarjetas items={tarjetasIndicadores(indicadores)} />
      </section>

      <section className="card" aria-labelledby="indicadores-sostenibilidad">
        <h3 id="indicadores-sostenibilidad">Indicadores de sostenibilidad</h3>
        {sostenibilidad?.sin_datos ? (
          <p className="alert alert-info" role="status">{sostenibilidad.mensaje}</p>
        ) : (
          <Tarjetas items={tarjetasSostenibilidad(sostenibilidad)} />
        )}
        {sostenibilidad && !sostenibilidad.sin_datos && (
          <p className="texto-suave">
            {formatearNumero(sostenibilidad.entregas, 0)} entregas consideradas en el cálculo.
          </p>
        )}
      </section>
    </div>
  )
}
