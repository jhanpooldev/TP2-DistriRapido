"""RNF-004: medición local de la latencia de respuestas 401/403.

La consigna define el SLA en un entorno de producción de demostración. Esta
prueba no sustituye esa medición: usa ``TestClient`` en proceso, sin red ni
base de datos, para verificar que la capa de autenticación y RBAC responde por
debajo de 300 ms. El resultado se documenta como medición local.
"""
import statistics
from time import perf_counter
from types import SimpleNamespace
from typing import Iterator

import pytest
from fastapi.testclient import TestClient

from app.api.v1.endpoints.dependencies import get_current_user
from app.core.database import get_db
from app.main import app

LIMITE_MS = 300
MUESTRAS = 10


def _fabrica_db() -> Iterator[object]:
    # Las respuestas 401/403 se deciden antes de consultar la base de datos.
    yield object()


@pytest.fixture
def client() -> TestClient:
    app.dependency_overrides.clear()
    app.dependency_overrides[get_db] = _fabrica_db
    with TestClient(app) as prueba:
        yield prueba
    app.dependency_overrides.clear()


def _medir(cliente: TestClient, metodo: str, url: str, **kwargs) -> tuple[int, float]:
    inicio = perf_counter()
    respuesta = cliente.request(metodo, url, **kwargs)
    transcurrido_ms = (perf_counter() - inicio) * 1000
    return respuesta.status_code, transcurrido_ms


def _muestras(cliente: TestClient, metodo: str, url: str, **kwargs) -> list[float]:
    cliente.request(metodo, url, **kwargs)  # calentamiento; no se contabiliza
    return [_medir(cliente, metodo, url, **kwargs)[1] for _ in range(MUESTRAS)]


def _verificar_latencia(muestras: list[float]) -> None:
    mediana = statistics.median(muestras)
    maxima = max(muestras)
    assert maxima < LIMITE_MS, (
        f"Latencia local 401/403: mediana {mediana:.2f} ms, máxima {maxima:.2f} ms; "
        f"el SLA exige menos de {LIMITE_MS} ms"
    )


def test_sin_credenciales_devuelve_401_en_menos_de_300_ms(client: TestClient) -> None:
    muestras = _muestras(client, "GET", "/api/v1/auth/me")
    _verificar_latencia(muestras)

    codigo, _ = _medir(client, "GET", "/api/v1/auth/me")
    assert codigo == 401


def test_token_invalido_devuelve_401_en_menos_de_300_ms(client: TestClient) -> None:
    cabeceras = {"Authorization": "Bearer token-invalido"}
    muestras = _muestras(client, "GET", "/api/v1/auth/me", headers=cabeceras)
    _verificar_latencia(muestras)

    codigo, _ = _medir(client, "GET", "/api/v1/auth/me", headers=cabeceras)
    assert codigo == 401


def test_rol_sin_permiso_devuelve_403_en_menos_de_300_ms(client: TestClient) -> None:
    gerente = SimpleNamespace(
        rol=SimpleNamespace(nombre="Gerente"),
        nombre="Gerente",
        id_usuario="11111111-1111-1111-1111-111111111111",
    )
    app.dependency_overrides[get_current_user] = lambda: gerente

    muestras = _muestras(client, "GET", "/api/v1/puntos-entrega")
    _verificar_latencia(muestras)

    codigo, _ = _medir(client, "GET", "/api/v1/puntos-entrega")
    assert codigo == 403
