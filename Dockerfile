# 0fficial base image
FROM python:3.11.3 as BASE
ENV VIRTUAL_ENV=/venv \
	PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	POETRY_VERSION=1.4.2

COPY poetry.lock pyproject.toml ./

RUN pip install "poetry==$POETRY_VERSION"
RUN python3 -m venv $VIRTUAL_ENV

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN poetry install --no-interaction --no-ansi --only main --no-root

FROM python:3.11.3-slim-buster

## Need this part b/c the debian package for postgres isn’t updated yet and won’t currently work with arm64 architectures. https://stackoverflow.com/a/70167233
# https://www.psycopg.org/docs/install.html#build-prerequisites
# https://www.psycopg.org/docs/install.html#psycopg-vs-psycopg-binary

RUN apt-get update -y && apt-get upgrade -y
RUN apt install -y python3-dev \
	libpq-dev

ENV VIRTUAL_ENV=/venv \
	PYTHONUNBUFFERED=1

COPY --from=BASE /venv /venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /usr/src/app

# copy project
COPY company_management/ company_management/
COPY manage.py manage.py

CMD []
