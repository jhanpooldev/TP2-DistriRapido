from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, TIMESTAMP, func, CheckConstraint, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base

class Rol(Base):
    __tablename__ = "roles"
    id_rol = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False, unique=True)
    descripcion = Column(String(255))
    usuarios = relationship("Usuario", back_populates="rol")

class Usuario(Base):
    __tablename__ = "usuarios"
    id_usuario = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(150), nullable=False, unique=True)
    contrasena_hash = Column(String(255), nullable=False)
    id_rol = Column(Integer, ForeignKey("roles.id_rol"), nullable=False)
    fecha_creacion = Column(TIMESTAMP(timezone=True), server_default=func.now())
    rol = relationship("Rol", back_populates="usuarios")
    puntos = relationship("PuntoEntrega", back_populates="operador")
    rutas = relationship("Ruta", back_populates="operador")

class PuntoEntrega(Base):
    __tablename__ = "puntos_entrega"
    id_punto = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    direccion = Column(String(255), nullable=False)
    latitud = Column(DECIMAL(10, 7), nullable=False)
    longitud = Column(DECIMAL(10, 7), nullable=False)
    peso_kg = Column(DECIMAL(10, 3), nullable=False)
    destinatario = Column(String(150), nullable=False)
    id_operador = Column(UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=False)
    fecha_registro = Column(TIMESTAMP(timezone=True), server_default=func.now())
    operador = relationship("Usuario", back_populates="puntos")
    ruta_puntos = relationship("RutaPunto", back_populates="punto")

class ParametrosVehiculo(Base):
    __tablename__ = "parametros_vehiculo"
    id_vehiculo = Column(Integer, primary_key=True, autoincrement=True)
    placa = Column(String(20), nullable=False, unique=True)
    capacidad_kg = Column(DECIMAL(10, 3), nullable=False)
    factor_emision_co2 = Column(DECIMAL(6, 3), nullable=False)
    consumo_litros_km = Column(DECIMAL(6, 3), nullable=False)
    velocidad_promedio_kmh = Column(DECIMAL(6, 2), nullable=False)
    tipo_combustible = Column(String(30), nullable=False)
    rutas = relationship("Ruta", back_populates="vehiculo")

class Ruta(Base):
    __tablename__ = "rutas"
    id_ruta = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_operador = Column(UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=False)
    id_vehiculo = Column(Integer, ForeignKey("parametros_vehiculo.id_vehiculo"), nullable=False)
    distancia_total_km = Column(DECIMAL(10, 3), nullable=False, default=0)
    tiempo_estimado_min = Column(DECIMAL(10, 2), nullable=False, default=0)
    co2_estimado_kg = Column(DECIMAL(10, 3), nullable=False, default=0)
    distancia_sin_optimizar_km = Column(DECIMAL(10, 3), nullable=False, default=0)
    tiempo_sin_optimizar_min = Column(DECIMAL(10, 2), nullable=False, default=0)
    co2_sin_optimizar_kg = Column(DECIMAL(10, 3), nullable=False, default=0)
    estado = Column(String(20), nullable=False, default="Confirmada")
    fecha_generacion = Column(TIMESTAMP(timezone=True), server_default=func.now())
    operador = relationship("Usuario", back_populates="rutas")
    vehiculo = relationship("ParametrosVehiculo", back_populates="rutas")
    puntos = relationship("RutaPunto", back_populates="ruta", order_by="RutaPunto.orden")

class RutaPunto(Base):
    __tablename__ = "ruta_puntos"
    id_ruta_punto = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_ruta = Column(UUID(as_uuid=True), ForeignKey("rutas.id_ruta"), nullable=False)
    id_punto = Column(UUID(as_uuid=True), ForeignKey("puntos_entrega.id_punto"), nullable=False)
    orden = Column(Integer, nullable=False)
    ruta = relationship("Ruta", back_populates="puntos")
    punto = relationship("PuntoEntrega", back_populates="ruta_puntos")

    __table_args__ = (
        UniqueConstraint("id_ruta", "orden", name="uq_ruta_puntos_orden"),
        CheckConstraint("orden > 0", name="ck_orden_positivo"),
    )