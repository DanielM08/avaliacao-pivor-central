# Golden files

Saídas esperadas versionadas para detectar regressão no motor de uniformidade.

| Arquivo | Origem |
|---------|--------|
| `uniformidade/indicadores.json` | `calcular_uniformidade` (domínio) com `fixtures/ensaio_exemplo.json` |
| `uniformidade/calculo_stateless.json` | Resposta de `POST /api/v1/calculos/uniformidade` (indicadores + classificação) |

Entrada: apenas [`fixtures/ensaio_exemplo.json`](../fixtures/ensaio_exemplo.json) (coletores + cadastro).

## Atualizar após mudança intencional no motor

```bash
make golden-update
```

Revise o diff no git antes de commitar.
