from uuid import uuid4

from application.helpers.datetime import utc_now
from application.mappers.avaliacao_mapper import avaliacao_to_response
from application.mappers.cadastro_mapper import cadastro_schema_to_entity
from application.mappers.coletor_mapper import coletor_schema_to_entity
from application.schemas import AvaliacaoResponse, CreateAvaliacaoRequest
from domain.entities.avaliacao import Avaliacao, AvaliacaoStatus
from domain.ports.repositories.avaliacao_repository import AvaliacaoRepository
from domain.services.coordenada_key import coordenada_key_from_cadastro


class CreateAvaliacaoCommand:
    def __init__(self, repo: AvaliacaoRepository) -> None:
        self._repo = repo

    async def execute(self, body: CreateAvaliacaoRequest) -> AvaliacaoResponse:
        cadastro = cadastro_schema_to_entity(body.cadastro)
        now = utc_now()
        avaliacao = Avaliacao(
            id=uuid4(),
            cadastro=cadastro,
            coletores=[coletor_schema_to_entity(c) for c in body.coletores],
            status=AvaliacaoStatus.RASCUNHO,
            coordenada_key=coordenada_key_from_cadastro(cadastro),
            created_at=now,
            updated_at=now,
        )
        saved = await self._repo.save(avaliacao)
        return avaliacao_to_response(saved)
