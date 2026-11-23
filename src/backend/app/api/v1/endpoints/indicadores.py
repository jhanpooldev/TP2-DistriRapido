from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.v1.endpoints.dependencies import get_current_user
from app.core.database import get_db
from app.models import Ruta, RutaPunto
from app.schemas import IndicadoresResponse, IndicadoresSostenibilidadResponse
from app.services.indicadores import (
    calcular_indicadores_logisticos,
    calcular_indicadores_sostenibilidad,
)

router = APIRouter()

# Según la matriz de permisos, la lectura de indicadores está permitida a
# Administrador, Operador y Gerente. El panel del gerente consume estos mismos
# totales globales, no un subconjunto por operador.
_FILTRO_RUTAS_CONFIRMADAS = func.lower(Ruta.estado) == "confirmada"


@router.get("", response_model=IndicadoresResponse)
def get_indicadores(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """RF-013 / RN-020: cantidad de rutas, distancia y emisiones totales."""
    cantidad, distancia, emisiones = (
        db.query(
            func.count(Ruta.id_ruta),
            func.coalesce(func.sum(Ruta.distancia_total_km), 0.0),
            func.coalesce(func.sum(Ruta.co2_estimado_kg), 0.0),
        )
        .filter(_FILTRO_RUTAS_CONFIRMADAS)
        .one()
    )
    return IndicadoresResponse(
        **calcular_indicadores_logisticos(cantidad, distancia, emisiones)
    )


@router.get("/sostenibilidad", response_model=IndicadoresSostenibilidadResponse)
def get_indicadores_sostenibilidad(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """RF-012 / RN-019: emisiones totales, por entrega y ahorro de CO₂."""
    emisiones, sin_optimizar = (
        db.query(
            func.coalesce(func.sum(Ruta.co2_estimado_kg), 0.0),
            func.coalesce(func.sum(Ruta.co2_sin_optimizar_kg), 0.0),
        )
        .filter(_FILTRO_RUTAS_CONFIRMADAS)
        .one()
    )
    entregas = (
        db.query(func.count(RutaPunto.id_ruta_punto))
        .join(Ruta, Ruta.id_ruta == RutaPunto.id_ruta)
        .filter(_FILTRO_RUTAS_CONFIRMADAS)
        .scalar()
        or 0
    )
    return IndicadoresSostenibilidadResponse(
        **calcular_indicadores_sostenibilidad(emisiones, sin_optimizar, entregas)
    )
