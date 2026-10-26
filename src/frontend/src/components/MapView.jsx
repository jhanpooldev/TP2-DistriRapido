import { useEffect, useRef, useState } from 'react'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { obtenerTrazadoCalles } from '../logica/rutaCalles'

const DEFAULT_CENTER = [-12.115, -76.97]
const DEFAULT_ZOOM = 12

const OSM_TILE_URL = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
const OSM_ATTRIBUTION = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'

function tieneCoordenadas(punto) {
  return (
    punto?.latitud !== null && punto?.latitud !== undefined && punto?.latitud !== '' &&
    punto?.longitud !== null && punto?.longitud !== undefined && punto?.longitud !== '' &&
    Number.isFinite(Number(punto.latitud)) && Number.isFinite(Number(punto.longitud))
  )
}

/**
 * Construye el popup con nodos DOM y textContent. No se interpola HTML con
 * datos del usuario: una direccion o un destinatario no pueden inyectar
 * etiquetas ni scripts en el mapa.
 */
function crearPopupParada(punto, numero) {
  const contenedor = document.createElement('div')
  contenedor.className = 'popup-parada'

  const titulo = document.createElement('strong')
  titulo.textContent = `Parada ${numero}`
  contenedor.appendChild(titulo)

  const agregarLinea = (etiqueta, valor) => {
    const linea = document.createElement('div')
    linea.className = 'popup-linea'

    const etiquetaEl = document.createElement('span')
    etiquetaEl.className = 'popup-etiqueta'
    etiquetaEl.textContent = etiqueta

    const valorEl = document.createElement('span')
    valorEl.textContent = valor

    linea.append(etiquetaEl, valorEl)
    contenedor.appendChild(linea)
  }

  const direccion = String(punto?.direccion ?? '').trim()
  const destinatario = String(punto?.destinatario ?? '').trim()
  const lat = Number(punto?.latitud)
  const lng = Number(punto?.longitud)

  agregarLinea('Direccion', direccion || 'Sin direccion registrada')
  if (!direccion) {
    agregarLinea('Coordenadas', `${lat.toFixed(6)}, ${lng.toFixed(6)}`)
  }
  agregarLinea('Destinatario', destinatario || 'Sin destinatario registrado')
  agregarLinea('Peso', `${punto?.peso_kg ?? '—'} kg`)

  return contenedor
}

function crearPopupOrigen(direccion) {
  const contenedor = document.createElement('div')
  contenedor.className = 'popup-parada'

  const titulo = document.createElement('strong')
  titulo.textContent = 'Centro de distribucion'
  contenedor.appendChild(titulo)

  const linea = document.createElement('div')
  linea.className = 'popup-linea'
  linea.textContent = String(direccion ?? '').trim() || 'Punto de partida y retorno de la ruta'
  contenedor.appendChild(linea)

  return contenedor
}

/** Recorrido completo: centro de distribucion -> paradas -> centro. */
function coordenadasDeRecorrido(puntos, origenLat, origenLng) {
  const paradas = puntos
    .filter(tieneCoordenadas)
    .map(punto => [Number(punto.latitud), Number(punto.longitud)])

  if (paradas.length === 0 || !tieneCoordenadas({ latitud: origenLat, longitud: origenLng })) {
    return paradas
  }

  const origen = [Number(origenLat), Number(origenLng)]
  return [origen, ...paradas, origen]
}

