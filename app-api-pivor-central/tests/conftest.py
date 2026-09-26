import json
import sys
from pathlib import Path
from typing import Any

import pytest

TESTS_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = TESTS_ROOT.parent
SRC = PROJECT_ROOT / "src"
GOLDEN_DIR = TESTS_ROOT / "golden"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def golden_path(relative: str) -> Path:
    return GOLDEN_DIR / relative


def load_golden(relative: str) -> dict[str, Any]:
    return json.loads(golden_path(relative).read_text(encoding="utf-8"))


def _round_floats(value: Any, places: int) -> Any:
    if isinstance(value, float):
        return round(value, places)
    if isinstance(value, dict):
        return {k: _round_floats(v, places) for k, v in value.items()}
    if isinstance(value, list):
        return [_round_floats(v, places) for v in value]
    return value


def assert_matches_golden(actual: dict[str, Any], relative: str, *, float_places: int = 2) -> None:
    expected = load_golden(relative)
    assert _round_floats(actual, float_places) == _round_floats(expected, float_places)


def write_golden(relative: str, data: dict[str, Any]) -> None:
    path = golden_path(relative)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


@pytest.fixture
def golden_loader():
    return load_golden
