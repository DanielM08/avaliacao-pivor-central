from uuid import UUID

from application.mappers.avaliacao_mapper import avaliacao_to_response
from application.schemas import AvaliacaoResponse
from domain.exceptions.domain_exception import DomainException, ExceptionType
from domain.ports.repositories.avaliacao_repository import AvaliacaoRepository


class GetAvaliacaoCommand:
    def __init__(self, repo: AvaliacaoRepository) -> None:
        self._repo = repo

    async def execute(self, avaliacao_id: UUID) -> AvaliacaoResponse:
        avaliacao = await self._repo.get_by_id(avaliacao_id)
        if not avaliacao:
            raise DomainException("Avaliação não encontrada", ExceptionType.NOT_FOUND)
        return avaliacao_to_response(avaliacao)
