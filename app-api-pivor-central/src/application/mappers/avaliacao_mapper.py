from application.mappers.cadastro_mapper import cadastro_entity_to_schema
from application.mappers.coletor_mapper import coletor_entity_to_schema
from application.schemas import AvaliacaoResponse, AvaliacaoStatusSchema
from domain.entities.avaliacao import Avaliacao


def avaliacao_to_response(avaliacao: Avaliacao) -> AvaliacaoResponse:
    return AvaliacaoResponse(
        id=avaliacao.id,
        cadastro=cadastro_entity_to_schema(avaliacao.cadastro),
        coletores=[coletor_entity_to_schema(c) for c in avaliacao.coletores],
        status=AvaliacaoStatusSchema(avaliacao.status.value),
        coordenada_key=avaliacao.coordenada_key,
        created_at=avaliacao.created_at,
        updated_at=avaliacao.updated_at,
    )
