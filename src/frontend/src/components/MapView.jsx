import { useEffect, useRef, useState } from 'react'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const DEFAULT_CENTER = [-12.115, -76.97]
const DEFAULT_ZOOM = 12

const OSM_TILE_URL = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
const OSM_ATTRIBUTION = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'

export default function MapView({ puntos = [], center = DEFAULT_CENTER, zoom = DEFAULT_ZOOM }) {
  const mapRef = useRef(null)
  const mapInstance = useRef(null)
  const capaRef = useRef(null)
  const polylineRef = useRef(null)
  const markersRef = useRef([])
  const fallosRef = useRef(0)

  const [sinTiles, setSinTiles] = useState(false)
  const [cargando, setCargando] = useState(true)

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
      polylineRef.current = null
      markersRef.current = []
    }
  }, [])

  useEffect(() => {
    const map = mapInstance.current
    if (!map) return

    markersRef.current.forEach(marker => marker.remove())
    markersRef.current = []

    if (polylineRef.current) {
      polylineRef.current.remove()
      polylineRef.current = null
    }

    const valid = puntos
      .filter(p => p.latitud != null && p.longitud != null)
      .map(p => [Number(p.latitud), Number(p.longitud)])

    if (valid.length === 0) return

    if (valid.length > 1) {
      polylineRef.current = L.polyline(valid, {
        color: '#2f7f68',
        weight: 4,
        opacity: 0.9,
        lineCap: 'round',
        lineJoin: 'round',
      }).addTo(map)
    }

    valid.forEach((coord, i) => {
      const marker = L.marker(coord, {
        icon: L.divIcon({
          className: '',
          html: `<div style="background:#2f7f68;color:#fff;border-radius:50%;width:28px;height:28px;display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:12px;border:2px solid #fff;box-shadow:0 2px 4px rgba(0,0,0,.25)">${i + 1}</div>`,
          iconSize: [28, 28],
          iconAnchor: [14, 14],
        }),
      })
        .addTo(map)
        .bindPopup(
          `<strong>Punto ${i + 1}</strong><br>${puntos[i].direccion || ''}<br>Peso: ${puntos[i].peso_kg} kg<br>Destinatario: ${puntos[i].destinatario || ''}`
        )

      markersRef.current.push(marker)
    })

    if (valid.length > 1) {
      map.fitBounds(L.latLngBounds(valid), { padding: [50, 50] })
    } else {
      map.setView(valid[0], 14)
    }
  }, [puntos])

  return (
    <div>
      <div className="mapa-contenedor">
        <div ref={mapRef} style={{ width: '100%', height: '500px' }} />

        {cargando && !sinTiles && (
          <div style={capaAviso}>
            Cargando mapa...
          </div>
        )}

        {sinTiles && (
          <div style={capaAviso}>
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
