import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.storage import storage


@pytest.fixture
def client():
    # TestClient without "with" does not run the lifespan, so no seed data is loaded.
    storage.reset()
    yield TestClient(app)
    storage.reset()


@pytest.fixture
def refeicao(client):
    payload = {"nome": "Feijoada", "tipo": "almoco", "data": "2026-11-26"}
    return client.post("/refeicoes", json=payload).json()
