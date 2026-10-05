"""Pruebas de la correccion de auditoria: rol en /auth/me, health y schemas."""
import pytest

from app.api.v1.endpoints.salud import health
from app.core.database import get_db
from app.main import app
from app.schemas import RolResponse, RutaResponse, UsuarioResponse


class SesionFalla:
    """Sesion que simula una base de datos inaccesible."""

    def execute(self, *args, **kwargs):
        from sqlalchemy.exc import OperationalError

        raise OperationalError("SELECT 1", {}, Exception("sin conexion"))

    def rollback(self):
        self.sesion_rollback = True


class Respuesta:
    def __init__(self):
        self.status_code = 200


def test_health_ok_devuelve_200():
    class SesionOk:
        def execute(self, *args, **kwargs):
            return 1

    respuesta = Respuesta()
    resultado = health(respuesta, SesionOk())
    assert respuesta.status_code == 200
    assert resultado["estado"] == "ok"
    assert resultado["base_datos"] == "ok"


def test_health_sin_bd_devuelve_503():
    sesion = SesionFalla()
    respuesta = Respuesta()
    resultado = health(respuesta, sesion)

    assert respuesta.status_code == 503
    assert resultado["estado"] == "degradado"
    assert resultado["base_datos"] == "error"
    assert getattr(sesion, "sesion_rollback", False) is True


def test_health_esta_registrado_en_ambas_rutas():
    paths = {r.path for r in app.routes}
    assert "/api/v1/health" in paths
    assert "/health" in paths


def test_ambos_health_comparten_el_mismo_handler():
    por_api = [r for r in app.routes if r.path == "/api/v1/health"]
    por_raiz = [r for r in app.routes if r.path == "/health"]
    assert len(por_api) == 1 and len(por_raiz) == 1
    assert por_api[0].endpoint is por_raiz[0].endpoint


def _usuario(**kwargs):
    base = dict(
        id_usuario="11111111-1111-1111-1111-111111111111",
        nombre="Operador Demo",
        correo="operador@distrirapido.com",
        id_rol=2,
        fecha_creacion="2026-01-01T00:00:00",
        rol=RolResponse(id_rol=2, nombre="Operador Logístico", descripcion="Gestiona puntos y rutas"),
    )
    base.update(kwargs)
    return UsuarioResponse(**base)


def test_usuario_response_expone_rol_anidado():
    datos = _usuario().model_dump()
    assert datos["rol"]["nombre"] == "Operador Logístico"
    assert datos["rol"]["id_rol"] == 2


def test_usuario_response_no_expone_hash():
    assert "contrasena_hash" not in _usuario().model_dump()


def test_rol_es_obligatorio():
    """id_rol es NOT NULL: un usuario sin rol es corrupcion de datos."""
    with pytest.raises(Exception):
        _usuario(rol=None)


def test_ruta_response_puntos_no_comparten_lista_por_defecto():
    """Evita el default mutable: cada RutaResponse debe tener su propia lista."""
    base = dict(
        id_operador="11111111-1111-1111-1111-111111111111",
        id_vehiculo=1,
        distancia_total_km=10.0,
        tiempo_estimado_min=20.0,
        co2_estimado_kg=1.0,
        distancia_sin_optimizar_km=12.0,
        tiempo_sin_optimizar_min=25.0,
        co2_sin_optimizar_kg=1.5,
        estado="Confirmada",
        fecha_generacion="2026-01-01T00:00:00",
    )
    primera = RutaResponse(id_ruta="22222222-2222-2222-2222-222222222222", puntos=[], **base)
    segunda = RutaResponse(id_ruta="44444444-4444-4444-4444-444444444444", **base)

    assert primera.puntos == [] and segunda.puntos == []
    primera.puntos.append("nuevo")
    assert segunda.puntos == []


def test_get_db_cierra_la_sesion():
    import inspect

    fuente = inspect.getsource(get_db)
    assert "finally" in fuente
    assert "close()" in fuente


def test_health_503_por_http():
    from fastapi.testclient import TestClient

    def get_db_roto():
        yield SesionFalla()

    app.dependency_overrides[get_db] = get_db_roto
    try:
        # Sin `with`: no se dispara el lifespan, asi que la BD real no se toca.
        cliente = TestClient(app)
        r = cliente.get("/api/v1/health")
        assert r.status_code == 503
        assert r.json()["estado"] == "degradado"

        r_raiz = cliente.get("/health")
        assert r_raiz.status_code == 503
        assert r_raiz.json()["base_datos"] == "error"
    finally:
        app.dependency_overrides.clear()