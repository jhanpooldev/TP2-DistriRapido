import React, { useState, useEffect, useCallback, lazy, Suspense } from 'react'
import api, { extraerError, limpiarCache } from './api/client'
import Login from './components/Login'

// El panel completo (mapas, rutas e impacto) solo se descarga despues del
// login. Asi el primer render no carga Leaflet ni el resto de pestañas.
const Dashboard = lazy(() => import('./components/Dashboard'))

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'))
  const [user, setUser] = useState(null)
  const [cargando, setCargando] = useState(Boolean(localStorage.getItem('token')))
  const [error, setError] = useState('')

  const logout = useCallback(() => {
    // Evita que el siguiente usuario vea respuestas cacheadas de la sesion anterior.
    limpiarCache()
    localStorage.removeItem('token')
    setToken(null)
    setUser(null)
    setCargando(false)
    setError('')
  }, [])

  const fetchMe = useCallback(async () => {
    setCargando(true)
    setError('')
    try {
      const r = await api.get('/auth/me')
      setUser(r.data)
    } catch (e) {
      // Solo se cierra la sesion si el token es invalido o vencido. Si el
      // backend esta caido se conserva el token para poder reintentar.
      if (e?.response?.status === 401) {
        logout()
      } else {
        setUser(null)
        setError(extraerError(e, 'No se pudo validar la sesión'))
      }
    } finally {
      setCargando(false)
    }
  }, [logout])

  useEffect(() => {
    if (token) fetchMe()
  }, [token, fetchMe])

  const login = (newToken) => {
    localStorage.setItem('token', newToken)
    setToken(newToken)
  }

  if (!token) return <Login onLogin={login} />

  if (cargando) {
    return (
      <main className="pantalla-centrada" id="contenido-principal">
        <div className="cargando" role="status" aria-live="polite">
          <span className="sr-only">Cargando sesión...</span>
        </div>
        <p>Cargando sesión...</p>
      </main>
    )
  }

  if (error || !user) {
    return (
      <main className="pantalla-centrada" id="contenido-principal">
        <div role="alert">
          <h2>No se pudo cargar la sesión</h2>
          <p className="sep">{error || 'Verifica que el backend esté corriendo en el puerto 8000.'}</p>
        </div>
        <div className="btn-grupo" style={{ justifyContent: 'center' }}>
          <button type="button" onClick={fetchMe}>Reintentar</button>
          <button type="button" className="btn-secondary" onClick={logout}>Cerrar sesión</button>
        </div>
      </main>
    )
  }

  return (
    <Suspense
      fallback={(
        <main className="pantalla-centrada" id="contenido-principal">
          <div className="cargando" role="status" aria-live="polite">
            <span className="sr-only">Cargando panel...</span>
          </div>
          <p>Cargando panel...</p>
        </main>
      )}
    >
      <Dashboard user={user} onLogout={logout} />
    </Suspense>
  )
}

export default App