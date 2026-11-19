import { defineConfig, devices } from '@playwright/test'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const directorioActual = path.dirname(fileURLToPath(import.meta.url))
const directorioBackend = path.resolve(directorioActual, '../backend')

// En Windows se usa el entorno virtual del backend; en el runner Linux de
// GitHub Actions las dependencias se instalan en el Python del sistema.
const comandoBackend = process.platform === 'win32'
  ? '".\\venv\\Scripts\\python.exe" -m uvicorn app.main:app --host 127.0.0.1 --port 8000'
  : 'python -m uvicorn app.main:app --host 127.0.0.1 --port 8000'

export default defineConfig({
  testDir: './e2e',
  outputDir: './test-results/artifacts',

  // La suite comparte una sola base de datos: se ejecuta en serie para que los
  // datos de prueba de un caso no interfieran con otro.
  fullyParallel: false,
  workers: 1,
  forbidOnly: Boolean(process.env.CI),
  retries: process.env.CI ? 1 : 0,
  timeout: 90_000,
  expect: { timeout: 10_000 },

  reporter: [
    ['list'],
    ['html', { outputFolder: 'playwright-report', open: 'never' }],
    ['json', { outputFile: 'test-results/results.json' }],
  ],

  use: {
    baseURL: 'http://127.0.0.1:5173',
    headless: true,
    locale: 'es-PE',
    timezoneId: 'America/Lima',
    actionTimeout: 15_000,
    navigationTimeout: 45_000,
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },

  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
  ],

  webServer: [
    {
      command: comandoBackend,
      cwd: directorioBackend,
      url: 'http://127.0.0.1:8000/health',
      reuseExistingServer: !process.env.CI,
      timeout: 120_000,
      stdout: 'ignore',
      stderr: 'pipe',
    },
    {
      command: 'npm run dev -- --host 127.0.0.1 --port 5173 --strictPort',
      url: 'http://127.0.0.1:5173',
      reuseExistingServer: !process.env.CI,
      timeout: 120_000,
      stdout: 'ignore',
      stderr: 'pipe',
    },
  ],
})
