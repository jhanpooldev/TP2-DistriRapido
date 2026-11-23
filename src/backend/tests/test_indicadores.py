"""Pruebas de RF-012, RF-013, RN-019 y RN-020."""
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from app.core.database import get_db
from app.api.v1.endpoints.dependencies import get_current_user
from app.main import app
from app.services.indicadores import (
    MENSAJE_SIN_DATOS,
    MENSAJE_SIN_SOSTENIBILIDAD,
    calcular_indicadores_logisticos,
    calcular_indicadores_sostenibilidad,
)


class _Query:
    def __init__(self, uno, escalar):
        self._uno = uno
        self._escalar = escalar

    def filter(self, *_args):
        return self

    def join(self, *_args):
        return self

    def one(self):
        return self._uno

    def scalar(self):
        return self._escalar


class _FakeDB:
    def __init__(self, uno=(0, 0.0, 0.0), escalar=0):
        self.uno = uno
        self.escalar = escalar

    def query(self, *_args):
        return _Query(self.uno, self.escalar)


@pytest.fixture(autouse=True)
def estado_limpio():
    app.dependency_overrides.clear()
    app.dependency_overrides[get_current_user] = lambda: SimpleNamespace(
        rol=SimpleNamespace(nombre="Gerente")
    )
    yield
    app.dependency_overrides.clear()


def test_calculo_logistico_sin_rutas_devuelve_cero_y_mensaje():
    resultado = calcular_indicadores_logisticos(0, 0, 0)
    assert resultado["cantidad_rutas"] == 0
    assert resultado["distancia_total_km"] == 0.0
    assert resultado["emisiones_estimadas_kg"] == 0.0
    assert resultado["mensaje"] == MENSAJE_SIN_DATOS


def test_calculo_logistico_suma_distancias_y_emisiones():
    resultado = calcular_indicadores_logisticos(3, 150.4567, 24.6)
    assert resultado["cantidad_rutas"] == 3
    assert resultado["distancia_total_km"] == 150.457
    assert resultado["emisiones_estimadas_kg"] == 24.6
    assert resultado["sin_datos"] is False


def test_calculo_sostenibilidad_por_entrega_y_ahorro():
    resultado = calcular_indicadores_sostenibilidad(24.0, 30.0, 12)
    assert resultado["emisiones_totales_kg"] == 24.0
    assert resultado["emisiones_por_entrega_kg"] == 2.0
    assert resultado["ahorro_co2_kg"] == 6.0
    assert resultado["ahorro_co2_pct"] == 20.0


def test_calculo_sostenibilidad_nunca_devuelve_ahorro_negativo():
    resultado = calcular_indicadores_sostenibilidad(30.0, 24.0, 10)
    assert resultado["ahorro_co2_kg"] == 0.0
    assert resultado["ahorro_co2_pct"] == 0.0


def test_calculo_sostenibilidad_sin_datos():
    resultado = calcular_indicadores_sostenibilidad(0, 0, 0)
    assert resultado["sin_datos"] is True
    assert resultado["mensaje"] == MENSAJE_SIN_SOSTENIBILIDAD
    assert resultado["emisiones_por_entrega_kg"] == 0.0


def test_endpoint_indicadores_devuelve_totales():
    app.dependency_overrides[get_db] = lambda: _FakeDB((3, 150.0, 24.6))
    respuesta = TestClient(app).get("/api/v1/indicadores")
    assert respuesta.status_code == 200
    assert respuesta.json()["cantidad_rutas"] == 3
    assert respuesta.json()["distancia_total_km"] == 150.0


def test_endpoint_indicadores_sin_rutas_muestra_mensaje():
    app.dependency_overrides[get_db] = lambda: _FakeDB()
    respuesta = TestClient(app).get("/api/v1/indicadores")
    assert respuesta.json()["mensaje"] == MENSAJE_SIN_DATOS


def test_endpoint_sostenibilidad_devuelve_comparacion():
    app.dependency_overrides[get_db] = lambda: _FakeDB((24.0, 30.0), escalar=12)
    respuesta = TestClient(app).get("/api/v1/indicadores/sostenibilidad")
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert datos["emisiones_por_entrega_kg"] == 2.0
    assert datos["ahorro_co2_pct"] == 20.0


def test_endpoint_sostenibilidad_sin_datos_muestra_mensaje():
    app.dependency_overrides[get_db] = lambda: _FakeDB((0, 0), escalar=0)
    respuesta = TestClient(app).get("/api/v1/indicadores/sostenibilidad")
    assert respuesta.json()["mensaje"] == MENSAJE_SIN_SOSTENIBILIDAD


def test_indicadores_requieren_autenticacion():
    app.dependency_overrides.pop(get_current_user)
    respuesta = TestClient(app).get("/api/v1/indicadores")
    assert respuesta.status_code == 401
