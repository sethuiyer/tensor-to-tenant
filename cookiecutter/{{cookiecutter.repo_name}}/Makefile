# Makefile for the {{ cookiecutter.course_short }} learner repo.
# Run from the repo root.

SHELL := /usr/bin/env bash
PY   := python{{ cookiecutter.python_version }}

.DEFAULT_GOAL := dispatch

.PHONY: dispatch help init journal week recovery remediate release badge forge design darbar auror gate progress test clean lint fmt

dispatch: ## Show help, or run `make week=14`, `make recovery=14`, `make remediate=18`, `make release=30`, `make badge=30`, `make forge=57`, `make design=54`, or `make darbar=42`.
	@if [ -n "$(week)" ]; then $(MAKE) --no-print-directory _week WEEK="$(week)"; \
	elif [ -n "$(recovery)" ]; then $(MAKE) --no-print-directory _recovery WEEK="$(recovery)"; \
	elif [ -n "$(remediate)" ]; then $(MAKE) --no-print-directory _remediate GATE="$(remediate)"; \
	elif [ -n "$(badge)" ]; then $(MAKE) --no-print-directory _badge WEEK="$(badge)"; \
	elif [ -n "$(forge)" ]; then $(MAKE) --no-print-directory _forge WEEK="$(forge)"; \
	elif [ -n "$(design)" ]; then $(MAKE) --no-print-directory _design WEEK="$(design)"; \
	elif [ -n "$(darbar)" ]; then $(MAKE) --no-print-directory _darbar PROBLEM="$(darbar)"; \
	elif [ "$(auror)" = "1" ] || [ "$(auror)" = "yes" ]; then $(MAKE) --no-print-directory _auror; \
	elif [ -n "$(release)" ]; then $(MAKE) --no-print-directory _release WEEK="$(release)"; \
	else $(MAKE) --no-print-directory help; fi

help: ## Show this help.
	@awk 'BEGIN {FS = ":.*##"; printf "Targets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  %-12s %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

init: ## Create venv and install dev deps.
	@test -d .venv || $(PY) -m venv .venv
	. .venv/bin/activate && pip install -U pip && \
		pip install -e ".[dev]"
	@echo "init done. Activate with: source .venv/bin/activate"

journal: ## Open the current week's journal entry in $EDITOR.
	@$(PY) scripts/new_week.py

week: ## Open a specific week: `make week=14`.
	@$(PY) scripts/new_week.py $(if $(WEEK),--week $(WEEK),)

_week:
	@$(PY) scripts/new_week.py --week "$(WEEK)"

recovery: ## Prepare a recovery plan after a week: `make recovery=14`.
	@$(PY) scripts/recovery.py --after-week "$(WEEK)"

_recovery:
	@$(PY) scripts/recovery.py --after-week "$(WEEK)"

remediate: ## Prepare remediation for a gate: `make remediate=18`.
	@$(PY) scripts/remediate.py --gate "$(GATE)"

_remediate:
	@$(PY) scripts/remediate.py --gate "$(GATE)"

release: ## Prepare a portfolio release: `make release=30`.
	@$(PY) scripts/release.py --week "$(WEEK)"

_release:
	@$(PY) scripts/release.py --week "$(WEEK)"

badge: ## Verify and award a portfolio badge: `make badge=30`.
	@$(PY) scripts/release.py --week "$(WEEK)" --check

_badge:
	@$(PY) scripts/release.py --week "$(WEEK)" --check

forge: ## Prepare a Forge artifact: `make forge=57`.
	@$(PY) scripts/forge.py --week "$(WEEK)"

_forge:
	@$(PY) scripts/forge.py --week "$(WEEK)"

design: ## Prepare a system-design artifact: `make design=54`.
	@$(PY) scripts/design.py --week "$(WEEK)"

_design:
	@$(PY) scripts/design.py --week "$(WEEK)"

darbar: ## Prepare Darbar evidence: `make darbar=42`.
	@$(PY) scripts/darbar.py --problem "$(PROBLEM)"

_darbar:
	@$(PY) scripts/darbar.py --problem "$(PROBLEM)"

auror: ## Verify the optional 548-problem Auror track: `make auror=1`.
	@$(PY) scripts/auror.py

_auror:
	@$(PY) scripts/auror.py

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
