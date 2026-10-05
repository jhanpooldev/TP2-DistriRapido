import uuid
from datetime import datetime, timezone

import pytest

from app.schemas import PuntoEntregaResponse


@pytest.fixture
def punto_factory():
    def _crear(latitud: float, longitud: float, sufijo: str = "A") -> PuntoEntregaResponse:
        return PuntoEntregaResponse(
            id_punto=uuid.uuid4(),
            direccion=f"Direccion de prueba {sufijo}",
            latitud=latitud,
            longitud=longitud,
            peso_kg=5.0,
            destinatario=f"Destinatario {sufijo}",
            id_operador=uuid.uuid4(),
            fecha_registro=datetime.now(timezone.utc).replace(tzinfo=None),
        )

    return _crear


@pytest.fixture
def veinte_puntos(punto_factory):
    return [
        punto_factory(-12.05 + i * 0.01, -77.00 + (i % 5) * 0.01, str(i))
        for i in range(20)
    ]