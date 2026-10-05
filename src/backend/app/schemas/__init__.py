from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator, model_validator
from datetime import datetime
from typing import Optional, List
import uuid

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    sub: Optional[str] = None

class UsuarioCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    correo: EmailStr
    password: str = Field(..., min_length=6)
    id_rol: int = Field(..., ge=1)

class RolResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_rol: int
    nombre: str
    descripcion: Optional[str] = None

class UsuarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_usuario: uuid.UUID
    nombre: str
    correo: str
    id_rol: int
    # Requerido: id_rol es NOT NULL en la BD, asi que un usuario sin rol es
    # corrupcion de datos y debe verse reflejada, no devolverse como null.
    rol: RolResponse
    fecha_creacion: datetime

class PuntoEntregaCreate(BaseModel):
    direccion: str = Field(..., min_length=1, max_length=255)
    latitud: float = Field(..., ge=-90, le=90)
    longitud: float = Field(..., ge=-180, le=180)
    peso_kg: float = Field(..., gt=0)
    destinatario: str = Field(..., min_length=1, max_length=150)

    @field_validator("direccion", "destinatario")
    @classmethod
    def no_vacios(cls, valor: str) -> str:
        limpio = valor.strip()
        if not limpio:
            raise ValueError("El campo no puede estar vacio ni contener solo espacios")
        return limpio

    @model_validator(mode="after")
    def coordenadas_geolocalizables(self):
        if self.latitud == 0 and self.longitud == 0:
            raise ValueError(
                "Coordenadas invalidas: el punto no pudo geolocalizarse. "
                "Selecciona la ubicacion en el mapa."
            )
        return self

class PuntoEntregaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_punto: uuid.UUID
    direccion: str
    latitud: float
    longitud: float
    peso_kg: float
    destinatario: str
    id_operador: uuid.UUID
    fecha_registro: datetime

class PuntoEntregaList(BaseModel):
    puntos: List[PuntoEntregaResponse]

class VehiculoCreate(BaseModel):
    placa: str = Field(..., min_length=1, max_length=20)
    capacidad_kg: float = Field(..., gt=0)
    factor_emision_co2: float = Field(..., gt=0)
    consumo_litros_km: float = Field(..., gt=0)
    velocidad_promedio_kmh: float = Field(..., gt=0)
    tipo_combustible: str = Field(..., min_length=1, max_length=30)

class VehiculoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_vehiculo: int
    placa: str
    capacidad_kg: float
    factor_emision_co2: float
    consumo_litros_km: float
    velocidad_promedio_kmh: float
    tipo_combustible: str

class RutaOptimizarRequest(BaseModel):
    id_vehiculo: int = Field(..., ge=1)
    punto_ids: List[uuid.UUID] = Field(...)

class PuntoRutaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_punto: uuid.UUID
    orden: int
    direccion: str
    latitud: float
    longitud: float
    peso_kg: float
    destinatario: str

class RutaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_ruta: uuid.UUID
    id_operador: uuid.UUID
    id_vehiculo: int
    distancia_total_km: float
    tiempo_estimado_min: float
    co2_estimado_kg: float
    distancia_sin_optimizar_km: float
    tiempo_sin_optimizar_min: float
    co2_sin_optimizar_kg: float
    ahorro_co2_kg: float = 0.0
    ahorro_co2_pct: float = 0.0
    ahorro_distancia_pct: float = 0.0
    sin_reduccion_significativa: bool = False
    estado: str
    fecha_generacion: datetime
    puntos: List[PuntoRutaResponse] = Field(default_factory=list)

class ResumenRuta(BaseModel):
    id_ruta: uuid.UUID
    puntos: List[PuntoRutaResponse]
    distancia_total_km: float
    tiempo_estimado_min: float
    co2_estimado_kg: float
    distancia_sin_optimizar_km: float
    tiempo_sin_optimizar_min: float
    co2_sin_optimizar_kg: float
    ahorro_co2_kg: float = 0.0
    ahorro_co2_pct: float = 0.0
    ahorro_distancia_pct: float = 0.0
    sin_reduccion_significativa: bool = False