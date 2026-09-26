import pytest

from tests.conftest import assert_matches_golden
from tests.fixtures.loader import load_ensaio_exemplo

pytestmark = [pytest.mark.integration, pytest.mark.golden]


@pytest.mark.asyncio
async def test_calculo_stateless_response_matches_golden(client):
    data = load_ensaio_exemplo()
    response = await client.post(
        "/api/v1/calculos/uniformidade",
        json={"coletores": data["coletores"]},
    )
    assert response.status_code == 200
    body = response.json()
    subset = {
        "indicadores": body["indicadores"],
        "classificacao": body["classificacao"],
    }
    assert_matches_golden(subset, "uniformidade/calculo_stateless.json")
