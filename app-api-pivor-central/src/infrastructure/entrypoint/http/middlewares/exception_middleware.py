from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from domain.exceptions.domain_exception import DomainException, ExceptionType

_STATUS_MAP = {
    ExceptionType.NOT_FOUND: 404,
    ExceptionType.AUTHORIZATION: 401,
    ExceptionType.VALIDATION: 422,
    ExceptionType.BUSINESS_RULE: 400,
    ExceptionType.INTERNAL: 500,
}


class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            return await call_next(request)
        except DomainException as exc:
            status = _STATUS_MAP.get(exc.type, 500)
            return JSONResponse(
                status_code=status,
                content={"type": exc.type.value, "detail": exc.detail},
            )
        except Exception:
            return JSONResponse(
                status_code=500,
                content={
                    "type": ExceptionType.INTERNAL.value,
                    "detail": "Erro interno do servidor",
                },
            )
