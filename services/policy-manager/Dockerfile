FROM python:3.12-bookworm AS builder

WORKDIR /app

RUN pip install pipx
RUN pipx install poetry==1.8.3

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_VIRTUALENVS_OPTIONS_ALWAYS_COPY=1 \
    POETRY_VIRTUALENVS_OPTIONS_NO_PIP=1 \
    POETRY_INSTALLER_PARALLEL=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    PATH=/root/.local/bin:$PATH

COPY pyproject.toml poetry.lock ./

RUN --mount=type=cache,target=$POETRY_CACHE_DIR \
    poetry install --without dev --sync --no-root

###

FROM python:3.12-slim-bookworm AS runtime

WORKDIR /app

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY policy_manager ./policy_manager

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

ENTRYPOINT ["python", "-m", "policy_manager.main"]
