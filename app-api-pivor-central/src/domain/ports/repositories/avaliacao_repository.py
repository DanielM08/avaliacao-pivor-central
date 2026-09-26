from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.avaliacao import Avaliacao, AvaliacaoStatus


class AvaliacaoListFilter:
    def __init__(
        self,
        coordenada_key: str | None = None,
        status: AvaliacaoStatus | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> None:
        self.coordenada_key = coordenada_key
        self.status = status
        self.limit = limit
        self.offset = offset


class AvaliacaoRepository(ABC):
    @abstractmethod
    async def save(self, avaliacao: Avaliacao) -> Avaliacao: ...

    @abstractmethod
    async def get_by_id(self, avaliacao_id: UUID) -> Avaliacao | None: ...

    @abstractmethod
    async def list(self, filtro: AvaliacaoListFilter) -> tuple[list[Avaliacao], int]: ...
