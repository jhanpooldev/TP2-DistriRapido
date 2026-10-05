import pytest
from fastapi.testclient import TestClient

def test_demo_lima_endpoint(client: TestClient):
    """Verifica que el endpoint de demo devuelva un escenario válido con centro y 5 puntos."""
    response = client.get("/api/rutas/demo-lima")
    assert response.status_code == 200
    data = response.json()
    assert data["centro_distribucion"]["id"] == "CD-CENTRAL"
    assert len(data["puntos_entrega"]) == 5
    assert data["capacidad_vehiculo_kg"] == 1200.0

def test_optimizar_ruta_exitoso(client: TestClient):
    """Verifica la optimización de rutas, reducción de distancia y cálculo de CO2."""
    demo_data = client.get("/api/rutas/demo-lima").json()
    response = client.post("/api/rutas/optimizar", json=demo_data)
    assert response.status_code == 200
    data = response.json()
    assert "id_ruta" in data
    assert len(data["secuencia_puntos"]) == 7  # 1 CD inicial + 5 puntos + 1 CD final
    assert data["distancia_optimizada_km"] > 0
    assert data["distancia_no_optimizada_km"] >= data["distancia_optimizada_km"]
    assert data["distancia_ahorrada_km"] >= 0
    assert data["emisiones_co2_kg"] > 0
    assert data["utilizacion_capacidad_pct"] > 0
    assert data["tiempo_estimado_min"] > 0

def test_optimizar_ruta_exceso_capacidad_error(client: TestClient):
    """Verifica que si la carga excede la capacidad del vehículo se retorne HTTP 400 (RN-008)."""
    demo_data = client.get("/api/rutas/demo-lima").json()
    # Reducir la capacidad a un valor inferior a la carga total (405 kg)
    demo_data["capacidad_vehiculo_kg"] = 200.0

    response = client.post("/api/rutas/optimizar", json=demo_data)
    assert response.status_code == 400
    assert "supera la capacidad máxima" in response.json()["detail"]
