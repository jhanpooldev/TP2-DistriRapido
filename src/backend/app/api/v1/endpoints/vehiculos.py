from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models import ParametrosVehiculo
from app.schemas import VehiculoCreate, VehiculoResponse
from app.api.v1.endpoints.dependencies import get_current_user, get_current_admin

router = APIRouter()

@router.post("", response_model=VehiculoResponse, status_code=status.HTTP_201_CREATED)
def create_vehiculo(vehiculo: VehiculoCreate, db: Session = Depends(get_db), admin = Depends(get_current_admin)):
    if db.query(ParametrosVehiculo).filter(ParametrosVehiculo.placa == vehiculo.placa).first():
        raise HTTPException(status_code=400, detail="Placa ya existe")
    db_veh = ParametrosVehiculo(**vehiculo.model_dump())
    db.add(db_veh)
    db.commit()
    db.refresh(db_veh)
    return db_veh

@router.get("", response_model=List[VehiculoResponse])
def list_vehiculos(db: Session = Depends(get_db), user = Depends(get_current_user)):
    return db.query(ParametrosVehiculo).all()

@router.get("/{vehiculo_id}", response_model=VehiculoResponse)
def get_vehiculo(vehiculo_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    veh = db.query(ParametrosVehiculo).filter(ParametrosVehiculo.id_vehiculo == vehiculo_id).first()
    if not veh:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return veh