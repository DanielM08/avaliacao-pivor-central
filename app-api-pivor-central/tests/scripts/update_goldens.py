"""Regenera arquivos em tests/golden/. Uso: make golden-update"""

import json
import sys
from pathlib import Path


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(project_root / "src"))
    sys.path.insert(0, str(project_root))

    from application.mappers.uniformidade_mapper import resultado_uniformidade_to_response
    from domain.services.uniformidade_service import calcular_uniformidade
    from domain.value_objects.coletor import Coletor
    from tests.conftest import write_golden
    from tests.fixtures.loader import load_ensaio_exemplo

    data = load_ensaio_exemplo()
    coletores = [Coletor(**item) for item in data["coletores"]]
    resultado = calcular_uniformidade(coletores)
    ind = resultado.indicadores

    write_golden(
        "uniformidade/indicadores.json",
        {
            "cuc": round(ind.cuc, 2),
            "ud": round(ind.ud, 2),
            "lmp": round(ind.lmp, 2),
            "lp25": round(ind.lp25, 2),
            "n": ind.n,
        },
    )

    resp = resultado_uniformidade_to_response(resultado)
    payload = json.loads(resp.model_dump_json())
    write_golden(
        "uniformidade/calculo_stateless.json",
        {
            "indicadores": payload["indicadores"],
            "classificacao": payload["classificacao"],
        },
    )

    print("Golden files atualizados em tests/golden/uniformidade/")


if __name__ == "__main__":
    main()
