.PHONY: lint fix format check test test-unit test-integration test-golden golden-update serve

SRC = src tests

lint:
	uv run ruff check $(SRC)

format:
	uv run ruff format $(SRC)

fix: format
	uv run ruff check --fix $(SRC)

check: lint
	uv run pytest -q

test:
	uv run pytest

test-unit:
	uv run pytest tests/unit -m unit

test-integration:
	uv run pytest tests/integration -m integration

test-golden:
	uv run pytest -m golden

golden-update:
	uv run python tests/scripts/update_goldens.py

serve:
	uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000 --app-dir src
