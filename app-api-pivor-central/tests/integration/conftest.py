import pytest
from httpx import ASGITransport, AsyncClient

from main import create_app


@pytest.fixture
def api_key() -> str:
    return "test-api-key"


@pytest.fixture
def app(api_key: str, monkeypatch):
    monkeypatch.setenv("API_KEY", api_key)
    return create_app()


@pytest.fixture
async def client(app, api_key: str):
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
        headers={"X-API-Key": api_key},
    ) as ac:
        yield ac
