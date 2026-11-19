import { test, expect } from '@playwright/test'
import { readFile } from 'node:fs/promises'
import {
  CREDENCIALES,
  API_BASE,
  cabeceras,
  crearPuntosDePrueba,
  crearRuta,
  eliminarPunto,
  eliminarRuta,
  limpiarRutaYPuntos,
  loginApi,
  loginUi,
  obtenerVehiculoId,
  prefijoUnico,
} from './utils'

test.describe('Flujos de negocio de punta a punta', () => {
  test('registra un pedido desde la interfaz y lo muestra en la tabla', async ({ page, request }) => {
    const token = await loginApi(request)
    const destinatario = prefijoUnico('E2E-UI')

    try {
      await loginUi(page)
      await page.locator('#punto-direccion').fill('Av. Prueba E2E 123, Lima')
      await page.locator('#punto-latitud').fill('-12.115')
      await page.locator('#punto-longitud').fill('-76.970')
      await page.locator('#punto-peso').fill('7.5')
      await page.locator('#punto-destinatario').fill(destinatario)
      await page.getByRole('button', { name: 'Registrar pedido' }).click()

      await expect(page.getByText('Pedido registrado. Ya aparece en la pestaña Rutas')).toBeVisible()
      await expect(page.getByRole('cell', { name: destinatario })).toBeVisible()
    } finally {
      const listado = await request.get(`${API_BASE}/puntos-entrega`, {
        headers: cabeceras(token),
        params: { limit: 100 },
      })
      const { puntos } = await listado.json()
      const creado = puntos.find((punto) => punto.destinatario === destinatario)
      if (creado) await eliminarPunto(request, token, creado.id_punto)
    }
  })

  test('valida los campos obligatorios antes de enviar el formulario', async ({ page }) => {
    await loginUi(page)
    await page.getByRole('button', { name: 'Registrar pedido' }).click()

    for (const selector of ['#punto-direccion', '#punto-latitud', '#punto-longitud', '#punto-peso', '#punto-destinatario']) {
      await expect(page.locator(selector)).toHaveAttribute('required', '')
    }
    await expect(page.getByText('Pedido registrado. Ya aparece en la pestaña Rutas')).toHaveCount(0)
  })

  test('calcula, guarda y exporta una ruta con dos pedidos', async ({ page, request }) => {
    const token = await loginApi(request)
    const idVehiculo = await obtenerVehiculoId(request, token)
    const { prefijo, puntos } = await crearPuntosDePrueba(request, token, 2)
    let idRuta = null

    try {
      await loginUi(page)
      await page.getByRole('tab', { name: /Rutas/ }).click()
      await expect(page.locator('#busqueda-pedidos')).toBeVisible()
      await page.locator('#busqueda-pedidos').fill(prefijo)

      const disponibles = page.locator('.sel-panel > div').first()
      await expect(disponibles.locator('.sel-item')).toHaveCount(2)
      await disponibles.getByRole('button', { name: 'Agregar' }).first().click()
      await expect(disponibles.locator('.sel-item')).toHaveCount(1)
      await disponibles.getByRole('button', { name: 'Agregar' }).first().click()
      await expect(disponibles.locator('.sel-item')).toHaveCount(0)

      await expect(page.getByText(/2 pedidos seleccionados/)).toBeVisible()
      await page.getByRole('button', { name: 'Optimizar (simular)' }).click()

      await expect(page.getByText(/Vista previa: esta ruta todavia no esta guardada/)).toBeVisible()
      await expect(page.getByRole('heading', { name: 'Ruta optimizada (simulacion)' })).toBeVisible()
      await expect(page.getByText('km', { exact: true })).toBeVisible()
      await expect(page.getByText('min', { exact: true })).toBeVisible()
      await expect(page.getByText('kg CO2', { exact: true })).toBeVisible()

      const [respuestaRuta] = await Promise.all([
        page.waitForResponse(
          (respuesta) => respuesta.url().endsWith('/api/v1/rutas') && respuesta.request().method() === 'POST'
        ),
        page.getByRole('button', { name: 'Confirmar y guardar' }).click(),
      ])
      const ruta = await respuestaRuta.json()
      idRuta = ruta.id_ruta

      await expect(page.getByText('Ruta confirmada y guardada.')).toBeVisible()
      await expect(page.getByRole('heading', { name: /Ruta [0-9a-f]{8}/ })).toBeVisible()

      const [descarga] = await Promise.all([
        page.waitForEvent('download'),
        page.getByRole('button', { name: /Exportar resumen/ }).click(),
      ])
      expect(descarga.suggestedFilename()).toMatch(/^ruta-[0-9a-f]{8}-\d{8}\.csv$/)
      const contenido = await readFile(await descarga.path(), 'utf8')
      expect(contenido).toContain(prefijo)
      expect(contenido).toContain('Orden,Destinatario')
    } finally {
      await limpiarRutaYPuntos(request, token, idRuta, puntos)
    }
  })

  test('bloquea el calculo cuando la seleccion tiene un solo pedido', async ({ page, request }) => {
    const token = await loginApi(request)
    const { prefijo, puntos } = await crearPuntosDePrueba(request, token, 2)

    try {
      await loginUi(page)
      await page.getByRole('tab', { name: /Rutas/ }).click()
      await page.locator('#busqueda-pedidos').fill(prefijo)
      const disponibles = page.locator('.sel-panel > div').first()
      await disponibles.getByRole('button', { name: 'Agregar' }).first().click()

      await expect(page.getByText(/Falta al menos 1 pedido: una ruta necesita 2 puntos/)).toBeVisible()
      await expect(page.getByRole('button', { name: 'Optimizar (simular)' })).toBeDisabled()
      await expect(page.getByRole('button', { name: 'Confirmar y guardar' })).toBeDisabled()
    } finally {
      await limpiarRutaYPuntos(request, token, null, puntos)
    }
  })

  test('informa cuando el filtro de rutas no tiene resultados', async ({ page }) => {
    await loginUi(page)
    await page.getByRole('tab', { name: /Rutas/ }).click()
    await page.locator('#filtro-desde').fill('2099-01-01')
    await page.getByRole('button', { name: 'Aplicar filtro' }).click()

    await expect(page.locator('p.vacio')).toContainText('Ninguna ruta coincide con el filtro aplicado.')
  })

  test('edita una ruta guardada y recalcula sus indicadores', async ({ page, request }) => {
    const token = await loginApi(request)
    const idVehiculo = await obtenerVehiculoId(request, token)
    const { puntos } = await crearPuntosDePrueba(request, token, 2)
    const ruta = await crearRuta(request, token, idVehiculo, puntos.map((punto) => punto.id_punto))
    let idRuta = ruta.id_ruta

    try {
      await loginUi(page)
      await page.getByRole('tab', { name: /Rutas/ }).click()
      const fila = page.getByRole('row').filter({ hasText: ruta.id_ruta.slice(0, 8) })
      await expect(fila).toBeVisible()
      await fila.getByRole('button', { name: /Editar la ruta/ }).click()

      await expect(page.getByRole('heading', { name: /Editando la ruta/ })).toBeVisible()
      await page.getByRole('button', { name: 'Guardar y recalcular' }).click()
      await expect(page.getByText('Ruta actualizada y recalculada con los puntos seleccionados.')).toBeVisible()
    } finally {
      await limpiarRutaYPuntos(request, token, idRuta, puntos)
    }
  })

  test('elimina una ruta guardada y la borra del sistema', async ({ page, request }) => {
    const token = await loginApi(request)
    const idVehiculo = await obtenerVehiculoId(request, token)
    const { puntos } = await crearPuntosDePrueba(request, token, 2)
    const ruta = await crearRuta(request, token, idVehiculo, puntos.map((punto) => punto.id_punto))

    try {
      await loginUi(page)
      await page.getByRole('tab', { name: /Rutas/ }).click()
      const fila = page.getByRole('row').filter({ hasText: ruta.id_ruta.slice(0, 8) })
      await expect(fila).toBeVisible()

      page.once('dialog', (dialogo) => dialogo.accept())
      await fila.getByRole('button', { name: /Eliminar la ruta/ }).click()
      await expect(page.getByText('Ruta eliminada.')).toBeVisible()

      const consulta = await request.get(`${API_BASE}/rutas/${ruta.id_ruta}`, {
        headers: cabeceras(token),
      })
      expect(consulta.status()).toBe(404)
    } finally {
      await limpiarRutaYPuntos(request, token, ruta.id_ruta, puntos)
    }
  })
})
