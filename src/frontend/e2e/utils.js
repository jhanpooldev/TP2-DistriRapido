import { expect } from '@playwright/test'

export const API_BASE = process.env.E2E_API_URL || 'http://127.0.0.1:8000/api/v1'

export const CREDENCIALES = {
  admin: { correo: 'admin@distrirapido.com', password: 'admin123' },
  operador: { correo: 'operador@distrirapido.com', password: 'operador123' },
}

export function prefijoUnico(etiqueta = 'E2E') {
  return `${etiqueta}-${Date.now()}-${Math.random().toString(16).slice(2, 8)}`
}

export function cabeceras(token) {
  return { Authorization: `Bearer ${token}` }
}

export async function loginApi(request, credenciales = CREDENCIALES.operador) {
  const respuesta = await request.post(`${API_BASE}/auth/login`, {
    form: { correo: credenciales.correo, password: credenciales.password },
  })
  if (!respuesta.ok()) {
    throw new Error(`Login API fallo (${respuesta.status()}): ${await respuesta.text()}`)
  }
  const cuerpo = await respuesta.json()
  return cuerpo.access_token
}

export async function loginUi(page, credenciales = CREDENCIALES.operador) {
  await page.goto('/')
  await page.locator('#correo').fill(credenciales.correo)
  await page.locator('#password').fill(credenciales.password)
  await page.getByRole('button', { name: 'Ingresar' }).click()
  await expect(page.getByRole('tab', { name: /Pedidos/ })).toBeVisible()
}

export async function obtenerVehiculoId(request, token) {
  const respuesta = await request.get(`${API_BASE}/vehiculos`, { headers: cabeceras(token) })
  if (!respuesta.ok()) {
    throw new Error(`No se pudo leer el catalogo de vehiculos (${respuesta.status()})`)
  }
  const vehiculos = await respuesta.json()
  if (!vehiculos.length) {
    throw new Error('No hay vehiculos registrados para ejecutar la prueba')
  }
  return vehiculos[0].id_vehiculo
}

export async function crearPunto(request, token, datos) {
  const respuesta = await request.post(`${API_BASE}/puntos-entrega`, {
    headers: cabeceras(token),
    data: datos,
  })
  if (!respuesta.ok()) {
    throw new Error(`No se pudo crear el punto (${respuesta.status()}): ${await respuesta.text()}`)
  }
  return respuesta.json()
}

export async function crearPuntosDePrueba(request, token, cantidad = 2) {
  const prefijo = prefijoUnico('E2E-PUNTO')
  const puntos = []
  for (let i = 0; i < cantidad; i += 1) {
    const punto = await crearPunto(request, token, {
      direccion: `Calle de prueba ${prefijo} ${i + 1}`,
      latitud: -12.10 - i * 0.01,
      longitud: -77.00 + i * 0.01,
      peso_kg: 5 + i,
      destinatario: `${prefijo}-${i + 1}`,
    })
    puntos.push(punto)
  }
  return { prefijo, puntos }
}

export async function crearRuta(request, token, idVehiculo, puntoIds) {
  const respuesta = await request.post(`${API_BASE}/rutas`, {
    headers: cabeceras(token),
    data: { id_vehiculo: idVehiculo, punto_ids: puntoIds },
  })
  if (!respuesta.ok()) {
    throw new Error(`No se pudo crear la ruta (${respuesta.status()}): ${await respuesta.text()}`)
  }
  return respuesta.json()
}

export async function eliminarRuta(request, token, idRuta) {
  const respuesta = await request.delete(`${API_BASE}/rutas/${idRuta}`, { headers: cabeceras(token) })
  if (![204, 404].includes(respuesta.status())) {
    throw new Error(`No se pudo limpiar la ruta ${idRuta} (${respuesta.status()})`)
  }
}

export async function eliminarPunto(request, token, idPunto) {
  const respuesta = await request.delete(`${API_BASE}/puntos-entrega/${idPunto}`, {
    headers: cabeceras(token),
  })
  // 400: el punto ya pertenece a una ruta; el caso de prueba debe borrar la
  // ruta antes que sus puntos. Se informa para no ocultar una limpieza fallida.
  if (![204, 404].includes(respuesta.status())) {
    throw new Error(`No se pudo limpiar el punto ${idPunto} (${respuesta.status()})`)
  }
}

export async function buscarPuntoPorDestinatario(request, token, destinatario) {
  const respuesta = await request.get(`${API_BASE}/puntos-entrega`, {
    headers: cabeceras(token),
    params: { limit: 100 },
  })
  if (!respuesta.ok()) {
    throw new Error(`No se pudo listar los puntos (${respuesta.status()})`)
  }
  const cuerpo = await respuesta.json()
  return cuerpo.puntos.find((punto) => punto.destinatario === destinatario) || null
}

export async function limpiarRutaYPuntos(request, token, idRuta, puntos) {
  if (idRuta) await eliminarRuta(request, token, idRuta)
  for (const punto of puntos) {
    await eliminarPunto(request, token, punto.id_punto)
  }
}