export default function MapView({
  puntos = [],
  origenLat = null,
  origenLng = null,
  origenDireccion = '',
  center = DEFAULT_CENTER,
  zoom = DEFAULT_ZOOM,
}) {
  const mapRef = useRef(null)
  const mapInstance = useRef(null)
  const capaRef = useRef(null)
  const capasRecorridoRef = useRef([])
  const markersRef = useRef([])
  const fallosRef = useRef(0)

  const [sinTiles, setSinTiles] = useState(false)
  const [cargando, setCargando] = useState(true)
  const [trazadoCalles, setTrazadoCalles] = useState(null)
  const [estadoTrazado, setEstadoTrazado] = useState('inactivo')

  // Crea (o recrea) la capa de tiles. Se separa del efecto de montaje para que
  // "Reintentar" no necesite recargar toda la aplicacion.
  const crearCapa = () => {
    const map = mapInstance.current
    if (!map) return

    if (capaRef.current) {
      map.removeLayer(capaRef.current)
      capaRef.current = null
    }

    fallosRef.current = 0
    setSinTiles(false)
    setCargando(true)

    const capa = L.tileLayer(OSM_TILE_URL, { attribution: OSM_ATTRIBUTION, maxZoom: 19 })

    capa.on('loading', () => setCargando(true))

    // US-005: un tile que carga no borra los errores previos, porque un
    // proveedor parcialmente caido deja el mapa a medias sin avisar.
    capa.on('tileload', () => {
      setCargando(false)
      if (fallosRef.current === 0) setSinTiles(false)
    })

    capa.on('tileerror', () => {
      fallosRef.current += 1
      setCargando(false)
      if (fallosRef.current >= 4) setSinTiles(true)
    })

    capa.addTo(map)
    capaRef.current = capa
  }

  useEffect(() => {
    if (mapInstance.current || !mapRef.current) return

    const map = L.map(mapRef.current, {
      center,
      zoom,
      zoomControl: true,
      attributionControl: true,
    })

    mapInstance.current = map
    crearCapa()

    // Sin esto la instancia de Leaflet sobrevive al cambio de pestaña y
    // duplica contenedores/contadores en cada montaje.
    return () => {
      map.remove()
      mapInstance.current = null
      capaRef.current = null
      capasRecorridoRef.current = []
      markersRef.current = []
    }
  }, [])

  // Pide a OSRM el trazado real por calles. Si el servicio no responde, el
  // mapa conserva el trazado recto como respaldo visible.
  useEffect(() => {
    const recorrido = coordenadasDeRecorrido(puntos, origenLat, origenLng)

    if (recorrido.length < 2) {
      setTrazadoCalles(null)
      setEstadoTrazado('inactivo')
      return
    }

    const controlador = new AbortController()
    let vigente = true

    setTrazadoCalles(null)
    setEstadoTrazado('cargando')

    obtenerTrazadoCalles(recorrido, { signal: controlador.signal })
      .then(resultado => {
        if (!vigente) return
        setTrazadoCalles(resultado)
        setEstadoTrazado(resultado ? 'calles' : 'aproximado')
      })
      .catch(() => {
        // obtenerTrazadoCalles ya devuelve null ante fallos, pero se cubre
        // cualquier rechazo inesperado para no dejar el aviso en "cargando".
        if (!vigente) return
        setTrazadoCalles(null)
        setEstadoTrazado('aproximado')
      })

    return () => {
      vigente = false
      controlador.abort()
    }
  }, [puntos, origenLat, origenLng])

  useEffect(() => {
    const map = mapInstance.current
    if (!map) return

    markersRef.current.forEach(marker => marker.remove())
    markersRef.current = []

    capasRecorridoRef.current.forEach(capa => capa.remove())
    capasRecorridoRef.current = []

    const validos = puntos
      .map((punto, indice) => ({ punto, indice }))
      .filter(({ punto }) => tieneCoordenadas(punto))

    if (validos.length === 0) return

    const coordenadasParadas = validos.map(({ punto }) => [
      Number(punto.latitud),
      Number(punto.longitud),
    ])

    const origenValido = tieneCoordenadas({ latitud: origenLat, longitud: origenLng })
    const recorrido = origenValido
      ? [[Number(origenLat), Number(origenLng)], ...coordenadasParadas, [Number(origenLat), Number(origenLng)]]
      : coordenadasParadas

    if (trazadoCalles?.trazado?.length > 1) {
      // Halo blanco debajo del trazado para que se lea sobre cualquier calle.
      capasRecorridoRef.current.push(
        L.polyline(trazadoCalles.trazado, {
          color: '#ffffff',
          weight: 9,
          opacity: 0.9,
          lineCap: 'round',
          lineJoin: 'round',
          interactive: false,
        }).addTo(map),
        L.polyline(trazadoCalles.trazado, {
          color: '#2f7f68',
          weight: 5,
          opacity: 0.95,
          lineCap: 'round',
          lineJoin: 'round',
        }).addTo(map)
      )
    } else if (recorrido.length > 1) {
      // Respaldo honesto: linea discontinua cuando no hay trazado por calles.
      capasRecorridoRef.current.push(
        L.polyline(recorrido, {
          color: '#2f7f68',
          weight: 4,
          opacity: 0.9,
          dashArray: '7 9',
          lineCap: 'round',
          lineJoin: 'round',
        }).addTo(map)
      )
    }

    if (origenValido) {
      markersRef.current.push(
        L.marker([Number(origenLat), Number(origenLng)], {
          title: 'Centro de distribucion',
          alt: 'Centro de distribucion: punto de partida y retorno de la ruta',
          keyboard: true,
          riseOnHover: true,
          icon: L.divIcon({
            className: '',
            html: '<div style="background:#1e2a26;color:#fff;border-radius:6px;width:30px;height:30px;display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:11px;border:2px solid #fff;box-shadow:0 2px 4px rgba(0,0,0,.25)">CD</div>',
            iconSize: [30, 30],
            iconAnchor: [15, 15],
          }),
        })
          .addTo(map)
          .bindPopup(crearPopupOrigen(origenDireccion))
      )
    }

    validos.forEach(({ punto, indice }, posicion) => {
      const numero = Number.isInteger(punto.orden) ? punto.orden : indice + 1
      const direccion = String(punto.direccion ?? '').trim()
      const etiqueta = direccion || `coordenadas ${Number(punto.latitud).toFixed(6)}, ${Number(punto.longitud).toFixed(6)}`

      const marker = L.marker(coordenadasParadas[posicion], {
        title: `Parada ${numero}: ${etiqueta}`,
        alt: `Parada ${numero}: ${etiqueta}`,
        keyboard: true,
        riseOnHover: true,
        icon: L.divIcon({
          className: '',
          html: `<div style="background:#2f7f68;color:#fff;border-radius:50%;width:28px;height:28px;display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:12px;border:2px solid #fff;box-shadow:0 2px 4px rgba(0,0,0,.25)">${numero}</div>`,
          iconSize: [28, 28],
          iconAnchor: [14, 14],
        }),
      })
        .addTo(map)
        .bindPopup(crearPopupParada(punto, numero))

      markersRef.current.push(marker)
    })

    const referencia = trazadoCalles?.trazado?.length > 1 ? trazadoCalles.trazado : recorrido
    if (referencia.length > 1) {
      map.fitBounds(L.latLngBounds(referencia), { padding: [50, 50] })
    } else {
      map.setView(referencia[0], 14)
    }
  }, [puntos, trazadoCalles, origenLat, origenLng, origenDireccion])

  const kilometrosCalles = trazadoCalles?.distanciaKm

  return (
    <div>
      <div className="mapa-contenedor">
        <div
          ref={mapRef}
          role="region"
          aria-label="Mapa de la ruta: recorrido por calles y paradas numeradas en orden de entrega"
          aria-busy={cargando}
          style={{ width: '100%', height: '500px' }}
        />

        {cargando && !sinTiles && (
          <div style={capaAviso} role="status" aria-live="polite">
            Cargando mapa...
          </div>
        )}

        {sinTiles && (
          <div style={capaAviso} role="alert">
            <strong>No se pudo cargar el mapa base.</strong>
            <br />
            El proveedor de mapas no responde en este momento. La ruta y el orden de
            entrega se muestran igualmente en la tabla inferior.
            <br />
            <button
              type="button"
              className="btn-secondary"
              style={{ marginTop: '10px' }}
              onClick={crearCapa}
            >
              Reintentar
            </button>
          </div>
        )}
      </div>

      {estadoTrazado !== 'inactivo' && (
        <p className="texto-suave" role="status" aria-live="polite" style={{ marginTop: 8 }}>
          {estadoTrazado === 'cargando' && 'Calculando el trazado por calles...'}
          {estadoTrazado === 'calles' && (
            <>
              Trazado por calles: {Number(kilometrosCalles).toFixed(1)} km
              {' '}(OSRM / OpenStreetMap). La distancia planificada del resumen se
              estima en linea recta.
            </>
          )}
          {estadoTrazado === 'aproximado' && (
            <>
              Trazado aproximado en linea recta: el servicio de calles no respondio.
              Los puntos y su orden siguen siendo validos.
            </>
          )}
        </p>
      )}
    </div>
  )
}

const capaAviso = {
  position: 'absolute',
  top: 10,
  left: 10,
  right: 10,
  padding: '11px 14px',
  background: 'rgba(255,255,255,0.96)',
  border: '1px solid #cbd6d2',
  borderRadius: '7px',
  fontSize: '13px',
  color: '#1e2a26',
  zIndex: 1000,
  boxShadow: '0 1px 3px rgba(30,42,38,0.06), 0 4px 14px rgba(30,42,38,0.05)',
}
