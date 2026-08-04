# Makefile for the {{ cookiecutter.course_short }} learner repo.
# Run from the repo root.

SHELL := /usr/bin/env bash
PY   := python{{ cookiecutter.python_version }}

.PHONY: help init journal gate progress test clean lint fmt

help: ## Show this help.
	@awk 'BEGIN {FS = ":.*##"; printf "Targets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  %-12s %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

init: ## Create venv and install dev deps.
	@test -d .venv || $(PY) -m venv .venv
	. .venv/bin/activate && pip install -U pip && \
		pip install -e ".[dev]"
	@echo "init done. Activate with: source .venv/bin/activate"

journal: ## Open the current week's journal entry in $EDITOR.
	@$(PY) scripts/new_week.py

gate: ## Run the milestone gate checker.
	@$(PY) scripts/milestone_gate.py

progress: ## Print weekly completion dashboard.
	@$(PY) scripts/progress.py

test: ## Run pytest across the engineering primitives.
	@$(PY) -m pytest 02_engineering_primitives -v

lint: ## Lint with ruff + mypy (if configured).
	@$(PY) -m ruff check . || true
	@$(PY) -m mypy 02_engineering_primitives || true

fmt: ## Auto-format with ruff.
	@$(PY) -m ruff format .

clean: ## Remove caches and venv.
	@rm -rf .pytest_cache .ruff_cache .mypy_cache .coverage htmlcov
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@echo "caches cleared (kept .venv)"