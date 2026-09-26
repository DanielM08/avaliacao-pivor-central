import pytest

from domain.services.uniformidade_service import calcular_uniformidade, gerar_coletores
from domain.value_objects.coletor import Coletor
from tests.conftest import load_golden
from tests.fixtures.loader import load_ensaio_exemplo

pytestmark = pytest.mark.unit


def _coletores_from_fixture() -> list[Coletor]:
    data = load_ensaio_exemplo()
    return [Coletor(**item) for item in data["coletores"]]


def test_calcular_uniformidade_ensaio_exemplo_regressao():
    esperado = load_golden("uniformidade/indicadores.json")
    resultado = calcular_uniformidade(_coletores_from_fixture())
    ind = resultado.indicadores

    assert ind.cuc == pytest.approx(esperado["cuc"], abs=0.01)
    assert ind.ud == pytest.approx(esperado["ud"], abs=0.01)
    assert ind.lmp == pytest.approx(esperado["lmp"], abs=0.01)
    assert ind.lp25 == pytest.approx(esperado["lp25"], abs=0.01)
    assert ind.n == esperado["n"]
    assert len(resultado.serie) == esperado["n"]


def test_gerar_coletores_raio_400_espacamento_5():
    data = load_ensaio_exemplo()
    cad = data["cadastro"]
    coletores = gerar_coletores(cad["raio"], cad["espacamento"])

    assert len(coletores) == 80
    assert coletores[0].si == 1 and coletores[0].dist == 5.0
    assert coletores[-1].si == 80 and coletores[-1].dist == 400.0
    assert all(c.v1 is None for c in coletores)
