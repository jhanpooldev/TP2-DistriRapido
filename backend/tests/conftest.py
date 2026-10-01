import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.models.auth import db_auth

@pytest.fixture(autouse=True)
def clean_db():
    """Limpia el almacén de datos antes de cada prueba unitaria."""
    db_auth.limpiar_todo()
    yield
    db_auth.limpiar_todo()

@pytest.fixture
def client():
    """Cliente HTTP de prueba para la API FastAPI."""
    return TestClient(app)
