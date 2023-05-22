FROM python:3.9-slim-bullseye AS parent
MAINTAINER CS LGBTQ+
# https://python-poetry.org/docs#ci-recommendations
ENV POETRY_VERSION=1.4.0
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv

# Tell Poetry where to place its cache and virtual environment
ENV POETRY_CACHE_DIR=/opt/.cache

# Create stage for Poetry installation
FROM parent as poetry-base

# Creating a virtual environment just for poetry and install it with pip
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Create a new stage from the base python image
FROM parent as python-app

# Copy Poetry to app image
COPY --from=poetry-base ${POETRY_VENV} ${POETRY_VENV}

# Add Poetry to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

COPY ./poetry.lock ./pyproject.toml /
RUN poetry install --only main

COPY mentor_match_web/app /app
COPY ./.bumpversion.cfg /.bumpversion.cfg

FROM python-app AS web
CMD ["poetry", "run", "gunicorn", "app:create_app()", "-b 0.0.0.0:80"]

FROM python-app AS worker
CMD poetry run celery --app=app.extensions.celery_app worker --loglevel=info
