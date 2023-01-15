FROM python:3.10-slim as base

WORKDIR /

ARG HOMEDIR=/app

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PIPENV_HIDE_EMOJIS=true \
    PIPENV_COLORBLIND=true \
    PIPENV_NOSPIN=true \
    PIPENV_DOTENV_LOCATION=.env

RUN set -ex && \
    groupadd -r app && \
    useradd -r -s /bin/false -d ${HOMEDIR} -g app app

RUN set -ex && \
    apt-get update && \
    rm -rf /var/lib/apt/lists/*

COPY Pipfile Pipfile.lock ./

RUN pip install --no-cache-dir pipenv==2022.8.31 && \
    pipenv install --deploy --system --ignore-pipfile --dev

WORKDIR ${HOMEDIR}
RUN chown -R app:app ${HOMEDIR}
COPY --chown=app:app . ${HOMEDIR}
