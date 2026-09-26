import pytest

from tests.conftest import load_golden
from tests.fixtures.loader import load_ensaio_exemplo

pytestmark = pytest.mark.integration


@pytest.mark.asyncio
async def test_fluxo_uniformidade_post_put_get(client):
    data = load_ensaio_exemplo()
    cad = data["cadastro"]
    esperado = load_golden("uniformidade/indicadores.json")

    created = await client.post(
        "/api/v1/avaliacoes",
        json={
            "cadastro": {
                "raio": cad["raio"],
                "espacamento": cad["espacamento"],
                "lamina_projeto": cad["lamina_projeto"],
            }
        },
    )
    assert created.status_code == 201
    avaliacao_id = created.json()["id"]

    updated = await client.put(
        f"/api/v1/avaliacoes/{avaliacao_id}/coletores",
        json={"coletores": data["coletores"]},
    )
    assert updated.status_code == 200
    assert len(updated.json()["coletores"]) == len(data["coletores"])

    uniformidade = await client.get(f"/api/v1/avaliacoes/{avaliacao_id}/uniformidade")
    assert uniformidade.status_code == 200
    body = uniformidade.json()
    ind = body["indicadores"]

    assert body["avaliacao_id"] == avaliacao_id
    assert ind["cuc"] == pytest.approx(esperado["cuc"], abs=0.01)
    assert ind["ud"] == pytest.approx(esperado["ud"], abs=0.01)
    assert ind["lmp"] == pytest.approx(esperado["lmp"], abs=0.01)
    assert ind["lp25"] == pytest.approx(esperado["lp25"], abs=0.01)
    assert ind["n"] == esperado["n"]
    assert body["classificacao"]["cuc"] == "Razoável"
    assert body["classificacao"]["ud"] == "Razoável"


@pytest.mark.asyncio
async def test_post_coletores_gerar(client):
    data = load_ensaio_exemplo()
    cad = data["cadastro"]

    created = await client.post(
        "/api/v1/avaliacoes",
        json={"cadastro": {"raio": cad["raio"], "espacamento": cad["espacamento"]}},
    )
    avaliacao_id = created.json()["id"]

    gerar = await client.post(f"/api/v1/avaliacoes/{avaliacao_id}/coletores/gerar")
    assert gerar.status_code == 200
    body = gerar.json()
    assert body["quantidade_gerada"] == 80
    assert len(body["avaliacao"]["coletores"]) == 80


@pytest.mark.asyncio
async def test_calculo_uniformidade_stateless(client):
    data = load_ensaio_exemplo()
    esperado = load_golden("uniformidade/indicadores.json")

    response = await client.post(
        "/api/v1/calculos/uniformidade",
        json={"coletores": data["coletores"]},
    )
    assert response.status_code == 200
    ind = response.json()["indicadores"]
    assert ind["cuc"] == pytest.approx(esperado["cuc"], abs=0.01)
    assert ind["n"] == esperado["n"]
