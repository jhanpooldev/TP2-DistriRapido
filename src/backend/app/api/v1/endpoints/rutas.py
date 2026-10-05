from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import datetime, time as time_type
from typing import List, Optional
import uuid

from app.core.database import get_db
from app.core.config import get_settings
from app.models import Ruta, RutaPunto, PuntoEntrega, ParametrosVehiculo
from app.schemas import RutaOptimizarRequest, RutaResponse, ResumenRuta, PuntoRutaResponse, PuntoEntregaResponse
from app.api.v1.endpoints.dependencies import get_current_operador, get_current_user
from app.services.optimizer import (
    nearest_neighbor, two_opt, route_distance,
    build_route_response, persist_ruta, calcular_ahorro, co2_kg_por_km,
)

router = APIRouter()
settings = get_settings()

MIN_PUNTOS = 2

# RN-013: estados que implican entregas ya realizadas o en marcha.
ESTADOS_CON_ENTREGAS = ("En curso", "Completada", "Cancelada")
ESTADOS_ELIMINABLES = ("Confirmada", "Borrador")

def _parsear_fecha(valor: str, fin_del_dia: bool = False) -> Optional[datetime]:
    """Acepta 'YYYY-MM-DD' o ISO completo.

    Devuelve None si el formato no es reconocido, para no aplicar un filtro
    invalido en silencio.
    """
    texto = valor.strip()
    try:
        fecha = datetime.strptime(texto, "%Y-%m-%d")
        return datetime.combine(fecha.date(), time_type.max) if fin_del_dia else fecha
    except ValueError:
        pass
    for formato in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f"):
        try:
            return datetime.strptime(texto, formato)
        except ValueError:
            continue
    return None

def get_puntos_entrega(db: Session, punto_ids: List[uuid.UUID], operador_id: uuid.UUID) -> List:
    return db.query(PuntoEntrega).filter(
        PuntoEntrega.id_punto.in_(punto_ids),
        PuntoEntrega.id_operador == operador_id
    ).all()

def _validar_cantidad_puntos(punto_ids: List[uuid.UUID]) -> None:
    cantidad = len(set(punto_ids))
    if cantidad < MIN_PUNTOS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Se requieren al menos {MIN_PUNTOS} puntos de entrega",
        )
    maximo = settings.MAX_PUNTOS_POR_RUTA
    if cantidad > maximo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"El maximo soportado es de {maximo} puntos por ruta; "
                f"se recibieron {cantidad}. Reduce los puntos e intenta de nuevo."
            ),
        )

def _validar_capacidad(puntos: List[PuntoEntregaResponse], vehiculo) -> None:
    """RN-014: la carga total no puede superar la capacidad del vehiculo."""
    peso_total = sum(p.peso_kg for p in puntos)
    capacidad = float(vehiculo.capacidad_kg)
    if peso_total > capacidad:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"La carga total ({peso_total:.1f} kg) supera la capacidad del "
                f"vehiculo ({capacidad:.1f} kg). Quita puntos o elige otro vehiculo."
            ),
        )

def _puntos_en_orden_de_ingreso(
    puntos_db: List, punto_ids: List[uuid.UUID]
) -> List[PuntoEntregaResponse]:
    por_id = {p.id_punto: p for p in puntos_db}
    return [
        PuntoEntregaResponse.model_validate(por_id[pid])
        for pid in dict.fromkeys(punto_ids)
        if pid in por_id
    ]

def _calcular_ruta(db: Session, request: RutaOptimizarRequest, operador):
    vehiculo = db.query(ParametrosVehiculo).filter(ParametrosVehiculo.id_vehiculo == request.id_vehiculo).first()
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehiculo no encontrado")

    _validar_cantidad_puntos(request.punto_ids)

    puntos_db = get_puntos_entrega(db, request.punto_ids, operador.id_usuario)
    if len(puntos_db) < MIN_PUNTOS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Alguno de los puntos seleccionados no existe o no te pertenece",
        )

    puntos_schema = [PuntoEntregaResponse.model_validate(p) for p in puntos_db]
    _validar_capacidad(puntos_schema, vehiculo)

    # RN-018: la ruta no optimizada es la misma en el orden en que ingreso.
    ruta_original = _puntos_en_orden_de_ingreso(puntos_db, request.punto_ids)
    dist_original = route_distance(ruta_original, settings.HOME_LAT, settings.HOME_LNG)

    nn_route, _ = nearest_neighbor(puntos_schema, settings.HOME_LAT, settings.HOME_LNG)
    opt_route = two_opt(nn_route, settings.HOME_LAT, settings.HOME_LNG)
    dist_opt = route_distance(opt_route, settings.HOME_LAT, settings.HOME_LNG)

    response = build_route_response(
        db, operador.id_usuario, request.id_vehiculo,
        opt_route, dist_opt, dist_original, vehiculo
    )
    return response, opt_route

