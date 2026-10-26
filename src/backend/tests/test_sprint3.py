"""Pruebas del Sprint 3: exportacion CSV del resumen de ruta (US-008)."""
import csv
import io
import uuid
from datetime import datetime

import pytest
from pydantic import ValidationError

from app.core.config import Settings, get_settings
from app.main import app
from app.schemas import PuntoRutaResponse, ResumenRuta
from app.services.exportacion import (
    celda_csv,
    generar_csv_resumen,
    nombre_archivo_csv,
)


class RutaFalsa:
    def __init__(self):
        self.id_ruta = uuid.UUID("12345678-1234-1234-1234-123456789abc")
        self.fecha_generacion = datetime(2026, 11, 5, 14, 30, 0)
        self.estado = "Confirmada"


def _punto(orden: int, destinatario: str, direccion: str, latitud: float = -12.115, longitud: float = -77.02):
    return PuntoRutaResponse(
        id_punto=uuid.uuid4(),
        orden=orden,
        direccion=direccion,
        latitud=latitud,
        longitud=longitud,
        peso_kg=10.5,
        destinatario=destinatario,
    )


@pytest.fixture
def resumen():
    return ResumenRuta(
        id_ruta=uuid.UUID("12345678-1234-1234-1234-123456789abc"),
        puntos=[
            _punto(2, "Cliente B", "Av. Siempre Viva 742"),
            _punto(1, "Cliente A", "Jr. Los Olivos 123"),
        ],
        distancia_total_km=18.4,
        tiempo_estimado_min=42.0,
        co2_estimado_kg=5.9133,
        distancia_sin_optimizar_km=24.1,
        tiempo_sin_optimizar_min=55.0,
        co2_sin_optimizar_kg=7.746,
        ahorro_co2_kg=1.8327,
        ahorro_co2_pct=23.66,
        ahorro_distancia_pct=23.65,
        sin_reduccion_significativa=False,
    )


def _filas(contenido: bytes):
    texto = contenido.decode("utf-8-sig")
    return list(csv.reader(io.StringIO(texto)))


def test_csv_incluye_puntos_en_orden_de_visita(resumen):
    filas = _filas(generar_csv_resumen(RutaFalsa(), resumen))
    indice_cabecera = filas.index(["Orden", "Destinatario", "Direccion", "Latitud", "Longitud", "Peso (kg)"])

    puntos = filas[indice_cabecera + 1:]
    assert [fila[0] for fila in puntos] == ["1", "2"]
    assert [fila[1] for fila in puntos] == ["Cliente A", "Cliente B"]


def test_csv_incluye_impacto_ambiental(resumen):
    texto = generar_csv_resumen(RutaFalsa(), resumen).decode("utf-8-sig")

    assert "Impacto estimado" in texto
    assert "Distancia optimizada (km),18.4" in texto
    assert "Ahorro de CO2 (kg),1.8327" in texto
    assert "Reduccion significativa,Si" in texto


def test_csv_neutraliza_formulas_en_texto(resumen):
    resumen.puntos = [
        _punto(1, '=HYPERLINK("http://malicioso")', "+SUM(1,1)"),
        _punto(2, "@comando", "Direccion normal"),
    ]

    filas = _filas(generar_csv_resumen(RutaFalsa(), resumen))
    indice_cabecera = filas.index(["Orden", "Destinatario", "Direccion", "Latitud", "Longitud", "Peso (kg)"])
    primera = filas[indice_cabecera + 1]

    assert primera[1].startswith("'=")
    assert primera[2].startswith("'+")
    assert filas[indice_cabecera + 2][1].startswith("'@")


def test_coordenadas_negativas_no_se_escapan(resumen):
    """Un signo menos en una coordenada es un numero, no una formula."""
    filas = _filas(generar_csv_resumen(RutaFalsa(), resumen))
    indice_cabecera = filas.index(["Orden", "Destinatario", "Direccion", "Latitud", "Longitud", "Peso (kg)"])
    primera = filas[indice_cabecera + 1]

    assert primera[3] == "-12.115"
    assert primera[4] == "-77.02"


def test_celda_csv_conserva_numeros_y_nulos():
    assert celda_csv(-12.5) == -12.5
    assert celda_csv(None) is None
    assert celda_csv("texto normal") == "texto normal"


def test_celda_csv_detecta_formula_con_espacios_iniciales():
    assert celda_csv("   =1+1").startswith("'")


def test_nombre_archivo_es_ascii_y_predecible():
    assert nombre_archivo_csv(RutaFalsa()) == "ruta-12345678-20261105.csv"


def test_endpoint_de_exportacion_esta_registrado():
    paths = {ruta.path for ruta in app.routes}
    assert "/api/v1/rutas/{ruta_id}/export" in paths


# --- Endurecimiento de configuracion y respuestas ---------------------------

def test_cors_no_usa_comodin_por_defecto():
    origenes = get_settings().origenes_cors
    assert "*" not in origenes
    assert "http://localhost:5173" in origenes


def test_produccion_rechaza_secreto_de_ejemplo():
    with pytest.raises(ValidationError):
        Settings(
            ENVIRONMENT="production",
            JWT_SECRET="clave-secreta-super-segura-para-desarrollo",
            _env_file=None,
        )


def test_produccion_rechaza_secreto_corto():
    with pytest.raises(ValidationError):
        Settings(ENVIRONMENT="production", JWT_SECRET="corto", _env_file=None)


def test_produccion_acepta_secreto_largo():
    settings = Settings(
        ENVIRONMENT="production",
        JWT_SECRET="a" * 64,
        _env_file=None,
    )
    assert settings.ENVIRONMENT == "production"


def test_cabeceras_de_seguridad_y_correlacion():
    from fastapi.testclient import TestClient

    cliente = TestClient(app)
    respuesta = cliente.get("/", headers={"X-Request-ID": "prueba-123"})

    assert respuesta.status_code == 200
    assert respuesta.headers["X-Request-ID"] == "prueba-123"
    assert respuesta.headers["X-Content-Type-Options"] == "nosniff"
    assert respuesta.headers["X-Frame-Options"] == "DENY"
    assert respuesta.headers["Referrer-Policy"] == "no-referrer"
