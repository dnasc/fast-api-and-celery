# syntax=docker/dockerfile:1
FROM python:3.8 AS base

RUN addgroup --system app && adduser --system --group app

USER app
ENV PATH "$PATH:/home/app/.local/bin"

WORKDIR /code
COPY ./app /code/app

RUN pip install -U --upgrade pip


FROM base as nlp

COPY requirements-nlp.txt /code/requirements.txt
RUN pip install -U --no-cache-dir --upgrade -r requirements.txt
RUN python -m spacy download xx_ent_wiki_sm
RUN python -m spacy download pt_core_news_sm


FROM base as api

COPY requirements-api.txt /code/requirements.txt
RUN pip install -U --no-cache-dir --upgrade -r requirements.txt


FROM nlp as worker

COPY requirements-worker.txt /code/requirements.txt
RUN pip install -U --no-cache-dir --upgrade -r requirements.txt
