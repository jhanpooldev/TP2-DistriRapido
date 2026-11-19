import { test, expect } from '@playwright/test'
import { CREDENCIALES, loginUi } from './utils'

test.describe('Autenticacion y navegacion principal', () => {
  test('muestra el formulario de acceso', async ({ page }) => {
    await page.goto('/')

    await expect(page.getByRole('heading', { name: 'EcoLogistica Lima' })).toBeVisible()
    await expect(page.locator('#correo')).toBeVisible()
    await expect(page.locator('#password')).toBeVisible()
    await expect(page.getByRole('button', { name: 'Ingresar' })).toBeVisible()
  })

  test('rechaza credenciales invalidas con un mensaje controlado', async ({ page }) => {
    await page.goto('/')
    await page.locator('#correo').fill(CREDENCIALES.admin.correo)
    await page.locator('#password').fill('clave-incorrecta')
    await page.getByRole('button', { name: 'Ingresar' }).click()

    await expect(page.getByRole('alert')).toHaveText(/Credenciales invalidas/)
    await expect(page.locator('#correo')).toBeVisible()
  })

  test('exige correo y contrasena antes de enviar', async ({ page }) => {
    await page.goto('/')
    await page.getByRole('button', { name: 'Ingresar' }).click()

    await expect(page.locator('#correo')).toHaveAttribute('required', '')
    await expect(page.locator('#password')).toHaveAttribute('required', '')
    await expect(page.getByRole('heading', { name: 'EcoLogistica Lima' })).toBeVisible()
  })

  test('inicia sesion como operador y muestra las cinco secciones', async ({ page }) => {
    await loginUi(page, CREDENCIALES.operador)

    await expect(page.getByRole('tab', { name: /Pedidos/ })).toBeVisible()
    await expect(page.getByRole('tab', { name: /Rutas/ })).toBeVisible()
    await expect(page.getByRole('tab', { name: /Mapa/ })).toBeVisible()
    await expect(page.getByRole('tab', { name: /Impacto/ })).toBeVisible()
    await expect(page.getByRole('tab', { name: /Vehiculos/ })).toBeVisible()
    await expect(page.locator('.app-usuario span')).toHaveText(/\S+/)
  })

  test('el administrador ve el formulario de alta de vehiculos', async ({ page }) => {
    await loginUi(page, CREDENCIALES.admin)
    await page.getByRole('tab', { name: /Vehiculos/ }).click()

    await expect(page.locator('#vehiculo-placa')).toBeVisible()
    await expect(page.getByRole('button', { name: 'Agregar vehiculo' })).toBeVisible()
  })

  test('el operador no ve el formulario de alta de vehiculos', async ({ page }) => {
    await loginUi(page, CREDENCIALES.operador)
    await page.getByRole('tab', { name: /Vehiculos/ }).click()

    await expect(page.locator('#vehiculo-placa')).toHaveCount(0)
    await expect(page.getByText('Solo un administrador puede agregar vehiculos')).toBeVisible()
  })

  test('cierra la sesion y limpia el token almacenado', async ({ page }) => {
    await loginUi(page, CREDENCIALES.operador)
    await page.getByRole('button', { name: 'Salir' }).click()

    await expect(page.locator('#correo')).toBeVisible()
    const token = await page.evaluate(() => localStorage.getItem('token'))
    expect(token).toBeNull()
  })
})
