from uuid import UUID

from application.helpers.datetime import utc_now
from application.mappers.avaliacao_mapper import avaliacao_to_response
from application.mappers.cadastro_mapper import cadastro_entity_to_schema, cadastro_schema_to_entity
from application.schemas import AvaliacaoResponse, PatchAvaliacaoRequest
from domain.entities.avaliacao import AvaliacaoStatus
from domain.exceptions.domain_exception import DomainException, ExceptionType
from domain.ports.repositories.avaliacao_repository import AvaliacaoRepository
from domain.services.coordenada_key import coordenada_key_from_cadastro


class PatchAvaliacaoCommand:
    def __init__(self, repo: AvaliacaoRepository) -> None:
        self._repo = repo

    async def execute(self, avaliacao_id: UUID, body: PatchAvaliacaoRequest) -> AvaliacaoResponse:
        avaliacao = await self._repo.get_by_id(avaliacao_id)
        if not avaliacao:
            raise DomainException("Avaliação não encontrada", ExceptionType.NOT_FOUND)

        if body.cadastro is not None:
            atual = cadastro_entity_to_schema(avaliacao.cadastro)
            merged = atual.model_copy(update=body.cadastro.model_dump(exclude_unset=True))
            avaliacao.cadastro = cadastro_schema_to_entity(merged)
            avaliacao.coordenada_key = coordenada_key_from_cadastro(avaliacao.cadastro)

        if body.status is not None:
            avaliacao.status = AvaliacaoStatus(body.status.value)

        avaliacao.updated_at = utc_now()
        saved = await self._repo.save(avaliacao)
        return avaliacao_to_response(saved)
