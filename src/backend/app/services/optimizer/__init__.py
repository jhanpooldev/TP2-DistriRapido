from math import radians, sin, cos, sqrt, asin
from typing import List, Tuple
import uuid
from datetime import datetime

from app.schemas import PuntoEntregaResponse, PuntoRutaResponse, RutaResponse, ResumenRuta
from app.core.config import get_settings
from app.models import ParametrosVehiculo, Ruta, RutaPunto
from sqlalchemy.orm import Session

settings = get_settings()

UMBRAL_REDUCCION_SIGNIFICATIVA_PCT = 1.0

def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    return 2 * R * asin(sqrt(a))

def nearest_neighbor(points: List[PuntoEntregaResponse], home_lat: float, home_lng: float) -> Tuple[List[PuntoEntregaResponse], float]:
    if not points:
        return [], 0.0
    unvisited = {p.id_punto: p for p in points}
    route = []
    current_lat, current_lng = home_lat, home_lng
    total_dist = 0.0
    while unvisited:
        nearest_id = min(
            unvisited.keys(),
            key=lambda pid: haversine(current_lat, current_lng, unvisited[pid].latitud, unvisited[pid].longitud)
        )
        nearest = unvisited.pop(nearest_id)
        total_dist += haversine(current_lat, current_lng, nearest.latitud, nearest.longitud)
        route.append(nearest)
        current_lat, current_lng = nearest.latitud, nearest.longitud
    total_dist += haversine(current_lat, current_lng, home_lat, home_lng)
    return route, total_dist

def two_opt(route: List[PuntoEntregaResponse], home_lat: float, home_lng: float, max_iterations: int = 1000) -> List[PuntoEntregaResponse]:
    if len(route) < 3:
        return route
    best = route[:]
    improved = True
    it = 0
    while improved and it < max_iterations:
        improved = False
        for i in range(1, len(best) - 2):
            for j in range(i + 1, len(best)):
                new_route = best[:i] + best[i:j][::-1] + best[j:]
                dist_new = route_distance(new_route, home_lat, home_lng)
                dist_best = route_distance(best, home_lat, home_lng)
                if dist_new < dist_best:
                    best = new_route
                    improved = True
                    break
            if improved:
                break
        it += 1
    return best

def route_distance(route: List[PuntoEntregaResponse], home_lat: float, home_lng: float) -> float:
    if not route:
        return 0.0
    total = haversine(home_lat, home_lng, route[0].latitud, route[0].longitud)
    for i in range(len(route) - 1):
        total += haversine(route[i].latitud, route[i].longitud, route[i+1].latitud, route[i+1].longitud)
    total += haversine(route[-1].latitud, route[-1].longitud, home_lat, home_lng)
    return total

def calculate_co2(dist_km: float, vehiculo: ParametrosVehiculo) -> float:
    return dist_km * float(vehiculo.consumo_litros_km) * float(vehiculo.factor_emision_co2)

def calculate_time_min(dist_km: float, vehiculo: ParametrosVehiculo) -> float:
    return dist_km / float(vehiculo.velocidad_promedio_kmh) * 60

def calcular_ahorro(
    dist_optimizada: float,
    dist_no_optimizada: float,
    factor_co2_kg_por_km: float = 0.0,
) -> dict:
    """RN-018: contrasta la ruta optimizada frente a la no optimizada.

    Los porcentajes nunca son negativos: si el resultado no fue mejor, se
    reportan en cero y se marca que no hubo reducción significativa.

    `factor_co2_kg_por_km` convierte los kilómetros ahorrados en kg de CO₂
    usando las emisiones del vehículo.
    """
    if dist_no_optimizada <= 0:
        return {
            "ahorro_co2_kg": 0.0,
            "ahorro_co2_pct": 0.0,
            "ahorro_distancia_pct": 0.0,
            "sin_reduccion_significativa": True,
        }

    ahorro_co2_pct = ((dist_no_optimizada - dist_optimizada) / dist_no_optimizada) * 100.0
    if ahorro_co2_pct < 0:
        ahorro_co2_pct = 0.0

    km_ahorrados = max(dist_no_optimizada - dist_optimizada, 0.0)

    return {
        "ahorro_co2_kg": round(km_ahorrados * factor_co2_kg_por_km, 3),
        "ahorro_co2_pct": round(ahorro_co2_pct, 2),
        "ahorro_distancia_pct": round(ahorro_co2_pct, 2),
        "sin_reduccion_significativa": ahorro_co2_pct < UMBRAL_REDUCCION_SIGNIFICATIVA_PCT,
    }

