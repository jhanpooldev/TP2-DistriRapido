import { useMemo, useState } from 'react'
import { CENTRO_LIMA, ordenarPorCercania, masCercano, formatoKm, haversineKm } from '../logica/distancia'

/**
 * Seleccion de puntos de entrega.
 *
 * En lugar de un listbox multiseleccion, el operador ve los pedidos ordenados
 * del mas cercano al mas lejano respecto de donde ya lleva la ruta, y puede
 * completar la seleccion de un solo clic con "Siguiente mas cercano".
 */
export default function SelectorPuntos({
  puntos,
  seleccionados,
  onChange,
  vehiculos = [],
  idVehiculo,
  maxPuntos = 20,
}) {
  const [busqueda, setBusqueda] = useState('')
  const [aviso, setAviso] = useState('')

  const vehiculo = vehiculos.find(v => v.id_vehiculo === Number(idVehiculo))
  const capacidad = vehiculo ? Number(vehiculo.capacidad_kg) : null

  // El origen de la medicion es el ultimo punto agregado. Sin seleccion, el
  // centro de Lima, para que la lista tenga un orden razonable desde el inicio.
  const seleccion = useMemo(
    () => seleccionados.map(id => puntos.find(p => p.id_punto === id)).filter(Boolean),
    [seleccionados, puntos]
  )
  const ultimo = seleccion.length > 0 ? seleccion[seleccion.length - 1] : null
  const origen = ultimo || CENTRO_LIMA

  const seleccionSet = useMemo(() => new Set(seleccionados), [seleccionados])

  const disponibles = useMemo(() => {
    const texto = busqueda.trim().toLowerCase()
    const pendientes = puntos.filter(p => !seleccionSet.has(p.id_punto))
    const filtrados = texto
      ? pendientes.filter(p =>
          `${p.direccion} ${p.destinatario}`.toLowerCase().includes(texto)
        )
      : pendientes
    return ordenarPorCercania(origen, filtrados)
  }, [puntos, seleccionSet, origen, busqueda])

  const pesoTotal = seleccion.reduce((suma, p) => suma + Number(p.peso_kg || 0), 0)
  const excedeCapacidad = capacidad != null && pesoTotal > capacidad
  const excedeMaximo = seleccionados.length >= maxPuntos
  const llenado = capacidad ? Math.min(100, (pesoTotal / capacidad) * 100) : 0

  // Motivo por el que ya no se puede agregar nada mas.
  const bloqueo = excedeCapacidad
    ? `La carga de ${pesoTotal.toFixed(1)} kg supera la capacidad de ${vehiculo.placa} (${capacidad} kg). Quita un pedido para continuar.`
    : excedeMaximo
      ? `Una ruta admite hasta ${maxPuntos} puntos.`
      : ''

  const alternar = (id) => {
    if (seleccionSet.has(id)) {
      setAviso('')
      onChange(seleccionados.filter(x => x !== id))
      return
    }
    if (bloqueo) {
      setAviso(bloqueo)
      return
    }

    // Antes de agregar se comprueba que la carga siga cabiendo en el vehiculo,
    // de modo que la seleccion nunca quede en un estado invalido sin avisar.
    const punto = puntos.find(p => p.id_punto === id)
    const nuevoPeso = pesoTotal + Number(punto?.peso_kg || 0)
    if (capacidad != null && nuevoPeso > capacidad) {
      setAviso(
        `${punto.direccion} pesa ${punto.peso_kg} kg y la carga llegaria a ${nuevoPeso.toFixed(1)} kg, por encima de los ${capacidad} kg de ${vehiculo.placa}. Quita otro pedido antes de agregar este.`
      )
      return
    }

    setAviso('')
    onChange([...seleccionados, id])
  }

  const agregarSiguiente = () => {
    if (bloqueo) {
      setAviso(bloqueo)
      return
    }
    const candidatos = disponibles.filter(p => Number(p.peso_kg || 0) <= (capacidad ?? Infinity))
    const siguiente = masCercano(origen, candidatos.length ? candidatos : disponibles)
    if (!siguiente) {
      setAviso('No quedan pedidos disponibles para agregar.')
      return
    }
    const nuevoPeso = pesoTotal + Number(siguiente.peso_kg || 0)
    if (capacidad != null && nuevoPeso > capacidad) {
      setAviso(
        `${siguiente.direccion} pesa ${siguiente.peso_kg} kg y la carga llegaría a ${nuevoPeso.toFixed(1)} kg, por encima de los ${capacidad} kg del vehiculo.`
      )
      return
    }
    setAviso('')
    onChange([...seleccionados, siguiente.id_punto])
  }

  const vaciar = () => {
    setAviso('')
    onChange([])
  }

  const distanciaDesdeOrigen = (p) => haversineKm(origen, p)
  const etiquetaOrigen = ultimo ? 'del ultimo punto' : 'del centro'

  return (
    <div className="card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', gap: 12, flexWrap: 'wrap' }}>
        <h3>1. Elige los pedidos que van en la ruta</h3>
        <span className="texto-suave">
          {seleccionados.length} de {puntos.length} pedidos
        </span>
      </div>
      <p className="texto-suave" style={{ marginBottom: 14 }}>
        Los pedidos se listan del mas cercano al mas lejano respecto a {etiquetaOrigen}. Agrega
        uno por uno o deja que la aplicacion elija el siguiente.
      </p>

      <div className="btn-grupo" style={{ marginBottom: 14 }}>
        <button type="button" onClick={agregarSiguiente} disabled={Boolean(bloqueo) || puntos.length < 2}>
          + Siguiente mas cercano
        </button>
        <button type="button" className="btn-secondary btn-sm" onClick={vaciar} disabled={seleccionados.length === 0}>
          Vaciar seleccion
        </button>
      </div>

      {aviso && <div className="alert alert-error">{aviso}</div>}

      <div className="sel-panel">
        <div>
          <label htmlFor="busqueda-pedidos">Pedidos disponibles</label>
          <input
            id="busqueda-pedidos"
            value={busqueda}
            onChange={e => setBusqueda(e.target.value)}
            placeholder="Buscar por direccion o destinatario"
          />

          <div className="sel-lista" style={{ marginTop: 10 }}>
            {disponibles.length === 0 ? (
              <div className="sel-vacio">
                {puntos.length === 0
                  ? 'Todavia no hay pedidos registrados. Crea uno en la pestaña "Pedidos".'
                  : seleccionados.length === puntos.length
                    ? 'Todos los pedidos ya estan en la ruta.'
                    : 'Ningun pedido coincide con la busqueda.'}
              </div>
            ) : (
              disponibles.map(p => (
                <div className="sel-item" key={p.id_punto}>
                  <div className="sel-datos">
                    <strong>{p.destinatario || p.direccion}</strong>
                    <span>{p.direccion} · {p.peso_kg} kg</span>
                  </div>
                  <span className="sel-dist">{formatoKm(distanciaDesdeOrigen(p))}</span>
                  <button type="button" className="btn-secondary btn-sm" onClick={() => alternar(p.id_punto)}>
                    Agregar
                  </button>
                </div>
              ))
            )}
          </div>
        </div>

        <div>
          <label>Ruta en construccion</label>
          <div className="sel-lista" style={{ marginTop: 10 }}>
            {seleccion.length === 0 ? (
              <div className="sel-vacio">Aun no agregaste ningun pedido.</div>
            ) : (
              seleccion.map((p, i) => (
                <div className="sel-item" key={p.id_punto}>
                  <span className="sel-orden">{i + 1}</span>
                  <div className="sel-datos">
                    <strong>{p.destinatario || p.direccion}</strong>
                    <span>{p.direccion} · {p.peso_kg} kg</span>
                  </div>
                  <button
                    type="button"
                    className="btn-ghost btn-sm"
                    onClick={() => alternar(p.id_punto)}
                    aria-label={`Quitar ${p.direccion}`}
                  >
                    Quitar
                  </button>
                </div>
              ))
            )}
          </div>

          <div style={{ marginTop: 14 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 13 }}>
              <span className="texto-suave">
                Carga: <strong style={{ color: excedeCapacidad ? 'var(--error)' : 'var(--texto)' }}>
                  {pesoTotal.toFixed(1)} kg
                </strong>
                {capacidad != null && ` de ${capacidad} kg`}
              </span>
              {capacidad != null && <span className="texto-suave">{Math.round(llenado)}%</span>}
            </div>
            <div className={`barra ${excedeCapacidad ? 'excedida' : llenado > 85 ? 'llena' : ''}`}>
              <div style={{ width: `${llenado}%` }} />
            </div>
            {seleccionados.length > 1 && (
              <p className="ayuda">
                Distancia acumulada entre los puntos elegidos:{' '}
                {formatoKm(
                  seleccion.reduce(
                    (total, p, i) => (i === 0 ? total : total + haversineKm(seleccion[i - 1], p)),
                    0
                  )
                )}
              </p>
            )}
          </div>
        </div>
      </div>

      {bloqueo && <p className="texto-error sep">{bloqueo}</p>}
    </div>
  )
}
