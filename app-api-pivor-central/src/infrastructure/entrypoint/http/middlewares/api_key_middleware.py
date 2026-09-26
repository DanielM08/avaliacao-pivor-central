from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from domain.exceptions.domain_exception import ExceptionType
from infrastructure.config.settings import Settings

_PUBLIC_PATHS = {"/health", "/docs", "/redoc", "/openapi.json"}


class ApiKeyMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, settings: Settings) -> None:
        super().__init__(app)
        self._settings = settings

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.url.path in _PUBLIC_PATHS:
            return await call_next(request)

        api_key = request.headers.get("X-API-Key")
        if not api_key or api_key != self._settings.api_key:
            return JSONResponse(
                status_code=401,
                content={
                    "type": ExceptionType.AUTHORIZATION.value,
                    "detail": "API key inválida ou ausente",
                },
            )
        return await call_next(request)
