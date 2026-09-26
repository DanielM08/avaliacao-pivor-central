from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Query, status

from application.commands.avaliacao.create_avaliacao_command import CreateAvaliacaoCommand
from application.commands.avaliacao.get_avaliacao_command import GetAvaliacaoCommand
from application.commands.avaliacao.list_avaliacoes_command import ListAvaliacoesCommand
from application.commands.avaliacao.patch_avaliacao_command import PatchAvaliacaoCommand
from application.commands.avaliacao.replace_coletores_command import ReplaceColetoresCommand
from application.commands.uniformidade.calcular_uniformidade_command import (
    CalcularUniformidadeCommand,
)
from application.commands.uniformidade.calcular_uniformidade_stateless_command import (
    CalcularUniformidadeStatelessCommand,
)
from application.commands.uniformidade.gerar_coletores_command import GerarColetoresCommand
from application.schemas import (
    AvaliacaoListResponse,
    AvaliacaoResponse,
    AvaliacaoStatusSchema,
    CalculoUniformidadeRequest,
    CreateAvaliacaoRequest,
    GerarColetoresResponse,
    PatchAvaliacaoRequest,
    ReplaceColetoresRequest,
    UniformidadeCalculoResponse,
    UniformidadeResponse,
)

router = APIRouter(prefix="/api/v1", tags=["avaliacoes"])


@router.get("/avaliacoes", response_model=AvaliacaoListResponse)
@inject
async def list_avaliacoes(
    command: FromDishka[ListAvaliacoesCommand],
    coordenada: str | None = Query(default=None),
    status: AvaliacaoStatusSchema | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> AvaliacaoListResponse:
    return await command.execute(coordenada, status, limit, offset)


@router.post("/avaliacoes", response_model=AvaliacaoResponse, status_code=status.HTTP_201_CREATED)
@inject
async def create_avaliacao(
    body: CreateAvaliacaoRequest,
    command: FromDishka[CreateAvaliacaoCommand],
) -> AvaliacaoResponse:
    return await command.execute(body)


@router.get("/avaliacoes/{avaliacao_id}", response_model=AvaliacaoResponse)
@inject
async def get_avaliacao(
    avaliacao_id: UUID,
    command: FromDishka[GetAvaliacaoCommand],
) -> AvaliacaoResponse:
    return await command.execute(avaliacao_id)


@router.patch("/avaliacoes/{avaliacao_id}", response_model=AvaliacaoResponse)
@inject
async def patch_avaliacao(
    avaliacao_id: UUID,
    body: PatchAvaliacaoRequest,
    command: FromDishka[PatchAvaliacaoCommand],
) -> AvaliacaoResponse:
    return await command.execute(avaliacao_id, body)


@router.put("/avaliacoes/{avaliacao_id}/coletores", response_model=AvaliacaoResponse)
@inject
async def replace_coletores(
    avaliacao_id: UUID,
    body: ReplaceColetoresRequest,
    command: FromDishka[ReplaceColetoresCommand],
) -> AvaliacaoResponse:
    return await command.execute(avaliacao_id, body)


@router.post(
    "/avaliacoes/{avaliacao_id}/coletores/gerar",
    response_model=GerarColetoresResponse,
)
@inject
async def gerar_coletores(
    avaliacao_id: UUID,
    command: FromDishka[GerarColetoresCommand],
) -> GerarColetoresResponse:
    return await command.execute(avaliacao_id)


@router.get(
    "/avaliacoes/{avaliacao_id}/uniformidade",
    response_model=UniformidadeResponse,
    tags=["uniformidade"],
)
@inject
async def calcular_uniformidade_avaliacao(
    avaliacao_id: UUID,
    command: FromDishka[CalcularUniformidadeCommand],
) -> UniformidadeResponse:
    return await command.execute(avaliacao_id)


@router.post(
    "/calculos/uniformidade",
    response_model=UniformidadeCalculoResponse,
    tags=["calculos"],
)
@inject
async def calcular_uniformidade_stateless(
    body: CalculoUniformidadeRequest,
    command: FromDishka[CalcularUniformidadeStatelessCommand],
) -> UniformidadeCalculoResponse:
    return await command.execute(body)
