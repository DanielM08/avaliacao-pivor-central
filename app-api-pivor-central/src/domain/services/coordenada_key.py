"""Geração da chave de coordenada para histórico (equivalente a normCoord no front)."""

import re

from domain.entities.avaliacao import CadastroPivo


def normalizar_texto_coordenada(texto: str | None) -> str:
    if not texto:
        return ""
    nums = re.findall(r"-?\d+[.,]?\d*", str(texto))
    if len(nums) >= 2:
        lat = float(nums[0].replace(",", "."))
        lng = float(nums[1].replace(",", "."))
        return f"{lat:.4f},{lng:.4f}"
    return str(texto).strip()


def coordenada_key_from_cadastro(cadastro: CadastroPivo) -> str:
    return normalizar_texto_coordenada(cadastro.coordenadas)
