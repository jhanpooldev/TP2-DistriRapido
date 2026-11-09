from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import Optional
import uuid

from app.core.database import get_db
from app.models import PuntoEntrega, RutaPunto
from app.schemas import PuntoEntregaCreate, PuntoEntregaResponse, PuntoEntregaList
from app.api.v1.endpoints.dependencies import get_current_operador

router = APIRouter()

# Tamano de pagina por defecto. El maximo evita que un cliente pida toda la
# tabla y anule el beneficio de la paginacion.
PAGE_SIZE_DEFAULT = 12
PAGE_SIZE_MAX = 100

@router.post("", response_model=PuntoEntregaResponse, status_code=status.HTTP_201_CREATED)
def create_punto(punto: PuntoEntregaCreate, db: Session = Depends(get_db), operador = Depends(get_current_operador)):
    db_punto = PuntoEntrega(
        direccion=punto.direccion,
        latitud=punto.latitud,
        longitud=punto.longitud,
        peso_kg=punto.peso_kg,
        destinatario=punto.destinatario,
        id_operador=operador.id_usuario,
    )
    db.add(db_punto)
    db.commit()
    db.refresh(db_punto)
    return db_punto

@router.get("", response_model=PuntoEntregaList)
def list_puntos(
    page: int = Query(1, ge=1),
    limit: int = Query(PAGE_SIZE_DEFAULT, ge=1, le=PAGE_SIZE_MAX),
    skip: Optional[int] = Query(None, ge=0, description="Offset explicito; reemplaza a page si se envia"),
    db: Session = Depends(get_db),
    operador = Depends(get_current_operador),
):
    """Listado paginado por operador.

    `page`/`limit` son la interfaz recomendada. `skip` se conserva para los
    scripts existentes que ya lo usaban.
    """
    filtro = PuntoEntrega.id_operador == operador.id_usuario
    total = db.query(func.count(PuntoEntrega.id_punto)).filter(filtro).scalar() or 0
    offset = skip if skip is not None else (page - 1) * limit

    puntos = (
        db.query(PuntoEntrega)
        .filter(filtro)
        .order_by(PuntoEntrega.fecha_registro.desc(), PuntoEntrega.id_punto)
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "puntos": puntos,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit,
    }

@router.get("/{punto_id}", response_model=PuntoEntregaResponse)
def get_punto(punto_id: uuid.UUID, db: Session = Depends(get_db), operador = Depends(get_current_operador)):
    punto = db.query(PuntoEntrega).filter(
        PuntoEntrega.id_punto == punto_id,
        PuntoEntrega.id_operador == operador.id_usuario
    ).first()
    if not punto:
        raise HTTPException(status_code=404, detail="Punto no encontrado")
    return punto

@router.put("/{punto_id}", response_model=PuntoEntregaResponse)
def update_punto(
    punto_id: uuid.UUID,
    punto: PuntoEntregaCreate,
    db: Session = Depends(get_db),
    operador = Depends(get_current_operador),
):
    """RN-009: un punto que ya pertenece a una ruta guardada no se modifica."""
    db_punto = db.query(PuntoEntrega).filter(
        PuntoEntrega.id_punto == punto_id,
        PuntoEntrega.id_operador == operador.id_usuario
    ).first()
    if not db_punto:
        raise HTTPException(status_code=404, detail="Punto no encontrado")

    if _esta_en_alguna_ruta(db, db_punto.id_punto):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El punto ya pertenece a una ruta guardada y no puede modificarse. "
                   "Edita la ruta desde la pestana Rutas.",
        )

    db_punto.direccion = punto.direccion
    db_punto.latitud = punto.latitud
    db_punto.longitud = punto.longitud
    db_punto.peso_kg = punto.peso_kg
    db_punto.destinatario = punto.destinatario
    db.commit()
    db.refresh(db_punto)
    return db_punto

@router.delete("/{punto_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_punto(punto_id: uuid.UUID, db: Session = Depends(get_db), operador = Depends(get_current_operador)):
    punto = db.query(PuntoEntrega).filter(
        PuntoEntrega.id_punto == punto_id,
        PuntoEntrega.id_operador == operador.id_usuario
    ).first()
    if not punto:
        raise HTTPException(status_code=404, detail="Punto no encontrado")

    # Sin esta comprobacion el borrado dejaba filas en ruta_puntos apuntando a un
    # punto inexistente, lo que rompia la lectura de la ruta con un error 500.
    if _esta_en_alguna_ruta(db, punto.id_punto):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El punto pertenece a una ruta guardada. Elimina la ruta primero "
                   "o quitale el punto desde la edicion de la ruta.",
        )

    db.delete(punto)
    db.commit()

def _esta_en_alguna_ruta(db: Session, punto_id) -> bool:
    return db.query(RutaPunto.id_ruta).filter(RutaPunto.id_punto == punto_id).first() is not None