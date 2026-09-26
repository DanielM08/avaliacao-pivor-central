import pytest
from httpx import ASGITransport, AsyncClient

from main import create_app

pytestmark = pytest.mark.integration


@pytest.mark.asyncio
async def test_health_without_api_key(monkeypatch):
    monkeypatch.setenv("API_KEY", "secret")
    app = create_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_protected_route_requires_api_key(monkeypatch):
    monkeypatch.setenv("API_KEY", "secret")
    app = create_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/avaliacoes")
    assert response.status_code == 401
    assert response.json()["type"] == "AUTHORIZATION"


@pytest.mark.asyncio
async def test_create_and_get_avaliacao(client):
    payload = {
        "cadastro": {
            "fazenda": "Jalapão",
            "coordenadas": "-10.5432, -46.4123",
            "raio": 400,
            "espacamento": 5,
        }
    }
    created = await client.post("/api/v1/avaliacoes", json=payload)
    assert created.status_code == 201
    body = created.json()
    assert body["cadastro"]["fazenda"] == "Jalapão"
    assert body["coordenada_key"] == "-10.5432,-46.4123"

    fetched = await client.get(f"/api/v1/avaliacoes/{body['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["id"] == body["id"]
