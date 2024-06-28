FROM python:3.12.4-slim
ENV PYTHONUNBUFFERED=1

ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_CACHE_DIR='/var/cache/pypoetry'

# System deps:
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    bash \
    build-essential \
    curl \
    gettext \
    git \
    libpq-dev \
    wget \
    # Cleaning cache:
    && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/* \
    && pip install "poetry==1.8.3" && poetry --version

RUN mkdir /lunchlog
WORKDIR /lunchlog
ADD pyproject.toml poetry.lock /lunchlog/
RUN poetry install
ADD . /lunchlog/
