####################
#   PYTHON BASE    #
####################
FROM python:3.12.3-slim-bookworm as python-base

ENV PYTHONUNBUFFERED=1 \
    # pip
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # Poetry
    POETRY_VERSION=1.8.3 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    # never create virtual environment automaticly, only use env prepared by us
    POETRY_VIRTUALENVS_CREATE=false \
    # this is where our requirements + virtual environment will live
    VIRTUAL_ENV="/venv"

ENV PATH="$PATH:$POETRY_HOME/bin:$VIRTUAL_ENV/bin"

# prepare virtual env
RUN python -m venv $VIRTUAL_ENV

# working directory and Python path
WORKDIR /app
ENV PYTHONPATH="/app:$PYTHONPATH"


#####################
#   BUILDER BASE    #
#####################
FROM python-base as builder-base

RUN apt-get update && \
    apt-get install -y apt-transport-https gnupg ca-certificates build-essential vim curl && \
    apt-get clean

RUN --mount=type=cache,target=/root/.cache \
    curl -sSL https://install.python-poetry.org | python -

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN poetry lock

RUN poetry install --no-root --only main

# Put bootstrapping scripts here

#########################
#   DEVELOPMENT BASE    #
#########################
FROM builder-base as development
RUN --mount=type=cache,target=/root/.cache \
    poetry install --no-root --with test

ENV LOG_LEVEL=debug

COPY ocr/configs ocr/configs
COPY download_models.py download_models.py

RUN $VIRTUAL_ENV/bin/python download_models.py


########################
#   PRODUCTION BASE    #
########################
FROM builder-base as production

COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $VIRTUAL_ENV $VIRTUAL_ENV

ENV LOG_LEVEL=info
ENV PATH="$PATH:$POETRY_HOME/bin:$VIRTUAL_ENV/bin"

WORKDIR /app

COPY ocr/configs ocr/configs
COPY download_models.py download_models.py

RUN $VIRTUAL_ENV/bin/python download_models.py

EXPOSE 8000

ENTRYPOINT ["fastapi", "run", "app.py"]
