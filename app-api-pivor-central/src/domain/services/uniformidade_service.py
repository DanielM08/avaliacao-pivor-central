"""Motor de uniformidade — portado de calcUnif() e geração de coletores."""

from dataclasses import dataclass
import math

from domain.exceptions.domain_exception import DomainException, ExceptionType
from domain.value_objects.coletor import Coletor

AREA_COLETOR_CM2 = 78.54


@dataclass(frozen=True)
class SerieUniformidadeItem:
    si: int
    dist: float | None
    li: float


@dataclass(frozen=True)
class IndicadoresUniformidade:
    cuc: float
    ud: float
    lmp: float
    lp25: float
    n: int


@dataclass(frozen=True)
class ResultadoUniformidade:
    indicadores: IndicadoresUniformidade
    serie: list[SerieUniformidadeItem]


def classificar_cuc(cuc: float) -> str:
    if cuc >= 90:
        return "Excelente"
    if cuc >= 80:
        return "Bom"
    if cuc >= 70:
        return "Razoável"
    return "Baixo"


def classificar_ud(ud: float) -> str:
    if ud >= 84:
        return "Excelente"
    if ud >= 68:
        return "Bom"
    if ud >= 56:
        return "Razoável"
    return "Baixo"


def calcular_uniformidade(coletores: list[Coletor]) -> ResultadoUniformidade:
    validos: list[tuple[int, float | None, float]] = []
    for c in coletores:
        volumes = [v for v in (c.v1, c.v2, c.v3, c.v4) if v is not None]
        if not volumes:
            continue
        media = sum(volumes) / len(volumes)
        li = (media / AREA_COLETOR_CM2) * 10
        validos.append((c.si, c.dist, li))

    if not validos:
        raise DomainException(
            "Nenhum coletor com leitura válida para cálculo de uniformidade",
            ExceptionType.VALIDATION,
        )

    s_si = sum(si for si, _, _ in validos)
    lmp = sum(si * li for si, _, li in validos) / s_si
    cuc = (1 - sum(si * abs(li - lmp) for si, _, li in validos) / (lmp * s_si)) * 100
    laminas = sorted(li for _, _, li in validos)
    k = max(1, math.ceil(len(laminas) * 0.25))
    lp25 = sum(laminas[:k]) / k
    ud = (lp25 / lmp) * 100

    serie = [SerieUniformidadeItem(si=si, dist=dist, li=li) for si, dist, li in validos]
    indicadores = IndicadoresUniformidade(
        cuc=cuc,
        ud=ud,
        lmp=lmp,
        lp25=lp25,
        n=len(validos),
    )
    return ResultadoUniformidade(indicadores=indicadores, serie=serie)


def gerar_coletores(raio: float | None, espacamento: float | None) -> list[Coletor]:
    if raio is None or espacamento is None or espacamento <= 0:
        raise DomainException(
            "raio e espacamento devem ser informados e espacamento > 0",
            ExceptionType.BUSINESS_RULE,
        )
    n = math.floor(raio / espacamento)
    if n <= 0:
        raise DomainException(
            "Não foi possível gerar coletores: floor(raio/espacamento) = 0",
            ExceptionType.BUSINESS_RULE,
        )
    return [
        Coletor(
            si=i + 1,
            dist=round((i + 1) * espacamento, 3),
            v1=None,
            v2=None,
            v3=None,
            v4=None,
        )
        for i in range(n)
    ]
