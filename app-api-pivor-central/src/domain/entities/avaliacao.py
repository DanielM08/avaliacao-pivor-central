from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from uuid import UUID

from domain.value_objects.coletor import Coletor


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class AvaliacaoStatus(str, Enum):
    RASCUNHO = "rascunho"
    CONCLUIDA = "concluida"


@dataclass
class CadastroPivo:
    empresa: str | None = None
    proprietario: str | None = None
    fazenda: str | None = None
    cidade: str | None = None
    estado: str | None = None
    coordenadas: str | None = None
    comp: float | None = None
    raio: float | None = None
    espacamento: float | None = None
    vazao: float | None = None
    vel: float | None = None
    pressao: float | None = None
    lamina_projeto: float | None = None
    canhao: str | None = None  # "Sim" | "Não"


@dataclass
class Avaliacao:
    id: UUID
    cadastro: CadastroPivo
    coletores: list[Coletor] = field(default_factory=list)
    status: AvaliacaoStatus = AvaliacaoStatus.RASCUNHO
    coordenada_key: str = ""
    created_at: datetime = field(default_factory=_utc_now)
    updated_at: datetime = field(default_factory=_utc_now)
