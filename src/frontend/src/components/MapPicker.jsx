import { useEffect, useRef, useState } from 'react'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import api from '../api/client'

const DEFAULT_CENTER = [-12.115, -76.97]
const OSM_TILE_URL = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
const OSM_ATTRIBUTION = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'

const ICON = L.divIcon({
  className: '',
  html: `<div style="background:#4a7fa5;color:#fff;border-radius:50% 50% 50% 0;transform:rotate(-45deg);width:30px;height:30px;border:2px solid #fff;box-shadow:0 2px 6px rgba(0,0,0,.28)"><div style="transform:rotate(45deg);width:100%;height:100%;display:flex;align-items:center;justify-content:center;font-size:13px">&#128205;</div></div>`,
  iconSize: [30, 30],
  iconAnchor: [15, 30],
  popupAnchor: [0, -28],
})

const MIN_CHARS = 2

export default function MapPicker({ latitud, longitud, onPick }) {
  const mapRef = useRef(null)
  const mapInstance = useRef(null)
  const markerRef = useRef(null)
  const onPickRef = useRef(onPick)
  onPickRef.current = onPick

  const [query, setQuery] = useState('')
  const [resultados, setResultados] = useState([])
  const [buscando, setBuscando] = useState(false)
  const [mensaje, setMensaje] = useState(null)
  const [geoError, setGeoError] = useState(false)

  const ponerMarcador = (lat, lng, mover = true) => {
    const map = mapInstance.current
    const pos = [lat, lng]

    if (markerRef.current) {
      markerRef.current.setLatLng(pos)
    } else if (map) {
      markerRef.current = L.marker(pos, { icon: ICON, draggable: true }).addTo(map)
      markerRef.current.on('dragend', ev => {
        const p = ev.target.getLatLng()
        onPickRef.current(p.lat, p.lng)
      })
    }

    if (map && mover) map.flyTo(pos, 17, { duration: 0.8 })
  }

  useEffect(() => {
    if (mapInstance.current || !mapRef.current) return

    const center =
      latitud != null && longitud != null && latitud !== '' && longitud !== ''
        ? [Number(latitud), Number(longitud)]
        : DEFAULT_CENTER

    const map = L.map(mapRef.current, { center, zoom: latitud ? 16 : 12 })

    L.tileLayer(OSM_TILE_URL, { attribution: OSM_ATTRIBUTION, maxZoom: 19 }).addTo(map)

    map.on('click', e => {
      ponerMarcador(e.latlng.lat, e.latlng.lng, false)
      onPickRef.current(e.latlng.lat, e.latlng.lng)
    })

    mapInstance.current = map

    // Evita que la instancia de Leaflet sobreviva al desmontaje del componente.
    return () => {
      map.remove()
      mapInstance.current = null
      markerRef.current = null
    }
  }, [])

  useEffect(() => {
    const map = mapInstance.current
    if (!map) return

    const tieneCoordenadas = latitud != null && longitud != null && latitud !== '' && longitud !== ''

    if (!tieneCoordenadas) {
      if (markerRef.current) {
        markerRef.current.remove()
        markerRef.current = null
      }
      return
    }

    ponerMarcador(Number(latitud), Number(longitud), false)
  }, [latitud, longitud])

  const buscar = async (e) => {
    e.preventDefault()
    const texto = query.trim()

    if (texto.length < MIN_CHARS) {
      setMensaje({ tipo: 'error', texto: `Escribe al menos ${MIN_CHARS} caracteres` })
      setResultados([])
      return
    }

    setBuscando(true)
    setMensaje(null)

    try {
      const r = await api.get('/geocoding/search', { params: { q: texto } })
      const lista = r.data.resultados || []
      setResultados(lista)

      if (lista.length === 0) {
        setMensaje({
          tipo: 'error',
          texto: `No se encontro "${texto}". Prueba con otra calle o marca el punto en el mapa.`,
        })
      }
    } catch (err) {
      const status = err.response?.status
      const detail = err.response?.data?.detail
      const texto =
        typeof detail === 'string'
          ? detail
          : status === 403
            ? 'Sesion expirada. Vuelve a iniciar sesion.'
            : status === 422
              ? 'Busqueda invalida. Escribe al menos 2 caracteres.'
              : err.code === 'ECONNABORTED'
                ? 'El servicio tardo demasiado. Intenta de nuevo.'
                : `No se pudo buscar (codigo ${status || 'sin respuesta'}). Revisa que el backend este corriendo en el puerto correcto.`

      setMensaje({ tipo: 'error', texto })
      setResultados([])
    } finally {
      setBuscando(false)
    }
  }

  const usarMiUbicacion = () => {
    if (!navigator.geolocation) {
      setMensaje({ tipo: 'error', texto: 'Tu navegador no soporta geolocalizacion.' })
      return
    }

    setMensaje({ tipo: 'info', texto: 'Obteniendo tu ubicacion...' })

    navigator.geolocation.getCurrentPosition(
      pos => {
        const { latitude, longitude } = pos.coords
        ponerMarcador(latitude, longitude)
        onPickRef.current(latitude, longitude)
        setMensaje({ tipo: 'ok', texto: 'Ubicacion detectada. Ajusta el marcador si es necesario.' })
      },
      () => {
        setMensaje({ tipo: 'error', texto: 'No se pudo obtener tu ubicacion. Permite el acceso o marca el punto en el mapa.' })
      },
      { enableHighAccuracy: true, timeout: 15000 }
    )
  }

  const elegirResultado = (item) => {
    ponerMarcador(item.latitud, item.longitud)
    onPickRef.current(item.latitud, item.longitud, item.direccion)
    setResultados([])
    setQuery('')
    setMensaje({ tipo: 'ok', texto: `Ubicacion fijada: ${item.direccion}` })
  }

  return (
    <div>
      <form onSubmit={buscar} className="picker-busqueda">
        <input
          type="text"
          value={query}
          onChange={e => setQuery(e.target.value)}
          placeholder="Busca una calle o avenida (ej. Av. Javier Prado, Lima)"
        />
        <button type="submit" disabled={buscando}>
          {buscando ? 'Buscando...' : 'Buscar'}
        </button>
        <button type="button" className="btn-secondary" onClick={usarMiUbicacion} disabled={geoError}>
          Mi ubicacion
        </button>
      </form>

      {mensaje && (
        <p className={`mensaje-inline ${mensaje.tipo}`}>{mensaje.texto}</p>
      )}

      {resultados.length > 0 && (
        <ul className="picker-lista">
          {resultados.map((item, i) => (
            <li key={`${item.latitud}-${item.longitud}-${i}`}>
              <button type="button" className="picker-item" onClick={() => elegirResultado(item)}>
                <strong>{item.direccion}</strong>
                <span>{item.descripcion}</span>
              </button>
            </li>
          ))}
        </ul>
      )}

      <div ref={mapRef} className="mapa-mini" />
      <p className="mapa-ayuda">
        Busca una direccion, usa tu ubicacion o haz click en el mapa. Arrastra el marcador para
        ajustar la posicion.
      </p>
    </div>
  )
}