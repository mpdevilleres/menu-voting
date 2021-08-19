FROM python:3.9-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    WORKDIR="/opt/src"

###############################################
# Builder Image
###############################################
FROM base AS builder

ENV POETRY_VERSION=1.1.6 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true

ENV PATH="$POETRY_HOME/bin:$PATH"

# System dependencies:
RUN apt-get update \
  && apt-get install -y build-essential python3-dev curl

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

WORKDIR $WORKDIR
COPY poetry.lock pyproject.toml README.md ./
COPY app ./app

# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN poetry install --no-dev

###############################################
# Runtime Image
###############################################
FROM base AS runtime
COPY --from=builder $WORKDIR/.venv $WORKDIR/.venv

ENV PATH="$WORKDIR/.venv/bin:$PATH"

WORKDIR $WORKDIR

RUN addgroup --system fastapi \
    && adduser --system --ingroup fastapi fastapi

COPY gunicorn_conf.py alembic.ini ./
COPY app ./app
COPY migrations ./migrations

RUN chown -R fastapi $WORKDIR

USER fastapi

CMD ["gunicorn", "-c", "gunicorn_conf.py", "app.server:app"]
