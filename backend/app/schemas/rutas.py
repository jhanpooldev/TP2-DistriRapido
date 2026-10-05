from typing import List, Optional
from pydantic import BaseModel, Field

class PuntoEntrega(BaseModel):
    id: str = Field(..., description="Identificador único del punto o pedido")
    direccion: str = Field(..., min_length=3, description="Dirección física en Lima")
    latitud: float = Field(..., ge=-12.5, le=-11.5, description="Latitud en Lima Metropolitana")
    longitud: float = Field(..., ge=-77.5, le=-76.5, description="Longitud en Lima Metropolitana")
    peso_kg: float = Field(0.0, ge=0, description="Peso del pedido en kg (RN-008)")
    destinatario: str = Field(..., description="Nombre del cliente")
    orden_visita: Optional[int] = None

class RutaOptimizarRequest(BaseModel):
    centro_distribucion: PuntoEntrega = Field(
        ...,
        description="Punto de origen y fin del recorrido (Centro de Distribución - RN-011)"
    )
    puntos_entrega: List[PuntoEntrega] = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Listado de pedidos a entregar"
    )
    capacidad_vehiculo_kg: float = Field(
        1000.0,
        gt=0,
        description="Capacidad máxima de carga del vehículo en kg"
    )
    tipo_vehiculo: str = Field(
        "van_diesel",
        description="Tipo de motorización: van_diesel, van_gnv, van_electrica"
    )

class RutaOptimizarResponse(BaseModel):
    id_ruta: str
    secuencia_puntos: List[PuntoEntrega]
    distancia_optimizada_km: float
    distancia_no_optimizada_km: float
    distancia_ahorrada_km: float
    tiempo_estimado_min: float
    emisiones_co2_kg: float
    co2_ahorrado_kg: float
    porcentaje_ahorro: float
    peso_total_kg: float
    capacidad_vehiculo_kg: float
    utilizacion_capacidad_pct: float
    mensaje: str
