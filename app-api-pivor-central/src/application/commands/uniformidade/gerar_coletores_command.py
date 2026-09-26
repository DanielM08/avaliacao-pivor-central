from uuid import UUID

from application.helpers.datetime import utc_now
from application.mappers.avaliacao_mapper import avaliacao_to_response
from application.schemas import GerarColetoresResponse
from domain.exceptions.domain_exception import DomainException, ExceptionType
from domain.ports.repositories.avaliacao_repository import AvaliacaoRepository
from domain.services.uniformidade_service import gerar_coletores


class GerarColetoresCommand:
    def __init__(self, repo: AvaliacaoRepository) -> None:
        self._repo = repo

    async def execute(self, avaliacao_id: UUID) -> GerarColetoresResponse:
        avaliacao = await self._repo.get_by_id(avaliacao_id)
        if not avaliacao:
            raise DomainException("Avaliação não encontrada", ExceptionType.NOT_FOUND)
        novos = gerar_coletores(avaliacao.cadastro.raio, avaliacao.cadastro.espacamento)
        avaliacao.coletores = novos
        avaliacao.updated_at = utc_now()
        saved = await self._repo.save(avaliacao)
        return GerarColetoresResponse(
            avaliacao=avaliacao_to_response(saved),
            quantidade_gerada=len(novos),
        )
