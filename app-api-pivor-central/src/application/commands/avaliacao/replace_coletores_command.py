from uuid import UUID

from application.helpers.datetime import utc_now
from application.mappers.avaliacao_mapper import avaliacao_to_response
from application.mappers.coletor_mapper import coletor_schema_to_entity
from application.schemas import AvaliacaoResponse, ReplaceColetoresRequest
from domain.exceptions.domain_exception import DomainException, ExceptionType
from domain.ports.repositories.avaliacao_repository import AvaliacaoRepository


class ReplaceColetoresCommand:
    def __init__(self, repo: AvaliacaoRepository) -> None:
        self._repo = repo

    async def execute(self, avaliacao_id: UUID, body: ReplaceColetoresRequest) -> AvaliacaoResponse:
        avaliacao = await self._repo.get_by_id(avaliacao_id)
        if not avaliacao:
            raise DomainException("Avaliação não encontrada", ExceptionType.NOT_FOUND)
        avaliacao.coletores = [coletor_schema_to_entity(c) for c in body.coletores]
        avaliacao.updated_at = utc_now()
        saved = await self._repo.save(avaliacao)
        return avaliacao_to_response(saved)