def co2_kg_por_km(vehiculo: ParametrosVehiculo) -> float:
    """Emisiones de CO₂ por kilómetro para el vehículo indicado."""
    return float(vehiculo.consumo_litros_km) * float(vehiculo.factor_emision_co2)

def build_route_response(
    db: Session,
    operador_id: uuid.UUID,
    vehiculo_id: int,
    ordered_points: List[PuntoEntregaResponse],
    dist_optimized: float,
    dist_unoptimized: float,
    vehiculo: ParametrosVehiculo,
) -> RutaResponse:
    co2_opt = calculate_co2(dist_optimized, vehiculo)
    co2_unopt = calculate_co2(dist_unoptimized, vehiculo)
    time_opt = calculate_time_min(dist_optimized, vehiculo)
    time_unopt = calculate_time_min(dist_unoptimized, vehiculo)
    ahorro = calcular_ahorro(dist_optimized, dist_unoptimized, co2_kg_por_km(vehiculo))

    puntos_ruta = [
        PuntoRutaResponse(
            id_punto=p.id_punto,
            orden=i + 1,
            direccion=p.direccion,
            latitud=p.latitud,
            longitud=p.longitud,
            peso_kg=p.peso_kg,
            destinatario=p.destinatario,
        )
        for i, p in enumerate(ordered_points)
    ]

    return RutaResponse(
        id_ruta=uuid.uuid4(),
        id_operador=operador_id,
        id_vehiculo=vehiculo_id,
        distancia_total_km=round(dist_optimized, 3),
        tiempo_estimado_min=round(time_opt, 2),
        co2_estimado_kg=round(co2_opt, 3),
        distancia_sin_optimizar_km=round(dist_unoptimized, 3),
        tiempo_sin_optimizar_min=round(time_unopt, 2),
        co2_sin_optimizar_kg=round(co2_unopt, 3),
        ahorro_co2_kg=ahorro["ahorro_co2_kg"],
        ahorro_co2_pct=ahorro["ahorro_co2_pct"],
        ahorro_distancia_pct=ahorro["ahorro_distancia_pct"],
        sin_reduccion_significativa=ahorro["sin_reduccion_significativa"],
        estado="Confirmada",
        fecha_generacion=datetime.utcnow(),
        puntos=puntos_ruta,
    )

def persist_ruta(
    db: Session,
    response: RutaResponse,
    ordered_points: List[PuntoEntregaResponse],
) -> Ruta:
    ruta = Ruta(
        id_ruta=response.id_ruta,
        id_operador=response.id_operador,
        id_vehiculo=response.id_vehiculo,
        distancia_total_km=response.distancia_total_km,
        tiempo_estimado_min=response.tiempo_estimado_min,
        co2_estimado_kg=response.co2_estimado_kg,
        distancia_sin_optimizar_km=response.distancia_sin_optimizar_km,
        tiempo_sin_optimizar_min=response.tiempo_sin_optimizar_min,
        co2_sin_optimizar_kg=response.co2_sin_optimizar_kg,
        estado=response.estado,
    )
    db.add(ruta)
    for i, p in enumerate(ordered_points):
        db.add(RutaPunto(id_ruta=response.id_ruta, id_punto=p.id_punto, orden=i + 1))
    db.commit()
    db.refresh(ruta)
    return ruta