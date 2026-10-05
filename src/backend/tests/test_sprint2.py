"""Pruebas de Sprint 2: US-004 (ahorro de CO2) y US-007 (rangos de fechas)."""
import uuid
from datetime import datetime, timedelta

import pytest

from app.api.v1.endpoints.rutas import _parsear_fecha
from app.services.optimizer import (
    calcular_ahorro,
    co2_kg_por_km,
    calculate_co2,
)


class VehiculoFalso:
    consumo_litros_km = 0.5
    factor_emision_co2 = 2.31
    velocidad_promedio_kmh = 30.0


@pytest.fixture
def vehiculo():
    return VehiculoFalso()


# --- US-004 CA1: porcentaje de reducción de CO2 -------------------------------

def test_ahorro_co2_pct_es_positivo(vehiculo):
    """Una ruta 20% mas corta reporta 20% menos CO2."""
    ahorro = calcular_ahorro(80.0, 100.0, co2_kg_por_km(vehiculo))
    assert ahorro["ahorro_co2_pct"] == 20.0
    assert ahorro["ahorro_distancia_pct"] == 20.0
    assert ahorro["sin_reduccion_significativa"] is False


def test_ahorro_co2_kg_usa_factor_del_vehiculo(vehiculo):
    """Los kg ahorrados deben venir del factor de emision, no de los km."""
    ahorro = calcular_ahorro(80.0, 100.0, co2_kg_por_km(vehiculo))
    esperado = 20.0 * 0.5 * 2.31
    assert ahorro["ahorro_co2_kg"] == pytest.approx(esperado, abs=0.01)


def test_ahorro_co2_kg_es_consistente_con_las_emisiones(vehiculo):
    """kg ahorrados == diferencia entre ambas emisiones estimadas."""
    dist_opt, dist_no_opt = 42.5, 61.3
    ahorro = calcular_ahorro(dist_opt, dist_no_opt, co2_kg_por_km(vehiculo))
    diferencia = calculate_co2(dist_no_opt, vehiculo) - calculate_co2(dist_opt, vehiculo)
    assert ahorro["ahorro_co2_kg"] == pytest.approx(diferencia, abs=0.01)


def test_sin_factor_devuelve_ahorro_co2_en_ceros():
    """Sin datos de emision no se inventan kg de CO2."""
    ahorro = calcular_ahorro(80.0, 100.0)
    assert ahorro["ahorro_co2_kg"] == 0.0
    assert ahorro["ahorro_co2_pct"] == 20.0


# --- US-004 CA2: caso sin reducción significativa -----------------------------

def test_casi_iguales_marca_sin_reduccion_significativa(vehiculo):
    """Diferencia menor al 1% no se reporta como ahorro."""
    ahorro = calcular_ahorro(99.5, 100.0, co2_kg_por_km(vehiculo))
    assert ahorro["sin_reduccion_significativa"] is True
    assert ahorro["ahorro_co2_pct"] == 0.5


def test_ahorro_negativo_se_acota_en_cero(vehiculo):
    """Una ruta peor nunca reporta ahorro negativo (RN-018)."""
    ahorro = calcular_ahorro(120.0, 100.0, co2_kg_por_km(vehiculo))
    assert ahorro["ahorro_co2_pct"] == 0.0
    assert ahorro["ahorro_co2_kg"] == 0.0
    assert ahorro["ahorro_distancia_pct"] == 0.0
    assert ahorro["sin_reduccion_significativa"] is True


def test_umbral_justo_limite_ya_es_significativo(vehiculo):
    """El umbral es 1%: exactamente 1% ya cuenta como reducción."""
    ahorro = calcular_ahorro(99.0, 100.0, co2_kg_por_km(vehiculo))
    assert ahorro["ahorro_co2_pct"] == 1.0
    assert ahorro["sin_reduccion_significativa"] is False


def test_justo_bajo_umbral_no_es_significativo(vehiculo):
    """Por debajo del 1% no se reporta ahorro."""
    ahorro = calcular_ahorro(99.1, 100.0, co2_kg_por_km(vehiculo))
    assert ahorro["ahorro_co2_pct"] == 0.9
    assert ahorro["sin_reduccion_significativa"] is True


def test_sobre_umbral_marca_significativa(vehiculo):
    ahorro = calcular_ahorro(98.0, 100.0, co2_kg_por_km(vehiculo))
    assert ahorro["ahorro_co2_pct"] == 2.0
    assert ahorro["sin_reduccion_significativa"] is False


def test_distancia_base_cero_no_divide(vehiculo):
    """Evita ZeroDivisionError."""
    ahorro = calcular_ahorro(0.0, 0.0, co2_kg_por_km(vehiculo))
    assert ahorro["ahorro_co2_pct"] == 0.0
    assert ahorro["ahorro_co2_kg"] == 0.0
    assert ahorro["sin_reduccion_significativa"] is True


# --- US-007: filtros por rango de fechas --------------------------------------

def test_parsear_fecha_acepta_solo_fecha():
    fecha = _parsear_fecha("2026-03-15")
    assert fecha is not None
    assert (fecha.year, fecha.month, fecha.day) == (2026, 3, 15)


def test_parsear_fecha_hasta_cierra_el_dia():
    """Un rango inclusivo debe incluir todo el dia 'hasta'."""
    fecha = _parsear_fecha("2026-03-15", fin_del_dia=True)
    assert fecha.hour == 23 and fecha.minute == 59 and fecha.second == 59


def test_parsear_fecha_desde_empieza_en_cero():
    fecha = _parsear_fecha("2026-03-15")
    assert (fecha.hour, fecha.minute, fecha.second) == (0, 0, 0)


def test_parsear_fecha_acepta_iso_completo():
    fecha = _parsear_fecha("2026-03-15T10:30:00")
    assert fecha is not None
    assert (fecha.hour, fecha.minute) == (10, 30)


def test_parsear_fecha_rechaza_texto_invalido():
    """Un formato ilegible devuelve None para no filtrar en silencio."""
    assert _parsear_fecha("no-es-fecha") is None
    assert _parsear_fecha("15/03/2026") is None
    assert _parsear_fecha("") is None


def test_parsear_fecha_desde_hasta_ordenados():
    """El rango completo debe poder construirse desde el formulario."""
    desde = _parsear_fecha("2026-03-01")
    hasta = _parsear_fecha("2026-03-31", fin_del_dia=True)
    assert desde < hasta