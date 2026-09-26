from enum import Enum


class ExceptionType(str, Enum):
    NOT_FOUND = "NOT_FOUND"
    AUTHORIZATION = "AUTHORIZATION"
    VALIDATION = "VALIDATION"
    BUSINESS_RULE = "BUSINESS_RULE"
    INTERNAL = "INTERNAL"


class DomainException(RuntimeError):
    """Erro de domínio ou aplicação com tipo mapeável para HTTP."""

    def __init__(self, detail: str, type: ExceptionType) -> None:
        super().__init__(detail)
        self.detail = detail
        self.type = type
