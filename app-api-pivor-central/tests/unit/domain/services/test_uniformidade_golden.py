from dataclasses import asdict

import pytest

from domain.services.uniformidade_service import calcular_uniformidade
from domain.value_objects.coletor import Coletor
from tests.conftest import assert_matches_golden
from tests.fixtures.loader import load_ensaio_exemplo

pytestmark = [pytest.mark.unit, pytest.mark.golden]


def test_uniformidade_indicadores_matches_golden_file():
    data = load_ensaio_exemplo()
    coletores = [Coletor(**item) for item in data["coletores"]]
    resultado = calcular_uniformidade(coletores)
    actual = asdict(resultado.indicadores)
    assert_matches_golden(actual, "uniformidade/indicadores.json")
