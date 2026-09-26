import pytest

from domain.entities.avaliacao import CadastroPivo
from domain.services.coordenada_key import coordenada_key_from_cadastro, normalizar_texto_coordenada

pytestmark = pytest.mark.unit


def test_normalizar_texto_coordenada():
    assert normalizar_texto_coordenada("-10.5432, -46.4123") == "-10.5432,-46.4123"
    assert normalizar_texto_coordenada("") == ""


def test_coordenada_key_from_cadastro():
    cad = CadastroPivo(coordenadas="-10.5432, -46.4123")
    assert coordenada_key_from_cadastro(cad) == "-10.5432,-46.4123"
