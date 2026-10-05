"""Pruebas del motor de ruteo. Cubre US-003 y EN-01."""
import time

import pytest

from app.core.config import get_settings
from app.services.optimizer import (
    haversine,
    nearest_neighbor,
    route_distance,
    two_opt,
    calculate_co2,
    calculate_time_min,
)

settings = get_settings()
HOME_LAT = settings.HOME_LAT
HOME_LNG = settings.HOME_LNG


class VehiculoFalso:
    consumo_litros_km = 0.5
    factor_emision_co2 = 2.31
    velocidad_promedio_kmh = 30.0


def test_haversine_distancia_conocida():
    # Lima centro -> Bogota es ~1892 km en linea recta
    distancia = haversine(-12.0464, -77.0428, 4.7110, -74.0721)
    assert 1850 < distancia < 1930


def test_haversine_misma_coordenada_es_cero():
    assert haversine(-12.115, -76.97, -12.115, -76.97) == 0.0


def test_veinte_puntos_completan_todos(punto_factory):
    puntos = [punto_factory(-12.05 + i * 0.01, -77.0, str(i)) for i in range(20)]
    ruta, distancia = nearest_neighbor(puntos, HOME_LAT, HOME_LNG)

    assert len(ruta) == 20
    assert distancia > 0
    assert {p.id_punto for p in ruta} == {p.id_punto for p in puntos}


def test_vecino_cercano_empieza_en_el_mas_cercano(punto_factory):
    cercano = punto_factory(-12.116, -76.971, "cercano")
    lejano = punto_factory(-12.30, -77.20, "lejano")

    ruta, _ = nearest_neighbor([lejano, cercano], HOME_LAT, HOME_LNG)

    assert ruta[0].id_punto == cercano.id_punto


def test_two_opt_no_empeora_la_distancia(punto_factory):
    puntos = [punto_factory(-12.05 + i * 0.02, -77.0 + (i % 3) * 0.02, str(i)) for i in range(10)]

    inicial, _ = nearest_neighbor(puntos, HOME_LAT, HOME_LNG)
    optimizada = two_opt(inicial, HOME_LAT, HOME_LNG)

    assert route_distance(optimizada, HOME_LAT, HOME_LNG) <= route_distance(inicial, HOME_LAT, HOME_LNG)


def test_two_opt_respeta_el_ruta_si_menos_de_tres_puntos(punto_factory):
    ruta = [punto_factory(-12.05, -77.0, "1"), punto_factory(-12.07, -77.02, "2")]
    assert two_opt(ruta, HOME_LAT, HOME_LNG) == ruta


def test_two_opt_conserva_todos_los_puntos(punto_factory):
    puntos = [punto_factory(-12.05 + i * 0.02, -77.0 + (i % 4) * 0.01, str(i)) for i in range(12)]
    inicial, _ = nearest_neighbor(puntos, HOME_LAT, HOME_LNG)
    optimizada = two_opt(inicial, HOME_LAT, HOME_LNG)

    assert len(optimizada) == len(puntos)
    assert {p.id_punto for p in optimizada} == {p.id_punto for p in puntos}


def test_rendimiento_veinte_puntos_menor_a_cinco_segundos(veinte_puntos):
    """EN-01: SLA de 5 segundos con 20 puntos."""
    duraciones = []

    for _ in range(5):
        inicio = time.perf_counter()
        ruta, _ = nearest_neighbor(veinte_puntos, HOME_LAT, HOME_LNG)
        ruta = two_opt(ruta, HOME_LAT, HOME_LNG)
        duraciones.append(time.perf_counter() - inicio)

    assert len(ruta) == 20
    assert max(duraciones) < 5.0, f"superó el SLA: {max(duraciones):.3f}s"


def test_calculo_de_co2_y_tiempo():
    vehiculo = VehiculoFalso()

    co2 = calculate_co2(10.0, vehiculo)
    minutos = calculate_time_min(10.0, vehiculo)

    assert co2 == pytest.approx(10.0 * 0.5 * 2.31)
    assert minutos == pytest.approx(10.0 / 30.0 * 60)
    assert co2 > 0
    assert minutos > 0