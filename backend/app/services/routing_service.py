import math
from typing import List, Tuple, Dict, Any

def calcular_distancia_haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calcula la distancia ortodrómica en kilómetros entre dos coordenadas geográficas
    utilizando la fórmula del semiverseno (Haversine).
    """
    R = 6371.0  # Radio medio de la Tierra en kilómetros
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(d_lon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 3)

def calcular_matriz_distancias(puntos: List[Dict[str, Any]]) -> List[List[float]]:
    """Genera una matriz simétrica de distancias en km entre todos los puntos."""
    n = len(puntos)
    matriz = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            d = calcular_distancia_haversine(
                puntos[i]["latitud"], puntos[i]["longitud"],
                puntos[j]["latitud"], puntos[j]["longitud"]
            )
            matriz[i][j] = d
            matriz[j][i] = d
    return matriz

def optimizar_tsp_2opt(matriz: List[List[float]]) -> Tuple[List[int], float]:
    """
    Resuelve el Problema del Viajero (TSP) utilizando la heurística de Vecino Más Próximo
    seguida de refinamiento local mediante intercambios 2-opt.
    El punto 0 es siempre el Centro de Distribución (origen y destino).
    """
    n = len(matriz)
    if n <= 1:
        return [0], 0.0
    if n == 2:
        return [0, 1, 0], round(matriz[0][1] * 2, 2)

    # Paso 1: Construcción inicial por Vecino Más Próximo
    visitados = [False] * n
    ruta = [0]
    visitados[0] = True
    actual = 0

    for _ in range(n - 1):
        mejor_dist = float("inf")
        siguiente = -1
        for j in range(n):
            if not visitados[j] and matriz[actual][j] < mejor_dist:
                mejor_dist = matriz[actual][j]
                siguiente = j
        if siguiente != -1:
            ruta.append(siguiente)
            visitados[siguiente] = True
            actual = siguiente

    ruta.append(0)  # Retorno al centro de distribución

    # Paso 2: Refinamiento local 2-opt
    mejorado = True
    max_iter = 50
    iter_count = 0

    def distancia_total(r: List[int]) -> float:
        return sum(matriz[r[k]][r[k + 1]] for k in range(len(r) - 1))

    mejor_distancia = distancia_total(ruta)

    while mejorado and iter_count < max_iter:
        mejorado = False
        iter_count += 1
        for i in range(1, len(ruta) - 2):
            for j in range(i + 1, len(ruta) - 1):
                # Nuevo tramo invirtiendo el segmento entre i y j
                nueva_ruta = ruta[:i] + ruta[i:j + 1][::-1] + ruta[j + 1:]
                d = distancia_total(nueva_ruta)
                if d < mejor_distancia - 0.001:
                    ruta = nueva_ruta
                    mejor_distancia = d
                    mejorado = True
                    break
            if mejorado:
                break

    return ruta, round(mejor_distancia, 2)

def estimar_emisiones_co2(distancia_km: float, tipo_vehiculo: str = "van_diesel") -> float:
    """
    Calcula las emisiones estimadas de CO2 en kg.
    Factores de emisión estándar en logística urbana:
    - van_diesel: 0.240 kg CO2 / km
    - van_gnv: 0.180 kg CO2 / km
    - van_electrica: 0.045 kg CO2 / km
    """
    factores = {
        "van_diesel": 0.240,
        "van_gnv": 0.180,
        "van_electrica": 0.045
    }
    factor = factores.get(tipo_vehiculo.lower(), 0.240)
    return round(distancia_km * factor, 3)
