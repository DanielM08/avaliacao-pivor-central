from contextlib import asynccontextmanager

from dishka import make_async_container
from dishka.integrations.fastapi import FastapiProvider, setup_dishka
from fastapi import FastAPI

from infrastructure.config.containers import AppProvider
from infrastructure.config.settings import Settings
from infrastructure.entrypoint.http.middlewares.api_key_middleware import ApiKeyMiddleware
from infrastructure.entrypoint.http.middlewares.exception_middleware import ExceptionMiddleware
from infrastructure.entrypoint.http.routes.avaliacao_routes import router as avaliacao_router
from infrastructure.entrypoint.http.routes.health_routes import router as health_router


def create_app() -> FastAPI:
    settings = Settings()
    container = make_async_container(AppProvider(), FastapiProvider())

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        yield
        await container.close()

    app = FastAPI(
        title="API Avaliação de Pivô Central",
        version="1.0.0",
        lifespan=lifespan,
    )

    setup_dishka(container=container, app=app)

    app.add_middleware(ExceptionMiddleware)
    app.add_middleware(ApiKeyMiddleware, settings=settings)

    app.include_router(health_router)
    app.include_router(avaliacao_router)

    return app


app = create_app()
