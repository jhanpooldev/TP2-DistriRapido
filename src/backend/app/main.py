from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import uuid

from sqlalchemy.exc import SQLAlchemyError

from app.core.database import init_db
from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.security import hash_password
from app.models import Rol, Usuario, ParametrosVehiculo
from app.core.database import SessionLocal

settings = get_settings()
logger = logging.getLogger(__name__)

def seed_data():
    db = SessionLocal()
    try:
        if not db.query(Rol).first():
            roles = [
                Rol(nombre="Administrador", descripcion="Acceso total al sistema"),
                Rol(nombre="Operador Logístico", descripcion="Gestiona puntos y rutas"),
                Rol(nombre="Gerente", descripcion="Visualiza reportes"),
            ]
            db.add_all(roles)
            db.commit()

        if not db.query(Usuario).first():
            admin_rol = db.query(Rol).filter(Rol.nombre == "Administrador").first()
            operador_rol = db.query(Rol).filter(Rol.nombre == "Operador Logístico").first()
            admin = Usuario(
                nombre="Admin DistriRapido",
                correo="admin@distrirapido.com",
                contrasena_hash=hash_password("admin123"),
                id_rol=admin_rol.id_rol,
            )
            operador = Usuario(
                nombre="Operador Principal",
                correo="operador@distrirapido.com",
                contrasena_hash=hash_password("operador123"),
                id_rol=operador_rol.id_rol,
            )
            db.add_all([admin, operador])
            db.commit()

        if not db.query(ParametrosVehiculo).first():
            vehiculo = ParametrosVehiculo(
                placa="ABC-123",
                capacidad_kg=1000.0,
                factor_emision_co2=2.68,
                consumo_litros_km=0.12,
                velocidad_promedio_kmh=35.0,
                tipo_combustible="Diesel",
            )
            db.add(vehiculo)
            db.commit()
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # La API debe arrancar aunque la base de datos no este disponible: de lo
    # contrario /health no podria reportar 503 justo cuando mas se necesita.
    try:
        init_db()
        seed_data()
    except SQLAlchemyError as exc:
        logger.error("No se pudo inicializar la base de datos: %s", exc)
    yield

app = FastAPI(
    title="EcoLogística Lima - API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

# Se reutiliza el mismo handler que /api/v1/health (SPECS.md L268) para que
# ambas rutas respondan con el mismo formato y no se puedan divergir.
from app.api.v1.endpoints.salud import health

app.add_api_route("/health", health, methods=["GET"], tags=["salud"])

@app.get("/")
def root():
    return {"message": "EcoLogística Lima API - v1.0.0", "docs": "/docs"}