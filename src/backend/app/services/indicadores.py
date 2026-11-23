"""Cálculo de indicadores a partir de rutas confirmadas (RN-019 y RN-020).

Las funciones son puras para que el criterio de cálculo pueda verificarse sin
base de datos; los endpoints solo se encargan de agregar las filas.
"""
MENSAJE_SIN_DATOS = "No hay datos disponibles para generar indicadores"
MENSAJE_SIN_SOSTENIBILIDAD = "No hay datos de sostenibilidad disponibles para generar indicadores"


def calcular_indicadores_logisticos(
    cantidad_rutas: int, distancia_total_km: float, emisiones_estimadas_kg: float
) -> dict:
    """RN-020: rutas, distancia y emisiones; cero y aviso si no hay rutas."""
    sin_datos = int(cantidad_rutas) == 0
    return {
        "cantidad_rutas": int(cantidad_rutas),
        "distancia_total_km": round(max(0.0, float(distancia_total_km)), 3),
        "emisiones_estimadas_kg": round(max(0.0, float(emisiones_estimadas_kg)), 3),
        "sin_datos": sin_datos,
        "mensaje": MENSAJE_SIN_DATOS if sin_datos else None,
    }


def calcular_indicadores_sostenibilidad(
    emisiones_optimizadas_kg: float,
    emisiones_sin_optimizar_kg: float,
    entregas: int,
) -> dict:
    """RN-019: total, por entrega y ahorro frente al recorrido sin optimizar."""
    optimizadas = max(0.0, float(emisiones_optimizadas_kg))
    sin_optimizar = max(0.0, float(emisiones_sin_optimizar_kg))
    cantidad_entregas = max(0, int(entregas))
    ahorro = max(0.0, sin_optimizar - optimizadas)  # RN-018: sin porcentajes negativos.
    ahorro_pct = (ahorro / sin_optimizar * 100) if sin_optimizar > 0 else 0.0
    sin_datos = cantidad_entregas == 0 or (optimizadas <= 0 and sin_optimizar <= 0)
    return {
        "emisiones_totales_kg": round(optimizadas, 3),
        "emisiones_por_entrega_kg": round(optimizadas / cantidad_entregas, 4) if cantidad_entregas else 0.0,
        "ahorro_co2_kg": round(ahorro, 3),
        "ahorro_co2_pct": round(ahorro_pct, 2),
        "entregas": cantidad_entregas,
        "sin_datos": sin_datos,
        "mensaje": MENSAJE_SIN_SOSTENIBILIDAD if sin_datos else None,
    }
