#Multistage build
FROM python:3.10.11-buster as builder
#install and configure poetry envs
RUN pip install poetry==1.8.3

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

#Copy poetry requirements
WORKDIR /app
COPY pyproject.toml poetry.lock ./
#install requirements
RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

#Runtime with venv
FROM python:3.10.11-slim-buster as runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

#Copy venv
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

#Copy source code
COPY src /app/src
COPY main.py /app

#Run bot
ENTRYPOINT ["python", "/app/main.py"]