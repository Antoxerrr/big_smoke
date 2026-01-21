FROM python:3.12-slim

ENV PROJECT_ROOT=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR $PROJECT_ROOT

RUN apt-get update \
    && apt-get install -y --no-install-recommends postgresql-client \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip wheel \
    && pip install poetry

COPY pyproject.toml poetry.lock $PROJECT_ROOT/

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi --only main

COPY . $PROJECT_ROOT

CMD ["sh", "./docker-entrypoint.sh"]
