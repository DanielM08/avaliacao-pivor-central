from application.mappers.avaliacao_mapper import avaliacao_to_response
from application.schemas import AvaliacaoListResponse, AvaliacaoStatusSchema
from domain.entities.avaliacao import AvaliacaoStatus
from domain.ports.repositories.avaliacao_repository import AvaliacaoListFilter, AvaliacaoRepository


class ListAvaliacoesCommand:
    def __init__(self, repo: AvaliacaoRepository) -> None:
        self._repo = repo

    async def execute(
        self,
        coordenada: str | None,
        status: AvaliacaoStatusSchema | None,
        limit: int,
        offset: int,
    ) -> AvaliacaoListResponse:
        status_entity = AvaliacaoStatus(status.value) if status else None
        filtro = AvaliacaoListFilter(
            coordenada_key=coordenada,
            status=status_entity,
            limit=limit,
            offset=offset,
        )
        items, total = await self._repo.list(filtro)
        return AvaliacaoListResponse(
            items=[avaliacao_to_response(a) for a in items],
            total=total,
            limit=limit,
            offset=offset,
        )
