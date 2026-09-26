import json
from pathlib import Path
from typing import Any

FIXTURE_PATH = Path(__file__).parent / "ensaio_exemplo.json"


def load_ensaio_exemplo() -> dict[str, Any]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
