# API — Avaliação de Pivô Central

API Python (FastAPI + Clean Architecture) para avaliações de pivô central.

Contrato: [`../docs/openapi.yaml`](../docs/openapi.yaml)  
Regras de negócio: [`../docs/regras-negocio.md`](../docs/regras-negocio.md)  
Fases e pendências: [`../docs/FASES.md`](../docs/FASES.md)

## Requisitos

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

## Configuração

```bash
cd app-api-pivor-central
uv sync
cp .env.example .env
```

## Executar

```bash
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000 --app-dir src
```

Documentação interativa: http://localhost:8000/docs

## Autenticação

Envie o header `X-API-Key` com o valor de `API_KEY` do `.env` (exceto em `GET /health`).

## Testes e lint

```bash
make test              # suíte completa
make test-unit         # domínio (tests/unit espelha src/)
make test-integration  # API ASGI (tests/integration)
make test-golden       # regressão vs tests/golden/
make golden-update     # regenerar arquivos golden
make lint              # ruff check
make fix               # ruff format + ruff check --fix
make check             # lint + testes
```

Detalhes: [`tests/golden/README.md`](tests/golden/README.md), [`tests/e2e/README.md`](tests/e2e/README.md).
