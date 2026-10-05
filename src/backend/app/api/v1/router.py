from fastapi import APIRouter
from app.api.v1.endpoints import auth, geocoding, puntos, rutas, vehiculos, salud

api_router = APIRouter()

api_router.include_router(salud.router, prefix="", tags=["salud"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(puntos.router, prefix="/puntos-entrega", tags=["puntos-entrega"])
api_router.include_router(rutas.router, prefix="/rutas", tags=["rutas"])
api_router.include_router(vehiculos.router, prefix="/vehiculos", tags=["vehiculos"])
api_router.include_router(geocoding.router, prefix="/geocoding", tags=["geocoding"])