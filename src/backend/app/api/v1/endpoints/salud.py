"""Endpoint de salud del servicio (SPECS.md: GET /api/v1/health)."""
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.database import get_db

router = APIRouter()


@router.get("/health")
def health(response: Response, db: Session = Depends(get_db)):
    """Comprueba que la API y la base de datos responden.

    Devuelve 503 si la base de datos no esta disponible, de modo que un
    despliegue unhealthy no se confunda con uno sano.
    """
    try:
        db.execute(text("SELECT 1"))
    except SQLAlchemyError:
        db.rollback()
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"estado": "degradado", "base_datos": "error", "version": "1.0.0"}

    return {"estado": "ok", "base_datos": "ok", "version": "1.0.0"}