@router.post("/optimizar", response_model=RutaResponse)
def optimizar_ruta(request: RutaOptimizarRequest, db: Session = Depends(get_db), operador = Depends(get_current_operador)):
    response, _ = _calcular_ruta(db, request, operador)
    return response

@router.post("", response_model=RutaResponse, status_code=status.HTTP_201_CREATED)
def confirmar_ruta(request: RutaOptimizarRequest, db: Session = Depends(get_db), operador = Depends(get_current_operador)):
    response, opt_route = _calcular_ruta(db, request, operador)
    persist_ruta(db, response, opt_route)
    return response

def _factor_co2_de_ruta(db: Session, ruta) -> float:
    """Emisiones de CO₂ por km del vehículo asignado a la ruta."""
    vehiculo = (
        db.query(ParametrosVehiculo)
        .filter(ParametrosVehiculo.id_vehiculo == ruta.id_vehiculo)
        .first()
    )
    return co2_kg_por_km(vehiculo) if vehiculo else 0.0

def _ruta_to_response(db: Session, ruta) -> RutaResponse:
    puntos = db.query(RutaPunto).filter(RutaPunto.id_ruta == ruta.id_ruta).order_by(RutaPunto.orden).all()
    puntos_schema = [
        PuntoRutaResponse(
            id_punto=rp.punto.id_punto,
            orden=rp.orden,
            direccion=rp.punto.direccion,
            latitud=rp.punto.latitud,
            longitud=rp.punto.longitud,
            peso_kg=rp.punto.peso_kg,
            destinatario=rp.punto.destinatario,
        )
        for rp in puntos
    ]
    ahorro = calcular_ahorro(
        float(ruta.distancia_total_km),
        float(ruta.distancia_sin_optimizar_km),
        _factor_co2_de_ruta(db, ruta),
    )
    return RutaResponse(
        id_ruta=ruta.id_ruta,
        id_operador=ruta.id_operador,
        id_vehiculo=ruta.id_vehiculo,
        distancia_total_km=ruta.distancia_total_km,
        tiempo_estimado_min=ruta.tiempo_estimado_min,
        co2_estimado_kg=ruta.co2_estimado_kg,
        distancia_sin_optimizar_km=ruta.distancia_sin_optimizar_km,
        tiempo_sin_optimizar_min=ruta.tiempo_sin_optimizar_min,
        co2_sin_optimizar_kg=ruta.co2_sin_optimizar_kg,
        ahorro_co2_kg=ahorro["ahorro_co2_kg"],
        ahorro_co2_pct=ahorro["ahorro_co2_pct"],
        ahorro_distancia_pct=ahorro["ahorro_distancia_pct"],
        sin_reduccion_significativa=ahorro["sin_reduccion_significativa"],
        estado=ruta.estado,
        fecha_generacion=ruta.fecha_generacion,
        puntos=puntos_schema,
    )

