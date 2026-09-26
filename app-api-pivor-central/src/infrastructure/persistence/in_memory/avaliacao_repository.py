from copy import deepcopy
from uuid import UUID

from domain.entities.avaliacao import Avaliacao
from domain.ports.repositories.avaliacao_repository import AvaliacaoListFilter, AvaliacaoRepository


class InMemoryAvaliacaoRepository(AvaliacaoRepository):
    def __init__(self) -> None:
        self._store: dict[UUID, Avaliacao] = {}

    async def save(self, avaliacao: Avaliacao) -> Avaliacao:
        self._store[avaliacao.id] = deepcopy(avaliacao)
        return deepcopy(avaliacao)

    async def get_by_id(self, avaliacao_id: UUID) -> Avaliacao | None:
        item = self._store.get(avaliacao_id)
        return deepcopy(item) if item else None

    async def list(self, filtro: AvaliacaoListFilter) -> tuple[list[Avaliacao], int]:
        items = list(self._store.values())
        if filtro.coordenada_key:
            items = [a for a in items if a.coordenada_key == filtro.coordenada_key]
        if filtro.status:
            items = [a for a in items if a.status == filtro.status]
        total = len(items)
        items.sort(key=lambda a: a.created_at, reverse=True)
        page = items[filtro.offset : filtro.offset + filtro.limit]
        return [deepcopy(a) for a in page], total
