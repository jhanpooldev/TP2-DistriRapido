import uuid
from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException, status

from backend.app.schemas.rutas import (
    PuntoEntrega,
    RutaOptimizarRequest,
    RutaOptimizarResponse,
)
from backend.app.services.routing_service import (
    calcular_matriz_distancias,
    optimizar_tsp_2opt,
    estimar_emisiones_co2,
)

router = APIRouter(prefix="/api/rutas", tags=["Optimización de Rutas Sostenibles"])

@router.post(
    "/optimizar",
    response_model=RutaOptimizarResponse,
    status_code=status.HTTP_200_OK,
    summary="Optimizar ruta de reparto y calcular ahorro de CO2",
    description="Calcula la secuencia óptima de reparto aplicando heurísticas TSP/2-opt, validando restricciones de capacidad y calculando el impacto ambiental."
)
def optimizar_ruta(data: RutaOptimizarRequest):
    # Validación de capacidad de carga vehicular (RN-008)
    peso_total = sum(p.peso_kg for p in data.puntos_entrega)
    if peso_total > data.capacidad_vehiculo_kg:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La carga total ({peso_total:.1f} kg) supera la capacidad máxima del vehículo ({data.capacidad_vehiculo_kg:.1f} kg)."
        )

    # Construir listado de todos los puntos: índice 0 = Centro de Distribución
    todos_puntos: List[Dict[str, Any]] = [
        {
            "id": data.centro_distribucion.id,
            "direccion": data.centro_distribucion.direccion,
            "latitud": data.centro_distribucion.latitud,
            "longitud": data.centro_distribucion.longitud,
            "peso_kg": 0.0,
            "destinatario": "Centro de Distribución (Base Central)"
        }
    ]
    for p in data.puntos_entrega:
        todos_puntos.append({
            "id": p.id,
            "direccion": p.direccion,
            "latitud": p.latitud,
            "longitud": p.longitud,
            "peso_kg": p.peso_kg,
            "destinatario": p.destinatario
        })

    # Calcular matriz de distancias
    matriz = calcular_matriz_distancias(todos_puntos)

    # Calcular distancia de la ruta NO optimizada (orden secuencial de ingreso)
    ruta_no_optimizada = list(range(len(todos_puntos))) + [0]
    distancia_no_opt = sum(matriz[ruta_no_optimizada[k]][ruta_no_optimizada[k + 1]] for k in range(len(ruta_no_optimizada) - 1))
    distancia_no_opt = round(distancia_no_opt, 2)

    # Calcular ruta optimizada mediante 2-opt
    indices_optimizados, distancia_opt = optimizar_tsp_2opt(matriz)

    # Distancia ahorrada y porcentaje
    distancia_ahorrada = max(0.0, round(distancia_no_opt - distancia_opt, 2))
    pct_ahorro = round((distancia_ahorrada / distancia_no_opt * 100), 1) if distancia_no_opt > 0 else 0.0

    # Estimación de emisiones de CO2
    co2_opt = estimar_emisiones_co2(distancia_opt, data.tipo_vehiculo)
    co2_no_opt = estimar_emisiones_co2(distancia_no_opt, data.tipo_vehiculo)
    co2_ahorrado = max(0.0, round(co2_no_opt - co2_opt, 3))

    # Estimación de tiempo (asumiendo velocidad media urbana en Lima de 25 km/h + 8 min por entrega)
    tiempo_transito_min = (distancia_opt / 25.0) * 60.0
    tiempo_entregas_min = len(data.puntos_entrega) * 8.0
    tiempo_total_min = round(tiempo_transito_min + tiempo_entregas_min, 1)

    # Reordenar los objetos PuntoEntrega con el orden asignado
    secuencia_puntos: List[PuntoEntrega] = []
    for orden, idx in enumerate(indices_optimizados):
        p_info = todos_puntos[idx]
        secuencia_puntos.append(PuntoEntrega(
            id=p_info["id"],
            direccion=p_info["direccion"],
            latitud=p_info["latitud"],
            longitud=p_info["longitud"],
            peso_kg=p_info["peso_kg"],
            destinatario=p_info["destinatario"],
            orden_visita=orden
        ))

    utilizacion_pct = round((peso_total / data.capacidad_vehiculo_kg) * 100, 1)

    return RutaOptimizarResponse(
        id_ruta=str(uuid.uuid4()),
        secuencia_puntos=secuencia_puntos,
        distancia_optimizada_km=distancia_opt,
        distancia_no_optimizada_km=distancia_no_opt,
        distancia_ahorrada_km=distancia_ahorrada,
        tiempo_estimado_min=tiempo_total_min,
        emisiones_co2_kg=co2_opt,
        co2_ahorrado_kg=co2_ahorrado,
        porcentaje_ahorro=pct_ahorro,
        peso_total_kg=round(peso_total, 2),
        capacidad_vehiculo_kg=data.capacidad_vehiculo_kg,
        utilizacion_capacidad_pct=utilizacion_pct,
        mensaje="Ruta optimizada exitosamente reduciendo distancia y emisiones de carbono."
    )

@router.get(
    "/demo-lima",
    response_model=RutaOptimizarRequest,
    summary="Obtener escenario de prueba de puntos de entrega en Lima Metropolitana",
    description="Proporciona un conjunto de datos representativo en Lima para demostraciones rápidas a stakeholders."
)
def obtener_demo_lima():
    centro = PuntoEntrega(
        id="CD-CENTRAL",
        direccion="Av. Argentina 2800, Cercado de Lima (Almacén Central DistriRápido)",
        latitud=-12.046374,
        longitud=-77.042793,
        peso_kg=0.01,
        destinatario="Centro de Distribución"
    )
    puntos = [
        PuntoEntrega(
            id="PED-001",
            direccion="Av. Larco 400, Miraflores",
            latitud=-12.122145,
            longitud=-77.029834,
            peso_kg=45.0,
            destinatario="Farmacia Santa María"
        ),
        PuntoEntrega(
            id="PED-002",
            direccion="Av. Javier Prado Este 2200, San Borja",
            latitud=-12.086432,
            longitud=-77.001243,
            peso_kg=120.0,
            destinatario="Tiendas Wong"
        ),
        PuntoEntrega(
            id="PED-003",
            direccion="Av. Camino Real 456, San Isidro",
            latitud=-12.098765,
            longitud=-77.036543,
            peso_kg=60.0,
            destinatario="Clínica El Golf"
        ),
        PuntoEntrega(
            id="PED-004",
            direccion="Av. Brasil 1400, Jesús María",
            latitud=-12.071234,
            longitud=-77.051234,
            peso_kg=85.0,
            destinatario="Distribuidora San Felipe"
        ),
        PuntoEntrega(
            id="PED-005",
            direccion="Av. Primavera 650, Santiago de Surco",
            latitud=-12.113456,
            longitud=-76.985678,
            peso_kg=95.0,
            destinatario="Supermercado Metro"
        )
    ]
    return RutaOptimizarRequest(
        centro_distribucion=centro,
        puntos_entrega=puntos,
        capacidad_vehiculo_kg=1200.0,
        tipo_vehiculo="van_diesel"
    )
