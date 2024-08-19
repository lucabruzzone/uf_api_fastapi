import pytest
from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)

# @pytest.mark.skip
def test_read_root():
    """
    Verifica que la ruta raíz ("/") de la API responde correctamente.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Health check baby"}  