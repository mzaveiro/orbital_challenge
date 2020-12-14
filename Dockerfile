FROM python:3.8-slim

# same as running python with "-u"
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    # paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

RUN set -eux; \
	apt-get update; \
	apt-get install -y --no-install-recommends \
    curl \
	; \
	rm -rf /var/lib/apt/lists/*

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

ARG HOST_UID=${HOST_UID:-1000}
ARG HOST_USER=${HOST_USER:-nodummy}
ARG PROJECT_NAME=${PROJECT_NAME}

RUN set -xe; \
    [ "${HOST_USER}" = "root" ] || \
    (adduser --home /home/${HOST_USER} --disabled-password --uid ${HOST_UID} --gecos ${HOST_USER} ${HOST_USER} \
    && chown -R "${HOST_UID}:${HOST_UID}" /home/${HOST_USER})

# copy project requirement files here to ensure they will be cached.
# PYSETUP_PATH var is set on the base image
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

# install dependencies
RUN poetry install --no-dev

# Prepare workspace
USER ${HOST_USER}
WORKDIR /home/${HOST_USER}

# Copy code
COPY . .
