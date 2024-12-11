import pytest
from fastapi.testclient import TestClient
from app.main import app  # Importa tu aplicación principal

# Crear cliente de prueba
@pytest.fixture
def client():
    return TestClient(app)
