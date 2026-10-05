import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from backend.app.core.config import settings
from backend.app.routers.auth import router as auth_router
from backend.app.routers.rutas import router as rutas_router

app = FastAPI(
    title="EcoLogística Lima - Optimizador de Rutas Sostenibles",
    description="""
    ## Sistema Web Inteligente de Distribución y Rutas Sostenibles
    Plataforma web para **DistriRápido S.A.C.** (Lima Metropolitana).
    
    ### Módulos Principales:
    * **Seguridad y MFA:** TOTP (RFC 6238), JWT de 8 horas (`RN-005`), revocación en logout y bloqueo `RN-002`.
    * **Optimización de Rutas:** Algoritmos combinatorios (TSP/VRP) para reducción de kilometraje y tiempos de entrega.
    * **Métricas de Sostenibilidad:** Estimación de huella de carbono y ahorro de emisiones de CO₂.
    """,
    version="1.1.0",
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

# Incluir rutas de módulos
app.include_router(auth_router)
app.include_router(rutas_router)

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
