"""Pruebas de validacion. Cubre US-001 y US-003."""
import uuid

import pytest
from pydantic import ValidationError

from app.schemas import PuntoEntregaCreate, RutaOptimizarRequest


def punto_valido(**overrides):
    datos = {
        "direccion": "Av. Javier Prado Este 4200",
        "latitud": -12.115,
        "longitud": -76.97,
        "peso_kg": 10.0,
        "destinatario": "Cliente Demo",
    }
    datos.update(overrides)
    return datos


def test_punto_valido_se_acepta():
    punto = PuntoEntregaCreate(**punto_valido())
    assert punto.latitud == -12.115


def test_direccion_vacia_o_solo_espacios_se_rechaza():
    with pytest.raises(ValidationError):
        PuntoEntregaCreate(**punto_valido(direccion="   "))


def test_destinatario_vacio_se_rechaza():
    with pytest.raises(ValidationError):
        PuntoEntregaCreate(**punto_valido(destinatario=" "))


@pytest.mark.parametrize(
    "campo,valor",
    [
        ("latitud", 91),
        ("latitud", -91),
        ("longitud", 181),
        ("longitud", -181),
    ],
)
def test_coordenada_fuera_de_rango_se_rechaza(campo, valor):
    with pytest.raises(ValidationError):
        PuntoEntregaCreate(**punto_valido(**{campo: valor}))


def test_coordenadas_no_geolocalizables_se_rechazan():
    """US-001: un punto que no pudo geolocalizarse no debe registrarse."""
    with pytest.raises(ValidationError) as error:
        PuntoEntregaCreate(**punto_valido(latitud=0, longitud=0))

    assert "geolocalizarse" in str(error.value)


def test_peso_deve_ser_positivo():
    with pytest.raises(ValidationError):
        PuntoEntregaCreate(**punto_valido(peso_kg=0))


def test_ruta_acepta_lista_de_puntos():
    ids = [uuid.uuid4(), uuid.uuid4()]
    request = RutaOptimizarRequest(id_vehiculo=1, punto_ids=ids)
    assert len(request.punto_ids) == 2