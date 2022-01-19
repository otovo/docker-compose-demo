FROM python:3.10-slim as base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PYTHONPATH=/app

# Install required OS-level dependencies
RUN apt-get update  \
    && apt-get install --no-install-recommends -y curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | POETRY_HOME=/opt/poetry python  \
    && cd /usr/local/bin  \
    && ln -s /opt/poetry/bin/poetry  \
    && poetry config virtualenvs.create false

# Set workdir
WORKDIR /app

# Upgrade pip and build tools
RUN pip install pip wheel setuptools --user --upgrade

#: Everything above this line should probably live in a remote base image, in a
#: real project, since curl and poetry versions don't change often. By putting
#: it in a base image, you can skip the extra steps when building your primary image

FROM base as dependencies

COPY poetry.lock pyproject.toml ./

# Install dependencies
RUN poetry install --no-dev --no-root

# Copy relevant files
COPY ./scripts/entrypoint.sh /app/entrypoint.sh
COPY ./scripts/start.sh /app/start.sh
COPY ./gunicorn.conf.py /app/gunicorn.conf.py

RUN chmod +x entrypoint.sh && chmod +x start.sh
RUN useradd -m myuser
USER myuser:myuser

ENTRYPOINT  ["bash", "/app/entrypoint.sh"]

FROM dependencies as web

CMD [ "/app/start.sh", "web" ]

FROM dependencies as worker

CMD [ "/app/start.sh", "worker" ]
