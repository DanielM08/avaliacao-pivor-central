from application.mappers.coletor_mapper import coletor_schema_to_entity
from application.mappers.uniformidade_mapper import resultado_uniformidade_to_response
from application.schemas import CalculoUniformidadeRequest, UniformidadeCalculoResponse
from domain.services.uniformidade_service import calcular_uniformidade


class CalcularUniformidadeStatelessCommand:
    async def execute(self, body: CalculoUniformidadeRequest) -> UniformidadeCalculoResponse:
        coletores = [coletor_schema_to_entity(c) for c in body.coletores]
        resultado = calcular_uniformidade(coletores)
        return resultado_uniformidade_to_response(resultado)
