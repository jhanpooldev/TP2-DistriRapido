import { test, expect } from '@playwright/test'
import {
  API_BASE,
  CREDENCIALES,
  cabeceras,
  crearPuntosDePrueba,
  limpiarRutaYPuntos,
  loginApi,
  loginUi,
} from './utils'

const RUTA_INEXISTENTE = '00000000-0000-4000-8000-000000000000'

test.describe('Resiliencia y manejo de errores HTTP', () => {
  test('el endpoint de salud responde con la API y la base de datos disponibles', async ({ request }) => {
    const respuesta = await request.get('http://127.0.0.1:8000/health')

    expect(respuesta.status()).toBe(200)
    const cuerpo = await respuesta.json()
    expect(cuerpo.estado).toBe('ok')
    expect(cuerpo.base_datos).toBe('ok')
    expect(cuerpo.version).toBe('1.0.0')
  })

  test('rechaza el acceso sin token con 401', async ({ request }) => {
    const respuesta = await request.get(`${API_BASE}/puntos-entrega`)

    expect(respuesta.status()).toBe(401)
    expect(respuesta.headers()['www-authenticate']).toContain('Bearer')
  })

  test('rechaza un token invalido con 401', async ({ request }) => {
    const respuesta = await request.get(`${API_BASE}/puntos-entrega`, {
      headers: cabeceras('token-invalido-de-prueba'),
    })

    expect(respuesta.status()).toBe(401)
  })

  test('valida las coordenadas fuera de rango con 422 y no crea el pedido', async ({ request }) => {
    const token = await loginApi(request)

    const respuesta = await request.post(`${API_BASE}/puntos-entrega`, {
      headers: cabeceras(token),
      data: {
        direccion: 'Direccion fuera de rango E2E',
        latitud: 91,
        longitud: -77.0,
        peso_kg: 5,
        destinatario: 'E2E-RESILIENCIA-422',
      },
    })

    expect(respuesta.status()).toBe(422)
    const cuerpo = await respuesta.json()
    expect(JSON.stringify(cuerpo.detail)).toContain('latitud')
  })

  test('rechaza una ruta con un solo punto con 400 y limpia el dato de prueba', async ({ request }) => {
    const token = await loginApi(request)
    const { puntos } = await crearPuntosDePrueba(request, token, 1)
    let idRuta = null

    try {
      const respuesta = await request.post(`${API_BASE}/rutas`, {
        headers: cabeceras(token),
        data: { id_vehiculo: 1, punto_ids: [puntos[0].id_punto] },
      })

      if (respuesta.status() === 201) {
        const ruta = await respuesta.json()
        idRuta = ruta.id_ruta
      }

      expect(respuesta.status()).toBe(400)
      const cuerpo = await respuesta.json()
      expect(cuerpo.detail).toContain('al menos 2 puntos')
    } finally {
      await limpiarRutaYPuntos(request, token, idRuta, puntos)
    }
  })

  test('devuelve 404 para una ruta que no existe', async ({ request }) => {
    const token = await loginApi(request)

    const respuesta = await request.get(`${API_BASE}/rutas/${RUTA_INEXISTENTE}`, {
      headers: cabeceras(token),
    })

    expect(respuesta.status()).toBe(404)
    expect((await respuesta.json()).detail).toBe('Ruta no encontrada')
  })

  test('impide duplicar una placa de vehiculo con 400', async ({ request }) => {
    const token = await loginApi(request, CREDENCIALES.admin)
    const listado = await request.get(`${API_BASE}/vehiculos`, { headers: cabeceras(token) })
    expect(listado.status()).toBe(200)

    const vehiculos = await listado.json()
    expect(vehiculos.length).toBeGreaterThan(0)

    const respuesta = await request.post(`${API_BASE}/vehiculos`, {
      headers: cabeceras(token),
      data: {
        placa: vehiculos[0].placa,
        capacidad_kg: 1000,
        factor_emision_co2: 2.68,
        consumo_litros_km: 0.12,
        velocidad_promedio_kmh: 35,
        tipo_combustible: 'Diesel',
      },
    })

    expect(respuesta.status()).toBe(400)
    expect((await respuesta.json()).detail).toBe('Placa ya existe')
  })

  test('devuelve cabeceras de endurecimiento y conserva el identificador de correlacion', async ({ request }) => {
    const identificador = 'e2e-resiliencia-0123456789'
    const respuesta = await request.get(`${API_BASE}/health`, {
      headers: { 'X-Request-ID': identificador },
    })

    expect(respuesta.status()).toBe(200)
    const cabecerasRespuesta = respuesta.headers()
    expect(cabecerasRespuesta['x-request-id']).toBe(identificador)
    expect(cabecerasRespuesta['x-content-type-options']).toBe('nosniff')
    expect(cabecerasRespuesta['x-frame-options']).toBe('DENY')
    expect(cabecerasRespuesta['referrer-policy']).toBe('no-referrer')
    expect(cabecerasRespuesta['permissions-policy']).toContain('geolocation=(self)')
  })

  test('no cachea la autenticacion y cachea solo el catalogo de vehiculos', async ({ request }) => {
    const login = await request.post(`${API_BASE}/auth/login`, {
      form: {
        correo: CREDENCIALES.operador.correo,
        password: CREDENCIALES.operador.password,
      },
    })
    expect(login.status()).toBe(200)
    expect(login.headers()['cache-control']).toBe('no-store')

    const token = (await login.json()).access_token
    const vehiculos = await request.get(`${API_BASE}/vehiculos`, { headers: cabeceras(token) })
    expect(vehiculos.status()).toBe(200)
    expect(vehiculos.headers()['cache-control']).toBe('private, max-age=300')
  })

  test('la interfaz informa cuando el backend no responde', async ({ page }) => {
    await page.route('**/api/v1/puntos-entrega**', (ruta) => ruta.abort('failed'))

    await loginUi(page)

    await expect(page.getByRole('alert')).toContainText('No se pudo conectar con el servidor')
    await expect(page.getByRole('tab', { name: /Pedidos/ })).toBeVisible()
  })

  test('la interfaz muestra el detalle de un error 500 del backend', async ({ page }) => {
    await page.route('**/api/v1/puntos-entrega**', (ruta) =>
      ruta.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({ detail: 'Fallo simulado del servidor' }),
      })
    )

    await loginUi(page)

    await expect(page.getByRole('alert')).toContainText('Fallo simulado del servidor')
  })
})
