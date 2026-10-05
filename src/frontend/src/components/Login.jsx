import React, { useState } from 'react'
import api, { extraerError } from '../api/client'

export default function Login({ onLogin }) {
  const [correo, setCorreo] = useState('operador@distrirapido.com')
  const [password, setPassword] = useState('operador123')
  const [error, setError] = useState('')
  const [enviando, setEnviando] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (enviando) return
    setEnviando(true)
    setError('')
    try {
      const r = await api.post('/auth/login', new URLSearchParams({ correo, password }))
      onLogin(r.data.access_token)
    } catch (err) {
      setError(
        err?.response?.status === 401 || err?.response?.status === 422
          ? 'Credenciales inválidas'
          : extraerError(err, 'No se pudo iniciar sesión')
      )
    } finally {
      setEnviando(false)
    }
  }

  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#f0f4f8' }}>
      <div className="card" style={{ width: '100%', maxWidth: '400px' }}>
        <h1 style={{ textAlign: 'center', marginBottom: '30px' }}>EcoLogística Lima</h1>
        {error && <div className="alert alert-error">{error}</div>}
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Correo</label>
            <input type="email" value={correo} onChange={e => setCorreo(e.target.value)} required />
          </div>
          <div className="form-group">
            <label>Contraseña</label>
            <input type="password" value={password} onChange={e => setPassword(e.target.value)} required />
          </div>
          <button type="submit" style={{ width: '100%' }} disabled={enviando}>
            {enviando ? 'Ingresando...' : 'Ingresar'}
          </button>
        </form>
        <p style={{ marginTop: '20px', fontSize: '12px', color: '#666', textAlign: 'center' }}>
          Demo: operador@distrirapido.com / operador123
        </p>
      </div>
    </div>
  )
}