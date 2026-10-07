import React, { useState } from 'react'
import api, { extraerError } from '../api/client'

export default function Login({ onLogin }) {
  const [correo, setCorreo] = useState('')
  const [password, setPassword] = useState('')
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
          ? 'Credenciales invalidas'
          : extraerError(err, 'No se pudo iniciar sesion')
      )
    } finally {
      setEnviando(false)
    }
  }

  return (
    <div className="login-envoltura">
      <div className="card login-tarjeta">
        <div className="login-marca">
          <div className="app-logo">E</div>
          <h1>EcoLogistica Lima</h1>
          <p>Optimizador de rutas sostenibles para DistriRapido S.A.C.</p>
        </div>

        <div className="login-valor">
          <strong>Para que sirve</strong>
          <ul>
            <li>Ordena los pedidos del dia de menor a mayor distancia.</li>
            <li>Calcula la ruta mas corta respetando la carga del vehiculo.</li>
            <li>Muestra cuantos kilometos, minutos y kilos de CO2 ahorra.</li>
          </ul>
        </div>

        {error && <div className="alert alert-error">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="correo">Correo</label>
            <input
              id="correo"
              type="email"
              value={correo}
              onChange={e => setCorreo(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Contrasena</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit" className="btn-block" disabled={enviando}>
            {enviando ? 'Ingresando...' : 'Ingresar'}
          </button>
        </form>

        </div>
    </div>
  )
}
