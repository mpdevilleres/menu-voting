SHELL := /usr/bin/env bash

IMAGE := backend
VERSION := latest

.PHONY: download-poetry
download-poetry:
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

.PHONY: install
install: download-poetry
	poetry install

.PHONY: check-safety
check-safety:
	poetry check
	poetry run pip check
	poetry run safety check --full-report
	poetry run bandit -ll -r app/

.PHONY: check-style
check-style:
	poetry run flake8 app tests
	poetry run black --config pyproject.toml --diff --check ./
	poetry run isort --settings-path pyproject.toml --check-only app tests

.PHONY: apply-style
apply-style:
	poetry run isort --settings-path pyproject.toml app tests
	poetry run black --config pyproject.toml ./

.PHONY: lint
lint: check-safety check-style

.PHONY: test
test:
	poetry run alembic upgrade head
	poetry run pytest tests
	poetry run alembic downgrade base
