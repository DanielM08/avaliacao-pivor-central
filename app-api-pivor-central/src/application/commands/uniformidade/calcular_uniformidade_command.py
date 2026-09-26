from uuid import UUID

from application.mappers.uniformidade_mapper import resultado_uniformidade_to_response
from application.schemas import UniformidadeResponse
from domain.exceptions.domain_exception import DomainException, ExceptionType
from domain.ports.repositories.avaliacao_repository import AvaliacaoRepository
from domain.services.uniformidade_service import calcular_uniformidade


class CalcularUniformidadeCommand:
    def __init__(self, repo: AvaliacaoRepository) -> None:
        self._repo = repo

    async def execute(self, avaliacao_id: UUID) -> UniformidadeResponse:
        avaliacao = await self._repo.get_by_id(avaliacao_id)
        if not avaliacao:
            raise DomainException("Avaliação não encontrada", ExceptionType.NOT_FOUND)
        resultado = calcular_uniformidade(avaliacao.coletores)
        base = resultado_uniformidade_to_response(resultado)
        return UniformidadeResponse(avaliacao_id=avaliacao_id, **base.model_dump())