@router.put("/{ruta_id}", response_model=RutaResponse)
def editar_ruta(
    ruta_id: uuid.UUID,
    request: RutaOptimizarRequest,
    db: Session = Depends(get_db),
    operador=Depends(get_current_operador),
):
    """US-002: reemplaza los puntos de una ruta guardada y recalcula (RN-018)."""
    ruta = db.query(Ruta).filter(Ruta.id_ruta == ruta_id).first()
    if not ruta:
        raise HTTPException(status_code=404, detail="Ruta no encontrada")
    if ruta.id_operador != operador.id_usuario:
        raise HTTPException(status_code=403, detail="No autorizado")

    _validar_cantidad_puntos(request.punto_ids)

    puntos_db = get_puntos_entrega(db, request.punto_ids, operador.id_usuario)
    if len(puntos_db) < MIN_PUNTOS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Alguno de los puntos seleccionados no existe o no te pertenece",
        )

    # RN-009: un punto que ya pertenece a otra ruta confirmada no se puede reutilizar.
    ya_asignados = (
        db.query(RutaPunto.id_punto)
        .join(Ruta, Ruta.id_ruta == RutaPunto.id_ruta)
        .filter(Ruta.id_operador == operador.id_usuario, Ruta.id_ruta != ruta_id)
        .all()
    )
    ids_asignados = {row[0] for row in ya_asignados}
    puntos_en_uso = [p for p in request.punto_ids if p in ids_asignados]
    if puntos_en_uso:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"{len(puntos_en_uso)} punto(s) ya pertenecen a otra ruta guardada "
                "y no pueden reasignarse."
            ),
        )

    vehiculo = db.query(ParametrosVehiculo).filter(ParametrosVehiculo.id_vehiculo == request.id_vehiculo).first()
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehiculo no encontrado")

    puntos_schema = [PuntoEntregaResponse.model_validate(p) for p in puntos_db]
    _validar_capacidad(puntos_schema, vehiculo)

    ruta_original = _puntos_en_orden_de_ingreso(puntos_db, request.punto_ids)
    dist_original = route_distance(ruta_original, settings.HOME_LAT, settings.HOME_LNG)

    nn_route, _ = nearest_neighbor(puntos_schema, settings.HOME_LAT, settings.HOME_LNG)
    opt_route = two_opt(nn_route, settings.HOME_LAT, settings.HOME_LNG)
    dist_opt = route_distance(opt_route, settings.HOME_LAT, settings.HOME_LNG)

    response = build_route_response(
        db, operador.id_usuario, request.id_vehiculo,
        opt_route, dist_opt, dist_original, vehiculo
    )

    # Actualiza la ruta existente en lugar de crear una nueva (US-002).
    db.query(RutaPunto).filter(RutaPunto.id_ruta == ruta_id).delete(synchronize_session=False)
    db.flush()

    ruta.id_vehiculo = request.id_vehiculo
    ruta.distancia_total_km = response.distancia_total_km
    ruta.tiempo_estimado_min = response.tiempo_estimado_min
    ruta.co2_estimado_kg = response.co2_estimado_kg
    ruta.distancia_sin_optimizar_km = response.distancia_sin_optimizar_km
    ruta.tiempo_sin_optimizar_min = response.tiempo_sin_optimizar_min
    ruta.co2_sin_optimizar_kg = response.co2_sin_optimizar_kg

    for i, punto in enumerate(opt_route, start=1):
        db.add(RutaPunto(id_ruta=ruta_id, id_punto=punto.id_punto, orden=i))

    db.commit()
    db.refresh(ruta)

    return _ruta_to_response(db, ruta)


@router.get("", response_model=List[RutaResponse])
def list_rutas(
    desde: Optional[str] = None,
    hasta: Optional[str] = None,
    estado: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    """US-007: listado con filtros por rango de fechas y estado."""
    query = db.query(Ruta)

    if user.rol.nombre != "Administrador":
        query = query.filter(Ruta.id_operador == user.id_usuario)

    if desde:
        fecha = _parsear_fecha(desde)
        if fecha is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Formato de 'desde' invalido. Usa YYYY-MM-DD.",
            )
        query = query.filter(Ruta.fecha_generacion >= fecha)

    if hasta:
        fecha = _parsear_fecha(hasta, fin_del_dia=True)
        if fecha is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Formato de 'hasta' invalido. Usa YYYY-MM-DD.",
            )
        query = query.filter(Ruta.fecha_generacion <= fecha)

    if estado:
        query = query.filter(func.lower(Ruta.estado) == estado.strip().lower())

    rutas = query.order_by(Ruta.fecha_generacion.desc()).offset(skip).limit(limit).all()
    return [_ruta_to_response(db, r) for r in rutas]

@router.get("/{ruta_id}", response_model=RutaResponse)
def get_ruta(ruta_id: uuid.UUID, db: Session = Depends(get_db), user = Depends(get_current_user)):
    ruta = db.query(Ruta).filter(Ruta.id_ruta == ruta_id).first()
    if not ruta:
        raise HTTPException(status_code=404, detail="Ruta no encontrada")
    if user.rol.nombre != "Administrador" and ruta.id_operador != user.id_usuario:
        raise HTTPException(status_code=403, detail="No autorizado")
    return _ruta_to_response(db, ruta)

