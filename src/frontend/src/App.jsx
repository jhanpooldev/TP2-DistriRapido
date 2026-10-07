import React, { useState, useEffect, useCallback } from 'react'
import api, { extraerError } from './api/client'
import Login from './components/Login'
import Dashboard from './components/Dashboard'

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'))
  const [user, setUser] = useState(null)
  const [cargando, setCargando] = useState(Boolean(localStorage.getItem('token')))
  const [error, setError] = useState('')

  const logout = useCallback(() => {
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
      <div className="pantalla-centrada">
        <div className="cargando" />
        <p>Cargando sesion...</p>
      </div>
    )
  }

  if (error || !user) {
    return (
      <div className="pantalla-centrada">
        <div>
          <h2>No se pudo cargar la sesion</h2>
          <p className="sep">{error || 'Verifica que el backend este corriendo en el puerto 8000.'}</p>
        </div>
        <div className="btn-grupo" style={{ justifyContent: 'center' }}>
          <button type="button" onClick={fetchMe}>Reintentar</button>
          <button type="button" className="btn-secondary" onClick={logout}>Cerrar sesion</button>
        </div>
      </div>
    )
  }

  return <Dashboard user={user} onLogout={logout} />
}

export default App