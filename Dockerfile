# Set a default Python version
ARG PYTHON_VERSION=3.11
#
#
#  Install General system packages stage
#
#
FROM python:${PYTHON_VERSION}-slim AS system-packages-stage

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN \
    --mount=type=cache,target=/var/cache/apt \
    apt-get update && \
    apt-get install -yqq libmagic1 && \
    apt-get install -yqq --no-install-recommends \
    make python3-psycopg2 nano curl supervisor wait-for-it && \
    apt-get autoremove && \
    apt-get clean
#
#
#  Install stage
#
#
FROM system-packages-stage AS compile-image
LABEL stage=compiler

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Pip Env-Variables
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PIP_DEFAULT_TIMEOUT=100
ENV PIP_NO_CACHE_DIR=1
ENV PIP_QUIET=1

RUN \
    --mount=type=cache,target=/var/cache/apt \
    apt-get install -yqq --no-install-recommends \
    build-essential gcc software-properties-common python3-psycopg2 libpq-dev python3-dev

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install -U --upgrade pip
RUN pip install wheel

COPY requirements/base.txt .
COPY requirements/production.txt .

RUN pip install -r ./production.txt

RUN find /opt/venv -type f -name "*.pyc" -delete 2>/dev/null
RUN find /opt/venv -type f -name "*.pyo" -delete 2>/dev/null
RUN find /opt/venv -type d -name "test" -name "tests" -delete 2>/dev/null


#
#
#  Build for development
#
#
FROM system-packages-stage AS build-dev

WORKDIR /app/

COPY --from=compile-image /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Supervisor config
RUN mkdir -p /var/log/supervisor

ADD ./.supervisord/supervisord.conf /etc/supervisor/supervisord.conf
ADD ./.supervisord/api.conf /etc/supervisor/conf.d/api.conf
ADD ./.supervisord/celery_worker.conf /etc/supervisor/conf.d/celery_worker.conf
ADD ./.supervisord/celery_beat.conf /etc/supervisor/conf.d/celery_beat.conf
ADD ./.supervisord/celery_flower.conf /etc/supervisor/conf.d/celery_flower.conf

RUN mkdir -p /app/logs/

# Add required scripts
COPY ./scripts /app/scripts
RUN sed -i 's/\r$//g' /app/scripts/*
RUN chmod -R +x /app/scripts/*

# For security and image performance, directories will be hardcoded

COPY apps /app/apps
COPY config /app/config
COPY staticfiles /app/staticfiles
COPY manage.py /app/manage.py
COPY makefile /app/makefile

ENTRYPOINT ["sh", "/app/scripts/entrypoint.sh"]

#
#
#  Build for production
#
#
FROM system-packages-stage AS build-prod

WORKDIR /app/

COPY --from=compile-image /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Supervisor config
RUN mkdir -p /var/log/supervisor

ADD ./.supervisord/supervisord.conf /etc/supervisor/supervisord.conf
ADD ./.supervisord/api.conf /etc/supervisor/conf.d/api.conf
ADD ./.supervisord/celery_worker.conf /etc/supervisor/conf.d/celery_worker.conf
ADD ./.supervisord/celery_beat.conf /etc/supervisor/conf.d/celery_beat.conf
ADD ./.supervisord/celery_flower.conf /etc/supervisor/conf.d/celery_flower.conf

RUN mkdir -p /app/logs/

# Add required scripts
COPY ./scripts /app/scripts
RUN sed -i 's/\r$//g' /app/scripts/*
RUN chmod -R +x /app/scripts/*

# For security and image performance, directories will be hardcoded
COPY apps /app/apps
COPY config /app/config
COPY staticfiles /app/staticfiles
COPY manage.py /app/manage.py
COPY makefile /app/makefile

ENTRYPOINT ["sh", "/app/scripts/entrypoint.sh"]
