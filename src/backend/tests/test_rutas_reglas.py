"""Pruebas de regresión para RN-002/RN-009, RN-013, US-007 y paginación."""
import uuid
from datetime import datetime, timezone
from types import SimpleNamespace

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.api.v1.endpoints import rutas
from app.api.v1.endpoints.dependencies import get_current_operador, get_current_user
from app.core.database import get_db
from app.main import app
from app.models import Ruta
from app.schemas import RutaResponse
from app.services.optimizer import build_route_response

OPERADOR_ID = uuid.uuid4()


class _Query:
    """Query falsa con los métodos encadenables usados por los endpoints."""

    def __init__(self, resultados=None, total=0):
        self.resultados = resultados if resultados is not None else []
        self.total = total

    def filter(self, *_args):
        return self

    def options(self, *_args):
        return self

    def order_by(self, *_args):
        return self

    def offset(self, *_args):
        return self

    def limit(self, *_args):
        return self

    def all(self):
        return self.resultados

    def first(self):
        return self.resultados[0] if self.resultados else None

    def count(self):
        return self.total

    def scalar(self):
        return self.total


class _FakeDB:
    def __init__(self, resultados=None, total=0):
        self.resultados = resultados or {}
        self.total = total

    def query(self, _entidad):
        return _Query(self.resultados.get("lista", []), self.total)


def _operador():
    return SimpleNamespace(id_usuario=OPERADOR_ID, rol=SimpleNamespace(nombre="Operador Logístico"))


def _respuesta_ruta():
    return RutaResponse(
        id_ruta=uuid.uuid4(),
        id_operador=OPERADOR_ID,
        id_vehiculo=1,
        distancia_total_km=1.0,
        tiempo_estimado_min=1.0,
        co2_estimado_kg=1.0,
        distancia_sin_optimizar_km=1.0,
        tiempo_sin_optimizar_min=1.0,
        co2_sin_optimizar_kg=1.0,
        estado="Confirmada",
        fecha_generacion=datetime.now(timezone.utc),
    )


@pytest.fixture(autouse=True)
def estado_limpio():
    app.dependency_overrides.clear()
    yield
    app.dependency_overrides.clear()


# --- RN-009 al confirmar ----------------------------------------------------

def test_validar_puntos_disponibles_rechaza_punto_en_uso():
    id_en_uso = uuid.uuid4()
    db = _FakeDB({"lista": [(id_en_uso,)]})
    with pytest.raises(HTTPException) as error:
        rutas._validar_puntos_disponibles(db, [id_en_uso, uuid.uuid4()])
    assert error.value.status_code == 400
    assert "ya pertenecen" in error.value.detail


def test_confirmar_ruta_rechaza_punto_ya_asignado(monkeypatch):
    id_en_uso = uuid.uuid4()
    db = _FakeDB({"lista": [(id_en_uso,)]})
    app.dependency_overrides[get_db] = lambda: db
    app.dependency_overrides[get_current_operador] = _operador
    monkeypatch.setattr(rutas, "_calcular_ruta", lambda *_args: (_respuesta_ruta(), []))
    persistido = []
    monkeypatch.setattr(rutas, "persist_ruta", lambda *_args: persistido.append(True))

    respuesta = TestClient(app).post(
        "/api/v1/rutas",
        json={"id_vehiculo": 1, "punto_ids": [str(id_en_uso), str(uuid.uuid4())]},
    )
    assert respuesta.status_code == 400
    assert "ya pertenecen" in respuesta.json()["detail"]
    assert persistido == []


def test_confirmar_ruta_con_puntos_libres_persiste(monkeypatch):
    db = _FakeDB({"lista": []})
    app.dependency_overrides[get_db] = lambda: db
    app.dependency_overrides[get_current_operador] = _operador
    monkeypatch.setattr(rutas, "_calcular_ruta", lambda *_args: (_respuesta_ruta(), []))
    persistido = []
    monkeypatch.setattr(rutas, "persist_ruta", lambda *_args: persistido.append(True))

    respuesta = TestClient(app).post(
        "/api/v1/rutas",
        json={"id_vehiculo": 1, "punto_ids": [str(uuid.uuid4()), str(uuid.uuid4())]},
    )
    assert respuesta.status_code == 201
    assert len(persistido) == 1


# --- RN-013 al editar -------------------------------------------------------

@pytest.mark.parametrize("estado", ["En curso", "Completada", "Cancelada"])
def test_editar_ruta_con_entregas_se_rechaza(estado):
    ruta = Ruta(id_ruta=uuid.uuid4(), id_operador=OPERADOR_ID, estado=estado)
    db = _FakeDB({"lista": [ruta]})
    app.dependency_overrides[get_db] = lambda: db
    app.dependency_overrides[get_current_operador] = _operador

    respuesta = TestClient(app).put(
        f"/api/v1/rutas/{ruta.id_ruta}",
        json={"id_vehiculo": 1, "punto_ids": [str(uuid.uuid4()), str(uuid.uuid4())]},
    )
    assert respuesta.status_code == 400
    assert "RN-013" in respuesta.json()["detail"]


# --- US-007 / fechas y paginación ------------------------------------------

def test_parsear_fecha_devuelve_utc():
    fecha = rutas._parsear_fecha("2026-03-15", fin_del_dia=True)
    assert fecha.tzinfo is not None
    assert fecha.utcoffset().total_seconds() == 0
    assert (fecha.hour, fecha.minute, fecha.second) == (23, 59, 59)


def test_respuesta_de_ruta_usa_fecha_con_zona_horaria():
    vehiculo = SimpleNamespace(
        consumo_litros_km=0.3,
        factor_emision_co2=2.6,
        velocidad_promedio_kmh=40,
    )
    respuesta = build_route_response(None, OPERADOR_ID, 1, [], 1.0, 2.0, vehiculo)
    assert respuesta.fecha_generacion.tzinfo is not None


def test_listado_rutas_con_skip_informa_pagina_efectiva():
    db = _FakeDB(total=50)
    app.dependency_overrides[get_db] = lambda: db
    app.dependency_overrides[get_current_user] = lambda: SimpleNamespace(
        id_usuario=OPERADOR_ID, rol=SimpleNamespace(nombre="Administrador")
    )

    respuesta = TestClient(app).get("/api/v1/rutas?skip=25&limit=12")
    assert respuesta.status_code == 200
    assert respuesta.headers["X-Page"] == "3"
    assert respuesta.headers["X-Total-Count"] == "50"


def test_listado_puntos_con_skip_informa_pagina_efectiva():
    db = _FakeDB(total=50)
    app.dependency_overrides[get_db] = lambda: db
    app.dependency_overrides[get_current_operador] = _operador

    respuesta = TestClient(app).get("/api/v1/puntos-entrega?skip=24&limit=12")
    assert respuesta.status_code == 200
    assert respuesta.json()["page"] == 3