@router.get("/{ruta_id}/resumen", response_model=ResumenRuta)
def get_resumen(ruta_id: uuid.UUID, db: Session = Depends(get_db), user = Depends(get_current_user)):
    ruta = db.query(Ruta).filter(Ruta.id_ruta == ruta_id).first()
    if not ruta:
        raise HTTPException(status_code=404, detail="Ruta no encontrada")
    if user.rol.nombre != "Administrador" and ruta.id_operador != user.id_usuario:
        raise HTTPException(status_code=403, detail="No autorizado")

    puntos = db.query(RutaPunto).filter(RutaPunto.id_ruta == ruta_id).order_by(RutaPunto.orden).all()
    puntos_schema = []
    for rp in puntos:
        p = rp.punto
        puntos_schema.append(PuntoRutaResponse(
            id_punto=p.id_punto,
            orden=rp.orden,
            direccion=p.direccion,
            latitud=p.latitud,
            longitud=p.longitud,
            peso_kg=p.peso_kg,
            destinatario=p.destinatario,
        ))

    ahorro = calcular_ahorro(
        float(ruta.distancia_total_km),
        float(ruta.distancia_sin_optimizar_km),
        _factor_co2_de_ruta(db, ruta),
    )

    return ResumenRuta(
        id_ruta=ruta.id_ruta,
        puntos=puntos_schema,
        distancia_total_km=ruta.distancia_total_km,
        tiempo_estimado_min=ruta.tiempo_estimado_min,
        co2_estimado_kg=ruta.co2_estimado_kg,
        distancia_sin_optimizar_km=ruta.distancia_sin_optimizar_km,
        tiempo_sin_optimizar_min=ruta.tiempo_sin_optimizar_min,
        co2_sin_optimizar_kg=ruta.co2_sin_optimizar_kg,
        ahorro_co2_kg=ahorro["ahorro_co2_kg"],
        ahorro_co2_pct=ahorro["ahorro_co2_pct"],
        ahorro_distancia_pct=ahorro["ahorro_distancia_pct"],
        sin_reduccion_significativa=ahorro["sin_reduccion_significativa"],
    )

@router.delete("/{ruta_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ruta(ruta_id: uuid.UUID, db: Session = Depends(get_db), user = Depends(get_current_user)):
    ruta = db.query(Ruta).filter(Ruta.id_ruta == ruta_id).first()
    if not ruta:
        raise HTTPException(status_code=404, detail="Ruta no encontrada")
    if user.rol.nombre != "Administrador" and ruta.id_operador != user.id_usuario:
        raise HTTPException(status_code=403, detail="No autorizado")

    # RN-013: una ruta con entregas en curso o completadas ya no se puede eliminar.
    if ruta.estado in ESTADOS_CON_ENTREGAS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "RN-013: no se puede eliminar una ruta que ya tiene entregas "
                f"en estado '{ruta.estado}'."
            ),
        )

    if ruta.estado not in ESTADOS_ELIMINABLES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo se pueden eliminar rutas confirmadas o en borrador",
        )

    db.query(RutaPunto).filter(RutaPunto.id_ruta == ruta_id).delete(synchronize_session=False)
    db.delete(ruta)
    db.commit()

@router.get("/{ruta_id}/puntos", response_model=List[PuntoRutaResponse])
def get_ruta_puntos(ruta_id: uuid.UUID, db: Session = Depends(get_db), user = Depends(get_current_user)):
    ruta = db.query(Ruta).filter(Ruta.id_ruta == ruta_id).first()
    if not ruta:
        raise HTTPException(status_code=404, detail="Ruta no encontrada")
    if user.rol.nombre != "Administrador" and ruta.id_operador != user.id_usuario:
        raise HTTPException(status_code=403, detail="No autorizado")
    puntos = db.query(RutaPunto).filter(RutaPunto.id_ruta == ruta_id).order_by(RutaPunto.orden).all()
    return [
        PuntoRutaResponse(
            id_punto=rp.punto.id_punto,
            orden=rp.orden,
            direccion=rp.punto.direccion,
            latitud=rp.punto.latitud,
            longitud=rp.punto.longitud,
            peso_kg=rp.punto.peso_kg,
            destinatario=rp.punto.destinatario,
        )
        for rp in puntos
    ]