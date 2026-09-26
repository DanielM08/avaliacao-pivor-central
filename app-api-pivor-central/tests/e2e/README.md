# Testes E2E (Fase 4+)

Esta pasta está reservada para testes **end-to-end** com stack completa:

- API rodando via `uvicorn` (ou container)
- PostgreSQL real (Docker Compose)
- Chamadas HTTP externas (`httpx` para `http://localhost:8000`)

Os testes atuais em `tests/integration/` usam `ASGITransport` (app in-process) e repositório **in-memory** — isso é integração, não E2E.

## Quando implementar

Após a [Fase 4 — Persistência](../../docs/FASES.md):

1. `docker compose up` (API + Postgres)
2. Fixtures de banco limpo por teste ou schema de teste
3. Arquivos `test_*.py` aqui com `@pytest.mark.e2e`
4. CI opcional: job separado `make test-e2e`

## Execução (futuro)

```bash
docker compose -f docker-compose.test.yml up -d
make test-e2e
```
