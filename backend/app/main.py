import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from backend.app.core.config import settings
from backend.app.routers.auth import router as auth_router

app = FastAPI(
    title="EcoLogística Lima - API de Autenticación MFA y Sesiones",
    description="""
    ## Módulo de Autenticación Multifactor y Gestión Segura de Sesiones
    Plataforma web inteligente de optimización de rutas sostenibles para **DistriRápido S.A.C.**
    
    ### Características de Seguridad:
    * **Autenticación Primaria:** Hashing seguro PBKDF2-HMAC-SHA256 con salt aleatoria (RN-004).
    * **MFA (RFC 6238):** TOTP de 6 dígitos compatible con Google Authenticator / Microsoft Authenticator.
    * **Códigos de Respaldo:** 5 códigos criptográficos de un solo uso para contingencia.
    * **Desafío en 2 Pasos:** Token temporal (`mfa_token`, 5 min) para evitar elevación no autorizada.
    * **Gestión de Sesiones:** JWT con expiración de 8 horas (RN-005) y revocación inmediata en Logout mediante lista negra de JTI.
    * **Protección contra Fuerza Bruta:** Bloqueo de cuenta temporal por 15 minutos tras 3 intentos fallidos consecutivos (RN-002).
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas de autenticación
app.include_router(auth_router)

# Ruta del archivo estático de prueba visual
STATIC_DIR = Path(__file__).resolve().parent / "static"
INDEX_HTML = STATIC_DIR / "index.html"

@app.get("/", response_class=HTMLResponse, summary="Panel visual interactivo de pruebas MFA")
def root_dashboard():
    if INDEX_HTML.exists():
        return FileResponse(INDEX_HTML)
    return HTMLResponse("<h1>EcoLogística Lima - Servidor API Activo</h1><p>Visite <a href='/docs'>/docs</a> para la documentación Swagger.</p>")

@app.get("/api/health", tags=["Monitoreo"], summary="Estado de salud de la API")
def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "env": settings.APP_ENV,
        "mfa_engine": "TOTP RFC 6238",
        "lockout_policy": "3 intentos x 15 minutos (RN-002)"
    }
