import { test, expect } from '@playwright/test'
import { mkdir } from 'node:fs/promises'
import path from 'node:path'
import {
  CREDENCIALES,
  crearPuntosDePrueba,
  crearRuta,
  limpiarRutaYPuntos,
  loginApi,
  loginUi,
  obtenerVehiculoId,
} from './utils'

const DIRECTORIO_EVIDENCIAS = path.resolve(
  process.cwd(),
  '../../docs/05 Evidencias/playwright-sprint4'
)

test.describe('Evidencias visuales del Sprint 4', () => {
  test.skip(({ browserName }) => browserName !== 'chromium', 'Las capturas se generan solo en Chromium')

  test('captura las pantallas principales con datos reales', async ({ page, request }) => {
    await mkdir(DIRECTORIO_EVIDENCIAS, { recursive: true })

    const capturar = (nombre) =>
      page.screenshot({
        path: path.join(DIRECTORIO_EVIDENCIAS, nombre),
        fullPage: true,
        animations: 'disabled',
      })

    const token = await loginApi(request)
    const idVehiculo = await obtenerVehiculoId(request, token)
    const { puntos } = await crearPuntosDePrueba(request, token, 2)
    let ruta = null

    try {
      ruta = await crearRuta(request, token, idVehiculo, puntos.map((punto) => punto.id_punto))

      await page.goto('/')
      await expect(page.getByRole('heading', { name: 'EcoLogistica Lima' })).toBeVisible()
      await capturar('01-login.png')

      await loginUi(page, CREDENCIALES.operador)
      await expect(page.getByRole('heading', { name: 'Pedidos registrados' })).toBeVisible()
      await capturar('02-panel-pedidos.png')

      await page.getByRole('tab', { name: /Rutas/ }).click()
      await expect(page.locator('#busqueda-pedidos')).toBeVisible()
      await expect(page.getByRole('heading', { name: 'Rutas guardadas' })).toBeVisible()
      await capturar('03-panel-rutas.png')

      await page.getByRole('tab', { name: /Mapa/ }).click()
      await page.locator('#mapa-ruta').selectOption(ruta.id_ruta)
      await expect(page.getByRole('heading', { name: /Ruta [0-9a-f]{8}/ })).toBeVisible()
      await expect(page.getByRole('region', { name: /Mapa de la ruta/ })).toBeVisible()
      await page.waitForTimeout(2500)
      await capturar('04-panel-mapa.png')

      await page.getByRole('tab', { name: /Impacto/ }).click()
      await page.locator('#ruta-impacto').selectOption(ruta.id_ruta)
      await expect(page.getByRole('heading', { name: 'Comparacion de emisiones' })).toBeVisible()
      await capturar('05-panel-impacto.png')

      await page.getByRole('tab', { name: /Vehiculos/ }).click()
      await expect(page.getByRole('heading', { name: 'Flota registrada' })).toBeVisible()
      await capturar('06-panel-vehiculos-operador.png')

      await page.getByRole('button', { name: 'Salir' }).click()
      await loginUi(page, CREDENCIALES.admin)
      await page.getByRole('tab', { name: /Vehiculos/ }).click()
      await expect(page.getByRole('heading', { name: 'Agregar vehiculo' })).toBeVisible()
      await capturar('07-panel-vehiculos-administrador.png')
    } finally {
      await limpiarRutaYPuntos(request, token, ruta?.id_ruta, puntos)
    }
  })
})
