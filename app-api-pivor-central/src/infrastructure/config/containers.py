from dishka import Provider, Scope, provide

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
from domain.ports.repositories.avaliacao_repository import AvaliacaoRepository
from infrastructure.config.settings import Settings
from infrastructure.persistence.in_memory.avaliacao_repository import InMemoryAvaliacaoRepository


class AppProvider(Provider):
    @provide(scope=Scope.APP)
    def settings(self) -> Settings:
        return Settings()

    @provide(scope=Scope.APP)
    def avaliacao_repository(self) -> AvaliacaoRepository:
        return InMemoryAvaliacaoRepository()

    @provide(scope=Scope.REQUEST)
    def create_avaliacao(self, repo: AvaliacaoRepository) -> CreateAvaliacaoCommand:
        return CreateAvaliacaoCommand(repo)

    @provide(scope=Scope.REQUEST)
    def get_avaliacao(self, repo: AvaliacaoRepository) -> GetAvaliacaoCommand:
        return GetAvaliacaoCommand(repo)

    @provide(scope=Scope.REQUEST)
    def list_avaliacoes(self, repo: AvaliacaoRepository) -> ListAvaliacoesCommand:
        return ListAvaliacoesCommand(repo)

    @provide(scope=Scope.REQUEST)
    def patch_avaliacao(self, repo: AvaliacaoRepository) -> PatchAvaliacaoCommand:
        return PatchAvaliacaoCommand(repo)

    @provide(scope=Scope.REQUEST)
    def replace_coletores(self, repo: AvaliacaoRepository) -> ReplaceColetoresCommand:
        return ReplaceColetoresCommand(repo)

    @provide(scope=Scope.REQUEST)
    def calcular_uniformidade(self, repo: AvaliacaoRepository) -> CalcularUniformidadeCommand:
        return CalcularUniformidadeCommand(repo)

    @provide(scope=Scope.REQUEST)
    def calcular_uniformidade_stateless(self) -> CalcularUniformidadeStatelessCommand:
        return CalcularUniformidadeStatelessCommand()

    @provide(scope=Scope.REQUEST)
    def gerar_coletores(self, repo: AvaliacaoRepository) -> GerarColetoresCommand:
        return GerarColetoresCommand(repo)
