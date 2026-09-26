"""DTOs HTTP / aplicação (Pydantic v2)."""

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CanhaoOpcao(str, Enum):
    SIM = "Sim"
    NAO = "Não"


class AvaliacaoStatusSchema(str, Enum):
    rascunho = "rascunho"
    concluida = "concluida"


class CadastroPivoSchema(BaseModel):
    model_config = ConfigDict(extra="ignore")

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
    canhao: CanhaoOpcao | None = None


class ColetorSchema(BaseModel):
    si: int = Field(ge=1)
    dist: float | None = Field(default=None, ge=0)
    v1: float | None = Field(default=None, ge=0)
    v2: float | None = Field(default=None, ge=0)
    v3: float | None = Field(default=None, ge=0)
    v4: float | None = Field(default=None, ge=0)


class CreateAvaliacaoRequest(BaseModel):
    cadastro: CadastroPivoSchema
    coletores: list[ColetorSchema] = Field(default_factory=list)


class PatchAvaliacaoRequest(BaseModel):
    cadastro: CadastroPivoSchema | None = None
    status: AvaliacaoStatusSchema | None = None


class ReplaceColetoresRequest(BaseModel):
    coletores: list[ColetorSchema] = Field(min_length=1)


class CalculoUniformidadeRequest(BaseModel):
    coletores: list[ColetorSchema] = Field(min_length=1)


class ErrorResponse(BaseModel):
    type: str
    detail: str


class IndicadoresUniformidadeSchema(BaseModel):
    cuc: float
    ud: float
    lmp: float
    lp25: float
    n: int


class SerieUniformidadeItemSchema(BaseModel):
    si: int
    dist: float | None = None
    li: float


class ClassificacaoUniformidadeSchema(BaseModel):
    cuc: str | None = None
    ud: str | None = None


class UniformidadeCalculoResponse(BaseModel):
    indicadores: IndicadoresUniformidadeSchema
    serie: list[SerieUniformidadeItemSchema]
    classificacao: ClassificacaoUniformidadeSchema | None = None


class UniformidadeResponse(UniformidadeCalculoResponse):
    avaliacao_id: UUID


class AvaliacaoResponse(BaseModel):
    id: UUID
    cadastro: CadastroPivoSchema
    coletores: list[ColetorSchema]
    status: AvaliacaoStatusSchema
    coordenada_key: str
    created_at: datetime
    updated_at: datetime


class AvaliacaoListResponse(BaseModel):
    items: list[AvaliacaoResponse]
    total: int
    limit: int
    offset: int


class GerarColetoresResponse(BaseModel):
    avaliacao: AvaliacaoResponse
    quantidade_gerada: int
