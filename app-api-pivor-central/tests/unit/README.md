# Testes unitários

A pasta espelha a estrutura de [`src/`](../src/): o caminho do teste indica o módulo testado.

| Teste | Módulo em `src/` |
|-------|------------------|
| `domain/services/test_uniformidade_service.py` | `domain/services/uniformidade_service.py` |
| `domain/services/test_uniformidade_golden.py` | `domain/services/uniformidade_service.py` (golden) |
| `domain/services/test_coordenada_key.py` | `domain/services/coordenada_key.py` |

Ao adicionar código em `src/application/commands/...`, crie `tests/unit/application/commands/...` com o mesmo layout.
