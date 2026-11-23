"""RF-005 / RN-009: edición y eliminación solo de puntos libres."""
import uuid
from datetime import datetime, timezone
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from app.api.v1.endpoints import puntos
from app.api.v1.endpoints.dependencies import get_current_operador
from app.core.database import get_db
from app.main import app
from app.models import PuntoEntrega

OPERADOR_ID = uuid.uuid4()
PAYLOAD = {
    "direccion": "Av. Nueva 123",
    "latitud": -12.1,
    "longitud": -77.0,
    "peso_kg": 7.5,
    "destinatario": "Nuevo destinatario",
}


class _Query:
    def __init__(self, entidad, punto=None, en_ruta=False):
        self.entidad = entidad
        self.punto = punto
        self.en_ruta = en_ruta

    def filter(self, *_args):
        return self

    def join(self, *_args):
        return self

    def first(self):
        if self.entidad is PuntoEntrega:
            return self.punto
        return (1,) if self.en_ruta else None


class _FakeDB:
    def __init__(self, punto=None, en_ruta=False):
        self.punto = punto
        self.en_ruta = en_ruta
        self.operaciones = []

    def query(self, entidad):
        return _Query(entidad, self.punto, self.en_ruta)

    def commit(self):
        self.operaciones.append("commit")

    def refresh(self, _obj):
        self.operaciones.append("refresh")

    def delete(self, _obj):
        self.operaciones.append("delete")


@pytest.fixture(autouse=True)
def estado_limpio():
    app.dependency_overrides.clear()
    app.dependency_overrides[get_current_operador] = lambda: SimpleNamespace(
        id_usuario=OPERADOR_ID
    )
    yield
    app.dependency_overrides.clear()


def _punto_libre():
    return PuntoEntrega(
        id_punto=uuid.uuid4(),
        direccion="Av. Vieja 456",
        latitud=-12.2,
        longitud=-77.1,
        peso_kg=3.0,
        destinatario="Destinatario original",
        id_operador=OPERADOR_ID,
        fecha_registro=datetime.now(timezone.utc).replace(tzinfo=None),
    )


def test_editar_punto_libre_actualiza_datos():
    punto = _punto_libre()
    db = _FakeDB(punto=punto)
    app.dependency_overrides[get_db] = lambda: db

    respuesta = TestClient(app).put(f"/api/v1/puntos-entrega/{punto.id_punto}", json=PAYLOAD)

    assert respuesta.status_code == 200
    assert respuesta.json()["direccion"] == PAYLOAD["direccion"]
    assert respuesta.json()["peso_kg"] == PAYLOAD["peso_kg"]
    assert "commit" in db.operaciones


def test_editar_punto_en_ruta_confirmada_se_rechaza():
    punto = _punto_libre()
    app.dependency_overrides[get_db] = lambda: _FakeDB(punto=punto, en_ruta=True)

    respuesta = TestClient(app).put(f"/api/v1/puntos-entrega/{punto.id_punto}", json=PAYLOAD)

    assert respuesta.status_code == 400
    assert respuesta.json()["detail"] == puntos.MENSAJE_EDITAR_PROTEGIDO


def test_eliminar_punto_libre_devuelve_204():
    punto = _punto_libre()
    db = _FakeDB(punto=punto)
    app.dependency_overrides[get_db] = lambda: db

    respuesta = TestClient(app).delete(f"/api/v1/puntos-entrega/{punto.id_punto}")

    assert respuesta.status_code == 204
    assert "delete" in db.operaciones


def test_eliminar_punto_en_ruta_confirmada_muestra_mensaje_documentado():
    punto = _punto_libre()
    app.dependency_overrides[get_db] = lambda: _FakeDB(punto=punto, en_ruta=True)

    respuesta = TestClient(app).delete(f"/api/v1/puntos-entrega/{punto.id_punto}")

    assert respuesta.status_code == 400
    assert respuesta.json()["detail"] == "No se puede eliminar un punto incluido en una ruta confirmada"
