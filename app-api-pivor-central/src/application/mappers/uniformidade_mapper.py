from application.schemas import (
    ClassificacaoUniformidadeSchema,
    IndicadoresUniformidadeSchema,
    SerieUniformidadeItemSchema,
    UniformidadeCalculoResponse,
)
from domain.services.uniformidade_service import (
    ResultadoUniformidade,
    classificar_cuc,
    classificar_ud,
)


def resultado_uniformidade_to_response(
    resultado: ResultadoUniformidade,
) -> UniformidadeCalculoResponse:
    ind = resultado.indicadores
    return UniformidadeCalculoResponse(
        indicadores=IndicadoresUniformidadeSchema(
            cuc=ind.cuc,
            ud=ind.ud,
            lmp=ind.lmp,
            lp25=ind.lp25,
            n=ind.n,
        ),
        serie=[SerieUniformidadeItemSchema(si=s.si, dist=s.dist, li=s.li) for s in resultado.serie],
        classificacao=ClassificacaoUniformidadeSchema(
            cuc=classificar_cuc(ind.cuc),
            ud=classificar_ud(ind.ud),
        ),
    )
