FROM python:3.11-alpine

RUN apk add --no-cache --virtual \
        .build-deps \
        gcc \
        g++ \
        musl-dev \
        python3-dev \
        cython \
        libffi-dev \
        tzdata

ENV TZ America/Sao_Paulo

ADD requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /pylineup/
RUN addgroup -S celery && adduser -S celery -G celery
RUN chown -R celery:celery /pylineup

USER celery
WORKDIR /pylineup
