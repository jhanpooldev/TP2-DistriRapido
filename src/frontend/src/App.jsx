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
      <div style={{ display: 'grid', placeItems: 'center', minHeight: '100vh' }}>
        <p>Cargando sesión...</p>
      </div>
    )
  }

  if (error || !user) {
    return (
      <div style={{ display: 'grid', placeItems: 'center', minHeight: '100vh', gap: '12px' }}>
        <p>{error || 'No se pudo cargar la sesión'}</p>
        <div style={{ display: 'flex', gap: '8px' }}>
          <button type="button" onClick={fetchMe}>Reintentar</button>
          <button type="button" onClick={logout}>Cerrar sesión</button>
        </div>
      </div>
    )
  }

  return <Dashboard user={user} onLogout={logout} />
}

export default App