# Base image with Poetry installed
FROM python:3.8 AS python-base
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
WORKDIR $PYSETUP_PATH
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-dev --no-root

# Stage 1: API Gateway Service
FROM python-base AS api_gateway
WORKDIR /app
COPY --from=python-base $PYSETUP_PATH $PYSETUP_PATH
COPY ./src/api_gateway.py .
CMD ["python", "api_gateway.py"]

# Stage 2: Image Processing Service
FROM python-base AS image_processing
WORKDIR /app
COPY --from=python-base $PYSETUP_PATH $PYSETUP_PATH
COPY ./src/image_processing_service.py .
CMD ["python", "image_processing_service.py"]

# Stage 3: Reconstruction Service
FROM python-base AS reconstruction
WORKDIR /app
COPY --from=python-base $PYSETUP_PATH $PYSETUP_PATH
COPY ./src/reconstruction_service.py .
CMD ["python", "reconstruction_service.py"]

# Stage 4: Visualization Service
FROM python-base AS visualization
WORKDIR /app
COPY --from=python-base $PYSETUP_PATH $PYSETUP_PATH
COPY ./src/visualization_service.py .
CMD ["python", "visualization_service.py"]
