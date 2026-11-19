import { test, expect } from '@playwright/test'
import { mkdir, writeFile } from 'node:fs/promises'
import path from 'node:path'
import { API_BASE, CREDENCIALES, cabeceras, loginApi, loginUi } from './utils'

const DIRECTORIO_RESULTADOS = path.resolve(process.cwd(), 'test-results')
const URL_FRONTEND = 'http://127.0.0.1:5173/'

// El observador se instala antes de navegar para no perder el LCP. En los
// navegadores que no exponen largest-contentful-paint queda en 0 y se reporta
// como no disponible en lugar de inventar un valor.
function observadorLcp() {
  window.__lcp = 0
  try {
    new PerformanceObserver((lista) => {
      const entradas = lista.getEntries()
      const ultima = entradas[entradas.length - 1]
      if (ultima) window.__lcp = ultima.startTime
    }).observe({ type: 'largest-contentful-paint', buffered: true })
  } catch {
    window.__lcp = 0
  }
}

async function medirNavegacion(page) {
  return page.evaluate(() => {
    const navegacion = performance.getEntriesByType('navigation')[0]
    const pintura = performance.getEntriesByType('paint')
    const fcp = pintura.find((entrada) => entrada.name === 'first-contentful-paint')
    const lcp = Number(window.__lcp || 0)

    return {
      ttfbMs: navegacion ? Math.round(navegacion.responseStart) : null,
      fcpMs: fcp ? Math.round(fcp.startTime) : null,
      lcpMs: lcp > 0 ? Math.round(lcp) : null,
      domContentLoadedMs: navegacion ? Math.round(navegacion.domContentLoadedEventEnd) : null,
      loadMs: navegacion ? Math.round(navegacion.loadEventEnd) : null,
    }
  })
}

async function medirApi(request, metodo, url, opciones = {}) {
  const inicio = Date.now()
  const respuesta = metodo === 'post'
    ? await request.post(url, opciones)
    : await request.get(url, opciones)
  return { ms: Date.now() - inicio, status: respuesta.status() }
}

test.describe('Rendimiento y tiempos de respuesta', () => {
  test('mide TTFB, FCP, LCP y los tiempos de la API', async ({ page, request, browser }, testInfo) => {
    const proyecto = testInfo.project.name
    const token = await loginApi(request)

    const api = {
      health: await medirApi(request, 'get', 'http://127.0.0.1:8000/health'),
      login: await medirApi(request, 'post', `${API_BASE}/auth/login`, {
        form: {
          correo: CREDENCIALES.operador.correo,
          password: CREDENCIALES.operador.password,
        },
      }),
      puntos: await medirApi(request, 'get', `${API_BASE}/puntos-entrega?page=1&limit=12`, {
        headers: cabeceras(token),
      }),
      rutas: await medirApi(request, 'get', `${API_BASE}/rutas?page=1&limit=12`, {
        headers: cabeceras(token),
      }),
      vehiculos: await medirApi(request, 'get', `${API_BASE}/vehiculos`, {
        headers: cabeceras(token),
      }),
    }

    // Calentamiento: la primera peticion a Vite compila dependencias. Se mide
    // la segunda carga para reportar el comportamiento estable del entorno.
    await page.addInitScript(observadorLcp)
    await page.goto(URL_FRONTEND, { waitUntil: 'load' })
    await expect(page.locator('#correo')).toBeVisible()
    await page.reload({ waitUntil: 'load' })
    await expect(page.locator('#correo')).toBeVisible()
    await page.waitForTimeout(1200)
    const login = await medirNavegacion(page)

    await loginUi(page)
    const estadoSesion = await page.context().storageState()

    // Contexto nuevo para medir el panel sin la cache del contexto de login.
    const contextoPanel = await browser.newContext({
      storageState: estadoSesion,
      locale: 'es-PE',
      timezoneId: 'America/Lima',
      viewport: { width: 1280, height: 720 },
    })
    const paginaPanel = await contextoPanel.newPage()
    await paginaPanel.addInitScript(observadorLcp)
    await paginaPanel.goto(URL_FRONTEND, { waitUntil: 'load' })
    await expect(paginaPanel.getByRole('tab', { name: /Pedidos/ })).toBeVisible({ timeout: 30_000 })
    await paginaPanel.waitForTimeout(1200)
    const panel = await medirNavegacion(paginaPanel)
    const userAgent = await paginaPanel.evaluate(() => navigator.userAgent)
    await contextoPanel.close()

    const datos = {
      proyecto,
      fecha: new Date().toISOString(),
      url: URL_FRONTEND,
      userAgent,
      viewport: { width: 1280, height: 720 },
      navegacion: { login, panel },
      api,
    }

    await mkdir(DIRECTORIO_RESULTADOS, { recursive: true })
    const archivo = path.join(DIRECTORIO_RESULTADOS, `performance-${proyecto}.json`)
    await writeFile(archivo, `${JSON.stringify(datos, null, 2)}\n`, 'utf8')
    await testInfo.attach(`performance-${proyecto}.json`, {
      body: JSON.stringify(datos, null, 2),
      contentType: 'application/json',
    })

    expect(login.ttfbMs).toBeGreaterThan(0)
    expect(login.fcpMs).toBeGreaterThan(0)
    expect(panel.ttfbMs).toBeGreaterThan(0)
    expect(panel.fcpMs).toBeGreaterThan(0)

    if (login.lcpMs !== null) expect(login.lcpMs).toBeLessThan(8000)
    if (panel.lcpMs !== null) expect(panel.lcpMs).toBeLessThan(8000)

    expect(login.ttfbMs).toBeLessThan(3000)
    expect(panel.ttfbMs).toBeLessThan(3000)
    expect(login.fcpMs).toBeLessThan(5000)
    expect(panel.fcpMs).toBeLessThan(5000)

    for (const [nombre, medicion] of Object.entries(api)) {
      expect(medicion.status, `La API ${nombre} debe responder 2xx`).toBeLessThan(400)
      expect(medicion.ms, `La API ${nombre} debe responder en menos de 5 s`).toBeLessThan(5000)
    }
  })
})
